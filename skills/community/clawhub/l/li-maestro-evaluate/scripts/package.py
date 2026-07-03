#!/usr/bin/env python3
"""Package li_maestro_evaluate skill as a ZIP archive."""

import json
import shutil
import sys
import time
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent.parent
    mf = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    version = mf.get("version", "0.0.0")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    zip_name = src.parent / f"li_maestro_evaluate-v{version}-{timestamp}"

    print(f"Packaging: {src}")
    print(f"Output:    {zip_name}.zip")

    # Files and directories to include
    includes = [
        "SKILL.md",
        "README.md",
        "manifest.json",
        "scripts/",
    ]

    def filter_func(path):
        p = Path(path)
        rel = p.relative_to(src).as_posix()
        for inc in includes:
            if inc.endswith("/") and rel.startswith(inc):
                return True
            if rel == inc:
                return True
        return False

    archive = shutil.make_archive(
        str(zip_name),
        "zip",
        root_dir=src,
        base_dir=".",
    )

    z = Path(archive)
    size_kb = z.stat().st_size / 1024
    print(f"Created:   {z.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
