#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pre_scanner.py — 在调用 LLM 前对 JD 做廉价的结构化扫描。"""
from __future__ import annotations

import re

RED_FLAG_KEYWORDS = [
    "抗压", "狼性", "996", "加班", "学习能力", "使命感",
    "owner", "拼搏", "奋斗", "高压", "结果导向", "超强执行力",
]


def scan(jd_text: str) -> dict:
    """返回 {red_flag_keywords, structure, length}。"""
    lowered = jd_text.lower()
    red_flags = {kw: lowered.count(kw.lower()) for kw in RED_FLAG_KEYWORDS}

    sections = sum(
        1 for line in jd_text.splitlines()
        if re.match(r"^#{1,3} ", line) or line.rstrip().endswith(("：", ":"))
    )

    has_versions = bool(re.search(r"\d+\.\d+", jd_text))
    structure = {
        "sections": sections,
        "tech_stack_listed": has_versions,
        "tech_stack_detail": "具体到版本号" if has_versions else "只有buzzword",
        "salary_mentioned": bool(
            re.search(r"薪|salary|K[·\.]?\s*薪|\d+K|万/月", jd_text, re.IGNORECASE)
        ),
        "equity_mentioned": bool(
            re.search(r"期权|股权|equity|RSU|ESOP", jd_text, re.IGNORECASE)
        ),
        "level_specified": bool(
            re.search(r"P\d|T\d|Senior|Junior|Staff|Principal|职级|高级|资深", jd_text)
        ),
    }

    return {
        "red_flag_keywords": red_flags,
        "structure": structure,
        "length": len(jd_text),
    }
