#!/usr/bin/env python3
"""Query historical weather data from the Caiyun Weather API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.caiyunapp.com/v2.6"

SKYCON_EN = {
    "CLEAR_DAY": "Clear", "CLEAR_NIGHT": "Clear",
    "PARTLY_CLOUDY_DAY": "Partly Cloudy", "PARTLY_CLOUDY_NIGHT": "Partly Cloudy",
    "CLOUDY": "Cloudy", "LIGHT_HAZE": "Light Haze", "MODERATE_HAZE": "Moderate Haze",
    "HEAVY_HAZE": "Heavy Haze", "LIGHT_RAIN": "Light Rain", "MODERATE_RAIN": "Moderate Rain",
    "HEAVY_RAIN": "Heavy Rain", "STORM_RAIN": "Storm Rain",
    "FOG": "Fog", "LIGHT_SNOW": "Light Snow", "MODERATE_SNOW": "Moderate Snow",
    "HEAVY_SNOW": "Heavy Snow", "STORM_SNOW": "Storm Snow",
    "DUST": "Dust", "SAND": "Sand", "WIND": "Windy",
}

SKYCON_ZH = {
    "CLEAR_DAY": "晴", "CLEAR_NIGHT": "晴",
    "PARTLY_CLOUDY_DAY": "多云", "PARTLY_CLOUDY_NIGHT": "多云",
    "CLOUDY": "阴", "LIGHT_HAZE": "轻度雾霾", "MODERATE_HAZE": "中度雾霾",
    "HEAVY_HAZE": "重度雾霾", "LIGHT_RAIN": "小雨", "MODERATE_RAIN": "中雨",
    "HEAVY_RAIN": "大雨", "STORM_RAIN": "暴雨",
    "FOG": "雾", "LIGHT_SNOW": "小雪", "MODERATE_SNOW": "中雪",
    "HEAVY_SNOW": "大雪", "STORM_SNOW": "暴雪",
    "DUST": "浮尘", "SAND": "沙尘", "WIND": "大风",
}


def get_token():
    token = os.environ.get("CAIYUN_TOKEN")
    if token:
        return token.strip()
    config_path = os.path.expanduser("~/.config/knowair/token")
    if os.path.isfile(config_path):
        with open(config_path) as f:
            return f.read().strip()
    return None


def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "knowair-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code}: {e.reason}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Network error: {e.reason}"}))
        sys.exit(1)


def format_historical(data, hours_back, lang):
    hourly = data.get("result", {}).get("hourly", {})
    skycon_map = SKYCON_ZH if lang == "zh" else SKYCON_EN

    temps = hourly.get("temperature", [])
    skycons = hourly.get("skycon", [])
    precip = hourly.get("precipitation", [])
    humidity = hourly.get("humidity", [])
    wind = hourly.get("wind", [])
    apparent = hourly.get("apparent_temperature", [])
    aqi_h = hourly.get("air_quality", {}).get("aqi", [])
    pm25_h = hourly.get("air_quality", {}).get("pm25", [])

    # Sample every 2-3 hours for readability
    step = 2 if hours_back <= 24 else 3
    entries = []

    for i in range(0, min(hours_back, len(temps)), step):
        entry = {
            "time": temps[i].get("datetime", ""),
            "temperature": temps[i].get("value"),
        }
        if i < len(apparent):
            entry["apparent_temperature"] = apparent[i].get("value")
        if i < len(skycons):
            entry["weather"] = skycon_map.get(skycons[i].get("value", ""), skycons[i].get("value", ""))
        if i < len(precip):
            entry["precip_intensity"] = precip[i].get("value", 0)
        if i < len(humidity):
            entry["humidity"] = f"{humidity[i].get('value', 0) * 100:.0f}%"
        if i < len(wind):
            entry["wind_speed"] = f"{wind[i].get('speed', 0):.1f} km/h"
        if i < len(aqi_h):
            entry["aqi"] = aqi_h[i].get("value", {}).get("chn")
        if i < len(pm25_h):
            entry["pm25"] = pm25_h[i].get("value")
        entries.append(entry)

    # Summary
    temp_vals = [t.get("value") for t in temps[:hours_back] if t.get("value") is not None]
    result = {"history": entries, "total_hours": min(hours_back, len(temps))}
    if temp_vals:
        result["summary"] = {
            "temp_high": max(temp_vals),
            "temp_low": min(temp_vals),
            "temp_avg": round(sum(temp_vals) / len(temp_vals), 1),
        }

    return result


def main():
    parser = argparse.ArgumentParser(description="Query Caiyun Historical Weather")
    parser.add_argument("--lng", type=float, required=True, help="Longitude (-180 to 180)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (-90 to 90)")
    parser.add_argument("--hours", type=int, default=24, help="Hours to look back (1-72)")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Output language")
    args = parser.parse_args()

    token = get_token()
    if not token:
        print(json.dumps({"error": "No API token found. Set CAIYUN_TOKEN env var or create ~/.config/knowair/token"}))
        sys.exit(2)

    hours = max(1, min(72, args.hours))
    url = f"{API_BASE}/{token}/{args.lng},{args.lat}/weather?hourlysteps={hours}&lang={args.lang}"
    data = api_get(url)
    result = format_historical(data, hours, args.lang)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
