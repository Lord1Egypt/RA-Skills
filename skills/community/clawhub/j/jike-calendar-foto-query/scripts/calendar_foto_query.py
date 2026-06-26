#!/usr/bin/env python3
"""
佛历查询 - 即刻数据 Skill 脚本。

功能说明：
1. 从命令行读取阳历日期。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/calendar/foto/detail` 查询数据。
4. 将结果输出为适合 AI 客户端阅读的文本或 JSON。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/calendar/foto/detail"
APPKEY_ENV_NAMES = ("JIKE_CALENDAR_FOTO_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
TITLE = "佛历查询 - 即刻数据"
FAIL_TITLE = "佛历查询失败"
FIELDS = [('foto_string', '佛历日期'), ('to_full_string', '完整说明'), ('festivals', '节日'), ('other_festivals', '其他节日'), ('is_month_zhai', '月斋'), ('is_day_zhai_ten', '十斋日'), ('is_day_zhai_six', '六斋日'), ('is_day_zhai_shuo_wang', '朔望斋'), ('xiu', '星宿'), ('animal', '生肖'), ('xiu_luck', '星宿吉凶'), ('gong', '宫'), ('shou', '兽'), ('zheng', '正')]


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取接口需要的 AppKey。
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
    1. 解析日期查询参数。
    2. `--date` 为必填阳历日期，格式 `YYYY-MM-DD`。
    3. 支持 `--json` 输出接口原始 JSON。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument("--date", required=True, help="阳历日期，格式 YYYY-MM-DD，例如 2024-01-18")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_date(date_value: str) -> str:
    """
    功能说明：
    1. 校验阳历日期格式是否为 `YYYY-MM-DD`。
    2. 使用标准日期解析避免无效日期进入接口。
    3. 返回清理后的日期字符串。

    @param date_value 用户输入日期
    @return string 合法日期字符串
    @raises ValueError 日期格式非法时抛出
    """
    value = date_value.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期格式必须为 YYYY-MM-DD，例如 2024-01-18") from exc
    return value


def request_api(date_value: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据日期类接口。
    2. 使用 `date` 和 `appkey` 查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param date_value 阳历日期
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode({'date': date_value, 'appkey': appkey})}"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def normalize_value(value: Any) -> str:
    """
    功能说明：
    1. 将接口字段值转换为中文展示文本。
    2. 数组字段用顿号连接，布尔字段展示为“是/否”。
    3. 空值统一展示为 `-`。

    @param value 接口字段值
    @return string 展示文本
    """
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item) or "-"
    if value is None or value == "":
        return "-"
    return str(value)


def print_text_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 输出日期类查询结果。
    2. 成功时按字段配置展示核心信息。
    3. 失败时展示接口 message。

    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print(f"\n{FAIL_TITLE}\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data") or {}
    print(f"\n{TITLE}\n")
    for field, label in FIELDS:
        print(f"  {label}: {normalize_value(data.get(field))}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        date_value = validate_date(args.date)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print(f"错误: 未找到 AppKey，请先配置环境变量 {APPKEY_ENV_NAMES[0]} 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(date_value, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
