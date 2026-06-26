# -*- coding: utf-8 -*-
"""全球航班查询与预订 - 航班搜索+性价比标签+座位余量+行李额度"""
import argparse, json, re, sys, urllib.request, urllib.error
from datetime import datetime

# ===== 代理配置 =====
PROXY_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

# ===== 中文城市→代码映射（100+城市）=====
CITY_CODE_MAP = {
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "成都": "CTU", "杭州": "HGH", "南京": "NKG", "武汉": "WUH",
    "长沙": "CSX", "重庆": "CKG", "西安": "SIA", "厦门": "XMN",
    "青岛": "TAO", "大连": "DLC", "昆明": "KMG", "丽江": "LJG",
    "桂林": "KWL", "苏州": "SZV", "珠海": "ZUH", "海口": "HAK",
    "三亚": "SYX", "天津": "TSN", "济南": "TNA", "沈阳": "SHE",
    "哈尔滨": "HRB", "长春": "CGQ", "郑州": "CGO", "合肥": "HFE",
    "福州": "FOC", "南昌": "KHN", "太原": "TYN", "石家庄": "SJW",
    "贵阳": "KWE", "南宁": "NNG", "兰州": "LHW", "银川": "INC",
    "呼和浩特": "HET", "乌鲁木齐": "URC", "拉萨": "LXA",
    "无锡": "WUX", "宁波": "NGB", "温州": "WNZ", "烟台": "YNT",
    "威海": "WEH", "佛山": "FUO", "东莞": "DGM", "中山": "ZGN",
    "扬州": "YTY", "大理": "DLU", "西双版纳": "JHG",
    "张家界": "DYG", "九寨沟": "JZH", "黄山": "TXN",
    "洛阳": "LYA", "敦煌": "DNH",
    "香港": "HKG", "澳门": "MFM", "台北": "TPE", "高雄": "KHH",
    "台南": "TNN", "台中": "TXG", "花莲": "HUN",
    "东京": "NRT", "大阪": "OSA", "京都": "OSA", "冲绳": "OKA",
    "北海道": "SPK", "福冈": "FUK", "名古屋": "NGO", "札幌": "SPK",
    "首尔": "SEL", "釜山": "PUS", "济州": "CJU",
    "曼谷": "BKK", "普吉": "HKT", "清迈": "CNX", "芭提雅": "UTP",
    "新加坡": "SIN",
    "吉隆坡": "KUL", "槟城": "PEN", "沙巴": "BKI",
    "河内": "HAN", "胡志明": "SGN", "岘港": "DAD", "芽庄": "CXR",
    "巴厘岛": "DPS", "雅加达": "CGK",
    "马尼拉": "MNL", "长滩岛": "MPH",
    "暹粒": "REP", "仰光": "RGN", "加德满都": "KTM",
    "科伦坡": "CMB", "马累": "MLE",
    "纽约": "NYC", "洛杉矶": "LAX", "旧金山": "SFO", "拉斯维加斯": "LAS",
    "夏威夷": "HNL", "塞班": "SPN", "关岛": "GUM",
    "伦敦": "LON", "巴黎": "PAR", "柏林": "BER", "罗马": "ROM",
    "米兰": "MIL", "巴塞罗那": "BCN", "马德里": "MAD",
    "悉尼": "SYD", "墨尔本": "MEL", "奥克兰": "AKL",
    "迪拜": "DXB", "阿布扎比": "AUH",
    "伊斯坦布尔": "IST", "莫斯科": "MOW",
    "温哥华": "YVR", "多伦多": "YYZ",
    "圣保罗": "GRU", "墨西哥城": "MEX",
    "孟买": "BOM", "新德里": "DEL",
    "开罗": "CAI", "约翰内斯堡": "JNB",
}

CODE_CITY_MAP = {v: k for k, v in CITY_CODE_MAP.items()}

