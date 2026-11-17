# -*- coding: utf-8 -*-
"""自然拼读 CVC：c + a + t = ? 拼读并写出单词（附图示）。"""
import common as C

LEVELS = [2, 4]

CVC_EMOJI = {
    "cat": "🐱", "hat": "🎩", "bat": "🦇", "mat": "🟫", "map": "🗺️", "bag": "👜",
    "cap": "🧢", "fan": "🌀", "jam": "🍯", "rat": "🐀", "can": "🥫", "pan": "🍳",
    "van": "🚐", "bad": "👎", "tag": "🏷️", "bed": "🛏️", "red": "🔴", "pen": "✏️",
    "hen": "🐔", "ten": "🔟", "leg": "🦵", "net": "🕸️", "pet": "🐶", "wet": "💧",
    "web": "🕸️", "pig": "🐷", "big": "🐘", "dig": "⛏️", "pin": "📌", "bin": "🗑️",
    "fin": "🐟", "sit": "🪑", "hit": "🥊", "bit": "🦷", "kid": "🧒", "lid": "🔧",
    "six": "6️⃣", "dog": "🐶", "log": "🪵", "hot": "🌶️", "pot": "🍲", "dot": "🔴",
    "top": "🔝", "mop": "🧹", "box": "📦", "fox": "🦊", "hop": "🐸", "pop": "🎈",
    "cop": "👮", "bus": "🚌", "sun": "☀️", "run": "🏃", "cup": "🥤", "pup": "🐶",
    "bug": "🐛", "rug": "🟫", "hug": "🤗", "mug": "🍵", "nut": "🥜", "cut": "✂️", "tub": "🛁",
}


def gen(level, rng, lang):
    vowel = rng.choice(list(C.CVC.keys()))
    word = rng.choice(C.CVC[vowel])
    em = CVC_EMOJI.get(word, "🔤")
    a, b, c = word[0], word[1], word[2]
    html = (
        f'<div class="pic" style="font-size:34pt">{em}</div>'
        f'<div class="sentence" style="text-align:center">'
        f'<span class="sound">{a}</span> + <span class="sound">{b}</span> + <span class="sound">{c}</span>'
        f' = <span class="blank"></span></div>'
    )
    title = "自然拼读 CVC"
    instr = C.INSTR["phonics_cvc"][lang]
    answer = f"{word}（{a}-{b}-{c}）"
    return (title, instr, html, answer)
