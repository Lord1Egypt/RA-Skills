# -*- coding: utf-8 -*-
"""主题词汇：展示一个主题下的若干单词与图示，供认读/跟读。"""
import common as C

LEVELS = [1, 2, 3]

THEMES = list(C.VOCAB.keys())


def gen(level, rng, lang):
    theme = rng.choice(THEMES)
    items = C.VOCAB[theme]
    k = min(6, len(items))
    chosen = rng.sample(items, k)
    cards = "".join(
        f'<div style="text-align:center;font-size:13pt;margin:1mm">'
        f'<div class="pic" style="font-size:30pt">{em}</div>{w}<div style="color:#999;font-size:9pt">{zh}</div></div>'
        for w, em, zh in chosen
    )
    html = f'<div style="font-size:15pt;font-weight:700;color:var(--accent);margin-bottom:2mm">{theme.title()}</div><div class="grid2" style="gap:3mm">{cards}</div>'
    title = f"主题词汇 · {theme.title()}"
    instr = C.INSTR["vocab_theme"][lang]
    answer = "、".join(w for w, em, zh in chosen)
    return (title, instr, html, answer)
