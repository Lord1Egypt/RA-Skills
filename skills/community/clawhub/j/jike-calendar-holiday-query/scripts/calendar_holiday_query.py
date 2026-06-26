#!/usr/bin/env python3
"""
即刻数据节假日查询 Skill 脚本。

功能说明：
1. 支持查询某天是否放假或调休、某月假期、某年假期。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/calendar/holiday/day`、`/v1/calendar/holiday/month`、`/v1/calendar/holiday/year` 接口。
4. 将假期名称、是否工作日、调休目标日期整理为可读文本。
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
API_PATH_MAP = {
    "day": "/v1/calendar/holiday/day",
    "month": "/v1/calendar/holiday/month",
    "year": "/v1/calendar/holiday/year",
}
APPKEY_ENV_NAMES = ("JIKE_CALENDAR_HOLIDAY_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取节假日查询需要的 AppKey。
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
    1. 解析节假日查询子命令参数。
    2. `day` 查询单日，`month` 查询月份，`year` 查询年份。
    3. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="节假日查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)
    day_parser = subparsers.add_parser("day", help="日期是否放假或调休")
    day_parser.add_argument("--day", required=True, help="阳历日期，格式 YYYY-MM-DD，例如 2021-06-14")
    month_parser = subparsers.add_parser("month", help="查询月份假期")
    month_parser.add_argument("--month", required=True, help="月份，格式 YYYY-MM，例如 2021-06")
    year_parser = subparsers.add_parser("year", help="查询年份假期")
    year_parser.add_argument("--year", required=True, help="年份，例如 2021")
    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def validate_args(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令校验日期、月份或年份格式。
    2. 日格式为 `YYYY-MM-DD`，月格式为 `YYYY-MM`，年格式为 4 位数字。
    3. 返回接口需要的业务参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    @raises ValueError 参数格式非法时抛出
    """
    if args.command == "day":
        try:
            datetime.strptime(args.day.strip(), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("day 格式必须为 YYYY-MM-DD，例如 2021-06-14") from exc
        return {"day": args.day.strip()}
    if args.command == "month":
        try:
            datetime.strptime(args.month.strip(), "%Y-%m")
        except ValueError as exc:
            raise ValueError("month 格式必须为 YYYY-MM，例如 2021-06") from exc
        return {"month": args.month.strip()}
    year = args.year.strip()
    if not year.isdigit() or len(year) != 4:
        raise ValueError("year 格式必须为 4 位年份，例如 2021")
    return {"year": year}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择节假日接口。
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
    3. 用于假期列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证节假日列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出假期列表表格。
    2. 自动计算列宽。
    3. 用于月份和年份假期结果展示。

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


def format_work(value: Any) -> str:
    """
    功能说明：
    1. 将接口中的 is_work 布尔字段转换为中文。
    2. True 表示工作日或调休上班，False 表示放假。
    3. 空值展示为 `-`。

    @param value 接口 is_work 字段
    @return string 中文说明
    """
    if value is True:
        return "上班/调休"
    if value is False:
        return "放假"
    return "-"


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据子命令输出节假日结果。
    2. 单日查询输出日期、名称、是否工作日和调休目标。
    3. 月份/年份查询输出假期列表表格。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n节假日查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data")
    print("\n节假日查询结果\n")
    if command == "day":
        data = data or {}
        print(f"  日期: {data.get('date') or '-'}")
        print(f"  名称: {data.get('name') or '-'}")
        print(f"  状态: {format_work(data.get('is_work'))}")
        print(f"  目标: {data.get('target') or '-'}")
        return 0
    rows = []
    for item in data or []:
        rows.append([item.get("date"), item.get("name"), format_work(item.get("is_work")), item.get("target") or "-"])
    print(f"  共 {len(rows)} 条\n")
    print_table(["日期", "名称", "状态", "目标日期"], rows)
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        params = validate_args(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_CALENDAR_HOLIDAY_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
