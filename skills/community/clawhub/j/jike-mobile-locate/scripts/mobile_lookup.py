#!/usr/bin/env python3
"""
即刻数据手机号码归属地查询 Skill 脚本。

功能说明：
1. 从命令行参数中读取一个或多个 11 位中国大陆手机号。
2. 按命令行参数、环境变量、脚本目录 .env 的优先级读取 AppKey。
3. 调用即刻数据开放接口 /v1/mobile/query 查询归属地。
4. 将结果格式化为适合 AI 客户端展示的文本或 JSON。

调用示例：
    python3 scripts/mobile_lookup.py 17611491111
    python3 scripts/mobile_lookup.py 17611491111 17611492222 --no-mask
    python3 scripts/mobile_lookup.py --key your_appkey 17611491111
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH = "/v1/mobile/query"
APPKEY_ENV_NAMES = ("JIKE_MOBILE_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取 Skill 调用接口需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取环境变量，便于 QClaw/OpenClaw/QoderWork 等客户端统一配置。
    4. 最后读取脚本目录下的 `.env` 文件，方便本地测试。

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


def parse_args(argv: list[str]) -> dict[str, Any]:
    """
    功能说明：
    1. 解析脚本参数，支持手机号、`--key`、`--no-mask`、`--json`。
    2. 支持用户直接传入一句话，脚本会从文本中提取 11 位手机号。
    3. 返回统一参数结构，后续查询逻辑只依赖该结构。

    @param argv 命令行参数列表
    @return dict 解析后的参数、手机号列表和错误信息
    """
    result: dict[str, Any] = {
        "cli_key": None,
        "phones": [],
        "no_mask": False,
        "json_output": False,
        "error": None,
    }

    raw_parts: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--key":
            if i + 1 >= len(argv):
                result["error"] = "错误: --key 后需要提供 AppKey"
                return result
            result["cli_key"] = argv[i + 1]
            i += 2
        elif arg == "--no-mask":
            result["no_mask"] = True
            i += 1
        elif arg == "--json":
            result["json_output"] = True
            i += 1
        else:
            raw_parts.append(arg)
            i += 1

    raw_text = " ".join(raw_parts)
    phones = re.findall(r"(?<!\d)1\d{10}(?!\d)", raw_text)
    result["phones"] = list(dict.fromkeys(phones))

    if not result["phones"]:
        result["error"] = (
            "错误: 需要提供至少一个 1 开头的 11 位手机号\n"
            "用法: python3 scripts/mobile_lookup.py [--key APPKEY] <手机号> [...]\n"
            "示例: python3 scripts/mobile_lookup.py 17611491111"
        )

    return result


def mask_mobile(mobile: str) -> str:
    """
    功能说明：
    1. 默认对手机号中间 4 位脱敏。
    2. 避免在 AI 客户端输出中暴露完整手机号。

    @param mobile 手机号码
    @return string 脱敏后的手机号
    """
    return mobile[:3] + "****" + mobile[7:]


def get_display_width(value: str) -> int:
    """
    功能说明：
    1. 计算字符串在终端中的展示宽度。
    2. 中文、全角字符按 2 个字符宽度处理，保证表格列对齐。
    3. 批量查询输出表格时使用该宽度做补齐。

    @param value 待计算的文本
    @return int 终端展示宽度
    """
    width = 0
    for char in value:
        width += 2 if unicodedata.east_asian_width(char) in ("F", "W") else 1
    return width


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据终端展示宽度补齐空格。
    3. 避免中文字段导致批量查询表格错位。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的单元格文本
    """
    text = str(value or "-")
    return text + " " * max(width - get_display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出批量查询结果表格。
    2. 自动根据表头和数据计算列宽。
    3. 统一展示号码、归属地、区号、邮编、运营商和类型。

    @param headers 表头列表
    @param rows 表格数据列表
    @return void
    """
    widths = [get_display_width(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], get_display_width(str(value or "-")))

    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    print(border)
    print("| " + " | ".join(pad_cell(header, widths[index]) for index, header in enumerate(headers)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(pad_cell(value, widths[index]) for index, value in enumerate(row)) + " |")
    print(border)


def query_mobile(mobile: str, appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 调用即刻数据手机号码归属地查询接口。
    2. 使用 `mobile` 和 `appkey` 两个查询参数。
    3. 将接口成功/失败结果统一转换为脚本内部结构。

    @param mobile 11 位手机号
    @param appkey 即刻数据 AppKey
    @return dict 查询结果，包含 success、mobile、data 或 error
    """
    params = urllib.parse.urlencode({"mobile": mobile, "appkey": appkey})
    url = f"{API_BASE_URL}{API_PATH}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"success": False, "mobile": mobile, "error": f"接口请求失败: HTTP {exc.code}"}
    except urllib.error.URLError as exc:
        return {"success": False, "mobile": mobile, "error": f"网络请求失败: {exc.reason}"}
    except Exception as exc:
        return {"success": False, "mobile": mobile, "error": f"请求异常: {exc}"}

    code = int(payload.get("code", 0) or 0)
    if code == 200:
        return {"success": True, "mobile": mobile, "data": payload.get("data") or {}}

    message = payload.get("message") or payload.get("msg") or "查询失败"
    return {
        "success": False,
        "mobile": mobile,
        "error": message,
        "code": code,
        "request_id": payload.get("request_id", ""),
    }


def print_text_result(results: list[dict[str, Any]], no_mask: bool = False) -> None:
    """
    功能说明：
    1. 将查询结果输出为人类可读文本。
    2. 单条查询使用卡片式文本，批量查询使用表格。
    3. 失败项保留错误原因，不影响其他手机号查询。

    @param results 查询结果列表
    @param no_mask 是否展示完整手机号
    @return void
    """
    if len(results) > 1:
        print(f"\n📱 手机号码归属地批量查询  共 {len(results)} 条\n")
        rows: list[list[Any]] = []
        for item in results:
            mobile = item["mobile"] if no_mask else mask_mobile(item["mobile"])
            if not item["success"]:
                rows.append([mobile, "失败", "-", "-", "-", item.get("error", "查询失败"), "-"])
                continue

            data = item.get("data") or {}
            rows.append([
                mobile,
                data.get("province") or "-",
                data.get("city") or "-",
                data.get("city_code") or "-",
                data.get("post_code") or "-",
                data.get("isp") or "-",
                data.get("isp_type") or "-",
            ])

        print_table(["号码", "省份", "城市", "区号", "邮编", "运营商", "类型"], rows)
        return

    for item in results:
        mobile = item["mobile"] if no_mask else mask_mobile(item["mobile"])
        if not item["success"]:
            print("\n📱 手机号码归属地查询失败\n")
            print(f"  号码:     {mobile}")
            print(f"  原因:     {item.get('error', '查询失败')}")
            continue

        data = item.get("data") or {}
        print("\n📱 手机号码归属地查询结果\n")
        print(f"  号码:     {mobile}")
        print(f"  省份:     {data.get('province') or '-'}")
        print(f"  城市:     {data.get('city') or '-'}")
        print(f"  运营商:   {data.get('isp') or '-'}")
        print(f"  类型:     {data.get('isp_type') or '-'}")
        print(f"  邮编:     {data.get('post_code') or '-'}")
        print(f"  区号:     {data.get('city_code') or '-'}")
        print(f"  行政区划: {data.get('area_code') or '-'}")


def main() -> int:
    parsed = parse_args(sys.argv[1:])
    if parsed["error"]:
        print(parsed["error"])
        return 1

    appkey = load_appkey(parsed["cli_key"])
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_MOBILE_KEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1

    results = [query_mobile(mobile, appkey) for mobile in parsed["phones"]]
    if parsed["json_output"]:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_text_result(results, parsed["no_mask"])

    return 0 if all(item["success"] for item in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
