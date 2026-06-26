#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from providers import normalize_category, search_pois

try:
    from amap_ip_location import get_ip_location
    IP_LOCATION_AVAILABLE = True
except ImportError:
    IP_LOCATION_AVAILABLE = False

try:
    from macos_location import get_macos_location
    MACOS_LOCATION_AVAILABLE = True
except ImportError:
    MACOS_LOCATION_AVAILABLE = False

SKILL_DIR = Path(__file__).resolve().parents[1]
UNIFIED_SEARCH = SKILL_DIR.parent / "unified-search" / "scripts" / "unified-search.sh"
ANCHORS_FILE = SKILL_DIR / "config" / "anchors.json"

SEARCH_PROVIDER_LIMIT = 15
RECOMMEND_PROVIDER_LIMIT = 8
SEARCH_WEB_VERIFY_LIMIT = 5
RECOMMEND_WEB_VERIFY_LIMIT = 3
SEARCH_DISPLAY_LIMIT = 10
RECOMMEND_DISPLAY_LIMIT = 3

CATEGORY_KEYWORDS = {
    "dessert": ["甜品", "冰淇淋", "酸奶", "gelato", "冰沙"],
    "cafe": ["咖啡", "咖啡店", "咖啡馆", "下午茶"],
    "tea": ["奶茶", "茶饮", "饮品", "果茶"],
    "bakery": ["面包", "蛋糕", "烘焙", "面包店"],
    "restaurant": ["饭馆", "餐厅", "美食", "吃饭"],
    "网吧": ["网吧", "网咖", "电竞馆"],
    "KTV": ["KTV", "唱歌", "量贩KTV"],
    "电影院": ["电影院", "影城", "看电影"],
    "酒店": ["酒店", "宾馆", "住宿", "旅馆", "民宿"],
    "医院": ["医院", "诊所", "综合医院"],
    "药店": ["药店", "药房", "大药房"],
    "快递": ["快递", "物流", "菜鸟驿站"],
    "健身房": ["健身房", "游泳", "健身"],
    "超市": ["超市", "便利店", "小卖部"],
    "银行": ["银行", "ATM", "存取款"],
    "充电站": ["充电桩", "充电站", "加油站"],
    "桌游": ["桌游", "剧本杀", "密室逃脱"],
    "台球": ["台球", "桌球"],
    "理发": ["理发", "美发"],
    "宠物": ["宠物"],
    "按摩": ["足疗", "按摩"],
}

CATEGORY_EVIDENCE_HINTS = {
    "dessert": ["甜品", "冰淇淋", "酸奶", "gelato", "咖啡甜品"],
    "cafe": ["咖啡", "咖啡馆", "下午茶", "拿铁"],
    "tea": ["奶茶", "茶饮", "果茶", "柠檬茶"],
    "bakery": ["面包", "蛋糕", "烘焙", "吐司"],
    "restaurant": ["饭馆", "餐厅", "美食", "火锅", "烧烤", "面馆", "小吃", "人均"],
    "电影院": ["电影院", "看电影", "影院", "影城", "影厅", "电影", "IMAX", "4DX", "杜比", "CINITY", "巨幕"],
}

CATEGORY_ALIASES = {
    "dessert": "dessert",
    "甜品": "dessert",
    "冰淇淋": "dessert",
    "酸奶": "dessert",
    "gelato": "dessert",
    "cafe": "cafe",
    "咖啡": "cafe",
    "咖啡店": "cafe",
    "咖啡馆": "cafe",
    "tea": "tea",
    "奶茶": "tea",
    "茶饮": "tea",
    "饮品": "tea",
    "bakery": "bakery",
    "面包": "bakery",
    "蛋糕": "bakery",
    "烘焙": "bakery",
    "restaurant": "restaurant",
    "dinner": "restaurant",
    "餐厅": "restaurant",
    "饭馆": "restaurant",
    "饭店": "restaurant",
    "吃饭": "restaurant",
    "晚餐": "restaurant",
    "馆子": "restaurant",
    "美食": "restaurant",
    "火锅": "restaurant",
    "烧烤": "restaurant",
    "面馆": "restaurant",
    # Non-food categories (aligned with amap_poi TYPECODE_MAP)
    "网吧": "网吧",
    "网咖": "网吧",
    "电竞": "网吧",
    "KTV": "KTV",
    "唱歌": "KTV",
    "电影院": "电影院",
    "看电影": "电影院",
    "影院": "电影院",
    "4D电影院": "电影院",
    "酒店": "酒店",
    "宾馆": "酒店",
    "旅馆": "酒店",
    "住宿": "酒店",
    "民宿": "酒店",
    "医院": "医院",
    "诊所": "医院",
    "药店": "药店",
    "药房": "药店",
    "快递": "快递",
    "物流": "快递",
    "菜鸟": "快递",
    "健身房": "健身房",
    "游泳馆": "健身房",
    "超市": "超市",
    "便利店": "超市",
    "银行": "银行",
    "加油站": "加油站",
    "充电桩": "充电站",
    "充电站": "充电站",
    "桌游": "桌游",
    "剧本杀": "桌游",
    "密室": "桌游",
    "台球": "台球",
    "桌球": "台球",
    "理发": "理发",
    "美发": "理发",
    "宠物": "宠物",
    "足疗": "按摩",
    "按摩": "按摩",
}

