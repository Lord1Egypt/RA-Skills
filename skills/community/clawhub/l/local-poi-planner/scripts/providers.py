#!/usr/bin/env python3
import json
import math
import os
import re
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

# Load .env.local if exists
SCRIPT_DIR = Path(__file__).parent.resolve()
ENV_FILE = SCRIPT_DIR.parent / ".env.local"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

# Import Amap modules
try:
    import amap_direction
    AMAP_AVAILABLE = True
except ImportError:
    AMAP_AVAILABLE = False

try:
    import amap_poi
    AMAP_POI_AVAILABLE = True
except ImportError:
    AMAP_POI_AVAILABLE = False

SKILL_DIR = Path(__file__).resolve().parents[1]
ANCHORS_FILE = SKILL_DIR / "config" / "anchors.json"
GEOCODE_OVERRIDES_FILE = SKILL_DIR / "config" / "geocode_overrides.json"

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
AMAP_TEXT_SEARCH_URL = "https://restapi.amap.com/v3/place/text"
AMAP_INPUTTIPS_URL = "https://restapi.amap.com/v3/assistant/inputtips"
UA = "local-poi-planner/0.2 (+OpenClaw skill)"

BIG_AOI_RE = re.compile(r"(大学|学院|学校|校区|医院|商场|广场|景区|公园|园区|火车站|机场)")
TRANSIT_NAME_RE = re.compile(r"(地铁站|公交站|轻轨站|火车站入口|公交枢纽)")
SCHOOL_RE = re.compile(r"(大学|学院|学校|校区)")

CATEGORY_ALIASES = {
    "dessert": "dessert",
    "cafe": "cafe",
    "tea": "tea",
    "bakery": "bakery",
    "restaurant": "restaurant",
    "dinner": "restaurant",
}

AMAP_CATEGORY_KEYWORDS = {
    "dessert": "甜品",
    "cafe": "咖啡",
    "tea": "奶茶",
    "bakery": "面包",
    "restaurant": "餐厅",
    "网吧": "网吧",
    "KTV": "KTV",
    "电影院": "电影院",
    "酒店": "酒店",
    "医院": "医院",
    "药店": "药店",
    "快递": "快递",
    "健身房": "健身房",
    "超市": "超市",
    "银行": "银行",
    "充电站": "充电桩",
    "桌游": "桌游",
    "台球": "台球",
    "理发": "理发",
    "宠物": "宠物",
    "按摩": "按摩",
}

# Maoyan cinema API
MAOYAN_CITY_MAP = {
    "天津": 40, "北京": 1, "上海": 10, "广州": 20, "深圳": 17,
    "成都": 7, "重庆": 3, "杭州": 18, "武汉": 13, "南京": 9,
    "西安": 8, "长沙": 14, "苏州": 22, "郑州": 15, "厦门": 13,
    "福州": 26, "青岛": 24, "大连": 28, "沈阳": 27, "昆明": 30,
}
MAOYAN_CINEMA_LIST_URL = "https://m.maoyan.com/ajax/cinemaList"
MAOYAN_CINEMA_DETAIL_URL = "https://m.maoyan.com/ajax/cinemaDetail"

SPECIAL_HALL_KEYWORDS = {
    "4DX": ["4DX", "4D", "4D影厅", "4DX厅"],
    "D-BOX": ["D-BOX", "DBOX"],
    "IMAX": ["IMAX"],
    "杜比": ["杜比", "Dolby", "杜比全景声"],
    "ScreenX": ["ScreenX", "SCREENX"],
    "CINITY": ["CINITY"],
    "中国巨幕": ["CGS", "中国巨幕"],
    "RealD": ["RealD", "REALD"],
    "LUXE": ["LUXE"],
    "VIP": ["VIP厅", "贵宾厅"],
    "4K厅": ["4K厅", "4K激光厅"],
    "激光厅": ["激光厅"],
    "PRIME": ["PRIME厅", "PRIME"],
}


def _normalize_place_key(text: str):
    return re.sub(r"[\s,，()（）\-_/]+", "", (text or "").strip().lower())


