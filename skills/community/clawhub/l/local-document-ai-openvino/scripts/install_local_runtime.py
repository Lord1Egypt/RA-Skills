#!/usr/bin/env python3
"""
Install runtime dependencies into the skill-local .vendor directory.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def run_install() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    vendor_dir = base_dir / ".vendor"
    tmp_dir = base_dir / "tmp" / "pip"
    requirements = base_dir / "requirements.txt"

    vendor_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["TMP"] = str(tmp_dir)
    env["TEMP"] = str(tmp_dir)
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--target",
        str(vendor_dir),
        "-r",
        str(requirements),
    ]
    proc = subprocess.run(cmd, env=env)
    if proc.returncode != 0:
        return proc.returncode

    if os.name == "nt":
        username = os.environ.get("USERNAME")
        if username:
            subprocess.run(
                [
                    "icacls",
                    str(vendor_dir),
                    "/grant",
                    f"{username}:(OI)(CI)F",
                    "/T",
                    "/C",
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(run_install())