MODE_ALIASES = {
    "search": "search",
    "recommend": "recommend",
}

PREFERENCE_HINTS = {
    "yogurt": ["酸奶", "yogurt"],
    "gelato": ["gelato", "手工冰淇淋", "意式冰淇淋"],
    "smoothie": ["冰沙", "果昔", "smoothie"],
    "light": ["清爽", "不腻", "轻食感"],
}

CONSTRAINT_HINTS = {
    "metro": ["地铁可达", "近地铁", "地铁站附近"],
    "seating": ["有座位", "堂食", "能坐着"],
    "environment": ["环境好", "适合约会", "安静", "适合聊天"],
    "mall": ["商场", "购物中心", "mall"],
}

AVOID_HINTS = {
    "night_market": ["夜市", "小吃街"],
    "takeaway_only": ["外带", "窗口", "档口"],
    "no_seating": ["无座位", "站着吃"],
}

CITYISH_RE = re.compile(r"(city8\.com|城市吧|map|地图|购物中心|商场|店|餐厅|饭馆|美食|甜品|冰淇淋|咖啡)", re.I)
RADIUS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(km|KM|公里|千米|m|M|米)")
EXPLICIT_MODE_RE = re.compile(r"\bmode\s*=\s*(search|recommend)\b", re.I)

SEARCH_HINTS = ["有哪些", "附近有什么", "帮我找", "找找", "列几个", "列出", "给我看看", "周边", "附近的", "附近", "2km", "1km", "3km"]
RECOMMEND_HINTS = ["推荐一家", "推荐一个", "帮我选", "挑一个", "最适合", "最值得", "帮我拍板", "首选", "哪个最好", "哪家最好"]


def load_anchors():
    if ANCHORS_FILE.exists():
        return json.loads(ANCHORS_FILE.read_text())
    return {}


def normalize_category(value: str):
    raw = (value or "").strip().lower()
    if not raw:
        return "restaurant"
    if raw in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[raw]
    for key, canonical in CATEGORY_ALIASES.items():
        if key in raw:
            return canonical
    return raw or "restaurant"


def normalize_mode(value: str):
    raw = (value or "").strip().lower()
    return MODE_ALIASES.get(raw, None)


def infer_mode(query: str):
    q = (query or "").strip()
    if not q:
        return "search"
    explicit = EXPLICIT_MODE_RE.search(q)
    if explicit:
        return explicit.group(1).lower()
    lowered = q.lower()
    if any(token.lower() in lowered for token in RECOMMEND_HINTS):
        return "recommend"
    if any(token.lower() in lowered for token in SEARCH_HINTS):
        return "search"
    return "search"


def infer_category(query: str):
    q = (query or "").lower()
    if any(x in q for x in ["甜品", "gelato", "酸奶", "冰淇淋", "dessert"]):
        return "dessert"
    if any(x in q for x in ["咖啡", "cafe"]):
        return "cafe"
    if any(x in q for x in ["奶茶", "茶饮", "果茶", "饮品"]):
        return "tea"
    if any(x in q for x in ["面包", "蛋糕", "烘焙", "bakery"]):
        return "bakery"
    if any(x in q for x in ["晚餐", "餐厅", "饭馆", "饭店", "吃饭", "馆子", "restaurant", "dinner", "美食", "火锅", "烧烤"]):
        return "restaurant"
    # Non-food categories
    if any(x in q for x in ["网吧", "网咖", "电竞"]):
        return "网吧"
    if any(x in q for x in ["KTV", "唱歌", "卡拉"]):
        return "KTV"
    if any(x in q for x in ["电影院", "看电影", "影院"]):
        return "电影院"
    if any(x in q for x in ["酒店", "宾馆", "旅馆", "住宿", "民宿"]):
        return "酒店"
    if any(x in q for x in ["医院", "诊所", "社区医院"]):
        return "医院"
    if any(x in q for x in ["药店", "药房"]):
        return "药店"
    if any(x in q for x in ["快递", "物流", "菜鸟"]):
        return "快递"
    if any(x in q for x in ["健身房", "健身", "游泳", "泳池", "游泳馆", "水上乐园", "运动", "锻炼", "gym", "fitness", "swim", "pool"]):
        return "健身房"
    if any(x in q for x in ["超市", "便利店", "小卖部"]):
        return "超市"
    if any(x in q for x in ["银行", "ATM", "存取款"]):
        return "银行"
    if any(x in q for x in ["加油站", "充电桩", "充电站"]):
        return "充电站"
    if any(x in q for x in ["桌游", "剧本杀", "密室"]):
        return "桌游"
    if any(x in q for x in ["台球", "桌球"]):
        return "台球"
    if any(x in q for x in ["理发", "美发", "剪发"]):
        return "理发"
    if any(x in q for x in ["宠物"]):
        return "宠物"
    if any(x in q for x in ["足疗", "按摩", "推拿"]):
        return "按摩"
    return None


