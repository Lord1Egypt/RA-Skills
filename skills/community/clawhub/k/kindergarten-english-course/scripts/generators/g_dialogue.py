# -*- coding: utf-8 -*-
"""情景对话：读对话，补全答句（B 部分）。"""
import common as C

LEVELS = [4]


def gen(level, rng, lang):
    q, bframe, words, emap = rng.choice(C.DIALOGUES)
    word = rng.choice(words)
    em = emap.get(word, "🔤")
    b_full = bframe.format(word)
    # 答句词库
    others = [w for w in words if w != word]
    bank = [word] + (rng.sample(others, min(2, len(others))) if others else [])
    bank = rng.sample(bank, len(bank))
    b_blank = bframe.format('<span class="blank"></span>')
    bank_html = "".join(f"<span>{w}</span>" for w in bank)
    html = (
        f'<div class="dialoguebox">'
        f'<div class="qA">A: {q}</div>'
        f'<div class="pic" style="font-size:30pt;text-align:left;margin:1mm 0">{em}</div>'
        f'<div class="qB">B: {b_blank}</div>'
        f'<div class="wordopt" style="margin-top:2mm">{bank_html}</div>'
        f"</div>"
    )
    title = "情景对话"
    instr = C.INSTR["dialogue"][lang]
    answer = f"A: {q}　B: {b_full}"
    return (title, instr, html, answer)
