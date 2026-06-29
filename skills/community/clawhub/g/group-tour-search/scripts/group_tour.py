# -*- coding: utf-8 -*-
"""
跟团游搜索与推荐 - ClawHub技能脚本
3个工具：跟团游搜索与推荐、去目的地火车票、去目的地机票
数据源：同程旅行（SCF代理）+ 飞猪旅行（SCF代理），零配置
"""
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ============ 配置 ============
TONGCHENG_PROXY = "https://1439498936-7vqpkiipef.ap-guangzhou.tencentscf.com"
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TC_TIMEOUT = 15
FG_TIMEOUT = 30

# ============ 场景→目的地映射 ============
SCENE_MAP = {
    "海边": ["三亚", "厦门", "北海", "涠洲岛", "平潭", "舟山", "青岛", "大连"],
    "沙滩": ["三亚", "厦门", "北海", "涠洲岛", "平潭"],
    "海岛": ["三亚", "涠洲岛", "平潭", "舟山", "厦门"],
    "古镇": ["乌镇", "西塘", "凤凰古城", "镇远", "婺源", "南浔"],
    "水乡": ["乌镇", "西塘", "南浔", "周庄", "同里"],
    "山水": ["桂林", "张家界", "九寨沟", "黄山", "稻城亚丁", "阳朔"],
    "自然": ["九寨沟", "稻城亚丁", "张家界", "桂林", "黄山", "恩施"],
    "亲子": ["三亚", "上海", "成都", "珠海", "广州", "桂林"],
    "家庭": ["三亚", "成都", "上海", "桂林", "厦门"],
    "人文": ["西安", "北京", "南京", "敦煌", "洛阳", "成都"],
    "历史": ["西安", "北京", "南京", "敦煌", "洛阳"],
    "古城": ["西安", "北京", "南京", "凤凰古城", "镇远", "丽江"],
    "雪山": ["丽江", "拉萨", "稻城亚丁", "峨眉山", "阿勒泰"],
    "高原": ["拉萨", "稻城亚丁", "丽江", "峨眉山", "青海湖"],
    "草原": ["呼伦贝尔", "中卫", "伊犁", "阿勒泰"],
    "沙漠": ["中卫", "张掖", "敦煌"],
    "边境": ["西双版纳", "芒市", "腾冲", "延吉"],
    "异域": ["西双版纳", "芒市", "腾冲", "喀什"],
    "温泉": ["腾冲", "峨眉山", "南京", "黄山"],
    "避暑": ["哈尔滨", "长春", "呼伦贝尔", "阿勒泰", "庐山", "青岛"],
    "冰雪": ["哈尔滨", "长春", "阿勒泰", "长白山"],
    "美食": ["成都", "长沙", "潮汕", "广州", "重庆"],
    "红色": ["延安", "井冈山", "遵义", "韶山"],
}

# 热门目的地（兜底推荐）
HOT_DESTINATIONS = ["三亚", "丽江", "桂林", "成都", "西安", "厦门", "张家界", "北京"]

# 城市名集合
_CITY_SET = set([
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
    "洛阳", "敦煌", "遵义", "延安", "潮汕", "延吉", "喀什",
])

# 景点/区域名→搜索关键词映射
_SPOT_TO_CITY = {
    "九寨沟": "九寨沟", "黄山": "黄山", "泰山": "泰山", "峨眉山": "峨眉山",
    "武夷山": "武夷山", "长白山": "长白山", "庐山": "庐山", "五台山": "五台山",
    "普陀山": "普陀山", "乌镇": "乌镇", "西塘": "西塘", "南浔": "南浔",
    "凤凰古城": "凤凰古城", "镇远": "镇远", "婺源": "婺源",
    "涠洲岛": "涠洲岛", "平潭": "平潭", "舟山": "舟山",
    "呼伦贝尔": "呼伦贝尔", "稻城亚丁": "稻城亚丁", "恩施": "恩施",
    "西双版纳": "西双版纳", "芒市": "芒市", "腾冲": "腾冲",
    "中卫": "中卫", "张掖": "张掖", "阿勒泰": "阿勒泰", "伊犁": "伊犁",
    "千岛湖": "千岛湖", "阳朔": "阳朔",
    "西江千户苗寨": "西江千户苗寨", "青海湖": "青海湖",
}


