from __future__ import annotations

import json
import socket
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .astronomy import dark_window_narrative, julian_day, moon_altitude, moon_interference_score, moon_phase, moonrise_moonset
from .models import SamplePoint
from .scoring import best_true_window, classify_cloud_stability, derive_night_window, deterministic_value, is_usable_observation_hour, longest_true_streak, moon_factor, safe_float, sample_stddev, segment_name

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
# Open-Meteo hourly forecast window (days from today)

OPEN_METEO_HOURLY_WINDOW_DAYS = 16

_MODEL_RATE_LIMIT_LOCK = threading.Lock()
_MODEL_NEXT_ALLOWED_AT: Dict[str, float] = {}
_SSL_CONTEXT: Optional[ssl.SSLContext] = None


def _model_rate_limit_interval_s(model: Optional[str], scope_mode: Optional[str]) -> float:
    if scope_mode == "national":
        return 0.35
    if scope_mode == "point_check":
        return 1.25
    return 0.9



def _apply_model_rate_limit(model: Optional[str], scope_mode: Optional[str]) -> None:
    model_key = model or "default"
    interval = _model_rate_limit_interval_s(model_key, scope_mode)
    with _MODEL_RATE_LIMIT_LOCK:
        now = time.monotonic()
        next_allowed = _MODEL_NEXT_ALLOWED_AT.get(model_key, now)
        wait_s = max(0.0, next_allowed - now)
        _MODEL_NEXT_ALLOWED_AT[model_key] = max(next_allowed, now) + interval
    if wait_s > 0:
        time.sleep(wait_s)



def _bump_model_cooldown(model: Optional[str], wait_s: float) -> None:
    model_key = model or "default"
    with _MODEL_RATE_LIMIT_LOCK:
        now = time.monotonic()
        current = _MODEL_NEXT_ALLOWED_AT.get(model_key, now)
        _MODEL_NEXT_ALLOWED_AT[model_key] = max(current, now) + max(wait_s, 0.0)



def _retry_after_seconds(exc: Exception) -> Optional[float]:
    if not isinstance(exc, urllib.error.HTTPError):
        return None
    headers = getattr(exc, "headers", None)
    if not headers:
        return None
    retry_after = headers.get("Retry-After")
    if not retry_after:
        return None
    try:
        return float(retry_after)
    except Exception:
        return None

def _extract_first_json_object(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        raise ValueError("Empty weather payload")
    start = text.find("{")
    if start < 0:
        raise ValueError("No JSON object found in weather payload")
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i+1])
    raise ValueError("Incomplete JSON object in weather payload")



def _is_daily_limit_exceeded_message(message: Optional[str]) -> bool:
    msg = (message or "").lower()
    return "daily api request limit exceeded" in msg or "please try again tomorrow" in msg



def classify_fetch_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code == 429 and _is_daily_limit_exceeded_message(str(exc)):
            return "daily_limit_exceeded"
        return f"http_{exc.code}"
    if isinstance(exc, urllib.error.URLError):
        reason = getattr(exc, "reason", None)
        if isinstance(reason, OSError) and "SSL" in reason.__class__.__name__.upper():
            return "ssl"
        if isinstance(reason, socket.timeout):
            return "timeout"
        return "url"
    if isinstance(exc, socket.timeout):
        return "timeout"
    if isinstance(exc, OSError) and "SSL" in exc.__class__.__name__.upper():
        return "ssl"
    if isinstance(exc, ValueError):
        return "parse"
    return exc.__class__.__name__.lower()



def _build_ssl_context() -> ssl.SSLContext:
    global _SSL_CONTEXT
    if _SSL_CONTEXT is not None:
        return _SSL_CONTEXT
    ctx = ssl.create_default_context()
    try:
        import certifi  # type: ignore
        ctx.load_verify_locations(cafile=certifi.where())
    except Exception:
        pass
    _SSL_CONTEXT = ctx
    return ctx



def _request_timeout_s(scope_mode: Optional[str]) -> float:
    if scope_mode == "national":
        return 12.0
    if scope_mode == "point_check":
        return 20.0
    return 16.0



