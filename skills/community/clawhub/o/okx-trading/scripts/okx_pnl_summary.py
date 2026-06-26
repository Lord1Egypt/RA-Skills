#!/usr/bin/env python3
"""Daily-digest helper: total equity, open positions, 24h fills, today's notional usage.

Designed to be the body of a scheduled morning Telegram message.
"""
from __future__ import annotations

import sys
import time

from _guardrails import summary as guardrail_summary
from _okx_client import account_api, env_summary, trade_api
from _pending import list_strategies


def main() -> int:
    acct = account_api()
    trd = trade_api()

    print(env_summary())
    print(guardrail_summary())
    print()

    # Equity
    bal = acct.get_account_balance()
    if bal.get("code") == "0" and bal.get("data"):
        print(f"Total equity (USDT-est): {bal['data'][0].get('totalEq', '0')}")
    else:
        print(f"Balance error: {bal.get('msg')!r}")

    # Open positions across non-spot instTypes
    pos = acct.get_positions()
    if pos.get("code") == "0":
        rows = pos.get("data") or []
        if rows:
            print(f"\nOpen positions ({len(rows)}):")
            for p in rows:
                print(
                    f"  {p.get('instId',''):<14} {p.get('posSide',''):<5} "
                    f"pos={p.get('pos','')} avgPx={p.get('avgPx','')} upl={p.get('upl','')}"
                )
        else:
            print("\nNo open positions.")
    else:
        print(f"\nPositions error: {pos.get('msg')!r}")

    # 24h fills (spot)
    since_ms = str(int((time.time() - 24 * 3600) * 1000))
    fills_resp = trd.get_fills_history(instType="SPOT", begin=since_ms, limit="100")
    if fills_resp.get("code") == "0":
        fills = fills_resp.get("data") or []
        print(f"\nLast 24h spot fills: {len(fills)}")
        realized = 0.0
        for f in fills:
            sz = float(f.get("fillSz") or 0)
            px = float(f.get("fillPx") or 0)
            side = f.get("side", "")
            notional = sz * px
            sign = -1.0 if side == "buy" else 1.0
            realized += sign * notional
            print(
                f"  {f.get('ts',''):<14} {f.get('instId',''):<14} {side:<4} "
                f"sz={sz} px={px} fee={f.get('fee','')}"
            )
        print(f"\nNet 24h spot flow (sells - buys, USDT-equiv): {realized:.2f}")
    else:
        print(f"\nFills error: {fills_resp.get('msg')!r}")

    # Active strategies (grids etc.)
    strategies = list_strategies()
    if strategies:
        print(f"\nActive strategies ({len(strategies)}):")
        for s in strategies:
            print(f"  {s.get('id','?')} {s.get('kind','?')} {s.get('instId','')}")
    else:
        print("\nNo active strategies.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
