"""Trip planner: find trains across nearby station pairs, with multi-leg support."""

import json
from datetime import datetime
from pathlib import Path

from geo import find_nearby_stations, haversine_miles
from gtfs import parse_gtfs_time, format_time, fuzzy_match_station, apply_realtime
from subway import (find_nearby_subway_stations, build_station_lines,
                    get_headway, compute_headways, get_time_bucket)


SCRIPTS_DIR = Path(__file__).resolve().parent
TRANSFERS_PATH = SCRIPTS_DIR / "transfers.json"

# Average walking speed for time estimates
WALK_SPEED_MPH = 3.0
MIN_PER_MILE = 60 / WALK_SPEED_MPH  # 20 min/mile


def _load_transfers():
    """Load the terminal-to-subway transfer mapping. Returns {} if missing."""
    if not TRANSFERS_PATH.exists():
        return {}
    try:
        with open(TRANSFERS_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def find_trip_options(origin_lat, origin_lon, dest_lat, dest_lon,
                      date_str, time_str=None, radius_miles=3.0,
                      origin_radius_miles=None, count=10,
                      stops=None, routes=None, trips=None,
                      stop_times=None, active_services=None, realtime=None):
    """
    Find trains across all nearby origin/destination station pairs.

    Returns list of train dicts sorted by arrival time, each with extra fields:
    origin_distance_miles, dest_distance_miles, route (branch name)
    """
    o_radius = origin_radius_miles if origin_radius_miles is not None else radius_miles
    origin_stations = find_nearby_stations(origin_lat, origin_lon, stops, o_radius)
    dest_stations = find_nearby_stations(dest_lat, dest_lon, stops, radius_miles)

    if not origin_stations or not dest_stations:
        return []

    # Build trip_stops index once
    trip_stops = {}
    for st in stop_times:
        tid = st["trip_id"]
        if tid not in trip_stops:
            trip_stops[tid] = []
        trip_stops[tid].append({
            "stop_id": st["stop_id"],
            "departure": st["departure_time"],
            "arrival": st["arrival_time"],
            "sequence": int(st["stop_sequence"]),
        })

    # Build distance lookups
    origin_dist = {s["stop_id"]: s["distance_miles"] for s in origin_stations}
    dest_dist = {s["stop_id"]: s["distance_miles"] for s in dest_stations}

    origin_ids = set(origin_dist.keys())
    dest_ids = set(dest_dist.keys())

    # Parse time filter
    target_min = None
    if time_str:
        parts = time_str.split(":")
        target_min = int(parts[0]) * 60 + int(parts[1])

    results = []
    for tid, tstops in trip_stops.items():
        trip = trips.get(tid)
        if not trip:
            continue
        if trip["service_id"] not in active_services:
            continue

        trip_origins = [ts for ts in tstops if ts["stop_id"] in origin_ids]
        trip_dests = [ts for ts in tstops if ts["stop_id"] in dest_ids]

        for o_stop in trip_origins:
            for d_stop in trip_dests:
                if int(o_stop["sequence"]) >= int(d_stop["sequence"]):
                    continue

                dep_min = parse_gtfs_time(o_stop["departure"])
                arr_min = parse_gtfs_time(d_stop["arrival"])

                if target_min is not None and dep_min < target_min:
                    continue

                route = routes.get(trip.get("route_id", ""), {})

                entry = {
                    "trip_id": tid,
                    "route": route.get("route_long_name", route.get("route_short_name", "?")),
                    "route_id": trip.get("route_id", ""),
                    "headsign": trip.get("trip_headsign", ""),
                    "depart": dep_min,
                    "depart_str": format_time(dep_min),
                    "arrive": arr_min,
                    "arrive_str": format_time(arr_min),
                    "duration": arr_min - dep_min,
                    "origin": stops[o_stop["stop_id"]]["stop_name"],
                    "origin_stop_id": o_stop["stop_id"],
                    "destination": stops[d_stop["stop_id"]]["stop_name"],
                    "dest_stop_id": d_stop["stop_id"],
                    "origin_distance_miles": origin_dist[o_stop["stop_id"]],
                    "dest_distance_miles": dest_dist[d_stop["stop_id"]],
                    "status": "Scheduled",
                    "delay_min": 0,
                }

                if realtime and tid in realtime:
                    apply_realtime(entry, realtime[tid],
                                    o_stop["stop_id"], d_stop["stop_id"], dep_min)

                results.append(entry)

    results.sort(key=lambda x: x["arrive"])
    return results[:count]


def find_alternatives(origin_name, dest_name, depart_time, date_str,
                      radius_miles=3.0, window_minutes=30, count=10,
                      stops=None, routes=None, trips=None,
                      stop_times=None, active_services=None, realtime=None):
    """
    Find alternatives to a specific train, prioritizing different branches.

    Cross-branch results (e.g., Hempstead Branch when reference is Port Jefferson)
    are ranked above same-branch nearby stops.
    """
    origin_matches = fuzzy_match_station(origin_name, stops)
    if not origin_matches:
        return []
    origin_id = origin_matches[0][0]

    dest_matches = fuzzy_match_station(dest_name, stops)
    if not dest_matches:
        return []
    dest_id = dest_matches[0][0]

    dest_stop = stops[dest_id]
    dest_lat = float(dest_stop["stop_lat"])
    dest_lon = float(dest_stop["stop_lon"])

    origin_stop = stops[origin_id]
    origin_lat = float(origin_stop["stop_lat"])
    origin_lon = float(origin_stop["stop_lon"])

    # Parse reference departure time
    parts = depart_time.split(":")
    ref_dep_min = int(parts[0]) * 60 + int(parts[1])

    # Determine reference branch
    ref_route_id = None
    for st in stop_times:
        if st["stop_id"] == dest_id:
            trip = trips.get(st["trip_id"])
            if trip:
                dep_min = parse_gtfs_time(st["departure_time"])
                if abs(dep_min - ref_dep_min) < 5:
                    ref_route_id = trip.get("route_id")
                    break

    # Compute window start as HH:MM for the time filter
    window_start_min = max(0, ref_dep_min - window_minutes)
    window_start_str = f"{window_start_min // 60}:{window_start_min % 60:02d}"

    results = find_trip_options(
        origin_lat=origin_lat, origin_lon=origin_lon,
        dest_lat=dest_lat, dest_lon=dest_lon,
        date_str=date_str,
        time_str=window_start_str,
        radius_miles=radius_miles,
        origin_radius_miles=0.5,
        count=count * 5,
        stops=stops, routes=routes, trips=trips,
        stop_times=stop_times, active_services=active_services,
        realtime=realtime,
    )

    # Filter to origin station only
    results = [r for r in results if r["origin_stop_id"] == origin_id]

    # Filter to window end
    results = [r for r in results if r["depart"] <= ref_dep_min + window_minutes]

    # Mark reference train and branch diversity
    for r in results:
        r["is_reference"] = (
            r["dest_stop_id"] == dest_id and
            r["depart"] == ref_dep_min
        )
        r["is_same_branch"] = (r.get("route_id") == ref_route_id) if ref_route_id else False

    # Sort: cross-branch first, then same-branch, each sub-sorted by arrival
    results.sort(key=lambda x: (x["is_same_branch"], x["arrive"]))
    return results[:count]


def plan_multi_leg_trip(origin_lat, origin_lon, dest_lat, dest_lon,
                        date_str, time_str=None, radius_miles=3.0, count=5,
                        systems=None):
    """
    Plan a multi-leg trip using commuter rail + subway.

    Args:
        origin_lat, origin_lon: Starting point
        dest_lat, dest_lon: Destination
        date_str: YYYY-MM-DD
        time_str: HH:MM (24h)
        radius_miles: Search radius for commuter rail stations
        count: Max results
        systems: Dict of {key: GtfsSystem} for commuter rail systems to search

    Returns list of journey dicts, each with:
        legs: list of leg dicts (commuter_rail, subway, walk)
        total_duration_min: estimated total time
        system: which commuter rail system
    """
    if not systems:
        return []

    transfers = _load_transfers()
    subway_stations = build_station_lines()
    headways = compute_headways()

    # Parse time for bucket
    if time_str:
        hour = int(time_str.split(":")[0])
    else:
        hour = datetime.now().hour
    time_bucket = get_time_bucket(hour)

    # Check if destination is near a commuter rail station (direct trip)
    # or needs a subway connection
    all_journeys = []

    for sys_key, system in systems.items():
        system.ensure_cache()
        stops = system.load_stops()
        routes = system.load_routes()
        trips = system.load_trips()
        stop_times = system.load_stop_times()
        active_services = system.load_active_services(date_str)

        now = datetime.now()
        realtime = None
        is_today = date_str == now.strftime("%Y-%m-%d")
        if is_today:
            realtime = system.fetch_realtime()

        # Try direct commuter rail trip
        direct_results = find_trip_options(
            origin_lat, origin_lon, dest_lat, dest_lon,
            date_str, time_str, radius_miles=radius_miles,
            count=count,
            stops=stops, routes=routes, trips=trips,
            stop_times=stop_times, active_services=active_services,
            realtime=realtime,
        )

        for r in direct_results:
            walk_dist = r["dest_distance_miles"]
            walk_min = round(walk_dist * MIN_PER_MILE)
            all_journeys.append({
                "system": sys_key,
                "legs": [
                    {
                        "type": "commuter_rail",
                        "system": system.short_name,
                        "from": r["origin"],
                        "to": r["destination"],
                        "depart": r["depart"],
                        "depart_str": r["depart_str"],
                        "arrive": r["arrive"],
                        "arrive_str": r["arrive_str"],
                        "duration": r["duration"],
                        "route": r["route"],
                        "status": r["status"],
                    },
                    {
                        "type": "walk",
                        "description": f"Walk to destination ({walk_dist:.1f} mi)",
                        "duration": walk_min,
                    },
                ],
                "total_duration_min": r["duration"] + walk_min,
                "depart": r["depart"],
                "depart_str": r["depart_str"],
            })

        # Try commuter rail to terminal + subway connection
        # Find which terminal stations are near the origin
        terminal_results = {}
        for terminal_name, transfer_info in transfers.items():
            if sys_key not in transfer_info.get("commuter_rail", []):
                continue

            # Find this terminal in the GTFS stops
            terminal_matches = fuzzy_match_station(terminal_name, stops)
            if not terminal_matches:
                continue
            terminal_id = terminal_matches[0][0]
            terminal_stop = stops[terminal_id]
            terminal_lat = float(terminal_stop["stop_lat"])
            terminal_lon = float(terminal_stop["stop_lon"])

            # Find trains from origin area to this terminal
            rail_options = find_trip_options(
                origin_lat, origin_lon,
                terminal_lat, terminal_lon,
                date_str, time_str,
                radius_miles=radius_miles,
                origin_radius_miles=None,
                count=count,
                stops=stops, routes=routes, trips=trips,
                stop_times=stop_times, active_services=active_services,
                realtime=realtime,
            )

            # For each rail option, find subway connection to destination
            for rail in rail_options:
                # Check if destination is close enough to walk from terminal
                terminal_to_dest = haversine_miles(
                    terminal_lat, terminal_lon, dest_lat, dest_lon
                )
                if terminal_to_dest < 0.5:
                    # Close enough to walk, no subway needed
                    continue  # already covered by direct results

                # Find subway stations near the destination
                dest_subway = find_nearby_subway_stations(
                    dest_lat, dest_lon, radius_miles=1.0,
                    station_lines=subway_stations,
                )
                if not dest_subway:
                    continue

                # Find which subway lines are available from this terminal
                available_lines = set()
                walk_to_subway_min = 5  # default
                for sub_station in transfer_info.get("subway_stations", []):
                    available_lines.update(sub_station["lines"])
                    walk_to_subway_min = min(
                        walk_to_subway_min, sub_station["walk_min"]
                    )

                # Find best subway connection: a line that serves both
                # the terminal and a station near the destination
                best_subway = None
                for dest_sub in dest_subway:
                    common_lines = available_lines & set(dest_sub["lines"])
                    if common_lines:
                        line = sorted(common_lines)[0]
                        headway_min = get_headway(
                            line, dest_sub["stop_id"], time_bucket, headways
                        )
                        # Estimate travel time from terminal to destination
                        # subway stop by distance (~17 mph average for subway)
                        dist = haversine_miles(
                            terminal_lat, terminal_lon,
                            dest_sub["lat"], dest_sub["lon"],
                        )
                        travel_min = round(dist * 3.5)

                        walk_from_subway = round(
                            dest_sub["distance_miles"] * MIN_PER_MILE
                        )

                        best_subway = {
                            "line": line,
                            "dest_station": dest_sub["name"],
                            "headway_min": headway_min,
                            "travel_min": travel_min,
                            "walk_from_subway_min": walk_from_subway,
                            "all_lines": sorted(common_lines),
                        }
                        break

                if not best_subway:
                    continue

                # Build multi-leg journey
                subway_wait = best_subway["headway_min"] or 5
                total = (
                    rail["duration"]
                    + walk_to_subway_min
                    + subway_wait / 2  # average wait = half headway
                    + best_subway["travel_min"]
                    + best_subway["walk_from_subway_min"]
                )

                headway_str = (
                    f"~every {best_subway['headway_min']:.0f} min"
                    if best_subway["headway_min"]
                    else "frequency unknown"
                )

                legs = [
                    {
                        "type": "commuter_rail",
                        "system": system.short_name,
                        "from": rail["origin"],
                        "to": rail["destination"],
                        "depart": rail["depart"],
                        "depart_str": rail["depart_str"],
                        "arrive": rail["arrive"],
                        "arrive_str": rail["arrive_str"],
                        "duration": rail["duration"],
                        "route": rail["route"],
                        "status": rail["status"],
                    },
                    {
                        "type": "walk",
                        "description": f"Walk to {best_subway['line']} train ({walk_to_subway_min} min)",
                        "duration": walk_to_subway_min,
                    },
                    {
                        "type": "subway",
                        "line": best_subway["line"],
                        "all_lines": best_subway["all_lines"],
                        "to": best_subway["dest_station"],
                        "duration": best_subway["travel_min"],
                        "headway": headway_str,
                    },
                ]

                if best_subway["walk_from_subway_min"] > 1:
                    legs.append({
                        "type": "walk",
                        "description": f"Walk to destination ({best_subway['walk_from_subway_min']} min)",
                        "duration": best_subway["walk_from_subway_min"],
                    })

                all_journeys.append({
                    "system": sys_key,
                    "legs": legs,
                    "total_duration_min": round(total),
                    "depart": rail["depart"],
                    "depart_str": rail["depart_str"],
                })

    # Sort by departure time, then total duration
    all_journeys.sort(key=lambda j: (j["depart"], j["total_duration_min"]))

    # Deduplicate: if a direct trip and a multi-leg trip use the same
    # commuter rail leg, keep the shorter total duration
    seen = set()
    unique = []
    for j in all_journeys:
        rail_leg = j["legs"][0]
        key = (rail_leg["depart"], rail_leg["from"], rail_leg["to"])
        if key not in seen:
            seen.add(key)
            unique.append(j)

    return unique[:count]
