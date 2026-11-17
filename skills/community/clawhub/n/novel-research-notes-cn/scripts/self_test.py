#!/usr/bin/env python3
"""Portable structural checks for this standalone Markdown skill."""
from pathlib import Path
import re
import sys
import struct

ROOT = Path(__file__).resolve().parents[1]
required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "README.en.md", "LICENSE", "icon-512.png", "assets/promo-1600x900.png", "fixtures/success-example.md", "fixtures/failure-example.md"]
errors = [f"missing: {p}" for p in required if not (ROOT / p).is_file()]

def text(path): return (ROOT / path).read_text(encoding="utf-8")
def is_png(path):
    return (ROOT / path).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
def png_size(path):
    data = (ROOT / path).read_bytes()
    return struct.unpack(">II", data[16:24]) if is_png(path) and len(data) >= 24 else (0, 0)
if not errors:
    skill, manifest, agent, readme = text("SKILL.md"), text("manifest.yaml"), text("agents/openai.yaml"), text("README.md")
    checks = [
        ("SKILL.md frontmatter name", "name: novel-research-notes-cn" in skill.split("---", 2)[1]),
        ("manifest name", re.search(r"^name: novel-research-notes-cn$", manifest, re.M)),
        ("manifest slug", re.search(r"^slug: novel-research-notes-cn$", manifest, re.M)),
        ("manifest icon", "icon: icon-512.png" in manifest),
        ("repository", "https://github.com/xxjrq/novel-research-notes-cn" in manifest),
        ("agent policy", "allow_implicit_invocation: true" in agent),
        ("agent description length", 25 <= len(re.search(r"short_description: (.+)", agent).group(1)) <= 64),
        ("Chinese README examples", "fixtures/success-example.md" in readme and "fixtures/failure-example.md" in readme),
        ("icon is PNG", is_png("icon-512.png")),
        ("promo is PNG", is_png("assets/promo-1600x900.png")),
        ("icon is 512x512", png_size("icon-512.png") == (512, 512)),
        ("promo is 1600x900", png_size("assets/promo-1600x900.png") == (1600, 900)),
    ]
    errors.extend(name for name, passed in checks if not passed)
if errors:
    print("SELF-TEST FAILED\n" + "\n".join("- " + e for e in errors)); sys.exit(1)
print("SELF-TEST PASSED: standalone files, naming, metadata, examples, and PNG assets verified.")