def _is_china_like_result(item: dict):
    if not item:
        return False
    address = item.get("address") or {}
    country_code = (address.get("country_code") or "").lower()
    if country_code == "cn":
        return True
    haystack = " ".join([
        item.get("display_name") or "",
        address.get("country") or "",
        address.get("state") or "",
        address.get("province") or "",
        address.get("city") or "",
        address.get("county") or "",
        address.get("municipality") or "",
    ]).lower()
    return any(token in haystack for token in ["中国", "china", "福建", "福州", "闽侯"])


def _score_nominatim_candidate(query_name: str, item: dict):
    score = 0
    display_name = item.get("display_name") or ""
    normalized_query = _normalize_place_key(query_name)
    normalized_display = _normalize_place_key(display_name)
    if normalized_display == normalized_query:
        score += 120
    elif normalized_query and normalized_query in normalized_display:
        score += 70

    address = item.get("address") or {}
    name_parts = [
        address.get("amenity") or "",
        address.get("building") or "",
        address.get("tourism") or "",
        address.get("road") or "",
        address.get("suburb") or "",
        address.get("city_district") or "",
        address.get("town") or "",
        address.get("village") or "",
        address.get("city") or "",
        address.get("county") or "",
        address.get("state") or "",
    ]
    normalized_parts = _normalize_place_key("".join(name_parts))
    if normalized_query and normalized_query in normalized_parts:
        score += 50

    if _is_china_like_result(item):
        score += 25
    return score


def _score_override_candidate(query_name: str, override_key: str):
    normalized_query = _normalize_place_key(query_name)
    normalized_key = _normalize_place_key(override_key)
    if not normalized_query or not normalized_key:
        return 0
    if normalized_key == normalized_query:
        return 200
    if normalized_key in normalized_query:
        return 120 + len(normalized_key)
    if normalized_query in normalized_key:
        return 80 + len(normalized_query)
    return 0


def _http_get_json(url, params=None, timeout=20, method="GET", data=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=method)
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "application/json")
    payload = None
    if data is not None:
        payload = data.encode("utf-8")
        req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, payload, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def load_anchors():
    if ANCHORS_FILE.exists():
        return json.loads(ANCHORS_FILE.read_text())
    return {}


def load_geocode_overrides():
    if GEOCODE_OVERRIDES_FILE.exists():
        return json.loads(GEOCODE_OVERRIDES_FILE.read_text())
    return {}


def normalize_category(category: str):
    raw = (category or "").strip().lower()
    return CATEGORY_ALIASES.get(raw, raw or "restaurant")


def _amap_key():
    return os.getenv("AMAP_KEY", "")


def _is_transit_candidate(name: str, type_text: str = "", level: str = ""):
    combined = " ".join([name or "", type_text or "", level or ""])
    return bool(TRANSIT_NAME_RE.search(combined) or "公交地铁站点" in combined or "交通设施服务" in combined)


def _origin_candidate_score(origin_name: str, candidate: dict):
    name = candidate.get("name") or ""
    type_text = candidate.get("type") or candidate.get("typecode") or ""
    score = 0

    if name == origin_name:
        score += 120
    elif origin_name in name:
        score += 60
    elif name in origin_name:
        score += 30

    if BIG_AOI_RE.search(origin_name) and BIG_AOI_RE.search(name):
        score += 30
    if SCHOOL_RE.search(origin_name):
        if "高等院校" in type_text or "学校" in type_text or str(type_text).startswith("1412"):
            score += 40
        if _is_transit_candidate(name, type_text, candidate.get("level", "")):
            score -= 140

    if candidate.get("location"):
        score += 10
    return score


def _normalize_text_poi(poi: dict):
    return {
        "id": poi.get("id"),
        "name": poi.get("name"),
        "lat": float((poi.get("location") or ",").split(",")[1]),
        "lon": float((poi.get("location") or ",").split(",")[0]),
        "display_name": poi.get("address") or poi.get("name"),
        "type": poi.get("type", ""),
        "typecode": poi.get("typecode", ""),
        "address": poi.get("address", ""),
        "provider": "amap_text",
        "entr_location": poi.get("entr_location"),
        "navi_poiid": poi.get("navi_poiid"),
    }


