#!/usr/bin/env python3
"""
Remove local Python build artifacts before publishing the plugin or skill package.
"""

from __future__ import annotations

from pathlib import Path
import shutil

SKIP_DIRS = {".git", "node_modules"}


def resolve_root() -> Path:
    """Clean the whole plugin when run from the repo; only the skill when installed standalone."""
    skill_root = Path(__file__).resolve().parents[1]
    plugin_root = skill_root.parents[1]
    return plugin_root if (plugin_root / ".plugin" / "plugin.json").is_file() else skill_root


def main() -> int:
    root = resolve_root()
    removed = 0

    def skipped(path: Path) -> bool:
        return any(part in SKIP_DIRS for part in path.relative_to(root).parts)

    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir() and not skipped(cache_dir):
            file_count = sum(1 for p in cache_dir.rglob("*") if p.is_file())
            shutil.rmtree(cache_dir, ignore_errors=True)
            removed += file_count
            removed += 1

    for pyc in root.rglob("*.pyc"):
        if skipped(pyc):
            continue
        pyc.unlink(missing_ok=True)
        removed += 1

    print(f"cleaned_artifacts={removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
