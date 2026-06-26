#!/usr/bin/env python3
"""Public OSM map context CLI.

The CLI intentionally uses only Python standard-library modules so a skill user
does not need API keys, paid accounts, databases, or dependency installation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CACHE_DIR = Path.home() / ".openclaw" / "public-osm-map-context"
DEFAULT_USER_AGENT = (
    "public-osm-map-context-skill/0.1 "
    "(https://openstreetmap.org; property screening; contact: local-user)"
)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
PHOTON_URL = "https://photon.komoot.io/api/"
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
EARTH_RADIUS_M = 6_371_000
DEFAULT_REQUEST_TIMEOUT_SECONDS = 8
DEFAULT_MAX_LIVE_SECONDS = 45
DEFAULT_OVERPASS_RETRIES = 1


AMENITY_CATEGORIES = {
    "supermarket": [
        ("shop", "supermarket"),
        ("shop", "convenience"),
        ("shop", "grocery"),
    ],
    "pharmacy": [
        ("amenity", "pharmacy"),
        ("healthcare", "pharmacy"),
        ("amenity", "clinic"),
        ("healthcare", "clinic"),
    ],
    "restaurant": [
        ("amenity", "restaurant"),
        ("amenity", "cafe"),
        ("amenity", "fast_food"),
        ("amenity", "food_court"),
    ],
    "gym": [
        ("leisure", "fitness_centre"),
        ("sport", "fitness"),
    ],
    "park": [
        ("leisure", "park"),
        ("landuse", "recreation_ground"),
    ],
}


TRANSIT_TAGS = [
    ("public_transport", "platform"),
    ("railway", "station"),
    ("railway", "tram_stop"),
    ("highway", "bus_stop"),
]


RISK_TAGS = [
    ("highway", "motorway"),
    ("highway", "trunk"),
    ("highway", "primary"),
    ("railway", "rail"),
    ("railway", "tram"),
    ("landuse", "industrial"),
]


@dataclass
class Point:
    lat: float
    lng: float


@dataclass
class AddressCandidate:
    query: str
    source: str
    precision: str


class JsonCache:
    def __init__(self, cache_dir: Path, ttl_days: int = 30) -> None:
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_days * 24 * 60 * 60
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, namespace: str, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.cache_dir / namespace / f"{digest}.json"

    def get(self, namespace: str, key: str) -> Any | None:
        path = self._path(namespace, key)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if payload.get("expires_at", 0) < time.time():
            return None
        return payload.get("value")

    def set(self, namespace: str, key: str, value: Any) -> None:
        path = self._path(namespace, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "expires_at": time.time() + self.ttl_seconds,
            "value": value,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {"cache_dir": str(self.cache_dir)}
        total = 0
        for namespace in ["geocode", "overpass"]:
            ns_dir = self.cache_dir / namespace
            count = len(list(ns_dir.glob("*.json"))) if ns_dir.exists() else 0
            stats[f"{namespace}_entries"] = count
            total += count
        stats["total_entries"] = total
        return stats


class FixtureProvider:
    def __init__(self, fixture_dir: Path) -> None:
        self.fixture_dir = fixture_dir
        self.nominatim = self._load("nominatim.json")
        self.overpass = self._load("overpass.json")

    def _load(self, name: str) -> dict[str, Any]:
        path = self.fixture_dir / name
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def geocode(self, query: str) -> dict[str, Any] | None:
        normalized = normalize_query(query)
        value = self.nominatim.get(normalized)
        if not value:
            return None
        return value

    def overpass_elements(self, bbox: tuple[float, float, float, float]) -> list[dict[str, Any]]:
        return list(self.overpass.get("elements", []))


class PublicOsmClient:
    def __init__(
        self,
        cache: JsonCache,
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: int = DEFAULT_REQUEST_TIMEOUT_SECONDS,
        max_live_seconds: int = DEFAULT_MAX_LIVE_SECONDS,
        overpass_retries: int = DEFAULT_OVERPASS_RETRIES,
        geocode_strategy: str = "photon-first",
        fixture: FixtureProvider | None = None,
    ) -> None:
        self.cache = cache
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_live_seconds = max_live_seconds
        self.overpass_retries = overpass_retries
        self.geocode_strategy = geocode_strategy
        self.fixture = fixture
        self.started_at = time.monotonic()
        self.last_nominatim_call = 0.0
        self.usage = {
            "nominatim_requests": 0,
            "photon_requests": 0,
            "overpass_requests": 0,
            "cache_hits": 0,
            "fixture_hits": 0,
            "errors": [],
            "runtime_budget_seconds": max_live_seconds,
        }

    def geocode(self, query: str) -> dict[str, Any] | None:
        normalized = normalize_query(query)
        cached = self.cache.get("geocode", normalized)
        if cached is not None:
            self.usage["cache_hits"] += 1
            return cached

        if self.fixture:
            value = self.fixture.geocode(query)
            if value:
                self.usage["fixture_hits"] += 1
                self.cache.set("geocode", normalized, value)
                return value
            return None

        if self.geocode_strategy == "nominatim-first":
            result = self._geocode_nominatim(query)
            if result is None:
                result = self._geocode_photon(query)
        else:
            result = self._geocode_photon(query)
            if result is None:
                result = self._geocode_nominatim(query)
        if result is not None:
            self.cache.set("geocode", normalized, result)
        return result

    def _geocode_nominatim(self, query: str) -> dict[str, Any] | None:
        request_timeout = self._request_timeout("nominatim", query=query)
        if request_timeout is None:
            return None
        self._respect_nominatim_rate_limit()
        params = urllib.parse.urlencode(
            {
                "q": query,
                "format": "jsonv2",
                "limit": "1",
                "addressdetails": "0",
            }
        )
        url = f"{NOMINATIM_URL}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=request_timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            self.usage["errors"].append({"service": "nominatim", "query": query, "error": str(exc)})
            return None

        self.usage["nominatim_requests"] += 1
        if not data:
            return None
        result = {
            "lat": float(data[0]["lat"]),
            "lng": float(data[0]["lon"]),
            "display_name": data[0].get("display_name"),
            "source": "nominatim",
        }
        return result

    def _geocode_photon(self, query: str) -> dict[str, Any] | None:
        request_timeout = self._request_timeout("photon", query=query)
        if request_timeout is None:
            return None
        params = urllib.parse.urlencode({"q": query, "limit": "1"})
        url = f"{PHOTON_URL}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=request_timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            self.usage["errors"].append({"service": "photon", "query": query, "error": str(exc)})
            return None
        self.usage["photon_requests"] += 1
        features = data.get("features") or []
        if not features:
            return None
        feature = features[0]
        coordinates = (feature.get("geometry") or {}).get("coordinates") or []
        if len(coordinates) < 2:
            return None
        props = feature.get("properties") or {}
        display_parts = [props.get("name"), props.get("city"), props.get("state"), props.get("country")]
        display_name = ", ".join(str(part) for part in display_parts if part)
        return {
            "lat": float(coordinates[1]),
            "lng": float(coordinates[0]),
            "display_name": display_name or None,
            "source": "photon",
        }

    def overpass_elements(self, bbox: tuple[float, float, float, float]) -> list[dict[str, Any]]:
        key = ",".join(f"{part:.5f}" for part in bbox)
        cached = self.cache.get("overpass", key)
        if cached is not None:
            self.usage["cache_hits"] += 1
            return list(cached)

        if self.fixture:
            elements = self.fixture.overpass_elements(bbox)
            self.usage["fixture_hits"] += 1
            self.cache.set("overpass", key, elements)
            return elements

        query = build_overpass_query(bbox)
        encoded = urllib.parse.urlencode({"data": query}).encode("utf-8")
        last_error = None
        for endpoint in OVERPASS_ENDPOINTS:
            req = urllib.request.Request(
                endpoint,
                data=encoded,
                headers={
                    "User-Agent": self.user_agent,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            for attempt in range(max(1, self.overpass_retries)):
                request_timeout = self._request_timeout("overpass", bbox=key)
                if request_timeout is None:
                    return []
                try:
                    with urllib.request.urlopen(req, timeout=request_timeout) as response:
                        data = json.loads(response.read().decode("utf-8"))
                    elements = data.get("elements", [])
                    self.usage["overpass_requests"] += 1
                    self.cache.set("overpass", key, elements)
                    return elements
                except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                    last_error = str(exc)
                    if attempt + 1 < max(1, self.overpass_retries):
                        self._sleep_with_budget(min(2**attempt, 2))
        self.usage["errors"].append({"service": "overpass", "bbox": key, "error": last_error})
        return []

    def _respect_nominatim_rate_limit(self) -> None:
        elapsed = time.time() - self.last_nominatim_call
        if elapsed < 1.1:
            self._sleep_with_budget(1.1 - elapsed)
        self.last_nominatim_call = time.time()

    def _remaining_live_seconds(self) -> float:
        if self.fixture:
            return float("inf")
        return self.max_live_seconds - (time.monotonic() - self.started_at)

    def _request_timeout(self, service: str, **context: Any) -> float | None:
        remaining = self._remaining_live_seconds()
        if remaining <= 0:
            payload = {"service": service, "error": "runtime_budget_exhausted"}
            payload.update(context)
            self.usage["errors"].append(payload)
            return None
        return max(1.0, min(float(self.timeout), remaining))

    def _sleep_with_budget(self, seconds: float) -> None:
        remaining = self._remaining_live_seconds()
        if remaining <= 0:
            return
        time.sleep(min(seconds, remaining))


def normalize_query(value: str) -> str:
    return " ".join(value.lower().strip().split())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def haversine_m(a: Point, b: Point) -> float:
    lat1 = math.radians(a.lat)
    lat2 = math.radians(b.lat)
    dlat = lat2 - lat1
    dlng = math.radians(b.lng - a.lng)
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(h))


def destination_minutes_range(distance_m: float) -> str:
    # Conservative line-distance conversion: routes are rarely straight.
    min_minutes = (distance_m * 1.2 / 1000) / 5.0 * 60
    max_minutes = (distance_m * 1.8 / 1000) / 4.2 * 60
    return f"{round(min_minutes):.0f}-{round(max_minutes):.0f}"


def walk_minutes_from_distance(distance_m: float) -> int:
    return max(1, round((distance_m / 1000) / 4.8 * 60))


def meters_range(distance_m: float) -> str:
    low = max(0, round(distance_m * 0.85 / 50) * 50)
    high = round(distance_m * 1.15 / 50) * 50
    if high < 50:
        high = 50
    return f"{low}-{high}"


STREET_SUFFIX_RE = (
    r"Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|"
    r"Place|Pl|Parade|Pde|Terrace|Tce|Highway|Hwy|Crescent|Cres|Square|Sq|Circuit|Cct"
)
ADDRESS_START_RE = re.compile(
    rf"(?:[A-Za-z0-9-]+/)?\d{{1,6}}[A-Za-z]?\s+"
    rf"(?:[A-Za-z0-9'’.-]+\s+){{0,8}}(?:{STREET_SUFFIX_RE})\b",
    re.IGNORECASE,
)
ADDRESS_END_RE = re.compile(
    r"(?:\b(?:VIC|NSW|QLD|SA|WA|TAS|ACT|NT)\s+\d{4}\b(?:,\s*Australia)?|"
    r"\b(?:Abu Dhabi|Dubai)\b(?:\s*[-,]\s*(?:United Arab Emirates|UAE))?)",
    re.IGNORECASE,
)
PRICE_RE = re.compile(r"\s+(?:A\$|AED|USD|US\$|\$|CNY|RMB|¥)\s*[\d,]", re.IGNORECASE)
BEDROOM_RE = re.compile(r"\b\d+\s*(?:bed|beds|bedroom|bedrooms|br)(?=\d|\b)", re.IGNORECASE)


def normalize_address_text(value: str) -> str:
    text = " ".join(value.replace("\u00a0", " ").split())
    text = PRICE_RE.split(text)[0]
    return text.strip(" ,;-")


def score_address_candidate(value: str) -> tuple[int, int]:
    normalized = value.lower()
    score = 0
    if re.search(r"\b(?:vic|nsw|qld|sa|wa|tas|act|nt)\s+\d{4}\b", normalized):
        score += 40
    if "australia" in normalized or "united arab emirates" in normalized or "uae" in normalized:
        score += 20
    if BEDROOM_RE.search(normalized):
        score -= 25
    if len(value) > 120:
        score -= 20
    return score, -len(value)


def clean_address_candidate(value: str) -> str:
    value = BEDROOM_RE.split(value)[-1]
    return normalize_address_text(value)


def extract_address_from_text(value: Any) -> str:
    text = safe_text(value)
    if not text:
        return ""
    normalized = normalize_address_text(text)
    candidates: list[str] = []
    for start in ADDRESS_START_RE.finditer(normalized):
        tail = normalized[start.end() : start.end() + 180]
        end = ADDRESS_END_RE.search(tail)
        if end:
            candidate = normalized[start.start() : start.end() + end.end()]
        else:
            candidate = start.group(0)
        candidate = clean_address_candidate(candidate)
        if candidate and candidate not in candidates:
            candidates.append(candidate)
    if not candidates:
        return ""
    return max(candidates, key=score_address_candidate)


def looks_like_street_address(value: str) -> bool:
    return bool(ADDRESS_START_RE.search(value))


def build_address_candidate(listing: dict[str, Any]) -> AddressCandidate | None:
    address = safe_text(listing.get("address"))
    if address and looks_like_street_address(address):
        return AddressCandidate(address, "address", "address")

    location = safe_text(listing.get("location"))
    if location and looks_like_street_address(location):
        return AddressCandidate(location, "location", "address")

    title_address = extract_address_from_text(listing.get("title"))
    if title_address:
        return AddressCandidate(title_address, "title", "address")

    description_address = extract_address_from_text(listing.get("description"))
    if description_address:
        return AddressCandidate(description_address, "description", "address")

    if address:
        return AddressCandidate(address, "address", "area")

    if location:
        return AddressCandidate(location, "location", "area")

    return None


def geocode_listing(client: PublicOsmClient, listing: dict[str, Any]) -> dict[str, Any]:
    lat = as_float(listing.get("lat"))
    lng = as_float(listing.get("lng"))
    if lat is not None and lng is not None:
        precision = listing.get("geo_precision") or ("address" if listing.get("address") else "area")
        query = safe_text(listing.get("address")) or safe_text(listing.get("location")) or safe_text(listing.get("title"))
        return {
            "lat": lat,
            "lng": lng,
            "precision": precision,
            "source": "input",
            "confidence": "high" if precision == "address" else "medium",
            "geocode_query_used": query,
            "address_extraction_source": "input_coordinates",
        }

    candidate = build_address_candidate(listing)
    if not candidate:
        return {
            "lat": None,
            "lng": None,
            "precision": "missing",
            "source": None,
            "confidence": "low",
            "geocode_query_used": None,
            "address_extraction_source": None,
        }

    result = client.geocode(candidate.query)
    if not result:
        return {
            "lat": None,
            "lng": None,
            "precision": "missing",
            "source": "nominatim",
            "confidence": "low",
            "geocode_query_used": candidate.query,
            "address_extraction_source": candidate.source,
        }

    source = result.get("source", "nominatim")
    if candidate.precision == "address" and source in {"nominatim", "fixture_nominatim"}:
        precision = "address"
        confidence = "medium"
    elif candidate.precision == "address" and source == "input":
        precision = "address"
        confidence = "high"
    else:
        # Photon is fast and useful for batch screening, but it often resolves
        # to a nearby POI or area label rather than the exact listing address.
        precision = "area"
        confidence = "low"
    return {
        "lat": result["lat"],
        "lng": result["lng"],
        "precision": precision,
        "source": source,
        "confidence": confidence,
        "query": candidate.query,
        "geocode_query_used": candidate.query,
        "address_extraction_source": candidate.source,
        "display_name": result.get("display_name"),
    }


def safe_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def build_overpass_query(bbox: tuple[float, float, float, float]) -> str:
    south, west, north, east = bbox
    bbox_text = f"{south:.6f},{west:.6f},{north:.6f},{east:.6f}"
    selectors: list[str] = []
    for pairs in AMENITY_CATEGORIES.values():
        for key, value in pairs:
            selectors.append(f'node["{key}"="{value}"]({bbox_text});')
            selectors.append(f'way["{key}"="{value}"]({bbox_text});')
    for key, value in TRANSIT_TAGS + RISK_TAGS:
        selectors.append(f'node["{key}"="{value}"]({bbox_text});')
        selectors.append(f'way["{key}"="{value}"]({bbox_text});')
    body = "\n  ".join(selectors)
    return f"[out:json][timeout:25];\n(\n  {body}\n);\nout center tags;"


def bbox_for_points(points: list[Point], padding_km: float = 1.0) -> tuple[float, float, float, float]:
    min_lat = min(p.lat for p in points)
    max_lat = max(p.lat for p in points)
    min_lng = min(p.lng for p in points)
    max_lng = max(p.lng for p in points)
    pad_lat = padding_km / 111.0
    mid_lat = (min_lat + max_lat) / 2
    pad_lng = padding_km / (111.0 * max(0.2, math.cos(math.radians(mid_lat))))
    return (min_lat - pad_lat, min_lng - pad_lng, max_lat + pad_lat, max_lng + pad_lng)


def cluster_key(point: Point, km: float = 1.5) -> str:
    lat_bucket = round(point.lat / (km / 111.0))
    lng_bucket = round(point.lng / (km / (111.0 * max(0.2, math.cos(math.radians(point.lat))))))
    return f"{lat_bucket}:{lng_bucket}"


def element_point(element: dict[str, Any]) -> Point | None:
    lat = element.get("lat")
    lon = element.get("lon")
    if lat is None and isinstance(element.get("center"), dict):
        lat = element["center"].get("lat")
        lon = element["center"].get("lon")
    lat_f = as_float(lat)
    lon_f = as_float(lon)
    if lat_f is None or lon_f is None:
        return None
    return Point(lat_f, lon_f)


def element_name(element: dict[str, Any]) -> str | None:
    tags = element.get("tags") or {}
    name = tags.get("name") or tags.get("name:en")
    return name if isinstance(name, str) and name.strip() else None


def amenity_category(tags: dict[str, Any]) -> str | None:
    for category, pairs in AMENITY_CATEGORIES.items():
        for key, value in pairs:
            if tags.get(key) == value:
                return category
    return None


def transit_type(tags: dict[str, Any]) -> str | None:
    if tags.get("railway") == "station":
        return "train_station"
    if tags.get("railway") == "tram_stop":
        return "tram_stop"
    if tags.get("highway") == "bus_stop":
        return "bus_stop"
    if tags.get("public_transport") == "platform":
        return "transit_platform"
    return None


def risk_type(tags: dict[str, Any]) -> str | None:
    highway = tags.get("highway")
    if highway in {"motorway", "trunk", "primary"}:
        return "primary_road"
    railway = tags.get("railway")
    if railway in {"rail", "tram"}:
        return "railway"
    if tags.get("landuse") == "industrial":
        return "industrial_landuse"
    return None


def analyze_elements(point: Point, elements: list[dict[str, Any]], precision: str) -> dict[str, Any]:
    amenities = {
        "radius_meters": 800,
        "supermarket_count": 0,
        "pharmacy_count": 0,
        "restaurant_count": 0,
        "gym_count": 0,
        "park_count": 0,
        "source": "overpass_osm",
    }
    nearest_transit: dict[str, Any] | None = None
    nearest_risks: dict[str, float | None] = {
        "near_primary_road_meters": None,
        "near_railway_meters": None,
        "industrial_landuse_nearby": None,
    }

    for element in elements:
        tags = element.get("tags") or {}
        ep = element_point(element)
        if not ep:
            continue
        distance = haversine_m(point, ep)
        category = amenity_category(tags)
        if category and distance <= 800:
            amenities[f"{category}_count"] += 1
        t_type = transit_type(tags)
        if t_type:
            if nearest_transit is None or distance < nearest_transit["distance_meters"]:
                nearest_transit = {
                    "nearest_stop_name": element_name(element),
                    "nearest_stop_type": t_type,
                    "distance_meters": round(distance),
                    "distance_meters_range": meters_range(distance),
                    "distance_type": "straight_line_estimate",
                    "walk_minutes_estimate": walk_minutes_from_distance(distance),
                    "source": "overpass_osm",
                }
        r_type = risk_type(tags)
        if r_type == "primary_road":
            current = nearest_risks["near_primary_road_meters"]
            if current is None or distance < current:
                nearest_risks["near_primary_road_meters"] = round(distance)
        elif r_type == "railway":
            current = nearest_risks["near_railway_meters"]
            if current is None or distance < current:
                nearest_risks["near_railway_meters"] = round(distance)
        elif r_type == "industrial_landuse" and distance <= 1000:
            nearest_risks["industrial_landuse_nearby"] = True

    if nearest_risks["industrial_landuse_nearby"] is None:
        nearest_risks["industrial_landuse_nearby"] = False

    if precision != "address":
        # Area-level geocoding should not imply listing-level exact distances.
        nearest_transit = area_level_transit(nearest_transit)
        amenities["precision_note"] = "area_level_location"
        nearest_risks = area_level_risks(nearest_risks)

    return {
        "amenities": amenities,
        "transit_access": nearest_transit,
        "risk_signals": nearest_risks,
    }


def area_level_transit(transit: dict[str, Any] | None) -> dict[str, Any] | None:
    if not transit:
        return None
    return {
        "nearest_stop_name": transit.get("nearest_stop_name"),
        "nearest_stop_type": transit.get("nearest_stop_type"),
        "source": transit.get("source"),
        "distance_type": "not_available_for_area_level_location",
        "precision_note": "area_level_location_no_listing_level_distance",
    }


def area_level_risks(risks: dict[str, float | bool | None]) -> dict[str, Any]:
    return {
        "area_has_primary_road_features": risks.get("near_primary_road_meters") is not None,
        "area_has_railway_features": risks.get("near_railway_meters") is not None,
        "industrial_landuse_nearby": bool(risks.get("industrial_landuse_nearby")),
        "precision_note": "area_level_location_no_listing_level_risk_distance",
    }


def assessment_confidence(geo: dict[str, Any], *, downgrade: bool = False) -> str:
    confidence = geo.get("confidence") or "low"
    if geo.get("precision") == "missing":
        return "low"
    if downgrade and confidence == "high":
        return "medium"
    return confidence


def limit_assessment(limitations: list[str], *extra: str) -> list[str]:
    values = [item for item in [*limitations, *extra] if item]
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def build_transport_assessment(result: dict[str, Any]) -> dict[str, Any]:
    geo = result.get("geo") or {}
    transit = result.get("transit_access") or {}
    destination = result.get("destination_access") or {}
    limitations = result.get("limitations") or []
    if geo.get("precision") == "missing":
        return {
            "conclusion": "自动地图定位失败，交通结论需人工复核。",
            "evidence": ["未拿到可用经纬度，只能提供手动地图复核链接。"],
            "confidence": "low",
            "limitations": limit_assessment(limitations, "geo_missing"),
        }
    if geo.get("precision") == "area":
        evidence = []
        if transit.get("nearest_stop_name"):
            evidence.append(f"区域级可见最近公共交通名称：{transit['nearest_stop_name']}。")
        if destination.get("destination"):
            evidence.append(f"到 {destination['destination']} 只能做区域级直线估算。")
        return {
            "conclusion": "当前只有区域级位置，交通只能做片区参考，不能作为楼栋级步行距离结论。",
            "evidence": evidence or ["缺少地址级定位，站点距离和路线时间都需人工复核。"],
            "confidence": assessment_confidence(geo, downgrade=True),
            "limitations": limit_assessment(limitations, "area_level_location"),
        }
    evidence = []
    if transit.get("nearest_stop_name"):
        evidence.append(
            f"到 OSM 记录的 {transit['nearest_stop_name']} 直线估算约 {transit.get('distance_meters_range', '待确认')}m。"
        )
    if destination.get("destination"):
        evidence.append(
            f"到 {destination['destination']} 的直线估算约 {destination.get('straight_line_km', '待确认')} km。"
        )
    conclusion = "交通可做首轮筛选，但真实步行路线和高峰通勤仍需人工复核。"
    if transit.get("nearest_stop_name") and destination.get("destination"):
        conclusion = "交通条件已有地址级 OSM 证据，可用于首轮排序。"
    return {
        "conclusion": conclusion,
        "evidence": evidence or ["已拿到地址级定位，但缺少可直接复述的站点或目的地距离。"],
        "confidence": assessment_confidence(geo),
        "limitations": limit_assessment(limitations, "straight_line_estimate_only"),
    }


def build_daily_convenience_assessment(result: dict[str, Any]) -> dict[str, Any]:
    geo = result.get("geo") or {}
    amenities = result.get("amenities") or {}
    limitations = result.get("limitations") or []
    if geo.get("precision") == "missing" or not amenities:
        return {
            "conclusion": "周边生活便利度自动分析失败，需要人工复核。",
            "evidence": ["未拿到可靠位置或配套数据。"],
            "confidence": "low",
            "limitations": limit_assessment(limitations, "geo_missing"),
        }
    score = (
        int(amenities.get("supermarket_count", 0))
        + int(amenities.get("pharmacy_count", 0))
        + int(amenities.get("restaurant_count", 0))
    )
    if score >= 10:
        conclusion = "生活便利度较好。"
    elif score >= 4:
        conclusion = "生活便利度中等，能满足基础日常需求。"
    else:
        conclusion = "公开 OSM 记录到的生活配套有限，需重点人工复核。"
    if geo.get("precision") == "area":
        conclusion = "区域级配套成熟度可做参考，但不能直接代表房源楼下的便利度。"
    evidence = [
        f"800m 范围内记录到超市 {amenities.get('supermarket_count', 0)} 家。",
        f"800m 范围内记录到药店/诊所 {amenities.get('pharmacy_count', 0)} 处。",
        f"800m 范围内记录到餐饮 {amenities.get('restaurant_count', 0)} 处。",
    ]
    return {
        "conclusion": conclusion,
        "evidence": evidence,
        "confidence": assessment_confidence(geo, downgrade=geo.get("precision") == "area"),
        "limitations": limit_assessment(limitations),
    }


def build_environment_risk_assessment(result: dict[str, Any]) -> dict[str, Any]:
    geo = result.get("geo") or {}
    risks = result.get("risk_signals") or {}
    limitations = result.get("limitations") or []
    if geo.get("precision") == "missing" or not risks:
        return {
            "conclusion": "环境风险自动分析失败，需要人工复核噪音和工业用地。",
            "evidence": ["未拿到可靠位置。"],
            "confidence": "low",
            "limitations": limit_assessment(limitations, "geo_missing"),
        }
    evidence: list[str] = []
    risk_level = "低"
    primary_road = risks.get("near_primary_road_meters")
    railway = risks.get("near_railway_meters")
    industrial = risks.get("industrial_landuse_nearby")
    if primary_road is not None:
        evidence.append(f"最近主路信号约 {primary_road}m。")
        if primary_road <= 120:
            risk_level = "高"
    if railway is not None:
        evidence.append(f"最近铁路/电车轨道信号约 {railway}m。")
        if railway <= 180:
            risk_level = "高"
        elif risk_level != "高":
            risk_level = "中"
    if industrial:
        evidence.append("1km 范围内发现工业用地信号。")
        risk_level = "高"
    if geo.get("precision") == "area":
        conclusion = "区域级环境风险可做参考，噪音源距离仍需人工复核。"
    elif risk_level == "高":
        conclusion = "环境风险偏高，需重点核对主路/轨道/工业干扰。"
    elif risk_level == "中":
        conclusion = "环境存在一定干扰可能，建议打开地图和原帖做二次确认。"
    else:
        conclusion = "当前未见明显高风险环境信号，但仍不等于实地安静。"
    return {
        "conclusion": conclusion,
        "evidence": evidence or ["未记录到明显主路、轨道或工业用地信号。"],
        "confidence": assessment_confidence(geo, downgrade=geo.get("precision") == "area"),
        "limitations": limit_assessment(limitations),
    }


def build_area_maturity_assessment(result: dict[str, Any]) -> dict[str, Any]:
    geo = result.get("geo") or {}
    amenities = result.get("amenities") or {}
    limitations = result.get("limitations") or []
    if geo.get("precision") == "missing":
        return {
            "conclusion": "区域成熟度无法自动判断，需要人工复核。",
            "evidence": ["缺少可用定位。"],
            "confidence": "low",
            "limitations": limit_assessment(limitations, "geo_missing"),
        }
    total_poi = (
        int(amenities.get("supermarket_count", 0))
        + int(amenities.get("pharmacy_count", 0))
        + int(amenities.get("restaurant_count", 0))
        + int(amenities.get("gym_count", 0))
        + int(amenities.get("park_count", 0))
    )
    if total_poi >= 12:
        conclusion = "区域成熟度较高。"
    elif total_poi >= 5:
        conclusion = "区域成熟度中等。"
    else:
        conclusion = "区域成熟度偏弱或公开 OSM 记录不足。"
    if geo.get("precision") == "area":
        conclusion = f"{conclusion.rstrip('。')}；这个结论只能代表片区，不代表具体楼栋。"
    evidence = [f"当前片区公开 OSM 记录到的常用配套总量约 {total_poi} 项。"]
    return {
        "conclusion": conclusion,
        "evidence": evidence,
        "confidence": assessment_confidence(geo, downgrade=geo.get("precision") == "area"),
        "limitations": limit_assessment(limitations),
    }


def build_assessments(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "transport_access": build_transport_assessment(result),
        "daily_convenience": build_daily_convenience_assessment(result),
        "environment_risk": build_environment_risk_assessment(result),
        "area_maturity": build_area_maturity_assessment(result),
    }


def verification_links(listing: dict[str, Any], geo: dict[str, Any]) -> dict[str, str]:
    lat = geo.get("lat")
    lng = geo.get("lng")
    query = (
        safe_text(geo.get("geocode_query_used"))
        or safe_text(listing.get("address"))
        or safe_text(listing.get("location"))
        or safe_text(listing.get("title"))
    )
    encoded = urllib.parse.quote(query)
    links = {
        "google_maps_manual": f"https://www.google.com/maps/search/?api=1&query={encoded}",
    }
    if lat is not None and lng is not None:
        links["openstreetmap"] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}"
    else:
        links["openstreetmap"] = f"https://www.openstreetmap.org/search?query={encoded}"
    return links


def listing_ref(listing: dict[str, Any]) -> dict[str, Any]:
    """Return a compact listing echo for downstream decision-layer joins."""
    return {
        "id": safe_text(listing.get("id")) or None,
        "listing_id": safe_text(listing.get("listing_id")) or None,
        "title": safe_text(listing.get("title")) or None,
        "price": safe_text(listing.get("price")) or None,
        "location": safe_text(listing.get("location")) or None,
        "url": safe_text(listing.get("url")) or None,
        "image_url": safe_text(listing.get("image_url")) or None,
    }


def analyze_batch(args: argparse.Namespace) -> dict[str, Any]:
    input_data = load_json(Path(args.input))
    listings = input_data.get("listings", input_data if isinstance(input_data, list) else [])
    if not isinstance(listings, list):
        raise SystemExit("Input must be a JSON object with listings[] or a listings array")

    fixture = FixtureProvider(Path(args.fixture_dir)) if args.fixture_dir else None
    cache = JsonCache(Path(args.cache_dir).expanduser(), ttl_days=args.cache_ttl_days)
    client = PublicOsmClient(
        cache,
        timeout=args.timeout,
        max_live_seconds=args.max_live_seconds,
        overpass_retries=args.overpass_retries,
        geocode_strategy=args.geocode_strategy,
        fixture=fixture,
    )

    destination_geo = client.geocode(args.destination) if args.destination else None
    destination_point = None
    if destination_geo:
        destination_point = Point(float(destination_geo["lat"]), float(destination_geo["lng"]))

    prepared: list[tuple[dict[str, Any], dict[str, Any], Point | None]] = []
    for index, listing in enumerate(listings):
        if not isinstance(listing, dict):
            continue
        listing_id = safe_text(listing.get("id")) or safe_text(listing.get("listing_id")) or f"listing_{index + 1}"
        listing["id"] = listing_id
        geo = geocode_listing(client, listing)
        point = None
        if geo.get("lat") is not None and geo.get("lng") is not None:
            point = Point(float(geo["lat"]), float(geo["lng"]))
        prepared.append((listing, geo, point))

    clusters: dict[str, list[Point]] = {}
    for _, _, point in prepared:
        if point:
            clusters.setdefault(cluster_key(point), []).append(point)

    cluster_elements: dict[str, list[dict[str, Any]]] = {}
    for key, points in clusters.items():
        bbox = bbox_for_points(points, padding_km=args.cluster_padding_km)
        cluster_elements[key] = client.overpass_elements(bbox)

    results = []
    status = "ok"
    for listing, geo, point in prepared:
        limitations = ["not_google_maps_verified", "public_transport_time_not_verified", "osm_coverage_may_be_incomplete"]
        ref = listing_ref(listing)
        result: dict[str, Any] = {
            "id": listing["id"],
            "listing_ref": ref,
            "geo": geo,
            "verification_links": verification_links(listing, geo),
            "limitations": list(limitations),
        }
        if not ref.get("url"):
            result["limitations"].append("original_listing_url_missing")
        if geo.get("confidence") == "low" and geo.get("precision") != "missing":
            result["limitations"].append("low_geocode_confidence")
        if point is None:
            result.update(
                {
                    "amenities": None,
                    "transit_access": None,
                    "risk_signals": None,
                }
            )
            result["limitations"].append("geo_missing")
            status = "partial"
        else:
            elements = cluster_elements.get(cluster_key(point), [])
            context = analyze_elements(point, elements, geo.get("precision", "missing"))
            result.update(context)
            origin_label = safe_text(geo.get("geocode_query_used")) or safe_text(listing.get("address")) or safe_text(listing.get("title")) or listing["id"]
            if isinstance(result.get("transit_access"), dict):
                result["transit_access"]["origin"] = origin_label
            if destination_point:
                distance = haversine_m(point, destination_point)
                result["destination_access"] = {
                    "origin": origin_label,
                    "destination": args.destination,
                    "distance_type": "straight_line_estimate",
                    "straight_line_km": round(distance / 1000, 2),
                    "walk_minutes_range": destination_minutes_range(distance),
                    "verified_route": False,
                    "source": "local_distance_estimate",
                }
                if geo.get("precision") != "address":
                    result["destination_access"]["precision_note"] = "area_level_location_no_listing_level_route"
                result["limitations"].append("route_time_is_estimated")
            if geo.get("precision") == "area":
                result["limitations"].append("area_level_location")
        result["status"] = "degraded" if geo.get("precision") == "missing" else ("partial" if geo.get("precision") == "area" else "ok")
        result["assessments"] = build_assessments(result)
        results.append(result)

    # Nominatim failures can be fully recovered by Photon fallback. Only mark
    # partial for service failures that leave map context incomplete.
    if any(error.get("service") == "overpass" for error in client.usage["errors"]) and status == "ok":
        status = "partial"
    if results and all(item["geo"].get("precision") == "missing" for item in results):
        status = "degraded"

    return {
        "status": status,
        "provider": "public_osm_fixture" if fixture else "public_osm",
        "analysis_level": args.level,
        "city": args.city,
        "destination": args.destination,
        "incremental": bool(args.incremental),
        "listings": results,
        "usage": client.usage,
    }


def cmd_doctor(args: argparse.Namespace) -> dict[str, Any]:
    cache_dir = Path(args.cache_dir).expanduser()
    return {
        "status": "ok",
        "provider": "public_osm",
        "requires_api_key": False,
        "requires_local_database": False,
        "requires_third_party_python_packages": False,
        "network_required_for_live_queries": True,
        "cache_dir": str(cache_dir),
        "python": sys.version.split()[0],
    }


def cmd_cache_stats(args: argparse.Namespace) -> dict[str, Any]:
    cache = JsonCache(Path(args.cache_dir).expanduser(), ttl_days=args.cache_ttl_days)
    return cache.stats()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Public OSM map context CLI")
    parser.add_argument("--cache-dir", default=os.environ.get("PUBLIC_OSM_MAP_CONTEXT_CACHE", str(DEFAULT_CACHE_DIR)))
    parser.add_argument("--cache-ttl-days", type=int, default=30)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check runtime capabilities")
    doctor.set_defaults(func=cmd_doctor)

    cache = subparsers.add_parser("cache-stats", help="Show local cache statistics")
    cache.set_defaults(func=cmd_cache_stats)

    analyze = subparsers.add_parser("analyze-batch", help="Analyze property listings with public OSM context")
    analyze.add_argument("--input", required=True, help="Path to listings JSON")
    analyze.add_argument("--destination", default="", help="Destination such as Melbourne CBD VIC")
    analyze.add_argument("--city", default="", help="City label for output metadata")
    analyze.add_argument("--level", choices=["basic", "deep"], default="deep")
    analyze.add_argument("--fixture-dir", default="", help="Use fixture JSON instead of public OSM network calls")
    analyze.add_argument("--incremental", action="store_true", help="Reuse cache and only fetch missing context")
    analyze.add_argument("--timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT_SECONDS)
    analyze.add_argument("--max-live-seconds", type=int, default=DEFAULT_MAX_LIVE_SECONDS)
    analyze.add_argument("--overpass-retries", type=int, default=DEFAULT_OVERPASS_RETRIES)
    analyze.add_argument("--geocode-strategy", choices=["photon-first", "nominatim-first"], default="photon-first")
    analyze.add_argument("--cluster-padding-km", type=float, default=1.0)
    analyze.set_defaults(func=analyze_batch)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except BrokenPipeError:
        return 1
    dump_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
