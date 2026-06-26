#!/usr/bin/env python3
"""Step 4 of the grid gate: place the initial limit orders for a confirmed grid.

Strategy state lives at ~/.aeon/okx/strategies/<strategy_id>.json after this
script completes successfully. Subsequent fills are handled by
okx_grid_step.py without further confirmation.
"""
from __future__ import annotations

import argparse
import sys
import time

from _audit import append as audit_append
from _okx_client import trade_api
from _pending import (
    PendingError,
    delete_pending,
    load_pending,
    new_id,
    save_strategy,
    validate_token,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True)
    p.add_argument("--confirmation-token", required=True)
    args = p.parse_args()

    try:
        record = load_pending(args.id)
        validate_token(record, args.confirmation_token)
    except PendingError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 3
    if record.get("kind") != "grid":
        print(f"REFUSED: proposal {args.id} is kind={record.get('kind')!r}, not 'grid'", file=sys.stderr)
        return 3

    payload = record["payload"]
    inst_id = payload["instId"]
    quote_sz = float(payload["quote_sz_per_level"])
    api = trade_api()

    strategy_id = "grid-" + new_id()
    active_orders: list[dict] = []
    failures: list[dict] = []

    for level_idx, level_px in enumerate(payload["level_prices"]):
        if level_px >= payload["ref_price_at_propose"]:
            # Sells deferred until matching buys fill — recorded as pending levels.
            continue
        # Spot limit buy: sz is base currency.
        base_sz = quote_sz / level_px
        sz_str = f"{base_sz:.8f}".rstrip("0").rstrip(".")
        px_str = f"{level_px:.8f}".rstrip("0").rstrip(".")

        resp = api.place_order(
            instId=inst_id,
            tdMode="cash",
            side="buy",
            ordType="limit",
            sz=sz_str,
            px=px_str,
        )
        data = (resp.get("data") or [{}])[0]
        if resp.get("code") == "0" and data.get("sCode") == "0":
            active_orders.append({
                "level_idx": level_idx,
                "side": "buy",
                "px": level_px,
                "sz_base": base_sz,
                "ordId": data.get("ordId", ""),
                "placed_at_epoch": int(time.time()),
            })
        else:
            failures.append({
                "level_idx": level_idx,
                "level_px": level_px,
                "msg": data.get("sMsg") or resp.get("msg") or "unknown",
                "sCode": data.get("sCode") or resp.get("code"),
            })

    strategy = {
        "id": strategy_id,
        "kind": "grid",
        "instId": inst_id,
        "low": payload["low"],
        "high": payload["high"],
        "levels": payload["levels"],
        "level_prices": payload["level_prices"],
        "quote_sz_per_level": quote_sz,
        "ref_price_at_apply": payload["ref_price_at_propose"],
        "active_orders": active_orders,
        "history": [],
        "halted": False,
        "halt_reason": None,
        "created_at_epoch": int(time.time()),
        # v0.2.0 — risk + autonomy controls confirmed at setup time.
        "min_profit_gap": float(payload.get("min_profit_gap") or 0.0),
        "max_position_base": float(payload.get("max_position_base") or 0.0),
        "trailing_pct": float(payload.get("trailing_pct") or 0.0),
        "max_rescales": int(payload.get("max_rescales") or 0),
        "rescales_used": 0,
    }
    save_strategy(strategy_id, strategy)
    delete_pending(args.id)
    audit_append(
        "grid_applied",
        strategy_id=strategy_id,
        instId=inst_id,
        low=payload["low"],
        high=payload["high"],
        levels=payload["levels"],
        active_orders=len(active_orders),
        failures=len(failures),
        min_profit_gap=strategy["min_profit_gap"],
        max_position_base=strategy["max_position_base"],
        trailing_pct=strategy["trailing_pct"],
        max_rescales=strategy["max_rescales"],
    )

    print(f"Grid applied. strategy id: {strategy_id}")
    print(f"  instId           : {inst_id}")
    print(f"  active buy orders: {len(active_orders)}")
    if failures:
        print(f"  failed levels    : {len(failures)} — review manually:")
        for f in failures:
            print(f"    level={f['level_idx']} px={f['level_px']} sCode={f['sCode']} msg={f['msg']!r}")
    print(f"  state file       : ~/.aeon/okx/strategies/{strategy_id}.json")
    print()
    print(f"Schedule grid maintenance with: schedule_create every 5m  task 'Run okx_grid_step.py' notify=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
