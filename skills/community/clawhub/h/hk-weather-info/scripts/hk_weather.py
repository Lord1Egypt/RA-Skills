#!/usr/bin/env python3
"""
HK Weather Info — HKO OpenData API client.
Usage: python3 hk_weather.py [--region REGION] [--lang tc|en|sc] [--action current|forecast|all]

Examples:
  python3 hk_weather.py                           # General HK weather, Traditional Chinese (default)
  python3 hk_weather.py --region "Tsuen Wan"      # Regional weather
  python3 hk_weather.py --lang en                 # English output
  python3 hk_weather.py --region "中央" --lang tc --action all
  python3 hk_weather.py --action current           # Current weather only
  python3 hk_weather.py --action forecast          # Forecast only
"""
import os, sys, json, urllib.request, urllib.error, argparse, re, csv, io
from datetime import datetime, timedelta

# HKO OpenData API — free, no key required
BASE_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"

# 1-minute temperature CSV URLs by language
CSV_URLS = {
    "en": "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv",
    "tc": "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_uc.csv",
    "sc": "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_sc.csv",
}

# Cache settings
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".hk_weather_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_TTL_SECONDS = 600  # 10 minutes

LANG_CHOICES = ["en", "tc", "sc"]

CSV_MAX_RETRIES = 2
CSV_CACHE_TTL = 60  # 1 minute cache for CSV data

# English-to-Chinese region name aliases for matching
REGION_ALIASES = {
    "tsuen wan": ["荃灣", "荃"],
    "yuen long": ["元朗"],
    "tuen mun": ["屯門"],
    "central": ["中環"],
    "wan chai": ["灣仔"],
    "kowloon": ["九龍"],
    "sha tin": ["沙田"],
    "tai po": ["大埔"],
    "tsing yi": ["青衣"],
    "kwun tong": ["觀塘"],
    "mong kok": ["旺角"],
    "aberdeen": ["香港仔"],
    "kennedy town": ["堅尼地城"],
    "sheung wan": ["上環"],
    "causeway bay": ["銅鑼灣"],
    "tin shui wai": ["天水圍"],
    "fanling": ["粉嶺"],
    "sheung shui": ["上水"],
    "lau fau shan": ["流浮山"],
    "cheung chau": ["長洲"],
    "lamma island": ["南丫島", "南丫"],
    "peng beng": ["坪洲"],
    "po toi": ["蒲台"],
    "sai kung": ["西貢"],
    "clear water bay": ["清水灣"],
    "happy valley": ["跑馬地"],
    "wong tai sin": ["黃大仙"],
    "san po kong": ["新蒲崗"],
    "lam tin": ["藍田"],
    "tsim sha tsui": ["尖沙咀"],
    "jordan": ["佐敦"],
    "yau ma tei": ["油麻地"],
    "sham shui po": ["深水埗"],
    "cheung sha wan": ["長沙灣"],
    "mei foo": ["美孚"],
    "lai king": ["荔景"],
    "kowloon tong": ["九龍塘"],
    "ho man tin": ["何文田"],
    "hung hom": ["紅磡"],
    "to kwa wan": ["土瓜灣"],
    "ma tau wai": ["馬頭圍"],
    "kai tak": ["啟德"],
    "ngau tau kok": ["牛頭角"],
    "sau mau ping": ["秀茂坪"],
    "tsz wan shan": ["慈雲山"],
    "choi hung": ["彩虹"],
    "po lam": ["寶琳"],
    "hang hau": ["坑口"],
    "tseung kwan o": ["將軍澳"],
    "lok fu": ["樂富"],
    "wong tai sin": ["黃大仙"],
    "diamond hill": ["鑽石山"],
    "choi wan": ["彩雲"],
    "shun lee": ["順利"],
}


def fetch_json(data_type, lang="en"):
    """Fetch from HKO API with simple file cache."""
    cache_file = os.path.join(CACHE_DIR, f"{data_type}_{lang}.json")

    # Check cache
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < CACHE_TTL_SECONDS:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)

    # Fetch fresh
    url = f"{BASE_URL}?dataType={data_type}&lang={lang}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hk-weather-info/1.1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        # Save cache
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return data
    except Exception as e:
        # Try to use stale cache if available
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"error": str(e)}


def match_region(data_list, region):
    """Match region to a data entry (case-insensitive partial match on 'place').
    Supports English region names via Chinese aliases."""
    if not region or not data_list:
        return None
    region_lower = region.lower()
    aliases = REGION_ALIASES.get(region_lower, [])
    for entry in data_list:
        place = entry.get("place", "")
        place_lower = place.lower()
        # Direct match
        if region_lower in place_lower:
            return entry
        # Alias match (English → Chinese)
        for alias in aliases:
            if alias in place:
                return entry
    return None


