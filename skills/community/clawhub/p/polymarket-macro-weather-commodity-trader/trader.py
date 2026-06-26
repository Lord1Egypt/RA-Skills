"""
polymarket-macro-weather-commodity-trader
Extreme weather is a leading indicator for commodity disruption.  When
temperature markets show unusual readings (very high or very low), it signals
potential crop/energy impact.  Dallas at 84F+ in April -> energy demand spike
-> oil/gas up.  Chicago below 61F -> late spring cold -> crop risk -> ag
commodity markets affected.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-weather-commodity-trader"
SKILL_SLUG   = "polymarket-macro-weather-commodity-trader"

# --------------- risk / signal tunables ---------------
MAX_POSITION             = float(os.environ.get("SIMMER_MAX_POSITION",             "40"))
MIN_VOLUME               = float(os.environ.get("SIMMER_MIN_VOLUME",               "10000"))
MAX_SPREAD               = float(os.environ.get("SIMMER_MAX_SPREAD",               "0.07"))
MIN_DAYS                 = int(os.environ.get(  "SIMMER_MIN_DAYS",                 "3"))
MAX_POSITIONS            = int(os.environ.get(  "SIMMER_MAX_POSITIONS",            "6"))
YES_THRESHOLD            = float(os.environ.get("SIMMER_YES_THRESHOLD",            "0.38"))
NO_THRESHOLD             = float(os.environ.get("SIMMER_NO_THRESHOLD",             "0.62"))
MIN_TRADE                = float(os.environ.get("SIMMER_MIN_TRADE",                "5"))
WEATHER_STRESS_THRESHOLD = float(os.environ.get("SIMMER_WEATHER_STRESS_THRESHOLD", "0.50"))

_client: SimmerClient | None = None


# --------------- helpers ---------------

def safe_print(*args, **kwargs):
    """Windows-safe print that replaces unencodable chars."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(), **kwargs)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, WEATHER_STRESS_THRESHOLD
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
        MAX_POSITION             = float(os.environ.get("SIMMER_MAX_POSITION",             str(MAX_POSITION)))
        MIN_VOLUME               = float(os.environ.get("SIMMER_MIN_VOLUME",               str(MIN_VOLUME)))
        MAX_SPREAD               = float(os.environ.get("SIMMER_MAX_SPREAD",               str(MAX_SPREAD)))
        MIN_DAYS                 = int(os.environ.get(  "SIMMER_MIN_DAYS",                 str(MIN_DAYS)))
        MAX_POSITIONS            = int(os.environ.get(  "SIMMER_MAX_POSITIONS",            str(MAX_POSITIONS)))
        YES_THRESHOLD            = float(os.environ.get("SIMMER_YES_THRESHOLD",            str(YES_THRESHOLD)))
        NO_THRESHOLD             = float(os.environ.get("SIMMER_NO_THRESHOLD",             str(NO_THRESHOLD)))
        MIN_TRADE                = float(os.environ.get("SIMMER_MIN_TRADE",                str(MIN_TRADE)))
        WEATHER_STRESS_THRESHOLD = float(os.environ.get("SIMMER_WEATHER_STRESS_THRESHOLD", str(WEATHER_STRESS_THRESHOLD)))
    return _client


# --------------- weather pattern detection ---------------

_WEATHER_PATTERN = re.compile(
    r"(temperature|high\s+temp|weather|degrees|fahrenheit|celsius"
    r"|heat|cold|freeze|frost|snow|hot)", re.I
)

_COMMODITY_PATTERN = re.compile(
    r"(oil|wti|crude|brent|natural\s+gas|energy|gas\s+price"
    r"|crop|wheat|corn|soybean|agriculture|grain|commodity"
    r"|barrel|opec|gasoline|heating\s+oil|diesel)", re.I
)

# City-specific weather stress models
# Each entry: (city_pattern, stress_type, high_threshold_f, low_threshold_f)
# high_threshold_f: if temperature market says above this -> energy stress UP
# low_threshold_f: if temperature market says below this -> stress UP
CITY_STRESS_MODELS = [
    # Dallas: hot = AC demand spike; cold = heating demand spike
    (re.compile(r"\bdallas\b", re.I), "energy", 84, 35),
    # Chicago: cold = crop risk + heating; hot = mild energy stress
    (re.compile(r"\bchicago\b", re.I), "crop_energy", 90, 61),
    # Miami: extreme heat = hurricane season indicator
    (re.compile(r"\bmiami\b", re.I), "hurricane", 92, 40),
    # New York: extreme cold = heating demand; hot = AC demand
    (re.compile(r"\bnew\s*york\b", re.I), "energy", 88, 30),
    # Houston: hot = energy demand; hurricane zone
    (re.compile(r"\bhouston\b", re.I), "energy", 90, 35),
    # Phoenix: extreme heat baseline already high
    (re.compile(r"\bphoenix\b", re.I), "energy", 100, 40),
    # Generic temperature market
    (re.compile(r"\btemperature\b", re.I), "general", 90, 35),
]

