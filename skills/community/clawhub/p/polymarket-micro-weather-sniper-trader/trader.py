"""
polymarket-micro-weather-sniper-trader
Trades Polymarket weather markets using NOAA forecasts as an information edge.

Core edge: NOAA weather forecasts are ~85% accurate for 1-2 day high temperature
predictions. Polymarket weather bins (e.g. "Will the high in Chicago be 40-41°F?")
are often mispriced at p=1-5% even when NOAA predicts that exact temperature range.
This skill finds the bin that matches the NOAA forecast and buys YES at a discount.

Also sells NO on near-certainty bins (p>80%) that NOAA disagrees with.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Real trades only with explicit --live flag.
"""
import os
import re
import json
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-micro-weather-sniper-trader"
SKILL_SLUG = "polymarket-micro-weather-sniper-trader"

# MICRO risk parameters
MAX_POSITION = float(os.environ.get("SIMMER_MAX_POSITION", "5"))
MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", "2"))
MAX_SPREAD = float(os.environ.get("SIMMER_MAX_SPREAD", "0.15"))
MIN_DAYS = int(os.environ.get("SIMMER_MIN_DAYS", "0"))
MAX_POSITIONS = int(os.environ.get("SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.40"))
NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", "0.80"))
MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", "2"))

# NOAA accuracy — our prior for forecast correctness
NOAA_ACCURACY = 0.85

# Supported cities with NOAA coordinates
CITIES = {
    "new york city": {"lat": 40.7769, "lon": -73.8740, "unit": "F"},
    "chicago": {"lat": 41.9742, "lon": -87.9073, "unit": "F"},
    "miami": {"lat": 25.7959, "lon": -80.2870, "unit": "F"},
    "los angeles": {"lat": 34.0522, "lon": -118.2437, "unit": "F"},
    "atlanta": {"lat": 33.6407, "lon": -84.4277, "unit": "F"},
    "seattle": {"lat": 47.4502, "lon": -122.3088, "unit": "F"},
    "austin": {"lat": 30.1942, "lon": -97.6697, "unit": "F"},
    "amsterdam": {"lat": 52.3676, "lon": 4.9041, "unit": "C"},
    "london": {"lat": 51.4700, "lon": -0.4543, "unit": "C"},
    "shanghai": {"lat": 31.1443, "lon": 121.8083, "unit": "C"},
    "busan": {"lat": 35.1796, "lon": 128.9382, "unit": "C"},
    "warsaw": {"lat": 52.2297, "lon": 21.0122, "unit": "C"},
    "helsinki": {"lat": 60.3172, "lon": 24.9633, "unit": "C"},
    "mexico city": {"lat": 19.4326, "lon": -99.1332, "unit": "C"},
    "hong kong": {"lat": 22.3193, "lon": 114.1694, "unit": "C"},
    "kuala lumpur": {"lat": 3.1390, "lon": 101.6869, "unit": "C"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "unit": "C"},
    "singapore": {"lat": 1.3521, "lon": 103.8198, "unit": "C"},
    "buenos aires": {"lat": -34.6037, "lon": -58.3816, "unit": "C"},
    "cape town": {"lat": -33.9249, "lon": 18.4241, "unit": "C"},
    "lagos": {"lat": 6.5244, "lon": 3.3792, "unit": "C"},
    "milan": {"lat": 45.4642, "lon": 9.1900, "unit": "C"},
    "shenzhen": {"lat": 22.5431, "lon": 114.0579, "unit": "C"},
}

