#!/usr/bin/env python3
"""
🌤️ Weather Market Scanner
===========================
Exploits the NOAA/Open-Meteo vs Polymarket pricing gap.

Strategy:
- Fetch Open-Meteo forecasts (free, accurate to ~1°C within 48h)
- Compare to Polymarket temperature bucket pricing
- Buy mispriced buckets where forecast confidence >> market price
- Edge persists because <50 traders compete in these markets

Cities tracked:
  Seoul, Tokyo, Shanghai, Ankara, NYC, Miami, Dallas, Atlanta, Hong Kong, Tel Aviv

Usage:
  python3 weather_scanner.py           # Scan + show plays
  python3 weather_scanner.py --buy     # Scan + execute best plays
  python3 weather_scanner.py --dry-run # Show what would be bought
"""

import os, sys, json, math, time
import urllib.request, urllib.parse
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ── City config ────────────────────────────────────────────────────────────────
CITIES = {
    # ⚠️ AIRPORT STATION COORDINATES — Polymarket resolves on airport stations, NOT city centers
    # Using exact airport lat/lon + ICAO station codes for METAR
    "Seoul":         {"lat": 37.4691,  "lon": 126.4505, "tz": "Asia/Seoul",                         "unit": "C", "station": "RKSI", "region": "asia"},
    "Tokyo":         {"lat": 35.7647,  "lon": 140.3864, "tz": "Asia/Tokyo",                         "unit": "C", "station": "RJTT", "region": "asia"},
    "Shanghai":      {"lat": 31.1443,  "lon": 121.8083, "tz": "Asia/Shanghai",                      "unit": "C", "station": "ZSPD", "region": "asia"},
    "Ankara":        {"lat": 40.1281,  "lon": 32.9951,  "tz": "Europe/Istanbul",                    "unit": "C", "station": "LTAC", "region": "eu"},
    "Hong Kong":     {"lat": 22.3080,  "lon": 113.9185, "tz": "Asia/Hong_Kong",                     "unit": "C", "station": "VHHH", "region": "asia"},
    "Tel Aviv":      {"lat": 32.0114,  "lon": 34.8867,  "tz": "Asia/Jerusalem",                     "unit": "C", "station": "LLBG", "region": "asia"},
    "New York City": {"lat": 40.7772,  "lon": -73.8726, "tz": "America/New_York",                   "unit": "F", "station": "KLGA", "region": "us"},  # LaGuardia, NOT Manhattan
    "Miami":         {"lat": 25.7959,  "lon": -80.2870, "tz": "America/New_York",                   "unit": "F", "station": "KMIA", "region": "us"},  # Miami Intl
    "Dallas":        {"lat": 32.8471,  "lon": -96.8518, "tz": "America/Chicago",                    "unit": "F", "station": "KDAL", "region": "us"},  # Love Field, NOT DFW
    "Atlanta":       {"lat": 33.6407,  "lon": -84.4277, "tz": "America/New_York",                   "unit": "F", "station": "KATL", "region": "us"},  # Hartsfield
    "London":        {"lat": 51.5048,  "lon": 0.0495,   "tz": "Europe/London",                      "unit": "C", "station": "EGLC", "region": "eu"},   # London City
    "Buenos Aires":  {"lat": -34.8222, "lon": -58.5358, "tz": "America/Argentina/Buenos_Aires",     "unit": "C", "station": "SAEZ", "region": "sa"},
    "Sao Paulo":     {"lat": -23.4356, "lon": -46.4731, "tz": "America/Sao_Paulo",                  "unit": "C", "station": "SBGR", "region": "sa"},
    "Seattle":       {"lat": 47.4502,  "lon": -122.3088,"tz": "America/Los_Angeles",                "unit": "F", "station": "KSEA", "region": "us"},  # Sea-Tac
    "Toronto":       {"lat": 43.6772,  "lon": -79.6306, "tz": "America/Toronto",                    "unit": "C", "station": "CYYZ", "region": "ca"},
    "Wellington":    {"lat": -41.3272, "lon": 174.8052, "tz": "Pacific/Auckland",                   "unit": "C", "station": "NZWN", "region": "oc"},
    "Lucknow":       {"lat": 26.7606,  "lon": 80.8893,  "tz": "Asia/Kolkata",                       "unit": "C", "station": "VILK", "region": "asia"},
}

