#!/usr/bin/env python3
"""
NYC Commuter Transit Tool

Unified CLI for LIRR, Metro-North, and NYC Subway trip planning.

Usage:
    mta.py lirr "Penn Station" "New Hyde Park" --time 17:00
    mta.py mnr "Grand Central" "White Plains" --time 17:00
    mta.py trip --near-origin work --near-dest home --time 17:00
    mta.py stations nearby --near home
    mta.py alerts
    mta.py alerts --system lirr
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from gtfs import GtfsSystem, parse_gtfs_time, format_time, fuzzy_match_station

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
DATA_DIR = SKILL_DIR / "data"
FEEDS_PATH = SCRIPTS_DIR / "feeds.json"


def _load_feeds():
    """Load feed configs from feeds.json."""
    if not FEEDS_PATH.exists():
        print(f"Error: missing config file {FEEDS_PATH}. "
              f"Reinstall the skill or check your install.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(FEEDS_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {FEEDS_PATH} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def _get_system(key):
    """Create a GtfsSystem for a given feed key."""
    feeds = _load_feeds()
    if key not in feeds:
        print(f"Error: unknown system '{key}'. Available: {', '.join(feeds.keys())}",
              file=sys.stderr)
        sys.exit(1)
    return GtfsSystem.from_config(key, feeds[key], DATA_DIR)


def _get_commuter_rail_systems():
    """Get all commuter rail GtfsSystems."""
    feeds = _load_feeds()
    systems = {}
    for key, config in feeds.items():
        if config.get("type") == "commuter_rail":
            systems[key] = GtfsSystem.from_config(key, config, DATA_DIR)
    return systems


def _handle_system_lookup(system_key, argv):
    """Handle: mta.py lirr|mnr "origin" "dest" [options]"""
    system = _get_system(system_key)

    parser = argparse.ArgumentParser(
        prog=f"mta.py {system_key}",
        description=f"Look up {system.name} train schedules."
    )
    parser.add_argument("origin", nargs="?", help="Origin station name or code")
    parser.add_argument("destination", nargs="?", help="Destination station name or code")
    parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD, default: today)")
    parser.add_argument("--time", "-t", help="Time (HH:MM 24h, default: now)")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of results")
    parser.add_argument("--stations", action="store_true", help="List all stations")
    parser.add_argument("--routes", action="store_true", help="List all routes/branches")
    parser.add_argument("--alerts", action="store_true", help="Show service alerts")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-live", action="store_true", help="Skip real-time data")
    parser.add_argument("--find-station", help="Search for a station")

    args = parser.parse_args(argv)
    system.ensure_cache()

    if args.stations:
        stops = system.load_stops()
        stations = [(s["stop_name"], s.get("stop_code", ""), sid)
                     for sid, s in stops.items()]
        stations.sort()
        for name, code, sid in stations:
            print(f"  {code:<5} {name}")
        return

    if args.routes:
        routes = system.load_routes()
        for rid, r in routes.items():
            long_name = r.get("route_long_name", "")
            short_name = r.get("route_short_name", "")
            print(f"  {short_name:<10} {long_name}")
        return

    if args.alerts:
        alerts = system.fetch_alerts()
        if not alerts:
            print(f"No active {system.short_name} alerts.")
            return
        if args.json:
            print(json.dumps(alerts, indent=2))
            return
        print(f"{system.short_name} Service Alerts ({len(alerts)})\n")
        for i, a in enumerate(alerts, 1):
            print(f"{i}. {a['header']}")
            if a["description"]:
                desc = a["description"][:200]
                if len(a["description"]) > 200:
                    desc += "..."
                print(f"   {desc}")
            print()
        return

    if args.find_station:
        stops = system.load_stops()
        matches = fuzzy_match_station(args.find_station, stops)
        if args.json:
            print(json.dumps([
                {"stop_id": sid, "name": name,
                 "code": stops[sid].get("stop_code", ""), "score": score}
                for sid, name, score in matches[:10]
            ], indent=2))
            return
        if not matches:
            print(f"No stations matching '{args.find_station}'")
        else:
            for sid, name, score in matches[:10]:
                code = stops[sid].get("stop_code", "")
                print(f"  {code:<5} {name} (score: {score})")
        return

    if not args.origin or not args.destination:
        parser.print_help()
        return

    stops = system.load_stops()
    origin_matches = fuzzy_match_station(args.origin, stops)
    if not origin_matches:
        print(f"No station found matching '{args.origin}'.")
        return
    origin_id, origin_name, _ = origin_matches[0]

    dest_matches = fuzzy_match_station(args.destination, stops)
    if not dest_matches:
        print(f"No station found matching '{args.destination}'.")
        return
    dest_id, dest_name, _ = dest_matches[0]

    now = datetime.now()
    date_str = args.date or now.strftime("%Y-%m-%d")
    time_str = args.time or now.strftime("%H:%M")

    realtime = None
    if not args.no_live and date_str == now.strftime("%Y-%m-%d"):
        realtime = system.fetch_realtime()

    trains = system.find_trains(origin_id, dest_id, date_str, time_str,
                                args.count, realtime)

    if args.json:
        print(json.dumps(trains, indent=2))
        return

    if not trains:
        print(f"No {system.short_name} trains from {origin_name} to {dest_name} "
              f"at/after {format_time(parse_gtfs_time(time_str + ':00'))}")
        return

    day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
    print(f"{system.short_name} trains from {origin_name} to {dest_name}")
    print(f"{day_name} {date_str}, at/after {format_time(parse_gtfs_time(time_str + ':00'))}")
    if realtime is not None:
        print("(with real-time data)")
    print()

    print(f"{'Depart':<10} {'Arrive':<10} {'Duration':<10} {'Branch':<25} {'To'}")
    print("-" * 75)
    for t in trains:
        dur = f"{t['duration']}min"
        print(f"{t['depart_str']:<10} {t['arrive_str']:<10} {dur:<10} "
              f"{t['route']:<25} {t['headsign']}")


def _handle_trip(argv):
    """Handle: mta.py trip --near-origin X --near-dest Y [options]"""
    from locations import resolve_location
    from trip import plan_multi_leg_trip

    parser = argparse.ArgumentParser(
        prog="mta.py trip",
        description="Plan a multi-leg commute across LIRR, Metro-North, and Subway."
    )
    parser.add_argument("--near-origin", required=True,
                        help="Origin: saved location name or lat,lon")
    parser.add_argument("--near-dest", required=True,
                        help="Destination: saved location name or lat,lon")
    parser.add_argument("--time", "-t", help="Depart at/after time (HH:MM 24h, default: now)")
    parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD, default: today)")
    parser.add_argument("--radius", type=float, default=3.0,
                        help="Search radius in miles (default: 3)")
    parser.add_argument("--count", "-n", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    origin_lat, origin_lon, origin_label = resolve_location(args.near_origin)
    dest_lat, dest_lon, dest_label = resolve_location(args.near_dest)

    now = datetime.now()
    date_str = args.date or now.strftime("%Y-%m-%d")
    time_str = args.time or now.strftime("%H:%M")

    systems = _get_commuter_rail_systems()

    journeys = plan_multi_leg_trip(
        origin_lat, origin_lon, dest_lat, dest_lon,
        date_str, time_str,
        radius_miles=args.radius, count=args.count,
        systems=systems,
    )

    if args.json:
        print(json.dumps(journeys, indent=2))
        return

    if not journeys:
        print(f"No transit options found from {origin_label} to {dest_label}")
        return

    print(f"Transit options from {origin_label} to {dest_label}")
    print(f"Departing after {format_time(parse_gtfs_time(time_str + ':00'))}\n")

    for i, j in enumerate(journeys, 1):
        total = j["total_duration_min"]
        print(f"Option {i} (~{total} min total):")
        for leg in j["legs"]:
            if leg["type"] == "commuter_rail":
                print(f"  {leg['depart_str']}  {leg['system']} {leg['from']} -> "
                      f"{leg['to']} ({leg['duration']}min, {leg['route']})")
            elif leg["type"] == "subway":
                lines_str = "/".join(leg.get("all_lines", [leg["line"]]))
                print(f"  {lines_str} train to {leg['to']} "
                      f"(~{leg['duration']}min, {leg['headway']})")
            elif leg["type"] == "walk":
                print(f"  {leg['description']}")
        print()


def _handle_stations_nearby(argv):
    """Handle: mta.py stations nearby --near X [options]"""
    from locations import resolve_location
    from geo import find_nearby_stations as find_nearby_rail
    from subway import find_nearby_subway_stations, build_station_lines

    parser = argparse.ArgumentParser(
        prog="mta.py stations nearby",
        description="Find transit stations near a location."
    )
    parser.add_argument("--near", help="Saved location name or lat,lon")
    parser.add_argument("--lat", type=float, help="Latitude")
    parser.add_argument("--lon", type=float, help="Longitude")
    parser.add_argument("--radius", type=float, default=3.0,
                        help="Search radius in miles (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    if args.near:
        lat, lon, label = resolve_location(args.near)
    elif args.lat is not None and args.lon is not None:
        lat, lon, label = args.lat, args.lon, f"{args.lat},{args.lon}"
    else:
        print("Error: provide --near <location> or --lat/--lon", file=sys.stderr)
        sys.exit(1)

    all_results = []

    # Commuter rail stations
    systems = _get_commuter_rail_systems()
    for sys_key, system in systems.items():
        system.ensure_cache()
        stops = system.load_stops()
        nearby = find_nearby_rail(lat, lon, stops, radius_miles=args.radius)
        for r in nearby:
            r["system"] = system.short_name
        all_results.extend(nearby)

    # Subway stations (smaller radius — there are a lot of them)
    subway_radius = min(args.radius, 1.5)
    subway_stations = build_station_lines()
    subway_nearby = find_nearby_subway_stations(
        lat, lon, radius_miles=subway_radius, station_lines=subway_stations
    )
    for s in subway_nearby:
        all_results.append({
            "stop_id": s["stop_id"],
            "stop_name": s["name"],
            "distance_miles": s["distance_miles"],
            "system": "Subway",
            "lines": s["lines"],
        })

    all_results.sort(key=lambda r: r["distance_miles"])

    if args.json:
        print(json.dumps(all_results, indent=2, default=list))
        return

    if not all_results:
        print(f"No stations within {args.radius} mi of {label}")
        return

    print(f"Stations near {label} ({lat}, {lon}):\n")
    for r in all_results:
        system = r.get("system", "")
        lines = r.get("lines", [])
        lines_str = f"  ({', '.join(lines)})" if lines else ""
        print(f"  [{system:<6}] {r['stop_name']:<30} {r['distance_miles']:.1f} mi{lines_str}")


def _handle_alerts(argv):
    """Handle: mta.py alerts [--system X]"""
    parser = argparse.ArgumentParser(
        prog="mta.py alerts",
        description="Show MTA service alerts."
    )
    parser.add_argument("--system", "-s",
                        help="Filter by system (lirr, mnr, subway). Shows all if omitted.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args(argv)

    feeds = _load_feeds()
    all_alerts = []

    for key, config in feeds.items():
        if args.system and key != args.system:
            continue
        system = GtfsSystem.from_config(key, config, DATA_DIR)
        alerts = system.fetch_alerts()
        for a in alerts:
            a["system"] = config["short_name"]
        all_alerts.extend(alerts)

    if args.json:
        print(json.dumps(all_alerts, indent=2))
        return

    if not all_alerts:
        label = f"{args.system}" if args.system else "MTA"
        print(f"No active {label} alerts.")
        return

    print(f"MTA Service Alerts ({len(all_alerts)})\n")
    for i, a in enumerate(all_alerts, 1):
        print(f"{i}. [{a['system']}] {a['header']}")
        if a["description"]:
            desc = a["description"][:200]
            if len(a["description"]) > 200:
                desc += "..."
            print(f"   {desc}")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: mta.py <command> [options]")
        print()
        print("Commands:")
        print("  lirr <origin> <dest>     LIRR schedule lookup")
        print("  mnr <origin> <dest>      Metro-North schedule lookup")
        print("  trip --near-origin X     Multi-leg trip planner")
        print("  stations nearby --near X Find nearby stations (all systems)")
        print("  alerts                   Service alerts (all systems)")
        return

    cmd = sys.argv[1]

    if cmd in ("lirr", "mnr"):
        _handle_system_lookup(cmd, sys.argv[2:])
    elif cmd == "trip":
        _handle_trip(sys.argv[2:])
    elif cmd == "stations":
        if len(sys.argv) > 2 and sys.argv[2] == "nearby":
            _handle_stations_nearby(sys.argv[3:])
        else:
            print("Usage: mta.py stations nearby --near <location>")
    elif cmd == "alerts":
        _handle_alerts(sys.argv[2:])
    else:
        print(f"Unknown command: {cmd}")
        print("Available: lirr, mnr, trip, stations, alerts")
        sys.exit(1)


if __name__ == "__main__":
    main()
