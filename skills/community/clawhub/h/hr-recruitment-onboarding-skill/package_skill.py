"""Build a distributable archive for the HR recruitment JD Skill."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ARCHIVE_NAME = "hr-recruitment-jd-skill.zip"
EXCLUDED_PARTS = {".git", "workspace", "__pycache__", ".pytest_cache", "dist"}


def _is_excluded(relative: Path) -> bool:
    name = relative.name
    return any(part in EXCLUDED_PARTS for part in relative.parts) or (
        name == ".env" or name.startswith(".env.") or name.endswith(".env")
    )


def package_skill(source_root: Path, output_dir: Path) -> Path:
    """Package source files while excluding runtime, cache, and secret data."""
    source_root = Path(source_root).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ARCHIVE_NAME

    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(source_root.rglob("*")):
            relative = path.relative_to(source_root)
            if path.is_file() and not _is_excluded(relative):
                archive.write(path, relative.as_posix())

    return archive_path


def main(argv: list[str] | None = None) -> int:
    """Parse package options, build the archive, and print its path."""
    source_root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=source_root.parent / "dist",
        help="directory in which to write the Skill archive",
    )
    arguments = parser.parse_args(argv)

    print(package_skill(source_root, arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