# ============ 代理调用 ============
def _call_tongcheng(rtype, params):
    """调用同程SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        TONGCHENG_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TC_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_fliggy(rtype, params, timeout=None):
    """调用飞猪SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    _timeout = timeout or FG_TIMEOUT
    try:
        with urllib.request.urlopen(req, timeout=_timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


# ============ 工具函数 ============
def _extract_destinations(query):
    """从用户输入中提取目的地列表（用于跟团游搜索）"""
    dests = []

    # 1. 先匹配场景关键词
    for scene, cities in SCENE_MAP.items():
        if scene in query:
            dests.extend(cities[:3])
            break

    # 2. 匹配景点→城市
    for spot, city in _SPOT_TO_CITY.items():
        if spot in query and city not in dests:
            dests.append(city)

    # 3. 匹配城市名
    for city in _CITY_SET:
        if city in query and city not in dests:
            dests.append(city)

    # 4. 兜底：无匹配时推荐热门
    if not dests:
        dests = HOT_DESTINATIONS[:3]

    return dests[:5]


def _extract_city_for_transport(query):
    """从查询中提取城市名（用于火车/机票查询）"""
    for spot, city in _SPOT_TO_CITY.items():
        if spot in query:
            return city
    for city in _CITY_SET:
        if city in query:
            return city
    return ""


def _smart_parse_date(date_str):
    """智能解析日期"""
    if not date_str:
        return "", "请提供出发日期，如：明天、7月1号、2026-07-01"

    today = datetime.now()
    date_str = date_str.strip()

    if date_str in ("今天", "今日"):
        return today.strftime("%Y-%m-%d"), ""
    if date_str == "明天":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d"), ""
    if date_str == "后天":
        return (today + timedelta(days=2)).strftime("%Y-%m-%d"), ""
    if date_str == "大后天":
        return (today + timedelta(days=3)).strftime("%Y-%m-%d"), ""

    m = re.match(r"(\d{1,2})月(\d{1,2})[日号]", date_str)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = today.year
        try:
            dt = datetime(year, month, day)
            if dt < today:
                dt = datetime(year + 1, month, day)
            return dt.strftime("%Y-%m-%d"), ""
        except ValueError:
            return "", f"日期格式错误：{date_str}"

    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt < today:
                return "", "日期不能早于今天"
            return dt.strftime("%Y-%m-%d"), ""
        except ValueError:
            continue

    if re.match(r"^\d{4}$", date_str):
        month, day = int(date_str[:2]), int(date_str[2:])
        try:
            dt = datetime(today.year, month, day)
            if dt < today:
                dt = datetime(today.year + 1, month, day)
            return dt.strftime("%Y-%m-%d"), ""
        except ValueError:
            pass

    return "", f"无法识别日期：{date_str}，请用如：明天、7月1号、2026-07-01"


def _clean_airline(name):
    """航司名清洗：含｜取最后一段"""
    if "｜" in name:
        name = name.split("｜")[-1]
    return name.strip()


def _parse_tour_data(data, dest):
    """解析同程跟团游数据"""
    if isinstance(data, dict) and data.get("error"):
        return f"查询{dest}跟团游失败：{data['error']}"

    trips = []
    if isinstance(data, dict):
        trips = data.get("data", {}).get("trips", [])
    elif isinstance(data, list):
        trips = data

    if not trips:
        return ""

    lines = []
    for i, t in enumerate(trips, 1):
        name = t.get("name", "")
        price = t.get("price", "")
        score = t.get("score", "")
        comment_num = t.get("commentNum", "")
        label_list = t.get("labelList", [])
        scenery = t.get("sceneryNameList", [])
        url = t.get("redirectUrl") or t.get("clawRedirectUrl") or ""

        score_str = ""
        if score:
            try:
                s = float(score)
                score_str = f"{s:.2f}" if s > 0 else ""
            except (ValueError, TypeError):
                score_str = str(score)

        label_str = "·".join(label_list[:3]) if label_list else ""

        scenery_str = ""
        if scenery:
            top = scenery[:5]
            scenery_str = "、".join(top)
            if len(scenery) > 5:
                scenery_str += f"等{len(scenery)}个景点"

        parts = [f"{i}. {name}"]
        detail = []
        if price:
            detail.append(f"¥{price}起")
        if score_str:
            detail.append(f"⭐{score_str}")
        if comment_num:
            detail.append(f"💬{comment_num}条评价")
        if label_str:
            detail.append(label_str)
        if detail:
            parts.append(" | ".join(detail))
        if scenery_str:
            parts.append(f"📍 {scenery_str}")
        if url:
            parts.append(f"🔗 [查看详情与预订]({url})")

        lines.append("\n".join(parts))

    return "\n\n".join(lines)


def _parse_train_data(data, dep, arr, date_str):
    """解析飞猪search_domestic_train数据（itemList→journeys→segments）"""
    items = []
    if isinstance(data, dict):
        d = data.get("data", data)
        if isinstance(d, dict):
            items = d.get("itemList", [])
        elif isinstance(d, list):
            items = d

    if not items:
        return ""

    lines = [f"🚄 {dep}→{arr} {date_str} 火车票", ""]

    for i, item in enumerate(items[:8], 1):
        journeys = item.get("journeys", [])
        jump_url = item.get("jumpUrl", "")

        for j in journeys[:1]:
            jtype = j.get("journeyType", "")
            segs = j.get("segments", [])

            seg_parts = []
            for s in segs:
                train_no = s.get("trainNo", "")
                dep_station = s.get("depStationShortName") or s.get("depStationName", "")
                arr_station = s.get("arrStationShortName") or s.get("arrStationName", "")
                dep_time = s.get("depDateTime", "")
                arr_time = s.get("arrDateTime", "")

                # 只取时分
                dep_hm = dep_time[11:16] if len(dep_time) >= 16 else dep_time
                arr_hm = arr_time[11:16] if len(arr_time) >= 16 else arr_time

                seg_parts.append(f"{train_no} {dep_station}→{arr_station} {dep_hm}→{arr_hm}")

            type_tag = "直达" if jtype == "直达" else "中转"
            line = f"{i}. [{'✅直达' if jtype == '直达' else '🔄中转'}] " + " | ".join(seg_parts)
            if jump_url:
                line += f"  [预订]({jump_url})"
            lines.append(line)

    return "\n".join(lines)


def _parse_flight_data(data, dep, arr, date_str):
    """解析飞猪search_flight数据（itemList→journeys→segments）"""
    items = []
    if isinstance(data, dict):
        d = data.get("data", data)
        if isinstance(d, dict):
            items = d.get("itemList", [])
        elif isinstance(d, list):
            items = d

    if not items:
        return ""

    lines = [f"✈️ {dep}→{arr} {date_str} 航班", ""]

    for i, item in enumerate(items[:8], 1):
        journeys = item.get("journeys", [])
        jump_url = item.get("jumpUrl", "")

        for j in journeys[:1]:
            jtype = j.get("journeyType", "")
            segs = j.get("segments", [])

            seg_parts = []
            for s in segs:
                flight_no = s.get("flightNo", "")
                airline = s.get("airlineShortName") or s.get("airlineName", "")
                airline = _clean_airline(airline)
                dep_station = s.get("depStationShortName") or s.get("depCityName", "")
                arr_station = s.get("arrStationShortName") or s.get("arrCityName", "")
                dep_time = s.get("depDateTime", "")
                arr_time = s.get("arrDateTime", "")

                dep_hm = dep_time[11:16] if len(dep_time) >= 16 else dep_time
                arr_hm = arr_time[11:16] if len(arr_time) >= 16 else arr_time

                seg_parts.append(f"{airline}{flight_no} {dep_station}→{arr_station} {dep_hm}→{arr_hm}")

            type_tag = "✅直达" if jtype == "直达" else "🔄中转"
            line = f"{i}. [{type_tag}] " + " | ".join(seg_parts)
            if jump_url:
                line += f"  [预订]({jump_url})"
            lines.append(line)

    return "\n".join(lines)


# ============ 工具1：跟团游搜索与推荐 ============
def search_tour(params):
    """跟团游搜索与推荐：搜索跟团游/私家团/纯玩线路，支持场景推荐和目的地搜索。"""
    destination = params.get("destination", "")
    query = params.get("query", "")

    text = f"{destination} {query}".strip()

    # 提取目的地列表
    dests = _extract_destinations(text)

    # 判断是否为场景推荐（无明确目的地关键词命中，只有场景词）
    is_scene = True
    for d in dests:
        if d in text:
            is_scene = False
            break

    search_count = 3 if is_scene else 1
    search_dests = dests[:search_count]

    results = []
    for dest in search_dests:
        resp = _call_tongcheng("tongcheng_travel_search", {"destination": dest})
        parsed = _parse_tour_data(resp, dest)
        if parsed:
            results.append((dest, parsed))

    if not results:
        return "暂无跟团游数据，建议换个目的地或场景试试，如：三亚跟团游、想去海边、亲子游"

    lines = []
    if is_scene and len(results) > 1:
        scene_hint = ""
        for scene, cities in SCENE_MAP.items():
            if scene in text:
                scene_hint = f"「{scene}」推荐以下目的地跟团游："
                break
        if not scene_hint:
            scene_hint = "为您推荐热门跟团游："
        lines.append(scene_hint)

    for dest, parsed in results:
        if len(results) > 1:
            lines.append(f"━━━ {dest} ━━━")
        lines.append(parsed)

    return "\n\n".join(lines)


# ============ 工具2：去目的地火车票 ============
def search_train(params):
    """去目的地火车票：查询到旅游目的地的火车票/高铁票，含直达和中转方案。"""
    departure = params.get("departure", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "明天")

    if not departure:
        return "请提供出发城市，如：上海、北京"
    if not destination:
        return "请提供旅游目的地，如：三亚、丽江"

    parsed_date, date_hint = _smart_parse_date(dep_date)
    if not parsed_date:
        return date_hint

    dest_city = _extract_city_for_transport(destination) or destination

    resp = _call_fliggy("search_domestic_train", {
        "origin": departure,
        "destination": dest_city,
        "depDate": parsed_date,
        "limit": 8,
    })

    if isinstance(resp, dict) and resp.get("error"):
        return f"查询火车票失败：{resp['error']}"

    text = _parse_train_data(resp, departure, dest_city, parsed_date)
    if text:
        return text
    return f"未查到{departure}→{dest_city}（{parsed_date}）的火车票，可能该路线无直达或中转，建议搜索机票"


# ============ 工具3：去目的地机票 ============
def search_flight(params):
    """去目的地机票：查询到旅游目的地的航班机票，含直达和中转方案。"""
    departure = params.get("departure", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "明天")

    if not departure:
        return "请提供出发城市，如：上海、北京"
    if not destination:
        return "请提供旅游目的地，如：三亚、丽江"

    parsed_date, date_hint = _smart_parse_date(dep_date)
    if not parsed_date:
        return date_hint

    dest_city = _extract_city_for_transport(destination) or destination

    resp = _call_fliggy("search_flight", {
        "origin": departure,
        "destination": dest_city,
        "depDate": parsed_date,
    })

    if isinstance(resp, dict) and resp.get("error"):
        return f"查询机票失败：{resp['error']}"

    text = _parse_flight_data(resp, departure, dest_city, parsed_date)
    if text:
        return text
    return f"未查到{departure}→{dest_city}（{parsed_date}）的航班，建议搜索火车票"


# ============ 入口 ============
TOOLS = {
    "search_tour": search_tour,
    "search_train": search_train,
    "search_flight": search_flight,
}


def run(tool_name, params_json):
    """技能入口"""
    tool = TOOLS.get(tool_name)
    if not tool:
        return json.dumps({"error": f"未知工具: {tool_name}"}, ensure_ascii=False)
    try:
        if isinstance(params_json, str):
            params = json.loads(params_json)
        else:
            params = params_json or {}
        result = tool(params)
        return result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        print(run(sys.argv[1], sys.argv[2]))
    else:
        print("用法: python group_tour.py <tool_name> <params_json>")
