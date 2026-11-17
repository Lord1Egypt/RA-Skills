#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_split — 评测语料确定性对半切分（防 in-sample 过拟合）。

split_of(doc_id): 按 id 前2位十六进制奇偶 → "calib" / "test"。
频谱构建、权重校准只用 calib 半；test 半只用于最终评测，永远不参与训练。
"""


def split_of(doc_id: str) -> str:
    try:
        return "calib" if int(doc_id[:2], 16) % 2 == 0 else "test"
    except (ValueError, TypeError):
        return "calib"


def filter_split(records, which):
    """which: calib / test / all 之一。"""
    if which == "all":
        return records
    return [r for r in records if split_of(r.get("id", "")) == which]
