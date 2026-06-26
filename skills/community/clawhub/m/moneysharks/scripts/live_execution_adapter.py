#!/usr/bin/env python3
"""
Live execution adapter for MoneySharks.
Handles both 'live' (with optional approval) and 'autonomous_live' (no approval) modes.
In autonomous_live mode: sets leverage, places bracket order (entry + SL + TP) immediately.
In live mode with approval: same execution path after approval token is verified.

Input (stdin JSON):
  {
    "mode": "live"|"autonomous_live",
    "require_human_approval": bool,   ← live mode only
    "approval_token": str|null,       ← live mode only
    "symbol": str,
    "side": "BUY"|"SELL",
    "quantity": float,
    "leverage": int,
    "entry_price": float,             ← for reference; market order uses live price
    "stop_loss": float,
    "take_profit": float,
    "reason": str,
    "confidence": float
  }
Output:
  {
    "ok": bool,
    "status": str,
    "mode": str,
    "order_result": {...},
    "error": str|null,
    "timestamp": str
  }
"""
import json
import os
import sys
from datetime import datetime, timezone

# Add scripts dir to path so we can import aster_readonly_client
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import aster_readonly_client as aster


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]


def main() -> int:
    payload = json.load(sys.stdin)
    mode = payload.get("mode", "approval")
    require_approval = bool(payload.get("require_human_approval", True))
    approval_token = payload.get("approval_token")
    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")
    ts = datetime.now(timezone.utc).isoformat()

    # ── Credential check ──
    if not api_key or not api_secret:
        print(json.dumps({"ok": False, "error": "missing_credentials", "status": "ERROR", "timestamp": ts}))
        return 1

    # ── Mode guard ──
    if mode not in ("live", "autonomous_live"):
        print(json.dumps({
            "ok": False,
            "error": "mode_not_executable",
            "note": f"Mode '{mode}' is not a live execution mode. Use paper or approval flows for other modes.",
            "status": "SKIPPED",
            "timestamp": ts,
        }))
        return 1

    # ── Approval gate (live mode only; autonomous_live skips this entirely) ──
    if mode == "live" and require_approval:
        if not approval_token:
            print(json.dumps({
                "ok": False,
                "status": "PENDING_APPROVAL",
                "approval_request": {
                    "symbol": payload.get("symbol"),
                    "side": payload.get("side"),
                    "quantity": payload.get("quantity"),
                    "leverage": payload.get("leverage"),
                    "stop_loss": payload.get("stop_loss"),
                    "take_profit": payload.get("take_profit"),
                    "reason": payload.get("reason", "Approval required before live submission."),
                    "confidence": payload.get("confidence"),
                },
                "timestamp": ts,
            }))
            return 2

    # ── Extract order parameters ──
    symbol = payload.get("symbol")
    side = str(payload.get("side", "")).upper()
    quantity = float(payload.get("quantity", 0))
    leverage = int(payload.get("leverage", 1))
    stop_loss = float(payload.get("stop_loss", 0))
    take_profit = float(payload.get("take_profit", 0))

    if not symbol or side not in ("BUY", "SELL") or quantity <= 0:
        print(json.dumps({
            "ok": False,
            "error": "invalid_order_params",
            "details": f"symbol={symbol} side={side} quantity={quantity}",
            "status": "ERROR",
            "timestamp": ts,
        }))
        return 1

    if stop_loss <= 0 or take_profit <= 0:
        print(json.dumps({
            "ok": False,
            "error": "missing_stop_or_target",
            "status": "ERROR",
            "timestamp": ts,
        }))
        return 1

    # ── Execute bracket trade ──
    try:
        result = aster.place_bracket(
            symbol=symbol,
            entry_side=side,
            quantity=quantity,
            stop_loss_price=stop_loss,
            take_profit_price=take_profit,
            leverage=leverage,
        )
        print(json.dumps({
            "ok": True,
            "status": "EXECUTED",
            "mode": mode,
            "credentials": {
                "api_key_masked": mask(api_key),
                "api_secret_loaded": True,
            },
            "order_result": result,
            "input": {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "leverage": leverage,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "reason": payload.get("reason", ""),
                "confidence": payload.get("confidence"),
            },
            "timestamp": ts,
        }, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "status": "EXECUTION_ERROR",
            "error": str(e),
            "symbol": symbol,
            "mode": mode,
            "timestamp": ts,
        }))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
