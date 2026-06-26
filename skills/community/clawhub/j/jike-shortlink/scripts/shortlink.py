#!/usr/bin/env python3
"""
即刻数据短链接 Skill 脚本。

功能说明：
1. 支持生成短链接、短链接还原、短链接访问统计三个子命令。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/shortlink/create`、`restore`、`stat` 接口。
4. 将结果输出为适合 AI 客户端阅读的文本或 JSON。

调用示例：
    python3 scripts/shortlink.py create --target https://www.jikeapi.cn/
    python3 scripts/shortlink.py restore --link http://t.jikeapi.cn/s/NgZYJ
    python3 scripts/shortlink.py stat --link http://t.jikeapi.cn/s/NgZYJ
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
from datetime import datetime
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {
    "create": "/v1/shortlink/create",
    "restore": "/v1/shortlink/restore",
    "stat": "/v1/shortlink/stat",
}
APPKEY_ENV_NAMES = ("JIKE_SHORTLINK_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取短链接接口需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取 `JIKE_SHORTLINK_KEY` 或通用 `JIKE_APPKEY` 环境变量。
    4. 最后读取脚本目录 `.env` 文件，方便本地测试。

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
    1. 解析短链接 Skill 的子命令参数。
    2. `create` 用于生成短链，支持访问次数和到期时间。
    3. `restore` 用于查询短链原始地址。
    4. `stat` 用于查询短链访问统计，可选起止时间。
    5. `--json` 支持放在子命令前或子命令后，降低用户使用成本。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="短链接 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="生成短链接")
    create_parser.add_argument("--target", required=True, help="原始地址，必须为国内已备案地址")
    create_parser.add_argument("--max-access-count", type=int, default=None, help="最大访问次数；不传代表不限制")
    create_parser.add_argument("--expiration-time", default="", help="到期时间，格式 YYYY-mm-dd HH:MM:SS")

    restore_parser = subparsers.add_parser("restore", help="短链接还原")
    restore_parser.add_argument("--link", required=True, help="短链接，例如 http://t.jikeapi.cn/s/NgZYJ")

    stat_parser = subparsers.add_parser("stat", help="短链接访问统计")
    stat_parser.add_argument("--link", required=True, help="短链接，例如 http://t.jikeapi.cn/s/NgZYJ")
    stat_parser.add_argument("--start-time", default="", help="起始时间，格式 YYYY-mm-dd HH:MM:SS，需和 end-time 同时传")
    stat_parser.add_argument("--end-time", default="", help="截止时间，格式 YYYY-mm-dd HH:MM:SS，需和 start-time 同时传")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def validate_url(value: str, field_name: str) -> str:
    """
    功能说明：
    1. 校验 target 或 link 是否为 http/https 链接。
    2. 避免用户传入空字符串、普通文本或不支持的协议。
    3. 返回清理后的 URL 字符串。

    @param value 用户输入 URL
    @param field_name 字段名称，用于错误提示
    @return string URL
    @raises ValueError URL 不合法时抛出
    """
    url = value.strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"{field_name} 必须是 http 或 https 链接")
    return url


def validate_datetime(value: str, field_name: str) -> str:
    """
    功能说明：
    1. 校验时间字符串是否符合接口要求的 `Y-m-d H:i:s` 格式。
    2. 仅在用户传入时间时校验。
    3. 校验通过后返回原始字符串，保持接口参数格式不变。

    @param value 用户输入时间
    @param field_name 字段名称，用于错误提示
    @return string 原始时间字符串
    @raises ValueError 时间格式错误时抛出
    """
    if not value:
        return ""
    try:
        datetime.strptime(value, DATETIME_FORMAT)
    except ValueError as exc:
        raise ValueError(f"{field_name} 格式必须是 YYYY-mm-dd HH:MM:SS") from exc
    return value


def validate_access_count(value: int | None) -> int | None:
    """
    功能说明：
    1. 校验短链接最大访问次数。
    2. 不传时返回 None，表示不限制。
    3. 传入时必须为正整数。

    @param value 最大访问次数
    @return int|None 校验后的访问次数
    @raises ValueError 访问次数非法时抛出
    """
    if value is None:
        return None
    if value <= 0:
        raise ValueError("max_access_count 必须大于 0")
    return value


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择短链接接口。
    2. 自动追加 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param command 子命令 create、restore 或 stat
    @param params 接口业务参数
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    request_params = {**params, "appkey": appkey}
    url = f"{API_BASE_URL}{API_PATH_MAP[command]}?{urllib.parse.urlencode(request_params)}"

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
    1. 根据短链接子命令构造接口参数。
    2. create 会校验原始链接、最大访问次数和到期时间。
    3. stat 会校验起止时间必须同时传入。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "create":
        params: dict[str, Any] = {"target": validate_url(args.target, "target")}
        access_count = validate_access_count(args.max_access_count)
        if access_count is not None:
            params["max_access_count"] = access_count
        expiration_time = validate_datetime(args.expiration_time, "expiration_time")
        if expiration_time:
            params["expiration_time"] = expiration_time
        return params

    if args.command == "restore":
        return {"link": validate_url(args.link, "link")}

    start_time = validate_datetime(args.start_time, "start_time")
    end_time = validate_datetime(args.end_time, "end_time")
    if bool(start_time) != bool(end_time):
        raise ValueError("start_time 和 end_time 需要同时传入")

    params = {"link": validate_url(args.link, "link")}
    if start_time and end_time:
        params["start_time"] = start_time
        params["end_time"] = end_time
    return params


def print_create_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出短链接生成结果。
    2. 展示原始链接、短链、无协议短链、到期时间和最大访问次数。
    3. 便于用户直接复制短链使用。

    @param data 短链接生成结果
    @return void
    """
    print("\n🔗 短链接生成结果\n")
    print(f"  原始链接:   {data.get('target') or '-'}")
    print(f"  短链接:     {data.get('link') or '-'}")
    print(f"  简短格式:   {data.get('simple_link') or '-'}")
    print(f"  到期时间:   {data.get('expiration_time') or '-'}")
    print(f"  最大访问数: {data.get('max_access_count') or '-'}")


def print_restore_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出短链接还原结果。
    2. 展示短链对应的原始链接。
    3. 便于用户确认短链最终跳转地址。

    @param data 短链接还原结果
    @return void
    """
    print("\n🔗 短链接还原结果\n")
    print(f"  原始链接: {data.get('target') or '-'}")


def print_stat_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出短链接访问统计结果。
    2. 展示最大访问次数、总访问次数和独立 IP 数。
    3. 便于用户评估短链传播情况。

    @param data 短链接统计结果
    @return void
    """
    print("\n🔗 短链接访问统计\n")
    print(f"  最大访问数: {data.get('max_access_count')}")
    print(f"  总访问数:   {data.get('access_count')}")
    print(f"  IP数量:     {data.get('ip_count')}")


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据接口 code 判断短链接操作是否成功。
    2. 按 create、restore、stat 分别调用不同展示逻辑。
    3. 失败时展示接口 message，便于用户检查链接、时间或 AppKey。

    @param command 子命令
    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n🔗 短链接操作失败\n")
        print(f"  原因: {payload.get('message') or '操作失败'}")
        return 2

    data = payload.get("data") or {}
    if command == "create":
        print_create_result(data)
    elif command == "restore":
        print_restore_result(data)
    else:
        print_stat_result(data)
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_SHORTLINK_KEY 或 JIKE_APPKEY")
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

    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
