#!/usr/bin/env python3
"""
即刻数据上海黄金交易所行情 Skill 脚本。

功能说明：
1. 按日期查询上海黄金交易所历史行情。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用 `/v1/gold/shgold/history` 接口。
4. 将品种、开盘价、最高价、最低价、收盘价、涨跌幅、成交量等字段整理为表格。
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
API_PATH = "/v1/gold/shgold/history"
APPKEY_ENV_NAMES = ("JIKE_GOLD_SHGOLD_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取上海黄金交易所行情查询需要的 AppKey。
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
    1. 解析上海黄金交易所行情查询参数。
    2. `--date` 为必填日期，格式 `YYYY-MM-DD`。
    3. 支持 `--json` 输出接口原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="上海黄金交易所行情 - 即刻数据")
    parser.add_argument("--date", required=True, help="日期，格式 YYYY-MM-DD，例如 2024-05-20")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_date(date_value: str) -> str:
    """
    功能说明：
    1. 校验日期格式是否为 `YYYY-MM-DD`。
    2. 使用标准日期解析避免无效日期进入接口。
    3. 返回清理后的日期字符串。

    @param date_value 用户输入日期
    @return string 合法日期字符串
    @raises ValueError 日期格式非法时抛出
    """
    value = date_value.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期格式必须为 YYYY-MM-DD，例如 2024-05-20") from exc
    return value


def request_api(date_value: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用上海黄金交易所历史行情接口。
    2. 使用 date 和 appkey 查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param date_value 查询日期
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode({'date': date_value, 'appkey': appkey})}"
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
    3. 用于行情表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证行情表格输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出行情列表表格。
    2. 自动计算列宽。
    3. 用于展示不同黄金品种的历史行情。

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


def print_text_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出上海黄金交易所行情查询结果。
    2. 成功时按品种展示开盘、最高、最低、收盘、涨跌幅、成交量。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n上海黄金交易所行情查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    rows = []
    for item in payload.get("data") or []:
        rows.append([
            item.get("date"), item.get("type"), item.get("opening_price"), item.get("max_price"), item.get("min_price"),
            item.get("closing_price"), item.get("change_price"), item.get("change_rate"), item.get("trading_volume"),
        ])
    print("\n上海黄金交易所行情查询结果\n")
    print_table(["日期", "品种", "开盘", "最高", "最低", "收盘", "涨跌", "涨跌幅", "成交量"], rows)
    print("\n  提示: 行情数据仅用于信息查询，不构成投资建议。")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        date_value = validate_date(args.date)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_GOLD_SHGOLD_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(date_value, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
