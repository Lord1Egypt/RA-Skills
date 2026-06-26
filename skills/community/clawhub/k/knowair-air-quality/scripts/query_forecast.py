#!/usr/bin/env python3
"""Query hourly or daily weather forecast from the Caiyun Weather API."""

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


def get_detail_step(detail_level, total):
    if detail_level == 0:
        if total <= 24:
            return 1
        elif total <= 72:
            return 3
        elif total <= 168:
            return 6
        else:
            return 12
    return max(1, detail_level)


def format_hourly(data, hours, detail_level, lang):
    hourly = data.get("result", {}).get("hourly", {})
    skycon_map = SKYCON_ZH if lang == "zh" else SKYCON_EN

    temps = hourly.get("temperature", [])[:hours]
    skycons = hourly.get("skycon", [])[:hours]
    precip = hourly.get("precipitation", [])[:hours]
    humidity = hourly.get("humidity", [])[:hours]
    wind = hourly.get("wind", [])[:hours]
    visibility = hourly.get("visibility", [])[:hours]
    pressure = hourly.get("pressure", [])[:hours]

    step = get_detail_step(detail_level, hours)
    entries = []

    for i in range(0, len(temps), step):
        entry = {
            "time": temps[i].get("datetime", ""),
            "temperature": temps[i].get("value"),
        }
        if i < len(skycons):
            entry["weather"] = skycon_map.get(skycons[i].get("value", ""), skycons[i].get("value", ""))
        if i < len(precip):
            entry["precip_probability"] = f"{precip[i].get('probability', 0):.0f}%"
            entry["precip_intensity"] = precip[i].get("value", 0)
        if i < len(humidity):
            entry["humidity"] = f"{humidity[i].get('value', 0) * 100:.0f}%"
        if i < len(wind):
            entry["wind_speed"] = f"{wind[i].get('speed', 0):.1f} km/h"
        entries.append(entry)

    # Forecast summary
    fc = data.get("result", {}).get("forecast_keypoint", "")
    result = {"hourly_forecast": entries, "total_hours": len(temps)}
    if fc:
        result["summary"] = fc
    return result


def format_daily(data, days, lang):
    daily = data.get("result", {}).get("daily", {})
    skycon_map = SKYCON_ZH if lang == "zh" else SKYCON_EN

    temps = daily.get("temperature", [])[:days]
    skycons_day = daily.get("skycon_08h_20h", daily.get("skycon", []))[:days]
    skycons_night = daily.get("skycon_20h_32h", [])[:days]
    precip = daily.get("precipitation", [])[:days]
    humidity_d = daily.get("humidity", [])[:days]
    wind_d = daily.get("wind", [])[:days]
    astro = daily.get("astro", [])[:days]
    aqi_d = daily.get("air_quality", {}).get("aqi", [])[:days]
    li = daily.get("life_index", {})
    uv = li.get("ultraviolet", [])[:days]
    comfort = li.get("comfort", [])[:days]
    carwash = li.get("carWashing", [])[:days]
    dressing = li.get("dressing", [])[:days]
    cold_risk = li.get("coldRisk", [])[:days]

    entries = []
    for i in range(len(temps)):
        entry = {
            "date": temps[i].get("date", "")[:10],
            "temp_high": temps[i].get("max"),
            "temp_low": temps[i].get("min"),
        }
        if i < len(skycons_day):
            entry["weather_day"] = skycon_map.get(skycons_day[i].get("value", ""), skycons_day[i].get("value", ""))
        if i < len(skycons_night):
            entry["weather_night"] = skycon_map.get(skycons_night[i].get("value", ""), skycons_night[i].get("value", ""))
        if i < len(precip):
            entry["precip_probability"] = f"{precip[i].get('probability', 0):.0f}%"
        if i < len(humidity_d):
            entry["humidity_avg"] = f"{humidity_d[i].get('avg', 0) * 100:.0f}%"
        if i < len(wind_d):
            entry["wind_avg"] = f"{wind_d[i].get('avg', {}).get('speed', 0):.1f} km/h"
        if i < len(astro):
            entry["sunrise"] = astro[i].get("sunrise", {}).get("time", "")
            entry["sunset"] = astro[i].get("sunset", {}).get("time", "")
        if i < len(aqi_d):
            entry["aqi_avg"] = aqi_d[i].get("avg", {}).get("chn")
        if i < len(uv):
            entry["uv"] = uv[i].get("desc", "")
        if i < len(comfort):
            entry["comfort"] = comfort[i].get("desc", "")
        if i < len(carwash):
            entry["car_wash"] = carwash[i].get("desc", "")
        if i < len(dressing):
            entry["dressing"] = dressing[i].get("desc", "")
        if i < len(cold_risk):
            entry["cold_risk"] = cold_risk[i].get("desc", "")
        entries.append(entry)

    fc = data.get("result", {}).get("forecast_keypoint", "")
    result = {"daily_forecast": entries, "total_days": len(entries)}
    if fc:
        result["summary"] = fc
    return result


def main():
    parser = argparse.ArgumentParser(description="Query Caiyun Weather Forecast")
    parser.add_argument("--lng", type=float, required=True, help="Longitude (-180 to 180)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (-90 to 90)")
    parser.add_argument("--type", choices=["hourly", "daily"], default="daily", dest="forecast_type")
    parser.add_argument("--hours", type=int, default=48, help="Hours to forecast (1-360)")
    parser.add_argument("--days", type=int, default=7, help="Days to forecast (1-15)")
    parser.add_argument("--detail-level", type=int, default=0, help="Detail level 0-6 (hourly mode)")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Output language")
    args = parser.parse_args()

    token = get_token()
    if not token:
        print(json.dumps({"error": "No API token found. Set CAIYUN_TOKEN env var or create ~/.config/knowair/token"}))
        sys.exit(2)

    if args.forecast_type == "hourly":
        hours = max(1, min(360, args.hours))
        url = f"{API_BASE}/{token}/{args.lng},{args.lat}/weather?hourlysteps={hours}&lang={args.lang}"
        data = api_get(url)
        result = format_hourly(data, hours, args.detail_level, args.lang)
    else:
        days = max(1, min(15, args.days))
        url = f"{API_BASE}/{token}/{args.lng},{args.lat}/weather?dailysteps={days}&lang={args.lang}"
        data = api_get(url)
        result = format_daily(data, days, args.lang)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
