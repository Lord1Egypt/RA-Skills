#!/usr/bin/env python3
"""
Bootstrap local runtime dependencies installed under the skill directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def bootstrap_local_vendor() -> list[str]:
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    python_tag = f"python{sys.version_info.major}.{sys.version_info.minor}"

    candidates: list[Path] = []
    env_vendor = os.environ.get("LOCAL_DOCUMENT_AI_VENDOR")
    if env_vendor:
        candidates.append(Path(env_vendor).expanduser())
    candidates.extend(
        [
            base_dir / ".vendor",
            base_dir / "vendor",
            base_dir / ".venv" / "Lib" / "site-packages",
            base_dir / ".venv" / "lib" / python_tag / "site-packages",
        ]
    )

    added: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate.is_dir():
            continue
        resolved = str(candidate.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved not in sys.path:
            sys.path.insert(0, resolved)
            added.append(resolved)
    return added