def format_current_weather(data, region=None):
    """Format current weather report."""
    lines = []

    # Temperature
    temp_data = data.get("temperature", {}).get("data", []) if isinstance(data.get("temperature"), dict) else data.get("temperature", [])
    if region:
        matched = match_region(temp_data, region)
        if matched:
            lines.append(f"🌡️ Temperature: {matched['value']}°{matched.get('unit', 'C')} ({matched['place']})")
        else:
            lines.append(f"🌡️ Temperature: No data for '{region}'. Showing all stations:")
            for t in temp_data[:5]:
                lines.append(f"   {t['place']}: {t['value']}°{t.get('unit', 'C')}")
    else:
        for t in temp_data[:5]:
            lines.append(f"🌡️ {t['place']}: {t['value']}°{t.get('unit', 'C')}")

    # Humidity
    humidity = data.get("humidity", {})
    if isinstance(humidity, dict):
        hum_data = humidity.get("data", [])
        if hum_data and isinstance(hum_data, list):
            h = hum_data[0]
            unit = h.get("unit", "%")
            if unit.lower() == "percent":
                unit = "%"
            lines.append(f"💧 Humidity: {h.get('value', '?')}{unit}")
        elif humidity.get("value"):
            unit = humidity.get("unit", "%")
            if unit.lower() == "percent":
                unit = "%"
            lines.append(f"💧 Humidity: {humidity.get('value', '?')}{unit}")
    elif isinstance(humidity, (int, float)):
        lines.append(f"💧 Humidity: {humidity}%")

    # Rainfall
    rainfall_data = data.get("rainfall", {}).get("data", []) if isinstance(data.get("rainfall"), dict) else data.get("rainfall", [])
    if region:
        matched = match_region(rainfall_data, region)
        if matched and "value" in matched:
            lines.append(f"🌧️ Rainfall: {matched['value']}{matched.get('unit', 'mm')} ({matched['place']})")
        else:
            lines.append(f"🌧️ Rainfall: No data for '{region}'")
    else:
        non_zero = [r for r in rainfall_data if float(r.get("value", 0)) > 0]
        if non_zero:
            for r in non_zero[:5]:
                lines.append(f"🌧️ {r['place']}: {r['value']}{r.get('unit', 'mm')}")
        else:
            lines.append("🌧️ Rainfall: No significant rainfall")

    # UV Index
    uv = data.get("uvindex", {})
    if uv and uv.get("data"):
        for u in uv["data"]:
            lines.append(f"☀️ UV Index: {u.get('value', '?')} ({u.get('place', '')})")

    # Weather icon
    icon = data.get("icon", [])
    if icon:
        lines.append(f"🌤️ Weather Icon: {icon[0] if isinstance(icon, list) else icon}")

    # Warning message — may be a string or a list of strings
    warning = data.get("warningMessage", "")
    if warning:
        if isinstance(warning, list):
            for w in warning:
                lines.append(f"⚠️ {w}")
        else:
            lines.append(f"⚠️ Active Warnings: {warning}")
    else:
        lines.append("⚠️ Active Warnings: None")

    # Rainstorm reminder
    reminder = data.get("rainstormReminder", "")
    if reminder:
        lines.append(f"🌧️ Rainstorm Reminder: {reminder}")

    # Update time
    update_time = data.get("updateTime", "")
    if update_time:
        lines.append(f"\n🕐 Last Updated: {update_time}")

    return "\n".join(lines)


def format_forecast(data):
    """Format local weather forecast."""
    lines = []

    # General situation
    general = data.get("generalSituation", "")
    if general:
        lines.append(f"📋 General Situation:\n{general}\n")

    # Forecast description
    forecast_desc = data.get("forecastDesc", "")
    if forecast_desc:
        lines.append(f"📅 Forecast:\n{forecast_desc}\n")

    # Tropical cyclone info
    tc_info = data.get("tcInfo", "")
    if tc_info:
        lines.append(f"🌀 Tropical Cyclone Info:\n{tc_info}\n")

    # Fire danger warning
    fire = data.get("fireDangerWarning", "")
    if fire:
        lines.append(f"🔥 Fire Danger Warning: {fire}\n")

    # Outlook
    outlook = data.get("outlook", "")
    if outlook:
        lines.append(f"🔮 Outlook:\n{outlook}\n")

    # Update time
    update_time = data.get("updateTime", "")
    if update_time:
        lines.append(f"🕐 Last Updated: {update_time}")

    return "\n".join(lines)


