#!/usr/bin/env python3
"""Remove generated Python cache files that pollute validator scans."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def clean(root: Path) -> list[Path]:
    removed: list[Path] = []
    for path in sorted(root.rglob("__pycache__")):
        if path.is_dir():
            shutil.rmtree(path)
            removed.append(path)
    for path in sorted(root.rglob("*.pyc")):
        if path.exists():
            path.unlink()
            removed.append(path)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to clean.")
    parser.add_argument("--check", action="store_true", help="Fail if generated files are present; do not delete.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    paths = sorted(list(root.rglob("__pycache__")) + list(root.rglob("*.pyc")))
    if args.check:
        if paths:
            for path in paths:
                print(path.relative_to(root))
            return 1
        print("No generated Python cache files found.")
        return 0
    removed = clean(root)
    print(f"Removed {len(removed)} generated Python cache path(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
