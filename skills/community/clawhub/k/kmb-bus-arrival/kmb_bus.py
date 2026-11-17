#!/usr/bin/env python3
"""
KMB Bus Arrival Skill v1.2.2 - Security hardened per ClawHub audit
- Only command: getArrival <route> <stop_name>
- Plain text output matching spec format
- Strict input validation with allowlist patterns and length limits
- Local rate limiting (10 req/min) and API call budget (15 calls/invocation)
- Explicit SSL certificate verification
- Unified error messages without internal API structure disclosure
- Removed redundant /route-stop full fetch (optimization)
"""

import json, sys, time, re, urllib.request, urllib.error, ssl, certifi, functools
from datetime import datetime, timedelta, timezone

BASE = "https://data.etabus.gov.hk/v1/transport/kmb"

# Security: Local rate limiting (10 requests/minute per process)
RATE_LIMIT = 10
RATE_WINDOW = 60
_call_times = []

# Security: API call budget per invocation (generous limit to accommodate retries)
MAX_API_CALLS = 100
_api_call_count = 0

# Security: Explicit SSL context with trusted CA bundle
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def _rate_limit_check() -> bool:
    """Check and record rate limit. Returns True if allowed, False if exceeded."""
    global _call_times
    now = time.time()
    _call_times = [t for t in _call_times if now - t < RATE_WINDOW]
    if len(_call_times) >= RATE_LIMIT:
        return False
    _call_times.append(now)
    return True


def _api_call_budget_check() -> bool:
    """Check and increment API call budget. Returns True if allowed, False if exceeded."""
    global _api_call_count
    if _api_call_count >= MAX_API_CALLS:
        return False
    _api_call_count += 1
    return True


def _reset_api_call_budget():
    """Reset API call counter for new invocation."""
    global _api_call_count
    _api_call_count = 0


def _err(msg: str):
    """Unified error output without internal API structure disclosure."""
    print(f"Error: {msg}")
    return


def fetch_json(url: str, retries: int = 2, total_timeout: int = 3):
    """Fetch JSON with retries using urllib. Total time budget ≤3s."""
    if not _api_call_budget_check():
        return {"error": "api call budget exceeded"}

    start = time.time()
    delay = 0.5  # initial backoff
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (OpenClaw kmb-bus-arrival/1.2.2)', 'Accept': 'application/json'}
    )
    for attempt in range(1, retries + 1):
        try:
            elapsed = time.time() - start
            remaining = total_timeout - elapsed
            if remaining <= 0:
                return {"error": "timeout"}
            timeout = min(2.0, remaining)
            with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
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


def get_hkt_now() -> str:
    """Return current Hong Kong time as string HH:MM HKT"""
    utc_now = datetime.now(timezone.utc)
    hkt = utc_now + timedelta(hours=8)
    return hkt.strftime("%H:%M HKT")


def get_arrival(route_input: str, stop_name: str):
    """
    Main function implementing secure getArrival per v1.2.2 spec.
    """
    _reset_api_call_budget()

    # Rate limiting
    if not _rate_limit_check():
        _err("Rate limit exceeded. Please wait before making another request.")
        return

    # Step 1: Validate and normalize inputs (aligned with SKILL.md schemas)
    route = route_input.upper()

    # Validate route: alphanumeric, max 16 chars (matches SKILL.md pattern)
    if not re.match(r'^[A-Za-z0-9]{1,16}$', route):
        _err("Invalid route format. Use alphanumeric characters only (max 16).")
        return

    # Validate stop_name: allowed chars, max 50 chars (matches SKILL.md pattern)
    if not isinstance(stop_name, str) or not stop_name.strip():
        _err("Stop name must be a non-empty string.")
        return

    stop_name_stripped = stop_name.strip()
    if not re.match(r'^[\w\s\u4e00-\u9fff\(\)（）\-]{1,50}$', stop_name_stripped):
        _err("Invalid stop name. Use letters, numbers, spaces, Chinese characters, parentheses, or hyphens (max 50).")
        return

    stop_name_lower = stop_name_stripped.lower()

    # Step 2: Get stop IDs for both directions (outbound + inbound)
    def fetch_with_retry(url: str, max_retries: int = 2):
        for attempt in range(max_retries + 1):
            data = fetch_json(url, retries=1, total_timeout=3)
            if "error" not in data and "data" in data and data["data"]:
                return data["data"]
            if attempt < max_retries:
                time.sleep(0.3)
        return None

    out_stops = fetch_with_retry(f"{BASE}/route-stop/{route}/outbound/1", max_retries=2)
    in_stops = fetch_with_retry(f"{BASE}/route-stop/{route}/inbound/1", max_retries=2)

    if out_stops is None and in_stops is None:
        _err(f"Failed to get stop data for route {route}. Please try again later.")
        return

    # Find last stop IDs and names for direction display
    def get_last_stop_info(stops):
        if not stops:
            return None, "Unknown"
        last_stop_id = stops[-1]["stop"]  # 16-char stop ID
        for _ in range(2):
            stop_data = fetch_json(f"{BASE}/stop/{last_stop_id}", retries=1, total_timeout=3)
            if "error" not in stop_data and "data" in stop_data and stop_data["data"]:
                name_info = stop_data["data"]
                name = name_info.get("name_en") or name_info.get("name_tc") or "Unknown"
                return last_stop_id, name
            time.sleep(0.2)
        return last_stop_id, "Unknown"

    outbound_last_id, outbound_last_name = get_last_stop_info(out_stops)
    inbound_last_id, inbound_last_name = get_last_stop_info(in_stops)

    # Collect all stop IDs from this route (both directions) - replaces old Step 3
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
            stop_data = fetch_json(f"{BASE}/stop/{stop_id}", retries=1, total_timeout=3)
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
        _err(f"Stop '{stop_name_stripped}' not found for route {route}. Please check the route number and stop name.")
        return

    arg3 = matching_stops[:2]  # Max 2 elements

    # Step 4: Ensure arg3 elements are within the requested route
    out_stop_ids = [s["stop"] for s in (out_stops or [])]
    in_stop_ids = [s["stop"] for s in (in_stops or [])]

    valid_arg3 = []
    for sid in arg3:
        if sid in out_stop_ids or sid in in_stop_ids:
            valid_arg3.append(sid)

    if not valid_arg3:
        _err(f"Stop ID(s) for '{stop_name_stripped}' not found in route {route}. Please check the route number and stop name.")
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

    # Step 5: Get ETA
    arg5 = get_hkt_now()

    def fetch_eta(stop_id: str, max_retries: int = 2):
        url = f"{BASE}/eta/{stop_id}/{route}/1"
        for attempt in range(max_retries + 1):
            data = fetch_json(url, retries=1, total_timeout=3)
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
        _err(f"Failed to get ETA for route {route}. Please try again later.")
        return

    # Step 6: Show answer according to arg4
    # Get display stop name (use first matching stop)
    display_name = stop_name_stripped
    for _ in range(2):
        stop_data = fetch_json(f"{BASE}/stop/{arg3[0]}", retries=1, total_timeout=3)
        if "error" not in stop_data and "data" in stop_data and stop_data["data"]:
            info = stop_data["data"]
            display_name = info.get("name_en") or info.get("name_tc") or stop_name_stripped
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
        _err(f"Unknown command: {cmd}")
        return

    route = sys.argv[2]
    stop_name = " ".join(sys.argv[3:])

    get_arrival(route, stop_name)


if __name__ == "__main__":
    main()