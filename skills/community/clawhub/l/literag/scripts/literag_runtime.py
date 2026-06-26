#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PREFERRED_PYTHON_CANDIDATES = [
    os.environ.get("LITERAG_PYTHON"),
    "/opt/homebrew/bin/python3",
    sys.executable,
    "python3",
]


def preferred_python() -> str:
    for candidate in PREFERRED_PYTHON_CANDIDATES:
        if not candidate:
            continue
        path = Path(candidate)
        if path.is_absolute():
            if path.exists() and os.access(path, os.X_OK):
                return str(path)
            continue
        return candidate
    return sys.executable
