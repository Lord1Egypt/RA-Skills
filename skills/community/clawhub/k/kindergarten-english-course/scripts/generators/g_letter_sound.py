# -*- coding: utf-8 -*-
"""字母发音：圈出与目标发音相同的图片（听音辨字母/看图选首音）。"""
import common as C

LEVELS = [1, 2]

# 主题词首字母 → emoji 图示（首音可辨）
_PIC_BY_INITIAL = {}


def _pic_pool():
    if _PIC_BY_INITIAL:
        return _PIC_BY_INITIAL
    for theme, words in C.VOCAB.items():
        for w, em, zh in words:
            _PIC_BY_INITIAL.setdefault(w[0], []).append((w, em))
    return _PIC_BY_INITIAL


def gen(level, rng, lang):
    pool = _pic_pool()
    # 选一个有足够候选的目标字母
    target = rng.choice([c for c in "bcdfglmprs" if len(pool.get(c, [])) >= 1])
    correct = rng.choice(pool[target])
    # 干扰项：首字母不同的图片
    others = [(w, em) for c, lst in pool.items() if c != target for (w, em) in lst]
    distract = rng.sample(others, min(3, len(others)))
    cells = [(correct[0], correct[1], True)] + [(w, em, False) for w, em in distract]
    cells = rng.sample(cells, len(cells))
    pic_html = "".join(
        f'<div class="pic">{em}<div class="wlbl">{w}</div></div>'
        for w, em, _is_c in cells
    )
    html = (
        f'<div class="pic" style="font-size:13pt;margin-bottom:2mm">'
        f'圈出以 <span class="sound">/{target}/</span> 开头的图：</div>'
        f'<div class="wordopt" style="gap:10mm">{pic_html}</div>'
    )
    title = "字母发音"
    instr = C.INSTR["letter_sound"][lang]
    answer = f"正确：{correct[0]}（/{target}/ 音；其余为干扰项）"
    return (title, instr, html, answer)
