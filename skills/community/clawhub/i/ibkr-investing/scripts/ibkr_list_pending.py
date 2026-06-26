#!/usr/bin/env python3
"""List currently pending (unconfirmed, unexpired) IBKR proposals."""
from __future__ import annotations

import sys

from _pending import list_pending


def main() -> int:
    rows = list_pending()
    if not rows:
        print("No pending proposals.")
        return 0
    print(f"Pending proposals ({len(rows)}):")
    for r in rows:
        payload = r.get("payload") or {}
        print(
            f"  {r['id']}  {payload.get('side','?'):>4} {payload.get('symbol','?'):<8} "
            f"shares={payload.get('shares','?')}  ~${payload.get('notional_usd','?')} "
            f"(ref=${payload.get('ref_price','?')})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
