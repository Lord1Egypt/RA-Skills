#!/usr/bin/env python3
"""Run neomano-x using the skill-local venv.

Usage:
  python3 run.py <dry-run|publish> --text "..." --image "/path.jpg"

Creates a helpful error if the venv is missing.
"""

import subprocess
import sys
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parents[1]
    venv_py = base_dir / ".venv" / "bin" / "python"
    if not venv_py.exists():
        raise SystemExit(
            f"ERROR: venv not found at {venv_py}. Run: python3 {base_dir}/scripts/bootstrap_venv.py"
        )
    target = base_dir / "scripts" / "x_post.py"
    cmd = [str(venv_py), str(target), *sys.argv[1:]]
    print("+", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
