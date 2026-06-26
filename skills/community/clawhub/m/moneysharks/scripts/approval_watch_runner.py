#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone


def main() -> int:
    payload = json.load(sys.stdin)
    out = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": payload.get("mode", "approval"),
        "status": "WATCHING_MARKET",
        "action": "scan-journal-propose",
        "note": "Always-on safe loop: scan market, journal decisions, and emit approval-gated proposals only."
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