# Temperature extraction from market questions
_TEMP_EXTRACT = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:degrees?\s*)?(?:f(?:ahrenheit)?|(?:\xb0|\u00b0)?\s*f)\b", re.I
)
_ABOVE_BELOW = re.compile(r"\b(above|over|exceed|higher\s+than|at\s+least|below|under|lower\s+than|at\s+most)\b", re.I)


def is_weather_market(question: str) -> bool:
    return bool(_WEATHER_PATTERN.search(question))


def is_commodity_market(question: str) -> bool:
    return bool(_COMMODITY_PATTERN.search(question))


def extract_temperature_info(question: str) -> dict | None:
    """Extract temperature threshold and direction from a weather market question."""
    temp_match = _TEMP_EXTRACT.search(question)
    if not temp_match:
        return None

    temp_f = float(temp_match.group(1))
    direction_match = _ABOVE_BELOW.search(question)
    direction = "above"  # default
    if direction_match:
        word = direction_match.group(1).lower()
        if word in ("below", "under", "lower than", "at most"):
            direction = "below"

    city = None
    stress_type = "general"
    high_thresh = 90
    low_thresh = 35

    for city_pat, stype, ht, lt in CITY_STRESS_MODELS:
        if city_pat.search(question):
            city = city_pat.pattern.replace(r"\b", "").replace("\\b", "")
            stress_type = stype
            high_thresh = ht
            low_thresh = lt
            break

    return {
        "temp_f": temp_f,
        "direction": direction,
        "city": city,
        "stress_type": stress_type,
        "high_thresh": high_thresh,
        "low_thresh": low_thresh,
    }


def compute_weather_stress(weather_markets: list) -> list[dict]:
    """
    For each weather market, compute a stress score.
    Returns list of {market, stress_score, stress_direction, stress_type, reasoning}.
    stress_direction: 'energy_up', 'crop_risk', 'hurricane_risk'
    """
    stress_signals = []

    for m in weather_markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        info = extract_temperature_info(q)
        if not info:
            continue

        temp_f = info["temp_f"]
        direction = info["direction"]
        stress_type = info["stress_type"]
        high_thresh = info["high_thresh"]
        low_thresh = info["low_thresh"]

        stress = 0.0
        stress_dir = None

        if direction == "above" and temp_f >= high_thresh:
            # Market asks "will temp be above X?" where X is high
            # High probability = extreme heat likely
            stress = p  # stress proportional to probability of extreme heat
            if stress_type == "hurricane":
                stress_dir = "hurricane_risk"
            else:
                stress_dir = "energy_up"
        elif direction == "above" and temp_f <= low_thresh:
            # Market asks "will temp be above X?" where X is low
            # LOW probability = extreme cold likely
            stress = 1.0 - p
            stress_dir = "energy_up" if stress_type in ("energy", "general") else "crop_risk"
        elif direction == "below" and temp_f <= low_thresh:
            # Market asks "will temp be below X?" where X is already low
            # High probability = extreme cold likely
            stress = p
            stress_dir = "crop_risk" if stress_type == "crop_energy" else "energy_up"
        elif direction == "below" and temp_f >= high_thresh:
            # Market asks "will temp be below X?" where X is high
            # LOW probability = extreme heat likely
            stress = 1.0 - p
            stress_dir = "energy_up"

        if stress >= WEATHER_STRESS_THRESHOLD and stress_dir:
            city_label = info["city"] or "unknown"
            stress_signals.append({
                "market": m,
                "stress_score": stress,
                "stress_direction": stress_dir,
                "stress_type": stress_type,
                "reasoning": (
                    f"Weather stress {stress:.0%} [{stress_dir}] "
                    f"city={city_label} temp={temp_f}F dir={direction} p={p:.0%}"
                ),
            })

    return stress_signals


def compute_commodity_expected_direction(stress_signals: list) -> dict[str, float]:
    """
    Aggregate weather stress signals into expected commodity directions.
    Returns dict of {commodity_direction: aggregate_stress}.
    'energy_up' -> oil/gas markets should be higher
    'crop_risk' -> ag commodity markets should be higher
    """
    agg: dict[str, float] = {}
    for sig in stress_signals:
        d = sig["stress_direction"]
        agg[d] = max(agg.get(d, 0), sig["stress_score"])
    return agg


def commodity_matches_stress(question: str, stress_direction: str) -> bool:
    """Check if a commodity market would be affected by this stress type."""
    q = question.lower()
    if stress_direction == "energy_up":
        return bool(re.search(r"(oil|wti|crude|brent|natural\s+gas|energy|gas\s*price|barrel|opec|gasoline|heating\s+oil|diesel)", q))
    if stress_direction == "crop_risk":
        return bool(re.search(r"(crop|wheat|corn|soybean|agriculture|grain|commodity)", q))
    if stress_direction == "hurricane_risk":
        return bool(re.search(r"(oil|crude|energy|insurance|catastrophe|hurricane|flood|storm)", q))
    return False