GAMMA_API = "https://gamma-api.polymarket.com"
METEO_API = "https://api.open-meteo.com/v1/forecast"
VISUAL_CROSSING_API = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# ── Thresholds ─────────────────────────────────────────────────────────────────
MAX_ENTRY_PRICE  = 0.45   # Only buy if market price ≤ 45¢
MIN_ENTRY_PRICE  = 0.05   # Skip near-zero lottery tickets (< 5¢)
MIN_EDGE         = 0.10   # Only buy if EV edge ≥ 10%
MIN_TRUE_PROB    = 0.45   # True probability must be ≥ 45%
MIN_DAYS_OUT     = 0      # Allow same-day if METAR confirms
MAX_DAYS_OUT     = 3      # Max 72h — beyond that forecast degrades
MAX_BET_SIZE     = 25.0   # Hard cap per trade (updated rule)
MIN_BET_SIZE     = 5.0
RESERVE_BUFFER   = 15.0   # Always keep $15 in wallet
MAX_SPREAD       = 0.03   # Skip if ask-bid spread > 3¢ (slippage filter)
KELLY_FRACTION   = 0.25   # Fractional Kelly sizing
METAR_API        = "https://aviationweather.gov/api/data/metar"

def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "ClawdipusRex/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def c_to_f(c):
    return c * 9/5 + 32

def get_forecast(city_cfg, target_date_str):
    """ECMWF forecast via Open-Meteo (airport station coords). Primary source."""
    params = urllib.parse.urlencode({
        "latitude":      city_cfg["lat"],
        "longitude":     city_cfg["lon"],
        "daily":         "temperature_2m_max",
        "timezone":      city_cfg["tz"],
        "forecast_days": 7,
        "models":        "ecmwf_ifs025",
        "bias_correction": "true",
    })
    try:
        data = fetch(f"{METEO_API}?{params}")
        for d, t in zip(data["daily"]["time"], data["daily"]["temperature_2m_max"]):
            if d == target_date_str and t is not None:
                if city_cfg["unit"] == "F":
                    return round(c_to_f(t), 1), "F"
                return round(t, 1), "C"
    except Exception:
        pass
    return None, city_cfg["unit"]

def get_hrrr_forecast(city_cfg, target_date_str):
    """HRRR/GFS seamless forecast — US cities only, best for D+0/D+1."""
    if city_cfg.get("region") != "us":
        return None
    params = urllib.parse.urlencode({
        "latitude":      city_cfg["lat"],
        "longitude":     city_cfg["lon"],
        "daily":         "temperature_2m_max",
        "timezone":      city_cfg["tz"],
        "forecast_days": 3,
        "models":        "gfs_seamless",
    })
    try:
        data = fetch(f"{METEO_API}?{params}")
        for d, t in zip(data["daily"]["time"], data["daily"]["temperature_2m_max"]):
            if d == target_date_str and t is not None:
                return round(c_to_f(t), 1) if city_cfg["unit"] == "F" else round(t, 1)
    except Exception:
        pass
    return None

def get_visual_crossing_forecast(city_cfg, target_date_str):
    """Visual Crossing API — high accuracy, global coverage, paid tier."""
    try:
        creds_path = Path.home() / ".config/visualcrossing/credentials.json"
        if not creds_path.exists():
            return None
        api_key = json.loads(creds_path.read_text()).get("api_key")
        if not api_key:
            return None
        lat, lon = city_cfg["lat"], city_cfg["lon"]
        params = urllib.parse.urlencode({
            "unitGroup": "metric",
            "key": api_key,
            "include": "days",
            "elements": "tempmax",
        })
        data = fetch(f"{VISUAL_CROSSING_API}/{lat},{lon}/{target_date_str}?{params}", timeout=10)
        days = data.get("days", [])
        if days:
            tempmax_c = days[0].get("tempmax")
            if tempmax_c is not None:
                if city_cfg["unit"] == "F":
                    return round(float(tempmax_c) * 9/5 + 32, 1)
                return round(float(tempmax_c), 1)
    except Exception:
        pass
    return None

