#!/usr/bin/env python3
"""旅行智能助手 - 国内旅行一站式服务，飞猪+高德双引擎
10个工具：飞猪8个(行程规划/火车票/机票/酒店/景点/极速搜索/万豪搜索/万豪详情) + 高德2个(美食/市内交通含打车)
"""
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import re

# ============================================================
# 代理配置（环境变量，禁止硬编码）
# ============================================================
FLIGGY_PROXY = os.environ.get("FLIGGY_PROXY", "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com")
GAODE_PROXY = os.environ.get("GAODE_PROXY", "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
TIMEOUT = 30

# ============================================================
# 代理调用函数
# ============================================================

def _call_flyai(tool_name, arguments):
    """通过飞猪SCF代理调用飞猪API"""
    payload = json.dumps(
        {"type": tool_name, "params": arguments},
        ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers["X-Proxy-Token"] = PROXY_TOKEN
    req = urllib.request.Request(
        FLIGGY_PROXY + "/proxy",
        data=payload, headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"error": str(e)}


def _call_gaode(api_type, params):
    """通过高德SCF代理调用高德API"""
    payload = json.dumps(
        {"type": api_type, "params": params},
        ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers["X-Proxy-Token"] = PROXY_TOKEN
    req = urllib.request.Request(
        GAODE_PROXY,
        data=payload, headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 飞猪返回数据解析
# ============================================================

def _parse_flyai_text(result):
    """统一解析飞猪代理返回数据，返回可读文本"""
    if not result:
        return "无返回数据"
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if "error" in result:
            return f"请求失败: {result['error']}"
        if "data" in result:
            data = result["data"]
            if isinstance(data, str):
                return data
            if isinstance(data, dict):
                if "itemList" in data:
                    return json.dumps(data["itemList"], ensure_ascii=False, indent=2)
                return json.dumps(data, ensure_ascii=False, indent=2)
            if isinstance(data, list):
                return json.dumps(data, ensure_ascii=False, indent=2)
            return str(data)
        if "text" in result:
            return result["text"]
        return json.dumps(result, ensure_ascii=False, indent=2)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 高德辅助函数
# ============================================================

_CITIES = [
    "北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉",
    "南京", "西安", "长沙", "天津", "苏州", "厦门", "青岛", "大连",
    "昆明", "贵阳", "南宁", "福州", "郑州", "哈尔滨", "沈阳", "长春",
    "济南", "太原", "合肥", "南昌", "石家庄", "兰州", "呼和浩特",
    "乌鲁木齐", "银川", "西宁", "拉萨", "海口", "三亚", "宁波",
    "无锡", "佛山", "东莞", "珠海", "中山", "惠州", "温州", "常州",
]


def _geocode(location_name, city=""):
    """用高德地理编码把地名转成经纬度，返回 (lng, lat) 或 None"""
    params = {"address": location_name}
    if city:
        params["city"] = city
    result = _call_gaode("geocode", params)
    if isinstance(result, dict) and "error" in result:
        # 重试：加城市前缀
        if city and city not in location_name:
            params2 = {"address": city + location_name, "city": city}
            result = _call_gaode("geocode", params2)
    geocodes = []
    if isinstance(result, dict):
        geocodes = result.get("geocodes", [])
    if not geocodes:
        return None
    loc = geocodes[0].get("location", "")
    if not loc or "," not in loc:
        return None
    parts = loc.split(",")
    try:
        return (float(parts[0]), float(parts[1]))
    except (ValueError, IndexError):
        return None


def _extract_city(text):
    """从文本中提取城市名"""
    for c in _CITIES:
        if c in text:
            return c
    return ""


def _estimate_taxi_fare(distance_m):
    """简单估算打车费用"""
    distance_km = distance_m / 1000
    if distance_km <= 0:
        return "¥0"
    if distance_km <= 3:
        return "¥14左右"
    cost = 14 + (distance_km - 3) * 2.5
    return f"¥{int(cost)}左右"


def _is_metro_line(name):
    """判断是否地铁/城轨线路"""
    kws = ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"]
    return any(kw in name for kw in kws)


# ============================================================
# 互动推荐（每个工具返回结果后提示其他相关功能）
# ============================================================

_TOOL_TIPS = {
    "plan_trip": "🗺️行程规划",
    "search_train": "🚄火车票",
    "search_flight": "✈️机票查询",
    "search_hotel": "🏨酒店搜索",
    "search_poi": "🎫景点门票",
    "search_fast": "⚡极速搜索",
    "search_marriott_hotel": "🏨万豪酒店",
    "get_marriott_hotel_info": "📋万豪详情",
    "search_food": "🍜美食推荐",
    "search_transport": "🚇市内交通",
}

# 工具间的推荐组合：当前工具 → 推荐的下一步工具
_RELATED_TIPS = {
    "plan_trip": ["search_train", "search_hotel", "search_poi", "search_food", "search_transport"],
    "search_train": ["search_hotel", "search_poi", "search_transport"],
    "search_flight": ["search_hotel", "search_poi", "search_transport"],
    "search_hotel": ["search_poi", "search_food", "search_transport"],
    "search_poi": ["search_hotel", "search_food", "search_transport"],
    "search_fast": ["search_hotel", "search_poi", "search_food"],
    "search_marriott_hotel": ["get_marriott_hotel_info", "search_food", "search_transport"],
    "get_marriott_hotel_info": ["search_marriott_hotel", "search_food", "search_transport"],
    "search_food": ["search_hotel", "search_poi", "search_transport"],
    "search_transport": ["search_food", "search_poi", "search_hotel"],
}


def _build_tips(current_tool, dest=""):
    """生成互动推荐提示文本"""
    related = _RELATED_TIPS.get(current_tool, [])
    if not related:
        return ""
    tips = []
    for t in related:
        if t in _TOOL_TIPS:
            tips.append(_TOOL_TIPS[t])
    if not tips:
        return ""
    prefix = f"\n\n💡 到了{dest}还可以：" if dest else "\n\n💡 你可能还想："
    return prefix + " | ".join(tips)


# ============================================================
# 飞猪工具（8个）
# ============================================================

def plan_trip(destination="", days="", **kwargs):
    """行程规划：输入目的地+天数，返回推荐行程安排"""
    if not destination or not days:
        return json.dumps({"error": "请提供destination(目的地)和days(天数)"}, ensure_ascii=False)
    result = _call_flyai("plan_trip", {"destination": destination, "days": str(days)})
    text = _parse_flyai_text(result)
    return json.dumps({
        "destination": destination,
        "days": days,
        "itinerary": text,
        "disclaimer": "⚠️ 行程仅供参考，请根据实际情况调整",
        "tips": _build_tips("plan_trip", destination)
    }, ensure_ascii=False, indent=2)


def search_train(origin="", destination="", date="", **kwargs):
    """火车票查询：出发地+目的地+日期，返回车次/余票/票价"""
    if not origin or not destination or not date:
        return json.dumps({"error": "请提供origin(出发地)、destination(目的地)、date(日期YYYY-MM-DD)"}, ensure_ascii=False)
    result = _call_flyai("search_train", {
        "origin": origin, "destination": destination, "date": date,
    })
    text = _parse_flyai_text(result)
    return json.dumps({
        "origin": origin, "destination": destination, "date": date,
        "trains": text,
        "disclaimer": "⚠️ 余票和票价实时变动，请以12306为准",
        "tips": _build_tips("search_train", destination)
    }, ensure_ascii=False, indent=2)


def search_flight(origin="", destination="", date="", **kwargs):
    """机票查询：出发地+目的地+日期，返回航班号/价格/时间"""
    if not origin or not destination or not date:
        return json.dumps({"error": "请提供origin(出发城市)、destination(到达城市)、date(日期YYYY-MM-DD)"}, ensure_ascii=False)
    args = {"origin": origin, "destination": destination}
    if date:
        args["depDate"] = date
    for k in ["back_date", "seat_class", "direct_only"]:
        if k in kwargs:
            args[k] = kwargs[k]
    result = _call_flyai("search_flight", args)
    text = _parse_flyai_text(result)
    return json.dumps({
        "origin": origin, "destination": destination, "date": date,
        "flights": text,
        "disclaimer": "⚠️ 机票价格实时变动，请以航司官网为准",
        "tips": _build_tips("search_flight", destination)
    }, ensure_ascii=False, indent=2)


def search_hotel(destination="", checkin="", checkout="", **kwargs):
    """酒店搜索：目的地+入住/离店日期+可选筛选，返回酒店/价格/链接"""
    if not destination or not checkin or not checkout:
        return json.dumps({"error": "请提供destination(目的地)、checkin(入住日期)、checkout(离店日期)"}, ensure_ascii=False)
    args = {"destName": destination, "checkInDate": checkin, "checkOutDate": checkout}
    for k, v in kwargs.items():
        if k in ["keywords", "star", "max_price", "hotel_type", "bed_type"]:
            args[k] = v
    result = _call_flyai("search_hotels", args)
    text = _parse_flyai_text(result)
    return json.dumps({
        "destination": destination, "checkin": checkin, "checkout": checkout,
        "hotels": text,
        "disclaimer": "⚠️ 酒店价格实时变动，请以预订页面为准",
        "tips": _build_tips("search_hotel", destination)
    }, ensure_ascii=False, indent=2)


def search_poi(keyword="", city="", **kwargs):
    """景点门票：关键词/城市，返回景点+门票价格+购票链接"""
    if not keyword and not city:
        return json.dumps({"error": "请提供keyword(关键词)或city(城市)"}, ensure_ascii=False)
    args = {}
    if keyword:
        args["keyword"] = keyword
    if city:
        args["cityName"] = city
    if "category" in kwargs:
        args["category"] = kwargs["category"]
    if "poi_level" in kwargs:
        args["poiLevel"] = kwargs["poi_level"]
    result = _call_flyai("search_poi", args)
    text = _parse_flyai_text(result)
    return json.dumps({
        "keyword": keyword, "city": city,
        "attractions": text,
        "disclaimer": "⚠️ 门票价格可能变动，请以景区官方为准",
        "tips": _build_tips("search_poi", city or keyword)
    }, ensure_ascii=False, indent=2)


def search_fast(keyword="", **kwargs):
    """极速搜索：通用关键词快速搜索"""
    if not keyword:
        return json.dumps({"error": "请提供keyword(搜索关键词)"}, ensure_ascii=False)
    result = _call_flyai("fliggy_fast_search", {"query": keyword})
    text = _parse_flyai_text(result)
    return json.dumps({
        "keyword": keyword,
        "results": text,
        "disclaimer": "⚠️ 搜索结果仅供参考",
        "tips": _build_tips("search_fast", keyword)
    }, ensure_ascii=False, indent=2)


def search_marriott_hotel(destination="", checkin="", checkout="", **kwargs):
    """万豪酒店搜索：搜索万豪集团旗下酒店"""
    if not destination:
        return json.dumps({"error": "请提供destination(目的地)"}, ensure_ascii=False)
    args = {"destName": destination}
    if checkin:
        args["checkInDate"] = checkin
    if checkout:
        args["checkOutDate"] = checkout
    for k in ["keywords", "max_price", "bed_type"]:
        if k in kwargs:
            args[k] = kwargs[k]
    result = _call_flyai("search_marriott_hotels", args)
    text = _parse_flyai_text(result)
    return json.dumps({
        "destination": destination, "checkin": checkin or "未指定", "checkout": checkout or "未指定",
        "hotels": text,
        "disclaimer": "⚠️ 万豪酒店价格实时变动，请以万豪官网为准",
        "tips": _build_tips("search_marriott_hotel", destination)
    }, ensure_ascii=False, indent=2)


def get_marriott_hotel_info(hotel_name="", hotel_id="", **kwargs):
    """万豪酒店详情：获取万豪酒店详细信息"""
    if not hotel_name and not hotel_id:
        return json.dumps({"error": "请提供hotel_name(酒店名称)或hotel_id(酒店ID)"}, ensure_ascii=False)
    args = {}
    if hotel_name:
        args["hotelName"] = hotel_name
    if hotel_id:
        args["shid"] = hotel_id
    if "review_keyword" in kwargs:
        args["reviewKeyword"] = kwargs["review_keyword"]
    result = _call_flyai("get_marriott_hotel_info", args)
    text = _parse_flyai_text(result)
    return json.dumps({
        "hotel_name": hotel_name, "hotel_id": hotel_id,
        "detail": text,
        "disclaimer": "⚠️ 房型和价格实时变动，请以万豪官网为准",
        "tips": _build_tips("get_marriott_hotel_info", hotel_name)
    }, ensure_ascii=False, indent=2)


# ============================================================
# 高德工具（2个，打车整合进市内交通）
# ============================================================

def search_food(location="", city="", keyword="", **kwargs):
    """美食推荐：基于位置搜索周边餐厅，返回名称/评分/人均/地址"""
    if not location and not city:
        return json.dumps({"error": "请提供location(位置)或city(城市)"}, ensure_ascii=False)

    search_loc = location or city
    search_city = city or _extract_city(search_loc)

    # 1. 地理编码获取经纬度
    coords = _geocode(search_loc, search_city)
    if not coords:
        return json.dumps({"error": f"无法获取「{search_loc}」的地理位置，请尝试更具体的地址"}, ensure_ascii=False)

    lng, lat = coords

    # 2. 周边搜索餐饮类型
    around_params = {
        "location": f"{lng},{lat}",
        "types": "050000",
        "offset": 15,
        "sortrule": "weight",
    }
    if search_city:
        around_params["city"] = search_city
    if keyword:
        around_params["keywords"] = keyword

    result = _call_gaode("place/around", around_params)
    if isinstance(result, dict) and "error" in result:
        return json.dumps({"error": f"美食搜索失败: {result['error']}"}, ensure_ascii=False)

    # 3. 解析POI数据
    pois = []
    if isinstance(result, dict):
        pois = result.get("pois", [])

    if not pois:
        return json.dumps({
            "location": search_loc,
            "message": f"在「{search_loc}」附近未找到餐厅",
        }, ensure_ascii=False)

    # 4. 格式化输出
    foods = []
    for i, poi in enumerate(pois[:15], 1):
        name = poi.get("name", "未知")
        rating = poi.get("rating", "")
        biz_ext = poi.get("biz_ext", {}) or {}
        cost = poi.get("cost", "") or biz_ext.get("cost", "")
        address = poi.get("address", "暂无")
        poi_type = poi.get("type", "")
        # 提取菜系标签
        type_parts = poi_type.split(";") if poi_type else []
        cuisine = type_parts[1] if len(type_parts) >= 2 else ""
        if not cuisine:
            cuisine = "美食"

        foods.append({
            "index": i,
            "name": name,
            "cuisine": cuisine,
            "rating": rating if rating and rating not in ("0", "-1") else "暂无",
            "avg_cost": f"¥{cost}" if cost and cost not in ("0", "-1") else "暂无",
            "address": address,
        })

    return json.dumps({
        "location": search_loc,
        "count": len(foods),
        "restaurants": foods,
        "disclaimer": "⚠️ 评分和人均消费仅供参考，请以实际为准",
        "tips": _build_tips("search_food", search_loc)
    }, ensure_ascii=False, indent=2)


def search_transport(origin="", destination="", city="", **kwargs):
    """市内交通：从A到B的打车预估+公交地铁路线+高德打车唤端链接"""
    if not origin or not destination:
        return json.dumps({"error": "请提供origin(起点)和destination(终点)"}, ensure_ascii=False)

    # 1. 地理编码获取起终点经纬度
    transport_city = city or _extract_city(origin) or _extract_city(destination)
    origin_coords = _geocode(origin, transport_city)
    if not origin_coords:
        return json.dumps({"error": f"无法获取「{origin}」的地理位置"}, ensure_ascii=False)

    dest_coords = _geocode(destination, transport_city)
    if not dest_coords:
        return json.dumps({"error": f"无法获取「{destination}」的地理位置"}, ensure_ascii=False)

    origin_loc = f"{origin_coords[0]},{origin_coords[1]}"
    dest_loc = f"{dest_coords[0]},{dest_coords[1]}"

    # 2. 驾车路线（打车预估）
    driving_result = _call_gaode("direction/driving", {
        "origin": origin_loc, "destination": dest_loc, "strategy": 0,
    })

    taxi_info = {}
    if isinstance(driving_result, dict) and "error" not in driving_result:
        route = driving_result.get("route", {})
        paths = route.get("paths", [])
        if paths:
            path = paths[0]
            distance = int(path.get("distance", 0))
            duration = int(path.get("duration", 0))
            taxi_info = {
                "distance_km": round(distance / 1000, 1),
                "duration_min": round(duration / 60),
                "taxi_fare_estimate": _estimate_taxi_fare(distance),
            }

    # 3. 生成高德打车唤端链接
    dest_encoded = urllib.parse.quote(destination)
    taxi_url = f"https://uri.amap.com/navigation?to={dest_coords[0]},{dest_coords[1]},{dest_encoded}&mode=car&callnative=1"
    if origin_coords:
        origin_encoded = urllib.parse.quote(origin)
        taxi_url += f"&from={origin_coords[0]},{origin_coords[1]},{origin_encoded}"

    # 4. 公交地铁路线
    transit_params = {
        "origin": origin_loc, "destination": dest_loc,
        "city": transport_city, "strategy": 0, "nightflag": 0,
    }
    transit_result = _call_gaode("direction/transit/integrated", transit_params)

    metro_routes = []
    bus_routes = []

    if isinstance(transit_result, dict) and "error" not in transit_result:
        route = transit_result.get("route", {})
        transits = route.get("transits", [])
        for t in transits[:6]:
            segments = t.get("segments", [])
            duration = int(t.get("duration", 0))
            walking_dist = int(t.get("walking_distance", "0") or 0)
            cost = t.get("cost", "")

            lines = []
            is_metro = False

            for seg in segments:
                bus_seg = seg.get("bus", {})
                if bus_seg:
                    bus_lines = bus_seg.get("buslines", [])
                    if bus_lines:
                        bl = bus_lines[0]
                        bl_name = bl.get("name", "")
                        dep_stop = bl.get("departure_stop", {}).get("name", "")
                        arr_stop = bl.get("arrival_stop", {}).get("name", "")
                        via_num = bl.get("via_num", 0)
                        if _is_metro_line(bl_name):
                            is_metro = True
                        lines.append({
                            "name": bl_name,
                            "departure": dep_stop,
                            "arrival": arr_stop,
                            "stops": via_num,
                            "is_metro": _is_metro_line(bl_name),
                        })

            route_item = {
                "lines": lines,
                "duration_min": round(duration / 60),
                "walking_distance_m": walking_dist,
                "cost": f"¥{cost}" if cost and cost != "0" else "",
            }

            if is_metro:
                metro_routes.append(route_item)
            else:
                bus_routes.append(route_item)

    return json.dumps({
        "origin": origin,
        "destination": destination,
        "city": transport_city,
        "taxi": taxi_info,
        "taxi_url": taxi_url,
        "taxi_tip": "🚕 点击链接可唤起高德地图APP打车",
        "metro_routes": metro_routes[:3],
        "bus_routes": bus_routes[:3],
        "disclaimer": "⚠️ 打车费用为估算，公交路线仅供参考，请以实际为准",
        "tips": _build_tips("search_transport", destination)
    }, ensure_ascii=False, indent=2)


# ============================================================
# 工具注册表和主入口
# ============================================================

TOOLS = {
    # 飞猪工具（8个）
    "plan_trip": plan_trip,
    "search_train": search_train,
    "search_flight": search_flight,
    "search_hotel": search_hotel,
    "search_poi": search_poi,
    "search_fast": search_fast,
    "search_marriott_hotel": search_marriott_hotel,
    "get_marriott_hotel_info": get_marriott_hotel_info,
    # 高德工具（2个）
    "search_food": search_food,
    "search_transport": search_transport,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python travel_assistant.py <tool_name> [key=value ...]")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(f"未知工具: {tool_name}")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k] = v
    print(TOOLS[tool_name](**kwargs))
