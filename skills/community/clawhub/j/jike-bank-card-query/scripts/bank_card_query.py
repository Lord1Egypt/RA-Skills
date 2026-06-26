#!/usr/bin/env python3
"""
即刻数据银行卡类型及真伪查询 Skill 脚本。

功能说明：
1. 支持银行卡类型及真伪查询，也支持查询银行列表。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/bank/card/query` 和 `/v1/bank/query` 接口。
4. 默认对银行卡号脱敏，避免在 AI 客户端输出完整敏感信息。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {
    "card": "/v1/bank/card/query",
    "list": "/v1/bank/query",
}
APPKEY_ENV_NAMES = ("JIKE_BANK_CARD_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取银行卡查询需要的 AppKey。
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
    1. 解析银行卡查询子命令参数。
    2. `card` 用于查询银行卡类型、卡名称、发卡行等信息。
    3. `list` 用于查询支持的银行列表。
    4. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="银行卡类型及真伪查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    card_parser = subparsers.add_parser("card", help="银行卡类型及真伪查询")
    card_parser.add_argument("--bank-card", required=True, help="银行卡号，长度 14-19 位；最后四位可用 1111 代替")
    card_parser.add_argument("--no-mask", action="store_true", help="展示完整银行卡号，默认脱敏")

    list_parser = subparsers.add_parser("list", help="查询银行列表")
    list_parser.add_argument("--bank-name", required=True, help="银行名称关键词，例如 工商")
    list_parser.add_argument("--bank-type", required=True, help="银行类别，例如 大型国有银行")
    list_parser.add_argument("--page", default="1", help="页码，默认 1")
    list_parser.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于银行列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证银行列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出银行列表表格。
    2. 自动计算表头和数据列宽。
    3. 表格用于展示银行名称、简称、类别、官网和客服电话。

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


def validate_bank_card(bank_card: str) -> str:
    """
    功能说明：
    1. 校验银行卡号是否为 14-19 位数字。
    2. 支持接口文档约定的最后四位使用 1111 代替。
    3. 返回清理后的银行卡号字符串。

    @param bank_card 用户输入的银行卡号
    @return string 清理后的银行卡号
    @raises ValueError 格式不合法时抛出
    """
    value = re.sub(r"\s+", "", bank_card.strip())
    if not re.fullmatch(r"\d{14,19}", value):
        raise ValueError("银行卡号需为 14-19 位数字，最后四位可用 1111 代替")
    return value


def mask_bank_card(bank_card: str) -> str:
    """
    功能说明：
    1. 默认对银行卡号中间部分脱敏。
    2. 保留前 6 位和后 4 位，便于用户识别卡 BIN 和尾号。
    3. 避免 AI 客户端输出完整敏感卡号。

    @param bank_card 银行卡号
    @return string 脱敏后的银行卡号
    """
    if len(bank_card) <= 10:
        return bank_card
    return bank_card[:6] + "*" * (len(bank_card) - 10) + bank_card[-4:]


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择银行卡接口。
    2. 自动追加 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param command 子命令 card 或 list
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


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令构造接口参数。
    2. `card` 校验银行卡号。
    3. `list` 传入银行名称、银行类别和分页参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "card":
        return {"bank_card": validate_bank_card(args.bank_card)}

    return {
        "bank_name": args.bank_name.strip(),
        "bank_type": args.bank_type.strip(),
        "page": args.page,
        "page_size": args.page_size,
    }


def print_card_result(payload: dict[str, Any], no_mask: bool) -> int:
    """
    功能说明：
    1. 输出银行卡类型及真伪查询结果。
    2. 默认脱敏展示银行卡号。
    3. 展示 Luhn 支持、卡类型、卡名称、卡 BIN、发卡行、官网和客服电话。

    @param payload 接口返回数据
    @param no_mask 是否展示完整银行卡号
    @return int 进程退出码
    """
    data = payload.get("data") or {}
    bank_card = data.get("bank_card") or ""
    print("\n💳 银行卡类型及真伪查询结果\n")
    print(f"  卡号:     {bank_card if no_mask else mask_bank_card(bank_card)}")
    print(f"  Luhn校验: {data.get('is_luhn')}")
    print(f"  卡类型:   {data.get('card_type') or '-'}")
    print(f"  卡名称:   {data.get('card_name') or '-'}")
    print(f"  卡BIN:    {data.get('card_bin') or '-'}")
    print(f"  卡长度:   {data.get('card_digits') or '-'}")
    print(f"  发卡行:   {data.get('bank_name') or '-'}")
    print(f"  英文简称: {data.get('bank_abbr') or '-'}")
    print(f"  官网:     {data.get('bank_weburl') or '-'}")
    print(f"  客服:     {data.get('bank_tel') or '-'}")
    return 0


def print_list_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出银行列表查询结果。
    2. 展示分页信息和银行条目表格。
    3. 表格字段包含银行名称、英文简称、类别、官网和客服电话。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    data = payload.get("data") or {}
    rows = []
    for item in data.get("data") or []:
        rows.append([item.get("bank_name"), item.get("bank_abbr"), item.get("bank_type"), item.get("bank_tel"), item.get("bank_weburl")])

    print(f"\n🏦 银行列表  第 {data.get('current_page', '-')} / {data.get('last_page', '-')} 页，共 {data.get('total', 0)} 条\n")
    print_table(["银行名称", "简称", "类别", "客服电话", "官网"], rows)
    return 0


def print_text_result(args: argparse.Namespace, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据接口 code 判断查询是否成功。
    2. 按 card/list 子命令选择展示逻辑。
    3. 失败时展示接口 message，便于用户修正卡号、银行名称或 AppKey。

    @param args argparse 解析结果
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n💳 银行卡查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    if args.command == "card":
        return print_card_result(payload, args.no_mask)
    return print_list_result(payload)


def main() -> int:
    args = parse_args(sys.argv[1:])
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_BANK_CARD_QUERY_KEY 或 JIKE_APPKEY")
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

    return print_text_result(args, payload)


if __name__ == "__main__":
    raise SystemExit(main())
