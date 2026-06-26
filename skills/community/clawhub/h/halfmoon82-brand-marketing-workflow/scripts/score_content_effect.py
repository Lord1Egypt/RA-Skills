#!/usr/bin/env python3
"""Score content effect with a simple transparent rubric."""
from __future__ import annotations
import json
import sys

RUBRIC = {
    "brand_consistency": 5,
    "channel_fit": 5,
    "clarity": 5,
    "actionability": 5,
}

def main() -> int:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    score = {k: RUBRIC[k] for k in RUBRIC}
    result = {
        "scores": score,
        "overall": sum(score.values()),
        "notes": payload.get("notes", "transparent placeholder scoring"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
