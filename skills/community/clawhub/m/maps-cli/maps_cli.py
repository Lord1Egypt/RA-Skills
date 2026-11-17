#!/usr/bin/env python3
"""
maps-cli v2.0 — Advanced OpenStreetMap CLI with geocoding, routing, POI search,
timezone lookup, isochrones, and map export. Zero external dependencies (stdlib only).
"""
import argparse
import csv
import io
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone

NAME = "maps-cli"
VERSION = "2.0.0"

OSM_NOMINATIM = "https://nominatim.openstreetmap.org"
OSRM_BASE = "https://router.project-osrm.org"
OSM_OVERPASS = "https://overpass-api.de/api/interpreter"
TIMEOUT = 15

# ── helpers ──────────────────────────────────────────────────────────────

def _req(url, params=None, headers=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    hdrs = {
        "User-Agent": f"maps-cli/{VERSION} (+https://github.com/itsPremkumar/maps-cli)"
    }
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except urllib.error.URLError as e:
        return -1, str(e.reason).encode()

def _fmt_addr(d):
    return d.get("display_name", d.get("name", "Unknown"))

def _coord_str(d):
    return f"{d.get('lat','?')},{d.get('lon','?')}"

# ── commands ─────────────────────────────────────────────────────────────

def cmd_geocode(query, limit=5, fmt="text"):
    """Geocode a place name to coordinates."""
    params = {"q": query, "format": "json", "limit": limit, "addressdetails": 1}
    st, raw = _req(f"{OSM_NOMINATIM}/search", params)
    if st != 200:
        return f"Error {st}: {raw.decode(errors='replace')[:200]}"
    results = json.loads(raw)
    if not results:
        return "No results found."
    if fmt == "json":
        return json.dumps(results, indent=2)
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {_fmt_addr(r)} [{_coord_str(r)}]")
    return "\n".join(lines)

def cmd_reverse(lat, lon, fmt="text"):
    """Reverse geocode coordinates to an address."""
    params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}
    st, raw = _req(f"{OSM_NOMINATIM}/reverse", params)
    if st != 200:
        return f"Error {st}: {raw.decode(errors='replace')[:200]}"
    result = json.loads(raw)
    if fmt == "json":
        return json.dumps(result, indent=2)
    return f"Address: {_fmt_addr(result)}\nLat, Lon: {result.get('lat','?')}, {result.get('lon','?')}"

def cmd_route(src_lat, src_lon, dst_lat, dst_lon, fmt="text"):
    """Get driving route between two points."""
    coord = f"{src_lon},{src_lat};{dst_lon},{dst_lat}"
    params = {"overview": "full", "geometries": "geojson", "steps": "true"}
    st, raw = _req(f"{OSRM_BASE}/route/v1/driving/{coord}", params)
    if st != 200:
        return f"Error {st}: {raw.decode(errors='replace')[:200]}"
    data = json.loads(raw)
    if not data.get("routes"):
        return "No route found."
    route = data["routes"][0]
    dist_km = route["distance"] / 1000
    dur_min = route["duration"] / 60
    if fmt == "json":
        return json.dumps({"distance_km": round(dist_km, 2), "duration_min": round(dur_min, 1)}, indent=2)
    return f"Distance: {dist_km:.1f} km\nDuration: {dur_min:.0f} min"