def _extract_fallback_keywords(query: str):
    """When infer_category returns None, extract meaningful search terms from the original query
    for direct Amap keyword search. Removes noise words, location hints, and pronouns."""
    if not query:
        return None
    noise = r'(我|我们|咱|咱们|自己|我这|我这里|我的位置|我的地点|当前位置|附近的|附近|周边的|周边|周围的|周围|方圆|出发|去|找|搜索|有没有|有什么|给我|帮我|我要|我想|请问|可以|能|怎么|哪里|哪有|哪儿|有的|一些|一下|个|的)'
    q = re.sub(noise, ' ', query)
    q = re.sub(r'\s+', ' ', q).strip()
    return q if q and len(q) >= 2 else None


def split_csv(s):
    if not s:
        return []
    return [x.strip() for x in re.split(r"[,，]", s) if x.strip()]


def parse_radius_m(text: str, default_m: int = 3000):
    if not text:
        return default_m
    m = RADIUS_RE.search(text)
    if not m:
        return default_m
    value = float(m.group(1))
    unit = m.group(2).lower()
    if unit in {"km", "公里", "千米"}:
        return int(value * 1000)
    return int(value)


def clean_origin_text(origin: str):
    """Clean origin text. Returns empty string for self-references so caller falls back to '未指定起点'."""
    if not origin:
        return origin
    origin = origin.strip(" ，,")
    origin = re.sub(r"\s*\d+(?:\.\d+)?\s*(?:km|KM|公里|千米|m|M|米)\s*$", "", origin)
    origin = re.sub(r"\s*(附近的|附近|周边的|周边)\s*$", "", origin)
    origin = origin.strip(" ，,")
    # Treat first-person pronouns as self-references → empty → fallback to "未指定起点" → triggers CoreLocation
    if origin and re.fullmatch(r"(我|我们|咱|咱们|自己|我这里|我这|我的位置|我的地点|当前位置)", origin):
        return ""
    return origin


def parse_request(args):
    query = args.query or ""
    origin = args.origin
    if not origin and query:
        m = re.search(r"(.+?)(附近|周边|出发)", query)
        if m:
            origin = clean_origin_text(m.group(1))
    raw_cat = args.category or infer_category(query)
    if raw_cat is None:
        raw_cat = _extract_fallback_keywords(query) or "restaurant"
    category = normalize_category(raw_cat)
    mode = normalize_mode(getattr(args, "mode", None)) or infer_mode(query)
    preferences = split_csv(args.preferences)
    constraints = split_csv(args.constraints)
    avoid = split_csv(args.avoid)
    radius_m = parse_radius_m(query)
    if radius_m == 3000:
        for c in constraints:
            candidate = parse_radius_m(c)
            if candidate != 3000:
                radius_m = candidate
                break

    if query and not preferences:
        q = query.lower()
        for key, hints in PREFERENCE_HINTS.items():
            if any(h in q for h in [x.lower() for x in hints]):
                preferences.append(key)
    if query and not constraints:
        q = query.lower()
        for key, hints in CONSTRAINT_HINTS.items():
            if any(h.lower() in q for h in hints):
                constraints.append(key)
    if query and not avoid:
        q = query.lower()
        for key, hints in AVOID_HINTS.items():
            if any(h.lower() in q for h in hints):
                avoid.append(key)

    origin_final = clean_origin_text(origin or "未指定起点")

    # Location resolution: try macOS CoreLocation first, fall back to IP geolocation
    ip_location = None
    NEARBY_HINTS_RE = re.compile(r"(附近|周边|附近有什么|周围的|周围的店|方圆)")
    if origin_final == "未指定起点" and NEARBY_HINTS_RE.search(query):
        if MACOS_LOCATION_AVAILABLE:
            try:
                ip_location = get_macos_location()
            except Exception:
                pass
        if not ip_location and IP_LOCATION_AVAILABLE:
            try:
                ip_location = get_ip_location()
            except Exception:
                pass

    return {
        "query": query,
        "origin": origin_final,
        "category": category,
        "mode": mode,
        "radius_m": radius_m,
        "preferences": sorted(set(preferences)),
        "constraints": sorted(set(constraints)),
        "avoid": sorted(set(avoid)),
        "ip_location": ip_location,
    }


def expand_anchors(origin):
    anchors_map = load_anchors()
    anchors = anchors_map.get(origin, [])
    if not anchors:
        anchors = [origin]
    uniq = []
    for x in [origin] + anchors:
        if x and x not in uniq:
            uniq.append(x)
    return uniq


def _reverse_geocode(lat, lon):
    """Convert GPS coordinates to a human-readable location via Amap regeo API."""
    key = os.getenv("AMAP_KEY", "")
    if not key:
        return None
    try:
        url = f"https://restapi.amap.com/v3/geocode/regeo?location={lon},{lat}&key={key}&radius=1000&extensions=base"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("status") == "1":
            comp = data["regeocode"]["addressComponent"]
            district = comp.get("district", "")
            township = comp.get("township", "")
            if township and township != "[]":
                return f"{district}{township}" if district else township
            return district or None
    except Exception:
        pass
    return None


