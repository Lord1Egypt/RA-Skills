#!/usr/bin/env python3
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    equity = float(payload["equity"])
    risk_pct = float(payload["risk_pct"])
    entry = float(payload["entry_price"])
    stop = float(payload["stop_loss"])
    leverage = float(payload["leverage"])
    stop_distance_pct = abs(entry - stop) / entry if entry else 0.0
    risk_usd = equity * risk_pct
    notional = 0.0 if stop_distance_pct == 0 else (risk_usd / stop_distance_pct)
    margin = notional / leverage if leverage else 0.0
    quantity = notional / entry if entry else 0.0
    print(json.dumps({
        "risk_usd": risk_usd,
        "stop_distance_pct": stop_distance_pct,
        "notional": notional,
        "margin": margin,
        "quantity": quantity,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
