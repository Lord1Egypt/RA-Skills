#!/usr/bin/env python3
"""
即刻数据经纬度位置查询 Skill 脚本。

功能说明：
1. 从命令行读取经度、纬度和坐标系。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/map/geocode/query` 查询位置详情。
4. 输出完整地址、国家、省、市、区、乡镇和街道。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/map/geocode/query"
APPKEY_ENV_NAMES = ("JIKE_MAP_GEOCODE_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
COORDINATE_SYSTEMS = {"gps", "baidu", "gaode", "mapbar"}


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取经纬度位置查询需要的 AppKey。
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
    1. 解析经纬度位置查询参数。
    2. 支持 gps、baidu、gaode、mapbar 四种坐标系。
    3. 支持 `--json` 输出原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="经纬度位置查询 - 即刻数据")
    parser.add_argument("--lng", required=True, help="经度，例如 114.30394")
    parser.add_argument("--lat", required=True, help="纬度，例如 34.79646")
    parser.add_argument("--coordinate-system", default="gps", choices=sorted(COORDINATE_SYSTEMS), help="坐标系：gps、baidu、gaode、mapbar")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_coordinate(value: str, field_name: str, min_value: Decimal, max_value: Decimal) -> str:
    """
    功能说明：
    1. 校验经度或纬度是否为数字。
    2. 校验经度范围为 -180 到 180，纬度范围为 -90 到 90。
    3. 返回原始字符串，保持接口参数精度。

    @param value 用户输入坐标
    @param field_name 字段名称，用于错误提示
    @param min_value 最小允许值
    @param max_value 最大允许值
    @return string 原始坐标字符串
    @raises ValueError 坐标非法时抛出
    """
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field_name} 必须是数字") from exc

    if number < min_value or number > max_value:
        raise ValueError(f"{field_name} 超出范围")
    return value


def request_api(lng: str, lat: str, coordinate_system: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据经纬度位置查询接口。
    2. 使用经度、纬度、坐标系和 appkey 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param lng 经度
    @param lat 纬度
    @param coordinate_system 坐标系
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    params = {"lng": lng, "lat": lat, "coordinate_system": coordinate_system, "appkey": appkey}
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
    1. 输出经纬度位置查询结果。
    2. 成功时展示完整地址和行政区划层级。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n📍 经纬度位置查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    print("\n📍 经纬度位置查询结果\n")
    print(f"  完整地址: {data.get('formatted_address') or '-'}")
    print(f"  国家:     {data.get('country') or '-'}")
    print(f"  省份:     {data.get('province') or '-'}")
    print(f"  城市:     {data.get('city') or '-'}")
    print(f"  区县:     {data.get('district') or '-'}")
    print(f"  乡镇:     {data.get('township') or '-'}")
    print(f"  街道:     {data.get('street') or '-'}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        lng = validate_coordinate(args.lng, "经度", Decimal("-180"), Decimal("180"))
        lat = validate_coordinate(args.lat, "纬度", Decimal("-90"), Decimal("90"))
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_MAP_GEOCODE_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(lng, lat, args.coordinate_system, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
