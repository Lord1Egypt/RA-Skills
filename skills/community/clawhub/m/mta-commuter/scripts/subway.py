"""Lightweight NYC Subway data layer.

Provides station-to-lines mapping, average headways by time-of-day,
and service alerts. No real-time arrival tracking — subway runs frequently
enough that headway estimates ("every ~8 min") are sufficient.
"""

import json
from datetime import datetime
from pathlib import Path

from geo import haversine_miles
from gtfs import GtfsSystem


SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
DATA_DIR = SKILL_DIR / "data"
HEADWAY_CACHE = DATA_DIR / ".subway_cache" / "headways.json"


def _get_subway_system():
    """Load subway GtfsSystem from feeds.json."""
    feeds_path = SCRIPTS_DIR / "feeds.json"
    if not feeds_path.exists():
        raise FileNotFoundError(
            f"Missing config file {feeds_path}. Reinstall the skill."
        )
    with open(feeds_path) as f:
        feeds = json.load(f)
    if "subway" not in feeds:
        raise KeyError("feeds.json is missing the 'subway' entry")
    return GtfsSystem.from_config("subway", feeds["subway"], DATA_DIR)


def get_time_bucket(hour):
    """Map an hour (0-23) to a time bucket name."""
    if 7 <= hour < 10:
        return "peak_am"
    elif 10 <= hour < 16:
        return "midday"
    elif 16 <= hour < 19:
        return "peak_pm"
    elif 19 <= hour < 22:
        return "evening"
    else:
        return "overnight"


def _current_time_bucket():
    """Get the time bucket for right now."""
    return get_time_bucket(datetime.now().hour)


def build_station_lines(subway=None):
    """Build mapping of parent station stop_id -> set of route short names.

    Only includes parent stations (location_type=1), not directional stops.
    Returns: {stop_id: {"name": str, "lat": float, "lon": float, "lines": [str, ...]}}
    """
    if subway is None:
        subway = _get_subway_system()
    subway.ensure_cache()

    stops = subway.load_stops()
    routes = subway.load_routes()
    trips = subway.load_trips()
    stop_times = subway.load_stop_times()

    # Build route_id -> short_name lookup
    route_names = {}
    for rid, r in routes.items():
        route_names[rid] = r.get("route_short_name", rid)

    # Find which routes serve which stops
    stop_routes = {}
    for st in stop_times:
        sid = st["stop_id"]
        trip = trips.get(st["trip_id"])
        if trip:
            route_name = route_names.get(trip["route_id"], "")
            if route_name:
                stop_routes.setdefault(sid, set()).add(route_name)

    # Aggregate to parent stations
    parent_stations = {}
    for sid, stop in stops.items():
        if stop.get("location_type") == "1":
            parent_stations[sid] = {
                "name": stop["stop_name"],
                "lat": float(stop["stop_lat"]),
                "lon": float(stop["stop_lon"]),
                "lines": set(),
            }

    # Directional stops (N/S suffix) inherit parent's lines
    for sid, routes_set in stop_routes.items():
        stop = stops.get(sid, {})
        parent_id = stop.get("parent_station", "")
        if parent_id and parent_id in parent_stations:
            parent_stations[parent_id]["lines"].update(routes_set)
        elif sid in parent_stations:
            parent_stations[sid]["lines"].update(routes_set)

    # Convert sets to sorted lists
    for station in parent_stations.values():
        station["lines"] = sorted(station["lines"])

    return parent_stations


