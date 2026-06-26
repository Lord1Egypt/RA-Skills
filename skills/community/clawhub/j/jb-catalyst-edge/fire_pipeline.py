#!/usr/bin/env python3
"""
fire_pipeline.py — Catalyst Edge RSI Alert Pipeline
====================================================
Runs the stock scanner (or reuses fresh results) and posts RSI threshold
alerts to Discord #retirement-edge when tickers cross into buy/sell territory.

RSI thresholds (standard):
  - BUY:  RSI < 30  (oversold — bull reversal zone)
  - SELL: RSI > 70  (overbought)
  - WATCH: RSI recovering above 60 after prior BUY signal (confirms recovery)

Idempotency: last_signaled_state stored in watchlist.json prevents re-posting
the same signal. Only NEW crossings trigger Discord posts.

FIRE modeling: for BUY signals, rough annual income estimate on $10k position
using known dividend yields from the yield_map.

Called by cron (fire-pipeline-sunday) or directly:
  python3 fire_pipeline.py
"""

import json, os, sys, subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
SKILL_DIR    = Path("/workspace/skills/catalyst-edge")
SCAN_DIR     = SKILL_DIR / "stock_scanner"
WATCHLIST_F  = SCAN_DIR / "watchlist.json"
LAST_SCAN_F  = SCAN_DIR / "last_scan.json"
SCAN_LOG_F   = SCAN_DIR / "scan_log.md"
STATE_FILE   = SCAN_DIR / "signaled_state.json"   # tracks last signaled RSI state

# ── Freshness threshold (minutes) ────────────────────────────────────────────
FRESH_MINUTES = 15

# ── Known dividend yields (annual, as decimal e.g. 0.035 = 3.5%) ─────────────
# Used for FIRE income estimate on BUY signals. Update as watchlist changes.
YIELD_MAP = {
    "VT":    0.0180,   # Vanguard Total World Stock ETF
    "VTI":   0.0134,   # Vanguard Total Stock Market
    "QYLD":  0.1100,   # Global X NASDAQ Covered Call  (~11% forward yield)
    "JEPI":  0.0850,   # J.P. Morgan Equity Premium Income (~8.5%)
    "SCHD":  0.0351,   # Schwab U.S. Dividend Equity (~3.5%)
    "VYM":   0.0310,   # Vanguard High Dividend Yield (~3.1%)
    "AMD":   0.0000,   # No dividend — growth play
}

# ── Discord channel config ────────────────────────────────────────────────────
DISCORD_CHANNEL_ID = "1484979090892259449"   # #retirement-edge
SERVER_ID          = "1480275532531761192"

# ── RSI thresholds ─────────────────────────────────────────────────────────────
RSI_BUY   = 30.0   # Oversold — consider buying
RSI_SELL  = 70.0   # Overbought — consider selling
RSI_RECOVER = 60.0 # Cross above this after prior BUY = confirming recovery / SELL

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_state():
    """Load last signaled RSI state per ticker. Returns {ticker: {'rsi': float, 'signal': str}}"""
    if STATE_FILE.exists():
        return load_json(STATE_FILE)
    return {}

def save_state(state):
    save_json(STATE_FILE, state)

def is_scan_fresh():
    """Return True if last_scan.json exists and is < FRESH_MINUTES old."""
    if not LAST_SCAN_F.exists():
        return False
    data = load_json(LAST_SCAN_F)
    scanned_at = data.get("scanned_at", "")
    # Format: "2026-03-22 13:25 CDT" or "2026-03-22 23:01 CST"
    try:
        # Handle both CDT/CST timezone labels
        ts_str = scanned_at.replace(" CDT ", " ").replace(" CST ", " ")
        scanned_dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M")
        age = datetime.now() - scanned_dt
        return age.total_seconds() < FRESH_MINUTES * 60
    except ValueError:
        return False

