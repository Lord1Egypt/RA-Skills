# -*- coding: utf-8 -*-
"""
酒店智能搜索 - ClawHub技能脚本
数据源：飞猪旅行 + 高德地图（SCF代理），零配置
5合1：酒店搜索 + 万豪搜索/详情/套餐 + 周边餐饮
"""
import json
import urllib.request
import urllib.error

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 60

_MARRIOTT_BRANDS = [
    "万豪", "喜来登", "威斯汀", "丽思卡尔顿", "JW", "万丽", "万枫",
    "艾美", "豪华精选", "W酒店", "瑞吉", "雅乐轩", "源宿",
]

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
]


# ============ 代理调用 ============
def _call_fliggy(rtype, params):
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = json.loads(r.read().decode("utf-8"))
            if isinstance(raw, dict) and "code" in raw:
                if raw.get("code") == 0:
                    return raw.get("data", raw)
                else:
                    return {"error": "SCF proxy error: " + str(raw.get("message", raw))}
            return raw
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:200]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_gaode(api, params):
    body = json.dumps({"type": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        GAODE_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = json.loads(r.read().decode("utf-8"))
            if isinstance(raw, dict) and "code" in raw:
                if raw.get("code") == 0:
                    return raw.get("data", raw)
                else:
                    return {"error": "SCF proxy error: " + str(raw.get("message", raw))}
            return raw
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:200]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


# ============ 辅助 ============
def _extract_city(query):
    for city in _CITIES:
        if city in query: return city
    return ""

def _build_tips(current_tool, query=""):
    city = _extract_city(query)
    d = city or "目的地"
    tips_map = {
        "search_hotels": "📋 附加服务：🏨" + d + "万豪品牌酒店 | 🎫推荐" + d + "景点 | 🍜" + d + "周边餐饮 | 🚄查去" + d + "的火车票 | ✈️查去" + d + "的机票",
        "search_marriott_hotels": "📋 附加服务：🏨" + d + "更多酒店 | 🎫推荐" + d + "景点 | 🍜" + d + "周边餐饮",
        "get_marriott_hotel_info": "📋 附加服务：🏨搜索更多万豪酒店 | 🎫推荐" + d + "景点 | 🍜" + d + "周边餐饮",
        "search_marriott_packages": "📋 附加服务：🏨搜索更多万豪酒店 | 🎫推荐" + d + "景点 | 🍜" + d + "周边餐饮",
        "search_food": "📋 附加服务：🏨推荐" + d + "酒店 | 🎫推荐" + d + "景点 | 🚇" + d + "市内交通",
    }
    return "\n\n" + tips_map.get(current_tool, "")

def _format_ai_text(data):
    if isinstance(data, dict) and "error" in data:
        return "查询失败: " + data["error"]
    inner = data.get("data", data) if isinstance(data, dict) else data
    if isinstance(inner, str):
        text = inner
        if "飞猪" not in text:
            text = text.rstrip() + "\n\n数据来源：飞猪旅行"
        return text
    if isinstance(inner, dict):
        items = inner.get("itemList", [])
        if items:
            return _format_hotel_list(data)
        text = json.dumps(inner, ensure_ascii=False, indent=2)
        if len(text) > 500: text = text[:500] + "..."
        return text
    return str(data) if data else "未找到相关信息。"

def _format_hotel_list(data):
    if isinstance(data, dict) and "error" in data:
        return "查询失败: " + data["error"]
    inner = data.get("data", data) if isinstance(data, dict) else data
    if inner is None: inner = {}
    items = inner.get("itemList", []) if isinstance(inner, dict) else []
    if not items: return "未找到符合条件的酒店，建议调整搜索条件后重试。"

    lines = ["找到 " + str(len(items)) + " 家酒店：", ""]
    for i, item in enumerate(items[:10], 1):
        info = item.get("info", item)
        name = info.get("title", info.get("name", ""))
        price = info.get("price", item.get("ticketPrice", ""))
        rating = info.get("rating", "")
        star = info.get("star", "")
        address = info.get("address", "")
        url = info.get("jumpUrl", info.get("detailUrl", item.get("jumpUrl", item.get("detailUrl", ""))))

        line = str(i) + ". " + name
        details = []
        if star and str(star).strip(): details.append(str(star).strip())
        if rating and str(rating).strip(): details.append("评分" + str(rating).strip())
        if price and str(price).strip(): details.append("¥" + str(price).strip() + "起")
        if details: line += " | " + " | ".join(details)
        lines.append(line)
        if address: lines.append("   地址：" + address)
        if url: lines.append("   预订：" + url)
        lines.append("")
    lines.append("价格实时变动，以实际下单为准")
    lines.append("数据来源：飞猪旅行")
    return "\n".join(lines)

def _format_food_list(data):
    if isinstance(data, dict) and "error" in data:
        return "查询失败: " + data["error"]
    pois = data.get("pois", []) if isinstance(data, dict) else []
    if not pois: return "未找到附近的餐饮，建议扩大搜索范围。"

    lines = ["找到 " + str(len(pois)) + " 家餐饮：", ""]
    for i, poi in enumerate(pois[:10], 1):
        name = poi.get("name", "")
        type_name = poi.get("type", "")
        address = poi.get("address", "")
        distance = poi.get("distance", "")
        biz = poi.get("biz_ext", {})
        rating = biz.get("rating", "") if isinstance(biz, dict) else ""
        cost = biz.get("cost", "") if isinstance(biz, dict) else ""

        line = str(i) + ". " + name
        details = []
        if type_name: details.append(type_name.split(";")[0])
        if rating and str(rating).strip() and str(rating) != "[]": details.append("评分" + str(rating))
        if cost and str(cost).strip() and str(cost) != "[]": details.append("人均¥" + str(cost))
        if distance: details.append(str(distance) + "米")
        if details: line += " | " + " | ".join(details)
        lines.append(line)
        if address: lines.append("   " + address)
        lines.append("")
    lines.append("数据来源：高德地图")
    return "\n".join(lines)


# ============ 工具函数 ============

def search_hotels(params):
    """酒店搜索：搜索国内酒店，返回实时价格和飞猪预订链接。"""
    query = params.get("query", "")
    if not query: return "请输入酒店搜索描述，如：三亚亚龙湾亲子酒店"
    data = _call_fliggy("fliggy_ai_search", {"query": query.strip()})
    text = _format_ai_text(data)
    return text + _build_tips("search_hotels", query)


def search_marriott_hotels(params):
    """万豪酒店搜索：搜索万豪集团旗下品牌酒店。"""
    query = params.get("query", "")
    if not query: return "请输入万豪品牌酒店搜索描述"
    q = query.strip()
    if "万豪" not in q and not any(brand in q for brand in _MARRIOTT_BRANDS):
        q = q + " 万豪"
    data = _call_fliggy("search_marriott_hotels", {"query": q})
    inner = data.get("data", data) if isinstance(data, dict) else data
    if inner is None or (isinstance(inner, dict) and not inner.get("itemList")) or (isinstance(data, dict) and data.get("status") == 0 and data.get("data") is None):
        data = _call_fliggy("fliggy_ai_search", {"query": q})
    text = _format_ai_text(data)
    return text + _build_tips("search_marriott_hotels", query)


def get_marriott_hotel_info(params):
    """万豪酒店详情：获取万豪品牌酒店的详细信息。"""
    query = params.get("query", "")
    if not query: return "请输入万豪酒店名称"
    data = _call_fliggy("get_marriott_hotel_info", {"query": query.strip()})
    if isinstance(data, dict) and (data.get("status") == 1 or (data.get("status") == 0 and data.get("data") is None)):
        data = _call_fliggy("fliggy_ai_search", {"query": query.strip() + " 详细信息"})
    text = _format_ai_text(data)
    return text + _build_tips("get_marriott_hotel_info", query)


def search_marriott_packages(params):
    """万豪套餐搜索：搜索万豪品牌酒店的套餐产品。"""
    query = params.get("query", "")
    if not query: return "请输入万豪酒店套餐搜索描述"
    data = _call_fliggy("search_marriott_packages", {"query": query.strip()})
    inner = data.get("data", data) if isinstance(data, dict) else data
    if inner is None or (isinstance(data, dict) and data.get("status") == 0 and data.get("data") is None):
        data = _call_fliggy("fliggy_ai_search", {"query": query.strip()})
    text = _format_ai_text(data)
    return text + _build_tips("search_marriott_packages", query)


def search_food(params):
    """周边餐饮：搜索酒店周边餐饮美食。"""
    query = params.get("query", "")
    if not query: return "请输入餐饮搜索描述，如：西湖附近美食"
    q = query.strip()
    city = _extract_city(q)

    geo_params = {"address": q.replace("附近", "").replace("周边", "")}
    if city: geo_params["city"] = city
    geo_data = _call_gaode("geocode", geo_params)

    location = ""
    if isinstance(geo_data, dict):
        geocodes = geo_data.get("geocodes", [])
        if geocodes: location = geocodes[0].get("location", "")

    if not location: return "无法定位搜索位置，请尝试更具体的地址描述"

    poi_params = {"location": location, "keywords": "美食", "types": "050000", "radius": "3000", "offset": "10"}
    if city: poi_params["city"] = city
    data = _call_gaode("poi_around", poi_params)
    text = _format_food_list(data)
    return text + _build_tips("search_food", query)
