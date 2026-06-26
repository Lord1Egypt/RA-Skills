#!/usr/bin/env python3
"""
Amap Direction Provider - Real-time accessibility calculation
Uses urllib (no external dependencies)
"""
import json
import math
import os
import ssl
import urllib.parse
import urllib.request
from typing import Dict, Optional, Tuple

# Try to load from .env.local if AMAP_KEY not in environment
def _load_env_file():
    """Simple .env.local loader without external dependencies"""
    try:
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env.local')
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('AMAP_KEY='):
                    key = line.split('=', 1)[1].strip().strip('"\'')
                    os.environ['AMAP_KEY'] = key
                    break
    except Exception:
        pass  # Silently ignore if file not found or unreadable

_load_env_file()

AMAP_KEY = os.getenv("AMAP_KEY", "")
if not AMAP_KEY:
    raise ValueError("AMAP_KEY not set. Please configure it in .env.local or set environment variable")

# Module availability flag
AMAP_AVAILABLE = True
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
AMAP_DIRECTION_URL = "https://restapi.amap.com/v3/direction/transit/integrated"
AMAP_WALKING_URL = "https://restapi.amap.com/v3/direction/walking"


def _to_int(value, default: int = 0) -> int:
    """Best-effort numeric casting for Amap string fields"""
    try:
        if value in (None, ""):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _format_distance(distance_m) -> str:
    distance_m = _to_int(distance_m, 0)
    if distance_m >= 1000:
        return f"{distance_m / 1000:.1f}km"
    return f"{distance_m}m"


def _normalize_dict(value):
    """Amap sometimes returns an object, sometimes a single-item list"""
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return item
    return {}


def _normalize_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    return []


def format_transit_detail_lines(details: Optional[Dict], max_parts: int = 0) -> list[str]:
    """Render concise, user-facing transit detail lines.

    max_parts <= 0 means no truncation (render the full route).
    """
    if not details:
        return []

    total_duration = _to_int(details.get("total_duration_min"), 0)
    walking_distance = _to_int(details.get("walking_distance"), 0)
    total_distance = _to_int(details.get("total_distance"), 0)
    segments_count = _to_int(details.get("segments_count"), 0)

    summary_bits = []
    if total_duration > 0:
        summary_bits.append(f"总时长 {total_duration}分钟")
    if walking_distance > 0:
        summary_bits.append(f"总步行 {_format_distance(walking_distance)}")
    if total_distance > 0:
        summary_bits.append(f"全程 {_format_distance(total_distance)}")
    if segments_count > 0:
        summary_bits.append(f"{segments_count} 段换乘/步行")

    lines = ["；".join(summary_bits)] if summary_bits else []

    shown = 0
    for step in details.get("steps", []):
        for part in step.get("parts", []):
            if max_parts > 0 and shown >= max_parts:
                lines.append("其余路段已省略")
                return lines

            if part.get("type") == "walking":
                distance = _format_distance(part.get("distance"))
                duration = _to_int(part.get("duration"), 0)
                instructions = part.get("instructions") or []
                if not instructions:
                    single = (part.get("instruction") or "步行").strip()
                    instructions = [single] if single else []
                head = f"步行 {distance}（约{duration}分钟）" if duration > 0 else f"步行 {distance}"
                if instructions:
                    lines.append(f"{head}：")
                    for instr in instructions:
                        lines.append(f"    · {instr}")
                else:
                    lines.append(head)
                shown += 1
                continue

            if part.get("type") == "bus":
                line_name = (part.get("line_name") or "未知线路").strip()
                departure = (part.get("departure_stop") or "未知站").strip()
                arrival = (part.get("arrival_stop") or "未知站").strip()
                via_count = _to_int(part.get("via_stops_count", part.get("via_stops")), 0)
                via_names = part.get("via_stop_names") or []
                duration = _to_int(part.get("duration"), 0)
                distance = _to_int(part.get("distance"), 0)
                is_subway = bool(part.get("is_subway"))
                verb = "乘坐地铁" if is_subway else "乘坐"

                # 1站 = 起终两站之间直达；via_count 为中间经停站数
                total_stops = via_count + 1 if via_count >= 0 else 0
                extras = []
                if total_stops > 0:
                    extras.append(f"共{total_stops}站")
                if duration > 0:
                    extras.append(f"约{duration}分钟")
                if distance > 0:
                    extras.append(_format_distance(distance))
                suffix = f"（{'，'.join(extras)}）" if extras else ""

                lines.append(f"{verb} {line_name}：{departure}（上） → {arrival}（下）{suffix}")

                if via_names:
                    lines.append(f"    途经：{'、'.join(via_names)}")

                alternatives = part.get("alternatives") or []
                if alternatives:
                    lines.append(f"    备选同段线路：{'、'.join(alternatives)}")

                shown += 1

    return lines


