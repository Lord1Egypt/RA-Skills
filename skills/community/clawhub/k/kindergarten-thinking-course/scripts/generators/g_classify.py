# -*- coding: utf-8 -*-
"""分类 / 配对 / 找相同 / 找不同"""
from common import *


def gen_classify(level, rng, lang="zh"):
    T = I18N[lang]
    sep = SEP[lang]
    themes = [("水果", EMOJI_FRUITS), ("动物", EMOJI_ANIMALS), ("交通工具", EMOJI_VEHICLES)]
    name, pool = rng.choice(themes)
    attr = rng.choice(["颜色", "类别"])
    if attr == "颜色":
        color_name, color_emoji = rng.choice(list(EMOJI_COLORS.items()))
        others = [c for c in EMOJI_COLORS.values() if c != color_emoji]
        items = [color_emoji] * 3 + [rng.choice(others) for _ in range(rng.randint(4, 6))]
        color_label = color_name if lang == "zh" else COLOR_EN[color_name]
        instr = T["instr_classify_color"].format(color=color_label)
    else:
        others = rng.choice([e for e in [EMOJI_ANIMALS, EMOJI_VEHICLES, EMOJI_FRUITS] if e != pool])
        items = rng.sample(pool, 4) + rng.sample(others, rng.randint(3, 4))
        theme_label = name if lang == "zh" else THEME_EN[name]
        instr = T["instr_classify_cat"].format(name=theme_label)
    rng.shuffle(items)
    targets = sorted([i for i, e in enumerate(items) if (attr == "颜色" and e == color_emoji) or (attr == "类别" and e in pool)])
    cells = "".join(f'<div class="cell lg">{e}</div>' for e in items)
    html = f'<div class="row">{cells}</div>'
    ans = T["ans_shape_prefix"] + sep.join(str(t + 1) for t in targets) + T["ans_suffix"]
    return T["title_classify"], instr, html, ans


def gen_match(level, rng, lang="zh"):
    T = I18N[lang]
    sep = SEP[lang]
    pool = rng.choice([EMOJI_ANIMALS, EMOJI_FRUITS, EMOJI_VEHICLES])
    left = rng.sample(pool, 4)
    right = left[:]
    rng.shuffle(right)
    mapping = [right.index(e) + 1 for e in left]
    left_html = "".join(f'<div class="cell lg">{e}</div>' for e in left)
    right_html = "".join(f'<div class="cell lg">{e}<span class="lab"> ({i+1})</span></div>' for i, e in enumerate(right))
    html = f'<div class="pair"><div class="paircol">{left_html}</div><div class="paircol">{right_html}</div></div>'
    instr = T["instr_match"]
    ans = sep.join(f"{i+1}→{mapping[i]}" for i in range(4))
    return T["title_match"], instr, html, ans


def gen_same(level, rng, lang="zh"):
    T = I18N[lang]
    n = 9
    pool = rng.choice([EMOJI_ANIMALS, EMOJI_FRUITS, EMOJI_VEHICLES])
    base = rng.sample(pool, n - 1)
    dup = rng.choice(base)
    items = base[:]
    items.insert(rng.randint(0, n - 1), dup)
    rng.shuffle(items)
    pos = [i for i, e in enumerate(items) if e == dup]
    cells = "".join(f'<div class="cell lg">{e}</div>' for e in items)
    html = f'<div class="row">{cells}</div>'
    instr = T["instr_same"]
    ans = T["ans_same_two"].format(x=pos[0] + 1, y=pos[1] + 1)
    return T["title_same"], instr, html, ans


def gen_diff(level, rng, lang="zh"):
    T = I18N[lang]
    n = 9 if level >= 2 else 6
    pool = rng.choice([EMOJI_ANIMALS, EMOJI_FRUITS, EMOJI_VEHICLES])
    normal = rng.choice(pool)
    others = [e for e in pool if e != normal]
    items = [normal] * n
    odd_idx = rng.randrange(n)
    items[odd_idx] = rng.choice(others)
    rng.shuffle(items)
    real_odd = items.index([e for e in items if e != normal][0])
    cells = "".join(f'<div class="cell lg">{e}</div>' for e in items)
    html = f'<div class="row">{cells}</div>'
    instr = T["instr_diff"]
    ans = T["ans_shape_prefix"] + str(real_odd + 1) + T["ans_suffix"]
    return T["title_diff"], instr, html, ans


TOPICS = {
    "classify": gen_classify,
    "match": gen_match,
    "same": gen_same,
    "diff": gen_diff,
}
