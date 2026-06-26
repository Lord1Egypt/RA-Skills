#!/usr/bin/env python3
"""
🦞 Position Monitor + Auto-Reinvest
=====================================
Checks positions every run. When anything resolves:
- Reports P&L to Telegram
- Auto-reinvests freed USDC into next best plays
- Runs weather scanner if fresh funds available

Run via cron every 30 minutes.
"""

import os, sys, json, time, subprocess
import urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timezone, date

WALLET = "0xF0D1010643A338534e2e0AEE25d372dbEA18BC2d"
STATE_FILE    = Path(__file__).parent / ".monitor_state.json"
DAILY_PNL_FILE = Path(__file__).parent / ".daily_pnl.json"
RESERVE = 15.0
MIN_DEPLOY = 40.0

# ── Circuit Breaker ────────────────────────────────────────────────────────────
CIRCUIT_BREAKER_PCT = 0.15   # Pause if daily loss > 15% of start-of-day portfolio

DATA_API  = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"

def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"known_positions": {}, "total_profit": 0.0, "total_wagered": 0.0}


# ── Daily Circuit Breaker ──────────────────────────────────────────────────────

def load_daily_pnl():
    """Load or initialize daily P&L tracker."""
    today = str(date.today())
    if DAILY_PNL_FILE.exists():
        data = json.loads(DAILY_PNL_FILE.read_text())
        if data.get("date") == today:
            return data
    # New day — reset
    return {"date": today, "start_portfolio": None, "realized_pnl": 0.0, "paused": False}


def save_daily_pnl(data):
    DAILY_PNL_FILE.write_text(json.dumps(data, indent=2))