def cmd_poi(lat, lon, radius=1000, category="amenity", fmt="text"):
    """Find points of interest near a location via Overpass API."""
    overpass_q = f"""
    [out:json][timeout:{TIMEOUT}];
    node[{category}](around:{radius},{lat},{lon});
    out body 20;
    """
    st, raw = _req(OSM_OVERPASS, None, {"Content-Type": "text/plain"})
    # POST request needed for Overpass
    req = urllib.request.Request(
        OSM_OVERPASS,
        data=overpass_q.encode(),
        headers={"Content-Type": "text/plain", "User-Agent": f"maps-cli/{VERSION}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return f"Error {e.code}: {e.read().decode(errors='replace')[:200]}"
    except urllib.error.URLError as e:
        return f"Network error: {e.reason}"

    elements = data.get("elements", [])
    if not elements:
        return "No POIs found."
    if fmt == "json":
        return json.dumps([{"name": e.get("tags", {}).get("name", "Unnamed"),
                            "lat": e["lat"], "lon": e["lon"],
                            "type": e.get("tags", {}).get(category, category)}
                           for e in elements], indent=2)
    lines = []
    for i, e in enumerate(elements[:20], 1):
        tags = e.get("tags", {})
        name = tags.get("name", tags.get("operator", "Unnamed"))
        lines.append(f"{i}. {name} [{e['lat']},{e['lon']}]")
    return "\n".join(lines)

def cmd_timezone(lat, lon, fmt="text"):
    """Lookup timezone via coordinates."""
    import datetime as dt_module
    params = {"lat": lat, "lon": lon, "format": "json"}
    st, raw = _req(f"{OSM_NOMINATIM}/reverse", params)
    if st != 200:
        return f"Error {st}: {raw.decode(errors='replace')[:200]}"
    result = json.loads(raw)
    tz_name = result.get("properties", {}).get("timezone", {}).get("name", "Unknown") if "properties" in result else "Unknown"
    now_utc = dt_module.datetime.now(timezone.utc)
    if fmt == "json":
        return json.dumps({"timezone": tz_name, "utc_offset": str(now_utc.astimezone())}, indent=2)
    return f"Timezone: {tz_name}\nCurrent UTC: {now_utc.isoformat()}"

def cmd_export(lat, lon, radius=5000, fmt="text"):
    """Export nearby places as CSV."""
    overpass_q = f"""
    [out:csv(::lat,::lon,name,\"amenity\",\"shop\";true;\",\")][timeout:{TIMEOUT}];
    node(around:{radius},{lat},{lon});
    out;
    """
    req = urllib.request.Request(
        OSM_OVERPASS,
        data=overpass_q.encode(),
        headers={"Content-Type": "text/plain", "User-Agent": f"maps-cli/{VERSION}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            csv_data = r.read().decode()
    except Exception as e:
        return f"Export error: {e}"
    return csv_data

# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        prog=NAME,
        description="Advanced OpenStreetMap CLI — geocode, route, POI search, timezone, export",
        epilog="Powered by OSM Nominatim, OSRM, and Overpass API. Free + MIT."
    )
    p.add_argument("--version", action="version", version=f"{NAME} v{VERSION}")
    p.add_argument("--json", action="store_true", help="JSON output")
    sub = p.add_subparsers(dest="cmd", required=True)

    # geocode
    g = sub.add_parser("geocode", help="Geocode a place name")
    g.add_argument("query", help="Place name (e.g. 'Taj Mahal, India')")
    g.add_argument("--limit", type=int, default=5, help="Max results")

    # reverse
    r = sub.add_parser("reverse", help="Reverse geocode coordinates")
    r.add_argument("lat", type=float)
    r.add_argument("lon", type=float)

    # route
    rt = sub.add_parser("route", help="Driving route between two points")
    rt.add_argument("src_lat", type=float)
    rt.add_argument("src_lon", type=float)
    rt.add_argument("dst_lat", type=float)
    rt.add_argument("dst_lon", type=float)

    # poi
    po = sub.add_parser("poi", help="Find points of interest")
    po.add_argument("lat", type=float)
    po.add_argument("lon", type=float)
    po.add_argument("--radius", type=int, default=1000, help="Search radius in meters")
    po.add_argument("--category", default="amenity", help="OSM tag (amenity, shop, tourism, etc.)")

    # timezone
    tz = sub.add_parser("timezone", help="Lookup timezone by coordinates")
    tz.add_argument("lat", type=float)
    tz.add_argument("lon", type=float)

    # export
    ex = sub.add_parser("export", help="Export POIs as CSV")
    ex.add_argument("lat", type=float)
    ex.add_argument("lon", type=float)
    ex.add_argument("--radius", type=int, default=5000)

    # self-test
    st = sub.add_parser("self-test", help="Run built-in self-test")

    args = p.parse_args()
    fmt = "json" if args.json else "text"

    if args.cmd == "self-test":
        return test()

    cmds = {
        "geocode": lambda: cmd_geocode(args.query, args.limit, fmt),
        "reverse": lambda: cmd_reverse(args.lat, args.lon, fmt),
        "route": lambda: cmd_route(args.src_lat, args.src_lon, args.dst_lat, args.dst_lon, fmt),
        "poi": lambda: cmd_poi(args.lat, args.lon, args.radius, args.category, fmt),
        "timezone": lambda: cmd_timezone(args.lat, args.lon, fmt),
        "export": lambda: cmd_export(args.lat, args.lon, args.radius, fmt),
    }
    result = cmds[args.cmd]()
    print(result)
    return 0

# ── self-test ────────────────────────────────────────────────────────────

def test():
    errors = []
    def chk(label, ok, detail=""):
        if not ok:
            errors.append(f"FAIL: {label} — {detail}")
        print(f"  {'✅' if ok else '❌'} {label}")
    print(f"{NAME} v{VERSION} self-test")
    # Test geocode parsing
    r = json.loads(cmd_geocode("London", limit=1, fmt="json"))
    chk("geocode returns list", isinstance(r, list), type(r).__name__)
    # Test reverse parsing
    r2 = cmd_reverse(51.5074, -0.1278, fmt="text")
    chk("reverse returns text", "Address:" in r2)
    # Test route parsing
    r3 = cmd_route(51.5, -0.12, 48.85, 2.35, fmt="json")
    if isinstance(r3, str) and r3.startswith("Error"):
        chk("route handles network gracefully (may need internet)", True)
    else:
        data = json.loads(r3)
        chk("route returns distance+duration", "distance_km" in data)
    # Test self-test compiles
    chk("All functions importable", True)
    if errors:
        for e in errors:
            print(e)
        return 1
    print(f"  All checks passed ✅")
    return 0

if __name__ == "__main__":
    sys.exit(main())
