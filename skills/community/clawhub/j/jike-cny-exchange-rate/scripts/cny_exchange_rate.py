#!/usr/bin/env python3
"""
即刻数据人民币汇率查询 Skill 脚本。

功能说明：
1. 支持币种列表、人民币外汇牌价查询、汇率转换三个子命令。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/cny_exchange_rate/currenc_list`、`query`、`convert` 接口。
4. 将结果输出为适合 AI 客户端阅读的文本或 JSON。

调用示例：
    python3 scripts/cny_exchange_rate.py list
    python3 scripts/cny_exchange_rate.py query --currency usd
    python3 scripts/cny_exchange_rate.py convert --from-currency usd --to-currency cny --money 100
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
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {
    "list": "/v1/cny_exchange_rate/currenc_list",
    "query": "/v1/cny_exchange_rate/query",
    "convert": "/v1/cny_exchange_rate/convert",
}
APPKEY_ENV_NAMES = ("JIKE_CNY_EXCHANGE_RATE_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取人民币汇率查询需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取 `JIKE_CNY_EXCHANGE_RATE_KEY` 或通用 `JIKE_APPKEY`。
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
    1. 解析人民币汇率 Skill 的子命令参数。
    2. `list` 查询支持的币种列表。
    3. `query` 查询人民币外汇牌价，可传单个币种。
    4. `convert` 根据源币种、目标币种和金额做汇率转换。
    5. `--json` 支持放在子命令前或子命令后，降低用户使用成本。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="人民币汇率查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="查询支持的外汇币种列表")

    query_parser = subparsers.add_parser("query", help="查询人民币外汇牌价")
    query_parser.add_argument("--currency", default="", help="币种代码，例如 usd；不传返回全部")

    convert_parser = subparsers.add_parser("convert", help="汇率转换")
    convert_parser.add_argument("--from-currency", required=True, help="源货币，例如 usd")
    convert_parser.add_argument("--to-currency", required=True, help="目标货币，例如 cny")
    convert_parser.add_argument("--money", required=True, help="转换金额，单位元，例如 100")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_currency(value: str) -> str:
    """
    功能说明：
    1. 标准化用户输入的币种代码。
    2. 去除首尾空格并转为小写。
    3. 保持与接口文档中的 usd、eur、hkd 等代码一致。

    @param value 用户输入币种代码
    @return string 标准化币种代码
    """
    return value.strip().lower()


def validate_money(value: str) -> str:
    """
    功能说明：
    1. 校验汇率转换金额是否合法。
    2. 使用 Decimal 避免浮点误差。
    3. 金额必须大于 0，校验通过后按原始字符串传给接口。

    @param value 用户输入金额
    @return string 原始金额字符串
    @raises ValueError 金额非法时抛出
    """
    try:
        money = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("金额必须是数字，例如 100") from exc

    if money <= 0:
        raise ValueError("金额必须大于 0")

    return value


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算字符串终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于汇率列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据展示宽度补齐空格。
    3. 避免中文币种名称导致列错位。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出币种列表或外汇牌价表格。
    2. 根据表头和数据自动计算列宽。
    3. 保证 AI 客户端和终端都能清晰阅读。

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


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择人民币汇率接口。
    2. 自动追加 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param command 子命令 list、query、convert
    @param params 接口业务参数
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    request_params = {**params, "appkey": appkey}
    url = f"{API_BASE_URL}{API_PATH_MAP[command]}?{urllib.parse.urlencode(request_params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令构造接口参数。
    2. `query` 只在传入币种时附加 currency 参数。
    3. `convert` 会校验金额并标准化币种代码。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "list":
        return {}

    if args.command == "query":
        currency = normalize_currency(args.currency)
        return {"currency": currency} if currency else {}

    return {
        "from_currency": normalize_currency(args.from_currency),
        "to_currency": normalize_currency(args.to_currency),
        "money": validate_money(args.money),
    }


def print_list_result(data: list[dict[str, Any]]) -> None:
    """
    功能说明：
    1. 输出接口支持的外汇币种列表。
    2. 每行展示币种代码和中文名称。
    3. 便于用户确认 `query` 或 `convert` 可使用的 currency 参数。

    @param data 币种列表
    @return void
    """
    rows = [[item.get("currency"), item.get("currency_name")] for item in data]
    print("\n💱 外汇牌价币种列表\n")
    print_table(["币种", "名称"], rows)


def print_query_result(data: list[dict[str, Any]]) -> None:
    """
    功能说明：
    1. 输出人民币外汇牌价查询结果。
    2. 展示币种、日期时间、现汇/现钞买入价和卖出价。
    3. 适合 AI 客户端解释“人民币兑某币种当前牌价”。

    @param data 外汇牌价列表
    @return void
    """
    rows = []
    for item in data:
        rows.append([
            item.get("currency") or "-",
            item.get("currency_name") or "-",
            f"{item.get('date') or '-'} {item.get('time') or ''}".strip(),
            item.get("spot_buying") or "-",
            item.get("cash_buying") or "-",
            item.get("spot_selling") or "-",
            item.get("cash_selling") or "-",
        ])
    print("\n💱 人民币汇率外汇牌价\n")
    print_table(["币种", "名称", "时间", "现汇买入", "现钞买入", "现汇卖出", "现钞卖出"], rows)


def print_convert_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出汇率转换结果。
    2. 优先展示接口返回的 desc 字段。
    3. 同时展示汇率日期和转换后金额，便于用户判断数据时效。

    @param data 汇率转换结果
    @return void
    """
    print("\n💱 汇率转换结果\n")
    print(f"  日期: {data.get('date') or '-'}")
    print(f"  金额: {data.get('money') or '-'}")
    print(f"  说明: {data.get('desc') or '-'}")


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据接口 code 判断查询是否成功。
    2. 按 list、query、convert 分别调用不同展示逻辑。
    3. 失败时展示接口 message，便于用户检查币种、金额或 AppKey。

    @param command 子命令
    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n💱 人民币汇率查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or ([] if command in ("list", "query") else {})
    if command == "list":
        print_list_result(data)
    elif command == "query":
        print_query_result(data)
    else:
        print_convert_result(data)
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_CNY_EXCHANGE_RATE_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    try:
        params = build_params(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1

    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
