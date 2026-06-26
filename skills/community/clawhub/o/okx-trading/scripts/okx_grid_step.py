#!/usr/bin/env python3
"""Maintain all active grids: detect filled orders, place opposite-side
re-stocking orders, halt grids that breach the daily notional cap, and (if
configured at setup time) auto-rescale the grid range when current price
drifts toward the band edge.

Designed to be called repeatedly by the aeon scheduler (every 5–15 minutes).
Idempotent: safe to call concurrently or after a missed tick.

Per-strategy autonomy controls (set at setup time, immutable afterwards):

    min_profit_gap    Refuse to place a sell restock priced below
                      avg_buy_px * (1 + gap). Default 0 (off).
    max_position_base Refuse to place a buy restock when the strategy's net
                      base inventory >= this. Default 0 (off).
    trailing_pct      When current price is within this fraction of either
                      band edge, recenter the grid on the current price
                      (preserving range size). Default 0 (halt instead).
    max_rescales      Hard ceiling on autonomous re-centers across the
                      grid's lifetime. Required when trailing_pct > 0.
"""
from __future__ import annotations

import sys
import time

from _audit import append as audit_append
from _guardrails import GuardrailError, check_daily_room
from _okx_client import market_api, trade_api
from _pending import (
    append_notional_log,
    list_strategies,
    update_strategy,
)


# ── Position accounting ───────────────────────────────────────────────────


def _position_base(history: list[dict]) -> float:
    """Net base-currency accumulated by this grid's trades. Floors at 0."""
    pos = 0.0
    for h in history:
        if h.get("event") is not None:
            continue
        try:
            sz = float(h.get("fillSz") or 0)
        except ValueError:
            continue
        side = h.get("side")
        if side == "buy":
            pos += sz
        elif side == "sell":
            pos -= sz
    return max(pos, 0.0)


def _avg_buy_px(history: list[dict]) -> float:
    """Average entry price for the currently-held position, computed from this
    grid's own fill history (FIFO-ish). Returns 0 when nothing is held."""
    base = 0.0
    quote = 0.0
    for h in history:
        if h.get("event") is not None:
            continue
        try:
            sz = float(h.get("fillSz") or 0)
            px = float(h.get("fillPx") or 0)
        except ValueError:
            continue
        side = h.get("side")
        if side == "buy":
            base += sz
            quote += sz * px
        elif side == "sell" and base > 1e-12:
            avg = quote / base
            consumed = min(sz, base)
            base -= consumed
            quote -= consumed * avg
    if base <= 1e-12:
        return 0.0
    return quote / base


# ── Grid maintenance helpers ──────────────────────────────────────────────


def _next_level_idx(level_count: int, current_idx: int, direction: str) -> int | None:
    """Return the level index where the opposite-side restock should go."""
    if direction == "buy_filled" and current_idx + 1 < level_count:
        return current_idx + 1
    if direction == "sell_filled" and current_idx - 1 >= 0:
        return current_idx - 1
    return None


def _format_sz(value: float) -> str:
    return f"{value:.8f}".rstrip("0").rstrip(".")


def _place_buy(api, inst_id: str, level_idx: int, level_px: float, quote_sz: float) -> dict | None:
    base_sz = quote_sz / level_px
    resp = api.place_order(
        instId=inst_id,
        tdMode="cash",
        side="buy",
        ordType="limit",
        sz=_format_sz(base_sz),
        px=_format_sz(level_px),
    )
    data = (resp.get("data") or [{}])[0]
    if resp.get("code") == "0" and data.get("sCode") == "0":
        return {
            "level_idx": level_idx,
            "side": "buy",
            "px": level_px,
            "sz_base": base_sz,
            "ordId": data.get("ordId", ""),
            "placed_at_epoch": int(time.time()),
        }
    return None


# ── Per-strategy iteration ────────────────────────────────────────────────


