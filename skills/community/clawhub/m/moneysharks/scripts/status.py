#!/usr/bin/env python3
"""
MoneySharks status report.
Shows: mode, halt state, circuit breaker, daily loss, open positions,
recent performance metrics, last cycle time, and active lessons.

usage: status.py <config.json> [--data-dir <dir>] [--json]
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_json(args: list, stdin_obj=None) -> dict:
    try:
        proc = subprocess.run(
            args,
            input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
        return json.loads(proc.stdout.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def fmt_usd(v) -> str:
    try:
        return f"${float(v):,.2f}"
    except Exception:
        return "n/a"


def fmt_pct(v) -> str:
    try:
        return f"{float(v) * 100:.1f}%"
    except Exception:
        return "n/a"


def time_ago(ts_str: str) -> str:
    if not ts_str:
        return "never"
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        secs = int(delta.total_seconds())
        if secs < 60:
            return f"{secs}s ago"
        elif secs < 3600:
            return f"{secs // 60}m ago"
        elif secs < 86400:
            return f"{secs // 3600}h ago"
        else:
            return f"{secs // 86400}d ago"
    except Exception:
        return ts_str


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: status.py <config.json> [--data-dir <dir>] [--json]", file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])
    json_output = "--json" in sys.argv

    data_dir = config_path.parent
    if "--data-dir" in sys.argv:
        idx = sys.argv.index("--data-dir")
        data_dir = Path(sys.argv[idx + 1])

    state_path = data_dir / "state.json"
    trades_path = data_dir / "trades.json"

    # ── Load config ──
    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except Exception:
            pass

    # ── Load state ──
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
        except Exception:
            pass

    # ── Load trades summary ──
    trades = []
    if trades_path.exists():
        try:
            trades = json.loads(trades_path.read_text())
        except Exception:
            pass

    # ── Fetch live account from Aster ──
    account_data = {}
    positions_data = []
    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")
    has_credentials = bool(api_key and api_secret)

    if has_credentials:
        bundle = run_json([sys.executable, str(base / "aster_readonly_client.py"), "account"])
        if not bundle.get("ok") is False:
            account_data = bundle.get("account", {})
            positions_data = bundle.get("positions", [])

    # ── Compute trade stats ──
    executed_trades = [t for t in trades if t.get("decision") in ("long", "short")]
    closed_trades = [t for t in executed_trades if t.get("outcome") in ("win", "loss", "breakeven")]
    wins = len([t for t in closed_trades if t.get("outcome") == "win"])
    losses = len([t for t in closed_trades if t.get("outcome") == "loss"])
    total_closed = wins + losses
    win_rate = wins / total_closed if total_closed > 0 else 0.0
    total_pnl = sum(float(t.get("realised_pnl", 0)) for t in closed_trades)

    # Today's closed trades (UTC)
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_trades = [
        t for t in closed_trades
        if (t.get("outcome_ts") or t.get("ts", ""))[:10] == today_str
    ]
    today_pnl = sum(float(t.get("realised_pnl", 0)) for t in today_trades)

    # Active open positions from Aster
    open_positions = [
        p for p in positions_data
        if abs(float(p.get("positionAmt", 0))) > 0
    ]

    # ── Metrics from state ──
    metrics = state.get("metrics", {})

    # ── Build status dict ──
    status_dict = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "mode": config.get("mode", "unknown"),
        "halt": bool(state.get("halt", False)),
        "circuit_breaker": bool(state.get("circuit_breaker", False)),
        "consecutive_errors": int(state.get("consecutive_errors", 0)),
        "daily_loss": float(state.get("daily_loss", 0)),
        "max_daily_loss": float(config.get("max_daily_loss", 0)),
        "last_cycle": state.get("last_run"),
        "credentials_loaded": has_credentials,
        "account": {
            "equity": float(account_data.get("totalWalletBalance") or account_data.get("equity") or 0),
            "available_margin": float(account_data.get("availableBalance") or account_data.get("available_margin") or 0),
            "daily_pnl": today_pnl,
        },
        "positions": [
            {
                "symbol": p.get("symbol"),
                "side": "LONG" if float(p.get("positionAmt", 0)) > 0 else "SHORT",
                "quantity": abs(float(p.get("positionAmt", 0))),
                "entry_price": float(p.get("entryPrice", 0)),
                "unrealised_pnl": float(p.get("unRealizedProfit", 0)),
                "leverage": p.get("leverage"),
            }
            for p in open_positions
        ],
        "trade_stats": {
            "total_trades": len(trades),
            "executed": len(executed_trades),
            "closed": total_closed,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 4),
            "total_pnl": round(total_pnl, 4),
            "today_closed": len(today_trades),
            "today_pnl": round(today_pnl, 4),
        },
        "metrics": {
            "win_rate": metrics.get("win_rate"),
            "avg_pnl": metrics.get("avg_pnl"),
            "effective_leverage_cap": metrics.get("effective_leverage_cap"),
            "confidence_multiplier": metrics.get("confidence_multiplier"),
            "recommended_min_confidence": metrics.get("recommended_min_confidence"),
            "leverage_reduction_active": metrics.get("leverage_reduction_active", False),
            "underperforming_symbols": metrics.get("underperforming_symbols", []),
            "lessons": metrics.get("lessons", []),
            "last_review_ts": metrics.get("last_review_ts"),
        },
        "config_summary": {
            "symbols": config.get("allowed_symbols", []),
            "base_value": config.get("base_value_per_trade"),
            "leverage_range": f"{config.get('min_leverage')}×–{config.get('max_leverage')}×",
            "max_daily_loss": config.get("max_daily_loss"),
            "max_total_exposure": config.get("max_total_exposure"),
            "cron_enabled": config.get("cron", {}).get("enabled", False),
        },
    }

    if json_output:
        print(json.dumps(status_dict, indent=2))
        return 0

    # ── Human-readable output ──
    halt_flag = " 🛑 HALTED" if status_dict["halt"] else ""
    cb_flag = " ⚡ CIRCUIT BREAKER" if status_dict["circuit_breaker"] else ""
    mode_emoji = {"autonomous_live": "🤖", "paper": "📝", "live": "📈", "approval": "✋"}.get(
        status_dict["mode"], "❓"
    )

    print(f"\n🦈  MoneySharks Status{halt_flag}{cb_flag}")
    print("─" * 50)
    print(f"  Mode:              {mode_emoji} {status_dict['mode']}")
    print(f"  Halt:              {'YES 🛑' if status_dict['halt'] else 'no'}")
    print(f"  Circuit breaker:   {'ACTIVE ⚡' if status_dict['circuit_breaker'] else 'clear'}")
    print(f"  Consecutive errors:{status_dict['consecutive_errors']}")

    if status_dict["max_daily_loss"]:
        dl_pct = (status_dict["daily_loss"] / status_dict["max_daily_loss"] * 100) if status_dict["max_daily_loss"] else 0
        print(f"  Daily loss:        {fmt_usd(status_dict['daily_loss'])} / {fmt_usd(status_dict['max_daily_loss'])} ({dl_pct:.1f}%)")
    else:
        print(f"  Daily loss:        {fmt_usd(status_dict['daily_loss'])}")

    print(f"  Last cycle:        {time_ago(status_dict['last_cycle'])}")
    print(f"  Credentials:       {'✓ loaded' if has_credentials else '✗ missing'}")

    if account_data:
        print(f"\n  Account:")
        print(f"    Equity:          {fmt_usd(status_dict['account']['equity'])}")
        print(f"    Available:       {fmt_usd(status_dict['account']['available_margin'])}")
        print(f"    Today PnL:       {fmt_usd(status_dict['account']['daily_pnl'])}")

    if status_dict["positions"]:
        print(f"\n  Open Positions ({len(status_dict['positions'])}):")
        for p in status_dict["positions"]:
            pnl_str = fmt_usd(p["unrealised_pnl"])
            print(f"    {p['symbol']:12s} {p['side']:5s}  qty={p['quantity']:.4f}  entry={p['entry_price']:.4f}  uPnL={pnl_str}")
    else:
        print(f"\n  Open Positions:    none")

    ts = status_dict["trade_stats"]
    print(f"\n  Trade History:")
    print(f"    Total trades:    {ts['total_trades']}  (executed={ts['executed']}, closed={ts['closed']})")
    if ts["closed"] > 0:
        print(f"    Win rate:        {fmt_pct(ts['win_rate'])}  ({ts['wins']}W / {ts['losses']}L)")
        print(f"    Total PnL:       {fmt_usd(ts['total_pnl'])}")
    print(f"    Today:           {ts['today_closed']} trades  {fmt_usd(ts['today_pnl'])}")

    m = status_dict["metrics"]
    if m.get("win_rate") is not None:
        print(f"\n  Adaptive Metrics:")
        print(f"    Win rate:        {fmt_pct(m['win_rate'])}")
        print(f"    Avg PnL/trade:   {fmt_usd(m.get('avg_pnl', 0))}")
        print(f"    Eff. lev cap:    {m.get('effective_leverage_cap', 'n/a')}×")
        print(f"    Confidence mult: {m.get('confidence_multiplier', 1.0):.2f}")
        if m.get("leverage_reduction_active"):
            print(f"    ⚠  Leverage reduction active (loss streak)")
        if m.get("underperforming_symbols"):
            print(f"    ⚠  Underperforming: {', '.join(m['underperforming_symbols'])}")

    if m.get("lessons"):
        print(f"\n  Active Lessons:")
        for lesson in m["lessons"]:
            print(f"    • {lesson}")

    cfg = status_dict["config_summary"]
    print(f"\n  Config:")
    print(f"    Symbols:         {', '.join(cfg['symbols'])}")
    print(f"    Base value:      {fmt_usd(cfg['base_value'])} / trade")
    print(f"    Leverage:        {cfg['leverage_range']}")
    print(f"    Max daily loss:  {fmt_usd(cfg['max_daily_loss'])}")
    print(f"    Cron:            {'enabled' if cfg['cron_enabled'] else 'disabled'}")

    if status_dict["halt"]:
        print(f"\n  ⚠  Agent is halted. Run resume.py to restart.")
    elif status_dict["circuit_breaker"]:
        print(f"\n  ⚡ Circuit breaker active ({status_dict['consecutive_errors']} consecutive errors).")
        print(f"     Run resume.py to clear and restart.")

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
