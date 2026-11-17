#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "references" / "council_roster.json").read_text(encoding="utf-8"))
for c in data["champions"]:
    print(f"{c['champion_id']:12}  {c['egg_id']:22}  {c.get('name', '')[:48]}")