def compute_headways(subway=None):
    """Compute average headways per route, station, and time bucket.

    Returns: {route_short_name: {parent_stop_id: {bucket: avg_minutes}}}
    Caches result to disk since this is expensive to compute.
    """
    if subway is None:
        subway = _get_subway_system()
    subway.ensure_cache()

    # Invalidate cache if older than the GTFS zip
    if HEADWAY_CACHE.exists():
        cache_mtime = HEADWAY_CACHE.stat().st_mtime
        gtfs_mtime = subway.cache_zip.stat().st_mtime if subway.cache_zip.exists() else 0
        if cache_mtime >= gtfs_mtime:
            with open(HEADWAY_CACHE) as f:
                return json.load(f)

    stops = subway.load_stops()
    routes = subway.load_routes()
    trips = subway.load_trips()
    stop_times = subway.load_stop_times()

    route_names = {}
    for rid, r in routes.items():
        route_names[rid] = r.get("route_short_name", rid)

    # Build parent_station lookup for directional stops
    parent_map = {}
    for sid, stop in stops.items():
        parent = stop.get("parent_station", "")
        if parent:
            parent_map[sid] = parent

    # Collect departure minutes by (route, parent_station, service_id)
    departures = {}
    for st in stop_times:
        trip = trips.get(st["trip_id"])
        if not trip:
            continue
        route_name = route_names.get(trip["route_id"], "")
        if not route_name:
            continue

        sid = st["stop_id"]
        parent_id = parent_map.get(sid, sid)

        dep_parts = st["departure_time"].split(":")
        dep_min = int(dep_parts[0]) * 60 + int(dep_parts[1])
        dep_hour = int(dep_parts[0])

        service_id = trip["service_id"]
        key = (route_name, parent_id, service_id)
        departures.setdefault(key, []).append((dep_min, dep_hour))

    # Compute average gap per time bucket (use Weekday as primary)
    headways = {}
    for (route, station, service_id), deps in departures.items():
        if service_id != "Weekday":
            continue

        # Group by time bucket
        bucket_deps = {}
        for dep_min, dep_hour in deps:
            bucket = get_time_bucket(dep_hour % 24)
            bucket_deps.setdefault(bucket, []).append(dep_min)

        station_headways = {}
        for bucket, minutes in bucket_deps.items():
            minutes.sort()
            if len(minutes) < 2:
                continue
            gaps = [minutes[i+1] - minutes[i] for i in range(len(minutes)-1)]
            gaps = [g for g in gaps if 0 < g < 60]  # filter out nonsense
            if gaps:
                station_headways[bucket] = round(sum(gaps) / len(gaps), 1)

        if station_headways:
            headways.setdefault(route, {})[station] = station_headways

    # Cache
    HEADWAY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(HEADWAY_CACHE, "w") as f:
        json.dump(headways, f)

    return headways


def get_headway(route, stop_id, time_bucket=None, headways=None):
    """Get average headway in minutes for a route at a station.

    Returns float (minutes) or None if no data.
    """
    if headways is None:
        headways = compute_headways()
    if time_bucket is None:
        time_bucket = _current_time_bucket()

    route_data = headways.get(route, {})
    station_data = route_data.get(stop_id, {})
    return station_data.get(time_bucket)


def find_nearby_subway_stations(lat, lon, radius_miles=1.0, station_lines=None):
    """Find subway stations near a point, with their lines.

    Returns list of dicts sorted by distance:
    [{"stop_id": "...", "name": "...", "lines": ["A","C","E"], "distance_miles": 0.3}, ...]
    """
    if station_lines is None:
        station_lines = build_station_lines()

    results = []
    for sid, info in station_lines.items():
        dist = haversine_miles(lat, lon, info["lat"], info["lon"])
        if dist <= radius_miles:
            results.append({
                "stop_id": sid,
                "name": info["name"],
                "lines": info["lines"],
                "lat": info["lat"],
                "lon": info["lon"],
                "distance_miles": round(dist, 2),
            })
    results.sort(key=lambda r: r["distance_miles"])
    return results


def estimate_subway_travel_time(from_station_id, to_station_id, route,
                                subway=None):
    """Estimate travel time between two subway stations on a route.

    Uses stop sequence count * ~2 min per stop as a rough estimate.
    Returns estimated minutes or None if can't determine.
    """
    if subway is None:
        subway = _get_subway_system()
    subway.ensure_cache()

    stops = subway.load_stops()
    trips = subway.load_trips()
    stop_times = subway.load_stop_times()

    # Find parent station IDs
    parent_map = {}
    for sid, stop in stops.items():
        parent = stop.get("parent_station", "")
        if parent:
            parent_map[sid] = parent

    routes = subway.load_routes()
    route_id = None
    for rid, r in routes.items():
        if r.get("route_short_name") == route:
            route_id = rid
            break
    if not route_id:
        return None

    # Find a representative trip on this route
    target_trip = None
    for tid, trip in trips.items():
        if trip["route_id"] == route_id:
            target_trip = tid
            break
    if not target_trip:
        return None

    # Get stops for this trip in order
    trip_stops = sorted(
        [st for st in stop_times if st["trip_id"] == target_trip],
        key=lambda x: int(x["stop_sequence"])
    )

    # Map to parent stations
    from_idx = None
    to_idx = None
    for i, st in enumerate(trip_stops):
        parent = parent_map.get(st["stop_id"], st["stop_id"])
        if parent == from_station_id and from_idx is None:
            from_idx = i
        if parent == to_station_id:
            to_idx = i

    if from_idx is not None and to_idx is not None and to_idx > from_idx:
        stop_count = to_idx - from_idx
        return stop_count * 2  # ~2 min per stop average

    return None


def fetch_subway_alerts(subway=None):
    """Fetch subway service alerts."""
    if subway is None:
        subway = _get_subway_system()
    return subway.fetch_alerts()
