#!/usr/bin/env python3
"""OpenClaw adapter for the shared go-next-move-core package."""

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
VENDORED_DEPENDENCIES = SCRIPT_DIR / "_vendor"
MONOREPO_ROOT = SCRIPT_DIR.parents[2]

# Keep the published, verified Skill tree free of runtime cache files.
sys.dont_write_bytecode = True

dependency_root = (
    VENDORED_DEPENDENCIES
    if (VENDORED_DEPENDENCIES / "go_next_move_core").is_dir()
    else MONOREPO_ROOT
)
if (dependency_root / "go_next_move_core").is_dir():
    dependency_path = str(dependency_root)
    sys.path[:] = [entry for entry in sys.path if entry != dependency_path]
    sys.path.insert(0, dependency_path)

from go_next_move_core.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
