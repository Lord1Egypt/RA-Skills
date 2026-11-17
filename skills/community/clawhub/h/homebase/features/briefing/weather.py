#!/usr/bin/env python3
"""
Weather Module for Homebase
Fetches weather from Open-Meteo (free, no API key) using configured coordinates.
"""

import json
import sys
from typing import Optional, Dict

def _get_coords():
    try:
        from core.config_loader import config
        return config.latitude, config.longitude
    except Exception:
        return 0.0, 0.0  # Set coordinates in config.json
LATITUDE, LONGITUDE = _get_coords()


def _home_timezone() -> str:
    """The household's own timezone, from config.

    Three Open-Meteo URLs here (plus one in trip_detector) hardcoded
    America/Los_Angeles while config.timezone sat unused. Harmless at home and
    in Seattle; on a trip to anywhere else it mislabels the hourly series,
    and fetch_weather_context slices that series by `start_hour <= h <=
    end_hour` — so the "what should the kids wear to school" window silently
    reported the wrong hours of the day.
    """
    try:
        from core.config_loader import config
        return config.timezone or "America/Los_Angeles"
    except Exception:
        return "America/Los_Angeles"


def _timezone_for(location: Optional[str]) -> str:
    """`auto` when a destination is named — Open-Meteo then returns the hourly
    series in the *destination's* local time, which is what an hour filter has
    to mean when the family is standing there. Home coords use home's zone."""
    return "auto" if location else _home_timezone()


# Successful lookups only. `@lru_cache` also memoized the `return None`
# failure path, so a single transient DNS blip pinned home coordinates for the
# rest of the process — the briefing reported home weather while the family was
# away, with only a stderr line to say so. A destination changes a couple of
# times a year, so a plain dict is enough, and the forecast call retries 3x
# while geocoding retries 0x.
_GEOCODE_CACHE: Dict[str, tuple] = {}


def _geocode_cache_clear() -> None:
    """Drop memoized coordinates. For tests."""
    _GEOCODE_CACHE.clear()


def geocode_location(location: str) -> Optional[tuple]:
    """
    Geocode a location name to (lat, lon) using the free Open-Meteo geocoding API.
    Returns None on failure, and does NOT cache that failure, so a later call
    in the same process is free to retry.
    """
    if not location:
        return None
    if location in _GEOCODE_CACHE:
        return _GEOCODE_CACHE[location]

    import urllib.parse
    import urllib.request as _req

    try:
        encoded = urllib.parse.quote(location)
        url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={encoded}&count=1&language=en&format=json"
        )
        with _req.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        results = data.get("results", [])
        if results:
            coords = (results[0]["latitude"], results[0]["longitude"])
            _GEOCODE_CACHE[location] = coords
            return coords
    except Exception as e:
        print(f"Geocode failed for '{location}': {e}", file=sys.stderr)
    return None


geocode_location.cache_clear = _geocode_cache_clear


