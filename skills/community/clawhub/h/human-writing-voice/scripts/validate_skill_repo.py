#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "references/storyscope-tells.md",
]

errors = []
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing {rel}")

skill = ROOT / "SKILL.md"
if skill.exists():
    text = skill.read_text()
    if not text.startswith("---\n"):
        errors.append("SKILL.md missing YAML frontmatter")
    else:
        parts = text.split("---", 2)
        if len(parts) < 3:
            errors.append("SKILL.md frontmatter not closed")
        else:
            frontmatter = parts[1]
            if not re.search(r"^name:\s*human-writing\s*$", frontmatter, re.M):
                errors.append("frontmatter name must be human-writing")
            if not re.search(r'^description:\s*".+"\s*$', frontmatter, re.M):
                errors.append("frontmatter description must be quoted")
    for needle in [
        "## Before Sending",
        "## Hard Bans",
        "structural AI tells",
        "No `it's not X, it's Y`",
    ]:
        if needle not in text:
            errors.append(f"SKILL.md missing {needle!r}")

for path in ROOT.rglob("*"):
    if path.is_file():
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel.startswith(".better-every-run/") or rel.startswith(".agent/"):
            errors.append(f"private artifact included: {rel}")
        if rel == "scripts/validate_skill_repo.py":
            continue
        data = path.read_text(errors="ignore")
        private_patterns = [
            (r"/Users/[^/\s]+/\.openclaw", "local OpenClaw home path"),
            (r"\." + "openclaw/workspace", "local workspace path"),
            (r"\b\d{9,12}\b", "long numeric chat/account id"),
            (r"\b(?:10|100|192)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "private network address"),
        ]
        for pattern, label in private_patterns:
            if re.search(pattern, data):
                errors.append(f"{label} in {rel}")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)

print("human-writing skill repo valid")
