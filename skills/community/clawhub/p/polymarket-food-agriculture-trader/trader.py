"""
polymarket-food-agriculture-trader
Trades food and agriculture prediction markets: crop yields, commodity prices,
food inflation, alternative protein, and supply shocks.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-food-agriculture-trader"
SKILL_SLUG   = "polymarket-food-agriculture-trader"

KEYWORDS = [
    'wheat', 'corn', 'soybean', 'coffee', 'cocoa', 'sugar',
    'food price', 'crop yield', 'drought', 'harvest', 'USDA', 'FAO',
    'food inflation', 'famine', 'supply shock', 'alternative protein',
    'Beyond Meat', 'Impossible Foods', 'lab-grown', 'vertical farming',
    'fertilizer', 'potash', 'nitrogen', 'El Niño crop', 'La Niña harvest',
    'WASDE', 'commodity', 'rice', 'palm oil', 'livestock', 'cattle',
    'food security', 'grain', 'oilseed',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "7"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by crop calendar and commodity type.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# USDA WASDE is published monthly. Most market-moving editions:
# Jun = first summer crop estimate (huge uncertainty), Aug = critical yield update,
# Nov = final pre-harvest estimate, Jan = annual wrap. Boost conviction in these months.
_WASDE_HIGH_IMPACT_MONTHS = {6, 8, 11, 1}

# Northern hemisphere planting window = Mar–May (uncertainty at peak = edge).
_PLANTING_MONTHS = {3, 4, 5}

# Brazil/Argentina soy/corn harvest = Jan–Apr (major Southern hemisphere window).
_SOUTH_HARVEST_MONTHS = {1, 2, 3, 4}

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
            if m.id not in seen and any(w in q for w in ("wheat", "corn", "coffee", "cocoa", "agriculture", "harvest", "food")):
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
            if m.id not in seen and any(w in q for w in ("wheat", "corn", "coffee", "cocoa", "agriculture", "harvest", "food")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def harvest_cycle_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.40) combining two agricultural
    structural edges:

    1. CROP CALENDAR / WASDE TIMING
       Agricultural markets have their highest information asymmetry at two
       points: (a) during the planting window (Mar–May) when yield uncertainty
       peaks, and (b) around USDA WASDE report months (Jun, Aug, Nov, Jan) when
       professional traders have better reads than retail on what the report
       will show. Outside these windows, edge compresses.

       Crop question + WASDE high-impact month (Jun, Aug, Nov, Jan) → 1.20x
       Crop question + planting season (Mar–May)                    → 1.15x
       Crop question + S. hemisphere harvest (Jan–Apr, soy/corn)    → 1.10x
       Crop question + off-season                                    → 0.90x
       Non-crop question                                             → 1.00x

    2. COMMODITY TYPE CONFIDENCE
       Different agricultural sub-categories have vastly different predictability
       based on supply concentration, data availability, and narrative vs data
       pricing.

       Cocoa / coffee (W. Africa + Brazil concentration)  → 1.25x
         Supply is ~70% concentrated in a few countries — weather events
         in Côte d'Ivoire, Ghana, or Brazil are strong, front-runnable signals.

       Wheat / corn / soy / grain / oilseed (USDA-driven) → 1.20x
         WASDE is the most data-rich public report in commodities — professional
         futures markets lead; Polymarket retail lags by days.

       Fertilizer / potash / nitrogen (input prices)      → 1.15x
         Upstream agricultural inputs move on Russian export policy and energy
         prices — longer lead times than retail appreciates.

       Alternative protein / lab-grown meat               → 1.10x
         FDA/USDA FSIS approval milestones are public record — regulatory
         calendar creates predictable resolution timing that retail ignores.

       Food inflation / CPI / FAO index                   → 1.05x
         Lagged, well-reported data — moderate edge at best.

       Famine / food crisis / food security               → 0.75x
         Humanitarian narratives create emotional pricing — geopolitical
         complexity makes timing very hard.

       Drought / wildfire crop damage                     → 0.85x
         Already heavily covered in media — crowded trade, edge mostly gone
         by the time a Polymarket question is created.

    Combined and capped at 1.40x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: crop calendar timing
    crop_keywords = ("wheat", "corn", "soy", "soybean", "maize", "rice", "grain",
                     "oilseed", "crop", "harvest", "yield", "planting", "cocoa",
                     "coffee", "sugar", "cotton", "palm oil", "livestock", "cattle")

    if any(w in q for w in crop_keywords):
        if month in _WASDE_HIGH_IMPACT_MONTHS:
            timing_mult = 1.20  # USDA WASDE high-impact months — pro vs retail divergence peaks
        elif month in _PLANTING_MONTHS:
            timing_mult = 1.15  # N. hemisphere planting — yield uncertainty at maximum
        elif month in _SOUTH_HARVEST_MONTHS:
            timing_mult = 1.10  # S. hemisphere harvest window — Brazil/Argentina soy/corn
        else:
            timing_mult = 0.90  # Off-season — catalysts scarce, less edge
    else:
        timing_mult = 1.0   # Non-crop questions — no seasonal timing edge

    # Factor 2: commodity type confidence
    if any(w in q for w in ("cocoa", "coffee", "cacao")):
        type_mult = 1.25  # High geographic concentration — weather in W. Africa/Brazil front-runnable

    elif any(w in q for w in ("wheat", "corn", "soybean", "soy", "maize", "rice",
                               "grain", "oilseed", "wasde", "usda", "crop yield")):
        type_mult = 1.20  # WASDE data-driven — professional futures lead, retail lags

    elif any(w in q for w in ("fertilizer", "potash", "nitrogen", "ammonia",
                               "phosphate", "urea")):
        type_mult = 1.15  # Upstream input markets — longer lead times than retail prices in

    elif any(w in q for w in ("alternative protein", "lab-grown", "lab grown",
                               "cultivated meat", "beyond meat", "impossible",
                               "plant-based")):
        type_mult = 1.10  # Regulatory calendar is public — milestones predictable

    elif any(w in q for w in ("food inflation", "food price", "cpi food",
                               "fao", "food index", "grocery")):
        type_mult = 1.05  # Data-driven but lagged — moderate edge

    elif any(w in q for w in ("famine", "food crisis", "food security",
                               "food shortage", "starvation", "hunger")):
        type_mult = 0.75  # Humanitarian narrative pricing — hard to time, high variance

    elif any(w in q for w in ("drought", "wildfire", "flood crop", "crop damage",
                               "crop failure", "flood harvest")):
        type_mult = 0.85  # Crowded media trade — edge mostly gone by question creation

    else:
        type_mult = 1.0

    return min(1.40, timing_mult * type_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with harvest cycle and commodity type adjustment:
    - Base conviction scales linearly with distance from threshold
    - harvest_cycle_bias() boosts WASDE-window and geographically concentrated
      commodities (cocoa, coffee), dampens crowded drought trades and
      emotionally priced food-crisis markets
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: replace market.current_probability with CME agricultural futures
    implied probability to trade the divergence between professional futures
    and Polymarket retail pricing.
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

    bias = harvest_cycle_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by harvest cycle bias
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
    print(f"[polymarket-food-agriculture-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-food-agriculture-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-food-agriculture-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades food and agriculture prediction markets: crop yields, commodity prices, food inflation, alternative protein, and supply shocks.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
