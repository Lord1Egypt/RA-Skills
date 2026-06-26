#!/usr/bin/env python3
"""
即刻数据天气查询 Skill 脚本。

功能说明：
1. 支持当前天气、未来 7 天天气、未来 15 天天气三个查询类型。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 根据 `--type now|7d|15d` 路由到即刻数据对应天气接口。
4. 将天气结果输出为适合 AI 客户端阅读的文本或 JSON。

调用示例：
    python3 scripts/weather_query.py --province 广东省 --city 深圳市 --area 南山区
    python3 scripts/weather_query.py --type 7d --province 广东省 --city 深圳市
    python3 scripts/weather_query.py --type 15d --province 广东省 --city 深圳市 --json
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
    "now": "/v1/weather/query/by-area",
    "7d": "/v1/weather/query/7d",
    "15d": "/v1/weather/query/15d",
}
APPKEY_ENV_NAMES = ("JIKE_WEATHER_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取天气查询需要的 AppKey。
    2. 优先使用命令行 `--key`，适合临时调试。
    3. 其次读取 `JIKE_WEATHER_QUERY_KEY` 或通用 `JIKE_APPKEY` 环境变量。
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
    1. 解析天气查询参数，包括查询类型、省份、城市、区县和输出格式。
    2. `--type` 默认使用 `now`，保持用户问“查天气”时优先返回当前天气。
    3. `area` 为选填参数，适配直辖市和只到城市级的查询场景。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="天气查询 - 即刻数据")
    parser.add_argument("--type", choices=sorted(API_PATH_MAP.keys()), default="now", help="查询类型：now 当前天气，7d 未来7天，15d 未来15天")
    parser.add_argument("--province", required=True, help="省份名称，例如 广东省、北京市")
    parser.add_argument("--city", required=True, help="城市名称，例如 深圳市、北京市")
    parser.add_argument("--area", default="", help="区县名称，选填，例如 南山区")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算字符串终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于天气预报表格列宽计算。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换成字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证天气预报表格在终端中对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出未来天气预报表格。
    2. 自动计算每列最大宽度。
    3. 统一展示日期、星期、天气、温度、湿度、降水和风力。

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


def request_api(query_type: str, province: str, city: str, area: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据查询类型选择即刻数据天气接口。
    2. 组装 province、city、area、appkey 查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param query_type 查询类型 now、7d 或 15d
    @param province 省份名称
    @param city 城市名称
    @param area 区县名称，可为空
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    path = API_PATH_MAP[query_type]
    params = {"province": province, "city": city, "appkey": appkey}
    if area:
        params["area"] = area
    url = f"{API_BASE_URL}{path}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def print_now_weather(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出当前天气实况。
    2. 展示地区、天气现象、温度、体感、湿度、风向风力、能见度和观测时间。
    3. 适合 AI 客户端直接转述给用户。

    @param data 当前天气数据
    @return void
    """
    location = " ".join(part for part in [data.get("province"), data.get("city"), data.get("area")] if part)
    print("\n☁️ 天气查询结果\n")
    print(f"  地区:     {location or '-'}")
    print(f"  天气:     {data.get('weather') or '-'}")
    print(f"  温度:     {data.get('temp') or '-'}℃")
    print(f"  体感温度: {data.get('feels_like') or '-'}℃")
    print(f"  湿度:     {data.get('humidity') or '-'}%")
    print(f"  风向:     {data.get('wind_dir') or '-'}")
    print(f"  风力:     {data.get('wind_scale') or '-'}级")
    print(f"  风速:     {data.get('wind_speed') or '-'} km/h")
    print(f"  能见度:   {data.get('vis') or '-'} km")
    print(f"  观测时间: {data.get('obs_time') or '-'}")


def print_forecast_weather(query_type: str, data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出未来 7 天或未来 15 天天气预报。
    2. 将接口返回列表整理为表格。
    3. 表格保留日期、星期、白天/夜间天气、最高/最低温、湿度、降水和白天风力。

    @param query_type 查询类型 7d 或 15d
    @param data 预报天气数据
    @return void
    """
    location = " ".join(part for part in [data.get("province"), data.get("city"), data.get("area")] if part)
    title = "未来7天天气预报" if query_type == "7d" else "未来15天天气预报"
    print(f"\n☁️ {title}  {location or '-'}\n")

    rows = []
    for item in data.get("list") or []:
        rows.append([
            item.get("date") or "-",
            item.get("week") or "-",
            item.get("weather_day") or "-",
            item.get("weather_night") or "-",
            f"{item.get('temp_min') or '-'}~{item.get('temp_max') or '-'}℃",
            f"{item.get('humidity') or '-'}%",
            item.get("precip") or "-",
            f"{item.get('wind_dir_day') or '-'} {item.get('wind_scale_day') or '-'}",
        ])

    print_table(["日期", "星期", "白天", "夜间", "温度", "湿度", "降水", "白天风力"], rows)


def print_text_result(query_type: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据接口 code 判断查询是否成功。
    2. 当前天气和预报天气使用不同展示逻辑。
    3. 失败时展示接口 message，便于用户修正地区参数或检查 AppKey。

    @param query_type 查询类型 now、7d 或 15d
    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n☁️ 天气查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    if query_type == "now":
        print_now_weather(data)
    else:
        print_forecast_weather(query_type, data)
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_WEATHER_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(args.type, args.province.strip(), args.city.strip(), args.area.strip(), appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(args.type, payload)


if __name__ == "__main__":
    raise SystemExit(main())
