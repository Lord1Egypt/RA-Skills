#!/usr/bin/env python3
"""
即刻数据成语词典 Skill 脚本。

功能说明：
1. 支持搜索成语、查询成语详情、随机成语和成语接龙。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/idiom/query`、`/v1/idiom/detail`、`/v1/idiom/random`、`/v1/idiom/last_word` 接口。
4. 将拼音、解释、出处、用法、近义词、反义词和接龙结果整理为可读文本。
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
    "search": "/v1/idiom/query",
    "detail": "/v1/idiom/detail",
    "random": "/v1/idiom/random",
    "last-word": "/v1/idiom/last_word",
}
APPKEY_ENV_NAMES = ("JIKE_IDIOM_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取成语词典查询需要的 AppKey。
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
    1. 解析成语词典子命令参数。
    2. `search` 搜索成语，`detail` 查询详情，`random` 随机成语，`last-word` 查询成语接龙。
    3. `--json` 支持放在子命令前或子命令后。
    4. 参数名称尽量保持和接口文档一致，方便后期维护。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="成语词典 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="搜索成语")
    search_parser.add_argument("--keyword", default="", help="成语关键词，例如 一心")
    search_parser.add_argument("--page", default="1", help="页码，默认 1")
    search_parser.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    detail_parser = subparsers.add_parser("detail", help="成语详情")
    detail_parser.add_argument("--id", required=True, help="成语 ID，例如 320")

    subparsers.add_parser("random", help="随机返回 10 个成语")

    last_word_parser = subparsers.add_parser("last-word", help="成语接龙")
    last_word_parser.add_argument("--keyword", required=True, help="查询的成语，例如 比翼双飞")
    last_word_parser.add_argument("--size", default="10", help="返回数量，默认 10")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于成语列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def truncate(value: Any, max_width: int = 40) -> str:
    """
    功能说明：
    1. 将解释、出处等长文本裁剪为列表摘要。
    2. 避免搜索结果输出过长影响 AI 客户端阅读。
    3. 详情查询仍展示完整字段。

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
    3. 保证成语列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出成语列表表格。
    2. 自动计算列宽。
    3. 用于搜索、随机和接龙结果展示。

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


def normalize_positive_int(value: str, field_name: str, max_value: int | None = None) -> str:
    """
    功能说明：
    1. 校验分页、ID、返回数量等参数必须为正整数。
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
    1. 根据成语子命令构造接口参数。
    2. 搜索接口传入关键词和分页，详情接口传入 ID，接龙接口传入成语和数量。
    3. 随机接口不需要业务参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "search":
        return {
            "keyword": args.keyword.strip(),
            "page": normalize_positive_int(args.page, "page"),
            "page_size": normalize_positive_int(args.page_size, "page_size", 50),
        }
    if args.command == "detail":
        return {"id": normalize_positive_int(args.id, "id")}
    if args.command == "last-word":
        return {"keyword": args.keyword.strip(), "size": normalize_positive_int(args.size, "size", 50)}
    return {}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择成语接口。
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


def join_words(value: Any) -> str:
    """
    功能说明：
    1. 将近义词、反义词等数组字段转换为中文顿号分隔文本。
    2. 空数组返回 `-`。
    3. 避免详情页输出 Python 列表格式。

    @param value 接口字段值
    @return string 展示文本
    """
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item) or "-"
    return str(value or "-")


def print_detail(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出成语详情。
    2. 展示成语、拼音、解释、出处、例句、故事、用法、近义词和反义词。
    3. 用于用户询问“某个成语是什么意思/出处是什么”的场景。

    @param data 成语详情数据
    @return void
    """
    print(f"  ID:     {data.get('id') or '-'}")
    print(f"  成语:   {data.get('word') or '-'}")
    print(f"  拼音:   {data.get('pinyin') or '-'}")
    print(f"  缩写:   {data.get('abbr') or '-'}")
    print(f"  解释:   {data.get('explanation') or '-'}")
    print(f"  出处:   {data.get('source_book') or '-'} {data.get('source_text') or ''}".rstrip())
    print(f"  例句:   {data.get('example_book') or '-'} {data.get('example_text') or ''}".rstrip())
    print(f"  故事:   {data.get('story') or '-'}")
    print(f"  用法:   {data.get('usage') or '-'}")
    print(f"  近义词: {join_words(data.get('similar'))}")
    print(f"  反义词: {join_words(data.get('opposite'))}")


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据子命令输出不同类型的成语结果。
    2. 搜索和随机输出表格，详情输出完整字段，接龙输出可接成语列表。
    3. 失败时统一展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n成语词典查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data")
    if command == "detail":
        print("\n成语详情查询结果\n")
        print_detail(data or {})
        return 0

    if command == "last-word":
        items = (data or {}).get("data") or []
        rows = [[item.get("id"), item.get("word")] for item in items]
        print(f"\n成语接龙查询结果  尾字：{(data or {}).get('last_word') or '-'}，共 {(data or {}).get('total_count') or len(rows)} 条\n")
        print_table(["ID", "成语"], rows)
        return 0

    items = data if isinstance(data, list) else (data or {}).get("data") or []
    rows = [[item.get("id"), item.get("word"), item.get("pinyin"), truncate(item.get("explanation"), 44)] for item in items]
    title = "随机成语查询结果" if command == "random" else f"成语搜索结果  共 {(data or {}).get('total') or len(rows)} 条"
    print(f"\n{title}\n")
    print_table(["ID", "成语", "拼音", "解释"], rows)
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
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_IDIOM_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
