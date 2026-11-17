# -*- coding: utf-8 -*-
"""tests/_docs.py — 双语包自适应文档读取（v7.0.0）。

CH 英文包按语言铁律不含 SKILL_ZH.md；文档断言经 zh_text() 读取时，
ZH 缺省会 raise unittest.SkipTest（该方法记 skip 不记 FAIL），
非 ZH 断言在两种包形态下都照常执行。
"""
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
HAS_ZH = (PKG / "SKILL_ZH.md").is_file()
DOCS = ("SKILL.md", "SKILL_ZH.md") if HAS_ZH else ("SKILL.md",)


def zh_text(encoding="utf-8"):
    if not HAS_ZH:
        raise unittest.SkipTest("CH 英文包无 SKILL_ZH.md：ZH 文档断言自适应跳过")
    return (PKG / "SKILL_ZH.md").read_text(encoding=encoding)
