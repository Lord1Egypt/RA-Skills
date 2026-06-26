"""
polymarket-catastrophe-trader
Trades Polymarket prediction markets on hurricane seasons, earthquake probabilities, wildfire forecasts, and extreme weather records that trigger insurance and reinsurance markets.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-catastrophe-trader"
SKILL_SLUG   = "polymarket-catastrophe-trader"

KEYWORDS = [
    'hurricane', 'tropical storm', 'category 5', 'Atlantic season', 'named storm',
    'tornado', 'wildfire', 'acres burned', 'fire season', 'earthquake', 'magnitude',
    'tsunami', 'volcanic eruption', '100-year flood', 'FEMA', 'disaster declaration',
    'billion-dollar disaster', 'polar vortex', 'bomb cyclone', 'derecho', 'heat dome',
    'hottest year', 'warmest year', 'temperature record', 'blizzard', 'ice storm',
    'above-normal season', 'NOAA', 'NHC', 'Category 4', 'major hurricane',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "7"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by hazard type, data quality,
# and whether it is currently peak season for the relevant natural peril.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Atlantic hurricane season: Jun 1 – Nov 30; peaks August–October.
_HURRICANE_PEAK_MONTHS   = {8, 9, 10}   # NHC issuing daily advisories; models update every 6h
_HURRICANE_ACTIVE_MONTHS = {6, 7, 11}   # Active but below peak frequency

# Western US wildfire season: May–October; peaks July–September.
_WILDFIRE_PEAK_MONTHS    = {7, 8, 9}    # NIFC daily updates; drought indices current
_WILDFIRE_ACTIVE_MONTHS  = {5, 6, 10}  # Fire weather increasing / decreasing

# Tornado alley season: March–June; peak April–May.
_TORNADO_PEAK_MONTHS     = {3, 4, 5, 6}

# Winter storm season: December–February.
_WINTER_STORM_MONTHS     = {12, 1, 2}

# Global temperature record: data finalised Jan–Feb; trajectory clear Oct–Dec.
_TEMP_RECORD_MONTHS      = {1, 2, 10, 11, 12}

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
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def catastrophe_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.35) combining two structural edges
    unique to catastrophe and extreme weather prediction markets:

    1. HAZARD TYPE / DATA QUALITY
       Catastrophe markets are uniquely mispriced because retail anchors on the
       most recent disaster (availability bias) rather than base rates from
       decades of scientific records. The edge scales with how well-modelled the
       hazard is:

       Named storm count / above-normal Atlantic season        → 1.25x
         NOAA seasonal outlooks have 40+ years of calibrated base rates.
         Above/below-normal classifications are ~70% accurate at 90-day lead.
         Retail over-reacts after the first storm (20–40% spike) and under-
         prices when early weeks are quiet. The base rate, not the headline,
         is the signal.

       Global temperature record (hottest year/month)          → 1.20x
         Climate trend is measured to ±0.01°C annually by NOAA, Berkeley
         Earth, and NASA GISS simultaneously. Retail doesn't check these. A
         year that is tracking 0.15°C above the prior record with 3 months
         remaining is a near-certainty the market underprices.

       Billion-dollar disaster count                           → 1.20x
         NOAA tracks US billion-dollar disasters since 1980. The trend is
         clearly upward — climate change + expanding insured asset base. Retail
         anchors to average years; above-trend frequency is structurally
         under-priced for season-count markets.

       Wildfire season severity (acres burned, state records)  → 1.20x
         NIFC year-to-date acres burned vs 10-year average is a 2–4 week
         leading indicator for "will X state set a fire record?" markets.
         Drought index (Palmer Z-score, PDSI) leads fire activity by weeks.
         This data is public, updated daily — retail doesn't look.

       Major hurricane (Cat 3+) landfall probability           → 1.10x
         NHC 2–5 day track cone probabilities are well-calibrated (verified
         annually against outcomes). Retail systematically overprices
         landfall probability when a storm exists anywhere in the Atlantic
         — the NHC's landfall-specific probability is far lower than visual
         cone intuition implies.

       Tornado season record / outbreak                        → 1.10x
         SPC seasonal outlook is reliable at the 3-month scale; specific
         outbreak timing within the season is genuinely harder to predict.

       FEMA disaster declaration                               → 0.85x
         Political and bureaucratic discretion adds real noise beyond the
         meteorological signal. Declaration timing relative to market
         resolution adds another layer of unpredictability.

       Earthquake (M7+, specific region/window)               → 0.80x
         Genuinely unpredictable on short timescales. USGS probabilistic
         seismic hazard models give long-run annual rates, not quarterly
         windows. Retail and trader are equally blind here.

       Tsunami / volcanic eruption                             → 0.75x
         Triggered by the underlying earthquake or geologic event that
         cannot itself be predicted. Lowest-edge category in catastrophe
         markets — trade only at MIN_TRADE floor.

    2. SEASONAL CALENDAR — PEAK SEASON TIMING
       Catastrophe data is only actionable when models are actively running.
       NOAA, NHC, and SPC issue daily updates during peak season — the signal
       quality of base-rate comparisons is highest when current season data
       is being produced in real time. Off-season markets are priced on stale
       data and thin volumes.

       Atlantic hurricane: peak Aug–Oct → 1.25x, shoulder Jun–Jul/Nov → 1.10x,
         off-season → 0.85x
       Western wildfire: peak Jul–Sep → 1.20x, shoulder May–Jun/Oct → 1.10x,
         off-season → 0.90x
       Tornado alley: peak Mar–Jun → 1.15x, off-season → 0.90x
       Winter storm: active Dec–Feb → 1.10x, off-season → 0.90x
       Temperature record: trajectory clear Oct–Dec, final Jan–Feb → 1.15x

    Combined and capped at 1.35x.
    Named storm count in Aug–Oct: 1.25 × 1.25 = 1.35x cap — maximum edge.
    Temperature record in Jan: 1.20 × 1.15 = 1.35x cap — trajectory certain.
    Tsunami any time: 0.75x — always near MIN_TRADE floor.
    Earthquake off-season: 0.80x × 1.0 = 0.80x — minimum data, minimum edge.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: hazard type / data quality
    if any(w in q for w in ("named storm", "atlantic season", "hurricane season",
                              "tropical storm count", "above-normal season",
                              "storm count", "named atlantic")):
        type_mult = 1.25  # NOAA 40+ year calibrated base rates; availability bias spike exploitable

    elif any(w in q for w in ("hottest year", "warmest year", "temperature record",
                               "hottest month", "warmest month", "global temperature",
                               "above pre-industrial", "record warm", "record high temperature")):
        type_mult = 1.20  # Measured to ±0.01°C; retail doesn't check Berkeley Earth / NASA GISS

    elif any(w in q for w in ("billion-dollar disaster", "billion dollar disaster",
                               "disaster count", "costliest disaster", "most expensive storm",
                               "billion in damage")):
        type_mult = 1.20  # NOAA tracks; upward trend structural; retail anchors to average years

    elif any(w in q for w in ("wildfire", "acres burned", "fire season",
                               "fire year", "wildfire season", "fire record",
                               "burn area", "containment")):
        type_mult = 1.20  # NIFC YTD vs 10-year average: 2-4 week leading indicator

    elif any(w in q for w in ("category 4", "category 5", "category 3", "major hurricane",
                               "cat 4", "cat 5", "cat 3", "hurricane landfall",
                               "make landfall", "direct hit")):
        type_mult = 1.10  # NHC 2-5 day track cone probabilities annually verified

    elif any(w in q for w in ("tornado", "twister", "outbreak", "tornado record",
                               "ef4", "ef5", "tornado alley", "tornado watch",
                               "violent tornado")):
        type_mult = 1.10  # SPC seasonal outlook reliable; specific outbreak harder

    elif any(w in q for w in ("disaster declaration", "fema", "emergency declaration",
                               "federal disaster", "major disaster", "presidential declaration")):
        type_mult = 0.85  # Political + bureaucratic timing noise beyond meteorological signal

    elif any(w in q for w in ("earthquake", "magnitude", "seismic", "tremor",
                               "fault line", "aftershock", "richter", "usgs")):
        type_mult = 0.80  # Fundamentally unpredictable on quarterly timescales

    elif any(w in q for w in ("tsunami", "volcanic", "eruption", "lava", "caldera",
                               "pyroclastic", "ash cloud", "lahars")):
        type_mult = 0.75  # Triggered by unpredictable seismic/geologic events

    else:
        type_mult = 1.0

    # Factor 2: seasonal calendar — peak season for the detected hazard type
    is_hurricane = any(w in q for w in ("hurricane", "tropical storm", "named storm",
                                          "atlantic season", "category", "nhc", "cyclone"))
    is_wildfire  = any(w in q for w in ("wildfire", "fire season", "acres burned",
                                          "fire year", "fire record", "burn area"))
    is_tornado   = any(w in q for w in ("tornado", "twister", "outbreak", "ef4", "ef5"))
    is_winter    = any(w in q for w in ("blizzard", "winter storm", "polar vortex",
                                          "bomb cyclone", "ice storm", "snowfall record",
                                          "snowpack", "nor'easter"))
    is_temp      = any(w in q for w in ("hottest", "warmest", "temperature record",
                                          "global temperature", "above pre-industrial"))

    if is_hurricane:
        if month in _HURRICANE_PEAK_MONTHS:
            season_mult = 1.25  # NHC daily advisories; models update every 6h; data richest
        elif month in _HURRICANE_ACTIVE_MONTHS:
            season_mult = 1.10  # Active season; storms possible; below peak frequency
        else:
            season_mult = 0.85  # Off-season; no active systems; base rate near zero

    elif is_wildfire:
        if month in _WILDFIRE_PEAK_MONTHS:
            season_mult = 1.20  # NIFC daily updates; drought indices current; red flag warnings active
        elif month in _WILDFIRE_ACTIVE_MONTHS:
            season_mult = 1.10  # Fire weather building or receding
        else:
            season_mult = 0.90  # Winter: most fires extinguished or absent

    elif is_tornado:
        if month in _TORNADO_PEAK_MONTHS:
            season_mult = 1.15  # SPC issuing daily outlooks; storm reports accumulating
        else:
            season_mult = 0.90  # Off-season: tornado markets nearly untradeable

    elif is_winter:
        if month in _WINTER_STORM_MONTHS:
            season_mult = 1.10  # GFS/ECMWF ensemble agreement highest in peak months
        else:
            season_mult = 0.90  # Off-season: winter storm markets on stale forecasts

    elif is_temp:
        if month in _TEMP_RECORD_MONTHS:
            season_mult = 1.15  # Jan–Feb final; Oct–Dec trajectory clear from NOAA/Berkeley Earth
        else:
            season_mult = 1.0   # Mid-year: too early to call year-end record with confidence

    else:
        season_mult = 1.0

    return min(1.35, type_mult * season_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with catastrophe availability-bias correction
    and seasonal data quality timing:
    - Base conviction scales linearly with distance from threshold
    - catastrophe_bias() corrects for the core behavioral error in this
      domain: retail anchors to the most vivid recent disaster rather than
      base rates from 40+ years of NOAA / NIFC / NHC records
    - Peak season multiplier boosts edge when real-time model data is active
    - Earthquake/tsunami dampened — unpredictable even with good data
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed NOAA's named-storm seasonal forecast directly into p for
    season-count markets; use NIFC YTD acres vs 10-year average for wildfire
    severity markets; USGS ShakeMap for post-earthquake aftershock markets.
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

    bias = catastrophe_bias(q)

    if p <= YES_THRESHOLD:
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


def _season_tag() -> str:
    """Return a human-readable tag for the currently active hazard season."""
    month = datetime.now(timezone.utc).month
    if month in _HURRICANE_PEAK_MONTHS:
        return "hurricane=PEAK"
    if month in _HURRICANE_ACTIVE_MONTHS:
        return "hurricane=active"
    if month in _WILDFIRE_PEAK_MONTHS:
        return "wildfire=PEAK"
    if month in _WILDFIRE_ACTIVE_MONTHS:
        return "wildfire=active"
    if month in _TORNADO_PEAK_MONTHS:
        return "tornado=PEAK"
    if month in _WINTER_STORM_MONTHS:
        return "winter-storm=active"
    return "season=transition"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[polymarket-catastrophe-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} {_season_tag()}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-catastrophe-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-catastrophe-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on hurricane seasons, earthquake probabilities, wildfire forecasts, and extreme weather records.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
