#!/usr/bin/env python3
"""Structure checks only; this Markdown Skill has no executable business engine."""
from pathlib import Path
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(rel):
    path = ROOT / rel
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"missing or empty: {rel}")
    return path

def png_size(path):
    with path.open("rb") as f:
        data = f.read(24)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])

required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "README.en.md",
            "LICENSE", "icon-512.png", "assets/promo-1600x900.png",
            "fixtures/success/lin-wan.json", "fixtures/failure/missing-chapters.json",
            "sources/chinese-novelist-skill.md"]
for item in required:
    need(item)

manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8") if (ROOT / "manifest.yaml").exists() else ""
for text in ['slug: "novel-character-arc-cn"', 'repository: "https://github.com/xxjrq/novel-character-arc-cn"', 'self_test: "python3 scripts/self_test.py"']:
    if text not in manifest:
        errors.append(f"manifest field absent: {text}")
if len([line for line in manifest.splitlines() if line.startswith('  - "')]) < 7:
    errors.append("manifest must contain tags and trigger words")

for rel, expected in [("icon-512.png", (512, 512)), ("assets/promo-1600x900.png", (1600, 900))]:
    try:
        if png_size(ROOT / rel) != expected:
            errors.append(f"wrong PNG dimensions: {rel}")
    except (OSError, ValueError, struct.error) as exc:
        errors.append(f"invalid PNG: {rel}: {exc}")

try:
    good = json.loads((ROOT / "fixtures/success/lin-wan.json").read_text(encoding="utf-8"))
    if not all(k in good for k in ("角色设定", "故事概要", "已写章节")) or not good["已写章节"]:
        errors.append("success fixture is not a complete input")
    bad = json.loads((ROOT / "fixtures/failure/missing-chapters.json").read_text(encoding="utf-8"))
    if "已写章节" in bad:
        errors.append("failure fixture must omit 已写章节")
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"invalid fixture JSON: {exc}")

if errors:
    print("SELF-TEST FAILED (structure validation):")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("SELF-TEST PASSED: package structure and fixture contracts are valid.")
print("Note: this validates structure and samples only; real behavior is the Markdown workflow in SKILL.md.")