def _http_get_json(url: str, params: Dict, timeout: int = 15) -> Optional[Dict]:
    """HTTP GET helper with error handling using urllib"""
    try:
        query = urllib.parse.urlencode(params)
        full_url = f"{url}?{query}"
        req = urllib.request.Request(full_url, method="GET")
        req.add_header("Accept", "application/json")
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        return {"error": str(e)}


def geocode_amap(address: str, city: str = "") -> Optional[Tuple[float, float]]:
    """
    Geocode address using Amap API
    Returns: (longitude, latitude) tuple
    """
    params = {
        "key": AMAP_KEY,
        "address": address,
        "city": city,
        "output": "json",
    }
    data = _http_get_json(AMAP_GEOCODE_URL, params)
    
    if not data or data.get("status") != "1":
        return None
    
    geocodes = data.get("geocodes", [])
    if not geocodes:
        return None
    
    location = geocodes[0].get("location", "")
    if "," in location:
        lng, lat = location.split(",")
        return (float(lng), float(lat))
    return None


def get_transit_details(origin_lng: float, origin_lat: float,
                        dest_lng: float, dest_lat: float,
                        city: str = "", cityd: str = "") -> Optional[Dict]:
    """
    Get detailed transit route with step-by-step instructions
    Returns full route details including bus lines, stops, walking segments
    """
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    
    params = {
        "key": AMAP_KEY,
        "origin": origin,
        "destination": destination,
        "strategy": 0,
        "output": "json",
    }
    
    if city:
        params["city"] = city
        params["cityd"] = cityd or city
    
    data = _http_get_json(AMAP_DIRECTION_URL, params)
    
    if not data or data.get("status") != "1":
        return None
    
    route = data.get("route", {})
    transits = route.get("transits", [])
    
    if not transits:
        return None
    
    best = transits[0]
    duration_sec = _to_int(best.get("duration"), 0)
    
    # Parse detailed segments
    detailed_steps = []
    for seg_idx, seg in enumerate(best.get("segments", []), 1):
        step_info = {"segment": seg_idx, "parts": []}
        
        # Walking part — keep the full turn-by-turn instruction list
        walking = _normalize_dict(seg.get("walking", {}))
        walk_dist = _to_int(walking.get("distance"), 0)
        if walking and walk_dist > 0:
            walk_dest = walking.get("destination", "")
            walk_steps = _normalize_list(walking.get("steps", []))
            instructions = []
            for ws in walk_steps:
                ws = _normalize_dict(ws)
                instr = (ws.get("instruction") or "").strip()
                if instr:
                    instructions.append(instr)
            first_instruction = instructions[0] if instructions else "步行"

            step_info["parts"].append({
                "type": "walking",
                "distance": walk_dist,
                "duration": _to_int(walking.get("duration"), 0) // 60,
                "instruction": first_instruction,
                "instructions": instructions,
                "destination": walk_dest
            })
        
        # Bus/Subway part — multiple buslines in one segment are ALTERNATIVES
        # for the same leg (same dep/arr), not sequential transfers.
        bus = _normalize_dict(seg.get("bus", {}))
        if bus:
            buslines = _normalize_list(bus.get("buslines", []))
            norm_lines = []
            for bl in buslines:
                bl = _normalize_dict(bl)
                departure = _normalize_dict(bl.get("departure_stop", {}))
                arrival = _normalize_dict(bl.get("arrival_stop", {}))
                via_raw = _normalize_list(bl.get("via_stops", []))
                via_names = []
                for v in via_raw:
                    v = _normalize_dict(v)
                    nm = (v.get("name") or "").strip()
                    if nm:
                        via_names.append(nm)
                line_type = (bl.get("type") or "").strip()
                line_name = (bl.get("name", "未知线路") or "未知线路").split("(")[0]
                norm_lines.append({
                    "line_name": line_name,
                    "line_type": line_type,
                    "is_subway": ("地铁" in line_type) or ("地铁" in line_name),
                    "departure_stop": departure.get("name", "未知站"),
                    "departure_location": departure.get("location", ""),
                    "arrival_stop": arrival.get("name", "未知站"),
                    "arrival_location": arrival.get("location", ""),
                    "via_stops_count": _to_int(bl.get("via_num"), 0),
                    "via_stop_names": via_names,
                    "duration": _to_int(bl.get("duration"), 0) // 60,
                    "distance": _to_int(bl.get("distance"), 0),
                })

            if norm_lines:
                primary = dict(norm_lines[0])
                primary["type"] = "bus"
                # backward-compat: keep via_stops as the integer count
                primary["via_stops"] = primary.get("via_stops_count", 0)
                primary["alternatives"] = [l["line_name"] for l in norm_lines[1:]]
                primary["alternative_lines"] = norm_lines[1:]
                step_info["parts"].append(primary)
        
        if step_info["parts"]:
            detailed_steps.append(step_info)
    
    return {
        "total_duration_min": duration_sec // 60,
        "total_distance": _to_int(best.get("distance"), 0),
        "walking_distance": _to_int(best.get("walking_distance"), 0),
        "cost": best.get("cost", 0),
        "segments_count": len(detailed_steps),
        "steps": detailed_steps,
        "origin": origin,
        "destination": destination
    }