AIRLINE_MAP = {
    "CA": "国航", "MU": "东航", "CZ": "南航", "HU": "海航",
    "9C": "春秋", "HO": "吉祥", "ZH": "深航", "MF": "厦航",
    "SC": "山航", "3U": "川航", "FM": "上航",
    "GS": "天津航", "PN": "西部航", "G5": "华夏航", "EU": "成都航",
    "NS": "河北航", "AQ": "九元航", "KY": "昆明航", "LT": "龙江航",
    "JR": "幸福航", "D7": "首都航", "Y8": "扬子江航", "OQ": "重庆航",
    "TV": "西藏航", "FU": "福航", "RY": "江西航", "GJ": "长龙航",
    "CX": "国泰", "KA": "港龙", "HX": "香港航", "UO": "港快运",
    "NX": "澳航", "BR": "长荣", "CI": "中华航", "AE": "华信", "B7": "立荣",
    "NH": "全日空", "JL": "日航", "GK": "捷星日本", "IJ": "日本春秋", "BC": "天马",
    "KE": "大韩", "OZ": "韩亚", "7C": "济州航", "TW": "德威",
    "TG": "泰航", "FD": "泰亚航", "SL": "泰狮航",
    "SQ": "新航", "TR": "酷航", "MI": "胜安",
    "MH": "马航", "AK": "马亚航",
    "VN": "越航", "VJ": "越捷",
    "GA": "印尼鹰航", "QG": "印尼连城", "JT": "狮航",
    "5J": "宿务航", "PR": "菲航",
    "BA": "英航", "VS": "维珍", "LH": "汉莎", "DE": "神鹰",
    "AF": "法航", "KL": "荷航", "AZ": "意航",
    "EK": "阿联酋", "EY": "阿提哈德", "QR": "卡塔尔",
    "TK": "土航", "SU": "俄航",
    "AA": "美航", "UA": "美联航", "DL": "达美",
    "AC": "加航", "QF": "澳航", "VA": "维珍澳", "NZ": "纽航",
    "QZ": "印尼亚航", "U2": "易捷", "FR": "瑞安", "W6": "维兹",
    "NK": "精神航", "B6": "捷蓝", "F9": "边防航",
}

NON_AIRPORT_KEYWORDS = [
    "火车站", "巴士", "轮渡", "港口", "码头",
    "Ferry", "Bus", "Heliport", "Harbour", "Harbor",
    "空军基地", "Air Force", "Military", "Army",
    "Offline", "OffLine Point", "Closed",
    "直升机", "Helicopter",
]

DOMESTIC_CITY_CODES = set(CITY_CODE_MAP.values()) | {"PEK", "PVG", "PKX", "TFU"}


def call_proxy(api_type, params, timeout=30):
    """调用RG代理，v3.1+代理已自动解包MCP响应，data直接是业务对象"""
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
        data = result.get("data", {})
        error = result.get("error")
        if error:
            return {"error": error}
        if isinstance(data, dict):
            return data
        if isinstance(data, str) and data:
            try:
                return json.loads(data)
            except Exception:
                return {"raw_text": data}
        if not data:
            return {"error": "empty data"}
        return data
    except Exception as e:
        return {"error": str(e)}


def _resolve_city_code(city_input):
    if not city_input:
        return city_input
    if re.match(r'^[A-Z]{2,4}$', city_input.upper()):
        return city_input.upper()
    return CITY_CODE_MAP.get(city_input, city_input)

def _is_domestic(code):
    if not code:
        return False
    return code.upper() in DOMESTIC_CITY_CODES

def _get_airline_name(code):
    if not code:
        return code or ""
    return AIRLINE_MAP.get(code.upper(), code)

def _is_civil_airport(name):
    if not name:
        return True
    for kw in NON_AIRPORT_KEYWORDS:
        if kw.lower() in name.lower():
            return False
    return True

def _format_duration(minutes):
    try:
        minutes = int(minutes) if minutes else 0
        if minutes <= 0:
            return ""
        h, m = divmod(minutes, 60)
        return f"{h}h{m}m" if m else f"{h}h"
    except (ValueError, TypeError):
        return str(minutes) if minutes else ""

def _format_time(dt_str):
    try:
        return dt_str[11:16] if len(dt_str) >= 16 else dt_str
    except (IndexError, TypeError):
        return str(dt_str) if dt_str else ""

def _format_wait_time(segs):
    if len(segs) < 2:
        return ""
    try:
        arr = datetime.fromisoformat(segs[0].get("arrTime", "").replace("Z", "+00:00"))
        dep = datetime.fromisoformat(segs[1].get("depTime", "").replace("Z", "+00:00"))
        w = int((dep - arr).total_seconds() / 60)
        return _format_duration(w) if w > 0 else ""
    except Exception:
        return ""


# ===== 4个工具函数 =====

def search_flights(from_city, to_city, from_date, from_airport=None, to_airport=None,
                   cabin_grade="ECONOMY", trip_type="ONE_WAY", ret_date=None,
                   adult_number=1, child_number=0):
    resolved_from = _resolve_city_code(from_city)
    resolved_to = _resolve_city_code(to_city)
    if not resolved_from and not from_airport:
        return f"❌ 无法识别出发城市「{from_city}」"
    if not resolved_to and not to_airport:
        return f"❌ 无法识别到达城市「{to_city}」"
    params = {"fromCity": resolved_from or "", "toCity": resolved_to or "",
              "fromDate": from_date, "cabinGrade": cabin_grade,
              "tripType": trip_type, "adultNumber": adult_number, "childNumber": child_number}
    if from_airport: params["fromAirport"] = from_airport.upper()
    if to_airport: params["toAirport"] = to_airport.upper()
    if ret_date: params["retDate"] = ret_date
    data = call_proxy("flight", params)
    return _format_flights(data, from_airport or resolved_from or from_city,
                           to_airport or resolved_to or to_city, resolved_to, to_airport)


