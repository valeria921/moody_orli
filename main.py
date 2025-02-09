from tkinter import *
import random
import os

window = Tk()
window.title("Moody Orli")

app_elements = {
    "flags": {
        "en": None,
        "pl": None,
        "ru": None,
    },
    "buttons": {
        "back": None,
        "icon": None,
    },
    "images": {
        "start_img": None,
        "question_img": None,
        "current_image": None,
        "current_image_screen": None,
    },
    "app_logic": {
        "language": None,
        "image_description": None,
        "previous_screen": None,
    },
    "phrases": {
        "en":[],
        "pl":[],
        "ru":[],
    },
    "widgets_list": [],
}

question_phrase = {
    "en": "↘️ Press to know ↙️",
    "pl": "↘️ Naciśnij i dowiedz się ↙️",
    "ru": "↘️ Нажми и узнай ↙️",
}

description_phrase = {
    "en": "Today you are",
    "pl": "Dzisiaj jesteś",
    "ru": "Сегодня ты",
}

with open("image_description_en.txt", "r") as file:
    app_elements["phrases"]["en"] = [line.strip() for line in file.readlines()]

with open("image_description_pl.txt", "r") as file:
    app_elements["phrases"]["pl"] = [line.strip() for line in file.readlines()]

with open("image_description_ru.txt", "r") as file:
    app_elements["phrases"]["ru"] = [line.strip() for line in file.readlines()]

def start():
    widget_list = app_elements["widgets_list"]

    app_elements["images"]["start_img"] = PhotoImage(file="ui/start.png")
    start_image = canvas.create_image(250, 280, image=app_elements["images"]["start_img"], anchor="center")
    widget_list.append(start_image)

    image_frame = canvas.create_rectangle(50, 30, 450, 530, outline="#002352", width=2)
    widget_list.append(image_frame)

    flags = ["en", "pl", "ru"]
    positions = [120, 250, 380]
    texts = ["English", "Polski", "Русский"]
    commands = [app_en, app_pl, app_ru]

    for i, lang in enumerate(flags):
        app_elements["flags"][lang] = PhotoImage(file=f"ui/flag_{lang}.png")
        button = Button(image=app_elements["flags"][lang], highlightthickness=0, borderwidth=1, command=commands[i])
        widget_list.append(canvas.create_window(positions[i], 625, window=button))
        label = Label(text=texts[i], font=("Courier New", 20, "bold"), fg="#002352", bg="#FFEDF2")
        label.place(x=positions[i], y=680, anchor="center")
        widget_list.append(label)

def app_en():
    app_elements["app_logic"]["language"] = "en"
    clean_screen(question_screen)

def app_pl():
    app_elements["app_logic"]["language"] = "pl"
    clean_screen(question_screen)

def app_ru():
    app_elements["app_logic"]["language"] = "ru"
    clean_screen(question_screen)

def question_screen():
    app_elements["app_logic"]["previous_screen"] = "start"
    widget_list = app_elements["widgets_list"]
    language = app_elements["app_logic"]["language"]

    image_frame = canvas.create_rectangle(50, 30, 450, 530, outline="#002352", width=2)
    widget_list.append(image_frame)

    app_elements["images"]["question_img"] = PhotoImage(file=f"ui/question_{language}.png")
    app_elements["images"]["current_image"] = app_elements["images"]["question_img"]
    app_elements["images"]["current_image_screen"] = canvas.create_image(250, 280,
                                                                         image=app_elements["images"]["current_image"],
                                                                         anchor="center")
    widget_list.append(app_elements["images"]["current_image_screen"])

    image_description = app_elements["app_logic"]["description"] = Label(text=question_phrase[language], font=("Courier New", 24, "bold"), fg="#002352",
                              bg="#FFEDF2")
    image_description.place(x=250, y=572, anchor="center")
    widget_list.append(image_description)

    app_elements["buttons"]["icon"] = PhotoImage(file="ui/icon.png")
    button_generate = Button(image=app_elements["buttons"]["icon"], highlightthickness=0, borderwidth=0,
                             command=random_img)
    widget_list.append(canvas.create_window(250, 689, window=button_generate))

    app_elements["buttons"]["back"] = PhotoImage(file="ui/back.png")
    button_back = Button(image=app_elements["buttons"]["back"], highlightthickness=0, borderwidth=0, command=go_back)
    widget_list.append(canvas.create_window(88, 689, window=button_back))

def random_img():
    app_elements["app_logic"]["previous_screen"] = "question_screen"
    language = app_elements["app_logic"]["language"]
    phrases = app_elements["phrases"][language]
    image_description = app_elements["app_logic"]["description"]

    folder_path = "photos"
    image_count = len([image for image in os.listdir(folder_path) if image.endswith((".png", ".jpg", ".jpeg"))])
    random_number = random.randint(1, image_count)
    app_elements["images"]["current_image"] = PhotoImage(file=f"{folder_path}/{random_number}.png")
    canvas.itemconfig(app_elements["images"]["current_image_screen"], image=app_elements["images"]["current_image"])

    image_description.config(text=f"{description_phrase[language]}\n{phrases[random_number-1]}")

def go_back():
    if app_elements["app_logic"]["previous_screen"] == "start":
        clean_screen(start)
    elif app_elements["app_logic"]["previous_screen"] == "question_screen":
        clean_screen(question_screen)

def clean_screen(next_screen=None):
    widget_list = app_elements["widgets_list"]
    for widget in widget_list:
        if isinstance(widget, int):  # Canvas object
            canvas.delete(widget)
        elif isinstance(widget, Label):
            widget.destroy()
    widget_list.clear()
    if next_screen:
        next_screen()

canvas = Canvas(width=500, height=900, bg="white", highlightthickness=0)
background_img = PhotoImage(file="ui/background.png")
background = canvas.create_image(250, 450, image=background_img, anchor="center")  # Store ID
canvas.pack()

start()

window.mainloop()
