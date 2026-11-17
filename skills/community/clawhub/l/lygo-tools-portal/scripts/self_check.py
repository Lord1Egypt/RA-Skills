#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for rel in (
    "SKILL.md",
    "references/TOOLS_MANIFEST.json",
    "references/SECURITY.md",
    "references/AGENT_CONTRACT.md",
    "scripts/resolve_tool.py",
):
    if not (ROOT / rel).exists():
        print("MISSING", rel)
        raise SystemExit(2)
data = json.loads((ROOT / "references/TOOLS_MANIFEST.json").read_text(encoding="utf-8"))
if not data.get("public_pages"):
    print("manifest empty public_pages")
    raise SystemExit(2)
bpm = next((p for p in data["public_pages"] if p.get("id") == "lygo-bpm-finder"), None)
if not bpm or "stack" not in bpm.get("urls", {}):
    print("bpm finder entry incomplete")
    raise SystemExit(2)
print("OK lygo-tools-portal")
raise SystemExit(0)