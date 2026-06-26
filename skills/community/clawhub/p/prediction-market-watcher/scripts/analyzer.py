"""
analyzer.py — Market analysis engine for Kalshi agent
Scores markets by edge, confidence, and risk. No SDK required.
"""

import re
from typing import Optional


def _to_cents(val) -> int:
    """Convert dollar string or int/float to cents."""
    try:
        return int(round(float(val) * 100))
    except (TypeError, ValueError):
        return 0


def score_market(market: dict, current_price_yes: Optional[int] = None) -> dict:
    """
    Score a single market for betting attractiveness.
    Returns a dict with score, reasoning, and recommended action.

    market: raw market dict from Kalshi API
    current_price_yes: override yes price in cents (uses market data if None)
    """
    result = {
        "ticker": market.get("ticker", "?"),
        "title": market.get("title", "?"),
        "score": 0,
        "confidence": "low",
        "recommended_side": None,
        "recommended_price": None,
        "reasoning": [],
        "skip": False,
        "skip_reason": None,
    }

    # ── Basic validity checks ──────────────────────────────────────────────
    status = market.get("status", "")
    if status not in ("open", "active"):
        result["skip"] = True
        result["skip_reason"] = f"Market status: {status}"
        return result

    # Support both old (cents int) and new (dollar string) API formats
    yes_bid = _to_cents(market.get("yes_bid_dollars") or market.get("yes_bid", 0))
    yes_ask = _to_cents(market.get("yes_ask_dollars") or market.get("yes_ask", 0))
    no_bid  = _to_cents(market.get("no_bid_dollars")  or market.get("no_bid", 0))
    no_ask  = _to_cents(market.get("no_ask_dollars")  or market.get("no_ask", 0))
    last_price = _to_cents(market.get("last_price_dollars") or market.get("last_price", 0))
    volume_24h = float(market.get("volume_24h_fp") or market.get("volume_24h", 0))
    open_interest = float(market.get("open_interest_fp") or market.get("open_interest", 0))
    liquidity = _to_cents(market.get("liquidity_dollars") or market.get("liquidity", 0))

    price_yes = current_price_yes or yes_ask or last_price or 50

    # ── Skip illiquid markets ──────────────────────────────────────────────
    if volume_24h < 100 and open_interest < 50:
        result["skip"] = True
        result["skip_reason"] = f"Low liquidity (24h vol: {volume_24h}, OI: {open_interest})"
        return result

    if yes_ask == 0 and no_ask == 0:
        result["skip"] = True
        result["skip_reason"] = "No active orderbook"
        return result

    # ── Spread analysis ────────────────────────────────────────────────────
    if yes_bid and yes_ask:
        spread = yes_ask - yes_bid
        if spread > 15:
            result["reasoning"].append(f"Wide spread ({spread}¢) — harder to profit")
            result["score"] -= 10
        elif spread <= 5:
            result["reasoning"].append(f"Tight spread ({spread}¢) — good liquidity")
            result["score"] += 10

    # ── Price extremes (near-certainties) ─────────────────────────────────
    if price_yes >= 90:
        result["reasoning"].append(f"YES trading at {price_yes}¢ — near certainty, low upside")
        result["score"] -= 15
    elif price_yes <= 10:
        result["reasoning"].append(f"YES trading at {price_yes}¢ — near-zero, buying NO is low upside")
        result["score"] -= 15
    elif 35 <= price_yes <= 65:
        result["reasoning"].append(f"YES at {price_yes}¢ — contested market, more edge potential")
        result["score"] += 8

    # ── Volume signal ──────────────────────────────────────────────────────
    if volume_24h > 1000:
        result["reasoning"].append(f"High 24h volume ({volume_24h}) — active market")
        result["score"] += 12
    elif volume_24h > 300:
        result["reasoning"].append(f"Moderate volume ({volume_24h})")
        result["score"] += 5

    # ── Category signals ──────────────────────────────────────────────────
    title_lower = market.get("title", "").lower()
    series = market.get("series_ticker", "").lower()

    # Sports — avoid (high variance, hard to edge)
    if any(w in title_lower for w in ["nba", "nfl", "nhl", "mlb", "nascar", "f1", "ufc", "boxing"]):
        result["reasoning"].append("Sports market — high variance, skip")
        result["score"] -= 20

    # Economic data — good for informed bets
    if any(w in title_lower for w in ["cpi", "fed", "rate", "gdp", "jobs", "unemployment", "inflation", "fomc"]):
        result["reasoning"].append("Economic data market — informational edge possible")
        result["score"] += 15

    # Crypto — we have edge here
    if any(w in title_lower for w in ["bitcoin", "btc", "eth", "solana", "sol", "crypto"]):
        result["reasoning"].append("Crypto market — Quirk has edge here")
        result["score"] += 20

    # Politics — volatile, skip unless high conviction
    if any(w in title_lower for w in ["trump", "biden", "congress", "senate", "house", "election", "president"]):
        result["reasoning"].append("Political market — high uncertainty, reduce score")
        result["score"] -= 5

    # ── Confidence rating ──────────────────────────────────────────────────
    if result["score"] >= 25:
        result["confidence"] = "high"
    elif result["score"] >= 10:
        result["confidence"] = "medium"
    else:
        result["confidence"] = "low"

    # ── Recommended action ─────────────────────────────────────────────────
    if result["confidence"] in ("high", "medium") and not result["skip"]:
        # Default: bet with the market's implied direction
        # More nuanced logic can be added with news/research context
        if price_yes < 50:
            result["recommended_side"] = "no"
            result["recommended_price"] = no_ask or (100 - price_yes)
        else:
            result["recommended_side"] = "yes"
            result["recommended_price"] = yes_ask or price_yes

    return result


def rank_markets(markets: list, top_n: int = 10) -> list:
    """Score and rank a list of markets, return top N non-skipped."""
    scored = [score_market(m) for m in markets]
    valid = [s for s in scored if not s["skip"]]
    ranked = sorted(valid, key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]


def format_market_report(scored_markets: list) -> str:
    """Human-readable report of top markets."""
    if not scored_markets:
        return "No scoreable markets found."

    lines = ["═" * 60, "  KALSHI MARKET ANALYSIS REPORT", "═" * 60]
    for i, m in enumerate(scored_markets, 1):
        lines.append(f"\n#{i} [{m['confidence'].upper()}] Score: {m['score']}")
        lines.append(f"   {m['title']}")
        lines.append(f"   Ticker: {m['ticker']}")
        if m["recommended_side"]:
            lines.append(
                f"   → Bet {m['recommended_side'].upper()} @ {m['recommended_price']}¢"
            )
        for r in m["reasoning"]:
            lines.append(f"   • {r}")
    lines.append("\n" + "═" * 60)
    return "\n".join(lines)