def search_airports(keyword):
    resolved = _resolve_city_code(keyword)
    if resolved and resolved != keyword:
        return f"✅「{keyword}」已映射为城市代码 {resolved}，可直接用中文城市名查航班"
    data = call_proxy("flight_airport", {"keyword": keyword})
    return _format_airports(data, keyword)


def check_flight_seats(routing_id):
    if not routing_id:
        return "❌ 请提供routingId（从航班搜索结果获取）"
    data = call_proxy("flight_seats", {"routingId": routing_id})
    return _format_seats(data)


def check_baggage_allowance(routing_id):
    if not routing_id:
        return "❌ 请提供routingId（从航班搜索结果获取）"
    data = call_proxy("flight_baggage", {"routingId": routing_id})
    return _format_baggage(data)


# ===== 格式化 =====

def _format_flights(data, from_label, to_label, to_city="", to_airport=""):
    if isinstance(data, dict) and "error" in data:
        return f"❌ 查询失败: {data['error']}"
    flights = data.get("flightInformationList") if isinstance(data, dict) else None
    if flights is None:
        return "未找到符合条件的航班。建议调整搜索条件或确认城市代码后重试。"
    if not flights:
        route = f" {from_label}→{to_label}" if from_label and to_label else ""
        return f"未找到符合条件的航班{route}。"
    flights.sort(key=lambda x: float(x.get("fromSmartValueScore", 0) or 0), reverse=True)
    top = flights[:10]
    direct = [f for f in top if len(f.get("fromSegments", [])) == 1]
    transfer = [f for f in top if len(f.get("fromSegments", [])) > 1]
    route_info = f" {from_label}→{to_label}" if from_label and to_label else ""
    lines = [f"✈️ 找到 {len(flights)} 个航班方案{route_info}，展示前10：", ""]
    if direct:
        lines += [f"━━━ 直飞航班 ({len(direct)}个) ━━━", ""]
        for i, fl in enumerate(direct, 1): _format_single_flight(lines, i, fl)
    if transfer:
        lines += [f"━━━ 中转航班 ({len(transfer)}个) ━━━", ""]
        for i, fl in enumerate(transfer, 1): _format_single_flight(lines, len(direct) + i, fl)
    lines.append("⚠️ 价格为参考价，以实际下单为准")
    lines.append("💡 可用check_flight_seats查询座位余量，check_baggage_allowance查询行李额度")
    dest_code = to_airport or to_city
    dest_name = CODE_CITY_MAP.get(dest_code, "")
    tips = [f"🏨推荐{dest_name}酒店" if dest_name else "🏨目的地酒店"]
    if _is_domestic(to_city) or _is_domestic(to_airport):
        tips.append(f"🚇{dest_name or dest_code}市内交通")
    lines.append("\n📋 附加服务：" + " | ".join(tips))
    return "\n".join(lines)


def _format_single_flight(lines, idx, fl):
    from_segs = fl.get("fromSegments", [])
    if not from_segs: return
    adult_price = fl.get("totalAdultPrice", "")
    currency = fl.get("currency", "")
    carrier_cn = _get_airline_name(fl.get("validatingCarrier", ""))
    smart_score = float(fl.get("fromSmartValueScore", 0) or 0)
    price_str = f"¥{adult_price}" if adult_price else "价格待查"
    score_label = " 🏆性价比之选" if smart_score >= 80 else ""
    if len(from_segs) == 1:
        seg = from_segs[0]
        lines.append(f"{idx}. {seg.get('flightNumber','')} [{carrier_cn}]{score_label}")
        lines.append(f"   {seg.get('depAirport','')} {_format_time(seg.get('depTime',''))} → {seg.get('arrAirport','')} {_format_time(seg.get('arrTime',''))}（{_format_duration(int(seg.get('duration',0) or 0))}）")
        lines.append(f"   💰 {price_str} {currency}")
        lines.append("")
    else:
        lines.append(f"{idx}. 中转 [{carrier_cn}]{score_label}")
        for j, seg in enumerate(from_segs):
            prefix = "├" if j < len(from_segs) - 1 else "└"
            lines.append(f"   {prefix} 第{j+1}段: {seg.get('flightNumber','')} {seg.get('depAirport','')}{_format_time(seg.get('depTime',''))}→{seg.get('arrAirport','')}{_format_time(seg.get('arrTime',''))}")
        wait = _format_wait_time(from_segs)
        if wait: lines.append(f"   ⏱️ 中转等待{wait}")
        lines.append(f"   💰 {price_str} {currency}")
        lines.append("")


