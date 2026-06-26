#!/usr/bin/env python3
"""
Polymarket Mispricing Events — Cross-Platform Consensus Trader

Scans all active Polymarket markets, estimates true probability by
cross-referencing Kalshi + Manifold, detects mispricings > threshold,
and trades via SimmerClient using Kelly criterion sizing.

Edge: When Polymarket price diverges from consensus of 2+ prediction markets,
there's a statistical arbitrage opportunity. This bot captures that gap.

Author: Mibayy
"""

import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime, timezone

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants & Config
# ---------------------------------------------------------------------------
SKILL_SLUG  = "polymarket-mispricing-events"
TRADE_SOURCE = "sdk:polymarket-mispricing-events"

# Entry / sizing
ENTRY_THRESHOLD   = float(os.environ.get("EVENTS_ENTRY_THRESHOLD", "0.15"))  # 15% gap min
KELLY_FRACTION    = float(os.environ.get("EVENTS_KELLY_FRACTION", "0.25"))   # quarter-kelly
TRADE_SIZE_MIN    = float(os.environ.get("EVENTS_TRADE_SIZE_MIN", "5.0"))
TRADE_SIZE_MAX    = float(os.environ.get("EVENTS_TRADE_SIZE_MAX", "50.0"))
MAX_POSITIONS     = int(os.environ.get("EVENTS_MAX_POSITIONS", "8"))

# Scanner filters
MIN_LIQUIDITY     = float(os.environ.get("EVENTS_MIN_LIQUIDITY", "500.0"))
MAX_SPREAD        = float(os.environ.get("EVENTS_MAX_SPREAD", "0.15"))
MAX_GAP_CAP       = float(os.environ.get("EVENTS_MAX_GAP_CAP", "0.35"))  # gap >35% = model wrong
MISPRICING_MIN    = float(os.environ.get("EVENTS_MISPRICING_MIN", "1.5")) # est_prob > mkt * 1.5

# Platform weights for consensus
PLATFORM_WEIGHTS  = {"kalshi": 0.55, "manifold": 0.45}

# API endpoints
GAMMA_URL   = "https://gamma-api.polymarket.com"
CLOB_URL    = "https://clob.polymarket.com"
KALSHI_URL  = "https://api.elections.kalshi.com/trade-api/v2"
MANIFOLD_URL = "https://api.manifold.markets/v0"

# Caches (in-process, reset each run)
_kalshi_cache  = None
_kalshi_ts     = 0.0
_KALSHI_TTL    = 600

_manifold_cache = None
_manifold_ts    = 0.0
_MANIFOLD_TTL   = 600

log = logging.getLogger("mispricing-events")

# ---------------------------------------------------------------------------
# HTTP Session
# ---------------------------------------------------------------------------
def _make_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=2, backoff_factor=0.3, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(pool_connections=4, pool_maxsize=10, max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

_session = _make_session()

# ---------------------------------------------------------------------------
# SimmerClient
# ---------------------------------------------------------------------------
_client = None
def get_client() -> SimmerClient:
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=os.environ.get("TRADING_VENUE", "sim"),
        )
    return _client


# ---------------------------------------------------------------------------
# Context check (flip-flop, slippage, edge)
# ---------------------------------------------------------------------------
def check_context(market_id: str, my_probability: float = None) -> tuple[bool, str]:
    try:
        client = get_client()
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        ctx = client.get_market_context(market_id, **params)
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning")
        if flip_flop and "SEVERE" in flip_flop:
            return False, f"flip-flop: {flip_flop}"
        slippage = ctx.get("slippage", {})
        if slippage.get("slippage_pct", 0) > 0.15:
            return False, "slippage too high"
        edge = ctx.get("edge_analysis", {})
        if edge.get("recommendation") == "HOLD":
            return False, "edge below threshold"
        return True, "ok"
    except Exception:
        return True, "context unavailable"


# ---------------------------------------------------------------------------
# Fuzzy title matching (Jaccard on word tokens)
# ---------------------------------------------------------------------------
def _normalize(text: str) -> set:
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    words = text.split()
    stopwords = {"will", "the", "a", "an", "in", "of", "to", "be", "is", "are",
                 "on", "at", "for", "with", "by", "or", "and", "not", "who"}
    return {w for w in words if len(w) > 2 and w not in stopwords}

