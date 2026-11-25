#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布前自检：①模板占位符残留 ②乱码字符。

用法:
    python3 scripts/check_placeholders.py

期望输出:
    LEFTOVER_COUNT 0
    GARBLED_COUNT 0
退出码 0 = 通过，1 = 有问题。

说明：敏感词/内部标识的脱敏扫描由发布方在包外单独执行，
不写入本包——避免检查器本身把词表随包公开。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
SCAN_EXT = (".md", ".py", ".json", ".txt")

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")
# U+FFFD 替换字符（编码损坏）/ 控制字符
GARBLED = re.compile(r"[\ufffd\u001a]")

files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in SCAN_EXT]

leftover = garbled = 0
for p in files:
    try:
        txt = p.read_text(encoding="utf-8")
    except Exception:
        continue
    rel = p.relative_to(ROOT)

    hits = PLACEHOLDER.findall(txt)
    if hits:
        print(f"LEFTOVER {rel} -> {hits}")
        leftover += len(hits)

    g = GARBLED.findall(txt)
    if g:
        print(f"GARBLED {rel} -> {len(g)} 处")
        garbled += len(g)

print(f"LEFTOVER_COUNT {leftover}")
print(f"GARBLED_COUNT {garbled}")
sys.exit(1 if (leftover or garbled) else 0)
