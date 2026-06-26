#!/usr/bin/env python3
"""Create a local venv and install dependencies.

Why: This environment enforces PEP 668 (externally-managed Python), so we avoid
system-wide installs and keep dependencies isolated per-skill.
"""

import os
import subprocess
import sys
from pathlib import Path


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    base_dir = Path(__file__).resolve().parents[1]
    venv_dir = base_dir / ".venv"

    if not (venv_dir / "bin" / "python").exists():
        run([sys.executable, "-m", "venv", str(venv_dir)])

    py = str(venv_dir / "bin" / "python")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", "requests", "requests_oauthlib"])

    print(f"✓ venv ready at {venv_dir}")


if __name__ == "__main__":
    raise SystemExit(main())
