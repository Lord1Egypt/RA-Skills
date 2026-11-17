#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""列出待改写的命中句（Humanizer 整改工作清单）"""
import sys, re, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from humanizer_check import (BANNED_STRUCT, BANNED_ABSTRACT, LIMIT_VAGUE,
                             LIMIT_EMOTION, IDIOMS)

PATS = [r'不是[^。！？]{1,15}而是', r'不仅仅?[^。！？]{0,12}更是',
        r'与其说[^。！？]{1,15}不如说', r'既[^。！？]{1,10}又[^。！？]{1,10}']

ap = argparse.ArgumentParser()
ap.add_argument("--kind", default="banned", choices=["banned", "pattern", "vague", "emotion", "idiom", "dash"])
ap.add_argument("--target", default="chapters/")
ap.add_argument("--limit", type=int, default=60)
args = ap.parse_args()

t = Path(args.target)
files = [t] if t.is_file() else sorted(t.rglob("*.md"))
files = [f for f in files if f.name != "_幕导语.md"]

words = {"banned": BANNED_STRUCT + BANNED_ABSTRACT, "vague": LIMIT_VAGUE,
         "emotion": LIMIT_EMOTION, "idiom": IDIOMS}.get(args.kind, [])
n = 0
for f in files:
    lines = f.read_text(encoding='utf-8').split('\n')
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        hits = []
        if args.kind == "pattern":
            for p in PATS:
                m = re.search(p, ln)
                if m:
                    hits.append(m.group(0))
        elif args.kind == "dash":
            c = ln.count('——')
            if c >= 2:
                hits.append(f'破折号×{c}')
        else:
            hits = [w for w in words if w in ln]
        if hits and n < args.limit:
            n += 1
            print(f"{f}:{i} [{','.join(hits[:3])}] {ln.strip()[:150]}")
print(f"\n--- 共列出 {n} 行（上限 {args.limit}）---")
