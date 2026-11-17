#!/usr/bin/env python3
"""
import os
Reach weather connector — consolidated NWS + SPC + METAR + Open-Meteo.

Wraps the data-tier tools from the hermes-weather-plugin into a single
Reach source so callers don't need to chain noaa_nws → open_meteo → SPC.

Actions:
  conditions   Current observed conditions at lat/lon (NWS ASOS)
  forecast     7-day or hourly NWS forecast
  alerts       Active NWS warnings/watches/advisories (by point or state)
  metar        Raw + decoded METAR for an ICAO station
  brief        Conditions + 3-period forecast + alert count (one-call overview)
  global       Current weather via Open-Meteo (works worldwide)
  severe       SPC Day 1 categorical outlook + active watches

All actions are pure Python + requests. No binary/Rust dependencies.
"""

import json
import logging
import sys
from typing import Optional

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests is required: pip install requests"}), file=sys.stderr)
    sys.exit(1)

logger = logging.getLogger(__name__)

_SESSION = requests.Session()
_SESSION.headers.update({
    "User-Agent": "ocas-reach/3.0 (os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com"))",
    "Accept": "application/geo+json,application/json",
})
_TIMEOUT = 30


def _get(url: str, params: dict = None) -> dict:
    resp = _SESSION.get(url, params=params, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _nws_resolve(lat: float, lon: float) -> dict:
    """Resolve lat/lon to NWS gridpoint + station metadata."""
    data = _get(f"https://api.weather.gov/points/{lat},{lon}")
    return data.get("properties", {})


def _val(props: dict, key: str):
    """Extract value from NWS observation property (handles nested {value, unitCode})."""
    v = props.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v


# ---------------------------------------------------------------------------
# NWS: conditions
# ---------------------------------------------------------------------------

def action_conditions(params: dict) -> dict:
    lat = float(params["lat"])
    lon = float(params["lon"])
    point = _nws_resolve(lat, lon)
    stations_url = point.get("observationStations", "")
    if not stations_url:
        return {"error": "No observation stations found"}
    stations = _get(stations_url)
    features = stations.get("features", [])
    if not features:
        return {"error": "No observation stations returned"}
    station = features[0]
    station_id = station["properties"]["stationIdentifier"]
    obs = _get(f"https://api.weather.gov/stations/{station_id}/observations/latest")
    props = obs.get("properties", {})
    return {
        "station": station_id,
        "station_name": station["properties"].get("name", ""),
        "timestamp": props.get("timestamp"),
        "temperature_c": _val(props, "temperature"),
        "dewpoint_c": _val(props, "dewpoint"),
        "wind_speed_kmh": _val(props, "windSpeed"),
        "wind_direction_deg": _val(props, "windDirection"),
        "wind_gust_kmh": _val(props, "windGust"),
        "barometric_pressure_pa": _val(props, "barometricPressure"),
        "visibility_m": _val(props, "visibility"),
        "text_description": props.get("textDescription", ""),
        "raw_metar": props.get("rawMessage", ""),
    }


# ---------------------------------------------------------------------------
# NWS: forecast
# ---------------------------------------------------------------------------

def action_forecast(params: dict) -> dict:
    lat = float(params["lat"])
    lon = float(params["lon"])
    hourly = params.get("hourly", False)
    if isinstance(hourly, str):
        hourly = hourly.lower() in ("true", "1", "yes")
    point = _nws_resolve(lat, lon)
    url = point["forecastHourly"] if hourly else point["forecast"]
    data = _get(url)
    periods = data.get("properties", {}).get("periods", [])
    limit = 24 if hourly else 14
    result = []
    for p in periods[:limit]:
        result.append({
            "name": p.get("name", ""),
            "start": p.get("startTime"),
            "end": p.get("endTime"),
            "temperature": p.get("temperature"),
            "temperature_unit": p.get("temperatureUnit"),
            "wind_speed": p.get("windSpeed"),
            "wind_direction": p.get("windDirection"),
            "short_forecast": p.get("shortForecast"),
            "detailed_forecast": p.get("detailedForecast", ""),
            "precip_chance": (p.get("probabilityOfPrecipitation") or {}).get("value"),
        })
    return {"periods": result, "location": {"lat": lat, "lon": lon}}


# ---------------------------------------------------------------------------
# NWS: alerts
# ---------------------------------------------------------------------------

def action_alerts(params: dict) -> dict:
    state = params.get("state")
    lat = params.get("lat")
    lon = params.get("lon")
    req_params = {"status": "actual", "message_type": "alert"}
    if state:
        req_params["area"] = state.upper()
    elif lat is not None and lon is not None:
        req_params["point"] = f"{lat},{lon}"
    else:
        return {"error": "Provide lat+lon or state"}
    data = _get("https://api.weather.gov/alerts/active", params=req_params)
    alerts = []
    for f in data.get("features", []):
        p = f.get("properties", {})
        alerts.append({
            "event": p.get("event"),
            "severity": p.get("severity"),
            "urgency": p.get("urgency"),
            "certainty": p.get("certainty"),
            "headline": p.get("headline"),
            "description": (p.get("description") or "")[:500],
            "onset": p.get("onset"),
            "expires": p.get("expires"),
            "sender_name": p.get("senderName"),
            "area_desc": p.get("areaDesc"),
        })
    return {"count": len(alerts), "alerts": alerts}


# ---------------------------------------------------------------------------
# METAR (aviationweather.gov)
# ---------------------------------------------------------------------------

def action_metar(params: dict) -> dict:
    station = params["station"].upper()
    data = _get("https://aviationweather.gov/api/data/metar", params={"ids": station, "format": "json"})
    if not data:
        return {"error": f"No METAR for {station}"}
    obs = data[0] if isinstance(data, list) else data
    return {
        "station": station,
        "raw": obs.get("rawOb", ""),
        "temperature_c": obs.get("temp"),
        "dewpoint_c": obs.get("dewp"),
        "wind_dir_deg": obs.get("wdir"),
        "wind_speed_kt": obs.get("wspd"),
        "wind_gust_kt": obs.get("wgst"),
        "visibility_mi": obs.get("visib"),
        "altimeter_inhg": obs.get("altim"),
        "flight_category": obs.get("fltcat"),
        "clouds": obs.get("clouds", []),
        "observation_time": obs.get("reportTime"),
    }


# ---------------------------------------------------------------------------
# Brief: conditions + forecast + alerts in one call
# ---------------------------------------------------------------------------

def action_brief(params: dict) -> dict:
    lat = float(params["lat"])
    lon = float(params["lon"])
    conditions = action_conditions({"lat": lat, "lon": lon})
    if "error" in conditions:
        return conditions
    forecast = action_forecast({"lat": lat, "lon": lon})
    alerts = action_alerts({"lat": lat, "lon": lon})
    if "error" in alerts:
        alerts = {"count": 0, "alerts": []}
    return {
        "conditions": conditions,
        "forecast_periods": forecast.get("periods", [])[:3],
        "alert_count": alerts.get("count", 0),
        "alerts_summary": [a.get("headline") for a in alerts.get("alerts", [])[:3]],
        "location": {"lat": lat, "lon": lon},
    }


# ---------------------------------------------------------------------------
# Open-Meteo: global weather
# ---------------------------------------------------------------------------

def action_global(params: dict) -> dict:
    lat = float(params["lat"])
    lon = float(params["lon"])
    units = params.get("units", "us")  # us or metric
    temp_unit = "fahrenheit" if units == "us" else "celsius"
    wind_unit = "mph" if units == "us" else "kmh"
    api_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                   "precipitation,weather_code,wind_speed_10m,wind_direction_10m,"
                   "wind_gusts_10m,surface_pressure",
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit,
    }
    data = _get("https://api.open-meteo.com/v1/forecast", params=api_params)
    return {
        "current": data.get("current", {}),
        "units": {
            "temperature": "°F" if units == "us" else "°C",
            "wind": "mph" if units == "us" else "km/h",
            "pressure": "hPa",
        },
        "location": {"lat": lat, "lon": lon},
    }


