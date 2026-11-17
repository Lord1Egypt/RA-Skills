# -*- coding: utf-8 -*-
"""等量代换"""
from common import *


def gen_swap(level, rng, lang="zh"):
    T = I18N[lang]
    # 等量代换：1 个 X = b 个 ★，问 c 个 X = ? 个 ★（结果为 c*b）
    X = rng.choice(list(EMOJI_COLORS.values()))
    b = rng.randint(2, 3)
    c = rng.randint(2, 4)
    ans = c * b
    html = (
        f'<div class="row" style="font-size:22px;gap:10px;align-items:center;">'
        f'<span>{X} = {"⭐" * b}</span>'
        f'<span style="color:#999;">→</span>'
        f'<span>{X * c} = ?⭐</span></div>'
    )
    instr = T["instr_swap"]
    ans_text = str(ans) + T["ans_swap_suffix"]
    return T["title_swap"], instr, html, ans_text


TOPICS = {
    "swap": gen_swap,
}
