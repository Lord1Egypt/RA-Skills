# -*- coding: utf-8 -*-
"""高频词认读：大字展示目标词，在同行中圈出该词。"""
import common as C

LEVELS = [3, 4]


def gen(level, rng, lang):
    target = rng.choice(C.SIGHT_WORDS)
    others = rng.sample([w for w in C.SIGHT_WORDS if w != target], 3)
    row = [target] + others
    row = rng.sample(row, len(row))
    html = (
        f'<div class="bigletter" style="font-size:34pt;color:var(--ink)">{target}</div>'
        f'<div class="wordopt" style="margin-top:3mm">'
        + "".join(f"<span>{w}</span>" for w in row)
        + "</div>"
    )
    title = "高频词认读"
    instr = C.INSTR["sight_words"][lang]
    answer = f"圈出：{target}"
    return (title, instr, html, answer)