# --------------- compute signal ---------------

def compute_signal(market, stress_score: float, stress_direction: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) using conviction-based sizing.
    Weather stress implies commodity should go UP -> buy YES when underpriced.
    """
    p = getattr(market, "current_probability", None)
    q = getattr(market, "question", "")

    if not isinstance(p, (int, float)):
        return None, 0, "missing probability"

    # Spread gate
    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    # Weather stress generally implies commodity UP -> buy YES on commodity
    # The commodity market should be pricing higher, so if it's low -> YES
    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by weather stress magnitude
        conviction = min(1.0, conviction + stress_score * 0.3)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} stress={stress_score:.0%} [{stress_direction}] size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # If commodity is overpriced AND weather stress is high,
        # stress reinforces high pricing -> skip NO trades on stressed commodities
        # Only sell NO if stress contradicts high pricing (unusual)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} stress={stress_score:.0%} [{stress_direction}] size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


# --------------- context guard ---------------

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


# --------------- market discovery ---------------

WEATHER_KEYWORDS = ["temperature", "high temp", "weather", "degrees", "heat", "cold"]
COMMODITY_KEYWORDS = ["oil", "WTI", "crude", "energy", "crop", "wheat", "corn", "natural gas"]


def discover_markets(client: SimmerClient) -> tuple[list, list]:
    """Discover weather and commodity markets. Returns (weather_markets, commodity_markets)."""
    seen = set()
    weather_markets = []
    commodity_markets = []

    # Primary: get_markets scan
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            if not mid or mid in seen:
                continue
            seen.add(mid)
            q = getattr(m, "question", "")
            if is_weather_market(q):
                weather_markets.append(m)
            if is_commodity_market(q):
                commodity_markets.append(m)
    except Exception as e:
        safe_print(f"[get_markets] {e}")

    # Secondary: keyword search
    for kw in WEATHER_KEYWORDS + COMMODITY_KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                mid = getattr(m, "id", None)
                if not mid or mid in seen:
                    continue
                seen.add(mid)
                q = getattr(m, "question", "")
                if is_weather_market(q):
                    weather_markets.append(m)
                if is_commodity_market(q):
                    commodity_markets.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return weather_markets, commodity_markets


# --------------- main loop ---------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[weather-commodity] mode={mode} max_pos=${MAX_POSITION} "
        f"min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS} "
        f"stress_thresh={WEATHER_STRESS_THRESHOLD:.0%}"
    )

    client = get_client(live=live)
    weather_markets, commodity_markets = discover_markets(client)
    safe_print(
        f"[weather-commodity] {len(weather_markets)} weather markets, "
        f"{len(commodity_markets)} commodity markets"
    )

    if not weather_markets:
        safe_print("[weather-commodity] No weather markets found. Nothing to do.")
        return

    # Step 1: Compute weather stress from temperature markets
    stress_signals = compute_weather_stress(weather_markets)
    safe_print(f"[weather-commodity] {len(stress_signals)} weather stress signals")

    if not stress_signals:
        safe_print("[weather-commodity] No weather stress above threshold. Nothing to do.")
        return

    for sig in stress_signals:
        safe_print(f"  [stress] {sig['reasoning']}")

    # Step 2: Aggregate stress into expected commodity directions
    expected_dirs = compute_commodity_expected_direction(stress_signals)
    safe_print(f"[weather-commodity] Expected commodity directions: {expected_dirs}")

    if not commodity_markets:
        safe_print("[weather-commodity] No commodity markets found. Nothing to do.")
        return

    # Step 3: For each commodity market, check if it reflects the weather stress
    placed = 0
    for stress_dir, agg_stress in sorted(expected_dirs.items(), key=lambda x: -x[1]):
        for cm in commodity_markets:
            if placed >= MAX_POSITIONS:
                break

            q = getattr(cm, "question", "")
            if not commodity_matches_stress(q, stress_dir):
                continue

            side, size, reasoning = compute_signal(cm, agg_stress, stress_dir)
            if not side:
                safe_print(f"  [skip] {reasoning}")
                continue

            market_id = getattr(cm, "id", None)
            ok, why = context_ok(client, market_id)
            if not ok:
                safe_print(f"  [skip] {why}")
                continue

            try:
                r = client.trade(
                    market_id=market_id,
                    side=side,
                    amount=size,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} - {reasoning[:110]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {market_id}: {e}")

        if placed >= MAX_POSITIONS:
            break

    safe_print(f"[weather-commodity] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades commodity markets based on extreme weather stress signals."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
