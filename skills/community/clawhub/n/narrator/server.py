#!/usr/bin/env python3
"""
Compatibility launcher for narrator skill.

The canonical implementation is the full upstream repo at /Users/buddy/narrator.
This shim forwards directly to it so all runtime behavior stays in one place.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _repo_python() -> tuple[Path, Path]:
    repo_dir = Path('/Users/buddy/narrator').resolve()
    if not repo_dir.exists():
        print(f"[narrator] Canonical repo not found: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    venv_python = repo_dir / '.venv' / 'bin' / 'python'
    if not venv_python.exists():
        print(
            f"[narrator] Python venv not found: {venv_python}\n"
            f"[narrator] Run: cd {repo_dir} && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    return repo_dir, venv_python


def main() -> None:
    repo_dir, python_bin = _repo_python()

    # Backward compatibility: if this is invoked with a style arg, forward it;
    # otherwise default to sports.
    args = sys.argv[1:] or ['sports']
    cmd = [str(python_bin), '-m', 'narrator'] + args

    env = os.environ.copy()
    env['PYTHONPATH'] = str(repo_dir)

    proc = subprocess.run(cmd, cwd=str(repo_dir), env=env)
    sys.exit(proc.returncode)


if __name__ == '__main__':
    main()
