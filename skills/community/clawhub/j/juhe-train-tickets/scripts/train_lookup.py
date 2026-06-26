#!/usr/bin/env python3
"""
火车票时刻表查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询指定出发站到到达站的火车班次、时刻、票价信息

用法:
    python train_lookup.py <出发站> <到达站> <日期>
    python train_lookup.py 北京 上海 2026-03-25
    python train_lookup.py 北京 上海 2026-03-25 --filter G
    python train_lookup.py 北京 上海 2026-03-25 --time 上午 --price

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_TRAIN_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_TRAIN_KEY=your_api_key
    3. 直接传参: python train_lookup.py --key your_api_key 北京 上海 2026-03-25

免费申请 API Key: https://www.juhe.cn/docs/api/id/817
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta

API_URL = "https://apis.juhe.cn/fapigw/train/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/817"

VALID_FILTERS = {"G", "D", "Z", "T", "K", "O", "F", "S"}
VALID_TIME_RANGES = {"凌晨", "上午", "下午", "晚上"}

FILTER_DESC = {
    "G": "高铁/城际",
    "D": "动车",
    "Z": "直达特快",
    "T": "特快",
    "K": "快速",
    "O": "其他",
    "F": "复兴号",
    "S": "智能动车组",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_TRAIN_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_TRAIN_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_date(date_str: str) -> str | None:
    """验证日期格式并检查是否在15天内，返回错误描述或 None"""
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return f"日期格式错误，请使用 YYYY-MM-DD 格式，例如：{datetime.now().strftime('%Y-%m-%d')}"

    today = datetime.now().date()
    if target < today:
        return f"日期 {date_str} 已过期，请查询今天或未来的日期"
    if target > today + timedelta(days=15):
        return f"日期 {date_str} 超出可查询范围（仅支持 15 天内），最远可查询至 {(today + timedelta(days=15)).strftime('%Y-%m-%d')}"
    return None


def query_trains(
    departure: str,
    arrival: str,
    date: str,
    api_key: str,
    filter_types: str = "",
    time_range: str = "",
    enable_booking: str = "1",
) -> dict:
    """调用聚合数据 API 查询列车时刻"""
    params = {
        "key": api_key,
        "search_type": "1",
        "departure_station": departure,
        "arrival_station": arrival,
        "date": date,
        "filter": filter_types,
        "enable_booking": enable_booking,
        "departure_time_range": time_range,
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    error_code = data.get("error_code", -1)
    if error_code == 0:
        return {"success": True, "trains": data.get("result", [])}

    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}"
    elif error_code == 10012:
        hint = "\n   今日免费调用次数已用尽，请升级套餐"
    elif error_code == 281701:
        hint = "\n   站点名称可能有误，或该日期/路线暂无可用班次"

    return {
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def format_flags(flags: list) -> str:
    """格式化列车标签"""
    if not flags:
        return ""
    return " ".join(f"[{f}]" for f in flags)


def format_price_detail(prices: list) -> str:
    """格式化票价信息（单行）"""
    if not prices:
        return ""
    parts = []
    for p in prices:
        seat = p.get("seat_name", "")
        price = p.get("price", "")
        num = p.get("num", "")
        if price:
            num_str = f"({num}张)" if num and num != "无" and num != "-" else ""
            parts.append(f"{seat}: ¥{price}{num_str}")
    return "  |  ".join(parts) if parts else ""


def print_train_table(trains: list, show_price: bool = False) -> None:
    """以表格形式输出班次列表"""
    if not trains:
        print("  （无符合条件的班次）")
        return

    if show_price:
        for t in trains:
            flags_str = format_flags(t.get("train_flags", []))
            flags_display = f"  {flags_str}" if flags_str else ""
            print(
                f"  🚄 {t['train_no']:6s}  "
                f"{t['departure_station']} {t['departure_time']} → "
                f"{t['arrival_station']} {t['arrival_time']}  "
                f"历时: {t['duration']}  "
                f"{'✓ 可订' if t.get('enable_booking') == 'Y' else '✗ 不可订'}"
                f"{flags_display}"
            )
            price_str = format_price_detail(t.get("prices", []))
            if price_str:
                print(f"         {price_str}")
        return

    headers = ["车次", "出发站", "出发时间", "到达站", "到达时间", "历时", "可预订", "标签"]

    rows = []
    for t in trains:
        flags_str = " ".join(t.get("train_flags", []))
        rows.append([
            t.get("train_no", ""),
            t.get("departure_station", ""),
            t.get("departure_time", ""),
            t.get("arrival_station", ""),
            t.get("arrival_time", ""),
            t.get("duration", ""),
            "✓" if t.get("enable_booking") == "Y" else "✗",
            flags_str,
        ])

    col_widths = []
    for i, h in enumerate(headers):
        col_widths.append(sum(2 if ord(c) > 127 else 1 for c in h))
    for row in rows:
        for i, cell in enumerate(row):
            width = sum(2 if ord(c) > 127 else 1 for c in str(cell))
            col_widths[i] = max(col_widths[i], width)

    def pad(text, width):
        actual = sum(2 if ord(c) > 127 else 1 for c in str(text))
        return str(text) + " " * max(0, width - actual)

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_row = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        print("| " + " | ".join(pad(cell, col_widths[i]) for i, cell in enumerate(row)) + " |")
    print(sep)


def parse_args(args: list) -> dict:
    """解析命令行参数"""
    result = {
        "cli_key": None,
        "departure": None,
        "arrival": None,
        "date": None,
        "filter": "",
        "time": "",
        "show_price": False,
        "show_all": False,
        "error": None,
    }

    i = 0
    positional = []

    while i < len(args):
        arg = args[i]
        if arg == "--key":
            if i + 1 < len(args):
                result["cli_key"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --key 后需要提供 API Key 值"
                return result
        elif arg == "--filter":
            if i + 1 < len(args):
                result["filter"] = args[i + 1].upper()
                i += 2
            else:
                result["error"] = "错误: --filter 后需要提供车次类型代码（如：G、D、GD）"
                return result
        elif arg == "--time":
            if i + 1 < len(args):
                result["time"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --time 后需要提供时段（凌晨/上午/下午/晚上）"
                return result
        elif arg == "--price":
            result["show_price"] = True
            i += 1
        elif arg == "--all":
            result["show_all"] = True
            i += 1
        else:
            positional.append(arg)
            i += 1

    if len(positional) < 3:
        result["error"] = (
            "错误: 需要提供出发站、到达站和日期\n"
            f"用法: python train_lookup.py [--key KEY] <出发站> <到达站> <日期> [选项]\n"
            f"示例: python train_lookup.py 北京 上海 {datetime.now().strftime('%Y-%m-%d')}\n"
            f"\n免费申请 API Key: {REGISTER_URL}"
        )
        return result

    result["departure"] = positional[0]
    result["arrival"] = positional[1]
    result["date"] = positional[2]

    if result["filter"]:
        invalid = [c for c in result["filter"] if c not in VALID_FILTERS]
        if invalid:
            result["error"] = (
                f"错误: 无效的车次类型代码 {''.join(invalid)}，"
                f"可用代码: {', '.join(sorted(VALID_FILTERS))}"
            )
            return result

    if result["time"] and result["time"] not in VALID_TIME_RANGES:
        result["error"] = (
            f"错误: 无效的时段 '{result['time']}'，"
            f"可用时段: {', '.join(VALID_TIME_RANGES)}"
        )
        return result

    return result


def main():
    args = sys.argv[1:]

    if not args:
        today = datetime.now().strftime("%Y-%m-%d")
        print("用法: python train_lookup.py [--key KEY] <出发站> <到达站> <日期> [选项]")
        print(f"示例: python train_lookup.py 北京 上海 {today}")
        print(f"      python train_lookup.py 广州 深圳 {today} --filter G --time 上午 --price")
        print(f"\n选项:")
        print(f"  --filter <代码>  车次类型筛选（G=高铁, D=动车, Z=直达特快, T=特快, K=快速）")
        print(f"  --time   <时段>  出发时段筛选（凌晨/上午/下午/晚上）")
        print(f"  --price          显示各坐席票价详情")
        print(f"  --all            显示所有班次（含不可预订）")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    parsed = parse_args(args)
    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_TRAIN_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_TRAIN_KEY=your_api_key")
        print("   3. 命令行参数: python train_lookup.py --key your_api_key <出发站> <到达站> <日期>")
        print(f"\n免费申请 Key（每天300次免费调用）: {REGISTER_URL}")
        sys.exit(1)

    date_err = validate_date(parsed["date"])
    if date_err:
        print(f"❌ {date_err}")
        sys.exit(1)

    departure = parsed["departure"]
    arrival = parsed["arrival"]
    date = parsed["date"]
    filter_types = parsed["filter"]
    time_range = parsed["time"]
    show_price = parsed["show_price"]
    enable_booking = "2" if parsed["show_all"] else "1"

    filter_desc = ""
    if filter_types:
        descs = [FILTER_DESC.get(c, c) for c in filter_types]
        filter_desc = f"  车型: {'/'.join(descs)}"
    time_desc = f"  时段: {time_range}" if time_range else ""
    booking_desc = "  含不可预订" if parsed["show_all"] else ""

    print(f"\n🚄 查询 {departure} → {arrival}  日期: {date}{filter_desc}{time_desc}{booking_desc}\n")

    result = query_trains(
        departure=departure,
        arrival=arrival,
        date=date,
        api_key=api_key,
        filter_types=filter_types,
        time_range=time_range,
        enable_booking=enable_booking,
    )

    if not result["success"]:
        print(f"❌ 查询失败: {result['error']}")
        sys.exit(1)

    trains = result["trains"]
    count = len(trains)

    if count == 0:
        print("未找到符合条件的班次。")
        print("建议：")
        print("  · 检查站点名称是否正确（如：北京南、上海虹桥）")
        print("  · 尝试去掉 --filter 或 --time 参数放宽筛选条件")
        print("  · 添加 --all 参数查看不可预订的班次")
        sys.exit(0)

    print(f"共找到 {count} 个班次：\n")
    print_train_table(trains, show_price=show_price)
    print()

    if not show_price and trains:
        print("提示：添加 --price 参数可查看各坐席票价详情")


if __name__ == "__main__":
    main()
