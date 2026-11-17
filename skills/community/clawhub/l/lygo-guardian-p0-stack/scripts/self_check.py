#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = [
    ROOT / "SKILL.md",
    ROOT / "references" / "SECURITY.md",
    ROOT / "src" / "guardian" / "integration_api.py",
    ROOT / "scripts" / "run_byte_gate.py",
]
missing = [str(p) for p in REQ if not p.exists()]
if missing:
    print("MISSING", missing)
    raise SystemExit(2)
print("OK")
raise SystemExit(0)