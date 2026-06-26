#!/usr/bin/env python3
import sys, json, os, time, urllib.request, urllib.parse, difflib
from datetime import datetime

BASE = "https://data.etagmb.gov.hk"
ROUTEFARELIST_URL = "https://data.hkbus.app/routeFareList.min.json"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "data")
os.makedirs(CACHE_DIR, exist_ok=True)

def load_cache(name, default=None):
    path = os.path.join(CACHE_DIR, name)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except:
            return default
    return default

def save_cache(name, data):
    path = os.path.join(CACHE_DIR, name)
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Cache save error {name}: {e}", file=sys.stderr)

def fetch_json(url, cache_name=None, ttl=3600):
    """Fetch JSON from URL with optional file caching."""
    if cache_name:
        cached = load_cache(cache_name)
        if cached:
            if time.time() - cached.get('_timestamp', 0) < ttl:
                return cached.get('data')
    # Set a user-agent to avoid 403 from some hosts
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OpenClawSkill/1.0)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        if cache_name:
            save_cache(cache_name, {'_timestamp': time.time(), 'data': data})
        return data
    except Exception as e:
        raise Exception(f"Fetch failed {url}: {e}")

def get_routes_all():
    """Fetch all routes list: /route (no param) returns regions with route codes."""
    return fetch_json(BASE + "/route", cache_name="routes_all.json", ttl=3600)

def get_route_details(region, route):
    """Fetch route details for region/route. Cached per key for 5 minutes."""
    key = f"{region}_{route}"
    cache = load_cache("route_details.json", default={})
    if key in cache:
        entry = cache[key]
        if time.time() - entry.get('_ts', 0) < 300:  # 5 minutes
            return entry['data']
    url = f"{BASE}/route/{urllib.parse.quote(region)}/{urllib.parse.quote(route)}"
    data = fetch_json(url)
    cache[key] = {'_ts': time.time(), 'data': data}
    save_cache("route_details.json", cache)
    return data

def get_stop_names(stop_id):
    """Fetch stop names for a stop ID via /stop-route/{stop_id}. Returns dict with 'en' and 'zh'."""
    stop_cache = load_cache("stop_names.json", default={})
    if stop_id in stop_cache:
        return stop_cache[stop_id]
    url = f"{BASE}/stop-route/{urllib.parse.quote(stop_id)}"
    try:
        # Use longer TTL for stop names as they don't change often
        resp = fetch_json(url, ttl=86400*7)
        # The response is a dict with 'data' array
        data_list = resp.get('data', []) if isinstance(resp, dict) else []
        if data_list and len(data_list) > 0:
            # The stop name is same across all entries; take first
            entry = data_list[0]
            names = {
                'en': entry.get('name_en'),
                'zh': entry.get('name_tc') or entry.get('name_sc')
            }
            # Clean None
            if names['en'] is None: names['en'] = ''
            if names['zh'] is None: names['zh'] = ''
            stop_cache[stop_id] = names
            save_cache("stop_names.json", stop_cache)
            return names
    except Exception as e:
        print(f"Error fetching stop {stop_id}: {e}", file=sys.stderr)
    return {'en': '', 'zh': ''}

def get_eta(stop_id):
    """Fetch ETA for a stop. Return full JSON."""
    url = f"{BASE}/eta/stop/{urllib.parse.quote(stop_id)}"
    return fetch_json(url, ttl=30)  # short TTL

def search_routes(route):
    """Search for route number across all regions. Return matches or suggestions."""
    try:
        routes_all = get_routes_all()
    except Exception as e:
        return {"route": route, "found": False, "error": str(e)}
    regions_data = routes_all.get('data', {}).get('routes', {})
    matches = []
    for region, rlist in regions_data.items():
        if route in rlist:
            matches.append(region)
    if matches:
        return {"route": route, "found": True, "regions": matches}
    else:
        # Collect all route numbers for fuzzy suggestion
        all_routes = set()
        for rlist in regions_data.values():
            all_routes.update(rlist)
        suggestions = difflib.get_close_matches(route, sorted(all_routes), n=5, cutoff=0.6)
        return {"route": route, "found": False, "suggestions": suggestions}

