#!/usr/bin/env python3
"""
即刻数据唐诗宋词元曲查询 Skill 脚本。

功能说明：
1. 支持古诗词列表、详情、随机诗词、诗人查询、诗人详情、词牌、朝代、类别和体裁查询。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用 `/v1/poetry/*` 系列接口。
4. 将诗词标题、作者、朝代、正文、译文、注释、赏析等信息整理为可读文本。
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
    "search": "/v1/poetry/query",
    "detail": "/v1/poetry/detail",
    "author": "/v1/poetry/author",
    "author-detail": "/v1/poetry/author/detail",
    "random": "/v1/poetry/random",
    "cipai": "/v1/poetry/cipai",
    "dynasty": "/v1/poetry/dynasty",
    "type": "/v1/poetry/type",
    "format": "/v1/poetry/format",
}
APPKEY_ENV_NAMES = ("JIKE_POETRY_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取诗词查询需要的 AppKey。
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
    1. 解析诗词查询子命令参数。
    2. 搜索类子命令保留接口文档中的筛选字段。
    3. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="唐诗宋词元曲查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="古诗词列表查询")
    for name, help_text in [("name", "诗词名称模糊搜索"), ("author", "诗人名称"), ("dynasty", "朝代"), ("type", "类别"), ("format", "体裁")]:
        search.add_argument("--" + name, default="", help=help_text)
    search.add_argument("--page", default="1", help="页码，默认 1")
    search.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    detail = subparsers.add_parser("detail", help="古诗词详情")
    detail.add_argument("--poetry-id", required=True, help="古诗词 ID，例如 4")

    author = subparsers.add_parser("author", help="诗人查询")
    author.add_argument("--name", default="", help="诗人名称模糊搜索，例如 杜甫")
    author.add_argument("--dynasty", default="", help="朝代，例如 唐代")
    author.add_argument("--page", default="1", help="页码，默认 1")
    author.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    author_detail = subparsers.add_parser("author-detail", help="诗人详情")
    author_detail.add_argument("--name", required=True, help="诗人名字，例如 杜甫")

    subparsers.add_parser("random", help="随机获取古诗词")

    cipai = subparsers.add_parser("cipai", help="词牌信息查询")
    cipai.add_argument("--name", required=True, help="词牌名，例如 水调歌头")
    cipai.add_argument("--page", default="1", help="页码，默认 1")
    cipai.add_argument("--page-size", default="10", help="每页数量，默认 10，最大 50")

    subparsers.add_parser("dynasty", help="朝代列表")
    subparsers.add_parser("type", help="古诗词类别列表")
    subparsers.add_parser("format", help="古诗词体裁列表")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_positive_int(value: str, field_name: str, max_value: int | None = None) -> str:
    """
    功能说明：
    1. 校验分页和 ID 参数必须为正整数。
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
    1. 根据诗词子命令构造接口参数。
    2. 搜索类接口只传非空筛选项。
    3. 列表查询保留 page 和 page_size 分页参数。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "search":
        params = {name: getattr(args, name).strip() for name in ["name", "author", "dynasty", "type", "format"] if getattr(args, name).strip()}
        params["page"] = normalize_positive_int(args.page, "page")
        params["page_size"] = normalize_positive_int(args.page_size, "page_size", 50)
        return params
    if args.command == "detail":
        return {"poetry_id": normalize_positive_int(args.poetry_id, "poetry_id")}
    if args.command == "author":
        params = {name: getattr(args, name).strip() for name in ["name", "dynasty"] if getattr(args, name).strip()}
        params["page"] = normalize_positive_int(args.page, "page")
        params["page_size"] = normalize_positive_int(args.page_size, "page_size", 50)
        return params
    if args.command == "author-detail":
        return {"name": args.name.strip()}
    if args.command == "cipai":
        return {"name": args.name.strip(), "page": normalize_positive_int(args.page, "page"), "page_size": normalize_positive_int(args.page_size, "page_size", 50)}
    return {}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择诗词接口。
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
    3. 用于诗词列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def truncate(value: Any, max_width: int = 48) -> str:
    """
    功能说明：
    1. 将长文本裁剪为列表摘要。
    2. 避免诗词正文、诗人介绍过长导致列表刷屏。
    3. 详情查询仍输出更完整内容。

    @param value 原始值
    @param max_width 最大展示宽度
    @return string 裁剪后的文本
    """
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
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
    3. 保证诗词列表输出对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出诗词列表表格。
    2. 自动计算列宽。
    3. 用于搜索、随机、诗人和词牌结果展示。

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