_client: SimmerClient | None = None


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_TRADE, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD
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
            pass
        MAX_POSITION = float(os.environ.get("SIMMER_MAX_POSITION", str(MAX_POSITION)))
        MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", str(MIN_TRADE)))
        MAX_SPREAD = float(os.environ.get("SIMMER_MAX_SPREAD", str(MAX_SPREAD)))
        MIN_DAYS = int(os.environ.get("SIMMER_MIN_DAYS", str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get("SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", str(NO_THRESHOLD)))
    return _client


# ---------------------------------------------------------------------------
# NOAA Weather API
# ---------------------------------------------------------------------------

def get_forecast(city: str) -> dict[str, int]:
    """Fetch weather forecast for a city. Tries NOAA, Open-Meteo, then wttr.in.
    Returns {date_str: high_temp_int}."""
    info = CITIES.get(city.lower())
    if not info:
        return {}

    # Try NOAA first (US only, most accurate)
    forecasts = _try_noaa(info, city)
    if forecasts:
        return forecasts

    # Try Open-Meteo (global, free, no API key)
    forecasts = _try_open_meteo(info, city)
    if forecasts:
        return forecasts

    # Final fallback: wttr.in (also free, different provider)
    return _try_wttr(city, info)


def _try_noaa(info: dict, city: str) -> dict[str, int]:
    headers = {"User-Agent": "kladde-weather-agent/1.0 (diagnostikon)", "Accept": "application/json"}
    try:
        req = Request(f"https://api.weather.gov/points/{info['lat']},{info['lon']}", headers=headers)
        with urlopen(req, timeout=10) as r:
            points = json.loads(r.read())
        forecast_url = points["properties"]["forecast"]
        req2 = Request(forecast_url, headers=headers)
        with urlopen(req2, timeout=10) as r:
            data = json.loads(r.read())
        forecasts = {}
        for period in data["properties"]["periods"]:
            if period.get("isDaytime", True):
                date_str = period["startTime"][:10]
                forecasts[date_str] = period["temperature"]
        return forecasts
    except Exception:
        return {}


def _try_open_meteo(info: dict, city: str) -> dict[str, int]:
    try:
        unit_param = "fahrenheit" if info["unit"] == "F" else "celsius"
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={info['lat']}&longitude={info['lon']}"
               f"&daily=temperature_2m_max&temperature_unit={unit_param}"
               f"&forecast_days=7")
        with urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        dates = data["daily"]["time"]
        temps = data["daily"]["temperature_2m_max"]
        return {d: round(t) for d, t in zip(dates, temps) if t is not None}
    except Exception as e:
        safe_print(f"  [open-meteo] {city}: {e}")
        return {}


def _try_wttr(city: str, info: dict) -> dict[str, int]:
    """wttr.in fallback. Returns Celsius by default; converts if city is F."""
    try:
        city_url = city.replace(" ", "+")
        url = f"https://wttr.in/{city_url}?format=j1"
        req = Request(url, headers={"User-Agent": "kladde-weather/1.0"})
        with urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        forecasts = {}
        for day in data.get("weather", [])[:7]:
            date = day["date"]
            temp_c = int(day["maxtempC"])
            if info["unit"] == "F":
                temp = round(temp_c * 9 / 5 + 32)
            else:
                temp = temp_c
            forecasts[date] = temp
        return forecasts
    except Exception as e:
        safe_print(f"  [wttr] {city}: {e}")
        return {}


# ---------------------------------------------------------------------------
# Market parsing
# ---------------------------------------------------------------------------

# "Will the highest temperature in Chicago be between 40-41°F on April 8?"
# "Will the highest temperature in Miami be 92°F or higher on April 6?"
_TEMP_BIN_RE = re.compile(
    r"highest temperature in (.+?) be (?:between )?(\d+)(?:[°]?[FC])?(?:\s*[-–]\s*(\d+))?",
    re.I,
)
_DATE_RE = re.compile(r"on (\w+ \d+)", re.I)
_OR_HIGHER_RE = re.compile(r"(\d+)[°]?[FC]? or higher", re.I)
_OR_BELOW_RE = re.compile(r"(\d+)[°]?[FC]? or (?:below|lower)", re.I)


def parse_weather_market(question: str) -> dict | None:
    """Parse a weather market question. Returns {city, low, high, date_str, type}."""
    m = _TEMP_BIN_RE.search(question)
    if not m:
        return None

    city = m.group(1).strip().lower()
    low_temp = int(m.group(2))
    high_temp = int(m.group(3)) if m.group(3) else low_temp

    # Check for "or higher" / "or below"
    market_type = "bin"
    oh = _OR_HIGHER_RE.search(question)
    if oh:
        market_type = "or_higher"
        low_temp = int(oh.group(1))
        high_temp = 999

    ob = _OR_BELOW_RE.search(question)
    if ob:
        market_type = "or_below"
        high_temp = int(ob.group(1))
        low_temp = -999

    # Parse date
    dm = _DATE_RE.search(question)
    date_str = dm.group(1) if dm else None

    return {"city": city, "low": low_temp, "high": high_temp, "date_str": date_str, "type": market_type}


def forecast_matches_bin(forecast_temp: int, parsed: dict) -> bool:
    """Check if NOAA forecast temperature falls within this market's bin."""
    return parsed["low"] <= forecast_temp <= parsed["high"]


