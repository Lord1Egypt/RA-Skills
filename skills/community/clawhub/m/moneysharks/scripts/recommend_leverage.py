#!/usr/bin/env python3
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    min_lev = float(payload["min_leverage"])
    max_lev = float(payload["max_leverage"])
    confidence = float(payload.get("confidence", 0))
    high_vol = bool(payload.get("high_volatility", False))
    if confidence < 0.6:
        lev = min_lev
    elif confidence < 0.8:
        lev = (min_lev + max_lev) / 2
    else:
        lev = max_lev
    if high_vol:
        lev = max(min_lev, lev - 1)
    print(json.dumps({"recommended_leverage": lev}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
