# -*- coding: utf-8 -*-
"""全球酒店搜索与推荐 - 场景识别+搜索+推荐+退改解读"""
import argparse, json, re, urllib.request, urllib.error, concurrent.futures
from datetime import datetime, timedelta

# ===== 代理配置 =====
PROXY_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

# ===== 搜索配置 =====
SEARCH_SIZE = 20
PER_TIER = 4

# ===== 74标签库 =====
TAG_CATEGORIES = {
    "酒店类型": ["商务酒店", "亲子酒店", "度假酒店", "性价比酒店", "机场酒店",
                 "运动友好酒店", "品质酒店", "华人友好酒店", "无障碍友好酒店"],
    "核心设施": ["免费WiFi", "免费停车场", "健身房", "户外泳池", "室内恒温泳池",
                 "洗衣服务", "公共温泉", "靠近海滩", "私人海滩"],
    "景观与房型": ["提供大床房", "提供双床房", "提供家庭房", "提供别墅房型",
                   "提供电竞主题房", "提供联通房", "提供三人间", "提供四人间",
                   "智能客房", "部分客房带有海景", "部分客房带有山景",
                   "部分客房带有城景", "部分客房带有花园景", "部分客房无窗",
                   "提供特色床型", "提供可吸烟房", "客房备有吹风机",
                   "备有热水壶", "备有拖鞋", "提供无障碍客房"],
    "服务与餐饮": ["24小时前台", "中式早餐", "客房点餐", "私人管家", "快速办理入住/退房"],
    "亲子家庭": ["儿童乐园", "儿童泳池", "儿童玩乐设施", "可提供婴儿床或围栏"],
    "特色卖点": ["SPA服务", "商务中心", "提供会议设施", "宴会厅", "乐园酒店",
                 "赌场酒店", "临近商场", "宠物友好", "酒店主题特色",
                 "无障碍通道", "无障碍停车位"],
    "交通与支付": ["机场接送班车", "自行车租赁", "支持支付宝/微信", "支持银联卡"],
    "服务细节": ["中文服务", "中文标识"],
}

# ===== 场景配置 =====
SCENE_CONFIG = {
    "亲子": {
        "icon": "👨‍👩‍👧",
        "required": ["亲子酒店"],
        "preferred_sea": ["儿童乐园", "儿童泳池", "提供家庭房", "靠近海滩", "可提供婴儿床或围栏"],
        "preferred_inland": ["儿童乐园", "室内恒温泳池", "中式早餐", "提供家庭房", "可提供婴儿床或围栏"],
        "excluded": ["仅限成人入住"],
        "star": [3.5, 5.0],
        "default_nights": 2,
    },
    "商务": {
        "icon": "💼",
        "required": ["商务酒店"],
        "preferred_tier1": ["免费WiFi", "24小时前台", "健身房", "提供会议设施"],
        "preferred_tier23": ["免费WiFi", "免费停车场", "中式早餐", "24小时前台"],
        "excluded": [],
        "star": [3.0, 5.0],
        "default_nights": 1,
    },
    "度假": {
        "icon": "🌴",
        "required": [],
        "preferred_sea": ["度假酒店", "户外泳池", "SPA服务", "靠近海滩", "私人海滩"],
        "preferred_inland": ["度假酒店", "户外泳池", "SPA服务", "公共温泉"],
        "excluded": [],
        "star": [3.5, 5.0],
        "default_nights": 2,
    },
    "背包": {
        "icon": "🎒",
        "required": [],
        "preferred": ["性价比酒店", "免费WiFi", "免费停车场", "中式早餐"],
        "excluded": [],
        "star": [0.0, 3.5],
        "default_nights": 1,
        "max_price": 300,
    },
    "通用": {
        "icon": "🏨",
        "required": [],
        "preferred": [],
        "excluded": [],
        "default_nights": 1,
    },
}

SEA_CITIES = {"三亚", "海口", "厦门", "青岛", "大连", "威海", "珠海", "北海",
              "舟山", "泉州", "漳州", "日照", "连云港", "烟台", "湛江"}
TIER1_CITIES = {"上海", "北京", "深圳", "广州"}

SCENE_KEYWORDS = {
    "亲子": ["亲子", "家庭", "小孩", "孩子", "儿童", "带娃", "遛娃", "一家三口", "全家", "婴儿", "宝宝", "小朋友"],
    "商务": ["出差", "商务", "办公", "会议", "商旅", "考察", "谈判", "客户拜访", "项目", "培训"],
    "度假": ["度假", "情侣", "蜜月", "浪漫", "海边", "海岛", "休闲", "温泉", "周末放松", "约会", "结婚", "纪念日"],
    "背包": ["背包", "穷游", "学生", "青旅", "便宜", "经济", "预算有限", "省钱", "性价比"],
}
SCENE_ICONS = {"商务": "💼", "亲子": "👨‍👩‍👧", "度假": "🌴", "背包": "🎒", "通用": "🏨"}

