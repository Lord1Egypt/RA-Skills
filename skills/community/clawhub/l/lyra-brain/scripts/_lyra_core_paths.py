"""Resolve LYRA_CORE root for lyra-brain scripts (v2.1.0 — explicit path only)."""
from __future__ import annotations

import os
from pathlib import Path


def lyra_core_root() -> Path:
    """Require operator-set env. No silent drive-letter / multi-user discovery."""
    for key in ("LYRA_CORE_ROOT", "LYRA_CORE"):
        v = (os.environ.get(key) or "").strip()
        if not v:
            continue
        p = Path(v)
        if (p / "modules" / "lyra_brain.py").is_file():
            return p.resolve()
        raise RuntimeError(
            f"{key}={p} does not contain modules/lyra_brain.py — fix path or unset"
        )
    raise RuntimeError(
        "LYRA_CORE_ROOT is required. Set it to the directory containing modules/lyra_brain.py "
        "(example: export LYRA_CORE_ROOT=/path/to/LYRA_CORE). "
        "This skill will not auto-scan other users' homes or drive letters."
    )
