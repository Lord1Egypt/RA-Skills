"""
polymarket-macro-fear-index-trader
Builds a custom fear index from ALL imported Polymarket markets and trades
the overreaction. Aggregates geopolitical escalation, falling crypto,
extreme weather, and rising disease signals into a composite fear score.
When fear is extreme, markets OVERREACT and everything gets sold -- this
skill buys the most oversold markets pushed below YES_THRESHOLD by panic.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-fear-index-trader"
SKILL_SLUG   = "polymarket-macro-fear-index-trader"

# Classification keywords for fear categories
GEO_FEAR_KW = [
    'war', 'invasion', 'military', 'escalation', 'nuclear', 'missile',
    'sanctions', 'conflict', 'attack', 'troops', 'nato', 'ceasefire',
    'occupation', 'airstrike', 'drone strike', 'territorial',
]
CRYPTO_KW = [
    'bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'sol', 'crypto',
    'xrp', 'above', 'below', 'price',
]
HEALTH_FEAR_KW = [
    'measles', 'pandemic', 'outbreak', 'cases', 'virus', 'disease',
    'epidemic', 'covid', 'bird flu', 'h5n1', 'mpox', 'who emergency',
    'mortality', 'infection',
]
WEATHER_FEAR_KW = [
    'hurricane', 'tornado', 'flood', 'wildfire', 'earthquake',
    'extreme weather', 'category 5', 'tropical storm', 'cyclone',
    'tsunami', 'heatwave', 'heat wave', 'drought', 'blizzard',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Skill-specific tunables
FEAR_THRESHOLD     = float(os.environ.get("SIMMER_FEAR_THRESHOLD",     "0.65"))
COMPLACENCY_THRESHOLD = float(os.environ.get("SIMMER_COMPLACENCY_THRESHOLD", "0.30"))
# Fear component weights
GEO_WEIGHT     = float(os.environ.get("SIMMER_GEO_WEIGHT",     "0.35"))
CRYPTO_WEIGHT  = float(os.environ.get("SIMMER_CRYPTO_WEIGHT",  "0.30"))
HEALTH_WEIGHT  = float(os.environ.get("SIMMER_HEALTH_WEIGHT",  "0.20"))
WEATHER_WEIGHT = float(os.environ.get("SIMMER_WEATHER_WEIGHT", "0.15"))

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
    global FEAR_THRESHOLD, COMPLACENCY_THRESHOLD
    global GEO_WEIGHT, CRYPTO_WEIGHT, HEALTH_WEIGHT, WEATHER_WEIGHT
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
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        FEAR_THRESHOLD     = float(os.environ.get("SIMMER_FEAR_THRESHOLD",     str(FEAR_THRESHOLD)))
        COMPLACENCY_THRESHOLD = float(os.environ.get("SIMMER_COMPLACENCY_THRESHOLD", str(COMPLACENCY_THRESHOLD)))
        GEO_WEIGHT     = float(os.environ.get("SIMMER_GEO_WEIGHT",     str(GEO_WEIGHT)))
        CRYPTO_WEIGHT  = float(os.environ.get("SIMMER_CRYPTO_WEIGHT",  str(CRYPTO_WEIGHT)))
        HEALTH_WEIGHT  = float(os.environ.get("SIMMER_HEALTH_WEIGHT",  str(HEALTH_WEIGHT)))
        WEATHER_WEIGHT = float(os.environ.get("SIMMER_WEATHER_WEIGHT", str(WEATHER_WEIGHT)))
    return _client


# ---------------------------------------------------------------------------
# Market classification and fear scoring
# ---------------------------------------------------------------------------

def classify_fear(question: str) -> str | None:
    """Classify a market into a fear category: 'geo', 'crypto', 'health', 'weather', or None."""
    q = question.lower()
    if any(kw in q for kw in GEO_FEAR_KW):
        return "geo"
    if any(kw in q for kw in CRYPTO_KW):
        return "crypto"
    if any(kw in q for kw in HEALTH_FEAR_KW):
        return "health"
    if any(kw in q for kw in WEATHER_FEAR_KW):
        return "weather"
    return None


def is_escalation_market(question: str) -> bool:
    """Check if a geo market implies escalation (high P = more fear)."""
    q = question.lower()
    return any(w in q for w in (
        "escalat", "invad", "invasion", "military action", "attack",
        "nuclear", "war", "missile", "airstrike", "troops",
    ))


def is_crypto_bullish_market(question: str) -> bool:
    """Check if a crypto market is bullish (high P = crypto up = LESS fear)."""
    q = question.lower()
    return any(w in q for w in ("above", "over", "reach", "hit", "exceed", "higher"))


def is_health_escalation(question: str) -> bool:
    """Check if a health market implies more cases/worse outcome (high P = more fear)."""
    q = question.lower()
    return any(w in q for w in (
        "cases", "exceed", "above", "more than", "outbreak", "pandemic",
        "emergency", "mortality", "deaths",
    ))


def is_weather_extreme(question: str) -> bool:
    """Check if a weather market implies extreme events (high P = more fear)."""
    q = question.lower()
    return any(w in q for w in (
        "category", "major", "extreme", "record", "exceed", "above",
        "hurricane", "tornado", "flood", "wildfire",
    ))


def compute_fear_score(prob: float, category: str, question: str) -> float:
    """
    Convert a market probability into a fear contribution (0.0 - 1.0).
    High score = more fear.
    """
    if category == "geo":
        # Escalation markets: high P = high fear
        if is_escalation_market(question):
            return prob
        # Ceasefire/peace markets: high P = low fear
        return 1 - prob

    elif category == "crypto":
        # Crypto bullish markets: high P = low fear (crypto up = calm)
        if is_crypto_bullish_market(question):
            return 1 - prob  # Low P(BTC up) = high crypto fear
        # Crypto bearish markets: high P = high fear
        return prob

    elif category == "health":
        if is_health_escalation(question):
            return prob  # High P(more cases) = high fear
        return 1 - prob

    elif category == "weather":
        if is_weather_extreme(question):
            return prob  # High P(extreme weather) = high fear
        return 1 - prob

    return 0.5


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based sizing per CLAUDE.md.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


def compute_panic_signal(market, fear_index: float) -> tuple[str | None, float, str]:
    """
    Panic-regime signal: buy oversold markets pushed too low by fear.
    Conviction scales with both how oversold the market is AND how extreme the fear is.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    if p > YES_THRESHOLD:
        return None, 0, f"Not oversold at {p:.1%} (above {YES_THRESHOLD:.0%})"

    # Base conviction from how far below threshold
    base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    # Fear multiplier: the more extreme the fear, the more likely it's panic-driven
    fear_excess = (fear_index - FEAR_THRESHOLD) / (1 - FEAR_THRESHOLD)
    fear_mult = 1 + min(0.5, fear_excess)  # Up to 1.5x boost from extreme fear

    conviction = min(1.0, base_conviction * fear_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
    edge = YES_THRESHOLD - p

    return "yes", size, (
        f"PANIC-BUY YES p={p:.0%} edge={edge:.0%} fear={fear_index:.0%} "
        f"size=${size} -- {q[:55]}"
    )


def compute_complacency_signal(market, fear_index: float) -> tuple[str | None, float, str]:
    """
    Complacency-regime signal: sell overpriced markets when fear is too low.
    Markets at high probabilities during extreme complacency may be overpriced.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    if p < NO_THRESHOLD:
        return None, 0, f"Not overpriced at {p:.1%} (below {NO_THRESHOLD:.0%})"

    # Base conviction from how far above threshold
    base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
    # Complacency multiplier: the lower the fear, the more complacent the market
    complacency_excess = (COMPLACENCY_THRESHOLD - fear_index) / COMPLACENCY_THRESHOLD
    complacency_mult = 1 + min(0.5, complacency_excess)

    conviction = min(1.0, base_conviction * complacency_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
    edge = p - NO_THRESHOLD

    return "no", size, (
        f"COMPLACENT-SELL NO p={p:.0%} edge={edge:.0%} fear={fear_index:.0%} "
        f"size=${size} -- {q[:50]}"
    )


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


def find_markets(client: SimmerClient) -> list:
    """
    Primary discovery via get_markets(limit=200).
    Returns ALL markets -- classification happens later.
    """
    seen: set[str] = set()
    unique: list = []

    # Primary: bulk fetch
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                seen.add(market_id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[macro-fear-index] mode={mode} max_pos=${MAX_POSITION} "
        f"fear_threshold={FEAR_THRESHOLD} complacency={COMPLACENCY_THRESHOLD}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[macro-fear-index] {len(markets)} total markets fetched")

    # Classify and score fear components
    geo_scores: list[float] = []
    crypto_scores: list[float] = []
    health_scores: list[float] = []
    weather_scores: list[float] = []

    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue
        p = float(p)
        cat = classify_fear(q)
        if cat == "geo":
            geo_scores.append(compute_fear_score(p, "geo", q))
        elif cat == "crypto":
            crypto_scores.append(compute_fear_score(p, "crypto", q))
        elif cat == "health":
            health_scores.append(compute_fear_score(p, "health", q))
        elif cat == "weather":
            weather_scores.append(compute_fear_score(p, "weather", q))

    # Compute component averages (default to neutral 0.5 if no markets found)
    geo_fear = sum(geo_scores) / len(geo_scores) if geo_scores else 0.5
    crypto_fear = sum(crypto_scores) / len(crypto_scores) if crypto_scores else 0.5
    health_fear = sum(health_scores) / len(health_scores) if health_scores else 0.5
    weather_fear = sum(weather_scores) / len(weather_scores) if weather_scores else 0.5

    safe_print(
        f"  [fear] geo={geo_fear:.2f}({len(geo_scores)}mkts) "
        f"crypto={crypto_fear:.2f}({len(crypto_scores)}mkts) "
        f"health={health_fear:.2f}({len(health_scores)}mkts) "
        f"weather={weather_fear:.2f}({len(weather_scores)}mkts)"
    )

    # Composite fear index (weighted average)
    fear_index = (
        GEO_WEIGHT * geo_fear
        + CRYPTO_WEIGHT * crypto_fear
        + HEALTH_WEIGHT * health_fear
        + WEATHER_WEIGHT * weather_fear
    )
    safe_print(f"  [fear-index] composite={fear_index:.2%}")

    # Determine regime
    placed = 0
    if fear_index > FEAR_THRESHOLD:
        # PANIC regime: markets are oversold by fear -- buy the most oversold
        safe_print(
            f"  [regime] PANIC (fear={fear_index:.0%} > {FEAR_THRESHOLD:.0%}) "
            f"-- looking for oversold markets to buy"
        )

        # Find all markets below YES_THRESHOLD, sorted by probability (most oversold first)
        oversold = []
        for m in markets:
            p = float(m.current_probability)
            if p <= YES_THRESHOLD:
                oversold.append(m)
        oversold.sort(key=lambda m: float(m.current_probability))

        safe_print(f"  [panic] {len(oversold)} oversold markets (p <= {YES_THRESHOLD:.0%})")

        for m in oversold:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_panic_signal(m, fear_index)
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
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    elif fear_index < COMPLACENCY_THRESHOLD:
        # COMPLACENCY regime: markets are overpriced -- sell the most overpriced
        safe_print(
            f"  [regime] COMPLACENCY (fear={fear_index:.0%} < {COMPLACENCY_THRESHOLD:.0%}) "
            f"-- looking for overpriced markets to sell"
        )

        overpriced = []
        for m in markets:
            p = float(m.current_probability)
            if p >= NO_THRESHOLD:
                overpriced.append(m)
        overpriced.sort(key=lambda m: float(m.current_probability), reverse=True)

        safe_print(f"  [complacency] {len(overpriced)} overpriced markets (p >= {NO_THRESHOLD:.0%})")

        for m in overpriced:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_complacency_signal(m, fear_index)
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
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    else:
        # NEUTRAL regime: no extreme fear or complacency -- use standard signals
        safe_print(
            f"  [regime] NEUTRAL (fear={fear_index:.0%}) "
            f"-- falling back to standard conviction signals"
        )
        for m in markets:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_signal(m)
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
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[macro-fear-index] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Custom fear index trader for Polymarket -- buys panic oversells, sells complacency overpricing."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
