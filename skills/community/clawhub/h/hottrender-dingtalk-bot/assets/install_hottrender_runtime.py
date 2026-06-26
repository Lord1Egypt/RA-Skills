#!/usr/bin/env python3
"""Install the bundled HotTrender runtime into a target directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install bundled HotTrender runtime.")
    parser.add_argument("--target", required=True, help="Destination directory for the runtime copy.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing target directory.")
    return parser.parse_args()


def copy_runtime(source: Path, target: Path, force: bool) -> None:
    if target.exists():
        if not force:
            raise SystemExit(f"target already exists: {target}; pass --force to overwrite")
        shutil.rmtree(target)
    shutil.copytree(source, target)
    (target / "out").mkdir(parents=True, exist_ok=True)
    env_example = target / ".env.example"
    env_file = target / ".env"
    if env_example.exists() and not env_file.exists():
        shutil.copy2(env_example, env_file)


def main() -> None:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    source = skill_dir / "assets" / "hottrender-runtime"
    if not source.exists():
        raise SystemExit(f"runtime bundle not found: {source}")
    target = Path(args.target).expanduser().resolve()
    copy_runtime(source, target, args.force)
    print(f"installed HotTrender runtime -> {target}")
    print("next:")
    print(f"  cd {target}")
    print("  python -m venv .venv")
    print("  . .venv/bin/activate")
    print("  pip install -r requirements.txt")
    print("  python scripts/fetch_daily_trends.py --output out/daily_trends.md")


if __name__ == "__main__":
    main()
