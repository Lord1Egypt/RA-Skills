#!/usr/bin/env python3
"""
即刻数据新华字典 Skill 脚本。

功能说明：
1. 支持拼音列表、部首列表、按拼音查汉字、按部首查汉字、汉字详情查询。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/character/pinyin`、`/v1/character/radicals`、`/v1/character/pinyin/query`、`/v1/character/radicals/query`、`/v1/character/chinese/detail` 接口。
4. 将汉字、拼音、部首、笔画、结构、繁体、同义反义等信息整理为可读文本。
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
    "pinyin-list": "/v1/character/pinyin",
    "radicals-list": "/v1/character/radicals",
    "pinyin": "/v1/character/pinyin/query",
    "radicals": "/v1/character/radicals/query",
    "detail": "/v1/character/chinese/detail",
}
APPKEY_ENV_NAMES = ("JIKE_CHARACTER_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取新华字典查询需要的 AppKey。
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
    1. 解析新华字典子命令参数。
    2. `pinyin-list` 和 `radicals-list` 返回基础列表。
    3. `pinyin`、`radicals`、`detail` 分别按拼音、部首、单字查询。
    4. `--limit` 只控制文本展示数量，不影响 JSON 输出。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="新华字典 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    parser.add_argument("--limit", default="30", help="文本输出最多展示数量，默认 30")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("pinyin-list", help="拼音列表")
    subparsers.add_parser("radicals-list", help="部首列表")
    pinyin_parser = subparsers.add_parser("pinyin", help="拼音查询汉字")
    pinyin_parser.add_argument("--pinyin", required=True, help="带声调拼音，例如 yī")
    radicals_parser = subparsers.add_parser("radicals", help="部首查询汉字")
    radicals_parser.add_argument("--radicals", required=True, help="部首，例如 口")
    detail_parser = subparsers.add_parser("detail", help="汉字详细信息")
    detail_parser.add_argument("--char", required=True, help="单个汉字，例如 好")
    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_limit(value: str) -> int:
    """
    功能说明：
    1. 校验文本展示数量必须为正整数。
    2. 避免拼音列表、部首列表一次性刷屏。
    3. 返回整数供文本输出截断使用。

    @param value 用户输入 limit
    @return int 展示数量
    @raises ValueError limit 非法时抛出
    """
    try:
        limit = int(value)
    except ValueError as exc:
        raise ValueError("limit 必须是正整数") from exc
    if limit < 1:
        raise ValueError("limit 必须大于 0")
    return limit


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令构造接口参数。
    2. 基础列表接口不传业务参数。
    3. 查询类接口传入拼音、部首或汉字。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "pinyin":
        return {"pinyin": args.pinyin.strip()}
    if args.command == "radicals":
        return {"radicals": args.radicals.strip()}
    if args.command == "detail":
        char = args.char.strip()
        if len(char) != 1:
            raise ValueError("char 必须是单个汉字，例如 好")
        return {"char": char}
    return {}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择新华字典接口。
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
    3. 用于汉字列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证汉字列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出汉字查询结果表格。
    2. 自动计算列宽。
    3. 用于拼音和部首查询结果展示。

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


def join_value(value: Any) -> str:
    """
    功能说明：
    1. 将数组或普通字段统一转换成展示文本。
    2. 拼音、同义词、反义词等数组用顿号连接。
    3. 空值统一展示为 `-`。

    @param value 接口字段值
    @return string 展示文本
    """
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item) or "-"
    return str(value or "-")


def print_text_result(command: str, payload: dict[str, Any], limit: int) -> int:
    """
    功能说明：
    1. 根据子命令输出新华字典结果。
    2. 列表类输出前 limit 条，详情类输出核心字段。
    3. 失败时展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @param limit 文本展示数量
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n新华字典查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data")
    print("\n新华字典查询结果\n")
    if command in {"pinyin-list", "radicals-list"}:
        items = data or []
        print(f"  总数: {len(items)}")
        print("  结果: " + "、".join(str(item) for item in items[:limit]))
        return 0
    if command in {"pinyin", "radicals"}:
        items = data or []
        rows = [[item.get("char"), item.get("radicals"), item.get("strokes"), join_value(item.get("pinyin")), item.get("structure")] for item in items[:limit]]
        print(f"  总数: {len(items)}，展示前 {min(limit, len(items))} 条\n")
        print_table(["汉字", "部首", "笔画", "拼音", "结构"], rows)
        return 0
    detail = data or {}
    print(f"  汉字:   {detail.get('char') or '-'}")
    print(f"  拼音:   {join_value(detail.get('pinyin'))}")
    print(f"  部首:   {detail.get('radicals') or '-'}")
    print(f"  笔画:   {detail.get('strokes') or '-'}")
    print(f"  结构:   {detail.get('structure') or '-'}")
    print(f"  繁体:   {detail.get('traditional') or '-'}")
    print(f"  异体字: {join_value(detail.get('variant'))}")
    print(f"  同义词: {join_value(detail.get('synonyms'))}")
    print(f"  反义词: {join_value(detail.get('antonyms'))}")
    print(f"  形近字: {join_value(detail.get('likeness'))}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        limit = normalize_limit(args.limit)
        params = build_params(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_CHARACTER_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload, limit)


if __name__ == "__main__":
    raise SystemExit(main())
