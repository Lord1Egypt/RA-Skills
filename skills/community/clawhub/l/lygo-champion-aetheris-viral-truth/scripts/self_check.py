"""Unified champion pack self-check — reads champion id from references/canon.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = [
    ROOT / "SKILL.md",
    ROOT / "references" / "canon.json",
    ROOT / "references" / "persona_pack.md",
    ROOT / "references" / "verifier_usage.md",
]

missing = [str(p) for p in REQ if not p.exists()]
if missing:
    print("MISSING_FILES:")
    for m in missing:
        print(" -", m)
    raise SystemExit(3)

canon = json.loads((ROOT / "references" / "canon.json").read_text(encoding="utf-8"))
champion = canon.get("champion")
if not champion or not isinstance(champion, str):
    print("BAD_CANON: champion missing")
    raise SystemExit(2)

vu = (ROOT / "references" / "verifier_usage.md").read_text(encoding="utf-8", errors="replace")
if "lygo-mint-verifier" not in vu.lower() and "clawhub" not in vu.lower():
    print("BAD_REF: verifier link missing")
    raise SystemExit(2)

h = canon.get("lygo_mint_sha256")
if h is not None and (not isinstance(h, str) or len(h) != 64):
    print("BAD_CANON: lygo_mint_sha256 invalid")
    raise SystemExit(2)

print("OK", champion)
raise SystemExit(0)