def fetch_weather(location: Optional[str] = None) -> Optional[Dict]:
    """
    Fetch today's weather from Open-Meteo API.

    Args:
        location: Optional location name (e.g. "Big Bear Lake, CA"). If None,
                  falls back to the configured home coordinates (Irvine, CA).

    Returns structured weather data or None on failure.
    Retries up to 3 times with short back-off (network can be flaky at 7 AM).
    """
    import time as _time
    import urllib.request

    # Resolve coordinates: named location takes priority over home coords
    lat, lon = LATITUDE, LONGITUDE
    if location:
        coords = geocode_location(location)
        if coords:
            lat, lon = coords
        else:
            print(f"Could not geocode '{location}', falling back to home coords.", file=sys.stderr)

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,weather_code,"
        f"wind_speed_10m,relative_humidity_2m"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&hourly=precipitation_probability"
        f"&temperature_unit=fahrenheit"
        f"&wind_speed_unit=mph"
        f"&timezone={_timezone_for(location)}"
        f"&forecast_days=1"
    )

    last_err = None
    for attempt, delay in enumerate([0, 2, 4]):
        if delay:
            _time.sleep(delay)
        try:
            with urllib.request.urlopen(url, timeout=8) as response:
                data = json.loads(response.read().decode())

            current = data.get("current", {})
            daily   = data.get("daily", {})
            hourly  = data.get("hourly", {})
            code    = current.get("weather_code", 0)

            hourly_probs = hourly.get("precipitation_probability") or []
            rain_windows = _extract_rain_windows(hourly_probs)

            return {
                "temp_current":    round(current.get("temperature_2m", 0)),
                "temp_feels_like": round(current.get("apparent_temperature", 0)),
                "temp_high":       round((daily.get("temperature_2m_max") or [0])[0]),
                "temp_low":        round((daily.get("temperature_2m_min") or [0])[0]),
                "condition":       weather_code_to_description(code),
                "wind_speed":      round(current.get("wind_speed_10m", 0)),
                "humidity":        round(current.get("relative_humidity_2m", 0)),
                "rain_chance":     (daily.get("precipitation_probability_max") or [0])[0],
                "rain_windows":    _format_rain_timing(rain_windows),
            }
        except Exception as e:
            last_err = e
            print(f"Weather fetch attempt {attempt + 1} failed: {e}", file=sys.stderr)

    print(f"Weather fetch gave up after 3 attempts: {last_err}", file=sys.stderr)
    return None


def _extract_rain_windows(hourly_probs: list, threshold: int = 30) -> list:
    """Group consecutive hours with precipitation probability >= threshold."""
    windows = []
    start = None
    for hour, prob in enumerate(hourly_probs):
        if prob >= threshold:
            if start is None:
                start = hour
        else:
            if start is not None:
                windows.append((start, hour - 1))
                start = None
    if start is not None:
        windows.append((start, len(hourly_probs) - 1))
    return windows


def _format_hour(h: int) -> str:
    """Format 0-23 hour as '12 AM', '3 PM', etc."""
    if h == 0:
        return "12 AM"
    elif h < 12:
        return f"{h} AM"
    elif h == 12:
        return "12 PM"
    else:
        return f"{h - 12} PM"


def _format_rain_timing(windows: list) -> str:
    """Format rain windows into a readable string like '2 – 5 PM' or '8 – 10 AM, 3 – 6 PM'."""
    if not windows:
        return ""
    parts = []
    for start, end in windows:
        if start == end:
            parts.append(f"around {_format_hour(start)}")
        else:
            start_suffix = "AM" if start < 12 else "PM"
            end_suffix = "AM" if end < 12 else "PM"
            start_num = start if start <= 12 else start - 12
            end_num = end if end <= 12 else end - 12
            if start_num == 0:
                start_num = 12
            if end_num == 0:
                end_num = 12
            if start_suffix == end_suffix:
                parts.append(f"{start_num}\u2009–\u2009{end_num} {end_suffix}")
            else:
                parts.append(f"{start_num} {start_suffix}\u2009–\u2009{end_num} {end_suffix}")
    return ", ".join(parts)


def weather_code_to_description(code: int) -> str:
    """Convert WMO weather code to human-readable description."""
    codes = {
        0:  "Clear sky",
        1:  "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Freezing fog",
        51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
        61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Light snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Rain showers", 81: "Moderate showers", 82: "Heavy showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail",
    }
    return codes.get(code, "Mixed conditions")


def generate_weather_suggestion(weather: Dict) -> str:
    """
    Return structured weather facts as a compact string.
    The agent composes the human-readable summary at dispatch time.
    """
    return (
        f"{weather['condition']}, {weather['temp_current']}°F "
        f"(High {weather['temp_high']}°F / Low {weather['temp_low']}°F) · "
        f"Humidity {weather['humidity']}% · Wind {weather['wind_speed']}mph · "
        f"Rain {weather['rain_chance']}%"
    )


