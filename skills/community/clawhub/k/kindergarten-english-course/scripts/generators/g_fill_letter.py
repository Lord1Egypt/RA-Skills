# -*- coding: utf-8 -*-
"""补全单词：给出图示与缺一个字母的单词，填上缺的字母。"""
import common as C

LEVELS = [2, 3]

_POOL = []


def _pool():
    if _POOL:
        return _POOL
    for t in C.VOCAB:
        for w, em, zh in C.VOCAB[t]:
            if len(w) >= 3:  # 太短的补全无意义
                _POOL.append((w, em))
    return _POOL


def gen(level, rng, lang):
    w, em = rng.choice(_pool())
    pos = rng.randint(0, len(w) - 1)
    masked = w[:pos] + "＿" + w[pos + 1:]
    html = (
        f'<div class="pic" style="font-size:34pt;margin-bottom:1mm">{em}</div>'
        f'<div class="sentence" style="text-align:center;font-size:22pt">{masked}'
        f'　<span class="blank"></span></div>'
    )
    title = "补全单词"
    instr = C.INSTR["fill_letter"][lang]
    answer = f"{w}（缺：{w[pos].upper()}）"
    return (title, instr, html, answer)
