#!/usr/bin/env python3
"""Query minute-level precipitation forecast from the Caiyun Weather API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.caiyunapp.com/v2.6"


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


def intensity_desc(val, lang):
    if lang == "zh":
        if val == 0:
            return "无降水"
        elif val < 0.031:
            return "毛毛雨"
        elif val < 0.25:
            return "小雨"
        elif val < 0.35:
            return "中雨"
        elif val < 0.48:
            return "大雨"
        else:
            return "暴雨"
    else:
        if val == 0:
            return "No precipitation"
        elif val < 0.031:
            return "Drizzle"
        elif val < 0.25:
            return "Light rain"
        elif val < 0.35:
            return "Moderate rain"
        elif val < 0.48:
            return "Heavy rain"
        else:
            return "Storm rain"


def format_minutely(data, lang):
    minutely = data.get("result", {}).get("minutely", {})
    precip_2h = minutely.get("precipitation_2h", [])
    precip = minutely.get("precipitation", [])
    probability = minutely.get("probability", [])
    description = minutely.get("description", "")
    datasource = minutely.get("datasource", "")

    # Sample every 5 minutes for display
    samples = []
    series = precip_2h if precip_2h else precip
    for i in range(0, min(120, len(series)), 5):
        val = series[i]
        samples.append({
            "minute": i,
            "intensity": round(val, 4),
            "description": intensity_desc(val, lang),
        })

    result = {
        "description": description,
        "precipitation_samples": samples,
        "datasource": datasource,
    }

    if probability:
        labels = ["0-30min", "30-60min", "60-90min", "90-120min"] if lang == "en" else ["0-30分钟", "30-60分钟", "60-90分钟", "90-120分钟"]
        result["probability"] = [
            {"period": labels[i], "probability": f"{probability[i]:.0f}%"}
            for i in range(min(4, len(probability)))
        ]

    return result


def main():
    parser = argparse.ArgumentParser(description="Query Caiyun Minutely Precipitation")
    parser.add_argument("--lng", type=float, required=True, help="Longitude (-180 to 180)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (-90 to 90)")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Output language")
    args = parser.parse_args()

    token = get_token()
    if not token:
        print(json.dumps({"error": "No API token found. Set CAIYUN_TOKEN env var or create ~/.config/knowair/token"}))
        sys.exit(2)

    url = f"{API_BASE}/{token}/{args.lng},{args.lat}/minutely?lang={args.lang}"
    data = api_get(url)
    result = format_minutely(data, args.lang)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
