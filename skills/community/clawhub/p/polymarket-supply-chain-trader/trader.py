"""
polymarket-supply-chain-trader
Trades supply chain, logistics, commodity, and shipping prediction markets on Polymarket.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-supply-chain-trader"
SKILL_SLUG   = "polymarket-supply-chain-trader"

KEYWORDS = [
    'shipping', 'port', 'container', 'supply chain', 'logistics',
    'commodity', 'crude oil', 'Brent', 'natural gas', 'LNG',
    'steel price', 'lithium', 'cobalt', 'critical mineral',
    'semiconductor', 'chip shortage', 'TSMC', 'GPU',
    'delivery delay', 'Maersk', 'Rotterdam', 'Suez', 'Panama Canal',
    'Red Sea', 'freight', 'Baltic Dry', 'EV battery',
]

# Risk parameters — declared as tunables in clawhub.json, tunable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by seasonal shipping cycles
# and commodity-specific predictability patterns.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS, YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        # Load tunable overrides set via the Simmer UI (SIMMER_* vars only).
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
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active markets matching strategy keywords, deduplicated."""
    seen, unique = set(), []

    # Fast markets (best for active trading, may not exist in older SDK)
    try:
        for m in client.get_fast_markets():
            q = getattr(m, "question", "").lower()
            if m.id not in seen and any(w in q for w in ("supply", "shipping", "oil", "gas", "chip",
                    "semiconductor", "commodity", "freight", "port", "suez", "canal", "lithium")):
                seen.add(m.id)
                unique.append(m)
    except (AttributeError, Exception):
        pass  # get_fast_markets may not exist in older SDK versions

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")

    # Bulk scan fallback
    try:
        for m in client.get_markets(limit=200):
            q = getattr(m, "question", "").lower()
            if m.id not in seen and any(w in q for w in ("supply chain", "shipping", "oil price",
                    "natural gas", "semiconductor", "chip", "freight", "port", "suez", "lithium")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def disruption_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.80–1.40) combining two supply chain
    structural edges:

    1. SEASONAL SHIPPING CYCLES
       Container shipping has a well-documented Q4 crunch (Oct–Dec) driven
       by pre-holiday inventory builds. Congestion and delay markets are
       structurally more likely to resolve YES in Q4. Q1 is off-season.

       Shipping market + Q4 (Oct–Dec) → 1.25x  (peak crunch, lean into disruption)
       Shipping market + Q1 (Jan–Mar) → 0.85x  (off-season, dampen disruption)
       Shipping market + other months  → 1.05x  (mild mid-year boost)

    2. COMMODITY PREDICTABILITY
       Different commodities have vastly different information availability.
       Oil is the most liquid and well-modeled commodity in the world.
       Agricultural markets depend heavily on weather — high variance.

       Crude oil / energy / LNG       → 1.20x  (highly liquid, well-modeled)
       Semiconductors / chips / GPU   → 1.15x  (documented cycles, policy-driven)
       Lithium / cobalt / EV battery  → 1.15x  (China-concentrated, export data trackable)
       Chokepoints (Suez, Red Sea)    → 1.10x  (geopolitical risk well-documented)
       Agricultural / grain / harvest → 0.85x  (weather-dependent, high variance)

    Combined and capped at 1.40x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: seasonal shipping multiplier
    if any(w in q for w in ("shipping", "container", "port", "cargo", "freight", "maersk", "vessel", "congestion")):
        if 10 <= month <= 12:
            seasonal_mult = 1.25   # Q4 peak — pre-holiday inventory crunch
        elif 1 <= month <= 3:
            seasonal_mult = 0.85   # Q1 off-season — lower disruption risk
        else:
            seasonal_mult = 1.05   # mild mid-year activity
    else:
        seasonal_mult = 1.0

    # Factor 2: commodity predictability multiplier
    if any(w in q for w in ("crude oil", "brent", "wti", "oil price", "natural gas", "lng", "energy price")):
        commodity_mult = 1.20
    elif any(w in q for w in ("semiconductor", "chip", "tsmc", "nvidia", "gpu", "chip shortage", "wafer")):
        commodity_mult = 1.15
    elif any(w in q for w in ("lithium", "cobalt", "ev battery", "battery supply", "critical mineral")):
        commodity_mult = 1.15
    elif any(w in q for w in ("suez", "panama canal", "strait of hormuz", "red sea", "cape of good hope", "bab-el-mandeb")):
        commodity_mult = 1.10
    elif any(w in q for w in ("wheat", "corn", "soybean", "crop", "harvest", "agricultural", "grain", "rice")):
        commodity_mult = 0.85
    else:
        commodity_mult = 1.0

    return min(1.4, seasonal_mult * commodity_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with seasonal and commodity disruption adjustment:
    - Base conviction scales linearly with distance from threshold
    - disruption_bias() combines Q4 shipping cycles with commodity predictability
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Baltic Dry Index weekly change or AIS vessel queue counts
    into p to trade the divergence between real freight data and market price.
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
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    bias = disruption_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by disruption bias
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


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
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[polymarket-supply-chain-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-supply-chain-trader] {len(markets)} candidate markets")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            print(f"  [skip] {why}")
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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-supply-chain-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades supply chain, logistics, commodity, and shipping prediction markets on Polymarket.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
