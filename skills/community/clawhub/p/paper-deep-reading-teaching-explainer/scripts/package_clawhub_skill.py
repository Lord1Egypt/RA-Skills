#!/usr/bin/env python3
"""Package this skill folder as a ClawHub-ready zip and .skill file."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import zipfile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    parser.add_argument("--slug", default=None)
    parser.add_argument("--version", default=None)
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    slug = args.slug or skill_dir.name
    version = args.version or "0.0.0"
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    zip_path = out_dir / f"{slug}-v{version}-clawhub.zip"
    skill_path = out_dir / f"{slug}-v{version}.skill"

    ignore = {"__pycache__", ".DS_Store", "dist", ".clawhubignore", "LICENSE"}
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in skill_dir.rglob("*"):
            rel = path.relative_to(skill_dir.parent)
            if any(part in ignore for part in rel.parts):
                continue
            if path.suffix.lower() in {".zip", ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pptx", ".docx", ".xlsx"}:
                continue
            if path.is_file():
                zf.write(path, rel.as_posix())

    shutil.copyfile(skill_dir / "SKILL.md", skill_path)
    print(zip_path)
    print(skill_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
