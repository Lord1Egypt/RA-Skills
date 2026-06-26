#!/usr/bin/env python3
"""
即刻数据老黄历查询 Skill 脚本。

功能说明：
1. 从命令行读取阳历日期和可选时间。
2. 按 `--key`、业务环境变量、通用环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/calendar/lunar/detail` 查询农历、黄历宜忌、吉神凶煞和节气等信息。
4. 将结果输出为适合 AI 客户端阅读的文本或 JSON。
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
API_PATH = "/v1/calendar/lunar/detail"
APPKEY_ENV_NAMES = ("JIKE_CALENDAR_LUNAR_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取老黄历查询接口需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取 `JIKE_CALENDAR_LUNAR_QUERY_KEY` 或通用 `JIKE_APPKEY`。
    4. 最后读取脚本目录 `.env` 文件，方便本地客户端配置。

    @param cli_key 命令行临时传入的 AppKey
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
    1. 解析老黄历查询参数。
    2. `--date` 为必填阳历日期，格式 `YYYY-MM-DD`。
    3. `--time` 为可选时间，格式 `HH:MM:SS`，默认 `00:00:00`。
    4. 支持 `--json` 输出接口原始 JSON，便于 AI 客户端结构化处理。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="老黄历查询 - 即刻数据")
    parser.add_argument("--date", required=True, help="阳历日期，格式 YYYY-MM-DD，例如 2024-02-02")
    parser.add_argument("--time", default="00:00:00", help="时间，格式 HH:MM:SS，默认 00:00:00")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_date(date_value: str) -> str:
    """
    功能说明：
    1. 校验阳历日期格式是否为 `YYYY-MM-DD`。
    2. 使用标准日期解析避免 2024-02-31 这类无效日期进入接口。
    3. 返回清理后的日期字符串。

    @param date_value 用户输入的阳历日期
    @return string 合法日期字符串
    @raises ValueError 日期格式或日期值非法时抛出
    """
    value = date_value.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期格式必须为 YYYY-MM-DD，例如 2024-02-02") from exc
    return value


def validate_time(time_value: str) -> str:
    """
    功能说明：
    1. 校验时间格式是否为 `HH:MM:SS`。
    2. 接口支持按时辰返回对应黄历信息，因此这里保留时间参数。
    3. 返回清理后的时间字符串。

    @param time_value 用户输入时间
    @return string 合法时间字符串
    @raises ValueError 时间格式非法时抛出
    """
    value = time_value.strip() or "00:00:00"
    if not re.fullmatch(r"\d{2}:\d{2}:\d{2}", value):
        raise ValueError("时间格式必须为 HH:MM:SS，例如 10:30:00")
    try:
        datetime.strptime(value, "%H:%M:%S")
    except ValueError as exc:
        raise ValueError("时间格式必须为 HH:MM:SS，例如 10:30:00") from exc
    return value


def request_api(date_value: str, time_value: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据老黄历查询接口。
    2. 使用 `date`、`time`、`appkey` 三个查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param date_value 阳历日期
    @param time_value 时间
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    params = {"date": date_value, "time": time_value, "appkey": appkey}
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


def join_items(value: Any) -> str:
    """
    功能说明：
    1. 将接口返回的数组或字符串统一转换为展示文本。
    2. 节日字段可能为空数组，展示时用 `-` 占位。
    3. 保持输出简洁，避免 AI 客户端展示 Python 列表格式。

    @param value 接口字段值
    @return string 展示文本
    """
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item) or "-"
    return str(value or "-")


def print_text_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 将老黄历接口返回结果输出为中文文本。
    2. 成功时重点展示公历、农历、宜忌、黄黑道、生肖、星座、节气和神位。
    3. 失败时展示接口 message，便于用户检查日期、AppKey 或接口权限。

    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n老黄历查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    print("\n老黄历查询结果\n")
    print(f"  公历:   {data.get('solar_date') or '-'}")
    print(f"  公历信息: {data.get('solar_full_string') or '-'}")
    print(f"  农历:   {data.get('lunar_string') or '-'}")
    print(f"  农历年: {data.get('lunar_year_in_gan_zhi') or '-'}年 / 生肖{data.get('lunar_year_sheng_xiao') or '-'}")
    print(f"  星座:   {data.get('solar_xing_zuo') or '-'}")
    print(f"  节气:   {data.get('lunar_jie_qi') or '-'}")
    print(f"  黄黑道: {data.get('lunar_day_tian_shen_type') or '-'} / {data.get('lunar_day_tian_shen') or '-'} / {data.get('lunar_day_tian_shen_luck') or '-'}")
    print(f"  宜:     {data.get('lunar_day_yi') or '-'}")
    print(f"  忌:     {data.get('lunar_day_ji') or '-'}")
    print(f"  喜神:   {data.get('lunar_day_position_xi') or '-'}")
    print(f"  福神:   {data.get('lunar_day_position_fu') or '-'}")
    print(f"  财神:   {data.get('lunar_day_position_cai') or '-'}")
    print(f"  节日:   {join_items(data.get('solar_festivals'))} / {join_items(data.get('lunar_festivals'))}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        date_value = validate_date(args.date)
        time_value = validate_time(args.time)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_CALENDAR_LUNAR_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(date_value, time_value, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
