#!/usr/bin/env python3
"""Mirror self-check (install smoke)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACK = Path(os.environ.get("LYGO_STACK_ROOT", "")).expanduser()

REQ_MIRROR = [
    ROOT / "SKILL.md",
    ROOT / "references" / "SECURITY.md",
]

missing = [str(p) for p in REQ_MIRROR if not p.exists()]
if missing:
    print("MISSING mirror", missing)
    raise SystemExit(2)

if STACK.is_dir():
    req_stack = [
        STACK / "pxpipe_lygo" / "compressor.py",
        STACK / "tools" / "pxpipe_lygo_for_agent.py",
        STACK / "docs" / "BIOPHASE7_PXPIPE_LYGO.md",
    ]
    miss_stack = [str(p) for p in req_stack if not p.exists()]
    if miss_stack:
        print("WARN LYGO_STACK_ROOT set but missing", miss_stack)
else:
    print("OK mirror (set LYGO_STACK_ROOT to verify stack paths)")

print("OK")
raise SystemExit(0)