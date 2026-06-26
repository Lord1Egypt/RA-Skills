#!/usr/bin/env python3
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    proposal = {
        "symbol": payload["symbol"],
        "side": payload["side"],
        "confidence": payload.get("confidence"),
        "leverage": payload.get("leverage"),
        "quantity": payload.get("quantity"),
        "stop_loss": payload.get("stop_loss"),
        "take_profit": payload.get("take_profit"),
        "status": "PENDING_APPROVAL"
    }
    print(json.dumps(proposal, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
