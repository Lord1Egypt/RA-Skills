#!/usr/bin/env python3
"""
即刻数据圆周率查询 Skill 脚本。

功能说明：
1. 支持查找圆周率指定位置开始的数字，也支持查找指定数字在圆周率中的位置。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/pi/find_number` 和 `/v1/pi/find_location` 接口。
4. 将查询结果输出为适合 AI 客户端阅读的文本或 JSON。
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
API_PATH_MAP = {
    "find-number": "/v1/pi/find_number",
    "find-location": "/v1/pi/find_location",
}
APPKEY_ENV_NAMES = ("JIKE_PI_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取圆周率查询需要的 AppKey。
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
    1. 解析圆周率查询子命令参数。
    2. `find-number` 用于查询指定位置开始的数字。
    3. `find-location` 用于查找指定数字串首次出现的位置。
    4. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]
    parser = argparse.ArgumentParser(description="圆周率查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    find_number = subparsers.add_parser("find-number", help="查找圆周率中指定位置的数字")
    find_number.add_argument("--start-location", required=True, help="起始位置，1 到 200000000")
    find_number.add_argument("--length", default="20", help="查询长度，1 到 1000，默认 20")

    find_location = subparsers.add_parser("find-location", help="查找指定数字在圆周率中的位置")
    find_location.add_argument("--find-number", required=True, help="需要查找的数字，1 到 25 位")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_int(value: str, field_name: str, min_value: int, max_value: int) -> str:
    """
    功能说明：
    1. 校验位置和长度参数必须是整数。
    2. 按接口文档限制取值范围。
    3. 返回字符串，保持传给接口的参数格式和文档一致。

    @param value 用户输入值
    @param field_name 字段名称，用于错误提示
    @param min_value 最小值
    @param max_value 最大值
    @return string 校验后的数字字符串
    @raises ValueError 参数非法时抛出
    """
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} 必须是整数") from exc
    if number < min_value or number > max_value:
        raise ValueError(f"{field_name} 取值范围是 {min_value} 到 {max_value}")
    return str(number)


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据圆周率子命令构造接口参数。
    2. `find-number` 校验起始位置和长度。
    3. `find-location` 校验目标数字串长度和纯数字格式。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    if args.command == "find-number":
        return {
            "start_location": normalize_int(args.start_location, "start_location", 1, 200000000),
            "length": normalize_int(args.length, "length", 1, 1000),
        }
    find_number = args.find_number.strip()
    if not re.fullmatch(r"\d{1,25}", find_number):
        raise ValueError("find_number 必须是 1 到 25 位数字")
    return {"find_number": find_number}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择圆周率接口。
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


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出圆周率查询结果。
    2. 指定位置查询返回数字串；位置查找返回位置、左右上下文和周边数字。
    3. 失败时展示接口 message。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n圆周率查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data")
    print("\n圆周率查询结果\n")
    if command == "find-number":
        print(f"  数字: {data or '-'}")
        return 0
    data = data or {}
    print(f"  查找数字: {data.get('find_number') or '-'}")
    print(f"  是否找到: {data.get('result')}")
    print(f"  位置数字: {data.get('location_number') or '-'}")
    print(f"  位置文本: {data.get('location_text') or '-'}")
    print(f"  左侧:     {data.get('find_number_left') or '-'}")
    print(f"  右侧:     {data.get('find_number_right') or '-'}")
    print(f"  周边:     {data.get('find_number_around') or '-'}")
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
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_PI_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
