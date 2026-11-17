#!/usr/bin/env python3
"""Standalone structural checks for novel-premise-test-cn."""
from pathlib import Path
import re, struct, sys

ROOT = Path(__file__).resolve().parents[1]
required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "README.en.md", "LICENSE", "fixtures/success-input.md", "fixtures/success-output.md", "fixtures/failure-input.md", "fixtures/failure-output.md", "assets/icon-512.png", "assets/promo-1600x900.png"]
errors = [f"missing: {item}" for item in required if not (ROOT / item).is_file()]

def read(name): return (ROOT / name).read_text(encoding="utf-8")
def png_size(name):
    data = (ROOT / name).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n": raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])

if not errors:
    skill, manifest, agent = read("SKILL.md"), read("manifest.yaml"), read("agents/openai.yaml")
    if not re.search(r"^name: novel-premise-test-cn$", skill, re.M): errors.append("SKILL frontmatter name")
    for needle in ["name: novel-premise-test-cn", "slug: novel-premise-test-cn", "repository: https://github.com/xxjrq/novel-premise-test-cn", "self_test: python3 scripts/self_test.py"]:
        if needle not in manifest: errors.append(f"manifest field: {needle}")
    for needle in ["display_name:", "short_description:", "default_prompt:", 'icon_small: "assets/icon-512.png"', 'icon_large: "assets/icon-512.png"', "$novel-premise-test-cn", "policy:", "allow_implicit_invocation: true"]:
        if needle not in agent: errors.append(f"agent field: {needle}")
    desc = re.search(r"^description: (.+)$", manifest, re.M)
    if not desc or not 80 <= len(desc.group(1)) <= 240: errors.append("manifest description length")
    short = re.search(r"short_description: (.+)$", agent, re.M)
    if not short or not 25 <= len(short.group(1).strip('"')) <= 64: errors.append("short_description length")
    for name, size in [("assets/icon-512.png", (512, 512)), ("assets/promo-1600x900.png", (1600, 900))]:
        try:
            if png_size(name) != size: errors.append(f"wrong image size: {name}")
        except (ValueError, struct.error, IndexError): errors.append(f"invalid PNG: {name}")
    for fixture in ["fixtures/success-output.md", "fixtures/failure-output.md"]:
        if len(read(fixture).strip()) < 80: errors.append(f"fixture too small: {fixture}")

if errors:
    print("SELF-TEST FAILED")
    print("\n".join(f"- {x}" for x in errors))
    sys.exit(1)
print("SELF-TEST PASSED: metadata, fixtures, and PNG dimensions are valid.")
