#!/usr/bin/env python3
"""Run code-audit helper script tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    basetemp = skill_dir / ".pytest-tmp"
    return subprocess.call(
        [
            sys.executable,
            "-m",
            "pytest",
            str(skill_dir / "tests"),
            "--basetemp",
            str(basetemp),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
