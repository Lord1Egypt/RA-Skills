#!/usr/bin/env python3
"""Query air quality forecast from monitoring stations via the Caiyun Weather API."""

import argparse
import json
import math
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.caiyunapp.com/v2.6"
STATION_API = "https://singer.caiyunhub.com/v3/aqi/forecast/station"


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


def api_get_safe(url):
    """Like api_get but returns None on error instead of exiting."""
    req = urllib.request.Request(url, headers={"User-Agent": "knowair-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def aqi_level(aqi, lang):
    if lang == "zh":
        levels = [(50, "优"), (100, "良"), (150, "轻度污染"), (200, "中度污染"), (300, "重度污染")]
        return next((l for v, l in levels if aqi <= v), "严重污染")
    levels = [(50, "Good"), (100, "Moderate"), (150, "Unhealthy for Sensitive"), (200, "Unhealthy"), (300, "Very Unhealthy")]
    return next((l for v, l in levels if aqi <= v), "Hazardous")


def health_advice(aqi, lang):
    if lang == "zh":
        if aqi <= 50:
            return "空气质量优秀，适合户外活动"
        elif aqi <= 100:
            return "空气质量可接受，敏感人群应减少户外运动"
        elif aqi <= 150:
            return "敏感人群应避免户外活动"
        elif aqi <= 200:
            return "所有人应减少户外活动"
        else:
            return "避免户外活动，建议佩戴口罩"
    else:
        if aqi <= 50:
            return "Air quality is excellent. Enjoy outdoor activities."
        elif aqi <= 100:
            return "Acceptable. Sensitive individuals should reduce outdoor exertion."
        elif aqi <= 150:
            return "Sensitive groups should avoid outdoor activity."
        elif aqi <= 200:
            return "Everyone should reduce outdoor activity."
        else:
            return "Avoid outdoor activity. Wear a mask if going outside."


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


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def format_station_data(station_data, api_data, hours, detail_level, lng, lat, lang):
    entries = []
    step = get_detail_step(detail_level, hours)

    # Process station data
    station_entries = {}
    if station_data and station_data.get("status") == "ok":
        results = station_data.get("result", {})
        stations = results.get("stations", [])

        # Find nearest station
        nearest = None
        min_dist = float("inf")
        for s in stations:
            slat = s.get("lat", 0)
            slng = s.get("lng", 0)
            dist = haversine(lat, lng, slat, slng)
            if dist < min_dist:
                min_dist = dist
                nearest = s

        if nearest:
            forecasts = nearest.get("forecasts", [])
            for fc in forecasts:
                dt = fc.get("datetime", "")
                station_entries[dt] = {
                    "time": dt,
                    "aqi": fc.get("aqi"),
                    "pm25": fc.get("pm25"),
                    "pm10": fc.get("pm10"),
                    "o3": fc.get("o3"),
                    "no2": fc.get("no2"),
                    "so2": fc.get("so2"),
                    "co": fc.get("co"),
                    "source": "station",
                }

    # Process API data as fallback
    api_entries = {}
    if api_data:
        hourly = api_data.get("result", {}).get("hourly", {})
        aqi_h = hourly.get("air_quality", {}).get("aqi", [])[:hours]
        pm25_h = hourly.get("air_quality", {}).get("pm25", [])[:hours]
        for i in range(len(aqi_h)):
            dt = aqi_h[i].get("datetime", "")
            api_entries[dt] = {
                "time": dt,
                "aqi": aqi_h[i].get("value", {}).get("chn"),
                "pm25": pm25_h[i].get("value") if i < len(pm25_h) else None,
                "source": "api",
            }

    # Merge: station takes priority
    all_times = sorted(set(list(station_entries.keys()) + list(api_entries.keys())))
    for t in all_times:
        if t in station_entries:
            entries.append(station_entries[t])
        elif t in api_entries:
            entries.append(api_entries[t])

    # Apply detail level sampling
    sampled = entries[::step] if step > 1 else entries

    # Summary stats
    aqi_vals = [e["aqi"] for e in entries if e.get("aqi") is not None]
    best_aqi = min(aqi_vals) if aqi_vals else None
    worst_aqi = max(aqi_vals) if aqi_vals else None
    current_aqi = aqi_vals[0] if aqi_vals else None

    result = {
        "forecast": sampled[:hours],
        "total_entries": len(entries),
    }

    if current_aqi is not None:
        result["current"] = {
            "aqi": current_aqi,
            "level": aqi_level(current_aqi, lang),
            "advice": health_advice(current_aqi, lang),
        }

    if best_aqi is not None:
        best_entry = next(e for e in entries if e.get("aqi") == best_aqi)
        worst_entry = next(e for e in entries if e.get("aqi") == worst_aqi)
        result["summary"] = {
            "best_aqi": best_aqi,
            "best_time": best_entry.get("time", ""),
            "worst_aqi": worst_aqi,
            "worst_time": worst_entry.get("time", ""),
            "avg_aqi": round(sum(aqi_vals) / len(aqi_vals), 1),
        }

    if nearest:
        result["station"] = {
            "name": nearest.get("name", ""),
            "distance_km": round(min_dist, 1),
        }

    return result


def main():
    parser = argparse.ArgumentParser(description="Query Caiyun Air Quality Forecast")
    parser.add_argument("--lng", type=float, required=True, help="Longitude (-180 to 180)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (-90 to 90)")
    parser.add_argument("--hours", type=int, default=120, help="Forecast hours (1-360)")
    parser.add_argument("--detail-level", type=int, default=0, help="Detail level 0-6")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Output language")
    args = parser.parse_args()

    token = get_token()
    if not token:
        print(json.dumps({"error": "No API token found. Set CAIYUN_TOKEN env var or create ~/.config/knowair/token"}))
        sys.exit(2)

    hours = max(1, min(360, args.hours))

    # Fetch station data
    station_url = f"{STATION_API}?token={token}&lng={args.lng}&lat={args.lat}&hours={hours}"
    station_data = api_get_safe(station_url)

    # Fetch API data as fallback
    api_url = f"{API_BASE}/{token}/{args.lng},{args.lat}/weather?hourlysteps={hours}"
    api_data = api_get_safe(api_url)

    if not station_data and not api_data:
        print(json.dumps({"error": "Failed to fetch air quality data from both station and API sources."}))
        sys.exit(1)

    result = format_station_data(station_data, api_data, hours, args.detail_level, args.lng, args.lat, args.lang)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
