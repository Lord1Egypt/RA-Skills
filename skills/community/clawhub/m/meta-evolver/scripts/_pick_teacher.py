#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出尚未蒸馏、含真实脚本的教师候选（排除已生成 meta-* 与 meta-* 本身）。"""
import json, os
SK = os.path.expanduser("~/.workbuddy/skills")
p = json.load(open(os.path.join(SK, "meta-evolver", "evolver_patterns.json"), encoding="utf-8"))
ti = p.get("teacher_index", [])
existing_meta = set(d[5:] for d in os.listdir(SK) if d.startswith("meta-"))
cands = []
for entry in ti:
    name = entry.get("name") if isinstance(entry, dict) else entry
    if not name or name.startswith("meta-"):
        continue
    if name in existing_meta:
        continue
    if not os.path.isfile(os.path.join(SK, name, "SKILL.md")):
        continue
    has_scripts = entry.get("has_scripts") if isinstance(entry, dict) else True
    cands.append((name, has_scripts, entry.get("size", 0) if isinstance(entry, dict) else 0))
# 优先有脚本、体量适中的教师
with_scripts = [c for c in cands if c[1]]
print("未蒸馏候选总数:", len(cands), "| 含脚本:", len(with_scripts))
print("含脚本候选前30:", [c[0] for c in with_scripts[:30]])