def run_or_load_scan():
    """
    Return scan results — use last_scan.json if fresh (<15 min),
    otherwise shell out to scan_once.py.
    """
    if is_scan_fresh():
        print(f"[Pipeline] last_scan.json is fresh (<{FRESH_MINUTES} min old) — using cached results.")
        return load_json(LAST_SCAN_F)
    else:
        print("[Pipeline] last_scan.json is stale — running scan_once.py ...")
        result = subprocess.run(
            [sys.executable, str(SCAN_DIR / "scan_once.py")],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[Pipeline] FATAL: scan_once.py failed:\n{result.stderr}")
            sys.exit(1)
        print(f"[Pipeline] scan_once.py completed.")
        return load_json(LAST_SCAN_F)

def compute_pct_from_sma200(price, rsi, change_pct):
    """
    We don't have explicit SMA200 from Alpha Vantage free tier without extra calls.
    Heuristic: use change_pct as a short-term momentum proxy.
    For display purposes, flag as N/A with a note.
    """
    # Real SMA200 requires TIME_SERIES_DAILY + 200+ days of data.
    # We note N/A here; scan_once.py could be extended to compute it.
    return None

def signal_strength(score):
    if score is None: return "UNKNOWN"
    if score >= 85: return "⭐⭐⭐ STRONG"
    if score >= 75: return "⭐⭐ CONVICTION"
    if score >= 60: return "⭐ MODERATE"
    return "WEAK"

def fire_yield_estimate(ticker, position=10_000):
    """Return (ticker, annual_income_str, is_growth_play) for a $10k position."""
    yield_rate = YIELD_MAP.get(ticker, 0.0)
    if yield_rate == 0.0:
        return None, "no dividend — growth play only", True
    annual = position * yield_rate
    return (
        f"${annual:,.2f}/yr",
        f"${annual/12:,.2f}/mo",
        False
    )

def append_to_log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M CDT")
    with open(SCAN_LOG_F, "a") as f:
        f.write(f"\n## FIRE Pipeline | {ts}\n{msg}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# ALERT LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_tickers(scan_data, prev_state):
    """
    Compare current RSI to previous signaled state and determine new alerts.
    Returns list of alert dicts.
    """
    alerts = []
    results = scan_data.get("results", [])
    errors  = scan_data.get("errors", [])

    for r in results:
        ticker = r["ticker"]
        rsi    = r.get("rsi")
        price  = r.get("price")
        chg    = r.get("change_pct", 0.0)
        score  = r.get("score")
        signal = r.get("signal", "UNKNOWN")

        if rsi is None or score is None:
            continue  # data error, skip

        prev = prev_state.get(ticker, {})
        prev_rsi    = prev.get("rsi")
        prev_signal = prev.get("signal")  # 'BUY_SIGNALED' or 'SELL_SIGNALED'

        # ── BUY signal: RSI crosses below 30 AND not previously signaled BUY ──
        if rsi < RSI_BUY and prev_signal != "BUY_SIGNALED":
            alerts.append({
                "action":       "BUY",
                "ticker":       ticker,
                "rsi":          rsi,
                "price":        price,
                "change_pct":   chg,
                "score":        score,
                "signal":       signal,
                "pct_sma200":   None,   # N/A without SMA200
                "reasoning":    _buy_reasoning(ticker, rsi, chg, score),
            })

        # ── SELL signal: RSI crosses above 70 AND not previously signaled SELL ─
        elif rsi > RSI_SELL and prev_signal != "SELL_SIGNALED":
            alerts.append({
                "action":       "SELL",
                "ticker":       ticker,
                "rsi":          rsi,
                "price":        price,
                "change_pct":   chg,
                "score":        score,
                "signal":       signal,
                "pct_sma200":   None,
                "reasoning":    _sell_reasoning(ticker, rsi, chg, score),
            })

        # ── RECOVERY SELL: RSI recovered above 60 after prior BUY signal ──────
        #    This means a prior BUY has now cleared — time to take profit / stop watching
        elif (prev_signal == "BUY_SIGNALED"
              and prev_rsi is not None
              and prev_rsi < RSI_BUY
              and rsi > RSI_RECOVER):
            alerts.append({
                "action":       "RECOVERY_SELL",
                "ticker":       ticker,
                "rsi":          rsi,
                "price":        price,
                "change_pct":   chg,
                "score":        score,
                "signal":       signal,
                "pct_sma200":   None,
                "reasoning":    f"RSI recovered {prev_rsi:.0f}→{rsi:.0f} — prior BUY cleared. Confirming bull reversal.",
            })

    return alerts

def _buy_reasoning(ticker, rsi, chg, score):
    if score and score >= 80:
        strength = "extreme oversold + strong momentum"
    elif rsi < 25:
        strength = "deep oversold — elevated bull reversal risk"
    else:
        strength = "oversold — RSI catching bid"
    return f"{ticker}: RSI={rsi:.1f} ({strength}). Score={score}.{_momentum_note(chg)}"

def _sell_reasoning(ticker, rsi, chg, score):
    if rsi > 80:
        zone = "extreme overbought — elevated pullback risk"
    else:
        zone = "overbought — momentum fading"
    return f"{ticker}: RSI={rsi:.1f} ({zone}). Score={score}.{_momentum_note(chg)}"

def _momentum_note(chg):
    if chg > 3:  return " Strong daily momentum."
    if chg > 0:  return " Positive intraday momentum."
    if chg > -2: return " Mild weakness."
    return " Heavy selling pressure."

# ═══════════════════════════════════════════════════════════════════════════════
# DISCORD EMBED BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

DISCORD_COLORS = {
    "BUY":            0x00C853,   # bright green
    "SELL":           0xD50000,   # red
    "RECOVERY_SELL":  0xF57C00,   # orange (not as severe as SELL)
}

def build_embed(alert, today_str):
    action  = alert["action"]
    ticker  = alert["ticker"]
    rsi     = alert["rsi"]
    price   = alert["price"]
    chg     = alert["change_pct"]
    score   = alert["score"]
    reasoning = alert["reasoning"]

    color = DISCORD_COLORS.get(action, 0xFFC107)  # yellow default

    # Action label
    if action == "BUY":
        label = "🟢 RSI BUY SIGNAL"
        fire_line = _build_fire_line(ticker)
    elif action == "RECOVERY_SELL":
        label = "🟡 RSI RECOVERY — PRIOR BUY CLEARED"
        fire_line = ""
    else:
        label = "🔴 RSI SELL SIGNAL"
        fire_line = ""

    # Score badge
    strength = signal_strength(score)

    embed = {
        "title": f"{label} | {ticker}",
        "color": color,
        "description": reasoning,
        "fields": [
            {
                "name":   "RSI (14)",
                "value":  f"**{rsi:.1f}** {'🔴' if rsi > 60 else '🟡' if rsi > 30 else '🟢'}",
                "inline": True,
            },
            {
                "name":   "Price",
                "value":  f"**${price:.2f}**",
                "inline": True,
            },
            {
                "name":   "Day Chg",
                "value":  f"**{chg:+.2f}%**",
                "inline": True,
            },
            {
                "name":   "Conviction Score",
                "value":  f"**{score}/100** — {strength}",
                "inline": True,
            },
            {
                "name":   "200-Day SMA",
                "value":  "N/A (SMA200 not in free-tier feed)",
                "inline": True,
            },
        ],
        "footer": {
            "text": f"Catalyst Edge | {today_str} | Idempotent — re-posts only on new crossings"
        },
    }

    if fire_line:
        embed["fields"].append({
            "name":   "FIRE Yield Estimate ($10K pos)",
            "value":  fire_line,
            "inline": False,
        })

    return embed

def _build_fire_line(ticker):
    annual, monthly, is_growth = fire_yield_estimate(ticker)
    if is_growth:
        return f"No dividend — growth play only"
    return f"~{annual} / yr  (~{monthly} / mo)"

# ═══════════════════════════════════════════════════════════════════════════════
# DISCORD POST (via message tool)
# ═══════════════════════════════════════════════════════════════════════════════

def post_to_discord(embed_blocks):
    """
    Send an embed to Discord #retirement-edge using the message tool.
    embed_blocks is a list of alert dicts; we send one rich embed per alert.
    """
    import os, subprocess, json as _json

    # Use the message tool via exec — just write the embed to a temp JSON
    # and let the claw's own tooling handle delivery.
    # We invoke via openclaw's CLI directly.
    payload = _json.dumps(embed_blocks, indent=2)
    tmp = "/tmp/fire_pipeline_discord_payload.json"
    with open(tmp, "w") as f:
        f.write(payload)

    # Invoke via openclaw message send
    cmd = [
        "openclaw", "message", "send",
        "--channel", "discord",
        "--target", DISCORD_CHANNEL_ID,
        "--file", tmp,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_pipeline():
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M CDT")
    print(f"\n{'='*60}")
    print(f"FIRE Pipeline | {today_str}")
    print(f"{'='*60}")

    # ── Step 1: Load scan results (cached or fresh) ──────────────────────────
    scan_data = run_or_load_scan()
    scanned_at = scan_data.get("scanned_at", "unknown")
    print(f"[1/5] Scan data loaded — scanned at: {scanned_at}")

    # ── Step 2: Load previous signaled state (idempotency) ─────────────────
    prev_state = load_state()
    print(f"[2/5] Loaded signaled state for {len(prev_state)} tickers")

    # ── Step 3: Evaluate RSI thresholds, find new crossings ────────────────
    alerts = evaluate_tickers(scan_data, prev_state)
    print(f"[3/5] Found {len(alerts)} new crossing(s)")
    for a in alerts:
        print(f"       → {a['action']}: {a['ticker']}  RSI={a['rsi']:.1f}  Score={a['score']}")

    if not alerts:
        msg = "No new RSI threshold crossings detected. No Discord alert posted."
        print(f"[4/5] {msg}")
        append_to_log(msg + f"\n  Scanned at: {scanned_at}")
        print("[5/5] Exiting — idempotent, no action taken.")
        return

    # ── Step 4: Post to Discord ──────────────────────────────────────────────
    print(f"[4/5] Posting {len(alerts)} alert(s) to #retirement-edge ...")
    for alert in alerts:
        embed = build_embed(alert, today_str)
        result = post_to_discord([embed])
        if result.returncode != 0:
            print(f"       ⚠ Failed to post {alert['ticker']}: {result.stderr[:120]}")
        else:
            print(f"       ✅ Posted: {alert['action']} | {alert['ticker']}")

    # ── Step 5: Update state + log ──────────────────────────────────────────
    new_state = dict(prev_state)
    for alert in alerts:
        t = alert["ticker"]
        sig_key = "BUY_SIGNALED" if alert["action"] == "BUY" else "SELL_SIGNALED"
        new_state[t] = {"rsi": alert["rsi"], "signal": sig_key}

    save_state(new_state)
    print(f"[5/5] Updated signaled state — {len(new_state)} ticker(s) tracked.")

    # Log to scan_log.md
    log_lines = []
    for a in alerts:
        fire_info = ""
        if a["action"] == "BUY":
            annual, monthly, _ = fire_yield_estimate(a["ticker"])
            fire_info = f" | FIRE est: {annual}/yr" if annual else " | FIRE: growth play"
        log_lines.append(
            f"- **{a['action']}** | {a['ticker']} | RSI={a['rsi']:.1f} | "
            f"Price=${a['price']:.2f} ({a['change_pct']:+.2f}%) | "
            f"Score={a['score']} | {a['reasoning']}{fire_info}"
        )

    append_to_log(
        "New RSI threshold crossings detected:\n" + "\n".join(log_lines)
    )

    print(f"\n✅ Pipeline complete. {len(alerts)} alert(s) posted. 🦅")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_pipeline()
