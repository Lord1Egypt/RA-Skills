#!/usr/bin/env python3
"""Mirror install smoke check — no publish."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQ = [
    ROOT / "SKILL.md",
    ROOT / "references" / "SECURITY.md",
    ROOT / "references" / "AGENT_CONTRACT.md",
    ROOT / "references" / "LATTICE_MAP.md",
    ROOT / "references" / "MUSIC_PORTAL.json",
    ROOT / "references" / "SKILLSPECTOR_AUDIT.md",
    ROOT / "scripts" / "_stack_paths.py",
    ROOT / "scripts" / "portal_status.py",
    ROOT / "scripts" / "self_check.py",
]
missing = [str(p) for p in REQ if not p.exists()]
if missing:
    print("MISSING", missing)
    raise SystemExit(2)

portal = json.loads((ROOT / "references" / "MUSIC_PORTAL.json").read_text(encoding="utf-8"))
assert portal.get("public", {}).get("listen"), "listen URL required"
assert portal.get("public", {}).get("donate_paypal"), "paypal required"
assert portal.get("live_portals", {}).get("kick"), "kick required"

print(
    json.dumps(
        {
            "ok": True,
            "skill": "lygo-excavationpro-music-lattice",
            "version": portal.get("version"),
            "signature": portal.get("signature"),
            "listen": portal["public"]["listen"],
            "streams": portal["public"]["hf_streams"],
        },
        indent=2,
    )
)
print("OK lygo-excavationpro-music-lattice self_check")
raise SystemExit(0)