def get_gmb_arrival(route, direction, stop_name, region):
    """Main function: given route, direction (1/2), stop name, region, return arrivals."""
    # Validate direction
    if direction not in ("1", "2"):
        return {"error": "Direction must be 1 or 2"}
    # Get route details
    try:
        details = get_route_details(region, route)
    except Exception as e:
        return {"error": f"Failed to fetch route details: {e}"}
    # Flatten all direction entries; handle two possible structures:
    # 1) data array contains entries with "directions" array inside
    # 2) data array directly contains direction objects (each with route_seq, orig_en, dest_en)
    all_directions = []
    route_id = None
    for entry in details.get('data', []):
        if route_id is None and 'route_id' in entry:
            route_id = entry.get('route_id')
        if 'directions' in entry:
            for d in entry['directions']:
                all_directions.append(d)
        elif 'route_seq' in entry:
            all_directions.append(entry)
    # Find the matching direction
    dir_data = None
    for d in all_directions:
        if str(d.get('route_seq')) == direction:
            dir_data = d
            break
    if not dir_data or route_id is None:
        return {"error": f"Direction {direction} not found for route {route} in region {region}"}
    orig_en = dir_data.get('orig_en', '')
    dest_en = dir_data.get('dest_en', '')
    # Load routeFareList
    try:
        rfl = fetch_json(ROUTEFARELIST_URL, cache_name="routeFareList.json", ttl=86400)
    except Exception as e:
        return {"error": f"Failed to load route fare list: {e}"}
    route_list = rfl.get('routeList', {})
    # Build composite key: route + 1 + orig_en + dest_en
    composite_key = f"{route}+1+{orig_en}+{dest_en}"
    route_entry = route_list.get(composite_key)
    if not route_entry:
        # Try to find any entry with matching route and direction (maybe serviceType differs)
        alt_key = f"{route}+1+{dest_en}+{orig_en}"
        route_entry = route_list.get(alt_key)
        if route_entry:
            # The directions might be swapped? But we already used direction; shouldn't swap.
            pass
        else:
            # As a fallback, try searching for any key that contains route and both names (in any order)
            for key, entry in route_list.items():
                if entry.get('co') and 'gmb' in entry.get('co') and entry.get('route') == route:
                    # Check if origin/destination match (allow swapped)
                    orig_match = (entry.get('orig', {}).get('en') == orig_en and entry.get('dest', {}).get('en') == dest_en) or (entry.get('orig', {}).get('en') == dest_en and entry.get('dest', {}).get('en') == orig_en)
                    if orig_match:
                        route_entry = entry
                        break
    if not route_entry:
        return {"error": f"Route entry not found in static data. Composite key: {composite_key}"}
    # Ensure GMB
    if 'gmb' not in route_entry.get('co', []):
        return {"error": "Route is not a GMB route in static data."}
    stop_ids = route_entry.get('stops', {}).get('gmb', [])
    if not stop_ids:
        return {"error": "No stop IDs for this route in static data."}
    # Match stop name
    target = stop_name.strip().lower()
    matched_sid = None
    matched_names = []
    # First try exact match by pre-fetching names as we iterate (we'll cache)
    for sid in stop_ids:
        names = get_stop_names(sid)
        en = names.get('en', '').lower()
        zh = names.get('zh', '').lower()
        # Compare with target
        if target == en or target == zh:
            matched_sid = sid
            matched_names = [names.get('en'), names.get('zh')]
            break
    if not matched_sid:
        # Fuzzy match: need all names
        all_candidates = []  # (name_en, name_zh, sid)
        for sid in stop_ids:
            names = get_stop_names(sid)
            en = names.get('en', '')
            zh = names.get('zh', '')
            if en:
                all_candidates.append((en, zh, sid))
            elif zh:
                all_candidates.append(('', zh, sid))
        # Use difflib on English names primarily; if not, Chinese.
        name_list = [c[0] if c[0] else c[1] for c in all_candidates]
        suggestions = difflib.get_close_matches(stop_name, name_list, n=5, cutoff=0.6)
        if suggestions:
            # Map suggestion to stop IDs
            sug_map = {}
            for sug in suggestions:
                for en, zh, sid in all_candidates:
                    if (en and en == sug) or (zh and zh == sug):
                        sug_map[sug] = sid
                        break
            return {"error": f"Stop '{stop_name}' not found (exact).", "suggestions": sug_map}
        else:
            return {"error": f"Stop '{stop_name}' not found on this route."}
    # Get ETA
    try:
        eta_data = get_eta(matched_sid)
    except Exception as e:
        return {"error": f"Failed to fetch ETA: {e}"}
    # Filter for our route_id and direction
    entries = []
    for item in eta_data.get('data', []):
        if item.get('route_id') == route_id and str(item.get('route_seq')) == direction:
            entries.append(item)
    if not entries:
        # It's possible the route doesn't have active ETA right now
        return {"stopId": matched_sid, "stopName": matched_names[0] if matched_names else "", "arrivals": [], "message": "No active ETA for this route at the moment."}
    entry = entries[0]
    eta_items = entry.get('eta', [])
    arrivals = []
    for eta_item in eta_items[:3]:
        ts = eta_item.get('timestamp')
        if ts:
            try:
                # Parse ISO with timezone, e.g., 2026-03-25T15:00:00.000+08:00
                # Python's fromisoformat can handle with fromisoformat(ts.replace('Z', '+00:00')) but better use datetime.strptime with %z if needed.
                # Simplest: keep only time part
                dt = datetime.fromisoformat(ts)
                time_str = dt.strftime("%H:%M")
                arrivals.append(f"{time_str} HKT")
            except Exception as e:
                # fallback: use diff minutes? could show "in X min"
                diff = eta_item.get('diff')
                if diff is not None:
                    arrivals.append(f"In {diff} min")
                else:
                    arrivals.append("Unknown")
    return {"stopId": matched_sid, "stopName": matched_names[0] if matched_names else "", "arrivals": arrivals}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No subcommand provided"}))
        sys.exit(1)
    subcmd = sys.argv[1]
    if subcmd == "searchRoutes":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing route argument"}))
            sys.exit(1)
        route = sys.argv[2]
        result = search_routes(route)
        print(json.dumps(result, ensure_ascii=False))
    elif subcmd == "getGMBArrival":
        if len(sys.argv) < 6:
            print(json.dumps({"error": "Missing arguments. Usage: getGMBArrival <route> <direction> <stop_name> <region>"}))
            sys.exit(1)
        route = sys.argv[2]
        direction = sys.argv[3]
        stop_name = sys.argv[4]
        region = sys.argv[5]
        result = get_gmb_arrival(route, direction, stop_name, region)
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"Unknown subcommand: {subcmd}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
