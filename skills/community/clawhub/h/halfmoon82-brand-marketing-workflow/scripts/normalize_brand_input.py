#!/usr/bin/env python3
"""Normalize loose brand input into a structured brief skeleton."""
from __future__ import annotations
import json
import sys
from pathlib import Path

DEFAULTS = {
    "brand_name": "",
    "brand_positioning": "",
    "brand_tone": "",
    "target_audience": [],
    "use_cases": [],
    "channels": [],
    "content_goals": [],
    "brand_dos": [],
    "brand_donts": [],
    "competitor_scope": [],
    "kpis": [],
    "constraints": {
        "budget": "",
        "language": "zh-CN",
        "region": "",
        "compliance": "public+authorized-only"
    }
}

def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps(DEFAULTS, ensure_ascii=False, indent=2))
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"brand_name": raw}
    out = DEFAULTS | {k: payload.get(k, v) for k, v in DEFAULTS.items() if k != "constraints"}
    constraints = DEFAULTS["constraints"] | payload.get("constraints", {})
    out["constraints"] = constraints
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
