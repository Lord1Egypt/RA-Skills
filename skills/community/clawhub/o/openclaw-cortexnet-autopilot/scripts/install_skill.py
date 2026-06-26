#!/usr/bin/env python3
"""Install this skill into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def default_target_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME", "").strip()
    if codex_home:
        return Path(codex_home).expanduser().resolve() / "skills"
    return Path.home() / ".codex" / "skills"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Install openclaw-cortexnet-autopilot skill locally")
    p.add_argument("--target-root", default=None, help="Target skills root (default: $CODEX_HOME/skills or ~/.codex/skills)")
    p.add_argument("--name", default="openclaw-cortexnet-autopilot", help="Installed skill folder name")
    p.add_argument("--force", action="store_true", help="Overwrite existing destination folder")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    if not (skill_root / "SKILL.md").exists():
        print(f"[ERROR] invalid skill root: {skill_root}")
        return 2

    target_root = Path(args.target_root).expanduser().resolve() if args.target_root else default_target_root()
    target_root.mkdir(parents=True, exist_ok=True)
    dest = target_root / args.name

    if dest.exists():
        if not args.force:
            print(f"[ERROR] destination exists (use --force): {dest}")
            return 3
        shutil.rmtree(dest)

    shutil.copytree(
        skill_root,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store"),
    )
    print(f"[OK] installed skill to: {dest}")
    print(f"[NEXT] use in Codex prompt: Use $openclaw-cortexnet-autopilot from {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
