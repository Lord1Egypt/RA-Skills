# -*- coding: utf-8 -*-
"""图形 / 方位"""
from common import *


def gen_shape(level, rng, lang="zh"):
    T = I18N[lang]
    sep = SEP[lang]
    k = 6 if level >= 2 else 4
    names = rng.sample(SHAPES, min(k, len(SHAPES)))
    target = rng.choice(names)
    items = []
    for nm in names:
        c = rng.choice(SHAPE_COLORS)
        items.append((nm, SVG_SHAPES[nm].format(c=c)))
    rng.shuffle(items)
    targets = [i for i, (nm, _) in enumerate(items) if nm == target]
    boxes = "".join(
        f'<div class="shapebox">{svg}<span class="lab">&nbsp;</span></div>' for nm, svg in items
    )
    html = f'<div class="row">{boxes}</div>'
    shape_label = target if lang == "zh" else SHAPE_NAMES_EN[target]
    instr = T["instr_shape"].format(shape=shape_label)
    ans = T["ans_shape_prefix"] + sep.join(str(t + 1) for t in targets) + T["ans_suffix"]
    return T["title_shape"], instr, html, ans


def gen_position(level, rng, lang="zh"):
    T = I18N[lang]
    cells = [None] * 9
    # 先放 A、B 于同一行或同一列，保证相对方向唯一（上/下/左/右）
    ar = rng.randrange(3)
    ac = rng.randrange(3)
    a_pos = ar * 3 + ac
    if rng.choice([True, False]):  # 同行 → 左右
        bc = rng.randrange(3)
        while bc == ac:
            bc = rng.randrange(3)
        b_pos = ar * 3 + bc
        dkey = "right" if bc > ac else "left"
    else:  # 同列 → 上下
        br = rng.randrange(3)
        while br == ar:
            br = rng.randrange(3)
        b_pos = br * 3 + ac
        dkey = "down" if br > ar else "up"
    emojis = rng.sample(EMOJI_ANIMALS, 3)
    cells[a_pos] = emojis[0]
    cells[b_pos] = emojis[1]
    empties = [i for i in range(9) if cells[i] is None]
    cells[rng.choice(empties)] = emojis[2]
    html_cells = "".join(f'<div class="cell lg">{c or ""}</div>' for c in cells)
    html = f'<div class="row" style="display:grid;grid-template-columns:repeat(3,44px);gap:4px;">{html_cells}</div>'
    instr = T["instr_position"].format(a=emojis[0], b=emojis[1])
    d_word = DIR_ZH[dkey] if lang == "zh" else DIR_EN[dkey]
    ans = T["ans_position"].format(a=emojis[0], b=emojis[1], d=d_word)
    return T["title_position"], instr, html, ans


TOPICS = {
    "shape": gen_shape,
    "position": gen_position,
}
