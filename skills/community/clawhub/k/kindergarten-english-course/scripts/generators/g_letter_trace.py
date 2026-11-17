# -*- coding: utf-8 -*-
"""字母描红 / 书写启蒙：大字示范 + 描红框 + 自写框。"""
import common as C

LEVELS = [1]


def _trace(n, up, lo):
    return (
        f'<div class="bigletter">{up} {lo}</div>'
        f'<div style="text-align:center;margin:2mm 0">'
        f'<span class="tracebox">{up}</span><span class="tracebox">{lo}</span></div>'
        f'<div style="text-align:center">'
        + "".join(f'<span class="writebox"></span>' for _ in range(3))
        + "</div>"
    )


def gen(level, rng, lang):
    up, lo = rng.choice(C.LETTER_PAIRS)
    title = f"字母描红 {up}{lo}"
    instr = C.INSTR["letter_trace"][lang]
    html = _trace(1, up, lo)
    answer = f"{up}{lo}：按笔顺描红并在虚线框内书写"
    return (title, instr, html, answer)
