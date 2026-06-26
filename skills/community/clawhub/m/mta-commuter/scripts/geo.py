"""Geographic utilities for transit station proximity calculations."""

import math


def haversine_miles(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points in miles.
    Uses the Haversine formula.
    """
    R = 3958.8  # Earth's radius in miles

    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_nearby_stations(lat, lon, stops, radius_miles=3.0):
    """
    Find transit stations within radius_miles of a lat/lon point.

    Args:
        lat: Latitude of the reference point
        lon: Longitude of the reference point
        stops: Dict from load_stops() — {stop_id: {stop_name, stop_lat, stop_lon, ...}}
        radius_miles: Search radius in miles (default 3.0)

    Returns:
        List of dicts sorted by distance:
        [{"stop_id": "1", "stop_name": "...", "stop_code": "...", "distance_miles": 1.2}, ...]
    """
    results = []
    for sid, stop in stops.items():
        slat = float(stop["stop_lat"])
        slon = float(stop["stop_lon"])
        dist = haversine_miles(lat, lon, slat, slon)
        if dist <= radius_miles:
            results.append({
                "stop_id": sid,
                "stop_name": stop["stop_name"],
                "stop_code": stop.get("stop_code", ""),
                "distance_miles": round(dist, 2),
            })
    results.sort(key=lambda r: r["distance_miles"])
    return results
