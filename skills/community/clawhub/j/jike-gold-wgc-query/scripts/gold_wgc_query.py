#!/usr/bin/env python3
"""
即刻数据国际实时金价 Skill 脚本。

功能说明：
1. 支持世界黄金协会最新金价和历史金价查询。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/gold/wgc/latest` 和 `/v1/gold/wgc/history` 接口。
4. 将重量单位、币种、价格日期和更新时间整理为可读文本。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {"latest": "/v1/gold/wgc/latest", "history": "/v1/gold/wgc/history"}
APPKEY_ENV_NAMES = ("JIKE_GOLD_WGC_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取国际金价查询需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取业务环境变量或通用 `JIKE_APPKEY`。
    4. 最后读取脚本目录 `.env` 文件。

    @param cli_key 命令行传入的 AppKey
    @return string AppKey，未找到时返回空字符串
    """
    if cli_key:
        return cli_key.strip()
    for env_name in APPKEY_ENV_NAMES:
        env_value = os.environ.get(env_name, "").strip()
        if env_value:
            return env_value
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return ""
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() in APPKEY_ENV_NAMES:
            value = value.strip().strip('"').strip("'")
            if value:
                return value
    return ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    功能说明：
    1. 解析国际金价子命令参数。
    2. `latest` 查询最新价格，`history` 查询历史价格。
    3. 历史接口支持按日期、重量单位和币种过滤。
    4. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="国际实时金价 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("latest", help="世界黄金协会最新价格")
    history = subparsers.add_parser("history", help="世界黄金协会历史价格")
    history.add_argument("--date", default="", help="日期，格式 YYYY-MM-DD；不传默认最新一天")
    history.add_argument("--weight-unit", default="grams,oz", help="重量单位，英文逗号拼接，例如 grams,oz")
    history.add_argument("--currency", default="cny,usd", help="货币代码，英文逗号拼接，例如 cny,usd")
    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令构造国际金价接口参数。
    2. 最新价格接口不需要业务参数。
    3. 历史价格接口可传日期、重量单位和币种筛选。

    @param args argparse 解析结果
    @return dict 接口业务参数
    @raises ValueError 日期格式非法时抛出
    """
    if args.command == "latest":
        return {}
    params = {}
    if args.date.strip():
        try:
            datetime.strptime(args.date.strip(), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("date 格式必须为 YYYY-MM-DD，例如 2025-04-28") from exc
        params["date"] = args.date.strip()
    if args.weight_unit.strip():
        params["weight_unit"] = args.weight_unit.strip()
    if args.currency.strip():
        params["currency"] = args.currency.strip()
    return params


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择国际金价接口。
    2. 自动追加 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param command 子命令名称
    @param params 接口业务参数
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH_MAP[command]}?{urllib.parse.urlencode({**params, 'appkey': appkey})}"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于价格表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证国际金价表格输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出国际金价表格。
    2. 自动计算列宽。
    3. 按重量单位和币种展示价格。

    @param headers 表头列表
    @param rows 表格数据列表
    @return void
    """
    widths = [display_width(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], display_width(str(value or "-")))
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    print(border)
    print("| " + " | ".join(pad_cell(header, widths[index]) for index, header in enumerate(headers)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(pad_cell(value, widths[index]) for index, value in enumerate(row)) + " |")
    print(border)


def build_price_rows(prices: dict[str, Any]) -> list[list[Any]]:
    """
    功能说明：
    1. 将接口 prices 多层结构转换成表格行。
    2. 第一层是重量单位，第二层是货币代码。
    3. 输出时统一展示为“重量单位 / 币种 / 价格”。

    @param prices 接口 prices 字段
    @return list 表格行
    """
    rows = []
    for weight_unit, currency_map in (prices or {}).items():
        if not isinstance(currency_map, dict):
            continue
        for currency, price in currency_map.items():
            rows.append([weight_unit, currency.upper(), price])
    return rows


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出国际金价查询结果。
    2. 最新价格展示 price_date 和 updated，历史价格展示 date。
    3. 失败时展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n国际金价查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data") or {}
    print("\n国际金价查询结果\n")
    if command == "latest":
        print(f"  价格时间: {data.get('price_date') or '-'}")
        print(f"  更新时间: {data.get('updated') or '-'}\n")
    else:
        print(f"  日期: {data.get('date') or '-'}\n")
    print_table(["重量单位", "币种", "价格"], build_price_rows(data.get("prices") or {}))
    print("\n  提示: 行情数据仅用于信息查询，不构成投资建议。")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        params = build_params(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_GOLD_WGC_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
