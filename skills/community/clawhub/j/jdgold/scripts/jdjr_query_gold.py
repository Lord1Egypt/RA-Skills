#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
黄金行情查询工具
支持查询上海黄金交易所、伦敦金、期货黄金等实时行情
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

from jdjr_config import get_source_attribution, get_source_metadata, get_claw_headers, set_claw


# 黄金代码映射 (支持的品种)
GOLD_CODES = {
    # 黄金
    "Au99.99": "SGE-Au99.99",       # 黄金99999
    "Au99.95": "SGE-Au99.95",       # Au9995
    "Au100g": "SGE-Au100g",         # 100g金条
    "Au(T+D)": "SGE-Au(T+D)",       # 黄金T+D
    "mAu(T+D)": "SGE-mAu(T+D)",     # Mini黄金延期
    "iAu99.99": "SGE-iAu99.99",     # iAu9999
    
    # 白银
    "Ag(T+D)": "SGE-Ag(T+D)",       # 白银延期
    "Ag99.99": "SGE-Ag99.99",       # 白银9999
    
    # 铂金
    "Pt99.95": "SGE-Pt99.95",       # Pt9995
    
    # 期货
    "au2602": "SHFE-au2602",        # 沪金2602
    
    # 伦敦金 (暂不支持)
    # "XAUUSD": "WG-XAUUSD",         # 伦敦金
}


BASE_URL = "https://ms.jr.jd.com/gw2/generic/ugActs/h5/m"


def query_gold(stock_code: str) -> dict:
    """查询黄金行情"""
    # 如果传入的是简写代码，转换为完整代码
    if stock_code in GOLD_CODES:
        stock_code = GOLD_CODES[stock_code]
    
    payload = {"paramMap": {"stockCode": stock_code}}
    
    req = urllib.request.Request(
        f"{BASE_URL}/queryStockData",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **get_claw_headers()},
        method="POST",
    )
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if not result.get("success") or result.get("resultCode") != 0:
        return {
            "success": False,
            "error": result.get("resultMsg", "查询失败"),
        }
    
    data = result.get("resultData", {}).get("data", {})
    
    # 解析数据
    current_price = float(data.get("currentPrice", 0))
    open_price = float(data.get("open", 0))
    change_price = float(data.get("changePrice", 0))
    change_ratio = float(data.get("changeRatio", 0))
    
    # 判断单位
    unit = "元/克"
    if "Ag" in stock_code and "T+D" not in stock_code:
        unit = "元/千克"  # 白银
    elif "Pt" in stock_code:
        unit = "元/克"   # 铂金
    elif "SHFE" in stock_code:
        unit = "元/克"   # 期货黄金
    
    return {
        "success": True,
        "data": {
            "stockCode": data.get("stockCode", ""),
            "stockName": data.get("stockName", ""),
            "uCode": stock_code,
            "unit": unit,
            "currentPrice": f"{current_price:.2f}",
            "open": f"{open_price:.2f}",
            "closedYesterday": data.get("closedYesterday", ""),
            "changePrice": f"{change_price:+.2f}",
            "changeRatio": f"{change_ratio*100:+.2f}%",
            "maxPrice": data.get("maxPrice", ""),
            "minPrice": data.get("minPrice", ""),
            "volume": data.get("volume", ""),
            "amount": data.get("amount", ""),
        },
        "source": get_source_metadata("GOLD"),
    }


def format_output(data: dict) -> str:
    """格式化输出"""
    if not data.get("success"):
        return f"❌ 查询失败: {data.get('error')}"
    
    d = data.get("data", {})
    unit = d.get("unit", "元/克")
    
    output = f"""
**{d.get('stockName', '')}** 实时行情：

| 项目 | 数据 |
|------|------|
| **现价** | {d.get('currentPrice')} {unit} |
| **涨跌额** | {d.get('changePrice')} 元 |
| **涨跌幅** | {d.get('changeRatio')} |
| **今开** | {d.get('open')} {unit} |
| **昨收** | {d.get('closedYesterday')} {unit} |
| **最高** | {d.get('maxPrice')} {unit} |
| **最低** | {d.get('minPrice')} {unit} |
| **成交量** | {d.get('volume')} 手 |

---
{get_source_attribution("GOLD")}
"""
    return output.strip()


def list_gold_codes():
    """列出支持的黄金品种"""
    print("\n支持的品种：")
    print("-" * 50)
    print(f"{'名称':<15} {'代码':<20} {'单位'}")
    print("-" * 50)
    
    categories = {
        "黄金": ["Au99.99", "Au99.95", "Au100g", "Au(T+D)", "mAu(T+D)", "iAu99.99"],
        "白银": ["Ag(T+D)", "Ag99.99"],
        "铂金": ["Pt99.95"],
        "期货": ["au2602"],
    }
    
    for cat, codes in categories.items():
        print(f"\n【{cat}】")
        for code in codes:
            full_code = GOLD_CODES.get(code, code)
            print(f"  {code:<15} {full_code:<20}")
    
    print("-" * 50)
    print("\n注意: 伦敦金(WG-XAUUSD)暂不支持")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="查询黄金实时行情",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 jdjr_query_gold.py Au99.95        # 查询 Au9995
  python3 jdjr_query_gold.py 黄金T+D        # 查询黄金T+D
  python3 jdjr_query_gold.py --list         # 列出所有支持的品种
        """
    )
    parser.add_argument("code", nargs="?", help="黄金代码或名称")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有支持的品种")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args()
    set_claw(args.claw)
    
    if args.list:
        list_gold_codes()
        return 0
    
    if not args.code:
        parser.print_help()
        print("\n可用黄金品种:")
        list_gold_codes()
        return 1
    
    code = args.code.strip()
    
    # 检查是否列出
    if code in ["黄金", "金", "list", "--list"]:
        list_gold_codes()
        return 0
    
    try:
        result = query_gold(code)
        print(format_output(result))
        return 0
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print("您的账户已被限制访问，如有疑问请联系京东黄金客服")
        else:
            print(f"❌ HTTP 错误: {exc.code}")
        return 1
    except urllib.error.URLError as exc:
        print(f"❌ 网络错误: {exc.reason}")
        return 1
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
