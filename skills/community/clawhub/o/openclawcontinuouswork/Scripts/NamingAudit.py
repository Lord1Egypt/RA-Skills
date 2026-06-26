#!/usr/bin/env python3
"""
NamingAudit.py
Scan files/folders and report names not following:
- single words or word groups
- each token starts with an uppercase letter
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOKEN_RE = re.compile(r"^[A-Z][a-zA-Z0-9]*$")


def is_valid_name(name: str) -> bool:
    if not name or name in {".", ".."}:
        return False
    tokens = [tok for tok in re.split(r"[\s_-]+", name) if tok]
    return all(TOKEN_RE.fullmatch(tok) for tok in tokens)


def suggest(name: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9\s_-]", " ", name)
    parts = [p for p in re.split(r"[\s_-]+", clean) if p]
    if not parts:
        return "Unnamed"
    fixed = [p[:1].upper() + p[1:] for p in parts]
    return "-".join(fixed)


def should_skip(path_parts: tuple[str, ...], include_hidden: bool) -> bool:
    if any(part in {".git", "__pycache__"} for part in path_parts):
        return True
    if not include_hidden and any(part.startswith(".") for part in path_parts):
        return True
    return False


def scan(root: Path, include_hidden: bool = False) -> list[dict]:
    issues: list[dict] = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if should_skip(rel.parts, include_hidden):
            continue

        target = p.stem if p.is_file() else p.name
        if is_valid_name(target):
            continue

        issues.append(
            {
                "path": str(rel),
                "type": "file" if p.is_file() else "folder",
                "current": p.name,
                "suggested": suggest(p.stem) + (p.suffix if p.is_file() else ""),
            }
        )
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-hidden", action="store_true")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    issues = scan(root, include_hidden=args.include_hidden)

    if args.json:
        print(json.dumps({"root": str(root), "count": len(issues), "issues": issues}, ensure_ascii=False, indent=2))
        return

    print(f"Root: {root}")
    print(f"Invalid Names: {len(issues)}")
    for idx, item in enumerate(issues, 1):
        print(f"{idx}. [{item['type']}] {item['path']}")
        print(f"   current:   {item['current']}")
        print(f"   suggested: {item['suggested']}")


if __name__ == "__main__":
    main()
