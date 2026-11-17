#!/usr/bin/env python3
"""Offline package checks; this does not pretend to test model-generated prose."""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(condition, message):
    if not condition:
        errors.append(message)

def png_size(path):
    data = path.read_bytes()
    need(data[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name} is not a PNG")
    need(data[12:16] == b"IHDR", f"{path.name} lacks IHDR")
    return struct.unpack(">II", data[16:24])

def main():
    # Structure validation: repository files and declared metadata must agree.
    required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md",
                "README.en.md", "LICENSE", "fixtures/success.json",
                "fixtures/failure-missing-fields.json", "assets/icon-512.png",
                "assets/promo-1600x900.png"]
    for relative in required:
        need((ROOT / relative).is_file(), f"missing required file: {relative}")
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    for field in ("name: novel-synopsis-pack-cn", "display_name: 小说投稿梗概包",
                  "repository: https://github.com/xxjrq/novel-synopsis-pack-cn",
                  "self_test: python3 scripts/self_test.py"):
        need(field in manifest, f"manifest missing or mismatched: {field}")
    short = re.search(r"^short_description: (.+)$", manifest, re.M)
    need(short is not None and 25 <= len(short.group(1).strip()) <= 64,
         "short_description must be 25–64 characters")
    need(len(re.findall(r"^  - .+$", manifest, re.M)) >= 7,
         "manifest needs at least four tags and three triggers")
    for filename, expected in (("icon-512.png", (512, 512)), ("promo-1600x900.png", (1600, 900))):
        path = ROOT / "assets" / filename
        if path.is_file():
            need(png_size(path) == expected, f"{filename} must be {expected[0]}x{expected[1]}")

    # Fixture validation: validates accepted/rejected input shape, not LLM output quality.
    success = json.loads((ROOT / "fixtures/success.json").read_text(encoding="utf-8"))
    for key in ("story_overview", "chapter_summaries", "submission_lengths"):
        need(bool(success.get(key)), f"success fixture lacks {key}")
    need({300, 800, 1500}.issubset(set(success.get("submission_lengths", []))),
         "success fixture lacks required target lengths")
    failure = json.loads((ROOT / "fixtures/failure-missing-fields.json").read_text(encoding="utf-8"))
    actual_missing = [k for k in ("story_overview", "chapter_summaries", "submission_lengths") if not failure.get(k)]
    need(actual_missing == failure.get("expected_missing"), "failure fixture does not accurately declare missing fields")
    expected_issues = failure.get("expected_issues")
    need(isinstance(expected_issues, list) and "故事未覆盖结局" in expected_issues,
         "failure fixture must declare the incomplete-ending issue")

    if errors:
        print("SELF-TEST FAILED")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print("SELF-TEST PASSED")
    print("Structure: metadata, required files, PNG dimensions, and fixture schema validated.")
    print("Behavior boundary: generated synopsis quality is intentionally not simulated or claimed by this offline check.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