def _resolve_gps_anchor(anchor):
    """If anchor is bare GPS coords, resolve to human-readable name."""
    m = re.match(r"^\s*(-?\d+\.?\d*)\s*[,，]\s*(-?\d+\.?\d*)\s*$", anchor)
    if m:
        resolved = _reverse_geocode(float(m.group(1)), float(m.group(2)))
        if resolved:
            return resolved
    return anchor


def build_queries(req, anchors, poi_candidates=None, mode="recommend"):
    keywords = CATEGORY_KEYWORDS.get(req["category"], [req["category"]])
    pref_terms = []
    for p in req["preferences"]:
        pref_terms.extend(PREFERENCE_HINTS.get(p, [p]))
    cons_terms = []
    for c in req["constraints"]:
        cons_terms.extend(CONSTRAINT_HINTS.get(c, [c]))

    core_pref = "/".join(pref_terms[:3]) if pref_terms else keywords[0]
    core_cons = " ".join(cons_terms[:3]) if cons_terms else ("堂食 有座位" if req["category"] == "restaurant" else "环境好")

    queries = []
    if mode == "recommend" and poi_candidates:
        for poi in poi_candidates[:2]:
            queries.append(f"{poi['name']} {req['origin']} 评价 环境 人均")
    for a in anchors[:2]:
        a_display = _resolve_gps_anchor(a)
        queries.append(f"{a_display} {keywords[0]} {core_cons} {core_pref}")
        if mode == "search":
            queries.append(f"{a_display} {' '.join(keywords[:3])} 哪些值得去")

    out = []
    for q in queries:
        if q not in out:
            out.append(q)
    return out[: (2 if mode == 'recommend' else 3)]


