#!/usr/bin/env python3
"""Create an isolated venv on first run, then execute the PDF exporter."""

from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VENV_DIR = SCRIPT_DIR / "venv"
VENV_PYTHON = VENV_DIR / "bin/python"
EXPORT_SCRIPT = SCRIPT_DIR / "export_pdf.py"
REQUIREMENTS_FILE = SCRIPT_DIR / "requirements.txt"


def ensure_environment() -> None:
    if VENV_PYTHON.exists():
        return

    print("Initializing export environment...", file=sys.stderr)
    try:
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    except Exception as exc:  # pragma: no cover - surfaces platform setup issues clearly
        raise RuntimeError(
            "Failed to create the PDF export virtual environment. "
            "Make sure Python 3 venv support is installed."
        ) from exc

    subprocess.check_call(
        [
            str(VENV_PYTHON),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--requirement",
            str(REQUIREMENTS_FILE),
        ],
        cwd=SCRIPT_DIR,
    )


def main() -> None:
    ensure_environment()
    os.execv(
        str(VENV_PYTHON),
        [str(VENV_PYTHON), str(EXPORT_SCRIPT), *sys.argv[1:]],
    )


if __name__ == "__main__":
    main()
