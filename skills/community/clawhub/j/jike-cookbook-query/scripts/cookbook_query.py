#!/usr/bin/env python3
"""
即刻数据菜谱查询 Skill 脚本。

功能说明：
1. 支持食材列表、菜谱搜索、菜谱详情和随机菜谱四类查询。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/cookbook/ingredient`、`/v1/cookbook/search`、`/v1/cookbook/detail`、`/v1/cookbook/random` 接口。
4. 将菜谱名称、做法步骤、主料辅料等信息整理为适合 AI 客户端展示的文本。
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
API_PATH_MAP = {
    "ingredient": "/v1/cookbook/ingredient",
    "search": "/v1/cookbook/search",
    "detail": "/v1/cookbook/detail",
    "random": "/v1/cookbook/random",
}
APPKEY_ENV_NAMES = ("JIKE_COOKBOOK_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取菜谱查询需要的 AppKey。
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
    1. 解析菜谱查询子命令参数。
    2. `ingredient` 查询食材列表，`search` 搜索菜谱，`detail` 查询菜谱详情，`random` 随机菜谱。
    3. `--json` 支持放在子命令前或子命令后。
    4. 分页参数保持接口原名 `page`、`page_size`，便于和 OpenAPI 文档对应。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="菜谱查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingredient_parser = subparsers.add_parser("ingredient", help="获取食材列表")
    ingredient_parser.add_argument("--keyword", default="", help="食材关键词，例如 鸡蛋")
    ingredient_parser.add_argument("--page", default="1", help="页码，默认 1")
    ingredient_parser.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    search_parser = subparsers.add_parser("search", help="通过名称搜索菜谱")
    search_parser.add_argument("--keyword", default="", help="菜谱关键词，例如 西红柿炒鸡蛋")
    search_parser.add_argument("--page", default="1", help="页码，默认 1")
    search_parser.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    detail_parser = subparsers.add_parser("detail", help="根据 ID 查询菜谱详情")
    detail_parser.add_argument("--id", required=True, help="菜谱 ID，例如 6")

    subparsers.add_parser("random", help="随机返回 10 个菜谱")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于食材和菜谱列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def truncate(value: Any, max_width: int = 32) -> str:
    """
    功能说明：
    1. 将长文本裁剪到指定展示宽度。
    2. 菜谱描述和做法可能很长，列表页只展示摘要。
    3. 详情页再输出完整步骤，避免列表刷屏。

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
    3. 保证列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出食材或菜谱列表表格。
    2. 自动计算列宽。
    3. 用于 AI 客户端快速展示多条结果。

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


def normalize_page(value: str, field_name: str, max_value: int | None = None) -> str:
    """
    功能说明：
    1. 校验分页参数必须为正整数。
    2. `page_size` 按接口文档限制最大 50。
    3. 返回字符串，保持传给接口的参数格式和文档一致。

    @param value 用户输入分页值
    @param field_name 字段名称，用于错误提示
    @param max_value 最大允许值
    @return string 校验后的分页值
    @raises ValueError 分页值非法时抛出
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
    1. 根据菜谱子命令构造接口参数。
    2. 列表类接口透传关键词和分页参数。
    3. 详情接口只传菜谱 ID，随机接口不传业务参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command in {"ingredient", "search"}:
        return {
            "keyword": args.keyword.strip(),
            "page": normalize_page(args.page, "page"),
            "page_size": normalize_page(args.page_size, "page_size", 50),
        }
    if args.command == "detail":
        return {"id": normalize_page(args.id, "id")}
    return {}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择菜谱接口。
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


def format_ingredients(items: Any) -> str:
    """
    功能说明：
    1. 将主料或辅料数组格式化为中文列表。
    2. 接口字段包含用量、食材 ID 和食材名称，展示时优先展示名称和用量。
    3. 空数组返回 `-`，避免详情页出现空白。

    @param items 接口返回的食材数组
    @return string 食材展示文本
    """
    if not isinstance(items, list) or not items:
        return "-"
    values = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("ingredients_name") or item.get("name") or "-"
        usage = item.get("usage") or "适量"
        values.append(f"{name}({usage})")
    return "、".join(values) or "-"


def print_recipe_detail(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出单个菜谱详情。
    2. 展示菜名、分类、耗时、口味、烹饪方式、主料辅料。
    3. 按步骤输出做法，方便 AI 客户端直接给用户操作指引。

    @param data 菜谱详情数据
    @return void
    """
    print(f"  ID:     {data.get('id') or '-'}")
    print(f"  菜名:   {data.get('name') or '-'}")
    print(f"  菜系:   {data.get('cuisine') or '-'}")
    print(f"  类型:   {data.get('type') or '-'}")
    print(f"  耗时:   {data.get('prep_time') or '-'}")
    print(f"  口味:   {data.get('taste') or '-'}")
    print(f"  做法:   {data.get('cooking_method') or '-'}")
    print(f"  主料:   {format_ingredients(data.get('main_ingredients'))}")
    print(f"  辅料:   {format_ingredients(data.get('secondary_ingredients'))}")
    print("\n  步骤:")
    for step in data.get("method") or []:
        if not isinstance(step, dict):
            continue
        print(f"  {step.get('step') or '-'}. {step.get('content') or '-'}")


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据子命令输出不同类型的菜谱结果。
    2. 列表类接口输出表格，详情接口输出完整做法。
    3. 失败时统一展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n菜谱查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data")
    if command == "detail":
        print("\n菜谱详情查询结果\n")
        print_recipe_detail(data or {})
        return 0

    if command == "ingredient":
        page_data = data or {}
        rows = [[item.get("id"), item.get("name"), item.get("type"), truncate(item.get("desc"), 42)] for item in page_data.get("data") or []]
        print(f"\n食材列表查询结果  共 {page_data.get('total') or len(rows)} 条\n")
        print_table(["ID", "食材", "类型", "简介"], rows)
        return 0

    items = data if isinstance(data, list) else (data or {}).get("data") or []
    rows = [[item.get("id"), item.get("name"), item.get("type"), item.get("prep_time"), item.get("taste"), item.get("cooking_method")] for item in items]
    title = "随机菜谱查询结果" if command == "random" else f"菜谱搜索结果  共 {(data or {}).get('total') or len(rows)} 条"
    print(f"\n{title}\n")
    print_table(["ID", "菜名", "类型", "耗时", "口味", "做法"], rows)
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
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_COOKBOOK_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
