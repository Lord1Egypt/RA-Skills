#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENGINE_DIR = SCRIPT_DIR / 'engine'
VENV_DIR = ENGINE_DIR / '.venv'
REQUIREMENTS = ENGINE_DIR / 'requirements.txt'


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    if not REQUIREMENTS.exists():
        raise FileNotFoundError(f'Requirements file not found: {REQUIREMENTS}')
    if not VENV_DIR.exists():
        run([sys.executable, '-m', 'venv', str(VENV_DIR)])
    python_bin = VENV_DIR / 'bin/python'
    run([str(python_bin), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([str(python_bin), '-m', 'pip', 'install', '-r', str(REQUIREMENTS)])
    print(str(python_bin))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
