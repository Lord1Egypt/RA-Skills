#!/usr/bin/env python3
"""Mirror install smoke check."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACK = Path(os.environ.get("LYGO_STACK_ROOT", "")).expanduser()

REQ = [
    ROOT / "SKILL.md",
    ROOT / "references" / "AGENT_CONTRACT.md",
    ROOT / "references" / "SECURITY.md",
    ROOT / "scripts" / "verify_anchors.py",
    ROOT / "scripts" / "_stack_paths.py",
]
missing = [str(p) for p in REQ if not p.exists()]
if missing:
    print("MISSING", missing)
    raise SystemExit(2)

if STACK.is_dir():
    stack_req = [
        STACK / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json",
        STACK / "tools" / "lygo_network_builder_verify.py",
    ]
    miss = [str(p) for p in stack_req if not p.exists()]
    if miss:
        print("WARN stack", miss)
else:
    print("OK mirror (set LYGO_STACK_ROOT for stack paths)")

print("OK")
raise SystemExit(0)