# -*- coding: utf-8 -*-
"""看图识词：给出图示与 3 个单词选项，圈出正确单词。"""
import common as C

LEVELS = [2, 3]

_ALL = []

THEMES = ["animals", "food", "colors", "body", "toys", "nature", "clothes", "school", "family"]


def _all_words():
    if _ALL:
        return _ALL
    for t in THEMES:
        for w, em, zh in C.VOCAB[t]:
            _ALL.append((w, em))
    return _ALL


def gen(level, rng, lang):
    allw = _all_words()
    correct = rng.choice(allw)
    others = [x for x in allw if x[0] != correct[0]]
    opts = rng.sample(others, min(2, len(others)))
    opts = [correct] + opts
    opts = rng.sample(opts, len(opts))
    opt_html = "".join(
        f"<span>{w}</span>" for w, em in opts
    )
    html = (
        f'<div class="pic" style="font-size:34pt;margin-bottom:1mm">{correct[1]}</div>'
        f'<div class="wordopt">{opt_html}</div>'
    )
    title = "看图识词"
    instr = C.INSTR["word_pic"][lang]
    answer = correct[0]
    return (title, instr, html, answer)
