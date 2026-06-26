#!/usr/bin/env python3
"""Package the music-education-research-writer skill as .zip, .skill, or both."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from typing import Iterable, List

from validate_skill import validate_skill_root

PACKAGE_NAME = "music-education-research-writer"


def iter_package_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if any(part in {"dist", "__pycache__"} for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix == ".pyc":
            continue
        yield path


def write_archive(root: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in iter_package_files(root):
            arcname = Path(root.name) / file_path.relative_to(root)
            archive.write(file_path, arcname.as_posix())


def package_skill(root: Path, output_dir: Path, fmt: str) -> List[Path]:
    ok, errors = validate_skill_root(root)
    if not ok:
        joined = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Validation failed:\n{joined}")

    outputs: List[Path] = []

    if fmt in {"zip", "both"}:
        zip_path = output_dir / f"{PACKAGE_NAME}.zip"
        write_archive(root, zip_path)
        outputs.append(zip_path)

    if fmt in {"skill", "both"}:
        skill_path = output_dir / f"{PACKAGE_NAME}.skill"
        write_archive(root, skill_path)
        outputs.append(skill_path)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Package the skill as zip, .skill, or both.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the skill root. Defaults to current directory.")
    parser.add_argument(
        "--format",
        choices=("zip", "skill", "both"),
        default="both",
        help="Archive format to generate. Defaults to both.",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Output directory for archive files. Defaults to ./dist relative to the skill root.",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir

    try:
        outputs = package_skill(root, output_dir, args.format)
    except ValueError as exc:
        print(exc)
        return 1

    for output in outputs:
        print(f"Created archive: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
