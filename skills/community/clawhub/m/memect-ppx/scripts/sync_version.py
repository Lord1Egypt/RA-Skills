#!/usr/bin/env python3
"""Sync this ClawHub skill version from the repository pyproject.toml."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = SKILL_DIR.parents[1]
PYPROJECT = ROOT / "pyproject.toml"
SKILL = SKILL_DIR / "SKILL.md"


def read_project_version() -> str:
    with PYPROJECT.open("rb") as f:
        data = tomllib.load(f)
    version = data["project"]["version"]
    if not isinstance(version, str) or not version.strip():
        raise ValueError("project.version must be a non-empty string")
    return version.strip()


def sync_skill_version(version: str) -> bool:
    text = SKILL.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^version:\s*.*$", f"version: {version}", text, count=1)
    if count != 1:
        raise ValueError(f"expected exactly one version field in {SKILL}")
    if updated == text:
        return False
    SKILL.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    version = read_project_version()
    changed = sync_skill_version(version)
    status = "updated" if changed else "already up to date"
    print(f"{SKILL.relative_to(ROOT)}: {status} ({version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
