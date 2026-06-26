#!/usr/bin/env python3
"""Package a validated skill directory into a zip archive."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from validate_skill import validate_skill

IGNORED_NAMES = {
    ".DS_Store",
}
IGNORED_DIRS = {
    ".git",
    "__pycache__",
}


def iter_files(skill_dir: Path):
    for path in skill_dir.rglob("*"):
        if path.name in IGNORED_NAMES:
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed: {path}")
        if path.is_file():
            yield path


def package_skill(skill_dir: Path, output_dir: Path | None) -> Path:
    errors = validate_skill(skill_dir)
    if errors:
        raise ValueError("Validation failed:\n- " + "\n- ".join(errors))

    target_dir = (output_dir or skill_dir.parent).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    archive_path = target_dir / f"{skill_dir.name}.skill.zip"

    with ZipFile(archive_path, "w", ZIP_DEFLATED) as zf:
        for path in iter_files(skill_dir):
            zf.write(path, path.relative_to(skill_dir))
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a skill directory into a zip archive.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("output_dir", nargs="?", help="Optional output directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] Not a directory: {skill_dir}")
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None

    try:
        archive = package_skill(skill_dir, output_dir)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"[OK] Created archive at {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
