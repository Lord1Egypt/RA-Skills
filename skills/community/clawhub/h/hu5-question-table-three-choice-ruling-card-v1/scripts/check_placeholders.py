#!/usr/bin/env python3
"""占位符自检：扫描本目录 .md/.py，统计残留双花括号占位符数量。
替换 9 占位符后应返回 LEFTOVER_COUNT 0；否则报错退出，提示照抄者尚未替换。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
PAT = re.compile(r"\{\{[^}]+\}\}")

leftover = 0
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix in (".md", ".py"):
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        hits = PAT.findall(txt)
        if hits:
            print(f"LEFTOVER {p.relative_to(ROOT)} -> {hits}")
            leftover += len(hits)

print(f"LEFTOVER_COUNT {leftover}")
sys.exit(1 if leftover else 0)