def check_circuit_breaker(portfolio_value: float) -> tuple[bool, str]:
    """
    Check if daily circuit breaker should be triggered or is already active.

    Returns: (is_paused, reason_message)
    """
    daily = load_daily_pnl()
    today = str(date.today())

    # Auto-reset on new day
    if daily.get("date") != today:
        daily = {"date": today, "start_portfolio": None, "realized_pnl": 0.0, "paused": False}

    # Initialize start-of-day portfolio value
    if daily["start_portfolio"] is None:
        daily["start_portfolio"] = portfolio_value
        save_daily_pnl(daily)
        return False, ""

    start = daily["start_portfolio"]
    if start <= 0:
        return False, ""

    # Current daily loss = drop in portfolio value from day start
    daily_pnl = portfolio_value - start
    daily_pnl_pct = daily_pnl / start

    # Check if we've hit the circuit breaker
    if daily_pnl_pct <= -CIRCUIT_BREAKER_PCT:
        if not daily.get("paused"):
            daily["paused"] = True
            daily["paused_at"] = datetime.now(timezone.utc).isoformat()
            daily["paused_pnl_pct"] = round(daily_pnl_pct * 100, 1)
            save_daily_pnl(daily)
        return True, (
            f"⛔ CIRCUIT BREAKER ACTIVE — Daily loss {daily_pnl_pct:.1%} exceeds "
            f"{CIRCUIT_BREAKER_PCT:.0%} threshold (start: ${start:.2f}, now: ${portfolio_value:.2f}). "
            f"All new trades paused until tomorrow."
        )

    # Was paused but recovered (shouldn't normally happen intraday, but handle it)
    if daily.get("paused") and daily_pnl_pct > -CIRCUIT_BREAKER_PCT:
        daily["paused"] = False
        save_daily_pnl(daily)

    save_daily_pnl(daily)
    return False, ""

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def get_positions():
    wallet = os.environ.get("WALLET_ADDRESS", WALLET)
    req = urllib.request.Request(
        f"{DATA_API}/positions?user={wallet}&sizeThreshold=0.01&limit=100",
        headers={"User-Agent": "ClawdipusRex/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    return data if isinstance(data, list) else data.get("data", [])

def get_balance():
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
    pk = os.environ.get("PRIVATE_KEY")
    wallet = os.environ.get("WALLET_ADDRESS", WALLET)
    client = ClobClient("https://clob.polymarket.com", key=pk, chain_id=137,
                        signature_type=1, funder=wallet)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    params = BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    bal = client.get_balance_allowance(params=params)
    return int(bal.get("balance", "0")) / 1e6

def run_script(script, extra_args=None):
    cmd = ["python3", str(Path(__file__).parent / script)]
    if extra_args:
        cmd.extend(extra_args)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return (r.stdout + r.stderr).strip()

def main():
    load_env()
    state = load_state()
    known = state.get("known_positions", {})
    total_profit = state.get("total_profit", 0.0)
    total_wagered = state.get("total_wagered", 0.0)

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ── Fetch current positions ────────────────────────────────────────────────
    try:
        positions = get_positions()
    except Exception as e:
        print(f"Error fetching positions: {e}")
        sys.exit(0)

    current = {}
    for p in positions:
        key = p.get("conditionId") or p.get("market") or p.get("title","")
        curr_price = float(p.get("curPrice") or p.get("currentPrice") or p.get("price") or 0)
        size = float(p.get("size") or 0)
        avg = float(p.get("avgPrice") or p.get("averagePrice") or 0)
        title = str(p.get("title") or p.get("market") or "")
        outcome = str(p.get("outcome",""))
        current[key] = {
            "title": title,
            "outcome": outcome,
            "size": size,
            "avg": avg,
            "curr": curr_price,
            "value": curr_price * size,
        }

    # ── Detect resolved positions ──────────────────────────────────────────────
    alerts = []
    for key, prev in known.items():
        if key not in current:
            # Position gone — resolved or sold
            curr = prev.get("curr", 0)
            avg = prev.get("avg", 0)
            size = prev.get("size", 0)
            title = prev.get("title", key)
            outcome = prev.get("outcome","")

            # Determine win/loss by last known price
            if curr >= 0.95:
                pnl = (1.0 - avg) * size
                total_profit += pnl
                total_wagered += avg * size
                alerts.append(f"✅ WON +${pnl:.2f} — {outcome} | {title[:55]}")
            elif curr <= 0.05:
                pnl = -avg * size
                total_wagered += avg * size
                alerts.append(f"❌ LOST ${abs(pnl):.2f} — {outcome} | {title[:55]}")
            else:
                # Unknown resolution
                alerts.append(f"🔄 CLOSED (unknown) — {outcome} | {title[:55]}")

    # ── Check for big price moves on open positions ────────────────────────────
    for key, cur in current.items():
        prev = known.get(key, {})
        prev_price = prev.get("curr", cur["curr"])
        move = cur["curr"] - prev_price
        if abs(move) >= 0.20 and cur["size"] > 5:  # 20+ cent move, meaningful size
            direction = "📈" if move > 0 else "📉"
            alerts.append(f"{direction} MOVE {move:+.0%} — {cur['outcome']} now {cur['curr']:.0%} | {cur['title'][:50]}")

    # ── Get wallet balance ─────────────────────────────────────────────────────
    try:
        balance = get_balance()
    except Exception:
        balance = 0.0

    # ── Portfolio summary ──────────────────────────────────────────────────────
    portfolio_value = sum(p["value"] for p in current.values()) + balance
    open_count = len(current)

    # ── Run Exit Manager (stop-loss / take-profit on Kalshi) ──────────────────
    exit_output = ""
    try:
        exit_output = run_script("exit_manager.py")
        if exit_output and "exit" in exit_output.lower() and "executed" not in exit_output.lower():
            exit_output = ""   # suppress "no exits" noise
    except Exception:
        pass

    # ── Daily Circuit Breaker check ────────────────────────────────────────────
    breaker_paused, breaker_msg = check_circuit_breaker(portfolio_value)

    # ── Auto-reinvest if funds available AND circuit breaker not tripped ──────
    reinvest_output = ""
    weather_output = ""
    if balance >= MIN_DEPLOY and not breaker_paused:
        # Try sports reinvest first
        reinvest_output = run_script("auto_reinvest.py")
        time.sleep(2)
        # Then weather scanner
        weather_output = run_script("weather_scanner.py", ["--buy"])
    elif balance >= MIN_DEPLOY and breaker_paused:
        alerts.append(breaker_msg)

    # ── Build notification ─────────────────────────────────────────────────────
    if alerts or (balance >= MIN_DEPLOY and reinvest_output):
        lines = [f"🦞 *Polymarket Update* — {now_str}\n"]

        if alerts:
            lines.append("*Resolved/Moved:*")
            for a in alerts:
                lines.append(f"  {a}")
            lines.append("")

        # Portfolio status
        roi = (total_profit / total_wagered * 100) if total_wagered > 0 else 0
        lines.append(f"*Portfolio:* ${portfolio_value:.2f} | {open_count} open positions")
        lines.append(f"*Total P&L:* +${total_profit:.2f} on ${total_wagered:.2f} wagered ({roi:.1f}% ROI)")
        lines.append(f"*Cash:* ${balance:.2f}")
        lines.append(f"*Goal:* $5,000 ({total_profit/5000*100:.1f}% there) 🏁")

        # Reinvest summary
        if reinvest_output and "deployed" in reinvest_output.lower():
            deployed_line = next((l for l in reinvest_output.split("\n") if "deployed" in l.lower()), "")
            if deployed_line:
                lines.append(f"\n*Auto-reinvested:* {deployed_line.strip()}")

        if weather_output and "mispriced" in weather_output.lower():
            lines.append(f"*Weather plays:* Scanner found new edges 🌤️")

        if exit_output and ("take_profit" in exit_output.lower() or "stop_loss" in exit_output.lower()):
            exit_lines = [l.strip() for l in exit_output.split("\n") if "exit" in l.lower() or "p&l" in l.lower()]
            if exit_lines:
                lines.append(f"\n*Exit Manager:* {' | '.join(exit_lines[:2])}")

        if breaker_paused:
            lines.append(f"\n{breaker_msg}")

        print("\n".join(lines))
    else:
        # Nothing notable — silent exit
        print("HEARTBEAT_OK")

    # ── Save state ─────────────────────────────────────────────────────────────
    state["known_positions"] = current
    state["total_profit"] = total_profit
    state["total_wagered"] = total_wagered
    state["last_run"] = now_str
    save_state(state)

if __name__ == "__main__":
    main()
