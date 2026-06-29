#!/usr/bin/env python3
"""清理 dist/ 目录中的旧版本 ZIP，只保留 _meta.json 中的最新版本"""
import json, os, re, glob
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import SKILLS_ROOT as SKILLS_DIR, DIST_DIR

# 读取所有技能最新版本
latest = {}
for entry in sorted(os.listdir(SKILLS_DIR)):
    meta_path = os.path.join(SKILLS_DIR, entry, "_meta.json")
    if not os.path.isfile(meta_path):
        continue
    try:
        with open(meta_path, encoding="utf-8") as f:
            d = json.load(f)
        ver = d.get("version", "1.0.0")
        latest[entry] = ver
    except Exception:
        pass

print("最新版本:")
for name, ver in sorted(latest.items()):
    print(f"  {name}-v{ver}.zip")

# 找出需要删除的旧版本
to_delete = []
for fname in os.listdir(DIST_DIR):
    if not fname.endswith(".zip"):
        continue
    m = re.match(r"^(.+?)-v[\d\.]+\.zip$", fname)
    if not m:
        continue
    sname = m.group(1)
    if sname in latest:
        expected = f"{sname}-v{latest[sname]}.zip"
        if fname != expected:
            to_delete.append(fname)

if not to_delete:
    print("\n✅ dist/ 中没有旧版本，无需清理")
else:
    print(f"\n需要删除的旧版本 ({len(to_delete)} 个):")
