#!/usr/bin/env python3
"""
今日国内油价查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询各省市 92/95/98 号汽油、0 号柴油价格

用法:
    python oil_price.py [--city 北京]

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_OIL_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_OIL_KEY=your_api_key
    3. 直接传参: python oil_price.py --key your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/540
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://apis.juhe.cn/gnyj/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/540"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_OIL_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_OIL_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def query_oil_price(api_key: str) -> dict:
    """查询全国油价"""
    params = {"key": api_key}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    if data.get("error_code") == 0:
        result = data.get("result") or []
        if isinstance(result, list):
            return {"success": True, "data": result}
        return {"success": True, "data": []}

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"

    return {
        "success": False,
        "error_code": error_code,
        "reason": f"{reason}{hint}",
    }


def filter_by_city(data: list, city_keyword: str) -> list:
    """按省市名称筛选（模糊匹配）"""
    if not city_keyword:
        return data
    keyword = city_keyword.strip()
    return [item for item in data if keyword in item.get("city", "")]


def format_table_output(data: list) -> None:
    """以表格形式输出油价"""
    if not data:
        print("暂无油价数据")
        return

    headers = ["省份/城市", "92号汽油", "95号汽油", "98号汽油", "0号柴油"]
    rows = []
    for item in data:
        rows.append([
            item.get("city", "-"),
            item.get("92h", "-"),
            item.get("95h", "-"),
            item.get("98h", "-"),
            item.get("0h", "-"),
        ])

    col_widths = [10, 10, 10, 10, 10]
    for row in rows:
        for i, cell in enumerate(row):
            width = sum(2 if ord(c) > 127 else 1 for c in str(cell))
            col_widths[i] = max(col_widths[i], width)

    def pad(text, width):
        actual = sum(2 if ord(c) > 127 else 1 for c in str(text))
        return str(text) + " " * max(0, width - actual)

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_row = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"

    print("⛽ 今日国内油价（单位：元/升）\n")
    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        print("| " + " | ".join(pad(cell, col_widths[i]) for i, cell in enumerate(row)) + " |")
    print(sep)


def main():
    args = sys.argv[1:]
    cli_key = None
    city_filter = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--city", "-c") and i + 1 < len(args):
            city_filter = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        i += 1

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_OIL_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_OIL_KEY=your_api_key")
        print("   3. 命令行参数: python oil_price.py --key your_api_key")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_oil_price(api_key)

    if not result["success"]:
        print(f"❌ {result.get('reason', result.get('error', '查询失败'))}")
        sys.exit(1)

    data = result.get("data", [])
    if city_filter:
        data = filter_by_city(data, city_filter)
        if not data:
            print(f"未找到与「{city_filter}」匹配的油价数据")
            sys.exit(0)

    format_table_output(data)
    print()
    print(json.dumps({"success": True, "data": data}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
