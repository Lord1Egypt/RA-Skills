#!/usr/bin/env python3
"""
生日花语 - 即刻数据 Skill 脚本。

功能说明：
1. 从命令行读取查询参数。
2. 按 `--key`、业务环境变量、通用环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/birthday/flower` 查询数据。
4. 将接口结果输出为适合 AI 客户端阅读的文本或 JSON。
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
API_PATH = "/v1/birthday/flower"
APPKEY_ENV_NAMES = ("JIKE_BIRTHDAY_FLOWER_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
FIELDS = [('birthday', '生日'), ('birthday_flower', '生日花'), ('birthday_flower_content', '生日花说明'), ('flower_lng', '花语'), ('flower_lng_content', '花语说明'), ('birthstone', '诞生石'), ('birthstone_content', '诞生石说明')]
OPTIONAL_PARAMS = [('birthday', '生日，格式 MM-DD，例如 02-06')]
REQUIRED_PARAMS = []
DATE_PARAMS = ['birthday']
TITLE = "生日花语 - 即刻数据"
FAIL_TITLE = "生日花语查询失败"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取调用即刻数据接口需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取当前 Skill 的业务环境变量或通用 `JIKE_APPKEY`。
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
    1. 解析命令行查询参数。
    2. 按接口文档保留原始参数含义，命令行参数使用横杠形式。
    3. 支持 `--json` 输出接口原始 JSON，便于 AI 客户端结构化处理。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description=TITLE)
    for param_name, help_text in REQUIRED_PARAMS:
        parser.add_argument("--" + param_name.replace("_", "-"), required=True, help=help_text)
    for param_name, help_text in OPTIONAL_PARAMS:
        parser.add_argument("--" + param_name.replace("_", "-"), default="", help=help_text)
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_date_param(param_name: str, value: str) -> str:
    """
    功能说明：
    1. 校验生日类参数是否为接口要求的 `MM-DD` 格式。
    2. 只在用户传入对应参数时校验，未传时交给接口按默认逻辑处理。
    3. 返回清理后的日期字符串。

    @param param_name 参数名
    @param value 参数值
    @return string 校验后的参数值
    @raises ValueError 日期格式非法时抛出
    """
    value = value.strip()
    if not value:
        return value
    if param_name in DATE_PARAMS and not re.fullmatch(r"\d{2}-\d{2}", value):
        raise ValueError(f"{param_name} 格式必须为 MM-DD，例如 02-06")
    return value


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 从命令行参数中组装接口业务参数。
    2. 必填参数必须传入；可选参数为空时不传给接口。
    3. 对生日等格式敏感字段做基础校验。

    @param args argparse 解析结果
    @return dict 接口业务参数
    """
    params = {}
    for param_name, _ in REQUIRED_PARAMS + OPTIONAL_PARAMS:
        value = getattr(args, param_name, "")
        value = validate_date_param(param_name, str(value))
        if value:
            params[param_name] = value
    return params


def request_api(params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据开放接口。
    2. 自动追加 `appkey` 参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param params 接口业务参数
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode({**params, 'appkey': appkey})}"
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
    1. 将接口返回字段统一转换成可读文本。
    2. 数组字段使用顿号连接，字典字段使用 JSON 保留结构。
    3. 空值统一展示为 `-`，便于用户判断无结果。

    @param value 接口字段值
    @return string 展示文本
    """
    if value is None or value == "":
        return "-"
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item) or "-"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def print_text_result(payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 将接口返回结果输出为中文文本。
    2. 成功时按 FIELDS 配置展示核心字段。
    3. 失败时展示接口 message，便于用户检查参数、AppKey 或接口权限。

    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print(f"\n{FAIL_TITLE}\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2
    data = payload.get("data") or {}
    print(f"\n{TITLE}\n")
    if isinstance(data, list):
        for index, item in enumerate(data, 1):
            print(f"  {index}. {normalize_value(item)}")
        return 0
    for field, label in FIELDS:
        print(f"  {label}: {normalize_value(data.get(field))}")
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
        print(f"错误: 未找到 AppKey，请先配置环境变量 {APPKEY_ENV_NAMES[0]} 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