def _format_airports(data, keyword):
    if isinstance(data, dict) and "error" in data:
        return f"❌ 搜索失败: {data['error']}"
    airports = data.get("airPortInformationList") if isinstance(data, dict) else None
    if not airports:
        return f"未找到匹配「{keyword}」的机场或城市。请尝试其他关键词，或直接使用中文城市名查航班。"
    civil = [ap for ap in airports if _is_civil_airport(ap.get("airportName", ""))]
    if not civil:
        return f"未找到匹配「{keyword}」的民用机场。"
    lines = [f"✈️ 找到 {len(civil)} 个结果：", ""]
    for i, ap in enumerate(civil, 1):
        lines.append(f"{i}. {ap.get('airportName','')}（{ap.get('airportCode','')}）")
        parts = []
        if ap.get("cityName"): parts.append(f"城市: {ap['cityName']}（{ap.get('cityCode','')}）")
        if ap.get("countryName"): parts.append(f"国家: {ap['countryName']}")
        if parts: lines.append("   " + " | ".join(parts))
        lines.append("")
    lines.append("💡 cityCode可用于城市级查航班，airportCode可用于精确查航班")
    lines.append("💡 也支持中文城市名直接查航班（如'北京→东京'）")
    return "\n".join(lines)


def _format_seats(data):
    if isinstance(data, dict) and "error" in data:
        return f"❌ 查询失败: {data['error']}"
    if not isinstance(data, dict): return str(data)
    msg = data.get("message", "")
    seats = data.get("flightSeatInfoList") or data.get("seatInformationList")
    if seats:
        lines = ["💺 座位信息：", ""]
        for s in (seats if isinstance(seats, list) else [seats]):
            code = s.get("cabinCode", s.get("cabinClass", ""))
            name = s.get("cabinName", "")
            avail = s.get("seatAvailable", s.get("availableCount", ""))
            price = s.get("price", "")
            line = f"  舱位 {code}（{name}）: 剩余 {avail}"
            if price: line += f" | 价格 ¥{price}"
            lines.append(line)
        return "\n".join(lines)
    if msg: return f"💺 {msg}"
    return json.dumps(data, ensure_ascii=False, indent=2)[:500]


def _format_baggage(data):
    if isinstance(data, dict) and "error" in data:
        return f"❌ 查询失败: {data['error']}"
    if not isinstance(data, dict): return str(data)
    msg = data.get("message", "")
    bags = data.get("baggageInfoList") or data.get("baggageAllowanceList")
    if bags:
        lines = ["🧳 行李额度：", ""]
        for b in (bags if isinstance(bags, list) else [bags]):
            pax = b.get("passengerType", "成人")
            check_in = b.get("checkInBaggage", b.get("checkedBaggage", ""))
            carry_on = b.get("carryOnBaggage", b.get("handBaggage", ""))
            lines.append(f"  {pax}: 托运 {check_in} | 随身 {carry_on}")
        return "\n".join(lines)
    if msg: return f"🧳 {msg}"
    return json.dumps(data, ensure_ascii=False, indent=2)[:500]


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(description="全球航班查询与预订 v1.1.0")
    sub = parser.add_subparsers(dest="command")
    p_flight = sub.add_parser("search", help="搜索航班")
    p_flight.add_argument("--from-city", required=True)
    p_flight.add_argument("--to-city", required=True)
    p_flight.add_argument("--date", required=True)
    p_flight.add_argument("--from-airport")
    p_flight.add_argument("--to-airport")
    p_flight.add_argument("--cabin", default="ECONOMY", choices=["ECONOMY", "BUSINESS", "FIRST"])
    p_flight.add_argument("--trip-type", default="ONE_WAY", choices=["ONE_WAY", "ROUND_TRIP"])
    p_flight.add_argument("--ret-date")
    p_flight.add_argument("--adults", type=int, default=1)
    p_flight.add_argument("--children", type=int, default=0)

    p_airport = sub.add_parser("airport", help="搜索机场/城市代码")
    p_airport.add_argument("--keyword", required=True)

    p_seats = sub.add_parser("seats", help="查询座位余量")
    p_seats.add_argument("--routing-id", required=True)

    p_baggage = sub.add_parser("baggage", help="查询行李额度")
    p_baggage.add_argument("--routing-id", required=True)

    args = parser.parse_args()
    if args.command == "search":
        print(search_flights(args.from_city, args.to_city, args.date,
                             args.from_airport, args.to_airport, args.cabin,
                             args.trip_type, args.ret_date, args.adults, args.children))
    elif args.command == "airport":
        print(search_airports(args.keyword))
    elif args.command == "seats":
        print(check_flight_seats(args.routing_id))
    elif args.command == "baggage":
        print(check_baggage_allowance(args.routing_id))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
