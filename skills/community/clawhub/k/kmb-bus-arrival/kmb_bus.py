#!/usr/bin/env python3
"""
KMB Bus Arrival Skill v1.2.1 - Complete rewrite per spec
- Follows steps 1-6 exactly
- Fresh API calls always (no caching)
- No old commands (getRouteDirection, getRouteInfo, getBusStopID, getNextArrivals removed)
- Only command: getArrival <route> <stop_name>
- Plain text output matching spec format
"""

import json, sys, time, re, urllib.request, urllib.error
from datetime import datetime, timedelta

BASE = "https://data.etabus.gov.hk/v1/transport/kmb"

def fetch_json(url, retries=2, total_timeout=3):
    """Fetch JSON with retries using urllib. Total time budget ≤3s."""
    start = time.time()
    delay = 0.5  # initial backoff
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (OpenClaw kmb-bus-arrival)', 'Accept': 'application/json'}
    )
    for attempt in range(1, retries + 1):
        try:
            elapsed = time.time() - start
            remaining = total_timeout - elapsed
            if remaining <= 0:
                return {"error": "timeout"}
            timeout = min(2.0, remaining)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode('utf-8')
                if not raw.strip():
                    raise ValueError("Empty response")
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}"}
        except urllib.error.URLError:
            if attempt < retries:
                time.sleep(min(delay, remaining if remaining > 0 else delay))
                delay *= 1.5
                continue
            return {"error": "network error"}
        except Exception:
            if attempt < retries:
                elapsed = time.time() - start
                time.sleep(min(delay, total_timeout - elapsed if total_timeout - elapsed > 0 else delay))
                delay *= 1.5
                continue
            return {"error": "unknown error"}
    return {"error": "max retries"}

def get_hkt_now():
    """Return current Hong Kong time as string HH:MM HKT"""
    utc_now = datetime.utcnow()
    hkt = utc_now + timedelta(hours=8)
    return hkt.strftime("%H:%M HKT")

