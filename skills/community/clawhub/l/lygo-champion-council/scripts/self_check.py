#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = [ROOT / "SKILL.md", ROOT / "references" / "council_roster.json", ROOT / "references" / "SECURITY.md"]
for p in REQ:
    if not p.is_file():
        print("MISSING", p)
        raise SystemExit(3)
data = json.loads((ROOT / "references" / "council_roster.json").read_text(encoding="utf-8"))
if data.get("count", 0) < 15:
    print("BAD_ROSTER count", data.get("count"))
    raise SystemExit(2)
print("OK council", data["count"])
raise SystemExit(0)