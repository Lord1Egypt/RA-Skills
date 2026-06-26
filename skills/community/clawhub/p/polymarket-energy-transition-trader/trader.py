"""
polymarket-energy-transition-trader
Trades energy transition markets: EV adoption, solar/wind capacity, nuclear restarts,
oil prices, and energy policy milestones.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-energy-transition-trader"
SKILL_SLUG   = "polymarket-energy-transition-trader"

KEYWORDS = [
    'electric vehicle', 'EV', 'Tesla', 'BYD', 'charging station',
    'solar', 'wind energy', 'renewable', 'nuclear', 'uranium',
    'oil price', 'Brent crude', 'OPEC', 'energy transition',
    'battery', 'grid', 'power plant', 'carbon', 'net zero', 'IEA',
    'offshore wind', 'hydrogen', 'natural gas', 'LNG', 'pipeline',
    'energy storage', 'gigawatt', 'capacity', 'reactor', 'SMR',
    'EV adoption', 'EV sales', 'energy policy', 'carbon capture',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "7"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by technology tier and data calendar.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# OPEC+ holds biannual ministerial meetings in June and December, plus extraordinary
# sessions. Uncertainty in oil markets peaks in the weeks before these meetings.
_OPEC_MEETING_MONTHS = {6, 12}

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

    # Fast markets (may not exist in older SDK)
    try:
        for m in client.get_fast_markets():
            q = getattr(m, "question", "").lower()
            if m.id not in seen and any(w in q for w in ("electric vehicle", "ev ", "tesla", "solar", "wind energy", "battery", "renewable")):
                seen.add(m.id)
                unique.append(m)
    except (AttributeError, Exception):
        pass

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
            if m.id not in seen and any(w in q for w in ("electric vehicle", "ev ", "tesla", "solar", "wind energy", "battery", "renewable")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def transition_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.40) combining two energy transition
    structural edges:

    1. ENERGY DATA CALENDAR TIMING
       Different energy sub-sectors have well-defined data release rhythms where
       professional markets reprice and Polymarket retail lags:

       EV / battery + Q1 (Jan–Mar):
         IEA and BloombergNEF publish prior-year EV sales totals in Jan–Feb.
         Biggest data update of the year — retail pricing lags by weeks. → 1.20x

       Solar / wind / renewable capacity + Q4 (Oct–Dec):
         Year-end installation rush — projects race to complete before Dec 31.
         IEA and IRENA confirm GW additions in Q4. → 1.20x

       Oil / OPEC + OPEC meeting months (Jun, Dec):
         OPEC+ biannual ministerial meetings drive oil threshold markets.
         Since 2022, OPEC+ has surprised with production cuts 70%+ of the time.
         Uncertainty — and therefore edge — peaks in the pre-meeting window. → 1.15x

       Natural gas / LNG + winter peak (Nov–Feb):
         Gas demand and storage drawdown narratives drive LNG price markets
         in the Northern hemisphere winter. → 1.10x

       Other / off-cycle: → 1.00x

    2. TECHNOLOGY TIER CONFIDENCE
       Energy sub-sectors have dramatically different predictability based on
       data availability and whether pricing is driven by hard data or narrative.

       Nuclear restart / SMR approval        → 1.25x
         Regulatory timelines are public record from national nuclear authority
         filings. US retail is poorly informed on European/Asian nuclear policy —
         enormous information asymmetry.

       OPEC production cut / oil supply      → 1.20x
         OPEC+ has surprised with cuts 70%+ of the time since 2022.
         Retail systematically underprices — they expect OPEC to do nothing.

       Solar / wind GW capacity milestones   → 1.20x
         IEA and IRENA publish confirmed project pipelines. Markets on
         "will X GW be installed by Y" frequently underprice the published data.

       EV adoption / market share / sales    → 1.15x
         IEA monthly data lags Polymarket pricing by 1–2 months.
         Chinese BYD sales data provides even earlier leading signal.

       Oil price threshold (Brent / WTI)     → 1.10x
         Directional OPEC+ bias is documented, but daily volatility adds noise.

       Natural gas / LNG                     → 1.10x
         Winter demand is predictable; storage data from EIA is public weekly.

       Carbon / net zero policy pledge       → 0.80x
         Government net-zero commitments almost never resolve cleanly on time.
         Retail overprices policy sincerity. Ambiguity = poor resolution signal.

       Hydrogen / green hydrogen milestone   → 0.75x
         Perennial "5 years away" technology — retail consistently overprices
         hydrogen milestones that get pushed back. Cost-curve reality lags hype.

    Combined and capped at 1.40x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: data calendar timing
    ev_keywords = ("electric vehicle", "ev adoption", "ev sales", "ev market",
                   "byd", "tesla sales", "battery electric", "plugin")
    renewable_keywords = ("solar", "wind", "offshore wind", "renewable",
                          "gigawatt", "gw installed", "capacity")
    oil_keywords = ("opec", "oil price", "brent", "wti", "crude", "oil production",
                    "oil supply", "production cut")
    gas_keywords = ("natural gas", "lng", "liquefied natural gas", "gas storage",
                    "gas price", "gas supply")

    if any(w in q for w in ev_keywords):
        timing_mult = 1.20 if month in (1, 2, 3) else 1.0   # Q1: annual EV data drop
    elif any(w in q for w in renewable_keywords):
        timing_mult = 1.20 if month in (10, 11, 12) else 1.0  # Q4: year-end install rush
    elif any(w in q for w in oil_keywords):
        timing_mult = 1.15 if month in _OPEC_MEETING_MONTHS else 1.0  # OPEC meeting months
    elif any(w in q for w in gas_keywords):
        timing_mult = 1.10 if month in (11, 12, 1, 2) else 1.0  # Winter demand peak
    else:
        timing_mult = 1.0

    # Factor 2: technology tier confidence
    if any(w in q for w in ("nuclear", "reactor", "smr", "small modular",
                             "uranium", "nuclear restart", "nuclear plant")):
        type_mult = 1.25  # Public regulatory filings — huge info asymmetry vs US retail

    elif any(w in q for w in ("opec", "production cut", "oil supply",
                               "opec+", "saudi", "aramco")):
        type_mult = 1.20  # OPEC+ cuts 70%+ since 2022 — retail consistently underprices

    elif any(w in q for w in ("solar", "wind", "offshore wind", "gigawatt",
                               "gw installed", "renewable capacity")):
        type_mult = 1.20  # IEA/IRENA pipeline data leads market pricing

    elif any(w in q for w in ("electric vehicle", "ev adoption", "ev sales",
                               "ev market share", "byd", "tesla deliveries")):
        type_mult = 1.15  # IEA monthly data lags Polymarket by 1-2 months

    elif any(w in q for w in ("oil price", "brent", "wti", "crude price")):
        type_mult = 1.10  # Directional OPEC+ bias documented but high daily variance

    elif any(w in q for w in ("natural gas", "lng", "gas price", "gas storage")):
        type_mult = 1.10  # EIA weekly storage data is public — seasonal predictable

    elif any(w in q for w in ("net zero", "carbon neutral", "carbon pledge",
                               "climate target", "emissions target", "paris agreement")):
        type_mult = 0.80  # Policy pledges rarely resolve cleanly — ambiguous criteria

    elif any(w in q for w in ("hydrogen", "green hydrogen", "h2", "electrolysis",
                               "fuel cell", "hydrogen fuel")):
        type_mult = 0.75  # Perennial hype; milestones consistently slip — retail overprices

    else:
        type_mult = 1.0

    return min(1.40, timing_mult * type_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with energy data calendar and technology tier adjustment:
    - Base conviction scales linearly with distance from threshold
    - transition_bias() boosts nuclear (info asymmetry) and OPEC/solar in peak
      data windows, dampens hydrogen hype and vague net-zero pledges
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed IEA EV monthly sales or EIA petroleum report into p to trade
    the divergence between public data and Polymarket retail pricing directly.
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

    bias = transition_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by transition bias
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
    print(f"[polymarket-energy-transition-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-energy-transition-trader] {len(markets)} candidate markets")

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
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-energy-transition-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades energy transition markets: EV adoption, solar/wind capacity, nuclear restarts, oil prices, and energy policy milestones.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
