#!/usr/bin/env python3
"""
全球大宗商品行情获取模块
获取伦敦金、伦敦银、伦敦铜、纽约铂、布伦特原油的实时价格和涨跌幅

依赖: pip install akshare pandas
"""

import argparse
import sys
import time
from datetime import datetime
from typing import Optional
from functools import wraps

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("错误: 请先安装依赖库")
    print("pip install akshare pandas")
    sys.exit(1)


# ============================================================
# 品种配置
# ============================================================

COMMODITY_CONFIG = {
    "gold": {
        "name": "伦敦金",
        "name_en": "London Gold (XAU)",
        "icon": "🟡",
        "unit": "美元/盎司",
        "ak_symbol": "XAU",
    },
    "silver": {
        "name": "伦敦银",
        "name_en": "London Silver (XAG)",
        "icon": "⚪",
        "unit": "美元/盎司",
        "ak_symbol": "XAG",
    },
    "copper": {
        "name": "伦敦铜",
        "name_en": "LME Copper",
        "icon": "🟤",
        "unit": "美元/吨",
        "ak_symbol": "CAD",
    },
    "platinum": {
        "name": "纽约铂",
        "name_en": "NYMEX Platinum",
        "icon": "🔘",
        "unit": "美元/盎司",
        "ak_symbol": "XPT",
    },
    "oil": {
        "name": "布伦特原油",
        "name_en": "Brent Crude Oil",
        "icon": "🛢️",
        "unit": "美元/桶",
        "ak_symbol": "OIL",
    },
}


