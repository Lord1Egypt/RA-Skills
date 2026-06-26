#!/usr/bin/env python3
"""
即刻数据 ISBN 图书查询 Skill 脚本。

功能说明：
1. 从命令行读取 ISBN 编号。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/book/isbn/query` 查询图书基础信息。
4. 输出书名、作者、出版社、出版日期、定价、装帧、页数和封面等字段。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/book/isbn/query"
APPKEY_ENV_NAMES = ("JIKE_BOOK_ISBN_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取 ISBN 图书查询需要的 AppKey。
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
    1. 解析 ISBN 图书查询参数。
    2. 支持 ISBN-10 或 ISBN-13，允许用户输入横杠和空格。
    3. 支持 `--json` 输出接口原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="ISBN图书查询 - 即刻数据")
    parser.add_argument("isbn", help="ISBN 编号，例如 9787115428028")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_isbn(isbn: str) -> str:
    """
    功能说明：
    1. 清理 ISBN 中的横杠和空格。
    2. 校验 ISBN-10 或 ISBN-13 基础格式。
    3. 返回清理后的 ISBN 字符串，避免把普通文本传给接口。

    @param isbn 用户输入 ISBN
    @return string 清理后的 ISBN
    @raises ValueError ISBN 格式不合法时抛出
    """
    value = re.sub(r"[\s-]+", "", isbn.strip())
    if not re.fullmatch(r"(?:\d{13}|\d{9}[\dXx])", value):
        raise ValueError("ISBN 格式不正确，请提供 ISBN-10 或 ISBN-13，例如 9787115428028")
    return value.upper()


def request_api(isbn: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据 ISBN 图书查询接口。
    2. 使用 `isbn` 和 `appkey` 两个查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param isbn ISBN 编号
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    params = {"isbn": isbn, "appkey": appkey}
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
    1. 输出 ISBN 图书查询结果。
    2. 成功时展示图书基础出版信息。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\nISBN图书查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    print("\nISBN图书查询结果\n")
    print(f"  书名:     {data.get('title') or '-'}")
    print(f"  作者:     {data.get('author') or '-'}")
    print(f"  译者:     {data.get('translator') or '-'}")
    print(f"  出版社:   {data.get('publisher') or '-'}")
    print(f"  出版日期: {data.get('publish_date') or '-'}")
    print(f"  ISBN-10:  {data.get('isbn10') or '-'}")
    print(f"  ISBN-13:  {data.get('isbn13') or data.get('isbn') or '-'}")
    print(f"  定价:     {data.get('price') or '-'}")
    print(f"  装帧:     {data.get('binding') or '-'}")
    print(f"  页数:     {data.get('page_count') or '-'}")
    print(f"  丛书:     {data.get('series') or '-'}")
    print(f"  封面:     {data.get('cover') or '-'}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        isbn = validate_isbn(args.isbn)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_BOOK_ISBN_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(isbn, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
