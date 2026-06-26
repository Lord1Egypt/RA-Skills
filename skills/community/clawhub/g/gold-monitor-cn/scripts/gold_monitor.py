#!/usr/bin/env python3
"""
黄金指标监控脚本
同时监控国内黄金ETF + 国际黄金相关指标

用法: python3 gold_monitor.py
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def print_section(title):
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print("="*60)

def main():
    print(f"\n{'🥇'*20}")
    print(f"  黄金指标监控面板")
    print(f"  更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'🥇'*20}")

    # ─────────────────────────────────────────────
    # 1. 国内黄金ETF
    # ─────────────────────────────────────────────
    print_section("【国内黄金ETF】")
    try:
        df_etf = ak.fund_etf_spot_em()
        gold_etfs = df_etf[df_etf['名称'].str.contains('黄金ETF', na=False)]
        result = gold_etfs[['代码', '名称', '最新价', '涨跌幅', '成交额']].head(10)
        result['涨跌幅'] = result['涨跌幅'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
        result['成交额'] = result['成交额'].apply(lambda x: f"{x/1e9:.2f}亿" if pd.notna(x) else "N/A")
        print(result.to_string(index=False))
    except Exception as e:
        print(f"❌ ETF数据获取失败: {e}")

    # ─────────────────────────────────────────────
    # 2. 国内现货黄金基准价（上海金交所）
    # ─────────────────────────────────────────────
    print_section("【上海金交所现货黄金基准价】(AU9999)")
    try:
        df_sge = ak.spot_golden_benchmark_sge()
        latest = df_sge.tail(5).copy()
        latest['晚盘价'] = latest['晚盘价'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        latest['早盘价'] = latest['早盘价'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        print(latest.to_string(index=False))
        print("💡 注: AU9999现货价单位为 元/克")
    except Exception as e:
        print(f"❌ SGE数据获取失败: {e}")

    # ─────────────────────────────────────────────
    # 3. 国际黄金期货（COMEX黄金主力）
    # ─────────────────────────────────────────────
    print_section("【国际黄金期货 COMEX GC主力】")
    try:
        df_intl = ak.futures_global_spot_em()
        # 主力合约（当月连续）
        gold_main = df_intl[df_intl['名称'] == 'COMEX黄金']
        if not gold_main.empty:
            row = gold_main.iloc[0]
            price = row.get('最新价', 'N/A')
            change = row.get('涨跌幅', 0)
            change_amt = row.get('涨跌额', 0)
            print(f"  主力合约 GC00Y:")
            print(f"    最新价: ${price} /盎司" if pd.notna(price) else "    最新价: N/A")
            print(f"    涨跌额: ${change_amt:+.2f}" if pd.notna(change_amt) else "    涨跌额: N/A")
            print(f"    涨跌幅: {change:+.2f}%" if pd.notna(change) else "    涨跌幅: N/A")
        else:
            # 展示近期合约
            gold_futures = df_intl[df_intl['名称'].str.contains('COMEX黄金', na=False)]
            gold_active = gold_futures[gold_futures['代码'].isin(['GC27M', 'GC27K', 'GC27J'])]
            if not gold_active.empty:
                print(gold_active[['代码', '名称', '最新价', '涨跌额', '涨跌幅']].head(3).to_string(index=False))
    except Exception as e:
        print(f"❌ 国际黄金期货获取失败: {e}")

    # ─────────────────────────────────────────────
    # 4. 美元指数
    # ─────────────────────────────────────────────
    print_section("【美元指数 DXY】")
    try:
        df_forex = ak.forex_spot_em()
        dxy = df_forex[df_forex['名称'].str.contains('美元指数', na=False, case=False)]
        if not dxy.empty:
            row = dxy.iloc[0]
            price = row.get('最新价', 'N/A')
            change = row.get('涨跌幅', 0)
            print(f"  美元指数: {price}" if pd.notna(price) else "  美元指数: N/A")
            print(f"  涨跌幅: {change:+.2f}%" if pd.notna(change) else "  涨跌幅: N/A")
            if pd.notna(change):
                if change > 0:
                    print("  📈 美元走强 → 黄金承压")
                else:
                    print("  📉 美元走弱 → 黄金利好")
        else:
            print("  未找到美元指数数据")
    except Exception as e:
        print(f"❌ 美元指数获取失败: {e}")

    # ─────────────────────────────────────────────
    # 5. 人民币汇率 USD/CNY
    # ─────────────────────────────────────────────
    print_section("【人民币汇率 USD/CNY】")
    try:
        df_forex = ak.forex_spot_em()
        usdcny = df_forex[df_forex['名称'].str.contains('美元人民币', na=False, case=False)]
        if not usdcny.empty:
            row = usdcny.iloc[0]
            price = row.get('最新价', 'N/A')
            change = row.get('涨跌幅', 0)
            print(f"  USD/CNY: {price}" if pd.notna(price) else "  USD/CNY: N/A")
            print(f"  涨跌幅: {change:+.2f}%" if pd.notna(change) else "  涨跌幅: N/A")
            if pd.notna(change):
                if change > 0:
                    print("  📈 人民币贬值 → 国内金价被动支撑")
                else:
                    print("  📉 人民币升值 → 国内金价相对走弱")
        else:
            print("  未找到汇率数据")
    except Exception as e:
        print(f"❌ 汇率获取失败: {e}")

    # ─────────────────────────────────────────────
    # 6. A股黄金矿业股（产业联动）
    # ─────────────────────────────────────────────
    print_section("【A股黄金矿业股】(产业联动参考)")
    try:
        df_stock = ak.stock_zh_a_spot_em()
        gold_mining = df_stock[df_stock['名称'].str.contains(
            '黄金|中金黄金|山东黄金|赤峰黄金|湖南黄金|西部黄金|招金黄金|中国黄金', 
            na=False
        )]
        result = gold_mining[['代码', '名称', '最新价', '涨跌幅', '成交额']].head(10)
        result['涨跌幅'] = result['涨跌幅'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
        result['成交额'] = result['成交额'].apply(lambda x: f"{x/1e9:.2f}亿" if pd.notna(x) else "N/A")
        print(result.to_string(index=False))
        print("\n💡 矿业股大涨通常为金价上涨的领先信号")
    except Exception as e:
        print(f"❌ 黄金矿业股获取失败: {e}")

    # ─────────────────────────────────────────────
    # 综合判断
    # ─────────────────────────────────────────────
    print_section("📌 综合判断要点")
    print("""
  1. 美元指数强弱 → 最核心的黄金反向指标
  2. 黄金矿业股涨幅 → 产业资本态度，领先现货1-2天
  3. ETF成交量是否放大 → 资金大幅入场信号
  4. 内外盘价差 → 正常约3-5%，过大可能有套利机会
  5. 溢价率 → ETF场内价格vs净值，过高需警惕回调风险
    """)

    print("\n" + "="*60)
    print("⚠️  数据仅供参考，不构成投资建议")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
