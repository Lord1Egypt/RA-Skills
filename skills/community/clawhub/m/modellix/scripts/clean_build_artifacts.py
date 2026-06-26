#!/usr/bin/env python3
"""
Remove local Python build artifacts before publishing the skill package.
"""

from __future__ import annotations

from pathlib import Path
import shutil


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    removed = 0

    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            file_count = sum(1 for p in cache_dir.rglob("*") if p.is_file())
            shutil.rmtree(cache_dir, ignore_errors=True)
            removed += file_count
            removed += 1

    for pyc in root.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)
        removed += 1

    print(f"cleaned_artifacts={removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
