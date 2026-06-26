#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def should_include(path: Path) -> bool:
    excluded_names = {"dist", "__pycache__", ".git"}
    excluded_suffixes = {".zip", ".pyc", ".pyo"}
    if any(part in excluded_names for part in path.parts):
        return False
    if path.name in {".DS_Store"}:
        return False
    if path.suffix.lower() in excluded_suffixes:
        return False
    return True


def load_version(skill_root: Path) -> str:
    version_file = skill_root / "VERSION.txt"
    version = version_file.read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError("VERSION.txt 文件不能为空")
    return version


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    project_root = skill_root.parents[2]

    version = load_version(skill_root)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = project_root / f"hopola-clawhub-v{version}-{ts}.zip"

    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for p in skill_root.rglob("*"):
            if not p.is_file():
                continue
            if not should_include(p):
                continue
            rel = p.relative_to(skill_root)
            zf.write(p, rel.as_posix())

    print(f"build_release_zip: PASS {zip_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
