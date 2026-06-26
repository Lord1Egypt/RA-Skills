#!/usr/bin/env python3
"""
即刻数据国内油价实时查询 Skill 脚本。

功能说明：
1. 支持按省份查询油价，也支持不传省份返回全部地区油价。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/petrol/query` 查询 92/95/98 号汽油和 0 号柴油价格。
4. 将结果整理为表格输出，适合 AI 客户端直接展示。
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
API_PATH = "/v1/petrol/query"
APPKEY_ENV_NAMES = ("JIKE_PETROL_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取国内油价查询需要的 AppKey。
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
    1. 解析国内油价查询参数。
    2. `--province` 可选，不传时返回全部地区油价。
    3. 支持 `--json` 输出接口原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="国内油价实时查询 - 即刻数据")
    parser.add_argument("--province", default="", help="省份名称，不传返回全部，例如 四川")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于油价表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证省份和油价字段对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出国内油价表格。
    2. 自动计算列宽。
    3. 展示省份、更新时间、92/95/98 号汽油和 0 号柴油价格。

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


def request_api(province: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据国内油价实时查询接口。
    2. 省份参数可为空；为空时返回全部地区油价。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param province 省份名称，可为空
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    params = {"appkey": appkey}
    if province:
        params["province"] = province
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def print_text_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出国内油价查询结果。
    2. 成功时将数组结果整理为表格。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n⛽ 国内油价查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    rows = []
    for item in payload.get("data") or []:
        rows.append([
            item.get("province"),
            f"{item.get('date') or '-'} {item.get('time') or ''}".strip(),
            item.get("petrol_92"),
            item.get("petrol_95"),
            item.get("petrol_98"),
            item.get("diesel_0"),
        ])

    print("\n⛽ 国内油价实时查询结果\n")
    print_table(["省份", "更新时间", "92汽油", "95汽油", "98汽油", "0号柴油"], rows)
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_PETROL_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(args.province.strip(), appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