# ---------------------------------------------------------------------------
# SPC: severe weather outlook
# ---------------------------------------------------------------------------

def action_severe(params: dict) -> dict:
    state = params.get("state")
    # Day 1 categorical outlook GeoJSON
    outlook = _get("https://www.spc.noaa.gov/products/outlook/day1otlk_cat.nolyr.geojson")
    categories = []
    for f in outlook.get("features", []):
        props = f.get("properties", {})
        categories.append({
            "label": props.get("LABEL", ""),
            "label2": props.get("LABEL2", ""),
            "stroke": props.get("stroke", ""),
        })

    # Active watches
    try:
        watches_data = _get("https://www.spc.noaa.gov/products/watch/activeWW.json")
        watches = watches_data if isinstance(watches_data, list) else []
    except Exception:
        watches = []

    result = {
        "day1_outlook": categories,
        "active_watches": watches,
    }

    # If state filter requested, reduce outlook to matching entries
    if state:
        state_upper = state.upper()
        # NWS alerts filtered by state
        alerts_result = action_alerts({"state": state_upper})
        result["state_alerts"] = alerts_result

    return result


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

ACTION_MAP = {
    "conditions": action_conditions,
    "forecast": action_forecast,
    "alerts": action_alerts,
    "metar": action_metar,
    "brief": action_brief,
    "global": action_global,
    "severe": action_severe,
}


def query(action: str, params: dict, auth: dict = None) -> dict:
    """Entry point called by reach.py for custom sources."""
    handler = ACTION_MAP.get(action)
    if handler is None:
        return {"error": f"Unknown action '{action}'. Valid: {', '.join(sorted(ACTION_MAP.keys()))}"}
    try:
        return handler(params)
    except requests.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text[:300]}", "action": action}
    except requests.ConnectionError as e:
        return {"error": f"Connection failed: {e}", "action": action}
    except Exception as e:
        logger.exception("weather query failed: %s %s", action, params)
        return {"error": f"{action} failed: {e}"}


# ---------------------------------------------------------------------------
# CLI usage (direct invocation for testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "query":
        print("Usage: weather.py query <action> [params_json]")
        print(f"Actions: {', '.join(sorted(ACTION_MAP.keys()))}")
        sys.exit(1)
    action = sys.argv[2]
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    result = query(action, params)
    print(json.dumps(result, indent=2, default=str))
