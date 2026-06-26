#!/usr/bin/env python3
"""
即刻数据车牌号码归属地查询 Skill 脚本。

功能说明：
1. 从命令行读取车牌号码或车牌前缀。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/vehicle/plate/query` 查询车牌归属地。
4. 输出车牌前缀、省份简称、省份和城市。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/vehicle/plate/query"
APPKEY_ENV_NAMES = ("JIKE_VEHICLE_PLATE_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取车牌归属地查询需要的 AppKey。
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
    1. 解析车牌归属地查询参数。
    2. 支持完整车牌，也支持至少前两位车牌前缀。
    3. 支持 `--json` 输出原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="车牌号码归属地 - 即刻数据")
    parser.add_argument("plate_number", help="车牌号码，至少前两位，例如 陕C88888 或 陕C")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_plate_number(value: str) -> str:
    """
    功能说明：
    1. 清理用户输入的车牌号空格。
    2. 校验至少传入前两位车牌前缀。
    3. 返回清理后的车牌号或车牌前缀。

    @param value 用户输入车牌号
    @return string 清理后的车牌号
    @raises ValueError 车牌号过短时抛出
    """
    plate_number = value.strip().replace(" ", "")
    if len(plate_number) < 2:
        raise ValueError("车牌号码至少需要传入前两位，例如 陕C")
    return plate_number


def request_api(plate_number: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据车牌号码归属地接口。
    2. 使用 `plate_number` 和 `appkey` 查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param plate_number 车牌号码或车牌前缀
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode({'plate_number': plate_number, 'appkey': appkey})}"
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
    1. 输出车牌归属地查询结果。
    2. 成功时展示车牌前缀、省份简称、省份和城市。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n🚗 车牌号码归属地查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    print("\n🚗 车牌号码归属地查询结果\n")
    print(f"  车牌前缀: {data.get('plate_prefix') or '-'}")
    print(f"  省份简称: {data.get('province_abbr') or '-'}")
    print(f"  省份:     {data.get('province') or '-'}")
    print(f"  城市:     {data.get('city') or '-'}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        plate_number = validate_plate_number(args.plate_number)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_VEHICLE_PLATE_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(plate_number, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
