#!/usr/bin/env python3
"""
Trailing stop manager — adjusts stop-loss on open positions as price moves in favour.
Called by autonomous_runner after the main trade loop, for each open position.

Input (stdin JSON):
  {
    "symbol": str,
    "side": "BUY"|"SELL",
    "entry_price": float,
    "current_price": float,
    "current_stop_loss": float,
    "atr": float,             ← ATR14 from latest features
    "trailing_mode": "atr"|"breakeven"|"percentage",  ← default "atr"
    "trailing_atr_multiplier": float,  ← default 1.5
    "breakeven_trigger_pct": float,    ← move SL to breakeven when price moves this % in favour (default 0.5%)
  }
Output:
  {
    "new_stop_loss": float|null,   ← null = no change
    "reason": str,
    "moved": bool
  }
"""
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    symbol = payload["symbol"]
    side = payload["side"].upper()
    entry = float(payload["entry_price"])
    current = float(payload["current_price"])
    old_sl = float(payload["current_stop_loss"])
    atr = float(payload.get("atr", 0))
    mode = payload.get("trailing_mode", "atr")
    atr_mult = float(payload.get("trailing_atr_multiplier", 1.5))
    be_trigger = float(payload.get("breakeven_trigger_pct", 0.005))

    is_long = side == "BUY"
    new_sl = None
    reason = "no_change"

    if is_long:
        pnl_pct = (current - entry) / entry if entry else 0

        if mode == "breakeven" or pnl_pct >= be_trigger:
            # Move to breakeven + small buffer
            be_sl = entry * 1.001  # breakeven + 0.1% buffer
            if be_sl > old_sl:
                new_sl = be_sl
                reason = f"breakeven_trigger (pnl={pnl_pct:.4f})"

        if mode == "atr" and atr > 0:
            trail_sl = current - (atr * atr_mult)
            if trail_sl > old_sl and trail_sl > entry * 0.999:
                new_sl = trail_sl
                reason = f"atr_trail (atr={atr:.2f}, mult={atr_mult})"

    else:  # SHORT
        pnl_pct = (entry - current) / entry if entry else 0

        if mode == "breakeven" or pnl_pct >= be_trigger:
            be_sl = entry * 0.999
            if be_sl < old_sl:
                new_sl = be_sl
                reason = f"breakeven_trigger (pnl={pnl_pct:.4f})"

        if mode == "atr" and atr > 0:
            trail_sl = current + (atr * atr_mult)
            if trail_sl < old_sl and trail_sl < entry * 1.001:
                new_sl = trail_sl
                reason = f"atr_trail (atr={atr:.2f}, mult={atr_mult})"

    moved = new_sl is not None
    print(json.dumps({
        "new_stop_loss": new_sl,
        "reason": reason,
        "moved": moved,
        "old_stop_loss": old_sl,
        "current_price": current,
        "pnl_pct": round(pnl_pct, 6) if entry else 0,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