def fetch_1min_temp_csv(lang="tc"):
    """Fetch 1-minute average temperature CSV from HKO. Returns list of dicts or None."""
    if lang not in CSV_URLS:
        return None

    url = CSV_URLS[lang]
    cache_file = os.path.join(CACHE_DIR, f"1min_temp_{lang}.csv")

    # Check 1-minute cache
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < CSV_CACHE_TTL:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if content.strip():
                    reader = csv.DictReader(io.StringIO(content))
                    return list(reader)
            except Exception:
                pass  # fall through to re-fetch

    # Fetch with retries
    last_err = None
    for attempt in range(CSV_MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hk-weather-info/1.1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode("utf-8")
            # Strip BOM
            content = content.lstrip('\ufeff')
            if not content.strip():
                last_err = "empty response"
                continue
            # Save cache
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(content)
            reader = csv.DictReader(io.StringIO(content))
            rows = list(reader)
            if rows:
                return rows
            last_err = "no data rows"
        except Exception as e:
            last_err = str(e)

    # Try stale cache as last resort
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)
                if rows:
                    return rows
        except Exception:
            pass

    return None


def get_1min_temp(rows, region=None):
    """Extract 1-minute temp: regional match or HK-wide average.
    Returns (temp_float, label_str) or None."""
    if not rows:
        return None

    # Identify column names (language-dependent)
    first = rows[0]
    # Place column: try common names including Chinese variants
    place_keys = [k for k in first.keys() if any(
        p in k.lower() for p in ("place", "地區", "地区", "station", "自動氣象站", "氣象站", "站")
    )]
    # Temperature column: try common names including Chinese variants with special chars
    temp_keys = [k for k in first.keys() if any(
        t in k.lower() for t in ("temperature", "溫度", "温度", "temp", "氣溫", "气温")
    )]

    if not place_keys or not temp_keys:
        return None

    place_col = place_keys[0]
    temp_col = temp_keys[0]

    if region:
        region_lower = region.lower()
        aliases = REGION_ALIASES.get(region_lower, [])
        # Also try the raw region name itself
        for row in rows:
            place_val = row.get(place_col, "")
            place_lower = place_val.lower()
            # Direct match (English name in Chinese text, or partial)
            if region_lower in place_lower:
                try:
                    temp = float(row[temp_col])
                    return (temp, place_val)
                except (ValueError, TypeError):
                    continue
            # Alias match
            for alias in aliases:
                if alias in place_val:
                    try:
                        temp = float(row[temp_col])
                        return (temp, place_val)
                    except (ValueError, TypeError):
                        continue
        # No regional match — fall through to average

    # HK-wide average
    temps = []
    for row in rows:
        try:
            t = float(row.get(temp_col, ""))
            temps.append(t)
        except (ValueError, TypeError):
            continue

    if temps:
        avg = sum(temps) / len(temps)
        return (round(avg, 1), None)  # None = average

    return None


def format_1min_temp(result, lang="tc"):
    """Format 1-minute average temperature line."""
    if result is None:
        return None
    temp, label = result
    if label:
        if lang == "tc":
            return f"🕒 1分鐘平均氣溫：{temp}°C（{label}）"
        elif lang == "sc":
            return f"🕒 1分钟平均气温：{temp}°C（{label}）"
        else:
            return f"🕒 1-Min Avg Temp: {temp}°C ({label})"
    else:
        if lang == "tc":
            return f"🕒 1分鐘平均氣溫：{temp}°C（全港平均）"
        elif lang == "sc":
            return f"🕒 1分钟平均气温：{temp}°C（全港平均）"
        else:
            return f"🕒 1-Min Avg Temp: {temp}°C (HK Average)"


def main():
    parser = argparse.ArgumentParser(description="HK Weather Info — HKO OpenData")
    parser.add_argument("--region", type=str, default=None, help="Target region/district (e.g. 'Tsuen Wan', 'Central')")
    parser.add_argument("--lang", type=str, default="tc", choices=LANG_CHOICES, help="Language: en, tc, or sc (default: tc)")
    parser.add_argument("--action", type=str, default="all", choices=["current", "forecast", "all"], help="What to fetch")
    args = parser.parse_args()

    region_display = args.region if args.region else "Hong Kong (General)"

    print(f"🇭🇰 HK Weather Info")
    print(f"   Region: {region_display}")
    print(f"   Language: {args.lang}")
    print("")

    if args.action in ("current", "all"):
        print("=" * 50)
        print("CURRENT WEATHER")
        print("=" * 50)
        current = fetch_json("rhrread", args.lang)
        if "error" in current:
            print(f"Error fetching current weather: {current['error']}")
        else:
            print(format_current_weather(current, args.region))
        print("")

    if args.action in ("forecast", "all"):
        print("=" * 50)
        print("LOCAL WEATHER FORECAST")
        print("=" * 50)
        forecast = fetch_json("flw", args.lang)
        if "error" in forecast:
            print(f"Error fetching forecast: {forecast['error']}")
        else:
            print(format_forecast(forecast))
        print("")

    # Step 3: 1-minute average temperature
    csv_rows = fetch_1min_temp_csv(args.lang)
    if csv_rows:
        result = get_1min_temp(csv_rows, args.region)
        line = format_1min_temp(result, args.lang)
        if line:
            print(line)
            print("")


if __name__ == "__main__":
    main()
