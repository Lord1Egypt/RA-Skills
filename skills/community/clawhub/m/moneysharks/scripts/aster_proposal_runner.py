#!/usr/bin/env python3
"""
Proposal runner: scan Aster market data for a symbol+side and emit an approval-gated proposal.
Uses real Aster read-only data to produce a live-ready order proposal pending user confirmation.

usage: aster_proposal_runner.py <config.json> <symbol> <side>
       side: BUY (long) or SELL (short)
"""
import json
import subprocess
import sys
from pathlib import Path


def run_json(args, stdin_obj=None, check=True):
    proc = subprocess.run(
        args,
        input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    if check and proc.returncode not in (0, 1):
        raise RuntimeError(f"subprocess failed ({proc.returncode}): {proc.stderr.decode()[:400]}")
    try:
        return json.loads(proc.stdout.decode())
    except Exception:
        return {"ok": False, "error": f"bad json output: {proc.stdout.decode()[:200]}"}


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: aster_proposal_runner.py <config.json> <symbol> <side>", file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])
    symbol = sys.argv[2].upper()
    side = sys.argv[3].upper()

    if side not in ("BUY", "SELL"):
        print("ERROR: side must be BUY or SELL", file=sys.stderr)
        return 1

    config = json.loads(config_path.read_text())

    # ── Full market scan (real klines + signal + confluence + sizing) ──
    scan = run_json([sys.executable, str(base / "market_scan_from_aster.py"), str(config_path), symbol])

    if scan.get("ok") is False:
        print(json.dumps({"ok": False, "error": f"scan failed: {scan.get('error')}", "symbol": symbol}))
        return 1

    # market_scan_from_aster returns:
    #   scan["market"]["last_price"] — current price
    #   scan["order"]["leverage"] — recommended leverage
    #   scan["order"]["stop_loss"], scan["order"]["take_profit"]
    #   scan["order"]["quantity"], scan["order"]["notional"]
    #   scan["confidence"]

    order = scan.get("order") or {}
    price = float(scan.get("market", {}).get("last_price") or 0)
    leverage = int(order.get("leverage") or config.get("min_leverage", 1))
    quantity = float(order.get("quantity") or 0)
    stop_loss = float(order.get("stop_loss") or 0)
    take_profit = float(order.get("take_profit") or 0)
    confidence = float(scan.get("confidence") or 0)

    # If scan gave us a signal we can use its exact order params;
    # otherwise compute from base_value for the requested side
    if not quantity or not stop_loss or not take_profit:
        # Fallback: basic sizing from base_value
        base_val = float(config.get("base_value_per_trade", 100))
        quantity = (base_val * leverage / price) if price else 0
        if side == "BUY":
            stop_loss = price * 0.985
            take_profit = price * 1.025
        else:
            stop_loss = price * 1.015
            take_profit = price * 0.975

    proposal = {
        "symbol": symbol,
        "side": side,
        "confidence": confidence,
        "leverage": leverage,
        "entry_price": price,
        "quantity": quantity,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "signal": scan.get("signal"),
        "signal_reason": scan.get("signal_reason"),
        "confluence": scan.get("confluence"),
        "status": "PENDING_APPROVAL",
    }

    result = {
        "ok": True,
        "symbol": symbol,
        "side": side,
        "scan_signal": scan.get("signal"),
        "proposal": proposal,
        "market": scan.get("market"),
        "status": "PENDING_APPROVAL",
        "note": "Real Aster market data used. Submit proposal to live_execution_adapter.py with approval_token to execute.",
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
