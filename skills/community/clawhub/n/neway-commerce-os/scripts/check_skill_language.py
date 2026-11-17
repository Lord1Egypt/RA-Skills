#!/usr/bin/env python3
"""Zero-Chinese self-check for the Neway Commerce OS skill.

The skill ships to a global audience, so every file in this repository must be
written in English. Chinese is allowed in exactly two places:

  1. ``README.cn.md`` — the Chinese translation of the README.
  2. Two frontmatter lines in ``SKILL.md`` — ``description_zh:`` and
     ``display_name:`` — which the skill marketplace requires.

Everything else, including every git commit message, must be Chinese-free.
A file that legitimately needs CJK data (for example a regex that must also
match a zh-CN build) should carry it as a ``\\uXXXX`` escape rather than a
literal character.

Usage
-----
    python check_skill_language.py [skill_root] [--json]

Exit code is 0 when the skill is clean, 1 when any Chinese text is found.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Han ideographs (BMP + supplementary planes), CJK punctuation, fullwidth forms.
# Written with escapes so this detector is itself Chinese-free.
CJK_RE = re.compile(
    "[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef"
    "\U00020000-\U0002ffff]"
)

SKIP_DIRS = {".git", ".workbuddy", "__pycache__", "node_modules", "dist", ".vite"}
SKIP_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".pdf",
    ".zip",
}

# Relative (posix) paths that may contain Chinese on purpose.
WHITELIST_FILES = {"README.cn.md"}

# Per-file frontmatter prefixes that may contain Chinese on purpose.
WHITELIST_LINE_PREFIXES = {
    "SKILL.md": ("description_zh:", "display_name:"),
}


def is_whitelisted_line(rel: str, line: str) -> bool:
    return any(line.startswith(prefix) for prefix in WHITELIST_LINE_PREFIXES.get(rel, ()))


def scan(root: Path) -> list[dict]:
    findings: list[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if set(path.relative_to(root).parts) & SKIP_DIRS:
            continue
        if path.suffix.lower() in SKIP_SUFFIXES or rel in WHITELIST_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_whitelisted_line(rel, line):
                continue
            for match in CJK_RE.finditer(line):
                findings.append(
                    {
                        "file": rel,
                        "line": lineno,
                        "char": match.group(),
                        "text": line.strip()[:120],
                    }
                )
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail if any Chinese text appears in the skill.")
    parser.add_argument(
        "skill_root",
        nargs="?",
        default=None,
        help="Skill root directory (default: the parent of this script).",
    )
    parser.add_argument("--json", action="store_true", help="Emit a JSON report instead of text.")
    args = parser.parse_args()

    root = Path(args.skill_root).resolve() if args.skill_root else Path(__file__).resolve().parents[1]
    if not root.exists():
        raise SystemExit(f"Skill root not found: {root}")

    findings = scan(root)

    if args.json:
        print(
            json.dumps(
                {"root": str(root), "clean": not findings, "findings": findings},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1 if findings else 0)

    if findings:
        print(f"CHINESE TEXT FOUND - {len(findings)} occurrence(s):\n")
        for item in findings:
            print(f"  {item['file']}:{item['line']}  '{item['char']}'  {item['text']}")
        print()
        print("This skill ships to a global audience. Translate to English, or - if the")
        print("Chinese is intentional - whitelist the file in scripts/check_skill_language.py.")
        raise SystemExit(1)

    print(f"OK - no Chinese text found under {root}.")
    print("Whitelisted on purpose: README.cn.md, SKILL.md (description_zh / display_name).")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
