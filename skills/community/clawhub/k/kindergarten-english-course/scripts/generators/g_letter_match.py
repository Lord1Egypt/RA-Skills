# -*- coding: utf-8 -*-
"""大小写配对：左列大写，右列打乱的小写，用线连起来。"""
import common as C

LEVELS = [1, 2]


def gen(level, rng, lang):
    n = 4
    pairs = rng.sample(C.LETTER_PAIRS, n)
    ups = [p[0] for p in pairs]
    los = rng.sample([p[1] for p in pairs], n)
    left = "".join(f"<div>{u}</div>" for u in ups)
    right = "".join(f"<div>{l}</div>" for l in los)
    html = (
        '<div class="matchrow">'
        f'<div class="matchcol">{left}</div>'
        '<div class="dotline"></div>'
        f'<div class="matchcol">{right}</div>'
        "</div>"
    )
    title = "大小写配对"
    instr = C.INSTR["letter_match"][lang]
    ans = "、".join(f"{u}-{l}" for u, l in pairs)
    return (title, instr, html, ans)