def _normalize_tip_poi(tip: dict):
    location = tip.get("location") or ""
    if "," not in location:
        return None
    lon, lat = location.split(",", 1)
    return {
        "id": tip.get("id"),
        "name": tip.get("name"),
        "lat": float(lat),
        "lon": float(lon),
        "display_name": (tip.get("district") or "") + ((" " + tip.get("address")) if tip.get("address") else ""),
        "type": "",
        "typecode": tip.get("typecode", ""),
        "address": tip.get("address", ""),
        "provider": "amap_inputtips",
    }


def _resolve_origin_via_amap_search(name):
    key = _amap_key()
    if not key:
        return None

    candidates = []

    try:
        tip_params = {
            "key": key,
            "keywords": name,
            "datatype": "poi",
            "citylimit": "false",
            "output": "json",
        }
        tip_data = _http_get_json(AMAP_INPUTTIPS_URL, params=tip_params, timeout=12)
        for tip in tip_data.get("tips", [])[:10]:
            normalized = _normalize_tip_poi(tip)
            if normalized:
                candidates.append(normalized)
    except Exception:
        pass

    try:
        text_params = {
            "key": key,
            "keywords": name,
            "offset": 10,
            "page": 1,
            "extensions": "all",
            "output": "json",
        }
        text_data = _http_get_json(AMAP_TEXT_SEARCH_URL, params=text_params, timeout=12)
        for poi in text_data.get("pois", [])[:10]:
            location = poi.get("location") or ""
            if "," not in location:
                continue
            candidates.append(_normalize_text_poi(poi))
    except Exception:
        pass

    if not candidates:
        return None

    deduped = []
    seen = set()
    for c in candidates:
        key = (c.get("name"), round(c.get("lat", 0.0), 6), round(c.get("lon", 0.0), 6))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(c)

    ranked = sorted(deduped, key=lambda c: _origin_candidate_score(name, c), reverse=True)
    best = ranked[0]
    if _origin_candidate_score(name, best) < 40:
        return None
    return {
        "name": name,
        "lat": best["lat"],
        "lon": best["lon"],
        "display_name": best.get("display_name") or best.get("name") or name,
        "provider": best.get("provider", "amap_search"),
        "resolved_name": best.get("name") or name,
        "type": best.get("type") or best.get("typecode") or "",
        "entr_location": best.get("entr_location"),
        "navi_poiid": best.get("navi_poiid"),
    }


def geocode_place(name):
    overrides = load_geocode_overrides()
    override_key = None
    if name in overrides:
        override_key = name
    else:
        ranked_override_keys = sorted(
            overrides.keys(),
            key=lambda key: _score_override_candidate(name, key),
            reverse=True,
        )
        if ranked_override_keys and _score_override_candidate(name, ranked_override_keys[0]) > 0:
            override_key = ranked_override_keys[0]
    if override_key:
        item = overrides[override_key]
        return {
            "name": name,
            "lat": float(item["lat"]),
            "lon": float(item["lon"]),
            "display_name": item.get("display_name", override_key),
            "provider": item.get("provider", "override"),
        }

    is_chinese = bool(re.search(r"[\u4e00-\u9fff]", name))

    if is_chinese and BIG_AOI_RE.search(name):
        resolved = _resolve_origin_via_amap_search(name)
        if resolved:
            return resolved

    # Chinese address: try Amap geocoding first
    if is_chinese:
        try:
            from amap_geocode import geocode_address
            result = geocode_address(name)
            if result.get("success") and not _is_transit_candidate(name, "", result.get("level", "")):
                return {
                    "name": name,
                    "lat": result["lat"],
                    "lon": result["lon"],
                    "display_name": result.get("formatted_address", name),
                    "provider": "amap",
                }
        except Exception:
            pass

    queries = [name]
    if is_chinese:
        queries.append(f"{name}, 中国")
    for q in queries:
        params = {
            "q": q,
            "format": "jsonv2",
            "limit": 3,
            "addressdetails": 1,
        }
        if is_chinese:
            params["accept-language"] = "zh-CN"
            params["countrycodes"] = "cn"
        data = _http_get_json(GEOCODE_URL, params=params)
        if not data:
            continue
        candidates = data
        if is_chinese:
            candidates = [item for item in data if _is_china_like_result(item)]
            if not candidates:
                continue
        ranked = sorted(candidates, key=lambda item: _score_nominatim_candidate(name, item), reverse=True)
        item = ranked[0]
        return {
            "name": name,
            "lat": float(item["lat"]),
            "lon": float(item["lon"]),
            "display_name": item.get("display_name", name),
            "provider": "osm",
        }
    return None