def get_arrival(route_input, stop_name):
    """
    Main function implementing steps 1-6 exactly per v1.2.1 spec.
    """
    # Step 1: Validate and normalize inputs
    route = route_input.upper()  # Convert to capital letters automatically
    
    # Validate route (alpha-numeric)
    if not re.match(r'^[A-Za-z0-9]+$', route):
        print(f"Error: Invalid route format: '{route_input}'")
        return
    
    # Validate stop name (string only)
    if not isinstance(stop_name, str) or not stop_name.strip():
        print("Error: Stop name must be a non-empty string.")
        return
    
    stop_name_lower = stop_name.lower().strip()
    
    # Step 2: Get all stop IDs for both directions
    def fetch_with_retry(url, max_retries=2):
        for attempt in range(max_retries + 1):
            data = fetch_json(url, retries=1, total_timeout=2)
            if "error" not in data and "data" in data and data["data"]:
                return data["data"]
            if attempt < max_retries:
                time.sleep(0.3)
        return None
    
    out_stops = fetch_with_retry(f"{BASE}/route-stop/{route}/outbound/1", max_retries=2)
    in_stops = fetch_with_retry(f"{BASE}/route-stop/{route}/inbound/1", max_retries=2)
    
    if out_stops is None and in_stops is None:
        print(f"Failed to get stop data for route {route}. Please try again later.")
        return
    
    # Find last stop IDs and names
    def get_last_stop_info(stops):
        if not stops:
            return None, "Unknown"
        last_stop_id = stops[-1]["stop"]  # 16-char stop ID
        # Fetch stop name with retry
        for _ in range(2):
            stop_data = fetch_json(f"{BASE}/stop/{last_stop_id}", retries=1, total_timeout=2)
            if "error" not in stop_data and "data" in stop_data and stop_data["data"]:
                name_info = stop_data["data"]
                name = name_info.get("name_en") or name_info.get("name_tc") or "Unknown"
                return last_stop_id, name
            time.sleep(0.2)
        return last_stop_id, "Unknown"
    
    outbound_last_id, outbound_last_name = get_last_stop_info(out_stops)
    inbound_last_id, inbound_last_name = get_last_stop_info(in_stops)
    
    # Step 3: Get all bus stops (fresh copy)
    all_stops_data = fetch_json(f"{BASE}/route-stop", retries=2, total_timeout=3)
    if "error" in all_stops_data or "data" not in all_stops_data:
        print("Failed to get bus stop data. Please try again later.")
        return
    
    all_stops = all_stops_data["data"]  # List of all route-stop entries
    
    # Step 4: Find 16-char bus stop ID(s) matching route AND stop name
    arg3 = []  # Dynamic array, max 2 elements
    
    for entry in all_stops:
        if entry.get("route", "").upper() == route:  # Exact match except case
            stop_id = entry.get("stop", "")
            if len(stop_id) == 16:  # 16-character bus stop ID
                # Need to get stop name to check against arg2
                # We'll batch this later, for now collect candidate IDs
                arg3.append(stop_id)
    
    # Now get stop names for candidate IDs (need to fetch from /stop/{stop_id})
    # But we can also filter by checking if stop_id is in out_stops or in_stops
    # and then fetch the name for those
    
    # Let's get unique stop IDs from route stops first
    route_stop_ids = set()
    if out_stops:
        for s in out_stops:
            route_stop_ids.add(s["stop"])
    if in_stops:
        for s in in_stops:
            route_stop_ids.add(s["stop"])
    
    # For each route stop ID, fetch its name and check against stop_name
    matching_stops = []
    for stop_id in route_stop_ids:
        for _ in range(2):
            stop_data = fetch_json(f"{BASE}/stop/{stop_id}", retries=1, total_timeout=2)
            if "error" not in stop_data and "data" in stop_data and stop_data["data"]:
                info = stop_data["data"]
                name_en = (info.get("name_en") or "").lower()
                name_tc = (info.get("name_tc") or "").lower()
                # Partial match for stop name
                if stop_name_lower in name_en or stop_name_lower in name_tc:
                    matching_stops.append(stop_id)
                break
            time.sleep(0.2)
        if len(matching_stops) >= 2:
            break
    
    if not matching_stops:
        print(f"Stop '{stop_name}' not found for route {route}. Please double check the bus route number AND bus stop name.")
        return
    
    arg3 = matching_stops[:2]  # Max 2 elements
    
    # Step 5: Ensure arg3 elements are within the requested route
    out_stop_ids = [s["stop"] for s in (out_stops or [])]
    in_stop_ids = [s["stop"] for s in (in_stops or [])]
    
    valid_arg3 = []
    for sid in arg3:
        if sid in out_stop_ids or sid in in_stop_ids:
            valid_arg3.append(sid)
    
    if not valid_arg3:
        print(f"Stop ID(s) for '{stop_name}' not found in route {route}. Please double check the bus route number AND bus stop name.")
        return
    
    arg3 = valid_arg3
    
    # Determine scenario (arg4)
    in_outbound = any(sid in out_stop_ids for sid in arg3)
    in_inbound = any(sid in in_stop_ids for sid in arg3)
    
    if len(arg3) == 1:
        if arg3[0] in out_stop_ids:
            arg4 = 0
        else:
            arg4 = 1
    else:  # len(arg3) == 2
        arg4 = 2
    
    # Step 6: Get ETA
    arg5 = get_hkt_now()
    
    def fetch_eta(stop_id, max_retries=2):
        url = f"{BASE}/eta/{stop_id}/{route}/1"
        for attempt in range(max_retries + 1):
            data = fetch_json(url, retries=1, total_timeout=2)
            if "error" not in data:
                items = data if isinstance(data, list) else data.get("data", [])
                if items:
                    etas = []
                    for it in items[:3]:  # Max 3 arrivals
                        eta_str = it.get("eta")
                        if eta_str:
                            try:
                                # Parse ISO format with timezone
                                if '+' in eta_str:
                                    time_part = eta_str.split('T')[1].split('+')[0][:5]
                                elif 'Z' in eta_str:
                                    dt = datetime.fromisoformat(eta_str.replace('Z', '+00:00'))
                                    dt_hkt = dt.replace(tzinfo=None) + timedelta(hours=8)
                                    time_part = dt_hkt.strftime('%H:%M')
                                else:
                                    time_part = eta_str.split('T')[1][:5] if 'T' in eta_str else eta_str[:5]
                                etas.append(time_part + ' HKT')
                            except Exception:
                                etas.append(eta_str)
                    if etas:
                        return etas
            if attempt < max_retries:
                time.sleep(0.3)
        return None
    
    # Fetch ETAs for all elements in arg3
    etas_result = []
    for sid in arg3:
        eta = fetch_eta(sid, max_retries=2)
        etas_result.append(eta)
    
    # Check if at least one succeeded
    if all(e is None for e in etas_result):
        print(f"Failed to get ETA for route {route}. Please try again later.")
        return
    
    # Step 6a: Show answer according to arg4
    # Get display stop name (use first matching stop)
    display_name = stop_name
    for _ in range(2):
        stop_data = fetch_json(f"{BASE}/stop/{arg3[0]}", retries=1, total_timeout=2)
        if "error" not in stop_data and "data" in stop_data and stop_data["data"]:
            info = stop_data["data"]
            display_name = info.get("name_en") or info.get("name_tc") or stop_name
            break
        time.sleep(0.2)
    
    if arg4 == 0:
        print(f"*{route} (to {outbound_last_name})*\n")
        print(f"Stop: *{display_name}*\n")
        print("Next arrivals:")
        if etas_result[0]:
            for t in etas_result[0]:
                print(f"- {t}")
        print(f"\n(Current Time: {arg5})")
    elif arg4 == 1:
        print(f"*{route} (to {inbound_last_name})*\n")
        print(f"Stop: *{display_name}*\n")
        print("Next arrivals:")
        if etas_result[0]:
            for t in etas_result[0]:
                print(f"- {t}")
        print(f"\n(Current Time: {arg5})")
    else:  # arg4 == 2
        print(f"*{route} (to {outbound_last_name} / {inbound_last_name})*\n")
        print(f"Stop: *{display_name}*\n")
        # Find which is outbound and which is inbound
        out_eta = None
        in_eta = None
        for i, sid in enumerate(arg3):
            if sid in out_stop_ids:
                out_eta = etas_result[i]
            else:
                in_eta = etas_result[i]
        
        if out_eta:
            print(f"Next arrivals (to {outbound_last_name}):")
            for t in out_eta:
                print(f"- {t}")
        if in_eta:
            print(f"Next arrivals (to {inbound_last_name}):")
            for t in in_eta:
                print(f"- {t}")
        print(f"\n(Current Time: {arg5})")

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 kmb_bus.py getArrival <route> <stop_name>")
        return
    
    cmd = sys.argv[1]
    if cmd != "getArrival":
        print(f"Unknown command: {cmd}")
        return
    
    route = sys.argv[2]
    stop_name = " ".join(sys.argv[3:])
    
    get_arrival(route, stop_name)

if __name__ == "__main__":
    main()
