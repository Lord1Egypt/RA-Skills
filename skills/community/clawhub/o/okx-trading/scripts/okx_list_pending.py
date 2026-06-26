#!/usr/bin/env python3
"""List currently pending (unconfirmed, unexpired) proposals."""
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
        kind = r.get("kind", "?")
        payload = r.get("payload") or {}
        if kind == "trade":
            print(
                f"  {r['id']}  TRADE  {payload.get('side','?').upper()} {payload.get('instId','?')} "
                f"~{payload.get('notional_usdt','?')} USDT (ref={payload.get('ref_price','?')})"
            )
        elif kind == "grid":
            print(
                f"  {r['id']}  GRID   {payload.get('instId','?')}  "
                f"[{payload.get('low','?')}–{payload.get('high','?')}] x {payload.get('levels','?')} levels, "
                f"{payload.get('quote_sz_per_level','?')} USDT/level"
            )
        else:
            print(f"  {r['id']}  {kind}  (unknown payload)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
