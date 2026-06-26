#!/usr/bin/env python3
"""
航班查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
通过出发地、目的地、出发日期查询航班信息

用法:
    python flight_query.py --departure BJS --arrival SHA --date 2025-06-18

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python flight_query.py --key your_api_key ...
    2. 环境变量：export JUHE_FLIGHT_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_FLIGHT_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/818
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

API_URL = "https://apis.juhe.cn/flight/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/818"

# 常用机场代码映射
AIRPORTS = {
    "BJS": "北京",
    "PEK": "北京首都",
    "PKX": "北京大兴",
    "SHA": "上海",
    "PVG": "上海浦东",
    "CAN": "广州",
    "SZX": "深圳",
    "CTU": "成都",
    "TFU": "成都天府",
    "KMG": "昆明",
    "XIY": "西安",
    "HGH": "杭州",
    "NKG": "南京",
    "WUH": "武汉",
    "TSN": "天津",
    "CGO": "郑州",
    "TAO": "青岛",
    "TNA": "济南",
    "DLC": "大连",
    "SHE": "沈阳",
    "HRB": "哈尔滨",
    "CGQ": "长春",
    "FOC": "福州",
    "XMN": "厦门",
    "NNN": "南宁",
    "KWL": "桂林",
    "SYX": "三亚",
    "HAK": "海口",
    "LHW": "兰州",
    "INC": "银川",
    "XNN": "西宁",
    "URC": "乌鲁木齐",
    "LXA": "拉萨",
    "KWE": "贵阳",
    "CKG": "重庆",
    "NGB": "宁波",
    "WUX": "无锡",
    "CSX": "长沙",
    "HFE": "合肥",
    "SJW": "石家庄",
    "TYN": "太原",
    "HET": "呼和浩特",
    "BAV": "包头",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_FLIGHT_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_FLIGHT_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_date(date_str: str) -> bool:
    """验证日期格式（yyyy-MM-dd）"""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_str))


def validate_airport_code(code: str) -> bool:
    """验证机场代码（3 位大写字母）"""
    pattern = r"^[A-Z]{3}$"
    return bool(re.match(pattern, code))


def query_flights(departure: str, arrival: str, departure_date: str, api_key: str = None) -> dict:
    """查询航班"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "departure": departure,
        "arrival": arrival,
        "departureDate": departure_date,
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "orderid": res.get("orderid", ""),
            "flightInfo": res.get("flightInfo", []),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def get_airport_name(code: str) -> str:
    """获取机场名称"""
    return AIRPORTS.get(code, code)


def format_flight_info(flight: dict, index: int = 0) -> str:
    """格式化单个航班信息"""
    lines = []

    airline_name = flight.get("airlineName", "")
    flight_no = flight.get("flightNo", "")

    lines.append(f"✈️ 航班 {index + 1}")
    lines.append("")

    if airline_name:
        lines.append(f"航空公司：{airline_name}")
    if flight_no:
        lines.append(f"航班号：{flight_no}")

    departure_name = flight.get("departureName", "")
    departure = flight.get("departure", "")
    departure_time = flight.get("departureTime", "")
    departure_date = flight.get("departureDate", "")

    if departure_name or departure:
        lines.append(f"出发：{departure_name} ({departure})")
    if departure_date:
        lines.append(f"出发日期：{departure_date}")
    if departure_time:
        lines.append(f"起飞时间：{departure_time}")

    arrival_name = flight.get("arrivalName", "")
    arrival = flight.get("arrival", "")
    arrival_time = flight.get("arrivalTime", "")
    arrival_date = flight.get("arrivalDate", "")

    if arrival_name or arrival:
        lines.append(f"到达：{arrival_name} ({arrival})")
    if arrival_date:
        lines.append(f"到达日期：{arrival_date}")
    if arrival_time:
        lines.append(f"到达时间：{arrival_time}")

    duration = flight.get("duration", "")
    if duration:
        lines.append(f"飞行时长：{duration}")

    transfer_num = flight.get("transferNum", 0)
    if transfer_num == 0:
        lines.append("中转：直飞")
    else:
        lines.append(f"中转：{transfer_num}次")

    ticket_price = flight.get("ticketPrice", 0)
    if ticket_price:
        lines.append(f"机票价格：¥{ticket_price}")

    # 显示航段信息
    segments = flight.get("segments", [])
    if segments and len(segments) > 1:
        lines.append("")
        lines.append("航段详情:")
        for i, seg in enumerate(segments):
            seg_airline = seg.get("airlineName", "")
            seg_flight = seg.get("flightNo", "")
            seg_dep = seg.get("departureName", "")
            seg_arr = seg.get("arrivalName", "")
            seg_time = seg.get("departureTime", "")
            arr_time = seg.get("arrivalTime", "")
            flight_time = seg.get("flightTime", "")

            lines.append(f"  航段 {i+1}: {seg_flight} {seg_dep}({seg_time}) → {seg_arr}({arr_time}) [飞行{flight_time}]")

    return "\n".join(lines)


