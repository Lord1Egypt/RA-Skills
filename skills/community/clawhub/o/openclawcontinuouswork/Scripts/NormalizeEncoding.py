#!/usr/bin/env python3
"""
NormalizeEncoding.py
Normalize text files to UTF-8 (no BOM) + LF to reduce write/parse errors.
"""

from __future__ import annotations

from pathlib import Path

TARGET_EXT = {".md", ".py", ".json", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {".git", "__pycache__"}


def normalize_file(path: Path) -> bool:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False

    text2 = text.replace("\r\n", "\n").replace("\r", "\n")
    new_raw = text2.encode("utf-8")

    if new_raw != path.read_bytes():
        path.write_bytes(new_raw)
        return True
    return False


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in TARGET_EXT:
            yield p


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    changed = 0
    for f in iter_files(root):
        if normalize_file(f):
            changed += 1
    print(f"Normalized files: {changed}")


if __name__ == "__main__":
    main()
