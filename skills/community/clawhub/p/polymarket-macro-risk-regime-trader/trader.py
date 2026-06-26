"""
polymarket-macro-risk-regime-trader
Detects macro risk regimes (risk-on vs risk-off) by reading signals across ALL
imported Polymarket categories simultaneously. When crypto trends down,
geopolitical escalation markets trend up, and commodity stress markets trend up,
the regime is risk-off. Trades markets in OTHER categories that haven't repriced
yet to the new regime.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-risk-regime-trader"
SKILL_SLUG   = "polymarket-macro-risk-regime-trader"

KEYWORDS = [
    'Bitcoin', 'Ethereum', 'BTC', 'ETH', 'crypto',
    'oil', 'crude', 'commodity', 'gold', 'natural gas',
    'war', 'military', 'Iran', 'Israel', 'Russia', 'Ukraine',
    'NATO', 'ceasefire', 'sanctions', 'invasion', 'nuclear',
    'China', 'Taiwan', 'Gaza', 'missile', 'escalation',
    'weather', 'hurricane', 'tornado', 'earthquake',
    'sports', 'NBA', 'NFL', 'soccer', 'tennis',
    'election', 'Trump', 'Biden', 'congress', 'regulation',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Regime-specific tunables
REGIME_CRYPTO_THRESHOLD = float(os.environ.get("SIMMER_REGIME_CRYPTO_THRESHOLD", "0.45"))
REGIME_GEO_THRESHOLD    = float(os.environ.get("SIMMER_REGIME_GEO_THRESHOLD",   "0.60"))
REGIME_COMMODITY_THRESHOLD = float(os.environ.get("SIMMER_REGIME_COMMODITY_THRESHOLD", "0.50"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global REGIME_CRYPTO_THRESHOLD, REGIME_GEO_THRESHOLD, REGIME_COMMODITY_THRESHOLD
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        if live:
            _client.live = True
        try:
            _client.apply_skill_config(SKILL_SLUG)
        except AttributeError:
            pass  # apply_skill_config only available in Simmer runtime
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        REGIME_CRYPTO_THRESHOLD = float(os.environ.get("SIMMER_REGIME_CRYPTO_THRESHOLD", str(REGIME_CRYPTO_THRESHOLD)))
        REGIME_GEO_THRESHOLD    = float(os.environ.get("SIMMER_REGIME_GEO_THRESHOLD",    str(REGIME_GEO_THRESHOLD)))
        REGIME_COMMODITY_THRESHOLD = float(os.environ.get("SIMMER_REGIME_COMMODITY_THRESHOLD", str(REGIME_COMMODITY_THRESHOLD)))
    return _client


# ---------------------------------------------------------------------------
# Category classification
# ---------------------------------------------------------------------------

_CRYPTO_TERMS = {"bitcoin", "btc", "ethereum", "eth", "solana", "sol", "xrp",
                 "crypto", "dogecoin", "doge", "litecoin", "cardano", "ada"}
_GEO_TERMS = {"war", "military", "iran", "israel", "russia", "ukraine", "nato",
              "ceasefire", "sanctions", "invasion", "nuclear", "china", "taiwan",
              "gaza", "missile", "escalation", "north korea", "dprk", "coup",
              "conflict", "attack", "strike", "bomb"}
_COMMODITY_TERMS = {"oil", "crude", "commodity", "gold", "natural gas", "wheat",
                    "copper", "silver", "brent", "wti", "barrel"}
_SPORTS_TERMS = {"nba", "nfl", "mlb", "nhl", "soccer", "tennis", "football",
                 "basketball", "baseball", "hockey", "ufc", "boxing"}
_WEATHER_TERMS = {"weather", "hurricane", "tornado", "earthquake", "flood",
                  "temperature", "precipitation", "storm", "wildfire"}


def classify_market(question: str) -> str:
    """Classify a market question into a category."""
    q = question.lower()
    if any(t in q for t in _CRYPTO_TERMS):
        return "crypto"
    if any(t in q for t in _GEO_TERMS):
        return "geopolitics"
    if any(t in q for t in _COMMODITY_TERMS):
        return "commodity"
    if any(t in q for t in _SPORTS_TERMS):
        return "sports"
    if any(t in q for t in _WEATHER_TERMS):
        return "weather"
    return "other"


# ---------------------------------------------------------------------------
# Regime detection
# ---------------------------------------------------------------------------

def compute_category_scores(markets: list) -> dict:
    """
    Compute average probability per category.
    Returns dict with keys: crypto_score, geo_risk_score, commodity_stress.
    """
    buckets: dict[str, list[float]] = {
        "crypto": [], "geopolitics": [], "commodity": [],
        "sports": [], "weather": [], "other": [],
    }
    for m in markets:
        q = getattr(m, "question", "")
        cat = classify_market(q)
        p = getattr(m, "current_probability", None)
        if p is not None:
            buckets[cat].append(p)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0.5

    return {
        "crypto_score": avg(buckets["crypto"]),
        "geo_risk_score": avg(buckets["geopolitics"]),
        "commodity_stress": avg(buckets["commodity"]),
        "counts": {k: len(v) for k, v in buckets.items()},
    }


def detect_regime(scores: dict) -> str:
    """
    Determine macro regime from category scores.
    risk_off: crypto weak AND geopolitical risk elevated AND commodity stress high.
    risk_on: opposite conditions.
    neutral: mixed signals.
    """
    crypto = scores["crypto_score"]
    geo    = scores["geo_risk_score"]
    commod = scores["commodity_stress"]

    if crypto < REGIME_CRYPTO_THRESHOLD and geo > REGIME_GEO_THRESHOLD and commod > REGIME_COMMODITY_THRESHOLD:
        return "risk_off"
    if crypto > (1 - REGIME_CRYPTO_THRESHOLD) and geo < (1 - REGIME_GEO_THRESHOLD):
        return "risk_on"
    return "neutral"


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """Find active markets via get_markets (primary) + keyword search (supplement)."""
    seen, unique = set(), []

    # 1. PRIMARY: broad scan of all markets
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[get_markets] {e}")

    # 2. SUPPLEMENT: keyword search for additional coverage
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, regime: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    In risk-off regime: markets still priced high (YES > NO_THRESHOLD) should
    reprice lower -- sell NO on them.
    In risk-on regime: markets still priced low (YES < YES_THRESHOLD) should
    reprice higher -- buy YES on them.
    Neutral regime: no trades.
    """
    p = market.current_probability
    q = getattr(market, "question", "")

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    if regime == "neutral":
        return None, 0, f"Neutral regime -- no cross-category edge at {p:.1%}"

    if regime == "risk_off" and p >= NO_THRESHOLD:
        # Market still priced high but regime is risk-off -- should be lower
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"RISK-OFF regime: NO YES={p:.0%} edge={edge:.0%} "
            f"size=${size} -- {q[:60]}"
        )

    if regime == "risk_on" and p <= YES_THRESHOLD:
        # Market still priced low but regime is risk-on -- should be higher
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"RISK-ON regime: YES {p:.0%} edge={edge:.0%} "
            f"size=${size} -- {q[:60]}"
        )

    return None, 0, f"No regime mismatch at {p:.1%} ({regime})"


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    """Check flip-flop and slippage safeguards."""
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            reason = ctx["discipline"].get("flip_flop_reason", "recent reversal")
            return False, f"Flip-flop: {reason}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[macro-risk-regime] mode={mode} max_pos=${MAX_POSITION} "
        f"crypto_thresh={REGIME_CRYPTO_THRESHOLD} geo_thresh={REGIME_GEO_THRESHOLD} "
        f"commodity_thresh={REGIME_COMMODITY_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[macro-risk-regime] {len(markets)} total markets discovered")

    # Compute category scores and detect regime
    scores = compute_category_scores(markets)
    regime = detect_regime(scores)
    safe_print(
        f"[macro-risk-regime] regime={regime.upper()} "
        f"crypto={scores['crypto_score']:.2f} geo={scores['geo_risk_score']:.2f} "
        f"commodity={scores['commodity_stress']:.2f} "
        f"counts={scores['counts']}"
    )

    if regime == "neutral":
        safe_print("[macro-risk-regime] Neutral regime -- no cross-category trades.")
        return

    # In risk-off: look for markets outside the driving categories that are still high
    # In risk-on: look for markets outside the driving categories that are still low
    # The driving categories (crypto, geo, commodity) already moved -- trade the laggards
    driving_cats = {"crypto", "geopolitics", "commodity"}
    tradeable = [
        m for m in markets
        if classify_market(getattr(m, "question", "")) not in driving_cats
    ]
    safe_print(f"[macro-risk-regime] {len(tradeable)} non-driving-category markets to scan")

    placed = 0
    for m in tradeable:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, regime)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=m.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[macro-risk-regime] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Detects macro risk regimes across all Polymarket categories and trades lagging markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