def get_transit_time(origin_lng: float, origin_lat: float, 
                     dest_lng: float, dest_lat: float,
                     city: str = "", cityd: str = "") -> Optional[Dict]:
    """
    Get transit (bus/subway + walk) time using Amap
    Returns accessibility info dict or None
    
    Args:
        city: Origin city code/name (e.g., "天津", "022")
        cityd: Destination city code/name (default: same as city)
    """
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    
    params = {
        "key": AMAP_KEY,
        "origin": origin,
        "destination": destination,
        "strategy": 0,  # fastest
        "output": "json",
    }
    
    # Only add city params if provided (Amap can auto-detect from coordinates)
    if city:
        params["city"] = city
        params["cityd"] = cityd or city
    
    data = _http_get_json(AMAP_DIRECTION_URL, params)
    
    if not data or data.get("status") != "1":
        return None
    
    route = data.get("route", {})
    transits = route.get("transits", [])
    
    if not transits:
        return None
    
    # Get best transit option
    best = transits[0]
    duration_sec = int(best.get("duration", 0))
    duration_min = duration_sec / 60
    segments = len(best.get("segments", []))
    
    # Calculate accessibility score (100 for 0 min, linear decrease)
    score = max(0, min(100, round(100 - duration_min * 2, 1)))
    
    # Format display string
    if duration_min < 60:
        display = f"🚇+🚶 {duration_min:.0f}分钟"
    else:
        display = f"🚇+🚶 {duration_min/60:.1f}小时"
    
    return {
        "duration_min": round(duration_min, 1),
        "mode": "transit",
        "score": score,
        "display": display,
        "segments": segments
    }