def get_weather_briefing(location: Optional[str] = None) -> Optional[str]:
    """
    Main entry point — fetch weather and generate suggestion.
    Returns formatted string for morning briefing or None on failure.

    `location` overrides the home coordinates for the days the household is
    somewhere else. It is the same override `fetch_weather` and
    `fetch_weather_context` already take; this entry point simply had no way to
    reach it, which meant a travelling family got Irvine's forecast in the one
    block of the briefing they are told to paste verbatim.
    """
    weather = fetch_weather(location)
    if not weather:
        return None

    suggestion = generate_weather_suggestion(weather)

    rain_warning = ""
    if weather["rain_chance"] >= 40:
        timing = weather.get("rain_windows", "")
        if timing:
            rain_warning = f"\n  ☂️ {weather['rain_chance']}% chance of rain (expected {timing}) — pack an umbrella"
        else:
            rain_warning = f"\n  ☂️ {weather['rain_chance']}% chance of rain — pack an umbrella"

    return f"🌤️ *Weather*\n  {suggestion}{rain_warning}"



# ─── School-window context ───────────────────────────────────────────────────
# get_weather_briefing() above answers "what is it like now" using current
# conditions plus the daily high/low. That cannot answer "what should the kids
# wear to school", because the daily high is often a mid-afternoon number with
# no bearing on an 8am drop-off, and because it carries no UV, air quality or
# sun times at all — none of which are visible in a temperature.

UV_BANDS = ((3, "low"), (6, "moderate"), (8, "high"), (11, "very high"))
AQI_BANDS = ((50, "good"), (100, "moderate"), (150, "unhealthy for sensitive groups"),
             (200, "unhealthy"))


def _band(value, bands, above):
    """Map a numeric reading onto its named band."""
    for ceiling, label in bands:
        if value < ceiling:
            return label
    return above


def _fetch_air_quality(lat: float, lon: float, tz: str = None) -> Optional[Dict]:
    """
    US AQI from Open-Meteo's air-quality host (separate from the forecast host).
    Boring most of the year, decisive in wildfire season. Returns None rather
    than raising — air quality is enrichment, not a hard dependency.
    """
    import urllib.request
    try:
        url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality"
            f"?latitude={lat}&longitude={lon}"
            f"&current=us_aqi,pm2_5&timezone={tz or _home_timezone()}"
        )
        with urllib.request.urlopen(url, timeout=10) as response:
            current = (json.loads(response.read().decode()).get("current") or {})
        aqi = current.get("us_aqi")
        if aqi is None:
            return None
        return {
            "us_aqi": aqi,
            "pm2_5": current.get("pm2_5"),
            "band": _band(aqi, AQI_BANDS, "very unhealthy"),
        }
    except Exception as e:
        print(f"Air quality fetch failed: {e}", file=sys.stderr)
        return None


