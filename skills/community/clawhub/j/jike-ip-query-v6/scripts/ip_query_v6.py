#!/usr/bin/env python3
"""
即刻数据 IPv6 地址查询 Skill 脚本。

功能说明：
1. 从命令行读取 IPv6 地址。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 调用即刻数据开放接口 `/v1/ip/query/v6` 查询 IPv6 归属地。
4. 将结果输出为适合 AI 客户端阅读的文本或 JSON。
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/ip/query/v6"
APPKEY_ENV_NAMES = ("JIKE_IP_QUERY_V6_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取调用即刻数据接口需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取业务环境变量或通用 `JIKE_APPKEY`。
    4. 最后读取脚本目录 `.env` 文件，方便本地验证。

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
    1. 解析 IPv6 查询参数。
    2. 支持 `--key` 临时传入 AppKey。
    3. 支持 `--json` 输出原始 JSON，便于 AI 客户端做结构化处理。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="IPv6地址查询 - 即刻数据")
    parser.add_argument("ip", help="IPv6 地址，例如 240e:1f:1::1")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def validate_ipv6(ip_value: str) -> str:
    """
    功能说明：
    1. 校验用户输入是否为合法 IPv6 地址。
    2. 使用标准库 ipaddress 避免将 IPv4 或普通文本传给 IPv6 接口。
    3. 返回标准化后的 IPv6 地址字符串。

    @param ip_value 用户输入的 IP 地址
    @return string 标准化后的 IPv6 地址
    @raises ValueError IP 格式不合法时抛出
    """
    try:
        ip_obj = ipaddress.ip_address(ip_value.strip())
    except ValueError as exc:
        raise ValueError("请提供合法的 IPv6 地址，例如 240e:1f:1::1") from exc

    if ip_obj.version != 6:
        raise ValueError("当前 Skill 仅支持 IPv6；IPv4 请使用 jike-ip-query-v4")

    return str(ip_obj)


def request_api(ip_value: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据 IPv6 地址查询接口。
    2. 使用 `ip` 和 `appkey` 两个查询参数。
    3. 返回接口 JSON；网络异常时返回统一错误结构。

    @param ip_value IPv6 地址
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH}?{urllib.parse.urlencode({'ip': ip_value, 'appkey': appkey})}"
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
    1. 将接口返回结果输出为人类可读文本。
    2. 成功时展示 IP、国家、省份、城市、地区、运营商和 Long 数值。
    3. 失败时展示接口 message，便于用户检查 IP 或 AppKey。

    @param payload 接口返回数据
    @return int 进程退出码，成功为 0，失败为 2
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n🌐 IPv6地址查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    data = payload.get("data") or {}
    province = data.get("province") or data.get("provinc") or "-"
    print("\n🌐 IPv6地址查询结果\n")
    print(f"  IP:      {data.get('ip') or '-'}")
    print(f"  国家:    {data.get('country') or '-'}")
    print(f"  省份:    {province}")
    print(f"  城市:    {data.get('city') or '-'}")
    print(f"  地区:    {data.get('area') or '-'}")
    print(f"  运营商:  {data.get('isp') or '-'}")
    print(f"  Long值:  {data.get('long_ip') or '-'}")
    return 0


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        ip_value = validate_ipv6(args.ip)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1

    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_IP_QUERY_V6_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    payload = request_api(ip_value, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2

    return print_text_result(payload)


if __name__ == "__main__":
    raise SystemExit(main())