def _process_strategy(strategy: dict) -> dict:
    if strategy.get("halted"):
        return strategy

    api = trade_api()
    inst_id = strategy["instId"]
    quote_sz = float(strategy["quote_sz_per_level"])
    level_prices: list[float] = strategy["level_prices"]
    active_orders: list[dict] = strategy.get("active_orders", [])
    history: list[dict] = strategy.get("history", [])

    # v0.2.0 autonomy controls (default to 0/off for grids created before).
    min_profit_gap = float(strategy.get("min_profit_gap") or 0.0)
    max_position_base = float(strategy.get("max_position_base") or 0.0)
    trailing_pct = float(strategy.get("trailing_pct") or 0.0)
    max_rescales = int(strategy.get("max_rescales") or 0)
    rescales_used = int(strategy.get("rescales_used") or 0)

    still_active: list[dict] = []
    new_orders: list[dict] = []

    # 1. Reconcile pending orders against OKX state, place restocks for fills.
    for order in active_orders:
        ord_id = order.get("ordId")
        if not ord_id:
            continue
        resp = api.get_order(instId=inst_id, ordId=ord_id)
        if resp.get("code") != "0" or not resp.get("data"):
            still_active.append(order)
            continue
        info = resp["data"][0]
        state = info.get("state", "")

        if state == "filled":
            fill_px = float(info.get("avgPx") or info.get("fillPx") or order["px"])
            fill_sz = float(info.get("accFillSz") or order["sz_base"])
            notional = fill_px * fill_sz
            history.append({
                "ts_epoch": int(time.time()),
                "ordId": ord_id,
                "side": order["side"],
                "level_idx": order["level_idx"],
                "fillPx": fill_px,
                "fillSz": fill_sz,
                "notional_usdt": notional,
            })
            audit_append(
                "fill",
                strategy_id=strategy["id"],
                instId=inst_id,
                side=order["side"],
                level_idx=order["level_idx"],
                fillPx=fill_px,
                fillSz=fill_sz,
                notional_usdt=round(notional, 4),
            )
            append_notional_log({
                "id": strategy["id"],
                "ordId": ord_id,
                "instId": inst_id,
                "side": order["side"],
                "notional_usdt": notional,
            })

            # Daily-cap halt — checked against the size of the *next* restock.
            try:
                check_daily_room(quote_sz)
            except GuardrailError as e:
                strategy["halted"] = True
                strategy["halt_reason"] = f"daily-cap breach after fill: {e}"
                audit_append("halted", strategy_id=strategy["id"], reason=str(e))
                continue

            direction = "buy_filled" if order["side"] == "buy" else "sell_filled"
            target_idx = _next_level_idx(len(level_prices), order["level_idx"], direction)
            if target_idx is None:
                continue
            target_px = level_prices[target_idx]
            target_side = "sell" if order["side"] == "buy" else "buy"

            # Cost-basis floor (sells).
            if target_side == "sell" and min_profit_gap > 0:
                avg_px = _avg_buy_px(history)
                if avg_px > 0 and target_px < avg_px * (1 + min_profit_gap):
                    audit_append(
                        "cost_basis_protected",
                        strategy_id=strategy["id"],
                        level_idx=target_idx,
                        target_px=target_px,
                        avg_px=round(avg_px, 6),
                        min_profit_gap=min_profit_gap,
                    )
                    continue

            # Position cap (buys).
            if target_side == "buy" and max_position_base > 0:
                pos = _position_base(history)
                if pos >= max_position_base:
                    audit_append(
                        "position_capped",
                        strategy_id=strategy["id"],
                        level_idx=target_idx,
                        position=round(pos, 8),
                        cap=max_position_base,
                    )
                    continue

            # Place restock.
            base_sz = quote_sz / target_px
            place = api.place_order(
                instId=inst_id,
                tdMode="cash",
                side=target_side,
                ordType="limit",
                sz=_format_sz(base_sz),
                px=_format_sz(target_px),
            )
            place_data = (place.get("data") or [{}])[0]
            if place.get("code") == "0" and place_data.get("sCode") == "0":
                new_orders.append({
                    "level_idx": target_idx,
                    "side": target_side,
                    "px": target_px,
                    "sz_base": base_sz,
                    "ordId": place_data.get("ordId", ""),
                    "placed_at_epoch": int(time.time()),
                })
                audit_append(
                    "restock",
                    strategy_id=strategy["id"],
                    side=target_side,
                    px=target_px,
                    sz=base_sz,
                    level_idx=target_idx,
                )
            else:
                history.append({
                    "ts_epoch": int(time.time()),
                    "event": "restock_failed",
                    "level_idx": target_idx,
                    "msg": place_data.get("sMsg") or place.get("msg"),
                })
        elif state in ("canceled", "mmp_canceled"):
            history.append({
                "ts_epoch": int(time.time()),
                "ordId": ord_id,
                "event": "cancelled_externally",
                "level_idx": order["level_idx"],
            })
        else:
            still_active.append(order)

    # 2. Trailing / auto-rescale. Runs only when configured at setup.
    rescaled = False
    if (
        not strategy.get("halted")
        and trailing_pct > 0
        and rescales_used < max_rescales
    ):
        try:
            tick = market_api().get_ticker(instId=inst_id)
        except Exception:
            tick = {"code": "-1"}
        if tick.get("code") == "0" and tick.get("data"):
            cur_px = float(tick["data"][0]["last"])
            band = float(strategy["high"]) - float(strategy["low"])
            threshold = band * trailing_pct
            near_top = cur_px > float(strategy["high"]) - threshold
            near_bottom = cur_px < float(strategy["low"]) + threshold
            if near_top or near_bottom:
                audit_append(
                    "rescale_started",
                    strategy_id=strategy["id"],
                    cur_px=cur_px,
                    old_low=strategy["low"],
                    old_high=strategy["high"],
                    near="top" if near_top else "bottom",
                )

                # Cancel everything still on the book.
                to_cancel = still_active + new_orders
                cancel_failures = 0
                for o in to_cancel:
                    if not o.get("ordId"):
                        continue
                    cresp = api.cancel_order(instId=inst_id, ordId=o["ordId"])
                    cdata = (cresp.get("data") or [{}])[0]
                    if cresp.get("code") != "0" or cdata.get("sCode") != "0":
                        cancel_failures += 1

                # New band centered on current price, preserving span.
                new_low = round(cur_px - band / 2, 8)
                new_high = round(cur_px + band / 2, 8)
                lvls = int(strategy["levels"])
                step = (new_high - new_low) / (lvls - 1)
                new_level_prices = [round(new_low + i * step, 8) for i in range(lvls)]

                # Re-seed initial buys below cur_px (subject to position cap).
                replacements: list[dict] = []
                cur_pos = _position_base(history)
                for idx, lvl_px in enumerate(new_level_prices):
                    if lvl_px >= cur_px:
                        continue
                    if max_position_base > 0 and cur_pos >= max_position_base:
                        audit_append(
                            "position_capped",
                            strategy_id=strategy["id"],
                            level_idx=idx,
                            position=round(cur_pos, 8),
                            cap=max_position_base,
                            context="rescale",
                        )
                        continue
                    placed = _place_buy(api, inst_id, idx, lvl_px, quote_sz)
                    if placed:
                        replacements.append(placed)

                strategy["low"] = new_low
                strategy["high"] = new_high
                strategy["level_prices"] = new_level_prices
                strategy["rescales_used"] = rescales_used + 1
                still_active = []
                new_orders = replacements
                rescaled = True
                audit_append(
                    "rescaled",
                    strategy_id=strategy["id"],
                    new_low=new_low,
                    new_high=new_high,
                    placed=len(replacements),
                    cancel_failures=cancel_failures,
                    rescales_used=strategy["rescales_used"],
                )

    strategy["active_orders"] = still_active + new_orders
    strategy["history"] = history
    strategy["last_step_epoch"] = int(time.time())
    strategy["_last_rescaled"] = rescaled  # transient hint for the summary line
    return strategy


def main() -> int:
    strategies = list_strategies()
    if not strategies:
        print("No active grid strategies.")
        return 0

    summary: list[str] = []
    for strategy in strategies:
        if strategy.get("kind") != "grid":
            continue
        before_active = len(strategy.get("active_orders", []))
        before_history = len(strategy.get("history", []))
        updated = _process_strategy(strategy)
        rescaled = updated.pop("_last_rescaled", False)
        update_strategy(updated["id"], updated)
        new_events = len(updated.get("history", [])) - before_history
        active_now = len(updated.get("active_orders", []))
        flags = []
        if rescaled:
            flags.append(f"RESCALED→[{updated['low']}–{updated['high']}]")
        if updated.get("halted"):
            flags.append(f"HALTED: {updated.get('halt_reason')!r}")
        summary.append(
            f"  {updated['id']:<22} {updated['instId']:<12} "
            f"active {before_active}→{active_now}, +{new_events} event(s) {' '.join(flags)}"
        )

    print(f"Grid step ({len(summary)} strategy/strategies):")
    for line in summary:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