def category_to_patterns(category):
    category = normalize_category(category)
    if category == "dessert":
        return [
            '["amenity"="cafe"]',
            '["shop"="pastry"]',
            '["shop"="confectionery"]',
            '["cuisine"~"ice_cream|dessert|coffee", i]',
        ]
    if category == "cafe":
        return [
            '["amenity"="cafe"]',
            '["cuisine"~"coffee", i]',
        ]
    if category == "tea":
        return [
            '["amenity"="cafe"]',
            '["cuisine"~"tea|bubble_tea|milk_tea", i]',
        ]
    if category == "bakery":
        return [
            '["shop"="bakery"]',
            '["shop"="pastry"]',
        ]
    if category == "restaurant":
        return [
            '["amenity"="restaurant"]',
            '["amenity"="fast_food"]',
            '["cuisine"~"restaurant|hotpot|japanese|western|chinese|bbq|noodle", i]',
        ]
    return ['["amenity"="restaurant"]']


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))



def search_overpass(req, origin_name, radius_m=2200, limit=8, enable_accessibility=True):
    from planner import rank_poi
    origin = geocode_place(origin_name)
    if not origin:
        return {"provider": "osm_overpass", "origin": None, "results": [], "error": "origin_geocode_failed"}

    patterns = category_to_patterns(req["category"])
    blocks = []
    for pat in patterns:
        blocks.append(f"node(around:{radius_m},{origin['lat']},{origin['lon']}){pat};")
        blocks.append(f"way(around:{radius_m},{origin['lat']},{origin['lon']}){pat};")
        blocks.append(f"relation(around:{radius_m},{origin['lat']},{origin['lon']}){pat};")
    query = "[out:json][timeout:20];(" + "".join(blocks) + ");out center tags;"

    try:
        data = _http_get_json(OVERPASS_URL, method="POST", data="data=" + urllib.parse.quote(query, safe=""))
    except Exception as e:
        return {"provider": "osm_overpass", "origin": origin, "results": [], "error": str(e)}

    anchors = load_anchors().get(origin_name, [])
    results = []
    seen = set()
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        lat = el.get("lat") or (el.get("center") or {}).get("lat")
        lon = el.get("lon") or (el.get("center") or {}).get("lon")
        if lat is None or lon is None:
            continue
        key = (name, round(lat, 5), round(lon, 5))
        if key in seen:
            continue
        seen.add(key)
        poi = {
            "name": name,
            "lat": lat,
            "lon": lon,
            "tags": tags,
            "distance_m": int(haversine_m(origin["lat"], origin["lon"], lat, lon)),
            "provider": "osm_overpass",
        }
        poi["score"] = rank_poi(req, poi, origin, anchors)
        results.append(poi)

    if enable_accessibility and AMAP_AVAILABLE and results:
        try:
            results = amap_direction.enrich_pois_with_accessibility(results, origin['lon'], origin['lat'])
        except Exception:
            pass

    if results and "total_score" in results[0]:
        results.sort(key=lambda x: (-x.get("total_score", 0), x.get("accessibility", {}).get("duration_min", 999)))
    else:
        results.sort(key=lambda x: (-x["score"], x["distance_m"]))

    return {"provider": "osm_overpass", "origin": origin, "results": results[:limit], "error": None}


