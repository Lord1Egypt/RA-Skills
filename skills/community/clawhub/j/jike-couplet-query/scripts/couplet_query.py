#!/usr/bin/env python3
"""
中文对联查询 - 即刻数据 Skill 脚本。

功能说明：
1. 支持关键词查询和随机返回两类能力。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/couplet/query` 和 `/v1/couplet/random` 接口。
4. 将列表结果整理为表格输出，适合 AI 客户端直接展示。
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
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {"query": "/v1/couplet/query", "random": "/v1/couplet/random"}
APPKEY_ENV_NAMES = ("JIKE_COUPLET_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
TITLE = "中文对联查询 - 即刻数据"
FAIL_TITLE = "中文对联查询失败"
ROW_FIELDS = [('upper_couplet', '上联'), ('lower_couplet', '下联')]
QUERY_REQUIRES_PAGE = False


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取查询接口需要的 AppKey。
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
    1. 解析查询和随机子命令参数。
    2. `query` 用于按关键词搜索，`random` 用于随机返回结果。
    3. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)
    query_parser = subparsers.add_parser("query", help="关键词查询")
    query_parser.add_argument("--keyword", required=True, help="关键词")
    if QUERY_REQUIRES_PAGE:
        query_parser.add_argument("--page", default="1", help="页码，默认 1")
        query_parser.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")
    subparsers.add_parser("random", help="随机返回结果")
    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_positive_int(value: str, field_name: str, max_value: int | None = None) -> str:
    """
    功能说明：
    1. 校验分页参数必须为正整数。
    2. `page_size` 按接口文档限制最大 50。
    3. 返回字符串，保持传给接口的参数格式和文档一致。

    @param value 用户输入值
    @param field_name 字段名称，用于错误提示
    @param max_value 最大允许值
    @return string 校验后的正整数字符串
    @raises ValueError 参数非法时抛出
    """
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} 必须是正整数") from exc
    if number < 1:
        raise ValueError(f"{field_name} 必须大于 0")
    if max_value and number > max_value:
        raise ValueError(f"{field_name} 不能超过 {max_value}")
    return str(number)


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令组装接口业务参数。
    2. 查询接口传入关键词和可选分页参数。
    3. 随机接口不传业务参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "random":
        return {}
    params = {"keyword": args.keyword.strip()}
    if QUERY_REQUIRES_PAGE:
        params["page"] = normalize_positive_int(args.page, "page")
        params["page_size"] = normalize_positive_int(args.page_size, "page_size", 50)
    return params


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择对应接口。
    2. 自动追加 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param command query 或 random
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
    3. 用于表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def truncate(value: Any, max_width: int = 54) -> str:
    """
    功能说明：
    1. 将长文本裁剪为列表摘要。
    2. 避免答案类字段过长导致终端刷屏。
    3. JSON 输出仍保留完整接口内容。

    @param value 原始值
    @param max_width 最大展示宽度
    @return string 裁剪后的文本
    """
    text = str(value or "-").replace("\n", " ").strip()
    current = 0
    chars = []
    for char in text:
        width = 2 if unicodedata.east_asian_width(char) in ("F", "W") else 1
        if current + width > max_width:
            chars.append("...")
            break
        chars.append(char)
        current += width
    return "".join(chars) or "-"


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证多列文本输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出查询结果表格。
    2. 自动计算列宽。
    3. 用于关键词查询和随机结果展示。

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


def get_items(data: Any) -> tuple[list[dict[str, Any]], int]:
    """
    功能说明：
    1. 兼容分页结构和数组结构两种接口返回。
    2. 分页结构读取 `data.data` 和 `data.total`。
    3. 数组结构直接作为结果列表。

    @param data 接口 data 字段
    @return tuple 结果列表和总数
    """
    if isinstance(data, dict):
        items = data.get("data") or []
        return items, int(data.get("total") or len(items))
    if isinstance(data, list):
        return data, len(data)
    return [], 0


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 将接口返回结果输出为表格。
    2. 成功时按 ROW_FIELDS 配置展示核心字段。
    3. 失败时展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print(f"\n{FAIL_TITLE}\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    items, total = get_items(payload.get("data"))
    rows = []
    for item in items:
        if not isinstance(item, dict):
            rows.append([truncate(item, 80)])
            continue
        rows.append([truncate(item.get(field), 54) for field, _ in ROW_FIELDS])
    headers = [label for _, label in ROW_FIELDS] if rows and len(rows[0]) > 1 else ["结果"]
    title = "随机结果" if command == "random" else "查询结果"
    print(f"\n{TITLE} 中文对联查询 - 即刻数据  共 {total} 条\n")
    print_table(headers, rows)
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
        print(f"错误: 未找到 AppKey，请先配置环境变量 {APPKEY_ENV_NAMES[0]} 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
