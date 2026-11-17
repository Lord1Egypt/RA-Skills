#!/usr/bin/env python3
"""Fetch current weather + daily forecast from Open-Meteo (free, no API key).

Zero dependencies — Python 3.8+ standard library only.

Usage:
  python3 get_weather.py "Taipei"                 # current + 3-day forecast
  python3 get_weather.py "Paris" --country FR     # disambiguate place name
  python3 get_weather.py --lat 25.05 --lon 121.53 # skip geocoding
  python3 get_weather.py "Tokyo" --days 7         # up to 16 days
  python3 get_weather.py "Denver" --fahrenheit
  python3 get_weather.py "Taipei" --json          # raw JSON for programmatic use

Exit codes: 0 success, 1 place not found, 2 API/network error.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def fetch_json(url: str, params: dict) -> dict:
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(full_url, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            reason = json.load(e).get("reason", str(e))
        except Exception:
            reason = str(e)
        print(f"API error: {reason}", file=sys.stderr)
        sys.exit(2)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(2)


def geocode(place: str, country: str | None) -> dict:
    data = fetch_json(GEOCODING_URL, {"name": place, "count": 10, "language": "en"})
    results = data.get("results")  # absent entirely when nothing matches
    if not results:
        print(f"Place not found: {place!r} (try the city name alone)", file=sys.stderr)
        sys.exit(1)
    if country:
        results = [r for r in results if r.get("country_code", "").upper() == country.upper()]
        if not results:
            print(f"No match for {place!r} in country {country!r}", file=sys.stderr)
            sys.exit(1)
    return results[0]


def describe(code) -> str:
    return WMO_CODES.get(code, f"Unknown (code {code})")


def main() -> None:
    p = argparse.ArgumentParser(description="Open-Meteo weather lookup (no API key)")
    p.add_argument("place", nargs="?", help="Place name, e.g. 'Taipei' or 'New York'")
    p.add_argument("--lat", type=float, help="Latitude (use with --lon instead of a place name)")
    p.add_argument("--lon", type=float, help="Longitude")
    p.add_argument("--country", help="ISO-3166 country code filter for geocoding, e.g. FR, US")
    p.add_argument("--days", type=int, default=3, help="Forecast days 0-16 (default 3)")
    p.add_argument("--fahrenheit", action="store_true", help="Use Fahrenheit and mph")
    p.add_argument("--json", action="store_true", help="Print raw JSON instead of formatted text")
    args = p.parse_args()

    if args.lat is not None and args.lon is not None:
        location = {"name": f"{args.lat},{args.lon}", "latitude": args.lat, "longitude": args.lon}
    elif args.place:
        location = geocode(args.place, args.country)
    else:
        p.error("provide a place name, or both --lat and --lon")

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                   "precipitation,weather_code,wind_speed_10m,wind_direction_10m,is_day",
        "timezone": "auto",
        "forecast_days": max(args.days, 1) if args.days else 1,
    }
    if args.days:
        params["daily"] = ("weather_code,temperature_2m_max,temperature_2m_min,"
                           "precipitation_sum,precipitation_probability_max,"
                           "sunrise,sunset,uv_index_max")
    if args.fahrenheit:
        params["temperature_unit"] = "fahrenheit"
        params["wind_speed_unit"] = "mph"

    data = fetch_json(FORECAST_URL, params)

    if args.json:
        data["location"] = location
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    t_unit = data["current_units"]["temperature_2m"]
    w_unit = data["current_units"]["wind_speed_10m"]
    parts = [str(location[k]) for k in ("name", "admin1", "country") if location.get(k)]
    place_label = ", ".join(dict.fromkeys(parts))  # drop duplicates like admin1 == country
    cur = data["current"]
    print(f"Weather for {place_label} ({data['timezone']})")
    print(f"  As of {cur['time']}: {describe(cur['weather_code'])}")
    print(f"  Temperature: {cur['temperature_2m']}{t_unit} "
          f"(feels like {cur['apparent_temperature']}{t_unit})")
    print(f"  Humidity: {cur['relative_humidity_2m']}%   "
          f"Wind: {cur['wind_speed_10m']} {w_unit} from {cur['wind_direction_10m']}°")
    if cur["precipitation"] > 0:
        print(f"  Precipitation (last interval): {cur['precipitation']} "
              f"{data['current_units']['precipitation']}")

    if args.days and "daily" in data:
        d = data["daily"]
        print(f"\n  {'Date':<12}{'Condition':<32}{'Min':>7}{'Max':>7}"
              f"{'Rain%':>7}{'Rain':>8}{'UV':>5}")
        for i, day in enumerate(d["time"]):
            print(f"  {day:<12}{describe(d['weather_code'][i]):<32}"
                  f"{d['temperature_2m_min'][i]:>6}°{d['temperature_2m_max'][i]:>6}°"
                  f"{d['precipitation_probability_max'][i]:>6}%"
                  f"{d['precipitation_sum'][i]:>6}mm"
                  f"{d['uv_index_max'][i]:>5}")
        print(f"\n  Sunrise {d['sunrise'][0][-5:]}  Sunset {d['sunset'][0][-5:]} (today, local time)")


if __name__ == "__main__":
    main()