def _format_amap_pois(pois, req, ref_lat, ref_lon, anchors, limit, enable_accessibility=True):
    """Format raw Amap POI results with filtering, scoring, and accessibility enrichment."""
    from planner import rank_poi
    results = []
    category = normalize_category(req.get("category", "restaurant"))

    for poi in pois:
        poi_name = poi.get("name", "")

        should_avoid = False
        for pattern in req.get("avoid", []):
            if pattern.lower() in poi_name.lower():
                should_avoid = True
                break
        if should_avoid:
            continue

        meets_constraints = True
        for constraint in req.get("constraints", []):
            if constraint == "seating" and not any(word in poi_name for word in ["厅", "堂", "店", "铺", "屋", "馆"]):
                meets_constraints = False
                break
        if not meets_constraints:
            continue

        distance_m = poi.get("distance_m")
        if distance_m in (None, "", 0):
            distance_m = poi.get("distance")
        try:
            distance_m = int(float(distance_m)) if distance_m not in (None, "") else None
        except (TypeError, ValueError):
            distance_m = None
        if distance_m is None:
            distance_m = int(haversine_m(ref_lat, ref_lon, poi.get("lat"), poi.get("lon")))

        formatted_poi = {
            "name": poi.get("name"),
            "lat": poi.get("lat"),
            "lon": poi.get("lon"),
            "address": poi.get("address"),
            "tel": poi.get("tel"),
            "distance_m": distance_m,
            "provider": "amap_poi",
            "typecode": poi.get("typecode"),
            "tags": {
                "name": poi.get("name"),
                "amenity": "restaurant" if category == "restaurant" else category,
                "cuisine": poi.get("type", ""),
                "typecode": poi.get("typecode", ""),
            },
        }
        formatted_poi["score"] = rank_poi(req, formatted_poi, {"lat": ref_lat, "lon": ref_lon}, anchors)
        results.append(formatted_poi)

        if len(results) >= limit:
            break

    if enable_accessibility and AMAP_AVAILABLE and results:
        try:
            results = amap_direction.enrich_pois_with_accessibility(results, ref_lon, ref_lat)
        except Exception:
            pass

    if results and "total_score" in results[0]:
        results.sort(key=lambda x: (-x.get("total_score", 0), x.get("accessibility", {}).get("duration_min", 999)))
    else:
        results.sort(key=lambda x: (-x["score"], x["distance_m"]))

    return results


def search_amap_poi(req, origin_name, radius_m=3000, limit=8, enable_accessibility=True):
    origin = geocode_place(origin_name)
    if not origin:
        return {"provider": "amap_poi", "origin": None, "results": [], "error": "origin_geocode_failed"}

    if not AMAP_POI_AVAILABLE:
        return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)

    category = normalize_category(req.get("category", "restaurant"))
    keywords = AMAP_CATEGORY_KEYWORDS.get(category, category or "餐厅")

    try:
        raw_results = amap_poi.search_by_keywords(
            keywords=keywords,
            center_lng=origin["lon"],
            center_lat=origin["lat"],
            radius=radius_m,
            limit=limit * 2,
        )
        if not raw_results:
            return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)
    except Exception:
        return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)

    anchors = load_anchors().get(origin_name, [])
    results = _format_amap_pois(raw_results, req, origin["lat"], origin["lon"], anchors, limit, enable_accessibility)
    return {"provider": "amap_poi", "origin": origin, "results": results, "error": None}


def search_amap_poi_by_coords(req, lat, lon, radius_m=3000, limit=8, enable_accessibility=True):
    """Like search_amap_poi, but takes explicit coordinates (e.g. from IP geolocation)
    instead of a place name that needs geocoding."""
    if not AMAP_POI_AVAILABLE:
        return {"provider": "amap_poi", "origin": None, "results": [], "error": "amap_poi_unavailable"}

    display_name = f"{lat:.6f},{lon:.6f}"
    origin = {
        "name": display_name,
        "lat": lat,
        "lon": lon,
        "display_name": display_name,
        "provider": "amap_ip",
    }

    category = normalize_category(req.get("category", "restaurant"))
    keywords = AMAP_CATEGORY_KEYWORDS.get(category, category or "餐厅")

    try:
        raw_results = amap_poi.search_by_keywords(
            keywords=keywords,
            center_lng=lon,
            center_lat=lat,
            radius=radius_m,
            limit=limit * 2,
        )
    except Exception:
        return {"provider": "amap_poi", "origin": origin, "results": [], "error": "search_failed"}

    anchors = load_anchors().get("", [])
    results = _format_amap_pois(raw_results or [], req, lat, lon, anchors, limit, enable_accessibility)
    return {"provider": "amap_poi", "origin": origin, "results": results, "error": None}


