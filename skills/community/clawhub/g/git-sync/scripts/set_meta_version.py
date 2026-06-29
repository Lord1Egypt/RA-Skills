#!/usr/bin/env python3
"""更新 _meta.json 的 version 字段"""
import json, sys

meta_file = sys.argv[1]
new_version = sys.argv[2]

with open(meta_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

old_ver = meta.get("version", "0.0.0")
meta["version"] = new_version

with open(meta_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"  ✅ _meta.json 版本号: {old_ver} → {new_version}")
