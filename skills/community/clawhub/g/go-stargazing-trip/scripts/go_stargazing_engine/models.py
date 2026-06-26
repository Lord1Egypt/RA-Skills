from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

Coordinate = Tuple[float, float]  # (lng, lat)

PolygonRing = List[Coordinate]

MultiPolygon = List[List[PolygonRing]]



@dataclass
class BoundingBox:
    name: str
    province: str
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float



@dataclass
class SamplePoint:
    id: str
    province: str
    scope_name: str
    lat: float
    lng: float
    weather_model: Optional[str] = None
    cloud_cover: Optional[float] = None
    humidity: Optional[float] = None
    visibility_m: Optional[float] = None
    wind_speed: Optional[float] = None
    moon_factor: Optional[float] = None
    elevation_m: Optional[float] = None
    # Nightly aggregation (computed over astronomical twilight window)
    night_avg_cloud: Optional[float] = None
    night_worst_cloud: Optional[float] = None
    night_avg_humidity: Optional[float] = None
    night_avg_visibility: Optional[float] = None
    night_avg_wind: Optional[float] = None
    moon_interference: Optional[float] = None  # 0=强干扰, 100=无干扰
    moonrise: Optional[str] = None
    moonset: Optional[str] = None
    moon_dark_window: Optional[str] = None
    night_avg_dew_point: Optional[float] = None
    night_max_precip: Optional[float] = None
    night_min_cloud_base: Optional[float] = None
    night_weather_codes: Optional[List[int]] = None
    usable_hours: Optional[float] = None
    longest_usable_streak_hours: Optional[float] = None
    best_window_start: Optional[str] = None
    best_window_end: Optional[str] = None
    best_window_segment: Optional[str] = None
    cloud_stddev: Optional[float] = None
    cloud_stability: Optional[str] = None
    worst_cloud_segment: Optional[str] = None
    stage1_status: str = "pending"
    merged_into: Optional[str] = None
    weather_source: Optional[str] = None
    fetch_attempts: int = 0
    fetch_recovered: bool = False
    fetch_error_type: Optional[str] = None
    fetch_error_message: Optional[str] = None
    final_score: Optional[float] = None
    score_breakdown: Optional[dict] = None



NATIONAL_SCOPE_BOXES = [
    {"province": "新疆", "min_lat": 34.3, "max_lat": 49.1, "min_lng": 73.8, "max_lng": 96.2},
    {"province": "西藏", "min_lat": 26.5, "max_lat": 36.5, "min_lng": 73.4, "max_lng": 99.1},
    {"province": "青海", "min_lat": 31.6, "max_lat": 39.2, "min_lng": 89.4, "max_lng": 103.1},
    {"province": "甘肃", "min_lat": 32.6, "max_lat": 42.8, "min_lng": 92.2, "max_lng": 108.7},
    {"province": "内蒙古", "min_lat": 37.4, "max_lat": 53.5, "min_lng": 97.2, "max_lng": 126.1},
    {"province": "宁夏", "min_lat": 35.2, "max_lat": 39.4, "min_lng": 104.2, "max_lng": 107.7},
    {"province": "山西", "min_lat": 34.6, "max_lat": 40.8, "min_lng": 110.2, "max_lng": 114.6},
    {"province": "河北", "min_lat": 36.0, "max_lat": 42.6, "min_lng": 113.5, "max_lng": 119.9},
]

# Major Chinese cities used for light-pollution estimation (name, lat, lng)