def _maoyan_http_get(url, params=None, timeout=15):
    """HTTP GET with Maoyan mobile headers."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148")
    req.add_header("Accept", "application/json")
    req.add_header("Referer", "https://m.maoyan.com/")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def _maoyan_city_id(city_name):
    for key, cid in MAOYAN_CITY_MAP.items():
        if key in (city_name or ""):
            return cid
    try:
        data = _maoyan_http_get("https://m.maoyan.com/ajax/search", {"kw": city_name or "", "cityId": "0", "stype": "0"})
        cities = (data.get("data") or {}).get("city") or []
        if cities:
            return cities[0].get("id")
    except Exception:
        pass
    return None


def search_maoyan_cinema_halls(city_name, special_hall_types=None, max_cinemas=100):
    """Search Maoyan for cinemas with specific hall types using the cinema list API.
    Returns dict with city_name, cinemas list (name, address, lat, lon, hall_types)."""
    if special_hall_types is None:
        special_hall_types = list(SPECIAL_HALL_KEYWORDS.keys())

    city_id = _maoyan_city_id(city_name)
    if not city_id:
        return {"city_name": city_name, "cinemas": [], "error": "city_not_found"}

    all_cinemas = []
    offset = 0
    FETCH_CAP = 500
    while len(all_cinemas) < FETCH_CAP:
        try:
            data = _maoyan_http_get(MAOYAN_CINEMA_LIST_URL,
                                    {"cityId": str(city_id), "offset": str(offset), "limit": "20"},
                                    timeout=15)
            cinemas = data.get("cinemas", [])
            if not cinemas:
                break
            all_cinemas.extend(cinemas)
            offset += 20
        except Exception:
            break

    results = []
    for cinema in all_cinemas[:max_cinemas]:
        tag = cinema.get("tag", {})
        hall_types_raw = tag.get("hallType", []) if isinstance(tag, dict) else []
        if not hall_types_raw:
            continue

        mapped = _map_hall_types(hall_types_raw, special_hall_types)
        if not mapped:
            continue

        cinema_name = cinema.get("nm", "")
        cinema_addr = cinema.get("addr", "")
        cinema_lat = cinema.get("lat")
        cinema_lng = cinema.get("lng")

        results.append({
            "name": cinema_name,
            "address": cinema_addr,
            "lat": float(cinema_lat) if cinema_lat else None,
            "lon": float(cinema_lng) if cinema_lng else None,
            "hall_types": mapped,
            "hall_types_raw": hall_types_raw,
            "maoyan_id": cinema.get("id"),
            "provider": "maoyan",
        })

    return {"city_name": city_name, "cinemas": results, "city_id": city_id, "error": None}


def _map_hall_types(hall_types_raw, target_types):
    """Map raw Maoyan hall type strings to our SPECIAL_HALL_KEYWORDS categories."""
    mapped = []
    for ht in hall_types_raw:
        for hall_key in target_types:
            keywords = SPECIAL_HALL_KEYWORDS.get(hall_key, [hall_key])
            if any(kw.upper() in ht.upper() for kw in keywords):
                if hall_key not in mapped:
                    mapped.append(hall_key)
    return mapped


def search_pois(req, origin_name, radius_m=3000, limit=8, enable_accessibility=True, ip_location=None):
    # When origin is unresolved but IP coordinates are available, use them directly
    if ip_location and (not origin_name or origin_name == "未指定起点"):
        return search_amap_poi_by_coords(
            req,
            lat=ip_location["lat"],
            lon=ip_location["lon"],
            radius_m=radius_m,
            limit=limit,
            enable_accessibility=enable_accessibility,
        )

    # Detect bare GPS coordinates (e.g., "39.060938,117.281150")
    gps_match = re.match(r"^\s*(-?\d+\.?\d*)\s*[,，]\s*(-?\d+\.?\d*)\s*$", origin_name)
    if gps_match and AMAP_POI_AVAILABLE:
        lat, lon = float(gps_match.group(1)), float(gps_match.group(2))
        result = search_amap_poi_by_coords(req, lat, lon, radius_m, limit, enable_accessibility)
        if result.get("results") and len(result["results"]) > 0:
            return result
        return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)

    is_chinese_location = bool(re.search(r"[\u4e00-\u9fff]", origin_name))

    if is_chinese_location and AMAP_POI_AVAILABLE:
        result = search_amap_poi(req, origin_name, radius_m, limit, enable_accessibility)
        if result.get("results") and len(result["results"]) > 0:
            return result
        return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)
    return search_overpass(req, origin_name, radius_m, limit, enable_accessibility)