def _retry_budget(scope_mode: Optional[str], explicit_max_retries: Optional[int]) -> int:
    if explicit_max_retries is not None:
        return max(0, explicit_max_retries)
    if scope_mode == "national":
        return 1
    if scope_mode == "point_check":
        return 2
    return 2



def _fetch_json_via_urllib(url: str, timeout_s: float) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "go-stargazing/1.x (+Open-Meteo client)",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s, context=_build_ssl_context()) as resp:
            return _extract_first_json_object(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        reason = body.strip()[:400]
        raise urllib.error.HTTPError(
            exc.url,
            exc.code,
            f"{exc.reason}: {reason}" if reason else str(exc.reason),
            exc.headers,
            None,
        )



def fetch_openmeteo_payload(point: SamplePoint, target_dt: datetime, timezone: str, model: Optional[str] = None, max_retries: Optional[int] = None, retry_delay_s: float = 0.8, scope_mode: Optional[str] = None) -> dict:
    # Query target date + next date, so the night window can include next-morning hours.
    end_date = (target_dt.date() + timedelta(days=1)).isoformat()
    params = {
        "latitude": point.lat,
        "longitude": point.lng,
        # Open-Meteo forecast currently rejects `cloud_base_height` on this endpoint.
        # Use low/mid/high cloud-cover layers instead; they are supported and are more
        # honest than faking cloud-base height. Terrain handling happens downstream.
        "hourly": "cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,relative_humidity_2m,visibility,wind_speed_10m,wind_gusts_10m,temperature_2m,dew_point_2m,precipitation,weather_code",
        "timezone": timezone,
        "start_date": target_dt.date().isoformat(),
        "end_date": end_date,
    }
    if model:
        params["models"] = model
    url = OPEN_METEO_FORECAST_URL + "?" + urllib.parse.urlencode(params)

    last_exc: Optional[Exception] = None
    retry_budget = _retry_budget(scope_mode, max_retries)
    total_attempts = max(1, retry_budget + 1)
    timeout_s = _request_timeout_s(scope_mode)
    for attempt in range(total_attempts):
        point.fetch_attempts = attempt + 1
        _apply_model_rate_limit(model, scope_mode)
        try:
            payload = _fetch_json_via_urllib(url, timeout_s=timeout_s)
            point.fetch_recovered = attempt > 0
            point.fetch_error_type = None
            point.fetch_error_message = None
            return payload
        except Exception as exc:
            last_exc = exc
            point.fetch_error_type = classify_fetch_error(exc)
            point.fetch_error_message = str(exc)[:240]
            if point.fetch_error_type == "daily_limit_exceeded":
                _bump_model_cooldown(model, 12 * 3600)
                raise last_exc
            if attempt < total_attempts - 1:
                if point.fetch_error_type == "http_429":
                    retry_after_s = _retry_after_seconds(exc)
                    wait_s = max(retry_delay_s * (2 ** attempt), retry_after_s or 0.0, 2.0)
                    _bump_model_cooldown(model, wait_s)
                    time.sleep(wait_s)
                else:
                    time.sleep(retry_delay_s * (attempt + 1))
    raise last_exc



def hourly_index(payload: dict, target_dt: datetime) -> int:
    times = payload.get("hourly", {}).get("time", [])
    if not times:
        raise RuntimeError("No hourly timeline")
    target_key = target_dt.replace(minute=0, second=0, microsecond=0).isoformat(timespec="minutes")
    try:
        return times.index(target_key)
    except ValueError:
        parsed = [datetime.fromisoformat(t) for t in times]
        target_hour = target_dt.replace(minute=0, second=0, microsecond=0)
        return min(range(len(parsed)), key=lambda i: abs((parsed[i] - target_hour).total_seconds()))



def hydrate_mock_weather(points: List[SamplePoint], target_dt: datetime, mode: str) -> None:
    """Mock weather: single-hour values + nightly aggregates."""
    for p in points:
        base = f"{p.province}:{p.lat:.4f}:{p.lng:.4f}:{target_dt.date().isoformat()}"
        # Simulate a night window of target evening → next morning (18:00-06:00)
        night_hours = 13
        night_cloud_vals = [deterministic_value(f"{base}:cloud:h{h}", 0, 60) for h in range(night_hours)]
        night_hum_vals = [deterministic_value(f"{base}:humidity:h{h}", 20, 80) for h in range(night_hours)]
        night_vis_vals = [deterministic_value(f"{base}:vis:h{h}", 15000, 25000) for h in range(night_hours)]
        night_wind_vals = [deterministic_value(f"{base}:wind:h{h}", 0.5, 10) for h in range(night_hours)]
        night_temp_vals = [deterministic_value(f"{base}:temp:h{h}", -8, 8) for h in range(night_hours)]
        night_gust_vals = [w + deterministic_value(f"{base}:gust:h{h}", 0.5, 6.0) for h, w in enumerate(night_wind_vals)]
        night_dew_vals = [t - deterministic_value(f"{base}:dewspread:h{h}", 1.0, 6.0) for h, t in enumerate(night_temp_vals)]

        # Single-hour: use hour matching target_dt (approx 23:00, i.e. 18:00 + 5h)
        snapshot_idx = min(5, night_hours - 1)
        p.cloud_cover = night_cloud_vals[snapshot_idx]
        p.humidity = night_hum_vals[snapshot_idx]
        p.visibility_m = night_vis_vals[snapshot_idx]
        p.wind_speed = night_wind_vals[snapshot_idx]

        # Nightly aggregates
        p.night_avg_cloud = round(sum(night_cloud_vals) / len(night_cloud_vals), 1)
        p.night_worst_cloud = max(night_cloud_vals)
        p.night_avg_humidity = round(sum(night_hum_vals) / len(night_hum_vals), 1)
        p.night_avg_visibility = round(sum(night_vis_vals) / len(night_vis_vals), 0)
        p.night_avg_wind = round(sum(night_wind_vals) / len(night_wind_vals), 1)
        p.night_avg_temperature = round(sum(night_temp_vals) / len(night_temp_vals), 1)
        p.night_max_gust = round(max(night_gust_vals), 1)
        p.night_avg_dew_point = round(sum(night_dew_vals) / len(night_dew_vals), 1)
        p.elevation_m = deterministic_value(base + ":elevation", 1500, 4200)

        # Moon interference (mock: based on moon phase)
        illum, _ = moon_phase(julian_day(target_dt))
        mock_moon_alt = deterministic_value(base + ":moon_alt", -30, 60)
        p.moon_interference = moon_interference_score(illum, mock_moon_alt)
        mock_usable = [is_usable_observation_hour(c, w, p.moon_interference) for c, w in zip(night_cloud_vals, night_wind_vals)]
        p.usable_hours = float(sum(1 for x in mock_usable if x))
        p.longest_usable_streak_hours = float(longest_true_streak(mock_usable))
        mock_times = [(target_dt.replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(hours=h)).isoformat(timespec="minutes") for h in range(night_hours)]
        mock_rel_hours = [18 + h for h in range(night_hours)]
        p.best_window_start, p.best_window_end, p.best_window_segment = best_true_window(mock_times, mock_usable, mock_rel_hours)
        p.cloud_stddev = round(sample_stddev(night_cloud_vals) or 0.0, 1)
        p.cloud_stability = classify_cloud_stability(p.cloud_stddev)
        worst_idx = max(range(len(night_cloud_vals)), key=lambda i: night_cloud_vals[i])
        p.worst_cloud_segment = segment_name(mock_rel_hours[worst_idx])
        p.moon_factor = moon_factor(target_dt, mode)
        p.weather_source = "mock"



def fetch_point_weather(point: SamplePoint, target_dt: datetime, timezone: str, mode: str, model: Optional[str] = None, scope_mode: Optional[str] = None) -> SamplePoint:
    """Fetch weather for a point, compute single-hour snapshot + nightly aggregation."""
    payload = fetch_openmeteo_payload(point, target_dt, timezone, model=model, scope_mode=scope_mode)
    point.weather_model = model or "ecmwf_ifs"
    hourly = payload.get("hourly", {})
    times = hourly.get("time", [])

    # Single-hour snapshot (closest to target time)
    idx = hourly_index(payload, target_dt)
    point.cloud_cover = safe_float(hourly.get("cloud_cover", [None])[idx]) if hourly.get("cloud_cover") else None
    point.humidity = safe_float(hourly.get("relative_humidity_2m", [None])[idx]) if hourly.get("relative_humidity_2m") else None
    point.visibility_m = safe_float(hourly.get("visibility", [None])[idx]) if hourly.get("visibility") else None
    point.wind_speed = safe_float(hourly.get("wind_speed_10m", [None])[idx]) if hourly.get("wind_speed_10m") else None
    point.elevation_m = safe_float(payload.get("elevation"))

    # ---- Nightly aggregation over astronomical twilight window ----
    window = derive_night_window(point.lat, point.lng, target_dt.date())
    if window is not None:
        start_h, end_h = window
        # Collect hourly indices within the night window
        night_cloud, night_hum, night_vis, night_wind = [], [], [], []
        night_temp, night_gust = [], []
        night_cloud_low, night_cloud_mid, night_cloud_high = [], [], []
        night_dew, night_precip = [], []
        night_weather_codes = []
        night_moon_scores = []
        usable_flags = []
        night_times = []
        night_rel_hours = []
        # Build list of (hour_index, hour_local) from times
        for i, t_str in enumerate(times):
            # Open-Meteo returns times already in the specified timezone (Asia/Shanghai)
            t = datetime.fromisoformat(t_str)
            # Convert the timestamp into a relative hour index for the target night:
            # target date 18:00 => 18, next day 02:00 => 26, etc.
            day_delta = (t.date() - target_dt.date()).days
            if day_delta not in (0, 1):
                continue
            rel_hour = day_delta * 24 + t.hour
            if not (start_h <= rel_hour <= end_h):
                continue
            cc = hourly.get("cloud_cover", [None])[i] if hourly.get("cloud_cover") else None
            rh = hourly.get("relative_humidity_2m", [None])[i] if hourly.get("relative_humidity_2m") else None
            vis = hourly.get("visibility", [None])[i] if hourly.get("visibility") else None
            ws = hourly.get("wind_speed_10m", [None])[i] if hourly.get("wind_speed_10m") else None
            gust = hourly.get("wind_gusts_10m", [None])[i] if hourly.get("wind_gusts_10m") else None
            temp = hourly.get("temperature_2m", [None])[i] if hourly.get("temperature_2m") else None
            low = hourly.get("cloud_cover_low", [None])[i] if hourly.get("cloud_cover_low") else None
            mid = hourly.get("cloud_cover_mid", [None])[i] if hourly.get("cloud_cover_mid") else None
            high = hourly.get("cloud_cover_high", [None])[i] if hourly.get("cloud_cover_high") else None
            dew = hourly.get("dew_point_2m", [None])[i] if hourly.get("dew_point_2m") else None
            precip = hourly.get("precipitation", [None])[i] if hourly.get("precipitation") else None
            wcode = hourly.get("weather_code", [None])[i] if hourly.get("weather_code") else None
            night_times.append(t.isoformat(timespec="minutes"))
            night_rel_hours.append(rel_hour)
            if cc is not None:
                night_cloud.append(cc)
            if rh is not None:
                night_hum.append(rh)
            if vis is not None:
                night_vis.append(vis)
            if ws is not None:
                night_wind.append(ws)
            if gust is not None:
                night_gust.append(gust)
            if temp is not None:
                night_temp.append(temp)
            if low is not None:
                night_cloud_low.append(low)
            if mid is not None:
                night_cloud_mid.append(mid)
            if high is not None:
                night_cloud_high.append(high)
            if dew is not None:
                night_dew.append(dew)
            if precip is not None:
                night_precip.append(precip)
            if wcode is not None:
                night_weather_codes.append(wcode)
            # Moon interference at this hour
            jd = julian_day(t)
            illum, _ = moon_phase(jd)
            moon_alt = moon_altitude(jd, point.lat, point.lng)
            interf = moon_interference_score(illum, moon_alt)
            night_moon_scores.append(interf)
            usable_flags.append(is_usable_observation_hour(cc, ws, interf))

        if night_cloud:
            point.night_avg_cloud = sum(night_cloud) / len(night_cloud)
            point.night_worst_cloud = max(night_cloud)
            point.night_avg_humidity = sum(night_hum) / len(night_hum) if night_hum else None
            point.night_avg_visibility = sum(night_vis) / len(night_vis) if night_vis else None
            point.night_avg_wind = sum(night_wind) / len(night_wind) if night_wind else None
            point.night_avg_temperature = round(sum(night_temp) / len(night_temp), 1) if night_temp else None
            point.night_max_gust = round(max(night_gust), 1) if night_gust else None
            point.night_avg_cloud_low = round(sum(night_cloud_low) / len(night_cloud_low), 1) if night_cloud_low else None
            point.night_avg_cloud_mid = round(sum(night_cloud_mid) / len(night_cloud_mid), 1) if night_cloud_mid else None
            point.night_avg_cloud_high = round(sum(night_cloud_high) / len(night_cloud_high), 1) if night_cloud_high else None
            point.night_avg_dew_point = round(sum(night_dew) / len(night_dew), 1) if night_dew else None
            point.night_max_precip = max(night_precip) if night_precip else None
            point.night_weather_codes = night_weather_codes
            point.moon_interference = sum(night_moon_scores) / len(night_moon_scores) if night_moon_scores else 100.0
            point.usable_hours = float(sum(1 for x in usable_flags if x))
            point.longest_usable_streak_hours = float(longest_true_streak(usable_flags))
            point.best_window_start, point.best_window_end, point.best_window_segment = best_true_window(night_times, usable_flags, night_rel_hours)
            point.cloud_stddev = round(sample_stddev(night_cloud) or 0.0, 1)
            point.cloud_stability = classify_cloud_stability(point.cloud_stddev)
            worst_idx = max(range(len(night_cloud)), key=lambda i: night_cloud[i])
            point.worst_cloud_segment = segment_name(night_rel_hours[worst_idx])
            # Moonrise/moonset for dark-window computation
            try:
                from astronomy import moonrise_moonset, dark_window_narrative
                tz_offset = 8.0  # Asia/Shanghai
                mr, ms = moonrise_moonset(point.lat, point.lng, target_dt.date(), tz_offset)
                if mr and ms:
                    point.moonrise = mr.strftime("%H:%M")
                    point.moonset = ms.strftime("%H:%M")
                elif mr and not ms:
                    point.moonrise = mr.strftime("%H:%M")
                    point.moonset = None
                elif ms and not mr:
                    point.moonrise = None
                    point.moonset = ms.strftime("%H:%M")
                if mr and ms:
                    dw_desc, dw_note = dark_window_narrative(
                        point.lat, point.lng, target_dt.date(),
                        int(point.best_window_start.split(":")[0]) if point.best_window_start else 0,
                        int(point.best_window_end.split(":")[0]) if point.best_window_end else 24,
                        tz_offset)
                    point.moon_dark_window = dw_desc
            except Exception:
                pass  # astronomy is optional for core scoring
        else:
            # No night hours found → use single-hour values as fallback
            point.night_avg_cloud = point.cloud_cover
            point.night_worst_cloud = point.cloud_cover
            point.night_avg_humidity = point.humidity
            point.night_avg_visibility = point.visibility_m
            point.night_avg_wind = point.wind_speed
            point.night_avg_temperature = None
            point.night_max_gust = None
            point.night_avg_cloud_low = None
            point.night_avg_cloud_mid = None
            point.night_avg_cloud_high = None
            point.moon_interference = 50.0  # uncertain
            point.usable_hours = 0.0
            point.longest_usable_streak_hours = 0.0
            point.best_window_start = None
            point.best_window_end = None
            point.best_window_segment = None
            point.cloud_stddev = None
            point.cloud_stability = None
            point.worst_cloud_segment = None

    point.moon_factor = moon_factor(target_dt, mode)
    point.weather_source = "openmeteo-http"
    return point



def _mark_fetch_failure(point: SamplePoint, model: Optional[str], exc: Exception) -> None:
    point.weather_model = model or "ecmwf_ifs"
    point.weather_source = "fetch_error"
    point.fetch_error_type = classify_fetch_error(exc)
    point.fetch_error_message = str(exc)[:240]
    point.cloud_cover = None
    point.humidity = None
    point.visibility_m = None
    point.wind_speed = None
    point.night_avg_cloud = None
    point.night_worst_cloud = None
    point.night_avg_humidity = None
    point.night_avg_visibility = None
    point.night_avg_wind = None
    point.night_avg_temperature = None
    point.night_max_gust = None
    point.moon_interference = None
    point.usable_hours = 0.0
    point.longest_usable_streak_hours = 0.0
    point.best_window_start = None
    point.best_window_end = None
    point.best_window_segment = None
    point.cloud_stddev = None
    point.cloud_stability = None
    point.worst_cloud_segment = None




def _copy_fetch_result(original: SamplePoint, updated: SamplePoint) -> None:
    original.weather_model = updated.weather_model
    original.cloud_cover = updated.cloud_cover
    original.humidity = updated.humidity
    original.visibility_m = updated.visibility_m
    original.wind_speed = updated.wind_speed
    original.elevation_m = updated.elevation_m
    original.night_avg_cloud = updated.night_avg_cloud
    original.night_worst_cloud = updated.night_worst_cloud
    original.night_avg_humidity = updated.night_avg_humidity
    original.night_avg_visibility = updated.night_avg_visibility
    original.night_avg_wind = updated.night_avg_wind
    original.night_avg_temperature = updated.night_avg_temperature
    original.night_max_gust = updated.night_max_gust
    original.moon_interference = updated.moon_interference
    original.usable_hours = updated.usable_hours
    original.longest_usable_streak_hours = updated.longest_usable_streak_hours
    original.best_window_start = updated.best_window_start
    original.best_window_end = updated.best_window_end
    original.best_window_segment = updated.best_window_segment
    original.cloud_stddev = updated.cloud_stddev
    original.cloud_stability = updated.cloud_stability
    original.worst_cloud_segment = updated.worst_cloud_segment
    original.moon_factor = updated.moon_factor
    original.weather_source = updated.weather_source
    original.fetch_attempts = updated.fetch_attempts
    original.fetch_recovered = updated.fetch_recovered
    original.fetch_error_type = updated.fetch_error_type
    original.fetch_error_message = updated.fetch_error_message




def hydrate_real_weather(points: List[SamplePoint], target_dt: datetime, timezone: str, mode: str, max_workers: int, model: Optional[str] = None, scope_mode: Optional[str] = None) -> None:
    if scope_mode == "national":
        primary_workers = max(1, min(max_workers, 4))
        retry_workers = 1 if len(points) <= 12 else min(2, primary_workers)
    else:
        # 单区复核 / 小范围查询：低频、串行，避免把限流打满
        primary_workers = 1
        retry_workers = 1
    failed_points: List[SamplePoint] = []

    with ThreadPoolExecutor(max_workers=primary_workers) as ex:
        future_map = {ex.submit(fetch_point_weather, p, target_dt, timezone, mode, model, scope_mode): p for p in points}
        for fut in as_completed(future_map):
            original = future_map[fut]
            try:
                updated = fut.result()
            except Exception as exc:
                failed_points.append(original)
                _mark_fetch_failure(original, model, exc)
                continue
            _copy_fetch_result(original, updated)

    if not failed_points:
        return

    time.sleep(2.0 if any((p.fetch_error_type == 'http_429') for p in failed_points) else 0.8)
    with ThreadPoolExecutor(max_workers=retry_workers) as ex:
        future_map = {ex.submit(fetch_point_weather, p, target_dt, timezone, mode, model, scope_mode): p for p in failed_points}
        for fut in as_completed(future_map):
            original = future_map[fut]
            try:
                updated = fut.result()
            except Exception as exc:
                _mark_fetch_failure(original, model, exc)
                continue
            _copy_fetch_result(original, updated)



def hydrate_weather(points: List[SamplePoint], real_weather: bool, target_dt: datetime, timezone: str, mode: str, max_workers: int, model: Optional[str] = None, scope_mode: Optional[str] = None) -> None:
    if real_weather:
        hydrate_real_weather(points, target_dt, timezone, mode, max_workers=max_workers, model=model, scope_mode=scope_mode)
    else:
        hydrate_mock_weather(points, target_dt, mode)
