#!/usr/bin/env python3
"""
polymarket-fee-aware-divergence

Trades AI-vs-market divergence on Polymarket-imported markets, but only when
the gap exceeds fees + spread + a configurable safety margin. Skips every
trade where the post-cost edge isn't real.

Run via clawhub cron (default */30 * * * *) or manually:
    python3 fee_aware_divergence.py
"""
import os
import sys
import time
from datetime import datetime, timezone

try:
    from simmer_sdk import SimmerClient
except ImportError:
    sys.exit("error: simmer-sdk not installed. Run: pip install simmer-sdk")


def env_float(name, default):
    try:
        return float(os.environ[name])
    except (KeyError, ValueError):
        return default


def env_int(name, default):
    try:
        return int(os.environ[name])
    except (KeyError, ValueError):
        return default


SKILL_SLUG = "polymarket-fee-aware-divergence"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

VENUE = os.environ.get("TRADING_VENUE", "sim")
TRADE_USD = env_float("FAD_TRADE_USD", 5.0)
MIN_NET_EDGE = env_float("FAD_MIN_NET_EDGE", 0.03)
SAFETY_MARGIN = env_float("FAD_SAFETY_MARGIN", 0.02)
MAX_SPREAD = env_float("FAD_MAX_SPREAD_PCT", 0.05)
MIN_TTR_MIN = env_float("FAD_MIN_TTR_MIN", 30)
MAX_TTR_HOURS = env_float("FAD_MAX_TTR_HOURS", 12)
MAX_TRADES = env_int("FAD_MAX_TRADES_PER_RUN", 3)
VERBOSE = bool(env_int("FAD_VERBOSE", 0))


def parse_ttr_hours(ctx):
    resolves_at = ctx["market"].get("resolves_at")
    if not resolves_at:
        return None
    try:
        dt = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt - datetime.now(timezone.utc)).total_seconds() / 3600.0


def evaluate(ctx):
    """Return (decision: 'yes'|'no'|None, reason, math_dict)."""
    m = ctx["market"]
    pos = ctx.get("position", {})
    discipline = ctx.get("discipline", {})
    slippage = ctx.get("slippage", {}) or {}

    if pos.get("has_position"):
        return None, "already-have-position", {}
    if discipline.get("flip_flop_warning"):
        return None, f"flip-flop:{discipline['flip_flop_warning']}", {}
    if m.get("status") != "active":
        return None, f"status:{m.get('status')}", {}

    ttr_h = parse_ttr_hours(ctx)
    if ttr_h is None:
        return None, "no-resolves-at", {}
    if ttr_h * 60 < MIN_TTR_MIN:
        return None, f"ttr-too-short:{ttr_h*60:.0f}m", {}
    if ttr_h > MAX_TTR_HOURS:
        return None, f"ttr-too-long:{ttr_h:.1f}h", {}

    ai = m.get("ai_consensus")
    price = m.get("current_price")
    if ai is None or price is None:
        return None, "no-ai-consensus", {}

    fee_bps = m.get("fee_rate_bps") or 0
    fee = fee_bps / 10_000.0
    spread = slippage.get("spread_pct") or 0.0
    if spread > MAX_SPREAD:
        return None, f"spread-too-wide:{spread:.3f}", {}

    raw_div = ai - price
    cost = fee + spread + SAFETY_MARGIN
    net_edge = abs(raw_div) - cost

    math = {
        "ai": ai,
        "mkt": price,
        "div": raw_div,
        "fee": fee,
        "spread": spread,
        "safety": SAFETY_MARGIN,
        "net": net_edge,
        "ttr_h": ttr_h,
    }

    if net_edge < MIN_NET_EDGE:
        return None, f"insufficient-net-edge:{net_edge:.3f}<{MIN_NET_EDGE:.3f}", math

    side = "yes" if raw_div > 0 else "no"
    return side, "ok", math


def format_reason(side, math):
    h = int(math["ttr_h"])
    mins = int((math["ttr_h"] - h) * 60)
    return (
        f"ai={math['ai']:.2f} mkt={math['mkt']:.2f} "
        f"div={math['div']:+.3f} fee={math['fee']:.3f} "
        f"spread={math['spread']:.3f} net={math['net']:+.3f} "
        f"ttr={h}h{mins:02d}m → {side}"
    )


def main():
    if "SIMMER_API_KEY" not in os.environ:
        sys.exit("error: SIMMER_API_KEY not set")

    client = SimmerClient(api_key=os.environ["SIMMER_API_KEY"], venue=VENUE)
    print(f"[{SKILL_SLUG}] venue={VENUE} trade_usd={TRADE_USD} "
          f"min_net_edge={MIN_NET_EDGE} max_per_run={MAX_TRADES}")

    markets = client.get_markets(status="active", limit=200)
    candidates = [m for m in markets if getattr(m, "import_source", None) == "polymarket"]
    print(f"[{SKILL_SLUG}] {len(candidates)} polymarket-tagged candidates")

    placed = 0
    skipped = 0
    skip_reasons = {}
    for m in candidates:
        if placed >= MAX_TRADES:
            print(f"[{SKILL_SLUG}] hit MAX_TRADES_PER_RUN={MAX_TRADES}")
            break
        try:
            ctx = client.get_market_context(m.id)
        except Exception as e:
            print(f"[{SKILL_SLUG}] context-error {m.id}: {e}")
            continue

        side, reason, math = evaluate(ctx)
        if side is None:
            skipped += 1
            skip_reasons[reason.split(":")[0]] = skip_reasons.get(reason.split(":")[0], 0) + 1
            if VERBOSE:
                print(f"[{SKILL_SLUG}] skip {m.id} — {reason}")
            continue

        msg = format_reason(side, math)
        print(f"[{SKILL_SLUG}] TRADE {m.id} {side} ${TRADE_USD} — {msg}")
        try:
            result = client.trade(
                m.id, side, TRADE_USD,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=msg,
            )
            print(f"[{SKILL_SLUG}]   shares={getattr(result, 'shares_bought', '?')}")
            placed += 1
            time.sleep(1)
        except Exception as e:
            print(f"[{SKILL_SLUG}]   trade-error: {e}")

    print(f"[{SKILL_SLUG}] done — placed={placed} skipped={skipped} "
          f"of {len(candidates)} candidates")
    if skip_reasons:
        top = sorted(skip_reasons.items(), key=lambda kv: -kv[1])
        print(f"[{SKILL_SLUG}] skip breakdown: " +
              ", ".join(f"{k}={v}" for k, v in top))


if __name__ == "__main__":
    main()
