#!/usr/bin/env python3
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    order = {
        "symbol": payload["symbol"],
        "side": payload["side"],
        "type": payload.get("type", "MARKET"),
        "quantity": payload["quantity"],
        "leverage": payload["leverage"],
        "stop_loss": payload.get("stop_loss"),
        "take_profit": payload.get("take_profit"),
    }
    print(json.dumps(order, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
