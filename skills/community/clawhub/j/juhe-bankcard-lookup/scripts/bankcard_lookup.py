#!/usr/bin/env python3
"""
银行卡类型及归属地查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询银行卡号的发卡银行、卡类型、归属地、客服电话等信息

用法:
    python bankcard_lookup.py <银行卡号>
    python bankcard_lookup.py 6228480402564890018
    python bankcard_lookup.py 6228480402564890018 6222021234567890123   # 批量查询

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_BANKCARDCODE_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_BANKCARDCODE_KEY=your_api_key
    3. 直接传参: python bankcard_lookup.py --key your_api_key <卡号>

免费申请 API Key: https://www.juhe.cn/docs/api/id/305
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://apis.juhe.cn/bankcardcore/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/305"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_BANKCARDCODE_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_BANKCARDCODE_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_bankcard(bankcard: str) -> str | None:
    """校验银行卡号格式，返回错误信息或 None"""
    if not bankcard:
        return "银行卡号不能为空"
    if not bankcard.isdigit():
        return "银行卡号必须为纯数字"
    if len(bankcard) < 15 or len(bankcard) > 19:
        return "银行卡号长度应为15-19位"
    return None


def query_bankcard(bankcard: str, api_key: str) -> dict:
    """查询单个银行卡信息"""
    bankcard = bankcard.strip()

    err = validate_bankcard(bankcard)
    if err:
        return {"bankcard": bankcard, "success": False, "error": err}

    params = urllib.parse.urlencode({"key": api_key, "bankcard": bankcard})
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"bankcard": bankcard, "success": False, "error": f"网络请求失败: {e}"}

    if data.get("error_code") == 0:
        r = data.get("result", {})
        return {
            "bankcard": r.get("bankcard", bankcard),
            "success": True,
            "bankname": r.get("bankname", ""),
            "abbreviation": r.get("abbreviation", ""),
            "cardtype": r.get("cardtype", ""),
            "nature": r.get("nature", ""),
            "province": r.get("province", ""),
            "city": r.get("city", ""),
            "card_bin": r.get("card_bin", ""),
            "bin_digits": r.get("bin_digits", ""),
            "card_digits": r.get("card_digits", ""),
            "isLuhn": r.get("isLuhn", ""),
            "banklogo": r.get("banklogo", ""),
            "weburl": r.get("weburl", ""),
            "kefu": r.get("kefu", ""),
        }

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（请求次数超限，请升级套餐）"
    elif error_code == 230501:
        hint = "（数据源超时，请稍后重试）"
    elif error_code == 230502:
        hint = "（银行卡号错误，请检查卡号）"
    elif error_code == 230503:
        hint = "（查询异常，请稍后重试）"
    return {
        "bankcard": bankcard,
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def format_result_line(result: dict) -> str:
    """格式化单条查询结果（多行）"""
    bc = result["bankcard"]
    if not result["success"]:
        return f"❌ {bc}  {result.get('error', '未知错误')}"

    bank = result.get("bankname", "")
    abbr = result.get("abbreviation", "")
    abbr_str = f"({abbr})" if abbr else ""
    cardtype = result.get("cardtype", "")
    nature = result.get("nature", "")
    province = result.get("province", "")
    city = result.get("city", "")
    location = " ".join(p for p in [province, city] if p)
    kefu = result.get("kefu", "")
    weburl = result.get("weburl", "")

    line1 = f"💳 {bc}  {bank}{abbr_str} {cardtype}"
    if nature:
        line1 += f"  {nature}"
    if location:
        line1 += f"  {location}"

    extras = []
    if kefu:
        extras.append(f"客服电话: {kefu}")
    if weburl:
        extras.append(f"官网: {weburl}")

    if extras:
        line2 = "   " + "  ".join(extras)
        return f"{line1}\n{line2}"
    return line1


def print_table(results: list) -> None:
    """以表格形式输出批量查询结果"""
    headers = ["银行卡号", "发卡银行", "简称", "卡类型", "省份", "城市", "客服", "备注"]

    rows = []
    for r in results:
        if not r["success"]:
            rows.append([r["bankcard"], "-", "-", "-", "-", "-", "-", r.get("error", "查询失败")])
        else:
            rows.append([
                r["bankcard"],
                r.get("bankname", ""),
                r.get("abbreviation", ""),
                r.get("cardtype", ""),
                r.get("province", ""),
                r.get("city", ""),
                r.get("kefu", ""),
                "✓",
            ])

    col_widths = [len(h) * 2 for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            width = sum(2 if ord(c) > 127 else 1 for c in str(cell))
            col_widths[i] = max(col_widths[i], width)

    def pad(text, width):
        actual = sum(2 if ord(c) > 127 else 1 for c in str(text))
        return str(text) + " " * max(0, width - actual)

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_row = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        print("| " + " | ".join(pad(cell, col_widths[i]) for i, cell in enumerate(row)) + " |")
    print(sep)


def main():
    args = sys.argv[1:]
    cli_key = None

    if "--key" in args:
        idx = args.index("--key")
        if idx + 1 < len(args):
            cli_key = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("错误: --key 后需要提供 API Key 值")
            sys.exit(1)

    if not args:
        print("用法: python bankcard_lookup.py [--key YOUR_KEY] <银行卡号> [银行卡号2 ...]")
        print("示例: python bankcard_lookup.py 6228480402564890018")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_BANKCARDCODE_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_BANKCARDCODE_KEY=your_api_key")
        print("   3. 命令行参数: python bankcard_lookup.py --key your_api_key <卡号>")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    results = [query_bankcard(bc, api_key) for bc in args]

    if len(results) == 1:
        print(format_result_line(results[0]))
        print()
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(f"共查询 {len(results)} 张银行卡:\n")
        print_table(results)
        print()
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