def run_unified_search(query):
    if not UNIFIED_SEARCH.exists():
        return {"query": query, "ok": False, "output": "unified-search script not found"}
    cmd = ["bash", str(UNIFIED_SEARCH), query, "--num", "5", "--topic", "general"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        text = (proc.stdout or "") + "\n" + (proc.stderr or "")
        return {"query": query, "ok": proc.returncode == 0, "output": text}
    except subprocess.TimeoutExpired:
        return {"query": query, "ok": False, "output": "timeout"}


def extract_candidate_lines(output):
    lines = []
    skip_prefixes = (
        "🔍 综合搜索:",
        "Run Dir:",
        "Query:",
        "Engine Summary",
        "Hit Summary",
        "✅ 综合搜索完成",
        "━━━━━━━━━━━━━━━━",
    )
    for raw in output.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(skip_prefixes):
            continue
        if line.startswith("Title:") or line.startswith("URL:"):
            lines.append(line)
        elif CITYISH_RE.search(line) and ("http" in line or "店" in line or "餐厅" in line or "饭馆" in line or "购物中心" in line or "商场" in line):
            lines.append(line)
    return lines[:20]


def _get_evidence_hints(category):
    """Auto-derive evidence hints from CATEGORY_EVIDENCE_HINTS or CATEGORY_ALIASES.

    If the category has curated hints in CATEGORY_EVIDENCE_HINTS, use those.
    Otherwise, collect all aliases that map to this category from CATEGORY_ALIASES.
    This means adding a new category to CATEGORY_ALIASES automatically generates hints.
    """
    if category in CATEGORY_EVIDENCE_HINTS:
        return CATEGORY_EVIDENCE_HINTS[category]
    hints = [category]
    for alias, canonical in CATEGORY_ALIASES.items():
        if canonical == category and alias != category:
            hints.append(alias)
    return hints


def score_evidence(req, candidate_lines):
    text = "\n".join(candidate_lines)
    score = 0
    hints = _get_evidence_hints(req["category"])

    if any(x in text for x in hints):
        score += 28
    if req["category"] == "restaurant" and any(x in text for x in ["人均", "美食", "餐厅", "饭馆", "火锅", "烧烤"]):
        score += 22
    if req["category"] != "restaurant" and any(x in text for x in ["环境", "堂食", "人均", "位置示意图", "交通指引"]):
        score += 18
    if req["category"] == "restaurant" and any(x in text for x in ["环境", "堂食", "位置", "营业时间", "评价"]):
        score += 18
    if any(x in text for x in ["购物中心", "商场", "广场"]):
        score += 10
    if req["origin"] in text:
        score += 10
    if any(a in text for a in expand_anchors(req["origin"])):
        score += 10
    if any(x in text for x in ["NO_EXACT_HIT", "bestHit: none", "none"]):
        score -= 10
    return max(0, min(100, score))


def _evidence_level(web_score):
    if web_score is None:
        return "none"
    if web_score >= 70:
        return "strong"
    if web_score >= 45:
        return "medium"
    return "weak"


def rank_poi(req, poi, origin, anchors):
    score = 0
    tags = poi.get("tags", {})
    name = (poi.get("name") or tags.get("name") or "").lower()
    cuisine = (tags.get("cuisine") or "").lower()
    shop = (tags.get("shop") or "").lower()
    amenity = (tags.get("amenity") or "").lower()
    category = normalize_category(req.get("category", "restaurant"))

    dist = poi.get("distance_m")
    if dist is None:
        dist = 99999
    if dist <= 500:
        score += 30
    elif dist <= 1200:
        score += 20
    elif dist <= 2500:
        score += 10

    if amenity == "cafe":
        score += 18
    if amenity == "restaurant":
        score += 18
    if shop in {"pastry", "confectionery", "bakery"}:
        score += 18
    if re.search(r"ice_cream|dessert|coffee", cuisine, re.I):
        score += 18

    if category == "dessert" and re.search(r"gelato|ice cream|yogurt|dessert|甜|冰|咖啡", name, re.I):
        score += 20
    if category == "restaurant" and re.search(r"餐|饭|锅|烧烤|面|馆|小吃|饺|包子|串|麻辣烫", name, re.I):
        score += 20
    if category == "restaurant" and re.search(r"中餐|火锅|烧烤|西餐|日餐|快餐|特色|地方风味", cuisine, re.I):
        score += 15
    if category == "tea" and re.search(r"茶|奶茶|饮品|果茶", name + " " + cuisine, re.I):
        score += 18
    if category == "bakery" and re.search(r"面包|蛋糕|烘焙|吐司", name + " " + cuisine, re.I):
        score += 18

    if "mall" in req.get("constraints", []) and re.search(r"广场|中心|mall|购物|时代", name, re.I):
        score += 10
    if "seating" in req.get("constraints", []) and amenity in {"cafe", "restaurant"}:
        score += 8

    text = " ".join([name, cuisine, shop, amenity])
    if "night_market" in req.get("avoid", []) and re.search(r"夜市|market", text, re.I):
        score -= 30
    if "takeaway_only" in req.get("avoid", []) and re.search(r"外带|窗口|档口", text, re.I):
        score -= 20

    return max(0, min(100, score))


def _normalize_text_for_match(text):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", (text or "").lower())


def _has_store_name_evidence(store_name, candidate_lines):
    target = _normalize_text_for_match(store_name)
    if not target:
        return False
    for line in candidate_lines:
        normalized = _normalize_text_for_match(line)
        if target in normalized:
            return True
    if len(target) >= 4:
        compact = target[: min(len(target), 8)]
        for line in candidate_lines:
            normalized = _normalize_text_for_match(line)
            if compact and compact in normalized:
                return True
    return False


def enrich_poi_with_web(req, pois, verify_limit=2):
    poi_list = []
    for idx, poi in enumerate(pois):
        p = dict(poi)
        p["_base_score"] = p.get("total_score", p.get("score", 0))
        poi_list.append(p)

    if verify_limit > 0:
        print(f"   ⏳ Web enrichment：并行搜 {min(verify_limit, len(poi_list))} 条 POI...", flush=True)
    web_futures = {}
    with ThreadPoolExecutor(max_workers=min(verify_limit, 5)) as executor:
        for p in poi_list[:verify_limit]:
            q = f"{p['name']} {req['origin']} 评价 环境 人均"
            future = executor.submit(run_unified_search, q)
            web_futures[future] = (p, q)

        for future in as_completed(web_futures):
            p, q = web_futures[future]
            run = future.result()
            lines = extract_candidate_lines(run["output"])
            web_score = score_evidence(req, lines)
            has_store_name = _has_store_name_evidence(p.get("name"), lines)
            if not has_store_name:
                web_score = min(web_score, 35)
            p["web_query"] = q
            p["web_score"] = web_score
            p["web_has_store_name"] = has_store_name
            p["web_lines"] = lines[:6]
            p["evidence_level"] = _evidence_level(web_score)
            p["total_score"] = int(p["_base_score"] * 0.75 + web_score * 0.25)
            print(f"   ✅ {p['name']} web_score={web_score}", flush=True)

    for p in poi_list[verify_limit:]:
        p["web_query"] = None
        p["web_score"] = None
        p["web_lines"] = []
        p["evidence_level"] = "none"
        p["total_score"] = int(p["_base_score"])

    poi_list.sort(key=lambda x: (-x.get("total_score", 0), x.get("distance_m", 99999)))
    for p in poi_list:
        p.pop("_base_score", None)
    return poi_list


def _build_evidence_bundles(req, search_runs):
    bundles = []
    for run in search_runs:
        lines = extract_candidate_lines(run["output"])
        score = score_evidence(req, lines)
        bundles.append({
            "query": run["query"],
            "score": score,
            "lines": lines,
            "ok": run["ok"],
        })
    bundles.sort(key=lambda x: x["score"], reverse=True)
    return bundles


def _assess_bundle_quality(bundles, req):
    """Assess whether unified-search evidence is sufficient."""
    if not bundles:
        return {"quality": "poor", "need_fallback": True, "reasons": ["no_evidence"]}

    scores = [b["score"] for b in bundles]
    max_score = max(scores) if scores else 0
    avg_score = sum(scores) / len(scores) if scores else 0

    reasons = []
    need_fallback = False

    zero_score_queries = [b for b in bundles if b["score"] <= 2]
    if zero_score_queries:
        reasons.append(f"{len(zero_score_queries)} queries with score<=2")
        need_fallback = True

    if max_score <= 2:
        reasons.append(f"max evidence score only {max_score}")
        need_fallback = True

    if avg_score < 10:
        reasons.append(f"avg evidence score {avg_score:.1f} < 10")
        need_fallback = True

    if not need_fallback:
        return {"quality": "acceptable", "need_fallback": False, "reasons": []}

    return {
        "quality": "poor" if max_score <= 2 else "weak",
        "need_fallback": need_fallback,
        "reasons": reasons,
    }


def _specialty_fallback_run(req):
    """Run specialty provider fallback. Returns a pseudo-run dict or None."""
    from providers import search_maoyan_cinema_halls, SPECIAL_HALL_KEYWORDS

    category = req.get("category", "")
    if category != "电影院":
        return None

    origin = req.get("origin", "")
    city_match = re.search(
        r'(天津|北京|上海|广州|深圳|成都|杭州|南京|武汉|西安|重庆|长沙|苏州|郑州|厦门|福州|青岛|大连|沈阳|昆明)',
        origin
    )
    city_name = city_match.group(1) if city_match else "天津"

    query_text = req.get("query", "")
    special_types = []
    for hall_key in SPECIAL_HALL_KEYWORDS:
        if any(kw.lower() in query_text.lower() for kw in SPECIAL_HALL_KEYWORDS[hall_key]):
            special_types.append(hall_key)

    if not special_types:
        special_types = ["4DX", "D-BOX", "IMAX", "杜比"]

    try:
        result = search_maoyan_cinema_halls(city_name, special_types, max_cinemas=80)
        cinemas = result.get("cinemas", [])
    except Exception:
        return None

    if not cinemas:
        return None

    lines = []
    lines.append(f"Title: 猫眼专项查询 {city_name} 电影院 {' '.join(special_types)}")
    lines.append(f"URL: https://m.maoyan.com/cinemas?cityName={urllib.parse.quote(city_name)}")
    for c in cinemas:
        hall_str = ", ".join(c.get("hall_types", []))
        addr = c.get("address", "")
        lines.append(f"Title: {c['name']} ({hall_str})")
        if addr:
            lines.append(f"{c['name']} {addr} 影厅: {hall_str} 电影院 看电影 影院 {city_name}")

    return {
        "query": f"猫眼专项: {origin} 电影院",
        "ok": True,
        "output": "\n".join(lines),
        "provider": "maoyan",
    }


def _confidence_band(results):
    if not results:
        return "low"
    top = results[0].get("total_score", results[0].get("score", 0))
    if len(results) >= 5 and top >= 75:
        return "high"
    if top >= 55:
        return "medium"
    return "low"


def decide_search(req, poi_result, search_runs, enriched_pois):
    bundles = _build_evidence_bundles(req, search_runs)
    anchors = expand_anchors(req["origin"])
    results = enriched_pois[:SEARCH_DISPLAY_LIMIT]

    if not results:
        return {
            "status": "ok",
            "mode": "search",
            "resolution_mode": "area_fallback",
            "confidence_band": "low",
            "summary": "结构化 POI 未返回稳定结果，当前只能回退到区域级线索。",
            "top_candidates": anchors[:2],
            "results": [],
            "evidence": bundles[:2],
        }

    top_candidates = [p["name"] for p in results[:3]]
    verified_count = sum(1 for p in results if p.get("web_score") is not None)
    summary = f"共找到 {len(results)} 个候选，优先看 {', '.join(top_candidates)}。已对前 {verified_count} 个候选做网页补充验证。"
    return {
        "status": "ok",
        "mode": "search",
        "resolution_mode": "list",
        "confidence_band": _confidence_band(results),
        "summary": summary,
        "top_candidates": top_candidates,
        "results": results,
        "evidence": bundles[:2],
    }


def decide_recommend(req, poi_result, search_runs, enriched_pois):
    bundles = _build_evidence_bundles(req, search_runs)
    anchors = expand_anchors(req["origin"])

    verified = [p for p in enriched_pois if p.get("web_score") is not None]
    strong_verified = [p for p in verified if p.get("web_score", 0) >= 45]

    if strong_verified:
        top = strong_verified[0]
        backups = [p["name"] for p in strong_verified[1:3]]
        if not backups:
            backups = [p["name"] for p in enriched_pois if p["name"] != top["name"]][:2]
        return {
            "status": "ok",
            "mode": "recommend",
            "resolution_mode": "store_level",
            "confidence": "high" if top.get("web_score", 0) >= 70 and top.get("total_score", 0) >= 75 else "medium",
            "top_pick": top["name"],
            "top_area": req["origin"],
            "backups": backups,
            "reason": "已先用结构化 POI 主源召回，再用 unified-search 对前排候选补充验证后拍板。",
            "poi_candidates": enriched_pois[:RECOMMEND_DISPLAY_LIMIT],
            "evidence": bundles[:2],
        }

    top_web = bundles[0] if bundles else None
    if not top_web or top_web["score"] < 45:
        return {
            "status": "ok",
            "mode": "recommend",
            "resolution_mode": "area_fallback",
            "confidence": "low",
            "top_pick": anchors[1] if len(anchors) > 1 else anchors[0],
            "backups": anchors[2:4],
            "reason": "当前店级网页证据不足，已降级为区域/锚点级推荐，避免幻觉式拍板店名。",
            "poi_candidates": enriched_pois[:RECOMMEND_DISPLAY_LIMIT],
            "evidence": bundles[:2],
        }

    return {
        "status": "ok",
        "mode": "recommend",
        "resolution_mode": "area_or_store",
        "confidence": "medium",
        "top_pick": anchors[1] if len(anchors) > 1 else anchors[0],
        "backups": [p["name"] for p in enriched_pois[:2]],
        "reason": "结构化主源已有候选，但网页证据仍不足以稳定拍板具体店名，因此维持区域级建议。",
        "poi_candidates": enriched_pois[:RECOMMEND_DISPLAY_LIMIT],
        "evidence": bundles[:2],
    }


def _attach_transit_details(poi_result, pois, limit=2):
    if not pois:
        return pois

    origin = poi_result.get("origin") or {}
    origin_lng = origin.get("lon")
    origin_lat = origin.get("lat")
    if origin_lng is None or origin_lat is None:
        return pois

    try:
        import amap_direction
    except Exception:
        return pois

    attached = 0
    for poi in pois:
        if attached >= limit:
            break

        accessibility = poi.get("accessibility") or {}
        if accessibility.get("mode") != "transit":
            continue

        dest_lng = poi.get("lon")
        dest_lat = poi.get("lat")
        if dest_lng is None or dest_lat is None:
            continue

        try:
            details = amap_direction.get_transit_details(origin_lng, origin_lat, dest_lng, dest_lat)
            if not details:
                continue
            poi["transit_details"] = details
            poi["transit_detail_lines"] = amap_direction.format_transit_detail_lines(details)
            attached += 1
        except Exception:
            continue

    return pois


def _accessibility_label(poi):
    accessibility = poi.get("accessibility") or {}
    duration_min = accessibility.get("duration_min")
    mode = accessibility.get("mode", "")
    if duration_min is None:
        return ""
    if mode == "walking":
        if duration_min <= 15:
            return "✅ 步行可达"
        elif duration_min <= 30:
            return "⚠️ 步行较远"
        else:
            return "❌ 步行不便"
    if duration_min <= 30:
        return "✅ 地铁可达"
    elif duration_min <= 45:
        return "⚠️ 勉强可达"
    else:
        return "❌ 公交不便"


def _render_poi_line(poi):
    parts = [
        poi["name"],
        f"score={poi.get('total_score', poi.get('score'))}",
        f"distance={poi.get('distance_m', '?')}m",
    ]
    accessibility = poi.get("accessibility") or {}
    if accessibility.get("display"):
        parts.append(f"access={accessibility['display']}")
    label = _accessibility_label(poi)
    if label:
        parts.append(label)
    if poi.get("evidence_level"):
        parts.append(f"evidence={poi['evidence_level']}")
    return "- " + " | ".join(parts)


def render_markdown(req, result, poi_result):
    lines = []
    lines.append("# Local POI Planner")
    lines.append("")
    lines.append(f"- 模式：{req['mode']}")
    lines.append(f"- 起点：{req['origin']}")
    lines.append(f"- 半径：{req.get('radius_m', 3000)}m")
    lines.append(f"- 类别：{req['category']}")
    lines.append(f"- 偏好：{', '.join(req['preferences']) or '未指定'}")
    lines.append(f"- 约束：{', '.join(req['constraints']) or '未指定'}")
    lines.append(f"- 回避：{', '.join(req['avoid']) or '未指定'}")
    lines.append(f"- provider: {poi_result.get('provider', 'unknown')}")
    lines.append(f"- origin resolved: {((poi_result.get('origin') or {}).get('display_name')) or '未解析'}")
    if result.get("mode") == "search":
        lines.append(f"- 置信带：{result['confidence_band']}")
        lines.append("")
        lines.append("## 概览")
        lines.append(f"- {result['summary']}")
        lines.append("")
        lines.append("## 优先看")
        for name in result.get("top_candidates", []):
            lines.append(f"- {name}")
        lines.append("")
        lines.append("## 候选列表")
        for poi in result.get("results", []):
            lines.append(_render_poi_line(poi))
            detail_lines = poi.get("transit_detail_lines") or []
            if detail_lines:
                lines.append("  - transit detail:")
                for item in detail_lines:
                    lines.append(f"    - {item}")
    else:
        lines.append(f"- 置信度：{result['confidence']}")
        lines.append("")
        lines.append("## 首选")
        lines.append(f"- 推荐：**{result['top_pick']}**")
        lines.append(f"- 理由：{result['reason']}")
        lines.append("")
        lines.append("## 结构化候选")
        for poi in result.get("poi_candidates", []):
            lines.append(_render_poi_line(poi))
            detail_lines = poi.get("transit_detail_lines") or []
            if detail_lines:
                lines.append("  - transit detail:")
                for item in detail_lines:
                    lines.append(f"    - {item}")
        lines.append("")
        lines.append("## 备选")
        if result.get("backups"):
            for x in result["backups"]:
                lines.append(f"- {x}")
        else:
            lines.append("- 暂无明确备选")
        lines.append("")
        lines.append("## 风险点")
        if result.get("resolution_mode") == "area_fallback":
            lines.append("- 当前是区域级/锚点级结论，不是稳定的店名级拍板")
            lines.append("- 如果要最终拍板，建议到场后二次筛店")
        else:
            lines.append("- 当前店级结果仍受网页索引质量与 POI 标注质量影响")
    lines.append("")
    lines.append("## 网页证据摘要")
    for ev in result.get("evidence", []):
        lines.append(f"### Query: {ev['query']}")
        lines.append(f"- score: {ev['score']}")
        for line in ev["lines"][:5]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", help="Natural language request")
    ap.add_argument("--origin")
    ap.add_argument("--category")
    ap.add_argument("--mode", choices=["search", "recommend"])
    ap.add_argument("--preferences")
    ap.add_argument("--constraints")
    ap.add_argument("--avoid")
    ap.add_argument("--format", choices=["json", "markdown"], default="json")
    ap.add_argument("--corelocation", action="store_true", help="Force CoreLocationCLI for current position")
    args = ap.parse_args()

    # --corelocation: resolve current position via CoreLocationCLI
    if args.corelocation:
        try:
            from macos_location import get_macos_location
            loc = get_macos_location(timeout=10)
            if loc:
                args.origin = f"{loc['lat']},{loc['lon']}"
                print(f"📍 CoreLocation: {loc['lat']:.5f}, {loc['lon']:.5f}", flush=True)
            else:
                print("⚠️ CoreLocation returned no coordinates, falling back", flush=True)
        except Exception as e:
            print(f"⚠️ CoreLocation failed ({e}), falling back", flush=True)

    t0 = time.time()
    print("⏳ 解析请求...", flush=True)

    req = parse_request(args)
    provider_limit = SEARCH_PROVIDER_LIMIT if req["mode"] == "search" else RECOMMEND_PROVIDER_LIMIT
    verify_limit = SEARCH_WEB_VERIFY_LIMIT if req["mode"] == "search" else RECOMMEND_WEB_VERIFY_LIMIT
    transit_attach_limit = 4 if req["mode"] == "search" else 2

    print(f"⏳ POI 搜索（{req['origin']}，半径 {req.get('radius_m', 3000)}m）...", flush=True)
    poi_result = search_pois(req, req["origin"], radius_m=req.get("radius_m", 3000), limit=provider_limit, ip_location=req.get("ip_location"))
    poi_candidates = poi_result.get("results", [])
    print(f"   ✅ POI 搜索：{len(poi_candidates)} 条候选（{time.time()-t0:.0f}s）", flush=True)
    print(f"⏳ Web enrichment（最多 {verify_limit} 条 POI，每条 30-90s）...", flush=True)
    enriched_pois = enrich_poi_with_web(req, poi_candidates, verify_limit=verify_limit)
    queries = build_queries(req, expand_anchors(req["origin"]), enriched_pois, mode=req["mode"])
    print(f"   ✅ 查询构建：{len(queries)} 条（{time.time()-t0:.0f}s）", flush=True)
    print(f"⏳ Unified-search（串行，每条 30-90s，共 {len(queries)} 条，请耐心等待 {len(queries)*45}-{len(queries)*90}s）...", flush=True)
    runs = [run_unified_search(q) for q in queries]

    print(f"   ✅ Unified-search 完成（{time.time()-t0:.0f}s）", flush=True)
    # Quality gate: trigger specialty fallback when evidence is weak
    pre_bundles = _build_evidence_bundles(req, runs)
    quality = _assess_bundle_quality(pre_bundles, req)
    if quality["need_fallback"]:
        print(f"   ⚠️ Evidence {quality['quality']} ({'; '.join(quality['reasons'])}), specialty fallback...", flush=True)
        fb = _specialty_fallback_run(req)
        if fb:
            runs.insert(0, fb)
    print("⏳ 决策 + 交通详情...", flush=True)
    if req["mode"] == "search":
        result = decide_search(req, poi_result, runs, enriched_pois)
        result["results"] = _attach_transit_details(
            poi_result,
            result.get("results", []),
            limit=transit_attach_limit,
        )
    else:
        result = decide_recommend(req, poi_result, runs, enriched_pois)
        result["poi_candidates"] = _attach_transit_details(
            poi_result,
            result.get("poi_candidates", []),
            limit=transit_attach_limit,
        )

    payload = {
        "request": req,
        "poi_provider": poi_result,
        "queries": queries,
        "result": result,
    }
    print(f"   ✅ 完成（总耗时 {time.time()-t0:.0f}s）", flush=True)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(req, result, poi_result))


if __name__ == "__main__":
    main()
