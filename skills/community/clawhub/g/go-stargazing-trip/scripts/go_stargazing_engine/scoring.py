from __future__ import annotations

import hashlib
import math
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from .astronomy import julian_day, moon_altitude, moon_interference_score, moon_phase, sunset_sunrise_times
from .models import SamplePoint

def deterministic_pct(seed_text: str) -> float:
    h = hashlib.md5(seed_text.encode()).hexdigest()
    return float(int(h[:8], 16) % 101)



def deterministic_value(seed_text: str, lower: float, upper: float) -> float:
    h = hashlib.md5(seed_text.encode()).hexdigest()
    ratio = (int(h[:8], 16) % 10000) / 10000.0
    return lower + (upper - lower) * ratio



def safe_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None



def moon_factor(target_dt: datetime, mode: str) -> float:
    day = target_dt.day
    cycle = ((day - 1) % 29) / 29.0
    illum = 1.0 - abs(cycle - 0.5) * 2
    return round((illum if mode == "moon" else 1 - illum) * 100, 2)



def classify_cloud(point: SamplePoint, mode: str) -> str:
    # Prefer nightly average cloud for coarse filtering; fall back to snapshot cloud_cover.
    c = point.night_avg_cloud if point.night_avg_cloud is not None else point.cloud_cover
    if c is None:
        return "drop"
    if mode == "moon":
        return "pass" if c <= 50 else "edge" if c <= 65 else "drop"
    return "pass" if c <= 35 else "edge" if c <= 50 else "drop"



def coarse_filter(points: Iterable[SamplePoint], mode: str) -> List[SamplePoint]:
    out: List[SamplePoint] = []
    for p in points:
        p.stage1_status = classify_cloud(p, mode)
        if p.stage1_status in {"pass", "edge"}:
            out.append(p)
    return out



def score_cloud(c: Optional[float]) -> float:
    return 0.0 if c is None else max(0.0, min(100.0, 100.0 - c * 1.6))



def score_humidity(h: Optional[float]) -> float:
    if h is None:
        return 0.0
    if h <= 40:
        return 100.0
    if h >= 95:
        return 0.0
    return max(0.0, 100.0 - (h - 40) / 55.0 * 100.0)



def score_visibility(v_m: Optional[float]) -> float:
    if v_m is None:
        return 0.0
    return max(0.0, min(100.0, (v_m / 1000.0) / 24.0 * 100.0))



def score_wind(w: Optional[float]) -> float:
    if w is None:
        return 0.0
    if w <= 2:
        return 100.0
    if w >= 12:
        return 0.0
    return max(0.0, 100.0 - (w - 2) / 10.0 * 100.0)



def is_usable_observation_hour(cloud: Optional[float], wind_kmh: Optional[float], moon_interference: Optional[float]) -> bool:
    """Heuristic for whether an hour is actually worth shooting.
    Designed for stargazing / milky-way style use.
    """
    if cloud is None:
        return False
    if cloud > 20:
        return False
    if wind_kmh is not None and wind_kmh > 28:
        return False
    if moon_interference is not None and moon_interference < 55:
        return False
    return True



def longest_true_streak(flags: List[bool]) -> int:
    best = cur = 0
    for x in flags:
        if x:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best



def sample_stddev(values: List[float]) -> Optional[float]:
    if not values:
        return None
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))



def classify_cloud_stability(stddev: Optional[float]) -> Optional[str]:
    if stddev is None:
        return None
    if stddev <= 10:
        return "stable"
    if stddev <= 20:
        return "mixed"
    return "volatile"



def segment_name(rel_hour: int) -> str:
    if rel_hour <= 22:
        return "前半夜"
    if rel_hour <= 26:
        return "中夜"
    return "后半夜"



