# -*- coding: utf-8 -*-
"""排序 / 规律"""
from common import *


def gen_order(level, rng, lang="zh"):
    T = I18N[lang]
    sep = SEP[lang]
    k = 5
    start = rng.randrange(0, len(SIZE_ORDER) - k)
    seq = SIZE_ORDER[start:start + k]
    answer = seq[:]
    rng.shuffle(seq)
    shown = list(range(1, k + 1))
    cells = "".join(f'<div class="cell lg">{seq[i]}</div><div class="cell">{shown[i]}</div>' for i in range(k))
    html = f'<div class="row">{cells}</div>'
    instr = T["instr_order"]
    order_map = [answer.index(e) + 1 for e in seq]
    ans = T["ans_order_prefix"] + sep.join(str(x) for x in order_map)
    return T["title_order"], instr, html, ans


def gen_pattern(level, rng, lang="zh"):
    T = I18N[lang]
    sep = SEP[lang]
    palettes = [
        list(EMOJI_COLORS.values()),
        rng.choice([EMOJI_ANIMALS, EMOJI_FRUITS, EMOJI_VEHICLES]),
    ]
    pal = rng.choice(palettes)
    if level <= 1:
        pattern = [pal[0], pal[1]]
    elif level == 2:
        pattern = rng.choice([[pal[0], pal[1], pal[1]], [pal[0], pal[0], pal[1]]])
    elif level == 3:
        pattern = [pal[0], pal[1], pal[2]]
    else:
        pattern = rng.choice([[pal[0], pal[1], pal[2], pal[0]], [pal[0], pal[1], pal[1], pal[2]]])
    reps = 3
    full = (pattern * (reps + 1))[:reps * len(pattern)]
    gaps = rng.sample(range(len(full)), 1 if level <= 2 else 2)
    display = []
    answers = []
    for i, e in enumerate(full):
        if i in gaps:
            display.append('<span class="gap">?</span>')
            answers.append(e)
        else:
            display.append(f'<div class="cell">{e}</div>')
    html = f'<div class="seq">{"".join(display)}</div>'
    instr = T["instr_pattern"]
    ans = T["ans_pattern_prefix"] + sep.join(answers)
    return T["title_pattern"], instr, html, ans


TOPICS = {
    "order": gen_order,
    "pattern": gen_pattern,
}
