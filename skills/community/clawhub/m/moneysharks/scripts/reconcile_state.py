#!/usr/bin/env python3
"""
Reconcile MoneySharks state against live Aster account data.
Fetches real positions, orders, and balances from Aster and updates state.json.

Input mode 1 (stdin JSON): reconcile against provided account/positions/orders dict
Input mode 2 (CLI): fetch from Aster API directly and update state.json

usage (as API reconciler — stdin):
  echo '{"account":{...},"positions":[...],"orders":[...]}' | reconcile_state.py

usage (live API reconcile):
  reconcile_state.py <config.json> [--data-dir <dir>] [--write]

  --write  Write reconciled state back to state.json (default: dry-run, JSON to stdout)
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_json(args: list) -> dict:
    try:
        proc = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20, check=False
        )
        return json.loads(proc.stdout.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def reconcile_from_dict(account: dict, positions: list, orders: list) -> dict:
    """Reconcile from pre-loaded data dict (stdin mode)."""
    total_exposure = sum(
        abs(float(p.get("notional", 0) or p.get("positionAmt", 0))) for p in positions
    )
    equity = float(
        account.get("totalWalletBalance")
        or account.get("equity")
        or 0
    )
    avail_margin = float(
        account.get("availableBalance")
        or account.get("available_margin")
        or equity
    )
    open_positions = [
        p for p in positions if abs(float(p.get("positionAmt", 0))) > 0
    ]
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "equity": equity,
        "available_margin": avail_margin,
        "total_exposure": total_exposure,
        "positions_count": len(open_positions),
        "orders_count": len(orders),
        "positions": [
            {
                "symbol": p.get("symbol"),
                "side": "LONG" if float(p.get("positionAmt", 0)) > 0 else "SHORT",
                "quantity": abs(float(p.get("positionAmt", 0))),
                "entry_price": float(p.get("entryPrice", 0)),
                "unrealised_pnl": float(p.get("unRealizedProfit", 0)),
                "leverage": p.get("leverage"),
                "notional": abs(float(p.get("notional", 0))),
            }
            for p in open_positions
        ],
    }


def main() -> int:
    base = Path(__file__).resolve().parent

    # ── Stdin mode (legacy / pipeline use) ──
    if len(sys.argv) == 1 or (len(sys.argv) >= 2 and sys.argv[1] == "-"):
        try:
            payload = json.load(sys.stdin)
            result = reconcile_from_dict(
                payload.get("account", {}),
                payload.get("positions", []),
                payload.get("orders", []),
            )
            print(json.dumps(result, indent=2))
            return 0
        except Exception as e:
            print(json.dumps({"ok": False, "error": str(e)}))
            return 1

    # ── CLI mode: fetch from Aster and write state.json ──
    config_path = Path(sys.argv[1])
    write_back = "--write" in sys.argv

    data_dir = config_path.parent
    if "--data-dir" in sys.argv:
        idx = sys.argv.index("--data-dir")
        data_dir = Path(sys.argv[idx + 1])

    state_path = data_dir / "state.json"
    ts = datetime.now(timezone.utc).isoformat()

    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except Exception:
            pass

    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")
    if not api_key or not api_secret:
        print(json.dumps({"ok": False, "error": "missing_credentials", "ts": ts}))
        return 1

    # ── Fetch live account bundle from Aster ──
    allowed_symbols = config.get("allowed_symbols", [])
    symbol = allowed_symbols[0] if allowed_symbols else None

    bundle = run_json(
        [sys.executable, str(base / "aster_readonly_client.py"), "account"]
        + ([symbol] if symbol else [])
    )

    if bundle.get("ok") is False:
        print(json.dumps({"ok": False, "error": f"account_fetch_failed: {bundle.get('error')}", "ts": ts}))
        return 1

    account = bundle.get("account", {})
    positions = bundle.get("positions", [])
    orders = bundle.get("orders", [])

    reconciled = reconcile_from_dict(account, positions, orders)
    reconciled["ok"] = True

    if write_back:
        # Load existing state and update account fields
        existing_state = {}
        if state_path.exists():
            try:
                existing_state = json.loads(state_path.read_text())
            except Exception:
                pass

        existing_state["account"] = {
            "equity": reconciled["equity"],
            "available_margin": reconciled["available_margin"],
            "total_exposure": reconciled["total_exposure"],
        }
        existing_state["reconciled_at"] = ts
        existing_state["positions_snapshot"] = reconciled["positions"]

        data_dir.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(existing_state, indent=2))
        reconciled["written_to"] = str(state_path)
        print(f"[{ts}] ✓ state.json updated: equity={reconciled['equity']:.2f}, "
              f"positions={reconciled['positions_count']}", file=sys.stderr)

    print(json.dumps(reconciled, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
