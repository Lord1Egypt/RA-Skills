#!/usr/bin/env python3
"""
手机号码归属地查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
输入手机号码或号段前缀，查询归属地省份/城市、区号、邮编、运营商、卡类型

用法:
    python mobile_lookup.py <手机号码>
    python mobile_lookup.py 13812345678
    python mobile_lookup.py 13812345678 13912345678 15912345678
    python mobile_lookup.py 1381234
    python mobile_lookup.py 13812345678 --no-mask

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_MOBILE_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_MOBILE_KEY=your_api_key
    3. 直接传参: python mobile_lookup.py --key your_api_key 13812345678

免费申请 API Key: https://www.juhe.cn/docs/api/id/11
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://apis.juhe.cn/mobile/get"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/11"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_MOBILE_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_MOBILE_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_phone(phone: str) -> str | None:
    """校验手机号格式，返回错误描述或 None"""
    if not phone.isdigit():
        return f"手机号码必须为纯数字，当前输入: {phone}"
    if not phone.startswith("1"):
        return f"手机号码必须以 1 开头，当前输入: {phone}"
    if len(phone) not in (7, 11):
        return f"手机号码应为 11 位，或号段前缀为 7 位，当前长度: {len(phone)}"
    return None


def mask_phone(phone: str) -> str:
    """对手机号中间4位脱敏，7位号段不脱敏"""
    if len(phone) == 11:
        return phone[:3] + "****" + phone[7:]
    return phone


def query_mobile(phone: str, api_key: str) -> dict:
    """调用聚合数据 API 查询手机号归属地"""
    params = {
        "phone": phone,
        "key": api_key,
        "dtype": "json",
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    error_code = data.get("error_code", -1)
    resultcode = data.get("resultcode", "")

    if str(error_code) == "0" or str(resultcode) == "200":
        result = data.get("result", {})
        return {"success": True, "phone": phone, "result": result}

    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}"
    elif error_code == 10012:
        hint = "\n   今日免费调用次数已用尽，请升级套餐"
    elif error_code == 201101:
        hint = "\n   手机号码不能为空"
    elif error_code == 201102:
        hint = "\n   错误的手机号码，请检查格式"
    elif error_code == 201103:
        hint = "\n   该号段查询无结果"

    return {
        "success": False,
        "phone": phone,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def print_single_result(phone: str, result: dict, no_mask: bool = False) -> None:
    """单条结果卡片式输出"""
    display = phone if no_mask else mask_phone(phone)
    province = result.get("province", "")
    city = result.get("city", "")
    areacode = result.get("areacode", "")
    zip_code = result.get("zip", "")
    company = result.get("company", "")
    card = result.get("card", "")

    location = province
    if city and city != province:
        location = f"{province} {city}"

    print(f"\n📱 手机号码归属地查询结果\n")
    print(f"  号码:   {display}")
    print(f"  省份:   {province or '—'}")
    print(f"  城市:   {city or '—'}")
    print(f"  归属地: {location or '—'}")
    print(f"  区号:   {areacode or '—'}")
    print(f"  邮编:   {zip_code or '—'}")
    print(f"  运营商: {company or '—'}")
    print(f"  卡类型: {card or '—'}")
    print()


def print_batch_table(results: list, no_mask: bool = False) -> None:
    """批量结果表格式输出"""
    headers = ["号码", "省份", "城市", "区号", "邮编", "运营商", "卡类型"]

    rows = []
    for item in results:
        phone = item["phone"]
        display = phone if no_mask else mask_phone(phone)
        if item["success"]:
            r = item["result"]
            rows.append([
                display,
                r.get("province", ""),
                r.get("city", ""),
                r.get("areacode", ""),
                r.get("zip", ""),
                r.get("company", ""),
                r.get("card", ""),
            ])
        else:
            rows.append([display, "查询失败", "", "", "", "", ""])

    col_widths = []
    for i, h in enumerate(headers):
        col_widths.append(sum(2 if ord(c) > 127 else 1 for c in h))
    for row in rows:
        for i, cell in enumerate(row):
            width = sum(2 if ord(c) > 127 else 1 for c in str(cell))
            col_widths[i] = max(col_widths[i], width)

    def pad(text, width):
        actual = sum(2 if ord(c) > 127 else 1 for c in str(text))
        return str(text) + " " * max(0, width - actual)

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_row = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"

    count = len(results)
    print(f"\n📱 手机号码归属地批量查询  共 {count} 条\n")
    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        print("| " + " | ".join(pad(cell, col_widths[i]) for i, cell in enumerate(row)) + " |")
    print(sep)
    print()


def parse_args(args: list) -> dict:
    """解析命令行参数"""
    result = {
        "cli_key": None,
        "phones": [],
        "no_mask": False,
        "error": None,
    }

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--key":
            if i + 1 < len(args):
                result["cli_key"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --key 后需要提供 API Key 值"
                return result
        elif arg == "--no-mask":
            result["no_mask"] = True
            i += 1
        else:
            result["phones"].append(arg)
            i += 1

    if not result["phones"]:
        result["error"] = (
            "错误: 需要提供至少一个手机号码\n"
            "用法: python mobile_lookup.py [--key KEY] <手机号码> [...]\n"
            "示例: python mobile_lookup.py 13812345678\n"
            f"\n免费申请 API Key: {REGISTER_URL}"
        )

    return result


def main():
    args = sys.argv[1:]

    if not args:
        print("用法: python mobile_lookup.py [--key KEY] <手机号码> [手机号码2 ...]")
        print("示例: python mobile_lookup.py 13812345678")
        print("      python mobile_lookup.py 13812345678 13912345678 --no-mask")
        print("      python mobile_lookup.py 1381234")
        print("\n选项:")
        print("  --no-mask        显示完整号码（默认对中间4位脱敏）")
        print("  --key <KEY>      直接传入 API Key")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    parsed = parse_args(args)
    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_MOBILE_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_MOBILE_KEY=your_api_key")
        print("   3. 命令行参数: python mobile_lookup.py --key your_api_key <手机号码>")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    phones = parsed["phones"]
    no_mask = parsed["no_mask"]

    for phone in phones:
        err = validate_phone(phone)
        if err:
            print(f"❌ 号码格式错误 [{phone}]: {err}")
            sys.exit(1)

    results = []
    for phone in phones:
        res = query_mobile(phone, api_key)
        results.append(res)

    if len(results) == 1:
        item = results[0]
        if item["success"]:
            print_single_result(item["phone"], item["result"], no_mask=no_mask)
        else:
            print(f"❌ 查询失败: {item['error']}")
            sys.exit(1)
    else:
        failed = [r for r in results if not r["success"]]
        if failed:
            for f in failed:
                print(f"⚠️  [{mask_phone(f['phone'])}] 查询失败: {f['error']}")
        print_batch_table(results, no_mask=no_mask)


if __name__ == "__main__":
    main()
