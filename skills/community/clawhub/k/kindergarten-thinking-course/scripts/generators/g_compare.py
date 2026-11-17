# -*- coding: utf-8 -*-
"""比较（多少 / 高矮）"""
from common import *


def gen_compare(level, rng, lang="zh"):
    T = I18N[lang]
    if level <= 1:
        a = rng.randint(2, 4)
        b = rng.randint(2, 4)
        while b == a:
            b = rng.randint(2, 4)
        left = "".join('<div class="cell">🔵</div>' for _ in range(a))
        right = "".join('<div class="cell">🔵</div>' for _ in range(b))
        html = f'<div class="row"><span>左边：</span>{left}</div><div class="row"><span>右边：</span>{right}</div>'
        instr = T["instr_compare_count"]
        more_key = "left" if a > b else "right"
        side_word = SIDE[lang][more_key]
        ans = T["ans_count_more"].format(side=side_word, n=max(a, b))
    else:
        heights = rng.sample([20, 35, 50, 65, 80], 3)
        bars = "".join(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;">'
            f'<div style="width:24px;height:{h}px;background:#4a90d9;border-radius:3px 3px 0 0;"></div>'
            f'<div class="lab">{i+1}</div></div>' for i, h in enumerate(heights)
        )
        html = f'<div class="row" style="align-items:flex-end;">{bars}</div>'
        instr = T["instr_compare_height"]
        order = sorted(range(3), key=lambda i: -heights[i])
        ans = SEP[lang].join(str(o + 1) for o in order)
    return T["title_compare"], instr, html, ans


TOPICS = {
    "compare": gen_compare,
}
