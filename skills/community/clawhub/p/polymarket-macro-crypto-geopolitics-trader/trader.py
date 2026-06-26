"""
polymarket-macro-crypto-geopolitics-trader
Trades the lag between geopolitical escalation markets and crypto price threshold
markets on Polymarket. Iran military escalation -> oil spike -> crypto drops
(inverse correlation in crisis). When geo markets moved but crypto thresholds
haven't adjusted yet, trade the divergence.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-crypto-geopolitics-trader"
SKILL_SLUG   = "polymarket-macro-crypto-geopolitics-trader"

KEYWORDS = [
    'Iran', 'Israel', 'military', 'war', 'ceasefire',
    'attack', 'strike', 'missile', 'escalation', 'conflict',
    'Bitcoin above', 'Bitcoin price', 'BTC above', 'BTC price',
    'Bitcoin below', 'crypto', 'Ethereum above', 'ETH price',
    'oil', 'crude', 'Hezbollah', 'Gaza', 'nuclear',
    'sanctions', 'invasion', 'drone',
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

# Strategy-specific tunables
GEO_HOT       = float(os.environ.get("SIMMER_GEO_HOT",       "0.60"))
CRYPTO_LAG    = float(os.environ.get("SIMMER_CRYPTO_LAG",     "0.10"))

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
    global GEO_HOT, CRYPTO_LAG
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
        GEO_HOT        = float(os.environ.get("SIMMER_GEO_HOT",       str(GEO_HOT)))
        CRYPTO_LAG     = float(os.environ.get("SIMMER_CRYPTO_LAG",    str(CRYPTO_LAG)))
    return _client


# ---------------------------------------------------------------------------
# Market classification
# ---------------------------------------------------------------------------

_GEO_ESCALATION_TERMS = {
    "iran", "israel", "military", "war", "attack", "strike", "missile",
    "escalation", "conflict", "hezbollah", "gaza", "invasion", "drone",
    "bomb", "nuclear", "sanctions",
}

_GEO_DEESCALATION_TERMS = {
    "ceasefire", "peace", "truce", "negotiation", "talks", "deal",
    "withdrawal", "diplomacy",
}

_CRYPTO_THRESHOLD_TERMS = {
    "bitcoin above", "btc above", "bitcoin price", "btc price",
    "bitcoin below", "btc below", "ethereum above", "eth above",
    "ethereum price", "eth price", "crypto",
}


def is_geo_escalation(question: str) -> bool:
    """Return True if market is about geopolitical escalation."""
    q = question.lower()
    # Must match escalation terms but NOT be purely de-escalation
    has_escalation = any(t in q for t in _GEO_ESCALATION_TERMS)
    is_pure_deesc = any(t in q for t in _GEO_DEESCALATION_TERMS) and not has_escalation
    return has_escalation and not is_pure_deesc


def is_geo_deescalation(question: str) -> bool:
    """Return True if market is about geopolitical de-escalation."""
    q = question.lower()
    return any(t in q for t in _GEO_DEESCALATION_TERMS)


def is_crypto_threshold(question: str) -> bool:
    """Return True if market is a crypto price threshold market."""
    q = question.lower()
    return any(t in q for t in _CRYPTO_THRESHOLD_TERMS)


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
# Geo-crypto divergence detection
# ---------------------------------------------------------------------------

def compute_geo_heat(markets: list) -> tuple[float, int]:
    """
    Compute weighted average of geopolitical escalation market probabilities.
    Higher = more conflict expected.
    De-escalation markets are inverted (1 - p) to contribute to heat.
    Returns (geo_heat, count).
    """
    probs = []
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if p is None:
            continue
        if is_geo_escalation(q):
            probs.append(p)
        elif is_geo_deescalation(q):
            probs.append(1 - p)  # Low ceasefire probability = high heat
    if not probs:
        return 0.5, 0
    return sum(probs) / len(probs), len(probs)


def compute_crypto_optimism(markets: list) -> tuple[float, int]:
    """
    Compute average of crypto price threshold market probabilities.
    Higher = market expects crypto to go up / stay above thresholds.
    Returns (crypto_optimism, count).
    """
    probs = []
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if p is None:
            continue
        if is_crypto_threshold(q):
            probs.append(p)
    if not probs:
        return 0.5, 0
    return sum(probs) / len(probs), len(probs)


def detect_divergence(geo_heat: float, crypto_optimism: float) -> str:
    """
    Detect divergence between geopolitical heat and crypto optimism.
    Returns: 'crypto_lagging_high', 'crypto_lagging_low', or 'no_divergence'.
    """
    divergence = abs(geo_heat - (1 - crypto_optimism))

    if geo_heat > GEO_HOT and crypto_optimism > 0.50:
        # Hot conflict but crypto still bullish -- crypto should be lower
        if divergence >= CRYPTO_LAG:
            return "crypto_lagging_high"

    if geo_heat < (1 - GEO_HOT) and crypto_optimism < (1 - 0.50):
        # Calming geopolitics but crypto still bearish -- crypto should be higher
        if divergence >= CRYPTO_LAG:
            return "crypto_lagging_low"

    return "no_divergence"


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, divergence_type: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    crypto_lagging_high: crypto thresholds are too optimistic -- sell NO on high ones.
    crypto_lagging_low: crypto thresholds are too pessimistic -- buy YES on low ones.
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

    if divergence_type == "crypto_lagging_high" and p >= NO_THRESHOLD:
        # Crypto still bullish but geo is hot -- sell NO (expect crypto to drop)
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"GEO-HOT crypto lag: NO YES={p:.0%} edge={edge:.0%} "
            f"size=${size} -- {q[:55]}"
        )

    if divergence_type == "crypto_lagging_low" and p <= YES_THRESHOLD:
        # Geo calming but crypto still bearish -- buy YES (expect crypto to rise)
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"GEO-CALM crypto lag: YES {p:.0%} edge={edge:.0%} "
            f"size=${size} -- {q[:55]}"
        )

    return None, 0, f"No tradeable lag at {p:.1%} ({divergence_type})"


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
        f"[crypto-geopolitics] mode={mode} max_pos=${MAX_POSITION} "
        f"geo_hot={GEO_HOT} crypto_lag={CRYPTO_LAG}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[crypto-geopolitics] {len(markets)} total markets discovered")

    # Compute geo heat and crypto optimism
    geo_heat, geo_count = compute_geo_heat(markets)
    crypto_opt, crypto_count = compute_crypto_optimism(markets)
    safe_print(
        f"[crypto-geopolitics] geo_heat={geo_heat:.2f} ({geo_count} markets) "
        f"crypto_optimism={crypto_opt:.2f} ({crypto_count} markets)"
    )

    divergence_type = detect_divergence(geo_heat, crypto_opt)
    safe_print(f"[crypto-geopolitics] divergence={divergence_type}")

    if divergence_type == "no_divergence":
        safe_print("[crypto-geopolitics] No geo-crypto divergence detected. Done.")
        return

    # Only trade crypto threshold markets (the lagging side)
    crypto_markets = [
        m for m in markets if is_crypto_threshold(getattr(m, "question", ""))
    ]
    safe_print(f"[crypto-geopolitics] {len(crypto_markets)} crypto threshold markets to scan")

    placed = 0
    for m in crypto_markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, divergence_type)
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

    safe_print(f"[crypto-geopolitics] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades geo-crypto divergence: Iran escalation vs BTC price thresholds on Polymarket."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
