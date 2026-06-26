#!/usr/bin/env python3
"""
全球汇率查询换算脚本 — 由聚合数据 (juhe.cn) 提供数据支持
依据官方 API 80 文档：货币列表、实时汇率查询换算

用法:
    python exchange_rate.py --from USD --to CNY
    python exchange_rate.py --from USD --to CNY --amount 100
    python exchange_rate.py --list

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_EXCHANGE_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_EXCHANGE_KEY=your_api_key
    3. 直接传参: python exchange_rate.py --key your_api_key --from USD --to CNY

免费申请 API Key: https://www.juhe.cn/docs/api/id/80
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

# 官方 API 80 文档仅包含以下两个接口
LIST_API_URL = "http://op.juhe.cn/onebox/exchange/list"
CURRENCY_API_URL = "http://op.juhe.cn/onebox/exchange/currency"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/80"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_EXCHANGE_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_EXCHANGE_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def _request(url: str, params: dict) -> dict:
    """发起 HTTP GET 请求"""
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(full_url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error_code": -1, "reason": f"网络请求失败: {e}"}


def query_currency_list(api_key: str) -> dict:
    """查询支持的货币列表"""
    data = _request(LIST_API_URL, {"key": api_key})
    if data.get("error_code") == 0:
        return {"success": True, "data": data.get("result", {})}
    return {
        "success": False,
        "error_code": data.get("error_code", -1),
        "reason": data.get("reason", "查询失败"),
    }


def convert_currency(api_key: str, from_curr: str, to_curr: str) -> dict:
    """查询两种货币间的实时汇率"""
    from_curr = from_curr.strip().upper()
    to_curr = to_curr.strip().upper()
    if not from_curr or not to_curr:
        return {"success": False, "reason": "请提供 from 和 to 货币代码"}

    data = _request(CURRENCY_API_URL, {
        "key": api_key,
        "from": from_curr,
        "to": to_curr,
    })
    if data.get("error_code") == 0:
        result = data.get("result", {})
        # API 返回 list，每项含 currencyF, currencyT, exchange, updateTime
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict) and item.get("currencyF") == from_curr and item.get("currencyT") == to_curr:
                    return {
                        "success": True,
                        "data": item,
                        "rate": float(item.get("exchange") or item.get("result") or 0),
                        "updateTime": item.get("updateTime", ""),
                    }
        # 兼容 dict 或单一数值
        return {"success": True, "data": result, "raw": data}
    hint = ""
    if data.get("error_code") in (10001, 10002):
        hint = f"（请检查 API Key，免费申请：{REGISTER_URL}）"
    return {
        "success": False,
        "error_code": data.get("error_code", -1),
        "reason": f"{data.get('reason', '查询失败')}{hint}",
    }


def format_currency_list(result: dict) -> None:
    """格式化货币列表输出"""
    if not result:
        print("暂无货币列表数据")
        return

    # result 可能是 list 或 dict，如 {"0": {"code": "USD", "name": "美元"}}
    if isinstance(result, list):
        for i, item in enumerate(result):
            if isinstance(item, dict):
                print(f"  {item.get('code', '-')}: {item.get('name', item)}")
            else:
                print(f"  {item}")
    elif isinstance(result, dict):
        for k, v in result.items():
            if isinstance(v, dict):
                print(f"  {v.get('code', k)}: {v.get('name', v)}")
            else:
                print(f"  {k}: {v}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def format_convert_output(result: dict, from_curr: str, to_curr: str, amount: float = None) -> None:
    """格式化汇率换算输出"""
    rate = result.get("rate")
    if rate is None:
        data = result.get("data", result)
        if isinstance(data, (int, float)):
            rate = float(data)
        elif isinstance(data, dict):
            val = data.get("exchange") or data.get("rate") or data.get("result")
            rate = float(val) if val is not None else None

    if rate is None:
        print("查询成功，但无法解析汇率。原始返回：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    update_time = result.get("updateTime", "")
    print(f"💱 {from_curr} → {to_curr}")
    print(f"   汇率: 1 {from_curr} = {rate} {to_curr}")
    if update_time:
        print(f"   更新: {update_time}")

    if amount and amount > 0:
        converted = round(amount * rate, 2)
        print(f"   换算: {amount} {from_curr} = {converted} {to_curr}")


def main():
    args = sys.argv[1:]
    cli_key = None
    from_curr = None
    to_curr = None
    amount = None
    do_list = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--from", "-f") and i + 1 < len(args):
            from_curr = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--to", "-t") and i + 1 < len(args):
            to_curr = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--amount", "-a") and i + 1 < len(args):
            try:
                amount = float(args[i + 1])
            except ValueError:
                pass
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--list", "-l"):
            do_list = True
            args = args[:i] + args[i + 1:]
            continue
        i += 1

    if not do_list and not (from_curr and to_curr):
        print("用法: python exchange_rate.py [--key KEY] --from <货币> --to <货币> [--amount 数量]")
        print("      python exchange_rate.py [--key KEY] --list")
        print("\n示例: python exchange_rate.py --from USD --to CNY")
        print("      python exchange_rate.py --from USD --to CNY --amount 100")
        print(f"\n官方文档（仅含货币列表、实时汇率换算两个接口）: {REGISTER_URL}")
        sys.exit(0)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_EXCHANGE_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_EXCHANGE_KEY=your_api_key")
        print("   3. 命令行参数: python exchange_rate.py --key your_api_key --from USD --to CNY")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    if do_list:
        result = query_currency_list(api_key)
        if not result["success"]:
            print(f"❌ {result.get('reason', '查询失败')}")
            sys.exit(1)
        print("💱 支持的货币列表\n")
        format_currency_list(result.get("data", {}))
        print()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if from_curr and to_curr:
        result = convert_currency(api_key, from_curr, to_curr)
        if not result["success"]:
            print(f"❌ {result.get('reason', '查询失败')}")
            sys.exit(1)
        format_convert_output(result, from_curr, to_curr, amount)
        print()
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
