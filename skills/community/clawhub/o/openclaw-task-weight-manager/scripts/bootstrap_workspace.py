#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def copy_if_missing(src: Path, dst: Path) -> bool:
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return True


def main() -> int:
    workspace = Path.cwd()
    target_dir = workspace / "task-weight-manager"

    created = []
    created.append(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if copy_if_missing(ASSETS / "thread-board-template.md", target_dir / "threads.md"):
        created.append(target_dir / "threads.md")
    if copy_if_missing(ASSETS / "decisions-template.md", target_dir / "decisions.md"):
        created.append(target_dir / "decisions.md")
    if copy_if_missing(ASSETS / "HEARTBEAT.example.md", workspace / "HEARTBEAT.md"):
        created.append(workspace / "HEARTBEAT.md")

    print("Bootstrapped Task Weight Manager files:")
    for path in created:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
