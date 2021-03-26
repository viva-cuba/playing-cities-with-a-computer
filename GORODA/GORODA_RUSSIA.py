# viva-cuba1990@yandex.ru

# Python 3.9.1 64-bit
# за основу взял код отсюда https://github.com/alexsok-bit/citygame/blob/master/main.py спасибо
# добавил голосовое управление
# выход из игры голосовой командой "ты выиграла"
# голосовой вызов помощи с названием городов на нужную букву. если не знаешь город на последнюю буквы сказанную компом просто скажи "звонок другу" все города начинающиеся с этой буквы выводится в консоль
# файл txt с Российскими городами
# звуковой сигнал для удобства, чтобы знать когда комп вас слушает

# добавил себе в голосой помощник, прикольно с компом играть. только он всегда выигрывает, поэтому добавил помощь




from gtts import gTTS
import playsound
import speech_recognition as sr
import os
import time
import random
from itertools import cycle



def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        os.startfile('apple.mp3')
        print("слушаю тебя:")
        
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("вы сказали: "+our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError as e:
        return "ошибка"

def do_tris_command(message):
    message = message.lower()

    

check_list = []
   
    
def normalize_city_name(name):
    return name.strip().lower().replace('ё', 'е')


def check_point(fun):
    check_list.append(fun)
    return fun


@check_point
def is_city_startswith_char(city, char, **kwargs):
    if char is None or city.startswith(char):
        return True
    else:
        say_message(f'Город должен начинаться с буквы {char.capitalize()}.')
        return False


@check_point
def is_non_cached(city, cache, **kwargs):
    if city not in cache:
        return True
    else:
        say_message("Этот город уже был назван.")
        return False


@check_point
def is_available(city, cities, **kwargs):
    if city in cities:
        return True
    else:
        say_message("Я такого города не знаю.")
        return False


def move_to_cache(city, cities, cache):
    # убираем из списка доступных
    cities.remove(city)
    # перекидываем город в кэш
    cache.add(city)


def get_next_char(city):
    wrong_char = ("Ъ", "ь", "ы", "й")
    # выбираем букву для следующего города
    for char in city[::-1]:
        if char in wrong_char:
            continue
        else:
            break
    else:
        raise RuntimeError
    return char


def user_point(char):
    user_say = listen_command()
    
    if user_say == 'Звонок другу':
        help = char
        # say_message('какая буква')
        # help = listen_command()
        lst = open('cities.txt', 'r', -1, 'utf-8')
        fil = lst.read()
        lists = fil.lower().split()
        print(list(filter(lambda x: x.startswith(help), lists)))

    if user_say == 'ты выиграла':
            say_message('ха-ха-ха, учи города и заходи ещё')
            exit()

    city = normalize_city_name(user_say)
    kw = {"char": char, "cache": cache, "cities": cities}
    if not all(x(city, **kw) for x in check_list):
        return user_point(char)
    return city


def ai_point(char):
    # выбираем город
    for city in cities:
        if city.startswith(char):
            break
    else:
        raise SystemExit("Вы победили!")
    say_message(city)
    return city


def main():
    char = None
    for point in cycle((user_point, ai_point)):
        next_city = point(char)
        move_to_cache(next_city, cities, cache)
        char = get_next_char(next_city)

def say_message(message):
    
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_" + \
    str(time.time())+"_"+str(random.randint(0, 1000))+".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    os.remove(file_voice_name)
    print("Голосовой ассистент: "+message)

    

if __name__ == '__main__':
    say_message("привет! называй город первый. и сюрприз  только Российские города")
    
    cache = set()
    # вот тут есть куча варинтов развания собыйти.
    cities = {normalize_city_name(x) for x in open("cities.txt", "r", -1, 'utf-8').readlines() if x.strip()}
    main()
    
    while True:
        command = listen_command()  # слушает команду
        do_tris_command(command)