def forecast_date_key(parsed: dict) -> str | None:
    """Convert parsed date like 'April 8' to ISO date string."""
    if not parsed.get("date_str"):
        return None
    try:
        year = datetime.now().year
        dt = datetime.strptime(f"{parsed['date_str']} {year}", "%B %d %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Core trading logic
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[weather-sniper] mode={mode} max_pos=${MAX_POSITION} "
               f"thresholds={YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%}")

    client = get_client(live=live)

    # Step 1: Find weather markets
    safe_print("[weather-sniper] scanning for weather markets...")
    seen, markets = set(), []
    # Search by each city name + generic terms
    search_terms = ["highest temperature", "temperature"]
    for city in CITIES:
        search_terms.append(f"temperature {city}")
    for kw in search_terms:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen and "temperature" in getattr(m, "question", "").lower():
                    seen.add(m.id)
                    markets.append(m)
        except Exception as e:
            safe_print(f"  [search] {kw}: {e}")

    # Also check fast markets for weather
    try:
        for m in client.get_fast_markets():
            if m.id not in seen and "temperature" in getattr(m, "question", "").lower():
                seen.add(m.id)
                markets.append(m)
    except Exception:
        pass

    # Bulk scan — many weather markets not found via keyword search
    try:
        for m in client.get_markets(limit=200):
            if m.id not in seen and "temperature" in getattr(m, "question", "").lower():
                seen.add(m.id)
                markets.append(m)
    except Exception:
        pass

    safe_print(f"[weather-sniper] {len(markets)} weather markets found")

    # Step 2: Parse markets and group by city+date
    parsed_markets = []
    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_weather_market(q)
        if parsed:
            parsed_markets.append((m, parsed))

    safe_print(f"[weather-sniper] {len(parsed_markets)} parseable weather bins")

    # Step 3: Get NOAA forecasts for relevant cities
    cities_needed = set()
    for m, parsed in parsed_markets:
        city = parsed["city"]
        if city in CITIES:
            cities_needed.add(city)

    forecasts = {}
    for city in cities_needed:
        fc = get_forecast(city)
        if fc:
            forecasts[city] = fc
            for date_str, temp in fc.items():
                unit = CITIES[city]["unit"]
                safe_print(f"  [noaa] {city}: {date_str} high={temp}°{unit}")

    if not forecasts:
        safe_print("[weather-sniper] no NOAA forecasts available. Done.")
        return

    # Step 4: Find opportunities — NOAA forecast vs market price
    placed = 0
    for m, parsed in parsed_markets:
        if placed >= MAX_POSITIONS:
            break

        city = parsed["city"]
        if city not in forecasts:
            continue

        date_key = forecast_date_key(parsed)
        if not date_key or date_key not in forecasts[city]:
            continue

        forecast_temp = forecasts[city][date_key]
        p = m.current_probability
        q = m.question

        # Spread gate
        if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
            continue

        matches = forecast_matches_bin(forecast_temp, parsed)

        side, size, reasoning, sig = None, 0, "", None

        if matches and p <= YES_THRESHOLD:
            # NOAA says YES and market is cheap — BUY YES
            edge = NOAA_ACCURACY - p
            conviction = min(1.0, edge / NOAA_ACCURACY)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            side = "yes"
            reasoning = (f"NOAA {forecast_temp} matches bin, market p={p:.0%}, "
                        f"edge={edge:.0%} — {q[:60]}")
            sig = {"edge": round(edge, 4), "confidence": NOAA_ACCURACY,
                   "signal_source": "noaa_weather", "forecast_temp": forecast_temp,
                   "city": city}

        elif not matches and p >= NO_THRESHOLD:
            # NOAA says NO and market is overpriced — SELL NO
            edge = p - (1 - NOAA_ACCURACY)
            conviction = min(1.0, edge / NOAA_ACCURACY)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            side = "no"
            reasoning = (f"NOAA {forecast_temp} OUTSIDE bin, market p={p:.0%}, "
                        f"edge={edge:.0%} — {q[:60]}")
            sig = {"edge": round(edge, 4), "confidence": NOAA_ACCURACY,
                   "signal_source": "noaa_weather", "forecast_temp": forecast_temp,
                   "city": city}

        if not side:
            continue

        safe_print(f"  [signal] {side.upper()} ${size:.2f} — {reasoning}")

        try:
            trade_kwargs = dict(
                market_id=m.id, side=side, amount=size,
                source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            if sig:
                trade_kwargs["signal_data"] = sig
            r = client.trade(**trade_kwargs)
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size:.2f} {tag} {status}")
            if r.success:
                placed += 1
            elif "trade limit" in str(r.error).lower():
                safe_print("  [stop] Daily trade limit reached.")
                break
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[weather-sniper] done. {placed} trades placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades Polymarket weather markets using NOAA forecast data."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
