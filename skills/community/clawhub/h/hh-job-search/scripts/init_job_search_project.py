#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

TEMPLATES = [
    "README-START.md",
    "PROFILE.md",
    "TARGET_ROLES.md",
    "SEARCH_RULES.md",
    "SOURCES.md",
    "PIPELINE.md",
    "OUTREACH_RULES.md",
    "BLACKLIST.md",
]


def main():
    if len(sys.argv) != 2:
        print("Usage: init_job_search_project.py <target-dir>", file=sys.stderr)
        sys.exit(2)

    target = Path(sys.argv[1])
    root = Path(__file__).resolve().parent.parent
    tpl_dir = root / "assets" / "templates"
    target.mkdir(parents=True, exist_ok=True)
    (target / "applications").mkdir(exist_ok=True)
    (target / "exports").mkdir(exist_ok=True)
    (target / "logs").mkdir(exist_ok=True)

    for name in TEMPLATES:
        dst = target / name
        if not dst.exists():
            shutil.copy2(tpl_dir / name, dst)

    print(f"Initialized job-search project at {target}")


if __name__ == "__main__":
    main()