def jaccard(a: str, b: str) -> float:
    sa, sb = _normalize(a), _normalize(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# ---------------------------------------------------------------------------
# Kalshi markets fetch
# ---------------------------------------------------------------------------
def _fetch_kalshi() -> list:
    global _kalshi_cache, _kalshi_ts
    now = time.time()
    if _kalshi_cache is not None and now - _kalshi_ts < _KALSHI_TTL:
        return _kalshi_cache
    try:
        r = _session.get(f"{KALSHI_URL}/markets", params={"limit": 200, "status": "open"}, timeout=10)
        if not r.ok:
            return _kalshi_cache or []
        data = r.json().get("markets", [])
        _kalshi_cache = data
        _kalshi_ts = now
        return data
    except Exception:
        return _kalshi_cache or []


# ---------------------------------------------------------------------------
# Manifold markets fetch
# ---------------------------------------------------------------------------
def _fetch_manifold() -> list:
    global _manifold_cache, _manifold_ts
    now = time.time()
    if _manifold_cache is not None and now - _manifold_ts < _MANIFOLD_TTL:
        return _manifold_cache
    try:
        r = _session.get(f"{MANIFOLD_URL}/markets", params={"limit": 500}, timeout=10)
        if not r.ok:
            return _manifold_cache or []
        data = r.json()
        _manifold_cache = data
        _manifold_ts = now
        return data
    except Exception:
        return _manifold_cache or []


# ---------------------------------------------------------------------------
# Cross-platform probability estimation
# ---------------------------------------------------------------------------
def estimate_probability(question: str, poly_price: float) -> tuple[float, list, int]:
    """
    Returns (estimated_prob, sources_used, confidence_0_to_3).
    Uses fuzzy matching to find same market on Kalshi/Manifold.
    Falls back to poly_price if no cross-platform match found.
    """
    sources  = []
    weighted = 0.0
    total_w  = 0.0

    # Kalshi
    kalshi_markets = _fetch_kalshi()
    best_k, best_ks = None, 0.0
    for km in kalshi_markets:
        title = km.get("title") or km.get("question") or ""
        sim = jaccard(question, title)
        if sim > best_ks:
            best_ks = sim
            best_k = km
    if best_k and best_ks >= 0.35:
        try:
            yes_price = float(best_k.get("yes_ask", best_k.get("last_price", 0)) or 0)
            if 0.02 < yes_price < 0.98:
                w = PLATFORM_WEIGHTS["kalshi"]
                weighted += yes_price * w
                total_w  += w
                sources.append(f"kalshi={yes_price:.2f}(sim={best_ks:.2f})")
        except Exception:
            pass

    # Manifold
    manifold_markets = _fetch_manifold()
    best_m, best_ms = None, 0.0
    for mm in manifold_markets:
        q = mm.get("question", "")
        sim = jaccard(question, q)
        if sim > best_ms:
            best_ms = sim
            best_m = mm
    if best_m and best_ms >= 0.35:
        try:
            prob = float(best_m.get("probability", 0) or 0)
            if 0.02 < prob < 0.98:
                w = PLATFORM_WEIGHTS["manifold"]
                weighted += prob * w
                total_w  += w
                sources.append(f"manifold={prob:.2f}(sim={best_ms:.2f})")
        except Exception:
            pass

    if total_w > 0:
        est = weighted / total_w
        confidence = len(sources)
    else:
        # No cross-platform data: fallback to polymarket price (no edge)
        est = poly_price
        confidence = 0

    return round(est, 4), sources, confidence


# ---------------------------------------------------------------------------
# Polymarket market scanner
# ---------------------------------------------------------------------------
def scan_for_mispricings() -> list:
    """Fetch active markets and return mispricing signals."""
    signals = []
    offset = 0
    limit  = 100
    max_pages = 5

    for _ in range(max_pages):
        try:
            r = _session.get(f"{GAMMA_URL}/markets", params={
                "closed": "false", "active": "true",
                "limit": limit, "offset": offset,
                "order": "liquidity", "ascending": "false",
            }, timeout=15)
            if not r.ok:
                break
            markets = r.json()
            if not markets:
                break
        except Exception as e:
            log.warning(f"Gamma fetch error: {e}")
            break

        for m in markets:
            try:
                # Basic filters
                liquidity = float(m.get("liquidity") or 0)
                if liquidity < MIN_LIQUIDITY:
                    continue

                outcomes = m.get("outcomes", "[]")
                if isinstance(outcomes, str):
                    outcomes = json.loads(outcomes)
                if len(outcomes) != 2:
                    continue  # binary only

                prices_str = m.get("outcomePrices", "[]")
                if isinstance(prices_str, str):
                    prices_str = json.loads(prices_str)
                if len(prices_str) < 2:
                    continue

                price_yes = float(prices_str[0])
                price_no  = float(prices_str[1])

                # Spread filter
                spread = abs(price_yes + price_no - 1.0)
                if spread > MAX_SPREAD:
                    continue

                # Skip near-resolved markets
                if price_yes > 0.92 or price_yes < 0.08:
                    continue

                question  = m.get("question", "")
                market_id = m.get("id", "")
                cid       = m.get("conditionId", "")

                if not question or not market_id:
                    continue

                # Estimate true probability
                est_prob, sources, confidence = estimate_probability(question, price_yes)

                # Check mispricing (YES underpriced)
                gap_yes = est_prob - price_yes
                if (confidence >= 1
                        and est_prob > price_yes * MISPRICING_MIN
                        and gap_yes >= ENTRY_THRESHOLD
                        and gap_yes <= MAX_GAP_CAP):
                    signals.append({
                        "market_id": market_id,
                        "condition_id": cid,
                        "question": question,
                        "side": "BUY",
                        "poly_price": price_yes,
                        "est_prob": est_prob,
                        "gap": gap_yes,
                        "liquidity": liquidity,
                        "sources": sources,
                        "confidence": confidence,
                    })

                # Check mispricing (NO underpriced = YES overpriced)
                gap_no = (1.0 - est_prob) - price_no
                if (confidence >= 1
                        and (1.0 - est_prob) > price_no * MISPRICING_MIN
                        and gap_no >= ENTRY_THRESHOLD
                        and gap_no <= MAX_GAP_CAP):
                    signals.append({
                        "market_id": market_id,
                        "condition_id": cid,
                        "question": question,
                        "side": "SELL",
                        "poly_price": price_yes,
                        "est_prob": est_prob,
                        "gap": gap_no,
                        "liquidity": liquidity,
                        "sources": sources,
                        "confidence": confidence,
                    })

            except Exception:
                continue

        offset += limit
        if len(markets) < limit:
            break

    # Sort by gap descending, take top 20
    signals.sort(key=lambda s: s["gap"], reverse=True)
    return signals[:20]


# ---------------------------------------------------------------------------
# Kelly sizing
# ---------------------------------------------------------------------------
def kelly_size(edge: float, price: float, capital: float) -> float:
    """
    Full Kelly = edge / (1 - price).
    We use KELLY_FRACTION * full_kelly, capped between min and max.
    """
    if price <= 0 or price >= 1:
        return TRADE_SIZE_MIN
    full_kelly_pct = edge / (1.0 - price)
    size = full_kelly_pct * KELLY_FRACTION * capital
    return max(TRADE_SIZE_MIN, min(TRADE_SIZE_MAX, round(size, 2)))


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler()],
    )

    client = get_client()

    log.info(f"[{SKILL_SLUG}] Starting")
    log.info(f"[{SKILL_SLUG}] Threshold={ENTRY_THRESHOLD:.0%} Kelly={KELLY_FRACTION} MaxPos={MAX_POSITIONS}")

    # Get current portfolio state
    try:
        portfolio   = client.get_portfolio()
        capital     = float(portfolio.get("sim_balance", 100.0))
        positions   = client.get_positions()
        open_count  = len([p for p in positions if not p.resolved]) if positions else 0
    except Exception as e:
        log.warning(f"Portfolio fetch failed: {e}")
        capital    = 100.0
        open_count = 0

    log.info(f"[{SKILL_SLUG}] Capital=${capital:.2f} OpenPositions={open_count}")

    if open_count >= MAX_POSITIONS:
        log.info(f"[{SKILL_SLUG}] Max positions reached ({open_count}/{MAX_POSITIONS}), skipping scan")
        return

    # Scan for mispricings
    log.info(f"[{SKILL_SLUG}] Scanning markets...")
    signals = scan_for_mispricings()
    log.info(f"[{SKILL_SLUG}] Found {len(signals)} mispricing signals")

    if not signals:
        log.info(f"[{SKILL_SLUG}] No signals this cycle")
        return

    trades_placed = 0
    slots_available = MAX_POSITIONS - open_count

    for sig in signals:
        if trades_placed >= slots_available:
            break

        question  = sig["question"]
        market_id = sig["market_id"]
        side      = sig["side"]
        est_prob  = sig["est_prob"]
        gap       = sig["gap"]
        sources   = sig["sources"]
        confidence = sig["confidence"]

        log.info(
            f"[{SKILL_SLUG}] Signal: {side} '{question[:60]}' "
            f"gap={gap:+.1%} est={est_prob:.2f} src={sources}"
        )

        # Context check
        ok, reason = check_context(market_id, my_probability=est_prob)
        if not ok:
            log.info(f"[{SKILL_SLUG}] Skip {market_id}: {reason}")
            continue

        # Kelly sizing
        price = sig["poly_price"] if side == "BUY" else (1.0 - sig["poly_price"])
        size  = kelly_size(gap, price, capital)

        try:
            market = client.find_markets(query=question[:80])
            if not market:
                log.warning(f"[{SKILL_SLUG}] Market not found via SDK: {question[:50]}")
                continue
            m = market[0] if isinstance(market, list) else market

            trade = client.trade(
                market_id=m.id,
                side=side,
                size=size,
                skill_slug=SKILL_SLUG,
                source=TRADE_SOURCE,
                metadata={
                    "gap": round(gap, 4),
                    "est_prob": est_prob,
                    "confidence": confidence,
                    "sources": "|".join(sources),
                },
            )
            log.info(
                f"[{SKILL_SLUG}] TRADED {side} ${size:.2f} on '{question[:50]}' "
                f"gap={gap:+.1%} — id={getattr(trade, 'id', '?')}"
            )
            trades_placed += 1
            capital -= size  # rough accounting

        except Exception as e:
            log.error(f"[{SKILL_SLUG}] Trade failed for {market_id}: {e}")
            continue

    log.info(f"[{SKILL_SLUG}] Done. {trades_placed} trades placed this cycle.")


if __name__ == "__main__":
    main()
