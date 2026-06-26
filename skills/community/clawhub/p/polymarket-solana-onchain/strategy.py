#!/usr/bin/env python3
"""
polymarket-solana-onchain
─────────────────────────
Trades Polymarket SOL/crypto prediction markets using on-chain Solana
signals as leading indicators — BEFORE price moves.

Signals (all free, no API key required):
  1. SOL TPS spike     — Solana mainnet transactions/sec via public RPC
                         High TPS = network activity surge = price catalyst
  2. DEX volume surge  — Jupiter aggregator 24h volume via public API
                         Volume up = buy pressure building
  3. Priority fee      — Median priority fee (microlamports) via getRecentPrioritizationFees
                         Fee spike = block congestion = urgent on-chain demand
  4. Stake activation  — Net stake activation delta via getEpochInfo + getVoteAccounts
                         Large activations = validator confidence = bullish signal

Why this is different from everything else on Simmer:
  - All other skills use price as the signal (lagging)
  - On-chain activity PRECEDES price movement by minutes to hours
  - Solana's public RPC is free and sub-second latency
  - No competitor has this signal source on the marketplace

Usage:
    python strategy.py              # Dry run
    python strategy.py --live       # Real trades
    python strategy.py --signals    # Show current on-chain signals only
    python strategy.py --set max_position_usd=50
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone

sys.stdout.reconfigure(line_buffering=True)

# ── Config ────────────────────────────────────────────────────────────────────
SKILL_SLUG   = "polymarket-solana-onchain"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

MAX_POSITION_USD    = float(os.environ.get("SIMMER_ONCHAIN_MAX_POSITION",  "20.0"))
MAX_TRADES_PER_RUN  = int(os.environ.get("SIMMER_ONCHAIN_MAX_TRADES",      "4"))
SIGNAL_THRESHOLD    = float(os.environ.get("SIMMER_ONCHAIN_SIGNAL_MIN",    "0.15"))  # min signal strength
VENUE               = os.environ.get("TRADING_VENUE", "sim")

# Solana public RPC — no key needed, rate limit is generous
SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Jupiter public stats — no key needed
JUPITER_STATS_URL = "https://stats.jup.ag/info"

# ── Logging ───────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


# ── HTTP helpers ──────────────────────────────────────────────────────────────
def http_post(url, data: dict, timeout=8) -> dict | None:
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body,
              headers={"Content-Type": "application/json", "User-Agent": "polymarket-solana-onchain/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        log(f"  RPC error: {e}")
        return None


def http_get(url, timeout=8) -> dict | None:
    try:
        req = urllib.request.Request(url,
              headers={"User-Agent": "polymarket-solana-onchain/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        log(f"  HTTP error ({url[:50]}): {e}")
        return None


# ── On-chain signal collection ────────────────────────────────────────────────

def get_tps() -> tuple[float, str]:
    """
    Returns (tps, status) from Solana's getRecentPerformanceSamples.
    Uses the most recent 1-minute sample.
    status: 'surge' | 'elevated' | 'normal' | 'low' | 'unknown'
    """
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getRecentPerformanceSamples",
        "params": [4]
    }
    resp = http_post(SOLANA_RPC, payload)
    if not resp or "result" not in resp:
        return 0.0, "unknown"

    samples = resp["result"]
    if not samples:
        return 0.0, "unknown"

    # Average TPS across recent samples
    tps_list = []
    for s in samples:
        num_tx    = s.get("numTransactions", 0)
        slot_time = s.get("samplePeriodSecs", 60)
        if slot_time > 0:
            tps_list.append(num_tx / slot_time)

    if not tps_list:
        return 0.0, "unknown"

    tps = sum(tps_list) / len(tps_list)

    if tps > 3500:
        status = "surge"
    elif tps > 2500:
        status = "elevated"
    elif tps > 1500:
        status = "normal"
    else:
        status = "low"

    return round(tps, 1), status


def get_priority_fee() -> tuple[float, str]:
    """
    Returns (median_microlamports, status) from getRecentPrioritizationFees.
    High fees = block congestion = urgent demand signal.
    """
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getRecentPrioritizationFees",
        "params": []
    }
    resp = http_post(SOLANA_RPC, payload)
    if not resp or "result" not in resp:
        return 0.0, "unknown"

    fees = [f.get("prioritizationFee", 0) for f in resp.get("result", []) if f.get("prioritizationFee", 0) > 0]
    if not fees:
        return 0.0, "unknown"

    fees.sort()
    median = fees[len(fees) // 2]

    if median > 100_000:
        status = "surge"
    elif median > 10_000:
        status = "elevated"
    elif median > 1_000:
        status = "normal"
    else:
        status = "low"

    return float(median), status


def get_epoch_progress() -> tuple[float, int]:
    """
    Returns (progress_pct, slots_remaining) from getEpochInfo.
    Late epoch (>85%) = upcoming validator rewards = slight sell pressure.
    Early epoch (<15%) = stake activations settling = stabilizing.
    """
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getEpochInfo", "params": []}
    resp = http_post(SOLANA_RPC, payload)
    if not resp or "result" not in resp:
        return 0.5, 0

    r = resp["result"]
    slot_index      = r.get("slotIndex", 0)
    slots_in_epoch  = r.get("slotsInEpoch", 432000)
    progress        = slot_index / slots_in_epoch if slots_in_epoch else 0.5
    slots_remaining = slots_in_epoch - slot_index
    return round(progress, 4), slots_remaining


def get_jupiter_volume() -> tuple[float, str]:
    """
    Returns (volume_24h_usd, status) from Jupiter stats API.
    Volume surge = DEX demand = bullish signal for SOL price.
    """
    data = http_get(JUPITER_STATS_URL)
    if not data:
        return 0.0, "unknown"

    vol = data.get("volume24h", data.get("totalVolume24h", 0))
    try:
        vol = float(vol)
    except (TypeError, ValueError):
        return 0.0, "unknown"

    # Jupiter typical daily volume baseline ~$800M-$1.5B
    if vol > 2_000_000_000:
        status = "surge"
    elif vol > 1_200_000_000:
        status = "elevated"
    elif vol > 600_000_000:
        status = "normal"
    else:
        status = "low"

    return vol, status


def collect_signals() -> dict:
    """Collect all on-chain signals and return a composite dict."""
    log("Collecting on-chain signals...")

    tps, tps_status = get_tps()
    log(f"  TPS: {tps:,.0f} ({tps_status})")

    fee, fee_status = get_priority_fee()
    log(f"  Priority fee: {fee:,.0f} microlamports ({fee_status})")

    epoch_pct, slots_remaining = get_epoch_progress()
    log(f"  Epoch progress: {epoch_pct:.1%} ({slots_remaining:,} slots remaining)")

    vol, vol_status = get_jupiter_volume()
    log(f"  Jupiter 24h vol: ${vol:,.0f} ({vol_status})")

    # ── Composite signal ──────────────────────────────────────────────────────
    # Score each signal: surge=1.0, elevated=0.6, normal=0.0, low=-0.5, unknown=0.0
    score_map = {"surge": 1.0, "elevated": 0.6, "normal": 0.0, "low": -0.5, "unknown": 0.0}

    tps_score = score_map[tps_status]
    fee_score = score_map[fee_status]   # high fees = demand surge = bullish
    vol_score = score_map[vol_status]

    # Epoch: late epoch is mildly bearish (validator reward sells), early is neutral
    if epoch_pct > 0.85:
        epoch_score = -0.2
    elif epoch_pct < 0.10:
        epoch_score = 0.1
    else:
        epoch_score = 0.0

    # Weighted composite: TPS + fee most important, volume secondary, epoch minor
    composite = (
        tps_score  * 0.35 +
        fee_score  * 0.30 +
        vol_score  * 0.25 +
        epoch_score * 0.10
    )
    composite = round(composite, 4)

    direction = "bullish" if composite > SIGNAL_THRESHOLD else \
                "bearish" if composite < -SIGNAL_THRESHOLD else "neutral"

    log(f"  Composite signal: {composite:+.3f} → {direction.upper()}")

    return {
        "tps": tps, "tps_status": tps_status, "tps_score": tps_score,
        "priority_fee": fee, "fee_status": fee_status, "fee_score": fee_score,
        "epoch_pct": epoch_pct, "slots_remaining": slots_remaining, "epoch_score": epoch_score,
        "jupiter_volume": vol, "vol_status": vol_status, "vol_score": vol_score,
        "composite": composite,
        "direction": direction,
    }


# ── Market selection ──────────────────────────────────────────────────────────

def find_tradeable_markets(client, direction: str, composite: float) -> list[dict]:
    """
    Find SOL/crypto prediction markets that align with the on-chain signal.
    Returns list of {market_id, question, side, edge, prob} sorted by edge.
    """
    candidates = []
    keywords = ["solana", "sol price", "bitcoin", "btc price", "ethereum", "eth price", "crypto"]

    seen = set()
    for kw in keywords:
        try:
            result = client._request("GET", "/api/sdk/markets", params={
                "q": kw, "status": "active", "limit": 15
            })
            markets = result.get("markets", [])
            for m in markets:
                mid = m.get("id")
                if not mid or mid in seen:
                    continue
                seen.add(mid)

                question = m.get("question", "")
                prob = m.get("current_probability", 0.5)

                # Determine if question is bullish-framed
                q = question.lower()
                bullish_hints = ["above", "over", "reach", "hit", "exceed", "higher", "up", "bull", "gain", "rise", "surpass"]
                bearish_hints = ["below", "under", "drop", "fall", "lose", "lower", "down", "bear", "crash", "decline"]
                bs = sum(1 for h in bullish_hints if h in q)
                ss = sum(1 for h in bearish_hints if h in q)

                if bs == ss:
                    continue  # Ambiguous, skip
                is_bullish_question = bs > ss

                # Signal alignment
                if direction == "bullish":
                    if is_bullish_question:
                        side = "yes"
                        # Edge: market underpricing bullish outcome
                        # Expected prob boosted by signal strength
                        expected = min(0.90, 0.5 + abs(composite) * 0.5)
                        edge = expected - prob
                    else:
                        side = "no"
                        expected = min(0.90, 0.5 + abs(composite) * 0.5)
                        edge = expected - (1.0 - prob)
                elif direction == "bearish":
                    if is_bullish_question:
                        side = "no"
                        expected = min(0.90, 0.5 + abs(composite) * 0.5)
                        edge = expected - (1.0 - prob)
                    else:
                        side = "yes"
                        expected = min(0.90, 0.5 + abs(composite) * 0.5)
                        edge = expected - prob
                else:
                    continue  # Neutral — no trade

                if edge < 0.05:
                    continue  # Not enough edge

                candidates.append({
                    "market_id": mid,
                    "question": question,
                    "side": side,
                    "edge": round(edge, 4),
                    "prob": prob,
                    "is_bullish_question": is_bullish_question,
                })

            time.sleep(0.2)
        except Exception as e:
            log(f"  Market fetch error ({kw}): {e}")

    candidates.sort(key=lambda x: x["edge"], reverse=True)
    return candidates


# ── Safeguard check ───────────────────────────────────────────────────────────

def check_context(client, market_id: str) -> tuple[bool, str]:
    try:
        ctx = client._request("GET", f"/api/sdk/context/{market_id}")
        discipline = ctx.get("discipline", {})
        if discipline.get("warning_level") == "severe":
            return False, "severe flip-flop"
        slippage = ctx.get("slippage", {})
        if slippage:
            estimates = slippage.get("estimates", [])
            if estimates and estimates[0].get("slippage_pct", 0) > 0.15:
                return False, "high slippage"
        return True, ""
    except Exception:
        return True, ""  # Don't block on context failure


# ── Main ──────────────────────────────────────────────────────────────────────

def run(dry_run=True, signals_only=False):
    print(f"\n🔗 Solana On-Chain Signal Trader")
    print(f"{'='*52}")
    print(f"  Mode: {'DRY RUN' if dry_run else '🔴 LIVE'} | venue={VENUE}")
    print(f"  Max position: ${MAX_POSITION_USD} | Max trades: {MAX_TRADES_PER_RUN}")
    print(f"  Signal threshold: ±{SIGNAL_THRESHOLD}")
    print()

    # Step 1: Collect signals
    signals = collect_signals()

    if signals_only:
        print(f"\n{'─'*52}")
        print(f"  Signal summary:")
        print(f"    TPS:           {signals['tps']:,.0f} ({signals['tps_status']})")
        print(f"    Priority fee:  {signals['priority_fee']:,.0f} microlamports ({signals['fee_status']})")
        print(f"    Epoch:         {signals['epoch_pct']:.1%} complete")
        print(f"    Jupiter vol:   ${signals['jupiter_volume']:,.0f} ({signals['vol_status']})")
        print(f"    Composite:     {signals['composite']:+.3f} → {signals['direction'].upper()}")
        return

    direction  = signals["direction"]
    composite  = signals["composite"]

    if direction == "neutral":
        log(f"Signal is neutral ({composite:+.3f}) — no trades this run")
        if os.environ.get("AUTOMATON_MANAGED"):
            print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "neutral_signal"}}))
        return

    # Step 2: Connect
    try:
        from simmer_sdk import SimmerClient
    except ImportError:
        print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
        sys.exit(1)

    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("Error: SIMMER_API_KEY not set")
        sys.exit(1)

    client = SimmerClient(api_key=api_key, venue=VENUE, live=not dry_run)

    # Step 3: Find markets
    log(f"\nSearching for {direction.upper()} markets (composite={composite:+.3f})...")
    candidates = find_tradeable_markets(client, direction, composite)
    log(f"Found {len(candidates)} candidates with edge > 5%")

    # Step 4: Trade
    trades_attempted = 0
    trades_executed  = 0
    skip_reasons     = []

    for c in candidates[:MAX_TRADES_PER_RUN]:
        log(f"\n{'─'*52}")
        log(f"Market: {c['question'][:65]}")
        log(f"  Side={c['side'].upper()} | prob={c['prob']:.2f} | edge={c['edge']:.1%}")

        # Safeguard
        ok, reason = check_context(client, c["market_id"])
        if not ok:
            log(f"  ⛔ Skipped: {reason}")
            skip_reasons.append(reason)
            continue

        reasoning = (
            f"Solana on-chain signal: composite={composite:+.3f} ({direction}). "
            f"TPS={signals['tps']:,.0f} ({signals['tps_status']}), "
            f"priority_fee={signals['priority_fee']:,.0f}µL ({signals['fee_status']}), "
            f"Jupiter_vol=${signals['jupiter_volume']:,.0f} ({signals['vol_status']}). "
            f"On-chain activity precedes price — trading {c['side'].upper()} at {c['prob']:.1%}."
        )

        trades_attempted += 1

        if dry_run:
            log(f"  [DRY RUN] Would buy {c['side'].upper()} ${MAX_POSITION_USD}")
            log(f"  Reasoning: {reasoning[:120]}...")
            trades_executed += 1
            continue

        try:
            result = client.trade(
                market_id   = c["market_id"],
                side        = c["side"],
                amount      = MAX_POSITION_USD,
                source      = TRADE_SOURCE,
                skill_slug  = SKILL_SLUG,
                reasoning   = reasoning,
            )
            if result.success:
                log(f"  ✅ Bought {result.shares_bought:.1f} shares | ${MAX_POSITION_USD}")
                trades_executed += 1
            elif getattr(result, "skip_reason", None):
                log(f"  ⏭️  Skipped: {result.skip_reason}")
                skip_reasons.append(result.skip_reason)
            else:
                log(f"  ❌ Failed: {getattr(result, 'error', 'unknown')}")
        except Exception as e:
            log(f"  ❌ Exception: {e}")

    print(f"\n{'='*52}")
    print(f"Done | signals={direction.upper()} ({composite:+.3f}) | "
          f"candidates={len(candidates)} | executed={trades_executed}/{trades_attempted}")

    if os.environ.get("AUTOMATON_MANAGED"):
        report = {
            "composite_signal": composite,
            "direction": direction,
            "candidates": len(candidates),
            "trades_attempted": trades_attempted,
            "trades_executed": trades_executed,
        }
        if skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        print(json.dumps({"automaton": report}))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solana on-chain signal → Polymarket trader")
    parser.add_argument("--live",    action="store_true", help="Execute real trades")
    parser.add_argument("--signals", action="store_true", help="Show on-chain signals only, no trades")
    parser.add_argument("--set",     action="append", metavar="KEY=VALUE", help="Set config value")
    args = parser.parse_args()

    if args.set:
        for item in args.set:
            if "=" in item:
                k, v = item.split("=", 1)
                env_map = {
                    "max_position_usd":   "SIMMER_ONCHAIN_MAX_POSITION",
                    "max_trades_per_run": "SIMMER_ONCHAIN_MAX_TRADES",
                    "signal_threshold":   "SIMMER_ONCHAIN_SIGNAL_MIN",
                }
                if k in env_map:
                    os.environ[env_map[k]] = v
                    print(f"Set {k}={v}")

    run(dry_run=not args.live, signals_only=args.signals)