def get_metar_temp(city_cfg):
    """Real-time METAR observation from airport station. D+0 only."""
    station = city_cfg.get("station")
    if not station:
        return None
    try:
        data = fetch(f"{METAR_API}?ids={station}&format=json", timeout=8)
        if data and isinstance(data, list):
            temp_c = data[0].get("temp")
            if temp_c is not None:
                if city_cfg["unit"] == "F":
                    return round(float(temp_c) * 9/5 + 32)
                return round(float(temp_c), 1)
    except Exception:
        pass
    return None

def get_best_forecast(city_cfg, target_date_str):
    """
    Returns (temp, source, sigma) using best available data:
    - METAR for today (real observation, tightest sigma)
    - HRRR for US D+0/D+1 (best regional model)
    - ECMWF for everything else
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    unit = city_cfg["unit"]

    # METAR — only for today
    if target_date_str == today:
        metar = get_metar_temp(city_cfg)
        if metar is not None:
            return metar, "METAR", 1.0  # tightest sigma — real observation

    # HRRR — US only, D+0 and D+1
    hrrr = get_hrrr_forecast(city_cfg, target_date_str)
    if hrrr is not None:
        return hrrr, "HRRR", 1.5

    # Visual Crossing — paid API, high accuracy global coverage
    vc = get_visual_crossing_forecast(city_cfg, target_date_str)

    # ECMWF — fallback for all cities
    ecmwf, _ = get_forecast(city_cfg, target_date_str)

    # Consensus: if both agree within 1°, tighter sigma + use average
    if vc is not None and ecmwf is not None:
        diff = abs(vc - ecmwf)
        avg = round((vc + ecmwf) / 2, 1)
        if diff <= 1.0:
            return avg, "VC+ECMWF", 0.8  # tight consensus — best non-METAR signal
        else:
            # Disagreement — use VC (paid, higher accuracy) but widen sigma
            return vc, "VisualCrossing", 2.0

    if vc is not None:
        return vc, "VisualCrossing", 1.5

    if ecmwf is not None:
        sigma = 2.0 if unit == "F" else 1.2
        return ecmwf, "ECMWF", sigma

    return None, None, 2.0

def get_weather_events():
    """Fetch open weather events from Polymarket."""
    data = fetch(f"{GAMMA_API}/events?closed=false&limit=200&order=volume24hr&ascending=false")
    weather = []
    for e in data:
        title = e.get("title", "")
        if "highest temperature" in title.lower() or "lowest temperature" in title.lower():
            weather.append(e)
    return weather

def parse_bucket(question, unit):
    """
    Extract temperature value from market question.
    Returns (temp_value, is_range, range_low, range_high, is_or_below, is_or_above)
    """
    import re
    q = question.lower()

    # "X°C or below" / "X°F or below"
    m = re.search(r'be\s+(-?\d+)[°℃℉]?\s*(?:°[cf])?\s*or\s+below', q)
    if m:
        return {"type": "below", "val": int(m.group(1))}

    # "X°C or higher"
    m = re.search(r'be\s+(-?\d+)[°℃℉]?\s*(?:°[cf])?\s*or\s+higher', q)
    if m:
        return {"type": "above", "val": int(m.group(1))}

    # "between X-Y°F" or "between X and Y"
    m = re.search(r'between\s+(-?\d+)[-–and\s]+(-?\d+)', q)
    if m:
        return {"type": "range", "low": int(m.group(1)), "high": int(m.group(2))}

    # "be X°C" (exact)
    m = re.search(r'be\s+(-?\d+)\s*°?[cCfF]?\s+on\s', q)
    if m:
        return {"type": "exact", "val": int(m.group(1))}

    return None

def prob_from_forecast(bucket, forecast_temp, sigma=1.2):
    """
    Estimate true probability from Open-Meteo forecast.
    Uses normal distribution around forecast with sigma=1.2°C (~2°F).
    """
    from math import erf, sqrt, exp, pi

    def cdf(x):
        return 0.5 * (1 + erf((x - forecast_temp) / (sigma * sqrt(2))))

    def pdf(x):
        return exp(-((x - forecast_temp) ** 2) / (2 * sigma ** 2)) / (sigma * sqrt(2 * pi))

    if bucket is None:
        return 0.0

    t = bucket.get("type")
    if t == "below":
        return cdf(bucket["val"] + 0.5)
    elif t == "above":
        return 1 - cdf(bucket["val"] - 0.5)
    elif t == "range":
        return cdf(bucket["high"] + 0.5) - cdf(bucket["low"] - 0.5)
    elif t == "exact":
        return cdf(bucket["val"] + 0.5) - cdf(bucket["val"] - 0.5)
    return 0.0

def kelly_size(prob, price, bankroll, fraction=0.25):
    """25% fractional Kelly sizing."""
    if price <= 0 or prob <= price:
        return 0
    b = (1 - price) / price  # odds
    q = 1 - prob
    k = (prob * b - q) / b
    k = max(0, k) * fraction
    return min(MAX_BET_SIZE, max(MIN_BET_SIZE, bankroll * k))

def scan_city(city_name, city_cfg, events, target_date=None):
    """Find mispriced weather markets for a city."""
    plays = []
    city_lower = city_name.lower()
    # Aliases for matching event titles
    city_aliases = [city_lower]
    if city_lower == "new york city":
        city_aliases.append("new york")

    # Find matching events
    for e in events:
        title = e.get("title", "").lower()
        if not any(alias in title for alias in city_aliases):
            continue

        # Figure out date from title
        import re
        date_m = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d+)', title)
        if not date_m:
            continue
        months = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
                  "july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
        month = months[date_m.group(1)]
        day = int(date_m.group(2))
        now = datetime.now(timezone.utc)
        year = now.year
        date_str = f"{year}-{month:02d}-{day:02d}"

        # Skip past dates
        market_date = datetime(year, month, day, tzinfo=timezone.utc)
        if market_date.date() < now.date():
            continue

        # Get best forecast (METAR > HRRR > ECMWF, airport coords)
        import datetime as _dt
        days_out = (market_date.date() - _dt.datetime.now(_dt.timezone.utc).date()).days
        if days_out > MAX_DAYS_OUT:
            continue  # Beyond forecast reliability window

        forecast_temp, forecast_src, sigma = get_best_forecast(city_cfg, date_str)
        if forecast_temp is None:
            continue
        unit = city_cfg["unit"]

        # Analyze each sub-market
        for m in e.get("markets", []):
            if m.get("closed"):
                continue
            prices_raw = m.get("outcomePrices", "[]")
            prices = json.loads(prices_raw) if isinstance(prices_raw, str) else prices_raw
            if not prices or len(prices) < 2:
                continue
            yes_price = float(prices[0])
            no_price  = float(prices[1])

            if yes_price <= 0.001 or yes_price >= 0.98:
                continue

            # Slippage filter — skip wide spreads
            spread = abs(yes_price - no_price - 1.0) if len(prices) >= 2 else 0
            # Approximate spread from YES+NO sum deviation
            spread = max(0, 1.0 - yes_price - no_price)
            if spread > MAX_SPREAD:
                continue

            bucket = parse_bucket(m.get("question",""), unit)
            if bucket is None:
                continue

            true_prob = prob_from_forecast(bucket, forecast_temp)
            # EV-based edge (not just prob - price)
            if yes_price > 0:
                ev = true_prob * (1.0 / yes_price - 1.0) - (1.0 - true_prob)
            else:
                ev = 0
            if true_prob < MIN_TRUE_PROB:
                continue
            if yes_price < MIN_ENTRY_PRICE or yes_price > MAX_ENTRY_PRICE:
                continue
            if ev >= MIN_EDGE:
                plays.append({
                    "city": city_name,
                    "date": date_str,
                    "question": m.get("question",""),
                    "slug": m.get("slug",""),
                    "market_price": yes_price,
                    "true_prob": true_prob,
                    "edge": ev,
                    "forecast": forecast_temp,
                    "forecast_src": forecast_src,
                    "sigma": sigma,
                    "days_out": days_out,
                    "spread": round(spread, 4),
                    "unit": unit,
                    "bucket": bucket,
                    "volume24hr": float(e.get("volume24hr", 0)),
                })

    return plays

def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def get_balance():
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
    pk = os.environ.get("PRIVATE_KEY")
    wallet = os.environ.get("WALLET_ADDRESS")
    client = ClobClient("https://clob.polymarket.com", key=pk, chain_id=137,
                        signature_type=1, funder=wallet)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    params = BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    bal = client.get_balance_allowance(params=params)
    return int(bal.get("balance", "0")) / 1e6

def buy_market(slug, size):
    import subprocess
    cmd = ["python3", str(Path(__file__).parent / "trader.py"),
           "--buy", "--slug", slug, "--yes", "--size", str(round(size, 2)), "--confirm"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    out = (r.stdout + r.stderr).strip()
    ok = any(x in out.lower() for x in ["matched", "delayed", "success", "order placed"])
    return ok, out

def main():
    parser = argparse.ArgumentParser(description="Weather Market Scanner")
    parser.add_argument("--buy",     action="store_true", help="Execute trades")
    parser.add_argument("--dry-run", action="store_true", help="Show plays without buying")
    parser.add_argument("--min-edge", type=float, default=MIN_EDGE, help="Min edge threshold")
    parser.add_argument("--max-price", type=float, default=MAX_ENTRY_PRICE, help="Max entry price")
    args = parser.parse_args()

    load_env()

    print("=" * 65)
    print("🌤️  WEATHER MARKET SCANNER")
    print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)
    print(f"\n📡 Fetching Open-Meteo forecasts + Polymarket events...")

    events = get_weather_events()
    print(f"   Found {len(events)} open weather events\n")

    all_plays = []
    for city_name, city_cfg in CITIES.items():
        try:
            plays = scan_city(city_name, city_cfg, events)
            all_plays.extend(plays)
            time.sleep(0.3)  # Rate limit Open-Meteo
        except Exception as ex:
            print(f"   ⚠️  {city_name}: {ex}")

    # Sort by edge
    all_plays.sort(key=lambda x: x["edge"], reverse=True)

    if not all_plays:
        print("🔍 No mispriced weather markets found right now.")
        print("   (Market may have already priced in the forecast)")
        return

    print(f"🎯 Found {len(all_plays)} mispriced weather plays:\n")
    print(f"  {'City':<12} {'Date':<10} {'Src':<6} {'D+':<3} {'Forecast':>9} {'Market':>7} {'True%':>7} {'EV':>6} {'Sprd':>5}  Market")
    print(f"  {'-'*12} {'-'*10} {'-'*6} {'-'*3} {'-'*9} {'-'*7} {'-'*7} {'-'*6} {'-'*5}  {'------'}")

    for p in all_plays:
        print(f"  {p['city']:<12} {p['date']:<10} {p.get('forecast_src','?'):<6} D+{p.get('days_out',0):<2} "
              f"{p['forecast']:>7.1f}°{p['unit']} "
              f"{p['market_price']:>6.1%} {p['true_prob']:>6.1%} {p['edge']:>+5.1%} {p.get('spread',0):>4.3f}  "
              f"{p['question'][:50]}")

    if args.buy or args.dry_run:
        balance = get_balance() if args.buy else 999
        deployable = balance - RESERVE_BUFFER
        per_trade = min(MAX_BET_SIZE, max(MIN_BET_SIZE, deployable / max(len(all_plays), 1)))

        print(f"\n{'💸 DRY RUN' if args.dry_run else '🚀 EXECUTING'} — ${deployable:.2f} available, ${per_trade:.2f}/trade\n")

        for p in all_plays[:5]:  # Max 5 weather plays
            size = kelly_size(p["true_prob"], p["market_price"], deployable)
            print(f"  ${size:.2f} → {p['city']} {p['date']} | {p['question'][:55]}")
            if args.buy:
                ok, out = buy_market(p["slug"], size)
                key = next((l.strip() for l in out.split("\n")
                            if any(x in l.lower() for x in ["matched","shares","error","failed"])), "")
                print(f"         {'✅' if ok else '❌'} {key[:60]}")
                time.sleep(2)

    print()

if __name__ == "__main__":
    main()