def safe_float(value) -> Optional[float]:
    """安全转换为浮点数"""
    if value is None or value == '' or value == '--':
        return None
    try:
        if pd.isna(value):
            return None
        if isinstance(value, str):
            value = value.replace('%', '').replace(',', '')
        return round(float(value), 4)
    except (ValueError, TypeError):
        return None


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """网络请求重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
            return {"error": f"重试{max_retries}次后失败: {str(last_error)}"}
        return wrapper
    return decorator


# ============================================================
# 数据获取函数
# ============================================================

@retry_on_failure(max_retries=2, delay=1.0)
def fetch_commodity_data(ak_symbol: str) -> dict:
    """
    通过 akshare 的 futures_foreign_hist 接口获取外盘期货历史行情数据。
    获取最近两个交易日的数据，用于计算当日涨跌幅。

    参数:
        ak_symbol: akshare 外盘期货品种代码，如 XAU, XAG, CAD, XPT, OIL

    返回:
        包含 latest_price, open, high, low, prev_close, change, change_pct 的字典
    """
    df = ak.futures_foreign_hist(symbol=ak_symbol)
    if df is None or df.empty:
        return {"error": f"接口返回空数据 (symbol={ak_symbol})"}

    # 取最后一行作为当日数据
    latest = df.iloc[-1]
    result = {
        "date": str(latest.get("date", "")),
        "latest_price": safe_float(latest.get("close")),
        "open": safe_float(latest.get("open")),
        "high": safe_float(latest.get("high")),
        "low": safe_float(latest.get("low")),
    }

    # 取倒数第二行作为前一交易日数据，计算涨跌
    if len(df) >= 2:
        prev = df.iloc[-2]
        prev_close = safe_float(prev.get("close"))
        result["prev_close"] = prev_close
        if result["latest_price"] is not None and prev_close is not None and prev_close != 0:
            result["change"] = round(result["latest_price"] - prev_close, 4)
            result["change_pct"] = round(result["change"] / prev_close * 100, 2)

    return result


# ============================================================
# 主要功能函数
# ============================================================

def fetch_all_commodities() -> dict:
    """获取所有品种的行情数据"""
    result = {
        "fetch_time": datetime.now().isoformat(),
        "commodities": [],
        "summary": {
            "up_count": 0,
            "down_count": 0,
            "flat_count": 0,
            "error_count": 0,
        }
    }

    for symbol, config in COMMODITY_CONFIG.items():
        print(f"  正在获取 {config['name']} ...", file=sys.stderr)

        data = fetch_commodity_data(config["ak_symbol"])

        commodity = {
            "name": config["name"],
            "name_en": config["name_en"],
            "icon": config["icon"],
            "symbol": symbol,
            "unit": config["unit"],
        }

        if "error" in data:
            commodity["error"] = data["error"]
            commodity["status"] = "error"
            result["summary"]["error_count"] += 1
        else:
            commodity.update(data)
            # 判断涨跌状态
            change_pct = data.get("change_pct")
            if change_pct is not None:
                if change_pct > 0:
                    commodity["status"] = "up"
                    result["summary"]["up_count"] += 1
                elif change_pct < 0:
                    commodity["status"] = "down"
                    result["summary"]["down_count"] += 1
                else:
                    commodity["status"] = "flat"
                    result["summary"]["flat_count"] += 1
            else:
                commodity["status"] = "unknown"

        result["commodities"].append(commodity)
        time.sleep(0.3)  # 避免请求过快

    # 生成市场情绪判断
    up = result["summary"]["up_count"]
    down = result["summary"]["down_count"]
    if up > down:
        result["summary"]["market_sentiment"] = "偏多"
    elif down > up:
        result["summary"]["market_sentiment"] = "偏空"
    else:
        result["summary"]["market_sentiment"] = "震荡"

    return result


def fetch_single_commodity(commodity: str) -> dict:
    """获取单个品种的行情数据"""
    if commodity not in COMMODITY_CONFIG:
        return {"error": f"不支持的品种: {commodity}，支持: {', '.join(COMMODITY_CONFIG.keys())}"}

    config = COMMODITY_CONFIG[commodity]
    print(f"  正在获取 {config['name']} ...", file=sys.stderr)

    data = fetch_commodity_data(config["ak_symbol"])

    result = {
        "fetch_time": datetime.now().isoformat(),
        "commodity": {
            "name": config["name"],
            "name_en": config["name_en"],
            "icon": config["icon"],
            "symbol": commodity,
            "unit": config["unit"],
        }
    }

    if "error" in data:
        result["commodity"]["error"] = data["error"]
        result["commodity"]["status"] = "error"
    else:
        result["commodity"].update(data)
        change_pct = data.get("change_pct")
        if change_pct is not None:
            if change_pct > 0:
                result["commodity"]["status"] = "up"
            elif change_pct < 0:
                result["commodity"]["status"] = "down"
            else:
                result["commodity"]["status"] = "flat"

    return result


def format_briefing(data: dict) -> str:
    """将行情数据格式化为 Markdown 简报"""
    lines = []
    lines.append("## 📊 大宗商品行情简报")
    lines.append("")
    lines.append(f"> 数据时间：{data.get('fetch_time', 'N/A')}")
    lines.append("")
    lines.append("| 品种 | 最新价 | 涨跌幅 | 涨跌额 | 今开 | 最高 | 最低 | 单位 |")
    lines.append("|------|--------|--------|--------|------|------|------|------|")

    for c in data.get("commodities", []):
        if c.get("status") == "error":
            lines.append(f"| {c['icon']} {c['name']} | ⚠️ 获取失败 | - | - | - | - | - | {c['unit']} |")
            continue

        price = c.get("latest_price", "-")
        change_pct = c.get("change_pct")
        change = c.get("change")
        open_p = c.get("open", "-")
        high = c.get("high", "-")
        low = c.get("low", "-")

        # 格式化涨跌幅
        if change_pct is not None:
            pct_str = f"+{change_pct}%" if change_pct >= 0 else f"{change_pct}%"
            if change_pct > 0:
                pct_str = f"🔺 {pct_str}"
            elif change_pct < 0:
                pct_str = f"🔻 {pct_str}"
        else:
            pct_str = "-"

        # 格式化涨跌额
        if change is not None:
            change_str = f"+{change}" if change >= 0 else f"{change}"
        else:
            change_str = "-"

        # 格式化价格
        price_str = f"{price:,.2f}" if isinstance(price, (int, float)) else str(price)
        open_str = f"{open_p:,.2f}" if isinstance(open_p, (int, float)) else str(open_p)
        high_str = f"{high:,.2f}" if isinstance(high, (int, float)) else str(high)
        low_str = f"{low:,.2f}" if isinstance(low, (int, float)) else str(low)

        lines.append(f"| {c['icon']} {c['name']} | {price_str} | {pct_str} | {change_str} | {open_str} | {high_str} | {low_str} | {c['unit']} |")

    lines.append("")

    # 市场摘要
    summary = data.get("summary", {})
    lines.append(f"**市场情绪：{summary.get('market_sentiment', 'N/A')}** "
                 f"（上涨 {summary.get('up_count', 0)} | "
                 f"下跌 {summary.get('down_count', 0)} | "
                 f"持平 {summary.get('flat_count', 0)}）")

    if summary.get("error_count", 0) > 0:
        lines.append(f"\n⚠️ 有 {summary['error_count']} 个品种数据获取失败")

    lines.append("")
    lines.append("*数据仅供参考，不构成投资建议。*")

    return "\n".join(lines)


def format_single(data: dict) -> str:
    """将单品种行情数据格式化为文本简报"""
    lines = []
    c = data.get("commodity", {})
    lines.append(f"## {c.get('icon', '')} {c.get('name', '')} ({c.get('name_en', '')})")
    lines.append("")
    lines.append(f"> 数据时间：{data.get('fetch_time', 'N/A')}")
    lines.append("")

    if c.get("status") == "error":
        lines.append(f"⚠️ 数据获取失败：{c.get('error', '未知错误')}")
        return "\n".join(lines)

    price = c.get("latest_price", "-")
    change_pct = c.get("change_pct")
    change = c.get("change")
    open_p = c.get("open", "-")
    high = c.get("high", "-")
    low = c.get("low", "-")
    prev_close = c.get("prev_close", "-")
    unit = c.get("unit", "")

    price_str = f"{price:,.2f}" if isinstance(price, (int, float)) else str(price)

    if change_pct is not None:
        pct_str = f"+{change_pct}%" if change_pct >= 0 else f"{change_pct}%"
        arrow = "🔺" if change_pct > 0 else ("🔻" if change_pct < 0 else "➖")
        pct_str = f"{arrow} {pct_str}"
    else:
        pct_str = "-"

    if change is not None:
        change_str = f"+{change}" if change >= 0 else f"{change}"
    else:
        change_str = "-"

    lines.append(f"- **最新价**: {price_str} {unit}")
    lines.append(f"- **涨跌幅**: {pct_str}")
    lines.append(f"- **涨跌额**: {change_str}")
    lines.append(f"- **今开**: {open_p:,.2f} {unit}" if isinstance(open_p, (int, float)) else f"- **今开**: {open_p}")
    lines.append(f"- **最高**: {high:,.2f} {unit}" if isinstance(high, (int, float)) else f"- **最高**: {high}")
    lines.append(f"- **最低**: {low:,.2f} {unit}" if isinstance(low, (int, float)) else f"- **最低**: {low}")
    lines.append(f"- **昨收**: {prev_close:,.2f} {unit}" if isinstance(prev_close, (int, float)) else f"- **昨收**: {prev_close}")

    if c.get("note"):
        lines.append(f"\n📝 {c['note']}")

    lines.append("")
    lines.append("*数据仅供参考，不构成投资建议。*")

    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="全球大宗商品行情获取工具")
    parser.add_argument("--mode", type=str, default="briefing",
                        choices=["briefing", "single"],
                        help="运行模式: briefing=全部品种简报, single=单品种查询 (默认: briefing)")
    parser.add_argument("--commodity", type=str,
                        choices=["gold", "silver", "copper", "platinum", "oil"],
                        help="单品种查询时指定品种")
    args = parser.parse_args()

    if args.mode == "single":
        if not args.commodity:
            print("错误: 单品种查询模式需要指定 --commodity 参数", file=sys.stderr)
            sys.exit(1)
        result = fetch_single_commodity(args.commodity)
    else:
        result = fetch_all_commodities()

    # 输出
    if args.mode == "briefing":
        output = format_briefing(result)
    else:
        output = format_single(result)

    print(output)


if __name__ == "__main__":
    main()
