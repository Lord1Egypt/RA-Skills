#!/usr/bin/env python3
"""
mbta.py — MBTA V3 API CLI tool for OpenClaw

Usage:
  python3 mbta.py departures <stop_name_or_id> [limit]
  python3 mbta.py alerts [--stop <stop_id>] [--route <route_id>]
  python3 mbta.py vehicles <route_id>
  python3 mbta.py stops <search_term>
  python3 mbta.py routes [--type <type>]

Set MBTA_API_KEY env var for higher rate limits.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

BASE_URL = "https://api-v3.mbta.com"
API_KEY = os.environ.get("MBTA_API_KEY", "")

ROUTE_TYPES = {
    0: "Light Rail",
    1: "Heavy Rail (Subway)",
    2: "Commuter Rail",
    3: "Bus",
    4: "Ferry",
}


def make_request(path: str, params: dict = None) -> dict:
    """Make a GET request to the MBTA V3 API."""
    if params is None:
        params = {}
    if API_KEY:
        params["api_key"] = API_KEY

    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={"Accept": "application/vnd.api+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ HTTP {e.code}: {e.reason}", file=sys.stderr)
        try:
            err = json.loads(body)
            for error in err.get("errors", []):
                print(f"   {error.get('title', '')}: {error.get('detail', '')}", file=sys.stderr)
        except Exception:
            print(f"   {body[:200]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def format_time(iso_str: str) -> str:
    """Format an ISO 8601 time string to a human-readable local time."""
    if not iso_str:
        return "—"
    try:
        # Parse with timezone
        dt = datetime.fromisoformat(iso_str)
        # Convert to local-ish display (keep as-is with offset)
        return dt.strftime("%-I:%M %p")
    except Exception:
        return iso_str


def cmd_stops(search_term: str):
    """Search for stops by name (client-side filter over parent stations)."""
    print(f"🔍 Searching for stops matching: {search_term!r}\n")
    # MBTA API doesn't support filter[name], so fetch parent stations and filter locally.
    # location_type=1 = parent stations (275 total — manageable)
    data = make_request("/stops", {
        "filter[location_type]": "1",
        "fields[stops]": "name,description,municipality,platform_name,location_type",
    })
    all_stops = data.get("data", [])
    search_lower = search_term.lower()
    stops = [s for s in all_stops if search_lower in s.get("attributes", {}).get("name", "").lower()]

    if not stops:
        # Widen to all stop types if no parent stations matched
        data2 = make_request("/stops", {
            "filter[location_type]": "0",
            "fields[stops]": "name,description,municipality,platform_name,location_type",
        })
        all_stops2 = data2.get("data", [])
        stops = [s for s in all_stops2 if search_lower in s.get("attributes", {}).get("name", "").lower()]
        if not stops:
            print("No stops found matching that name.")
            return

    print(f"Found {len(stops)} stop(s):\n")
    for stop in stops[:20]:  # cap at 20 results
        attr = stop.get("attributes", {})
        sid = stop.get("id", "")
        name = attr.get("name", "Unknown")
        desc = attr.get("description", "")
        muni = attr.get("municipality", "")
        platform = attr.get("platform_name", "")
        loc_type = attr.get("location_type", 0)
        type_label = {0: "Stop/Platform", 1: "Station", 2: "Entrance/Exit", 3: "Generic Node", 4: "Boarding Area"}.get(loc_type, "Stop")

        print(f"  Stop ID : {sid}")
        print(f"  Name    : {name}")
        if desc:
            print(f"  Desc    : {desc}")
        if platform:
            print(f"  Platform: {platform}")
        if muni:
            print(f"  City    : {muni}")
        print(f"  Type    : {type_label}")
        print()


def resolve_stop_id(stop_name_or_id: str) -> str:
    """If argument looks like an ID, return as-is; otherwise search by name."""
    import re
    if re.match(r'^[a-zA-Z0-9_\-]+$', stop_name_or_id) and ' ' not in stop_name_or_id:
        # Looks like an ID (no spaces) — return directly
        return stop_name_or_id
    # Has spaces — treat as a name search over parent stations
    data = make_request("/stops", {
        "filter[location_type]": "1",
        "fields[stops]": "name",
    })
    all_stops = data.get("data", [])
    search_lower = stop_name_or_id.lower()
    matches = [s for s in all_stops if search_lower in s.get("attributes", {}).get("name", "").lower()]
    if not matches:
        print(f"❌ No stops found matching: {stop_name_or_id!r}", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"ℹ️  Multiple stops matched '{stop_name_or_id}'. Using: {matches[0]['attributes']['name']} (ID: {matches[0]['id']})", file=sys.stderr)
    else:
        print(f"ℹ️  Resolved '{stop_name_or_id}' → {matches[0]['attributes']['name']} (ID: {matches[0]['id']})", file=sys.stderr)
    return matches[0]["id"]


def cmd_departures(stop_arg: str, limit: int = 10):
    """Show next departures from a stop. Uses real-time predictions, falls back to schedule."""
    stop_id = resolve_stop_id(stop_arg)
    print(f"🚌 Next {limit} departures from stop: {stop_id}\n")

    now = datetime.now(timezone.utc)

    # --- Try real-time predictions first ---
    data = make_request("/predictions", {
        "filter[stop]": stop_id,
        "sort": "departure_time",
        "include": "route,trip,stop",
        "fields[predictions]": "departure_time,arrival_time,direction_id,status,stop_sequence",
        "fields[routes]": "long_name,short_name,type",
        "fields[trips]": "headsign,direction_id",
        "fields[stops]": "name,platform_name",
    })

    predictions = data.get("data", [])
    included = {f"{item['type']}/{item['id']}": item for item in data.get("included", [])}

    if predictions:
        source = "real-time"
        items = predictions
    else:
        # --- Fall back to schedule ---
        print("ℹ️  No real-time predictions — showing scheduled departures.\n")
        source = "schedule"
        min_time = now.strftime("%H:%M")
        sched_data = make_request("/schedules", {
            "filter[stop]": stop_id,
            "filter[min_time]": min_time,
            "sort": "departure_time",
            "include": "route,trip",
            "fields[schedules]": "departure_time,arrival_time,direction_id,stop_sequence",
            "fields[routes]": "long_name,short_name,type",
            "fields[trips]": "headsign,direction_id",
            "page[limit]": str(limit * 2),
        })
        items = sched_data.get("data", [])
        included = {f"{item['type']}/{item['id']}": item for item in sched_data.get("included", [])}

    if not items:
        print("No upcoming departures found.")
        print("Tip: Try searching for a stop ID with: python3 mbta.py stops <name>")
        return

    count = 0
    for item in items:
        if count >= limit:
            break
        attr = item.get("attributes", {})
        rels = item.get("relationships", {})

        dep_time = attr.get("departure_time") or attr.get("arrival_time")
        if not dep_time:
            continue

        # Skip past departures (schedules may include them)
        try:
            dep_dt = datetime.fromisoformat(dep_time)
            if dep_dt < now:
                continue
        except Exception:
            pass

        status = attr.get("status", "")

        # Resolve route
        route_id = rels.get("route", {}).get("data", {}).get("id", "")
        route_key = f"route/{route_id}"
        route = included.get(route_key, {}).get("attributes", {})
        route_name = route.get("short_name") or route.get("long_name") or route_id
        route_type = ROUTE_TYPES.get(route.get("type"), "Transit")

        # Resolve trip/headsign
        trip_id = rels.get("trip", {}).get("data", {}).get("id", "")
        trip_key = f"trip/{trip_id}"
        trip = included.get(trip_key, {}).get("attributes", {})
        headsign = trip.get("headsign", "")

        time_str = format_time(dep_time)

        print(f"  {time_str:>10}  |  {route_type}: {route_name:<12}  |  → {headsign}")
        if status:
            print(f"              Status: {status}")
        count += 1

    if count == 0:
        print("No upcoming departures found.")
    else:
        label = "🟢 Live" if source == "real-time" else "🗓️  Scheduled"
        print(f"\n  {label}")


def cmd_alerts(stop_id: str = None, route_id: str = None):
    """Show active service alerts."""
    params = {
        "filter[activity]": "BOARD,EXIT,RIDE",
        "fields[alerts]": "header,description,severity,effect,lifecycle,updated_at,informed_entity",
    }
    label_parts = []
    if stop_id:
        params["filter[stop]"] = stop_id
        label_parts.append(f"stop {stop_id}")
    if route_id:
        params["filter[route]"] = route_id
        label_parts.append(f"route {route_id}")

    label = " / ".join(label_parts) if label_parts else "all routes"
    print(f"🚨 Active alerts for: {label}\n")

    data = make_request("/alerts", params)
    alerts = data.get("data", [])

    if not alerts:
        print("✅ No active alerts. Service appears to be running normally.")
        return

    print(f"Found {len(alerts)} active alert(s):\n")
    for alert in alerts:
        attr = alert.get("attributes", {})
        header = attr.get("header", "No header")
        desc = attr.get("description", "")
        severity = attr.get("severity", 0)
        effect = attr.get("effect", "")
        lifecycle = attr.get("lifecycle", "")
        updated = attr.get("updated_at", "")

        severity_label = "🔴" if severity >= 7 else "🟡" if severity >= 4 else "🔵"

        print(f"{severity_label} [{effect}] {header}")
        if lifecycle:
            print(f"   Lifecycle: {lifecycle}")
        if updated:
            try:
                dt = datetime.fromisoformat(updated)
                updated_fmt = dt.strftime("%b %-d, %-I:%M %p")
                print(f"   Updated  : {updated_fmt}")
            except Exception:
                print(f"   Updated  : {updated}")
        if desc:
            # Truncate long descriptions
            desc_short = desc[:300] + "..." if len(desc) > 300 else desc
            print(f"   Details  : {desc_short}")
        print()


def cmd_vehicles(route_id: str):
    """Show current vehicle positions for a route."""
    print(f"🚍 Current vehicles on route: {route_id}\n")

    data = make_request("/vehicles", {
        "filter[route]": route_id,
        "include": "stop,trip",
        "fields[vehicles]": "label,current_status,direction_id,speed,updated_at,occupancy_status,carriages",
        "fields[stops]": "name",
        "fields[trips]": "headsign",
    })

    vehicles = data.get("data", [])
    included = {f"{item['type']}/{item['id']}": item for item in data.get("included", [])}

    if not vehicles:
        print(f"No vehicles currently tracked on route {route_id}.")
        print("Route may not be running, or real-time tracking isn't available.")
        return

    print(f"Tracking {len(vehicles)} vehicle(s):\n")
    for v in vehicles:
        attr = v.get("attributes", {})
        rels = v.get("relationships", {})

        label = attr.get("label", v.get("id", "?"))
        status = attr.get("current_status", "")
        direction_id = attr.get("direction_id", 0)
        speed = attr.get("speed")
        occupancy = attr.get("occupancy_status", "")
        updated = attr.get("updated_at", "")

        # Resolve current stop (API type is "stop" singular)
        stop_id = rels.get("stop", {}).get("data", {}).get("id", "")
        stop_key = f"stop/{stop_id}"
        stop_name = included.get(stop_key, {}).get("attributes", {}).get("name", stop_id or "Unknown")

        # Resolve trip/headsign (API type is "trip" singular)
        trip_id = rels.get("trip", {}).get("data", {}).get("id", "")
        trip_key = f"trip/{trip_id}"
        headsign = included.get(trip_key, {}).get("attributes", {}).get("headsign", "")

        status_map = {
            "INCOMING_AT": "Incoming at",
            "STOPPED_AT": "Stopped at",
            "IN_TRANSIT_TO": "In transit to",
        }
        status_label = status_map.get(status, status)

        dir_label = f"Direction {direction_id}"

        print(f"  Vehicle #{label}")
        print(f"    Heading  : {headsign or dir_label}")
        print(f"    Status   : {status_label} {stop_name}")
        if speed is not None:
            print(f"    Speed    : {speed} mph")
        if occupancy and occupancy != "NO_DATA_AVAILABLE":
            occ_map = {
                "MANY_SEATS_AVAILABLE": "Many seats available",
                "FEW_SEATS_AVAILABLE": "Few seats available",
                "STANDING_ROOM_ONLY": "Standing room only",
                "CRUSHED_STANDING_ROOM_ONLY": "Very crowded",
                "FULL": "Full",
                "NOT_ACCEPTING_PASSENGERS": "Not accepting passengers",
            }
            print(f"    Occupancy: {occ_map.get(occupancy, occupancy)}")
        if updated:
            try:
                dt = datetime.fromisoformat(updated)
                print(f"    Updated  : {dt.strftime('%-I:%M:%S %p')}")
            except Exception:
                print(f"    Updated  : {updated}")
        print()


def cmd_routes(route_type: str = None):
    """List all routes, optionally filtered by type."""
    params = {"fields[routes]": "short_name,long_name,type,description,color"}
    if route_type is not None:
        params["filter[type]"] = route_type

    type_label = ROUTE_TYPES.get(int(route_type), f"type {route_type}") if route_type else "all"
    print(f"🗺️  MBTA Routes ({type_label}):\n")

    data = make_request("/routes", params)
    routes = data.get("data", [])

    if not routes:
        print("No routes found.")
        return

    # Group by type
    by_type = {}
    for r in routes:
        rt = r.get("attributes", {}).get("type", 3)
        by_type.setdefault(rt, []).append(r)

    for rt in sorted(by_type.keys()):
        print(f"  {ROUTE_TYPES.get(rt, f'Type {rt}')}:")
        for r in by_type[rt]:
            attr = r.get("attributes", {})
            short = attr.get("short_name", "")
            long = attr.get("long_name", "")
            name = f"{short} — {long}" if short and long and short != long else (long or short or r["id"])
            print(f"    {r['id']:20s}  {name}")
        print()


def print_usage():
    print(__doc__)
    print("Commands:")
    print("  departures <stop_name_or_id> [limit=10]  — Next departures from a stop")
    print("  alerts [--stop <id>] [--route <id>]      — Active service alerts")
    print("  vehicles <route_id>                      — Current vehicle positions")
    print("  stops <search_term>                      — Search for stops by name")
    print("  routes [--type 0|1|2|3|4]               — List routes (0=LR,1=HR,2=CR,3=Bus,4=Ferry)")
    print()
    print("Examples:")
    print("  python3 mbta.py stops 'South Station'")
    print("  python3 mbta.py departures place-sstat 5")
    print("  python3 mbta.py departures 'Back Bay' 10")
    print("  python3 mbta.py alerts --route Red")
    print("  python3 mbta.py alerts --stop place-sstat")
    print("  python3 mbta.py vehicles Red")
    print("  python3 mbta.py routes --type 1")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
        return

    cmd = args[0]

    if cmd == "stops":
        if len(args) < 2:
            print("Usage: python3 mbta.py stops <search_term>", file=sys.stderr)
            sys.exit(1)
        cmd_stops(" ".join(args[1:]))

    elif cmd == "departures":
        if len(args) < 2:
            print("Usage: python3 mbta.py departures <stop_name_or_id> [limit]", file=sys.stderr)
            sys.exit(1)
        stop = args[1]
        limit = int(args[2]) if len(args) > 2 else 10
        cmd_departures(stop, limit)

    elif cmd == "alerts":
        stop_id = None
        route_id = None
        i = 1
        while i < len(args):
            if args[i] == "--stop" and i + 1 < len(args):
                stop_id = args[i + 1]
                i += 2
            elif args[i] == "--route" and i + 1 < len(args):
                route_id = args[i + 1]
                i += 2
            else:
                # Positional: first = stop, second = route (legacy)
                if stop_id is None:
                    stop_id = args[i]
                elif route_id is None:
                    route_id = args[i]
                i += 1
        cmd_alerts(stop_id, route_id)

    elif cmd == "vehicles":
        if len(args) < 2:
            print("Usage: python3 mbta.py vehicles <route_id>", file=sys.stderr)
            sys.exit(1)
        cmd_vehicles(args[1])

    elif cmd == "routes":
        route_type = None
        i = 1
        while i < len(args):
            if args[i] == "--type" and i + 1 < len(args):
                route_type = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_routes(route_type)

    else:
        print(f"Unknown command: {cmd!r}", file=sys.stderr)
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
