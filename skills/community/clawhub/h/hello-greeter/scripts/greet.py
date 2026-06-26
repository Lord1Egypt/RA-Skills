#!/usr/bin/env python3
"""Generate personalized greetings in multiple languages and tones."""

import argparse

GREETINGS = {
    "en": {"formal": "Good day", "casual": "Hey", "playful": "Howdy"},
    "zh": {"formal": "您好", "casual": "你好", "playful": "嗨"},
    "ja": {"formal": "こんにちは", "casual": "やあ", "playful": "おーい"},
    "es": {"formal": "Buenos días", "casual": "Hola", "playful": "¡Qué tal!"},
    "fr": {"formal": "Bonjour", "casual": "Salut", "playful": "Coucou"},
}

SUFFIXES = {
    "en": {"formal": "It is a pleasure to meet you.", "casual": "Welcome!", "playful": "Ready for an adventure?"},
    "zh": {"formal": "很高兴见到您。", "casual": "欢迎！", "playful": "准备好冒险了吗？"},
    "ja": {"formal": "お会いできて光栄です。", "casual": "ようこそ！", "playful": "冒険の準備はいい？"},
    "es": {"formal": "Es un placer conocerle.", "casual": "¡Bienvenido!", "playful": "¡Listo para la aventura?"},
    "fr": {"formal": "Enchanté de vous rencontrer.", "casual": "Bienvenue !", "playful": "Prêt pour l'aventure ?"},
}


def greet(name: str, lang: str, tone: str) -> str:
    greeting = GREETINGS.get(lang, GREETINGS["en"]).get(tone, GREETINGS["en"]["casual"])
    suffix = SUFFIXES.get(lang, SUFFIXES["en"]).get(tone, SUFFIXES["en"]["casual"])
    return f"{greeting}, {name}! {suffix}"


def main():
    parser = argparse.ArgumentParser(description="Generate a greeting")
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument("--lang", default="en", choices=list(GREETINGS.keys()), help="Language")
    parser.add_argument("--tone", default="casual", choices=["formal", "casual", "playful"], help="Tone")
    args = parser.parse_args()
    print(greet(args.name, args.lang, args.tone))


if __name__ == "__main__":
    main()