def best_true_window(times: List[str], flags: List[bool], rel_hours: List[int]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    best_start = best_end = None
    best_len = cur_start = None
    cur_len = 0
    for i, ok in enumerate(flags):
        if ok:
            if cur_start is None:
                cur_start = i
                cur_len = 1
            else:
                cur_len += 1
            if best_len is None or cur_len > best_len:
                best_len = cur_len
                best_start = cur_start
                best_end = i
        else:
            cur_start = None
            cur_len = 0
    if best_start is None or best_end is None:
        return None, None, None

    # Use relative night hours instead of raw ISO timestamps, to avoid timezone/date rendering drift.
    start_hour = rel_hours[best_start] % 24
    end_hour = (rel_hours[best_end] + 1) % 24
    start_ts = f"{start_hour:02d}:00"
    end_ts = f"{end_hour:02d}:00"
    return start_ts, end_ts, segment_name(rel_hours[best_start])



def normalize_night_window(window: Optional[Tuple[int, int]]) -> Tuple[int, int]:
    """Normalize astronomy-derived window into a sane observation-night band.

    Expected semantic window is target evening through next morning, i.e. within [18, 30].
    Some astronomy calculations may return reversed or daytime-looking windows like (8, 17).
    In those cases, fall back to the agreed fixed observation band 18:00-06:00.
    """
    default_window = (18, 30)
    if window is None:
        return default_window
    start_h, end_h = window
    if end_h < start_h:
        end_h += 24
    if start_h < 16 or start_h > 23:
        return default_window
    if end_h <= start_h or end_h > 36:
        return default_window
    start_h = max(18, start_h)
    end_h = min(30, end_h)
    if end_h <= start_h:
        return default_window
    return start_h, end_h



def derive_night_window(latitude_deg: float, longitude_deg: float, target_date) -> Tuple[int, int]:
    """Derive the observation-night window from astronomical twilight datetimes.

    Sunset (civil twilignt at -18°) marks the START of the astronomical night.
    Sunrise marks the END (possibly on the next calendar day).
    """
    default_window = (18, 30)
    sunset_dt, sunrise_dt = sunset_sunrise_times(latitude_deg, longitude_deg, target_date, tz_offset_h=8.0, altitude_deg=-18.0)
    if sunset_dt is None or sunrise_dt is None:
        return default_window

    # Astronomical sunset is always the START of the observation window.
    # Sunrise is always the END; if it's same calendar day as sunset,
    # it must be the *next day's* sunrise → add one day.
    start_dt = sunset_dt
    end_dt = sunrise_dt
    if end_dt.date() <= start_dt.date():
        end_dt = end_dt + timedelta(days=1)

    start_h = (start_dt.date() - target_date).days * 24 + start_dt.hour
    end_h = (end_dt.date() - target_date).days * 24 + end_dt.hour
    return normalize_night_window((start_h, end_h))



def compute_final_score(point: SamplePoint, mode: str) -> None:
    """Score a point using nightly aggregated weather when available.
    Uses nightly avg cloud / worst cloud, falling back to single-hour values.
    Moon interference is incorporated as moonlight_score [0-100].
    """
    # Prefer nightly aggregation; fall back to single-hour snapshot
    cloud_for_scoring = point.night_avg_cloud if point.night_avg_cloud is not None else point.cloud_cover
    humidity_for_scoring = point.night_avg_humidity if point.night_avg_humidity is not None else point.humidity
    vis_for_scoring = point.night_avg_visibility if point.night_avg_visibility is not None else point.visibility_m
    wind_for_scoring = point.night_avg_wind if point.night_avg_wind is not None else point.wind_speed

    cloud = score_cloud(cloud_for_scoring)
    humidity = score_humidity(humidity_for_scoring)
    visibility = score_visibility(vis_for_scoring)
    wind = score_wind(wind_for_scoring)

    # Moon: use moonlight interference score if computed, else fallback
    if point.moon_interference is not None:
        # moon_interference: 0=strong interference, 100=no interference
        # Convert to moonlight_score [0-100] where 100=best
        moonlight_score = point.moon_interference
    else:
        moonlight_score = point.moon_factor or 0.0

    # moonlight_score: 0 = bright moon above horizon, 100 = no moonlight
    # For stargazing: less moonlight = better → moonlight_helps = (100 - moonlight_score)
    # For moon-viewing: moonlight helps scenic quality → moonlight_helps = moonlight_score
    if mode == "moon":
        weights = {"moon": 35, "cloud": 25, "visibility": 20, "humidity": 15, "wind": 5}
        moonlight_helps = moonlight_score
        total = moonlight_helps * 0.35 + cloud * 0.25 + visibility * 0.20 + humidity * 0.15 + wind * 0.05
    else:
        weights = {"cloud": 40, "humidity": 20, "visibility": 20, "moon": 15, "wind": 5}
        moonlight_helps = 100 - moonlight_score  # less moonlight = better for stargazing
        total = cloud * 0.40 + humidity * 0.20 + visibility * 0.20 + moonlight_helps * 0.15 + wind * 0.05

    # Hard gates: avoid promoting places that only look good on averages.
    if point.night_worst_cloud is not None and point.night_worst_cloud > 80:
        total = min(total, 69.9)
    if point.longest_usable_streak_hours is not None and point.longest_usable_streak_hours < 3:
        total = min(total, 64.9)

    point.final_score = round(total, 2)
    point.score_breakdown = {
        "weights": weights,
        "cloud_score": round(cloud, 2),
        "humidity_score": round(humidity, 2),
        "visibility_score": round(visibility, 2),
        "moonlight_score": round(moonlight_score, 2),
        "wind_score": round(wind, 2),
        "night_avg_cloud": round(point.night_avg_cloud, 1) if point.night_avg_cloud is not None else None,
        "night_worst_cloud": round(point.night_worst_cloud, 1) if point.night_worst_cloud is not None else None,
        "night_avg_humidity": round(point.night_avg_humidity, 1) if point.night_avg_humidity is not None else None,
        "night_avg_visibility": round(point.night_avg_visibility, 0) if point.night_avg_visibility is not None else None,
        "night_avg_wind": round(point.night_avg_wind, 1) if point.night_avg_wind is not None else None,
        "moon_interference": round(point.moon_interference, 1) if point.moon_interference is not None else None,
        "usable_hours": point.usable_hours,
        "longest_usable_streak_hours": point.longest_usable_streak_hours,
    }


