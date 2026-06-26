#!/usr/bin/env python3
"""
节假日安排查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询指定日期的节假日信息、调休安排、农历信息等

用法:
    python holiday_query.py --date 2025-05-01
    python holiday_query.py --date 2025-05-01 --detail

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python holiday_query.py --key your_api_key --date 2025-05-01
    2. 环境变量：export JUHE_DATE_HOLIDAY_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_DATE_HOLIDAY_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/606
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

API_URL = "http://apis.juhe.cn/fapig/calendar/day"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/606"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_DATE_HOLIDAY_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_DATE_HOLIDAY_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_date(date_str: str) -> bool:
    """验证日期格式（yyyy-MM-dd）"""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date_str))


def query_holiday(date: str, api_key: str = None) -> dict:
    """查询节假日信息"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    if not date:
        return {"success": False, "error": "未提供日期"}

    params = {
        "key": api_key,
        "date": date,
        "detail": 1,
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "date": res.get("date", ""),
            "week": res.get("week", ""),
            "status": res.get("status"),
            "statusDesc": res.get("statusDesc", ""),
            "lunarYear": res.get("lunarYear", ""),
            "lunarMonth": res.get("lunarMonth", ""),
            "lunarDate": res.get("lunarDate", ""),
            "animal": res.get("animal", ""),
            "suit": res.get("suit", ""),
            "avoid": res.get("avoid", ""),
            "term": res.get("term", ""),
            "desc": res.get("desc", ""),
            "gzYear": res.get("gzYear", ""),
            "gzMonth": res.get("gzMonth", ""),
            "gzDate": res.get("gzDate", ""),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_status(status, status_desc: str) -> str:
    """格式化节假日状态"""
    if status == 1:
        return f"🎉 {status_desc}（法定节假日）"
    elif status == 2:
        return f"💼 {status_desc}（调休上班）"
    else:
        return f"📅 {status_desc}"


def format_result(result: dict, detail: bool = False) -> str:
    """格式化查询结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    lines = []
    date = result.get("date", "")
    week = result.get("week", "")
    status = result.get("status")
    status_desc = result.get("statusDesc", "")

    lines.append(f"📅 {date} 节假日查询结果")
    lines.append("")
    lines.append(f"日期：{date}")
    lines.append(f"星期：{week}")
    lines.append(f"状态：{format_status(status, status_desc)}")

    if detail:
        lunar_year = result.get("lunarYear", "")
        lunar_month = result.get("lunarMonth", "")
        lunar_date = result.get("lunarDate", "")
        animal = result.get("animal", "")

        if lunar_year and lunar_month and lunar_date:
            lines.append(f"农历：{lunar_year}年 {lunar_month}月 {lunar_date}")
        if animal:
            lines.append(f"生肖：{animal}")

        gz_year = result.get("gzYear", "")
        gz_month = result.get("gzMonth", "")
        gz_date = result.get("gzDate", "")
        if gz_year and gz_month and gz_date:
            lines.append(f"干支：{gz_year}年 {gz_month}月 {gz_date}日")

        term = result.get("term", "")
        if term:
            lines.append(f"节气：{term}")

        desc = result.get("desc", "")
        if desc:
            lines.append(f"说明：{desc}")

        suit = result.get("suit", "")
        avoid = result.get("avoid", "")

        if suit:
            # 简化显示宜忌
            suit_items = suit.split(".")[:5]  # 只显示前 5 项
            lines.append(f"宜：{' '.join(suit_items)}")
        if avoid:
            avoid_items = avoid.split(".")[:5]  # 只显示前 5 项
            lines.append(f"忌：{' '.join(avoid_items)}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    date = None
    detail = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--date" and i + 1 < len(args):
            date = args[i + 1]
            i += 2
        elif args[i] == "--detail":
            detail = True
            i += 1
        elif args[i] in ("--help", "-h"):
            print("用法：python holiday_query.py --date 日期 [--detail] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --date DATE      查询日期，格式：yyyy-MM-dd（必填）")
            print("  --detail         显示详细信息（农历、黄历宜忌等）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python holiday_query.py --date 2025-05-01")
            print("  python holiday_query.py --date 2025-05-01 --detail")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not date:
        print("错误：缺少必填参数 --date")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not validate_date(date):
        print(f"错误：日期格式错误 '{date}'，请使用 yyyy-MM-dd 格式")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_DATE_HOLIDAY_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_DATE_HOLIDAY_KEY=your_api_key")
        print("   3. 命令行参数：python holiday_query.py --key your_api_key --date 2025-05-01")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_holiday(date, api_key)
    print(format_result(result, detail))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
