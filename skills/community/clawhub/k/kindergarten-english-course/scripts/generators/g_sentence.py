# -*- coding: utf-8 -*-
"""简单句型：看图，从词库中选词把句子补充完整。"""
import common as C

LEVELS = [3, 4]


def gen(level, rng, lang):
    frame, words, emap = rng.choice(C.SENTENCE_PATTERNS)
    word = rng.choice(words)
    em = emap.get(word, "🔤")
    # 词库：正确项 + 2 个干扰（同主题池内其他词）
    distract = [w for w in words if w != word]
    if len(distract) >= 2:
        bank = [word] + rng.sample(distract, 2)
    else:
        bank = [word] + distract
    bank = rng.sample(bank, len(bank))
    sentence = frame.format('<span class="blank"></span>')
    bank_html = "".join(f"<span>{w}</span>" for w in bank)
    html = (
        f'<div class="pic" style="font-size:34pt;margin-bottom:1mm">{em}</div>'
        f'<div class="sentence">{sentence}</div>'
        f'<div class="wordopt" style="margin-top:2mm">{bank_html}</div>'
    )
    title = "简单句型"
    instr = C.INSTR["sentence"][lang]
    answer = frame.format(word)
    return (title, instr, html, answer)
