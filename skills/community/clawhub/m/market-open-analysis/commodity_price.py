#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
commodity_price.py - 国际商品价格查询 Skill
使用 CommodityPriceAPI 获取 WTI 原油、黄金等国际商品价格
"""

import requests
import json
import sys
import os
from datetime import datetime

# API 配置
# ⚠️ 请在使用前配置您的 CommodityPriceAPI Key！
# 获取方式：https://commoditypriceapi.com
API_KEY = "YOUR_COMMODITY_PRICE_API_KEY_HERE"  # ← 请修改这里
API_BASE_URL = "https://api.commoditypriceapi.com/v2"

# API 端点
ENDPOINTS = {
    "latest": "/rates/latest",      # 最新价格
    "historical": "/rates/historical",  # 历史价格
    "range": "/rates/range"         # 价格范围
}

# 支持的商品代码
SUPPORTED_COMMODITIES = {
    "XAU": {"name": "黄金", "unit": "盎司", "type": "贵金属"},
    "XAG": {"name": "白银", "unit": "盎司", "type": "贵金属"},
    "XPT": {"name": "铂金", "unit": "盎司", "type": "贵金属"},
    "XPD": {"name": "钯金", "unit": "盎司", "type": "贵金属"},
    "WTIOIL-FUT": {"name": "WTI 原油", "unit": "桶", "type": "能源"},
    "BRENT-FUT": {"name": "布伦特原油", "unit": "桶", "type": "能源"},
    "NG-FUT": {"name": "天然气", "unit": "MMBtu", "type": "能源"},
    "COPPER-FUT": {"name": "铜", "unit": "磅", "type": "金属"},
    "CORN-FUT": {"name": "玉米", "unit": "蒲式耳", "type": "农产品"},
    "WHEAT-FUT": {"name": "小麦", "unit": "蒲式耳", "type": "农产品"},
    "SOYBEAN-FUT": {"name": "大豆", "unit": "蒲式耳", "type": "农产品"},
    "SUGAR-FUT": {"name": "糖", "unit": "磅", "type": "农产品"},
    "COFFEE-FUT": {"name": "咖啡", "unit": "磅", "type": "农产品"},
    "COTTON-FUT": {"name": "棉花", "unit": "磅", "type": "农产品"},
}


def get_commodity_prices(symbols=None, base="USD"):
    """
    获取商品最新价格
    
    Args:
        symbols: 商品代码列表，如 ["XAU", "WTIOIL-FUT"]，None 则获取所有
        base: 基础货币，默认 USD
    
    Returns:
        dict: 价格数据
    """
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Accept": "application/json"
        }
        
        # 如果没有指定 symbols，使用默认的原油和黄金
        if symbols is None:
            symbols = ["XAU", "WTIOIL-FUT"]
        
        params = {
            "base": base,
            "symbols": ",".join(symbols)
        }
        
        url = f"{API_BASE_URL}{ENDPOINTS['latest']}"
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            return {
                "success": True,
                "timestamp": result.get("timestamp"),
                "base": result.get("base"),
                "rates": result.get("rates", {}),
                "metadata": result.get("metadata", {})
            }
        else:
            return {
                "success": False,
                "error": "API 返回失败"
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败：{str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON 解析失败：{str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误：{str(e)}"
        }


def get_historical_prices(date, symbols=None, base="USD"):
    """
    获取历史价格
    
    Args:
        date: 日期（YYYY-MM-DD 格式）
        symbols: 商品代码列表
        base: 基础货币，默认 USD
    
    Returns:
        dict: 历史价格数据
    """
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Accept": "application/json"
        }
        
        if symbols is None:
            symbols = ["XAU", "WTIOIL-FUT"]
        
        params = {
            "base": base,
            "symbols": ",".join(symbols),
            "date": date
        }
        
        url = f"{API_BASE_URL}{ENDPOINTS['historical']}"
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            return {
                "success": True,
                "date": date,
                "base": result.get("base", "USD"),
                "rates": result.get("rates", {}),
                "historical": True
            }
        else:
            return {
                "success": False,
                "error": "API 返回失败"
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败：{str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON 解析失败：{str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误：{str(e)}"
        }


def get_price_range(start_date, end_date, symbols=None, base="USD"):
    """
    获取价格范围（历史区间）
    
    Args:
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        symbols: 商品代码列表
        base: 基础货币，默认 USD
    
    Returns:
        dict: 价格范围数据
    """
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Accept": "application/json"
        }
        
        if symbols is None:
            symbols = ["XAU", "WTIOIL-FUT"]
        
        params = {
            "base": base,
            "symbols": ",".join(symbols),
            "start_date": start_date,
            "end_date": end_date
        }
        
        url = f"{API_BASE_URL}{ENDPOINTS['range']}"
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            return {
                "success": True,
                "start_date": start_date,
                "end_date": end_date,
                "base": result.get("base"),
                "rates": result.get("rates", {}),
                "range": True
            }
        else:
            return {
                "success": False,
                "error": "API 返回失败"
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败：{str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON 解析失败：{str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误：{str(e)}"
        }


def format_price(price, symbol):
    """格式化价格显示"""
    commodity = SUPPORTED_COMMODITIES.get(symbol, {})
    unit = commodity.get("unit", "")
    name = commodity.get("name", symbol)
    
    # 根据价格范围决定小数位数
    if price >= 1000:
        return f"{price:,.0f}"
    elif price >= 100:
        return f"{price:,.2f}"
    else:
        return f"{price:,.4f}"


def format_result(data, output_format="text"):
    """
    格式化结果
    
    Args:
        data: API 返回的数据
        output_format: 输出格式 (text/json/markdown)
    
    Returns:
        str: 格式化后的文本
    """
    if not data.get("success"):
        return f"❌ 错误：{data.get('error', '未知错误')}"
    
    rates = data.get("rates", {})
    timestamp = data.get("timestamp", 0)
    date = data.get("date", "")
    base = data.get("base", "USD")
    is_historical = data.get("historical", False)
    is_range = data.get("range", False)
    
    # 转换时间戳
    if timestamp:
        dt = datetime.fromtimestamp(timestamp)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        time_str = date if date else "未知"
    
    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    elif output_format == "markdown":
        output = []
        output.append("## 💰 国际商品价格")
        output.append(f"\n📅 时间：{time_str}")
        output.append(f"💱 基础货币：{base}")
        output.append("")
        output.append("| 商品 | 价格 | 单位 |")
        output.append("|------|------|------|")
        
        for symbol, price_data in rates.items():
            commodity = SUPPORTED_COMMODITIES.get(symbol, {})
            name = commodity.get("name", symbol)
            unit = commodity.get("unit", "")
            
            # 处理历史价格（返回的是 dict）
            if isinstance(price_data, dict):
                close = price_data.get("close", 0)
                price_fmt = format_price(close, symbol)
                output.append(f"| {name} | ${price_fmt} (close) | {unit} |")
            else:
                price_fmt = format_price(price_data, symbol)
                output.append(f"| {name} | ${price_fmt} | {unit} |")
        
        return "\n".join(output)
    
    else:  # text
        output = []
        output.append("=" * 50)
        output.append("💰 国际商品价格")
        output.append("=" * 50)
        output.append(f"📅 时间：{time_str}")
        output.append(f"💱 基础货币：{base}")
        if is_historical:
            output.append("📜 历史价格")
        output.append("")
        
        for symbol, price_data in rates.items():
            commodity = SUPPORTED_COMMODITIES.get(symbol, {})
            name = commodity.get("name", symbol)
            unit = commodity.get("unit", "")
            
            # 处理历史价格（返回的是 dict）
            if isinstance(price_data, dict):
                close = price_data.get("close", 0)
                open_p = price_data.get("open", 0)
                high = price_data.get("high", 0)
                low = price_data.get("low", 0)
                price_fmt = format_price(close, symbol)
                output.append(f"{name}: ${price_fmt} / {unit} (O:${open_p}, H:${high}, L:${low}, C:${close})")
            else:
                price_fmt = format_price(price_data, symbol)
                output.append(f"{name}: ${price_fmt} / {unit}")
        
        output.append("")
        output.append("=" * 50)
        return "\n".join(output)


def get_price_summary(symbols=None):
    """
    获取简洁的价格摘要（用于快速查询）
    
    Args:
        symbols: 商品代码列表
    
    Returns:
        str: 简洁摘要
    """
    data = get_commodity_prices(symbols)
    
    if not data.get("success"):
        return f"❌ {data.get('error')}"
    
    rates = data.get("rates", {})
    summary = []
    
    for symbol in symbols or ["XAU", "WTIOIL-FUT"]:
        if symbol in rates:
            price = rates[symbol]
            commodity = SUPPORTED_COMMODITIES.get(symbol, {})
            name = commodity.get("name", symbol)
            unit = commodity.get("unit", "")
            price_fmt = format_price(price, symbol)
            summary.append(f"{name}: ${price_fmt}/{unit}")
    
    return ", ".join(summary)


def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="国际商品价格查询")
    parser.add_argument("symbols", nargs="*", help="商品代码（如 XAU, WTIOIL-FUT）")
    parser.add_argument("-f", "--format", choices=["text", "json", "markdown"], 
                        default="text", help="输出格式")
    parser.add_argument("-b", "--base", default="USD", help="基础货币")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有支持的商品")
    parser.add_argument("-d", "--date", help="历史日期（YYYY-MM-DD 格式）")
    parser.add_argument("--range", nargs=2, metavar=("START_DATE", "END_DATE"),
                        help="价格范围查询（YYYY-MM-DD YYYY-MM-DD）")
    
    args = parser.parse_args()
    
    if args.list:
        print("支持的商品代码：")
        print("")
        for code, info in SUPPORTED_COMMODITIES.items():
            print(f"  {code:15} {info['name']:10} ({info['type']}) - {info['unit']}")
        return
    
    # 如果没有指定 symbols，使用默认的原油和黄金
    symbols = args.symbols if args.symbols else ["XAU", "WTIOIL-FUT"]
    
    # 根据参数选择查询类型
    if args.date:
        print(f"查询历史价格：{args.date}")
        data = get_historical_prices(args.date, symbols, args.base)
    elif args.range:
        print(f"查询价格范围：{args.range[0]} 至 {args.range[1]}")
        data = get_price_range(args.range[0], args.range[1], symbols, args.base)
    else:
        print("查询最新价格")
        data = get_commodity_prices(symbols, args.base)
    
    # 格式化输出
    output = format_result(data, args.format)
    print(output)


if __name__ == "__main__":
    main()