def get_walking_time(origin_lng: float, origin_lat: float,
                     dest_lng: float, dest_lat: float) -> Optional[Dict]:
    """
    Get pure walking time using Amap (fallback when transit unavailable)
    """
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    
    params = {
        "key": AMAP_KEY,
        "origin": origin,
        "destination": destination,
        "output": "json",
    }
    
    data = _http_get_json(AMAP_WALKING_URL, params)
    
    if not data or data.get("status") != "1":
        return None
    
    route = data.get("route", {})
    paths = route.get("paths", [])
    
    if not paths:
        return None
    
    duration_sec = int(paths[0].get("duration", 0))
    duration_min = duration_sec / 60
    
    # Walking score penalized more heavily
    score = max(0, min(100, round(100 - duration_min * 3, 1)))
    
    display = f"🚶 {duration_min:.0f}分钟" if duration_min < 60 else f"🚶 {duration_min/60:.1f}小时"
    
    return {
        "duration_min": round(duration_min, 1),
        "mode": "walking",
        "score": score,
        "display": display
    }


def estimate_walking_time(origin_lng: float, origin_lat: float,
                           dest_lng: float, dest_lat: float) -> Dict:
    """
    Fallback: Estimate walking time using haversine + average walking speed
    Used when Amap API fails or for quick estimation
    """
    # Haversine distance
    r = 6371000  # Earth radius in meters
    p1, p2 = math.radians(origin_lat), math.radians(dest_lat)
    dp = math.radians(dest_lat - origin_lat)
    dl = math.radians(dest_lng - origin_lng)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    distance_m = 2 * r * math.asin(math.sqrt(a))
    
    # Average walking speed: 5km/h = 83m/min
    duration_min = distance_m / 83
    score = max(0, min(100, round(100 - duration_min * 3, 1)))
    display = f"🚶 ~{duration_min:.0f}分钟(估算)"
    
    return {
        "duration_min": round(duration_min, 1),
        "mode": "estimate",
        "score": score,
        "display": display
    }


def get_accessibility(origin_lng: float, origin_lat: float,
                      dest_lng: float, dest_lat: float) -> Dict:
    """
    Get best accessibility info for a destination
    Priority: transit > walking API > estimation
    """
    # Try transit first
    result = get_transit_time(origin_lng, origin_lat, dest_lng, dest_lat)
    if result:
        return result
    
    # Fallback to walking API
    result = get_walking_time(origin_lng, origin_lat, dest_lng, dest_lat)
    if result:
        return result
    
    # Final fallback: estimation
    return estimate_walking_time(origin_lng, origin_lat, dest_lng, dest_lat)


def enrich_pois_with_accessibility(pois: list, origin_lng: float, origin_lat: float) -> list:
    """
    Add accessibility data to list of POIs
    """
    for poi in pois:
        dest_lng = poi.get("lon")
        dest_lat = poi.get("lat")
        
        if dest_lng is None or dest_lat is None:
            poi["accessibility"] = {
                "duration_min": 999,
                "mode": "error",
                "score": 0,
                "display": "❌ 无位置数据",
                "error": "Missing coordinates"
            }
            continue
        
        acc = get_accessibility(origin_lng, origin_lat, dest_lng, dest_lat)
        poi["accessibility"] = acc
        
        # Recalculate total score with accessibility weight
        # Original score (0-100) * 0.7 + Accessibility score * 0.3
        original_score = poi.get("score", 50)
        poi["total_score"] = round(original_score * 0.7 + acc.get("score", 0) * 0.3, 1)
    
    # Re-sort by total_score (descending), then by duration
    pois.sort(key=lambda x: (-x.get("total_score", 0), x.get("accessibility", {}).get("duration_min", 999)))
    return pois


if __name__ == "__main__":
    # Generic test - requires AMAP_KEY environment variable
    print("Testing Amap Direction Provider...")
    print("Note: Set AMAP_KEY env var before running")
    
    # Example: Test with coordinates (no geocode needed)
    # Origin: Tianjin University of Finance and Economics
    origin_lng, origin_lat = 117.2769, 39.0639
    # Destination: Sample nearby point
    test_dest_lng, test_dest_lat = 117.2800, 39.0600
    
    # Test with explicit city parameter
    result = get_transit_time(origin_lng, origin_lat, test_dest_lng, test_dest_lat, city="天津")
    print(f"Transit with city param: {result}")
    
    # Test auto-detection (no city param)
    result = get_accessibility(origin_lng, origin_lat, test_dest_lng, test_dest_lat)
    print(f"Accessibility (auto-detect): {result}")
