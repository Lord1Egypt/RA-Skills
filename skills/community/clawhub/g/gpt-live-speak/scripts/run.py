#!/usr/bin/env python3

import hashlib
import os
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
REQUIREMENTS = SKILL_DIR / "requirements.txt"

cache_home = Path(
    os.environ.get(
        "XDG_CACHE_HOME",
        Path.home() / ".cache",
    )
)

CACHE_DIR = cache_home / "openclaw" / "speak"
VENV_DIR = CACHE_DIR / "venv"
STAMP = CACHE_DIR / "requirements.sha256"

PYTHON = VENV_DIR / "bin" / "python"
SPEAK_SCRIPT = SKILL_DIR / "scripts" / "speak.py"


def requirements_hash():
    return hashlib.sha256(
        REQUIREMENTS.read_bytes()
    ).hexdigest()


def ensure_runtime():
    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not PYTHON.exists():
        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(VENV_DIR),
            ],
            check=True,
        )

    wanted = requirements_hash()

    installed = (
        STAMP.read_text().strip()
        if STAMP.exists()
        else None
    )

    if installed != wanted:
        subprocess.run(
            [
                str(PYTHON),
                "-m",
                "pip",
                "install",
                "-q",
                "--disable-pip-version-check",
                "-r",
                str(REQUIREMENTS),
            ],
            check=True,
        )

        STAMP.write_text(
            wanted + "\n"
        )


def main():
    ensure_runtime()

    os.execv(
        str(PYTHON),
        [
            str(PYTHON),
            str(SPEAK_SCRIPT),
            *sys.argv[1:],
        ],
    )


if __name__ == "__main__":
    main()