PLACE_TYPE_RULES = {
    "机场": ["机场", "T1", "T2", "T3", "航站楼", "国际机场"],
    "火车站": ["火车站", "高铁站", "北站", "南站", "东站", "西站", "动车站"],
    "景点": ["景区", "景点", "公园", "古镇", "海边", "海滩", "迪士尼", "环球影城",
             "外滩", "西湖", "长城", "故宫", "鼓浪屿", "亚特兰蒂斯", "长隆"],
    "区/县": ["CBD", "市中心", "陆家嘴", "春熙路", "王府井", "南京路", "天河", "福田", "朝阳区", "浦东"],
}

TIER_LABELS = {
    "budget": {"icon": "💰", "name": "性价比之选"},
    "mid": {"icon": "🏨", "name": "品质推荐"},
    "high": {"icon": "✨", "name": "豪华体验"},
}

# ===== 代理调用 =====

def call_proxy(api_type, params, timeout=30):
    """调用RG代理，返回解析后的数据"""
    body = json.dumps({"type": api_type, "params": params}, ensure_ascii=False, separators=(",", ":"))
    req = urllib.request.Request(
        PROXY_URL, data=body.encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            result = json.loads(r.read().decode("utf-8"))
        if result.get("code") != 0:
            return {"error": result.get("error", "proxy error")}
        raw = result.get("data", "")
        ct = result.get("content_type", "")
        return _parse_mcp(raw, ct)
    except Exception as e:
        return {"error": str(e)}


def _parse_mcp(raw, content_type):
    """解析MCP JSON-RPC响应"""
    if not raw:
        return {"error": "empty response"}
    try:
        if "text/event-stream" in (content_type or ""):
            for line in raw.split("\n"):
                if line.startswith("data:"):
                    return _extract_mcp_result(json.loads(line[5:].strip()))
        return _extract_mcp_result(json.loads(raw))
    except Exception:
        return {"error": "parse fail", "raw": raw[:200]}


def _extract_mcp_result(result):
    if "error" in result:
        return {"error": str(result["error"].get("message", result["error"]))[:200]}
    res = result.get("result", result)
    if isinstance(res, dict) and "content" in res:
        contents = res["content"]
        if isinstance(contents, list) and len(contents) > 0:
            f = contents[0]
            if isinstance(f, dict) and f.get("type") == "text":
                t = f.get("text", "")
                try:
                    return json.loads(t)
                except Exception:
                    return {"raw_text": t}
    return res


# ===== 意图解析 =====

def detect_scenes(query):
    if not query:
        return ["通用"]
    scenes = []
    for scene, keywords in SCENE_KEYWORDS.items():
        for kw in keywords:
            if kw in query:
                scenes.append(scene)
                break
    return scenes if scenes else ["通用"]


def infer_place_type(query, place):
    combined = (query or "") + place
    for ptype, keywords in PLACE_TYPE_RULES.items():
        for kw in keywords:
            if kw in combined:
                return ptype
    return "城市"


def infer_occupancy(query, scene):
    adult_count = 2
    child_count = 0
    child_ages = []
    room_count = 1
    if not query:
        return {"adultCount": adult_count, "childCount": child_count,
                "childAgeDetails": child_ages, "roomCount": room_count}
    child_patterns = [
        (r"带(?:娃|孩子|小孩|小朋友|宝宝|婴儿)", 1),
        (r"一家三口", 1), (r"一家四口", 2),
        (r"两个(?:娃|孩子|小孩)", 2), (r"三个(?:娃|孩子|小孩)", 3),
    ]
    for pattern, count in child_patterns:
        if re.search(pattern, query):
            child_count = count
            break
    if re.search(r"团建|团队|公司", query):
        num_match = re.search(r"(\d+)(?:人|个)", query)
        if num_match:
            total = int(num_match.group(1))
            room_count = max(1, (total + 1) // 2)
    return {"adultCount": adult_count, "childCount": child_count,
            "childAgeDetails": child_ages, "roomCount": room_count}


def infer_default_nights(scenes, query):
    if query:
        nights_match = re.search(r"住(\d+)(?:晚|天)", query)
        if nights_match:
            return int(nights_match.group(1))
    for scene in scenes:
        config = SCENE_CONFIG.get(scene, {})
        if "default_nights" in config:
            return config["default_nights"]
    return 1


def infer_max_price(query, scenes, place):
    if not query:
        return None
    price_match = re.search(r"(?:¥|块钱?|元)?(\d+)(?:以内|以下|之内|左右|块)", query)
    if price_match:
        return int(price_match.group(1))
    cheap_words = ["便宜", "经济", "省钱", "预算有限", "穷游"]
    if any(w in query for w in cheap_words):
        if place in TIER1_CITIES:
            return 400
        elif "度假" in scenes:
            return 500
        else:
            return 300
    return None


def infer_star_rating(query, scenes, place):
    if query:
        grade_map = {"经济型": [0.0, 2.0], "经济": [0.0, 2.0],
                     "舒适型": [2.5, 3.5], "舒适": [2.5, 3.5],
                     "高档型": [3.5, 4.5], "高档": [3.5, 4.5],
                     "豪华型": [4.5, 5.0], "豪华": [4.5, 5.0]}
        for g, r in grade_map.items():
            if g in query:
                return r
        # 口语化星级关键词
        if "五星" in query or "5星" in query:
            return [4.5, 5.0]
        if "四星" in query or "4星" in query:
            return [3.5, 4.5]
        if "三星" in query or "3星" in query:
            return [2.5, 3.5]
        if any(w in query for w in ["便宜", "经济", "省钱"]):
            return [0.0, 2.5]
    primary = scenes[0] if scenes else "通用"
    config = SCENE_CONFIG.get(primary, {})
    if "star" in config:
        return list(config["star"])
    return None


# ===== 搜索参数构建 =====

def build_search_args(destination, check_in, stay_nights, scenes, query="",
                      place_type="城市", star_rating=None, max_price=None,
                      max_distance=None, preferred_brand=None, required_tag=None,
                      preferred_tag=None, excluded_tag=None, min_room_size=None,
                      adult_count=2, child_count=0, child_ages=None,
                      room_count=1, country_code=None, size=SEARCH_SIZE,
                      use_required_tags=True, use_distance=True, use_star=True):
    primary_scene = scenes[0] if scenes else "通用"
    config = SCENE_CONFIG.get(primary_scene, SCENE_CONFIG["通用"])

    check_in_param = {"checkInDate": check_in, "stayNights": stay_nights}
    if adult_count > 0:
        check_in_param["adultCount"] = adult_count

    args = {
        "place": destination,
        "placeType": place_type,
        "originQuery": query or f"{destination}酒店",
        "size": size,
        "checkInParam": check_in_param,
    }
    if country_code:
        args["countryCode"] = country_code

    filter_options = {}
    if use_star and star_rating:
        filter_options["starRatings"] = star_rating
    if use_distance and max_distance and max_distance > 0:
        filter_options["distanceInMeter"] = max_distance
    if filter_options:
        args["filterOptions"] = filter_options

    hotel_tags = {}
    is_sea = destination in SEA_CITIES or any(
        kw in (query + destination) for kw in ["海边", "海滩", "海景", "海岛"])
    is_tier1 = destination in TIER1_CITIES

    all_required = []
    if use_required_tags and config.get("required"):
        all_required = list(config["required"])
    if required_tag:
        user_req = [t.strip() for t in required_tag.replace("，", ",").split(",") if t.strip()]
        all_required.extend(t for t in user_req if t not in all_required)
    if all_required:
        hotel_tags["requiredTags"] = all_required

    all_preferred = []
    if primary_scene == "亲子":
        all_preferred = list(config.get("preferred_sea" if is_sea else "preferred_inland", []))
    elif primary_scene == "商务":
        all_preferred = list(config.get("preferred_tier1" if is_tier1 else "preferred_tier23", []))
    elif primary_scene == "度假":
        all_preferred = list(config.get("preferred_sea" if is_sea else "preferred_inland", []))
    elif primary_scene == "背包":
        all_preferred = list(config.get("preferred", []))
    if preferred_tag:
        user_pref = [t.strip() for t in preferred_tag.replace("，", ",").split(",") if t.strip()]
        all_preferred.extend(t for t in user_pref if t not in all_preferred)
    if all_preferred:
        hotel_tags["preferredTags"] = all_preferred[:6]

    all_excluded = list(config.get("excluded", []))
    if excluded_tag:
        user_exc = [t.strip() for t in excluded_tag.replace("，", ",").split(",") if t.strip()]
        all_excluded.extend(t for t in user_exc if t not in all_excluded)
    if all_excluded:
        hotel_tags["excludedTags"] = all_excluded

    effective_max_price = max_price
    if not effective_max_price and "max_price" in config:
        effective_max_price = config["max_price"]
    if effective_max_price:
        hotel_tags["maxPricePerNight"] = float(effective_max_price)

    if preferred_brand:
        hotel_tags["preferredBrands"] = [t.strip() for t in preferred_brand.replace("，", ",").split(",") if t.strip()]
    if min_room_size and min_room_size > 0:
        hotel_tags["minRoomSize"] = min_room_size
    if hotel_tags:
        args["hotelTags"] = hotel_tags

    return args


# ===== 搜索（含降级） =====

def _do_search(search_args):
    result = call_proxy("hotel_search", search_args, 25)
    if isinstance(result, dict) and "error" in result:
        return []
    return _extract_hotels(result)


def _extract_hotels(data):
    if isinstance(data, dict):
        for key in ["hotelInformationList", "hotels", "data", "results"]:
            if key in data:
                val = data[key]
                return val if isinstance(val, list) else []
    if isinstance(data, list):
        return data
    return []


def _search_fallback(original_args, destination, scenes, star_rating, max_distance):
    # 降级1：去required标签
    args2 = json.loads(json.dumps(original_args))
    if "hotelTags" in args2 and "requiredTags" in args2.get("hotelTags", {}):
        del args2["hotelTags"]["requiredTags"]
        if not args2["hotelTags"]:
            del args2["hotelTags"]
    hotels = _do_search(args2)
    if hotels:
        return hotels
    # 降级2：去距离
    args3 = json.loads(json.dumps(args2))
    if "filterOptions" in args3:
        args3["filterOptions"].pop("distanceInMeter", None)
        if not args3["filterOptions"]:
            del args3["filterOptions"]
    hotels = _do_search(args3)
    if hotels:
        return hotels
    # 降级3：最简搜索
    args4 = {
        "place": destination,
        "placeType": "城市",
        "originQuery": original_args.get("originQuery", f"{destination}酒店"),
        "size": original_args.get("size", SEARCH_SIZE),
        "checkInParam": original_args.get("checkInParam", {}),
    }
    return _do_search(args4)


# ===== 价格分档选择 =====

def _get_price(hotel):
    price_info = hotel.get("price") or {}
    if isinstance(price_info, dict):
        p = price_info.get("lowestPrice")
        return float(p) if p else 99999
    return float(price_info) if price_info else 99999


def select_by_price_tier(hotels, per_tier=PER_TIER):
    if not hotels:
        return []
    sorted_hotels = sorted(hotels, key=_get_price)
    with_price = [h for h in sorted_hotels if _get_price(h) < 99999]
    without_price = [h for h in sorted_hotels if _get_price(h) >= 99999]

    if not with_price:
        for h in without_price:
            h["_price_tier"] = "mid"
        return without_price[:per_tier * 3]

    total = len(with_price)
    third = max(1, total // 3)
    budget = with_price[:third]
    mid = with_price[third:third * 2]
    high = with_price[third * 2:]

    result = []
    for h in budget[:per_tier]:
        h["_price_tier"] = "budget"
        result.append(h)
    for h in mid[:per_tier]:
        h["_price_tier"] = "mid"
        result.append(h)
    for h in high[:per_tier]:
        h["_price_tier"] = "high"
        result.append(h)

    remaining = per_tier - len([h for h in result if h.get("_price_tier") == "mid"])
    for h in without_price[:remaining]:
        h["_price_tier"] = "mid"
        result.append(h)
    return result


# ===== 并发详情获取 =====

def _fetch_one_detail(hotel_id, check_in, check_out, occupancy):
    try:
        detail = call_proxy("hotel_detail", {
            "hotelId": int(hotel_id),
            "dateParam": {"checkInDate": check_in, "checkOutDate": check_out},
            "occupancyParam": occupancy,
        }, 20)
        if isinstance(detail, dict) and "error" not in detail:
            return (hotel_id, detail)
    except Exception:
        pass
    return (hotel_id, None)


def fetch_details_concurrent(hotels, check_in, check_out, occupancy, max_workers=6):
    details = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for hotel in hotels:
            hotel_id = str(hotel.get("hotelId", ""))
            if not hotel_id:
                continue
            f = executor.submit(_fetch_one_detail, hotel_id, check_in, check_out, occupancy)
            futures[f] = hotel_id
        for f in concurrent.futures.as_completed(futures):
            r = f.result()
            if r and r[1]:
                details[r[0]] = r[1]
    return details


# ===== 退改政策解读 =====

def interpret_cancellation(policies, check_in_date=None):
    if not policies:
        return "暂无退改信息"
    now = datetime.now()
    sorted_p = sorted(policies, key=lambda p: p.get("fromDate", ""))
    checkin_dt = None
    if check_in_date:
        try:
            checkin_dt = datetime.fromisoformat(check_in_date)
        except Exception:
            pass
    parts = []
    for p in sorted_p:
        from_date = p.get("fromDate", "")
        amount = p.get("amount") or 0
        percent = p.get("percent") or 0
        desc = p.get("description", "")
        date_str = ""
        days_before = ""
        is_past = False
        if from_date:
            try:
                dt = datetime.fromisoformat(from_date)
                date_str = dt.strftime("%m月%d日")
                if dt.date() < now.date():
                    is_past = True
                if checkin_dt:
                    diff = (checkin_dt.date() - dt.date()).days
                    if diff > 0:
                        days_before = f"入住前{diff}天"
            except Exception:
                date_str = from_date[:10]
        if amount == 0 and percent == 0:
            if is_past:
                parts.append("不可免费取消")
            elif days_before:
                parts.append(f"{days_before}前免费取消")
            elif date_str:
                parts.append(f"{date_str}前免费取消")
            else:
                parts.append("免费取消")
        elif amount > 0:
            if is_past:
                parts.append(f"不可免费取消，取消扣¥{int(amount)}")
            elif days_before:
                parts.append(f"{days_before}后取消扣¥{int(amount)}")
            elif date_str:
                parts.append(f"{date_str}后取消扣¥{int(amount)}")
            else:
                parts.append(f"取消扣¥{int(amount)}")
        elif percent > 0:
            if is_past:
                parts.append(f"不可免费取消，取消扣{int(percent)}%房费")
            elif days_before:
                parts.append(f"{days_before}后取消扣{int(percent)}%房费")
            else:
                parts.append(f"取消扣{int(percent)}%房费")
        elif desc:
            parts.append(desc)
    return "；".join(parts) if parts else "暂无退改信息"


# ===== 推荐理由生成 =====

def generate_reason(hotel, scene, config, all_hotels, is_sea, tier="mid"):
    tags = hotel.get("tags") or []
    amenities = hotel.get("hotelAmenities") or []
    all_features = [str(t) for t in tags] + [str(a) for a in amenities]
    star = hotel.get("starRating", 0) or 0
    price_info = hotel.get("price", {})
    price = price_info.get("lowestPrice", 0) if isinstance(price_info, dict) else 0
    dist = hotel.get("distanceInMeters")

    reasons = []
    if tier == "budget":
        reasons.append("性价比之选" if price and price > 0 else "经济实惠")
    elif tier == "high":
        if star >= 5:
            reasons.append(f"{int(star)}星豪华")
        elif star >= 4:
            reasons.append(f"{int(star)}星高端")

    if scene == "商务":
        if any(f in all_features for f in ["免费WiFi", "健身房"]):
            reasons.append("设施齐全适合办公")
        if any(f in all_features for f in ["提供会议设施", "商务中心"]):
            reasons.append("有会议室/商务中心")
        if star >= 4 and tier != "high":
            reasons.append(f"{int(star)}星品质")
        if dist and dist < 2000:
            reasons.append("近目标地点")
    elif scene == "亲子":
        if "儿童乐园" in all_features:
            reasons.append("有儿童乐园")
        if "儿童泳池" in all_features:
            reasons.append("有儿童泳池")
        if "提供家庭房" in all_features:
            reasons.append("有家庭房")
        if is_sea and any(f in all_features for f in ["靠近海滩", "私人海滩"]):
            reasons.append("近海滩")
        if not reasons and star >= 4:
            reasons.append(f"{int(star)}星亲子友好")
    elif scene == "度假":
        if is_sea and any(f in all_features for f in ["靠近海滩", "私人海滩", "部分客房带有海景"]):
            reasons.append("海景/近海滩")
        if "户外泳池" in all_features:
            reasons.append("有户外泳池")
        if "SPA服务" in all_features:
            reasons.append("有SPA")
        if "公共温泉" in all_features:
            reasons.append("有温泉")
        if not reasons and star >= 4:
            reasons.append(f"{int(star)}星度假体验")
    elif scene == "背包":
        if tier != "budget" and price and price > 0:
            reasons.append("性价比之选")
        if any(f in all_features for f in ["免费停车场", "免费WiFi"]):
            reasons.append("基础设施齐全")
    else:
        if star >= 5 and tier != "high":
            reasons.append(f"{int(star)}星豪华")
        elif star >= 4 and tier != "high":
            reasons.append(f"{int(star)}星品质")
        if dist and dist < 1000:
            reasons.append("位置便利")

    return "，".join(reasons[:3]) if reasons else "综合推荐"


# ===== 输出格式化 =====

def _pick_tags(hotel, limit=4):
    tags = hotel.get("tags") or []
    result = list(tags[:limit])
    if len(result) < limit:
        amenities = hotel.get("hotelAmenities") or []
        for a in amenities:
            if len(result) >= limit:
                break
            a_str = str(a)
            if a_str not in result:
                result.append(a_str)
    return result


def _build_filters_desc(star_rating, max_price, max_distance, preferred_brand, required_tag, min_room_size):
    parts = []
    if star_rating:
        if isinstance(star_rating, list) and len(star_rating) == 2:
            parts.append(f"{star_rating[0]}-{star_rating[1]}星")
    if max_price:
        parts.append(f"¥{max_price}内")
    if max_distance:
        parts.append(f"{max_distance/1000:.0f}km内" if max_distance >= 1000 else f"{max_distance}m内")
    if preferred_brand:
        parts.append(preferred_brand)
    if required_tag:
        parts.append(required_tag)
    if min_room_size:
        parts.append(f"{min_room_size}㎡+")
    return " | ".join(parts) if parts else ""


def format_output_tiered(hotels, details_map, scenes, destination, check_in, check_out,
                          filters_desc, occupancy, fallback_level=0, user_has_price_pref=False):
    primary_scene = scenes[0] if scenes else "通用"
    config = SCENE_CONFIG.get(primary_scene, SCENE_CONFIG["通用"])
    icon = SCENE_ICONS.get(primary_scene, "🏨")
    is_sea = destination in SEA_CITIES or any(
        kw in destination for kw in ["海边", "海滩", "海景", "海岛"])

    # 计算晚数
    try:
        nights = (datetime.fromisoformat(check_out) - datetime.fromisoformat(check_in)).days
    except Exception:
        nights = 1

    # 价格区间
    prices = [_get_price(h) for h in hotels if _get_price(h) < 99999]
    price_range = ""
    if prices:
        price_range = f" · ¥{int(min(prices))}-{int(max(prices))}/晚"

    lines = []
    header = f"{icon} {primary_scene}推荐 · {destination} · {check_in}({nights}晚){price_range}"
    if filters_desc:
        header += f" · 筛选：{filters_desc}"
    lines.append(header)

    # 人数信息行
    adult = occupancy.get("adultCount", 2)
    child = occupancy.get("childCount", 0)
    rooms = occupancy.get("roomCount", 1)
    people_parts = [f"{adult}成人"]
    if child and child > 0:
        people_parts.append(f"{child}儿童")
    lines.append(f"👥 {''.join(people_parts)} · {rooms}间")
    lines.append("")

    # 按档位分组
    current_tier = None
    for i, hotel in enumerate(hotels, 1):
        tier = hotel.get("_price_tier", "mid")
        if tier != current_tier:
            current_tier = tier
            tier_info = TIER_LABELS.get(tier, TIER_LABELS["mid"])
            if not user_has_price_pref:
                tier_prices = [_get_price(h) for h in hotels if h.get("_price_tier") == tier and _get_price(h) < 99999]
                tier_price_str = f" ¥{int(min(tier_prices))}-{int(max(tier_prices))}/晚" if tier_prices else ""
                lines.append(f"{tier_info['icon']} {tier_info['name']}{tier_price_str}")
                lines.append("")

        name = hotel.get("name", "未知酒店")
        star = hotel.get("starRating", 0)
        star_s = f"⭐{star}" if star else ""
        price_info = hotel.get("price", {})
        price = price_info.get("lowestPrice", 0) if isinstance(price_info, dict) else price_info
        price_s = f"💰¥{int(price)}/晚" if price else ""

        addr = hotel.get("address", "")
        dist = hotel.get("distanceInMeters")
        dist_s = ""
        if dist is not None:
            try:
                d = int(dist)
                dist_s = f"📏{d}m" if d < 1000 else f"📏{d/1000:.1f}km"
            except (ValueError, TypeError):
                pass
        addr_line = " | ".join(filter(None, [addr[:30], dist_s]))

        tag_list = _pick_tags(hotel, limit=4)
        tag_s = " ".join(str(t) for t in tag_list) if tag_list else ""

        reason = generate_reason(hotel, primary_scene, config, hotels, is_sea, tier)

        # 退改
        cancel_s = ""
        hid = str(hotel.get("hotelId", ""))
        detail = details_map.get(hid, {})
        if detail:
            plans = detail.get("roomRatePlans", [])
            if plans:
                policies = plans[0].get("cancellationPolicies", [])
                if policies:
                    cancel_s = interpret_cancellation(policies, check_in)

        url = hotel.get("detailUrl") or hotel.get("bookingUrl", "")

        lines.append(f"{i}. {name} {star_s} {price_s}".rstrip())

        img = hotel.get("imageUrl", "")
        if img:
            lines.append(f"   ![]({img})")

        if addr_line:
            lines.append(f"   📍 {addr_line}")

        desc = hotel.get("description", "")
        if desc:
            clean = re.sub(r'<[^>]+>', '', desc)
            clean = re.sub(r'^(酒店简介描述|酒店简介|简介描述)\s*', '', clean).strip()
            sentences = re.split(r'[。！？]', clean)
            summary_parts = []
            for s in sentences:
                s = s.strip()
                if s and len(s) >= 4:
                    summary_parts.append(s)
                    if len(summary_parts) >= 2:
                        break
            if summary_parts:
                summary = '。'.join(summary_parts) + '。'
                if len(summary) > 80:
                    summary = summary[:77] + '...'
                lines.append(f"   💬 {summary}")

        if tag_s:
            lines.append(f"   🏷️ {tag_s}")
        if reason:
            lines.append(f"   💡 {reason}")
        if cancel_s:
            lines.append(f"   🔄 退改：{cancel_s}")
        if url:
            lines.append(f"   🔗 {url}")
        lines.append("")

    lines.append("数据来源：RollingGo | 价格实时变动，以实际下单为准")
    if fallback_level > 0:
        fallback_desc = {
            1: "已放宽必选标签",
            2: "已放宽距离和标签限制",
            3: "已放宽所有筛选，展示城市热门酒店",
        }
        desc = fallback_desc.get(fallback_level, f"级别{fallback_level}")
        lines.append(f"⚠️ 降级搜索：{desc}")

    return "\n".join(lines)


# ===== 主函数 =====

def hotel_search_and_recommend(destination, scene="通用", check_in=None, check_out=None,
                                guests=1, query=None, star_rating=None, max_price=None,
                                max_distance=None, preferred_brand=None, required_tag=None,
                                preferred_tag=None, excluded_tag=None, min_room_size=None,
                                stay_nights=None, adult_count=None, child_count=None,
                                child_ages=None, room_count=None, country_code=None):
    """1次调用完成场景识别→参数补全→搜索→详情→退改解读→推荐理由"""
    if not destination:
        return "请提供目的地"

    # 1. 场景检测
    detected_scenes = detect_scenes(query or "")
    if query and scene in ("通用", ""):
        scenes = detected_scenes
    else:
        scenes = [scene] if scene and scene != "通用" else detected_scenes

    # 2. 参数智能补全
    today = datetime.now()
    if not check_in:
        check_in = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    nights = stay_nights or infer_default_nights(scenes, query or "")
    if not check_out:
        check_out_dt = datetime.fromisoformat(check_in) + timedelta(days=nights)
        check_out = check_out_dt.strftime("%Y-%m-%d")

    place_type = infer_place_type(query or "", destination)

    if adult_count or child_count is not None:
        occupancy = {"adultCount": adult_count or 2, "childCount": child_count or 0,
                     "roomCount": room_count or 1}
    else:
        occupancy = infer_occupancy(query or "", scenes[0])
        if guests and guests >= 2 and occupancy["adultCount"] < guests:
            occupancy["adultCount"] = guests

    if child_ages:
        try:
            occupancy["childAgeDetails"] = [int(a.strip()) for a in child_ages.replace("，", ",").split(",") if a.strip()]
        except ValueError:
            pass

    # 星级
    effective_star = None
    if star_rating:
        s = star_rating.strip()
        grade_map = {"经济型": [0.0, 2.0], "经济": [0.0, 2.0],
                     "舒适型": [2.5, 3.5], "舒适": [2.5, 3.5],
                     "高档型": [3.5, 4.5], "高档": [3.5, 4.5],
                     "豪华型": [4.5, 5.0], "豪华": [4.5, 5.0]}
        if s in grade_map:
            effective_star = grade_map[s]
        else:
            parts = s.replace("，", ",").split(",")
            try:
                effective_star = [float(parts[0]), float(parts[1])] if len(parts) > 1 else [float(parts[0]), 5.0]
            except ValueError:
                effective_star = infer_star_rating(query or "", scenes, destination)
    else:
        effective_star = infer_star_rating(query or "", scenes, destination)

    # 商务场景：一线城市星级下限3.5，其他城市3.0
    if not effective_star and "商务" in scenes:
        if destination in TIER1_CITIES:
            effective_star = [3.5, 5.0]
        else:
            effective_star = [3.0, 5.0]

    effective_max_price = max_price or infer_max_price(query or "", scenes, destination)

    # 放宽星级下限，覆盖全价位
    if effective_star and effective_star[0] > 0:
        effective_star = [0.0, effective_star[1]]

    user_has_price_pref = bool(max_price) or bool(effective_max_price)

    filters_desc = _build_filters_desc(
        effective_star, effective_max_price, max_distance,
        preferred_brand, required_tag, min_room_size)

    # 3. 搜索
    search_args = build_search_args(
        destination=destination, check_in=check_in, stay_nights=nights,
        scenes=scenes, query=query or "", place_type=place_type,
        star_rating=effective_star, max_price=effective_max_price,
        max_distance=max_distance, preferred_brand=preferred_brand,
        required_tag=required_tag, preferred_tag=preferred_tag,
        excluded_tag=excluded_tag, min_room_size=min_room_size,
        adult_count=occupancy["adultCount"],
        child_count=occupancy.get("childCount", 0),
        child_ages=occupancy.get("childAgeDetails"),
        room_count=occupancy.get("roomCount", 1),
        country_code=country_code,
        size=SEARCH_SIZE,
    )

    hotels = _do_search(search_args)
    fallback_level = 0

    if not hotels:
        hotels = _search_fallback(search_args, destination, scenes, effective_star, max_distance)
        fallback_level = 1 if hotels else 3

    if not hotels:
        return f"未找到{destination}的酒店，建议更换目的地或日期"

    # 4. 价格分档选择
    if not user_has_price_pref:
        selected = select_by_price_tier(hotels, PER_TIER)
    else:
        budget_limit = effective_max_price
        in_budget = [h for h in hotels if _get_price(h) <= budget_limit]
        if in_budget:
            selected = sorted(in_budget, key=_get_price)[:PER_TIER * 3]
        else:
            selected = sorted(hotels, key=_get_price)[:PER_TIER * 3]

    # 5. 并发获取详情
    detail_occupancy = {
        "adults": occupancy["adultCount"],
        "roomCount": occupancy.get("roomCount", 1),
    }
    if occupancy.get("childCount", 0) > 0:
        detail_occupancy["childCount"] = occupancy["childCount"]
        if occupancy.get("childAgeDetails"):
            detail_occupancy["childAgeDetails"] = occupancy["childAgeDetails"]

    details_map = fetch_details_concurrent(selected, check_in, check_out, detail_occupancy)

    # 6. 格式化输出
    formatted = format_output_tiered(
        selected, details_map, scenes, destination,
        check_in, check_out, filters_desc, occupancy,
        fallback_level, user_has_price_pref)

    return formatted


# ===== CLI入口 =====

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="全球酒店搜索与推荐")
    parser.add_argument("--destination", required=True, help="目的地")
    parser.add_argument("--scene", default="通用", help="场景：商务/亲子/度假/背包/通用")
    parser.add_argument("--check-in", default=None, help="入住日期 YYYY-MM-DD")
    parser.add_argument("--check-out", default=None, help="退房日期 YYYY-MM-DD")
    parser.add_argument("--guests", type=int, default=1, help="入住人数")
    parser.add_argument("--query", default=None, help="用户原始查询")
    parser.add_argument("--max-price", type=int, default=None, help="每晚价格上限")
    parser.add_argument("--star-rating", default=None, help="星级筛选")
    parser.add_argument("--preferred-brand", default=None, help="偏好品牌")
    parser.add_argument("--required-tag", default=None, help="必须标签")
    parser.add_argument("--preferred-tag", default=None, help="偏好标签")
    parser.add_argument("--excluded-tag", default=None, help="排除标签")
    parser.add_argument("--min-room-size", type=int, default=None, help="最小房间面积")
    parser.add_argument("--max-distance", type=int, default=None, help="距离上限(米)")
    parser.add_argument("--country-code", default=None, help="国家代码")
    parser.add_argument("--stay-nights", type=int, default=None, help="入住晚数")
    parser.add_argument("--adult-count", type=int, default=None, help="成人数量")
    parser.add_argument("--child-count", type=int, default=None, help="儿童数量")
    parser.add_argument("--child-ages", default=None, help="儿童年龄")
    parser.add_argument("--room-count", type=int, default=None, help="房间数")

    args = parser.parse_args()
    result = hotel_search_and_recommend(
        destination=args.destination, scene=args.scene,
        check_in=args.check_in, check_out=args.check_out,
        guests=args.guests, query=args.query,
        star_rating=args.star_rating, max_price=args.max_price,
        max_distance=args.max_distance, preferred_brand=args.preferred_brand,
        required_tag=args.required_tag, preferred_tag=args.preferred_tag,
        excluded_tag=args.excluded_tag, min_room_size=args.min_room_size,
        stay_nights=args.stay_nights, adult_count=args.adult_count,
        child_count=args.child_count, child_ages=args.child_ages,
        room_count=args.room_count, country_code=args.country_code,
    )
    print(result)