def format_result(result: dict, departure: str, arrival: str, date: str) -> str:
    """格式化查询结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    lines = []
    lines.append(f"✈️ 航班查询结果")
    lines.append("")
    lines.append(f"出发地：{get_airport_name(departure)} ({departure})")
    lines.append(f"目的地：{get_airport_name(arrival)} ({arrival})")
    lines.append(f"出发日期：{date}")
    lines.append("")

    flight_info = result.get("flightInfo", [])
    if not flight_info:
        return "\n".join(lines) + "⚠️ 暂未查询到航班信息"

    lines.append(f"共找到 {len(flight_info)} 个航班:\n")

    for i, flight in enumerate(flight_info):
        lines.append(format_flight_info(flight, i))
        lines.append("")
        lines.append("—" * 50)
        lines.append("")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    departure = None
    arrival = None
    date = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--departure" and i + 1 < len(args):
            departure = args[i + 1].upper()
            i += 2
        elif args[i] == "--arrival" and i + 1 < len(args):
            arrival = args[i + 1].upper()
            i += 2
        elif args[i] == "--date" and i + 1 < len(args):
            date = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python flight_query.py --departure 出发地 --arrival 目的地 --date 日期 [--key API_KEY]")
            print("")
            print("选项:")
            print("  --departure DEP  出发地机场三字代码（必填），如 BJS(北京)、SHA(上海)、CAN(广州)")
            print("  --arrival ARR    目的地机场三字代码（必填），如 BJS、SHA、CAN")
            print("  --date DATE      出发日期，格式：yyyy-MM-dd（必填）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("常用机场代码:")
            print("  BJS-北京  SHA-上海  CAN-广州  SZX-深圳  CTU-成都")
            print("  KMG-昆明  XIY-西安  HGH-杭州  NKG-南京  WUH-武汉")
            print("")
            print("示例:")
            print("  python flight_query.py --departure BJS --arrival SHA --date 2025-06-18")
            print("  python flight_query.py --departure CAN --arrival BJS --date 2025-06-20")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    # 参数验证
    if not departure:
        print("错误：缺少必填参数 --departure")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not arrival:
        print("错误：缺少必填参数 --arrival")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not date:
        print("错误：缺少必填参数 --date")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not validate_airport_code(departure):
        print(f"错误：出发地代码格式错误 '{departure}'，请输入 3 位大写字母（如 BJS）")
        sys.exit(1)

    if not validate_airport_code(arrival):
        print(f"错误：目的地代码格式错误 '{arrival}'，请输入 3 位大写字母（如 SHA）")
        sys.exit(1)

    if not validate_date(date):
        print(f"错误：日期格式错误 '{date}'，请使用 yyyy-MM-dd 格式")
        sys.exit(1)

    if departure == arrival:
        print("错误：出发地和目的地不能相同")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_FLIGHT_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_FLIGHT_KEY=your_api_key")
        print("   3. 命令行参数：python flight_query.py --key your_api_key --departure BJS --arrival SHA --date 2025-06-18")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_flights(departure, arrival, date, api_key)
    print(format_result(result, departure, arrival, date))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
