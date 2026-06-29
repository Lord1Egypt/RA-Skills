#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币市场报告生成脚本
支持全市场概览和单币深度分析
"""

import json
import sys
import urllib.request
from datetime import datetime

def fetch_market_data():
    """从CoinGecko获取市场概览"""
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"❌ 获取市场数据失败: {e}", file=sys.stderr)
        return []

def format_report(data):
    """生成格式化报告"""
    if not data:
        print("❌ 无数据")
        return

    now = datetime.utcnow().strftime("%Y-%m-%d")

    # 涨幅榜
    gainers = sorted(data, key=lambda x: x.get("price_change_percentage_24h", 0) or 0, reverse=True)[:5]
    # 跌幅榜
    losers = sorted(data, key=lambda x: x.get("price_change_percentage_24h", 0) or 0)[:5]

    print(f"📊 加密市场日报 - {now}\n")

    print("🏆 涨幅榜：")
    for c in gainers:
        chg = c.get("price_change_percentage_24h", 0) or 0
        print(f"  {c['symbol'].upper()} +{chg:.1f}%" if chg >= 0 else f"  {c['symbol'].upper()} {chg:.1f}%")

    print("\n📉 跌幅榜：")
    for c in losers:
        chg = c.get("price_change_percentage_24h", 0) or 0
        print(f"  {c['symbol'].upper()} {chg:.1f}%" if chg < 0 else f"  {c['symbol'].upper()} +{chg:.1f}%")

    print(f"\n💰 总市值：${data[0].get('market_cap', 0)/1e12:.2f}T" if data else "")
    print(f"📊 恐惧贪婪指数：需额外API")

def format_analysis(coin_id):
    """单币深度分析"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&community_data=false&developer_data=false"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"❌ 获取{coin_id}数据失败: {e}")
        return

    md = data.get("market_data", {})
    print(f"🔍 {data.get('name', coin_id)} 深度分析\n")
    print(f"💰 当前价格：${md.get('current_price', {}).get('usd', 'N/A'):,.2f}")
    print(f"📈 24h涨跌：{md.get('price_change_percentage_24h', 0):.2f}%")
    print(f"📉 7d涨跌：{md.get('price_change_percentage_7d', 0):.2f}%")
    print(f"📊 30d涨跌：{md.get('price_change_percentage_30d', 0):.2f}%")
    print(f"🏆 市值排名：#{data.get('market_cap_rank', 'N/A')}")
    print(f"💎 市值：${md.get('market_cap', {}).get('usd', 0)/1e9:.1f}B")
    print(f"🔄 24h交易量：${md.get('total_volume', {}).get('usd', 0)/1e9:.1f}B")
    ath = md.get('ath', {}).get('usd', 0)
    ath_change = md.get('ath_change_percentage', {}).get('usd', 0)
    print(f"📈 ATH：${ath:,.2f} (距ATH {ath_change:.1f}%)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["overview", "analysis"], default="overview")
    parser.add_argument("--coin", default="ethereum")
    args = parser.parse_args()

    if args.type == "overview":
        data = fetch_market_data()
        format_report(data)
    else:
        format_analysis(args.coin)
