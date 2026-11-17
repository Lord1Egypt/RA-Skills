#!/usr/bin/env python3
"""Package NovelForge into a distribution ZIP archive."""

import argparse
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from novelforge_engine import __version__

EXCLUDE_PATTERNS = {
    ".git",
    ".github",
    ".novelforge",
    "__pycache__",
    ".DS_Store",
    "dist",
    ".coverage",
    "htmlcov",
    "scratch",
}

EXCLUDE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".swp",
    ".swo",
}

def should_exclude(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    if any(p in EXCLUDE_PATTERNS or p.endswith("-workspace") for p in parts):
        return True
    if rel_path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False

def package_skill(output_path: Path = None) -> Path:
    version = __version__
    if output_path is None:
        dist_dir = ROOT / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        output_path = dist_dir / f"novelforge-{version}.zip"

    print(f"Packaging NovelForge v{version} to {output_path}...")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        file_count = 0
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if should_exclude(rel):
                continue
            zf.write(path, rel)
            file_count += 1

    size_kb = output_path.stat().st_size / 1024
    print(f"Successfully packaged {file_count} files ({size_kb:.1f} KB) -> {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package NovelForge into a ZIP archive")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output ZIP path")
    args = parser.parse_args()
    package_skill(args.output)