def fetch_weather_context(start_hour: int = 8, end_hour: int = 17,
                          location: Optional[str] = None,
                          date: Optional[str] = None) -> Optional[Dict]:
    """
    Hourly conditions across a window, plus UV, sun times and air quality.

    Built for the "what to wear" question: the morning-to-midday swing decides
    whether to send a layer that can be shed, and a high UV on a mild morning
    is the case that catches people out.

    `date` (YYYY-MM-DD) selects the day; defaults to today. Tomorrow is the
    evening brief's case — the API is asked for `date - today + 1` days and
    the hourly and daily arrays are sliced to the target day. Past dates and
    dates more than a week out return None.

    Returns None if the hourly series is unavailable. UV and air quality
    degrade to None individually rather than failing the whole call.
    """
    import urllib.request
    from datetime import datetime, timedelta, timezone

    lat, lon = LATITUDE, LONGITUDE
    tz = _timezone_for(location)
    if location:
        coords = geocode_location(location)
        if coords:
            lat, lon = coords
        else:
            tz = _home_timezone()   # fell back to home coords, so home's zone

    today = datetime.now().date()
    if date:
        try:
            target = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return None
    else:
        target = today

    day_offset = (target - today).days
    if day_offset < 0 or day_offset > 6:
        return None
    # One day of slack: with `timezone=auto` the series is indexed in the
    # DESTINATION's local dates, which can already be a day ahead of this
    # machine's. Asking for exactly day_offset+1 days would then not contain
    # the target day at all.
    forecast_days = min(day_offset + 2, 8)
    target_prefix = target.strftime("%Y-%m-%d")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,apparent_temperature,"
        "precipitation_probability,wind_speed_10m"
        "&daily=uv_index_max,sunrise,sunset"
        "&temperature_unit=fahrenheit&wind_speed_unit=mph"
        f"&timezone={tz}&forecast_days={forecast_days}"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Weather context fetch failed: {e}", file=sys.stderr)
        return None

    # The arrays are indexed in whatever zone we asked for, and `auto` means
    # the destination's. Re-derive "today" in THAT zone before slicing: a
    # machine-local date picks the wrong row once the destination's calendar
    # day has rolled past home's, and far enough east it matches no row at all
    # — the whole context block then vanished, and run.sh treats a missing
    # context as non-fatal, so it went out silently short.
    if not date:
        offset_s = data.get("utc_offset_seconds")
        if isinstance(offset_s, (int, float)):
            target_prefix = (
                datetime.now(timezone.utc) + timedelta(seconds=offset_s)
            ).strftime("%Y-%m-%d")

    hourly = data.get("hourly") or {}
    times = hourly.get("time") or []
    if not times:
        return None

    temps = hourly.get("temperature_2m") or []
    feels = hourly.get("apparent_temperature") or []
    rain  = hourly.get("precipitation_probability") or []
    wind  = hourly.get("wind_speed_10m") or []

    def at(seq, i, rounded=True):
        if i >= len(seq) or seq[i] is None:
            return None
        return round(seq[i]) if rounded else seq[i]

    hours = []
    for i, stamp in enumerate(times):
        if stamp[:10] != target_prefix:
            continue
        if not (start_hour <= int(stamp[11:13]) <= end_hour):
            continue
        hours.append({
            "t":     stamp[11:16],
            "temp":  at(temps, i),
            "feels": at(feels, i),
            "rain":  at(rain, i, rounded=False),
            "wind":  at(wind, i),
        })

    if not hours:
        return None

    seen_temps = [h["temp"] for h in hours if h["temp"] is not None]
    seen_rain  = [h["rain"] for h in hours if h["rain"] is not None]

    daily = data.get("daily") or {}
    # Locate the day by VALUE, not by an offset counted from the machine's
    # date. Indexing positionally returned a different day's UV, sunrise and
    # sunset than the `hours` in the same dict — two days stitched into one
    # object with nothing marking the seam.
    daily_days = daily.get("time") or []
    try:
        target_idx = daily_days.index(target_prefix)
    except ValueError:
        target_idx = None

    def at_target(key):
        seq = daily.get(key) or []
        if target_idx is None or target_idx >= len(seq):
            return None
        return seq[target_idx]

    uv = at_target("uv_index_max")
    sunrise, sunset = at_target("sunrise"), at_target("sunset")

    return {
        "window": f"{start_hour:02d}:00-{end_hour:02d}:00",
        "hours": hours,
        "summary": {
            "temp_min": min(seen_temps) if seen_temps else None,
            "temp_max": max(seen_temps) if seen_temps else None,
            "swing":    (max(seen_temps) - min(seen_temps)) if seen_temps else None,
            "rain_max": max(seen_rain) if seen_rain else None,
        },
        "uv": ({"index_max": uv, "band": _band(uv, UV_BANDS, "extreme")}
               if isinstance(uv, (int, float)) else None),
        "sun": {
            "sunrise": sunrise[11:16] if sunrise else None,
            "sunset":  sunset[11:16] if sunset else None,
        },
        "air": _fetch_air_quality(lat, lon, tz),
    }


if __name__ == "__main__":
    print("Fetching Irvine weather...")
    result = get_weather_briefing()
    print(result or "Failed to fetch weather")