def join_lines(value: Any) -> str:
    """
    功能说明：
    1. 将诗词正文、译文、注释等数组字段转换为换行文本。
    2. 字符串字段原样返回。
    3. 空值返回 `-`。

    @param value 接口字段值
    @return string 展示文本
    """
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item) or "-"
    return str(value or "-")


def get_items(data: Any) -> tuple[list[Any], int]:
    """
    功能说明：
    1. 兼容分页结构和数组结构两种返回。
    2. 分页结构读取 `data.data` 和 `data.total`。
    3. 数组结构直接返回列表和长度。

    @param data 接口 data 字段
    @return tuple 结果列表和总数
    """
    if isinstance(data, dict):
        items = data.get("data") or []
        return items, int(data.get("total") or len(items))
    if isinstance(data, list):
        return data, len(data)
    return [], 0


def print_poetry_detail(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出单首诗词详情。
    2. 展示标题、作者、朝代、类别、体裁、正文、译文、注释和赏析。
    3. 用于用户询问某首诗完整内容、翻译或赏析的场景。

    @param data 诗词详情数据
    @return void
    """
    print(f"  ID:   {data.get('poetry_id') or '-'}")
    print(f"  题名: {data.get('name') or '-'}")
    print(f"  作者: {data.get('author') or '-'} / {data.get('dynasty') or '-'}")
    print(f"  分类: {data.get('type') or '-'} / {data.get('format') or '-'}")
    print("\n  正文:")
    print(join_lines(data.get("content")))
    print("\n  译文:")
    print(truncate(join_lines(data.get("translate") or data.get("translate_res")), 280))
    print("\n  注释:")
    print(truncate(join_lines(data.get("notes")), 280))
    print("\n  赏析:")
    print(truncate(join_lines(data.get("appreciation") or data.get("appreciation_res")), 280))


def print_author_detail(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出诗人详情。
    2. 展示姓名、朝代、生平简介和主要资料段落摘要。
    3. 避免诗人生平字段过长导致终端刷屏。

    @param data 诗人详情数据
    @return void
    """
    print(f"  姓名: {data.get('name') or '-'}")
    print(f"  朝代: {data.get('dynasty') or '-'}")
    print(f"  生平: {truncate(data.get('lifetime'), 260)}")
    desc = data.get("desc") or []
    for item in desc[:3]:
        if isinstance(item, dict):
            print(f"  {item.get('type') or '资料'}: {truncate(' '.join(item.get('content') or []), 220)}")


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据子命令输出不同类型的诗词结果。
    2. 详情类输出完整字段，列表类输出表格。
    3. 失败时统一展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n诗词查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data")
    if command == "detail":
        print("\n古诗词详情查询结果\n")
        print_poetry_detail(data or {})
        return 0
    if command == "author-detail":
        print("\n诗人详情查询结果\n")
        print_author_detail(data or {})
        return 0
    if command in {"dynasty", "type", "format"}:
        items = data or []
        print(f"\n诗词{command}列表  共 {len(items)} 条\n")
        print("  " + "、".join(str(item) for item in items))
        return 0
    items, total = get_items(data)
    if command == "author":
        rows = [[item.get("name"), item.get("dynasty")] for item in items if isinstance(item, dict)]
        print(f"\n诗人查询结果  共 {total} 条\n")
        print_table(["诗人", "朝代"], rows)
        return 0
    if command == "cipai":
        rows = [[item.get("name"), truncate(item.get("desc"), 80)] for item in items if isinstance(item, dict)]
        print(f"\n词牌查询结果  共 {total} 条\n")
        print_table(["词牌", "说明"], rows)
        return 0
    rows = [[item.get("poetry_id"), item.get("name"), item.get("author"), item.get("dynasty"), truncate(item.get("content"), 56)] for item in items if isinstance(item, dict)]
    title = "随机古诗词" if command == "random" else "古诗词列表"
    print(f"\n{title}查询结果  共 {total} 条\n")
    print_table(["ID", "题名", "作者", "朝代", "正文摘要"], rows)
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
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_POETRY_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
