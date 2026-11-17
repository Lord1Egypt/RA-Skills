#!/usr/bin/env python3
"""
Market Signals — 市场技术信号扫描器（v1.1.0）

从价格数据计算技术指标信号：RSI、均线交叉、成交量异动、
ATR波动率、MACD、布林带、VWAP。支持支撑/阻力位识别、
多股票扫描、信号历史追踪、信号组合综合评分。

用法:
    python3 scripts/market_signals.py --file prices.csv
    python3 scripts/market_signals.py --file prices.csv --indicators rsi,ma,macd
    python3 scripts/market_signals.py --file prices.csv --scan
    python3 scripts/market_signals.py --file prices.csv --history
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ── 数据读取 ────────────────────────────────────────────

def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _col(values, idx):
    return values[idx] if idx < len(values) else "0"


def parse_float(val):
    try:
        return float(str(val).replace(",", "").replace(" ", ""))
    except (ValueError, TypeError):
        return 0.0


# ── 基础指标 ──────────────────────────────────────────

def compute_sma(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def compute_std(prices, period):
    """标准差。"""
    if len(prices) < period:
        return None
    mean = sum(prices[-period:]) / period
    variance = sum((p - mean) ** 2 for p in prices[-period:]) / period
    return math.sqrt(variance)


def compute_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(-period, 0):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return round(100 - 100 / (1 + rs), 1)


def compute_atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        return None
    trs = []
    for i in range(-period, 0):
        h = highs[i]; l = lows[i]; pc = closes[i-1]
        tr = max(h-l, abs(h-pc), abs(l-pc))
        trs.append(tr)
    return round(sum(trs) / period, 2)


def compute_macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow:
        return None, None
    ema_fast = sum(prices[-fast:]) / fast if len(prices) >= fast else 0
    ema_slow = sum(prices[-slow:]) / slow
    macd = ema_fast - ema_slow
    sig = sum(prices[-signal:]) / signal if len(prices) >= signal else 0
    return round(macd, 4), round(macd - sig, 4)


def compute_ema(prices, period):
    """指数移动平均。"""
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for p in prices[period:]:
        ema = (p - ema) * multiplier + ema
    return round(ema, 2)


# ── 布林带 ────────────────────────────────────────────

def compute_bollinger(prices, period=20, num_std=2):
    """布林带：中轨(MA20)、上轨/下轨(±2σ)、带宽、%b。"""
    if len(prices) < period:
        return None, None, None, None, None
    ma = compute_sma(prices, period)
    std = compute_std(prices, period)
    if ma is None or std is None:
        return None, None, None, None, None
    upper = round(ma + num_std * std, 2)
    lower = round(ma - num_std * std, 2)
    bandwidth = round((upper - lower) / ma * 100, 2) if ma > 0 else 0
    current = prices[-1]
    b_pct = round((current - lower) / (upper - lower), 3) if (upper - lower) > 0 else 0.5
    return round(ma, 2), upper, lower, bandwidth, b_pct


# ── VWAP ──────────────────────────────────────────────

def compute_vwap(prices, volumes):
    """成交量加权均价。"""
    if len(prices) < 1 or sum(abs(v) for v in volumes) == 0:
        return None
    vwap = sum(p * v for p, v in zip(prices, volumes)) / sum(abs(v) for v in volumes)
    return round(vwap, 2)


# ── 支撑/阻力位 ─────────────────────────────────────

def find_support_resistance(prices, lookback=20):
    """基于近期高低点识别支撑位和阻力位。"""
    if len(prices) < lookback:
        lookback = len(prices)
    recent = prices[-lookback:]
    high = max(recent)
    low = min(recent)
    # 寻找局部极值
    supports = []
    resistances = []
    for i in range(2, len(recent) - 2):
        if recent[i] < recent[i-1] and recent[i] < recent[i+1]:
            supports.append(recent[i])
        if recent[i] > recent[i-1] and recent[i] > recent[i+1]:
            resistances.append(recent[i])
    # 取最近的局部极值的均值
    s1 = round(sum(supports[-3:]) / len(supports[-3:]), 2) if supports else round(low, 2)
    r1 = round(sum(resistances[-3:]) / len(resistances[-3:]), 2) if resistances else round(high, 2)
    return s1, r1, round(low, 2), round(high, 2)


# ── 信号组合评分 ─────────────────────────────────────

def compute_composite_score(signals_dict):
    """多信号综合评分（0-100）。"""
    score = 50  # 中性起点
    details = []

    # RSI
    rsi = signals_dict.get("rsi")
    if rsi is not None:
        if rsi < 30:
            score += 15
            details.append("RSI超卖(+15)")
        elif rsi > 70:
            score -= 15
            details.append("RSI超买(-15)")
        elif 30 <= rsi <= 40:
            score += 8
            details.append("RSI偏低(+8)")
        elif 60 <= rsi <= 70:
            score -= 8
            details.append("RSI偏高(-8)")

    # 均线
    ma_signal = signals_dict.get("ma_signal", "")
    if "多头" in ma_signal:
        score += 20
        details.append("多头排列(+20)")
    elif "空头" in ma_signal:
        score -= 20
        details.append("空头排列(-20)")
    elif "偏强" in ma_signal:
        score += 8
        details.append("短线偏强(+8)")
    elif "偏弱" in ma_signal:
        score -= 8
        details.append("短线偏弱(-8)")

    # MACD
    macd_hist = signals_dict.get("macd_hist")
    if macd_hist is not None:
        if macd_hist > 0:
            score += 10
            details.append("MACD金叉(+10)")
        else:
            score -= 10
            details.append("MACD死叉(-10)")

    # 成交量
    vol_signal = signals_dict.get("vol_signal", "")
    if "放量↑↑" in vol_signal:
        score += 12
        details.append("放量↑↑(+12)")
    elif "放量↑" in vol_signal:
        score += 6
        details.append("放量↑(+6)")
    elif "缩量↓↓" in vol_signal:
        score -= 8
        details.append("缩量↓↓(-8)")

    # 布林带位置
    bb_pct = signals_dict.get("bb_pct")
    if bb_pct is not None:
        if bb_pct > 0.9:
            score -= 10
            details.append("布林上轨附近(-10)")
        elif bb_pct < 0.1:
            score += 12
            details.append("布林下轨附近(+12)")

    score = max(0, min(100, score))
    return score, details


def recommend(score):
    if score >= 75:
        return "买入"
    elif score >= 60:
        return "关注"
    elif score >= 40:
        return "观望"
    else:
        return "回避"


# ── 单股票分析（增强版） ──────────────────────────────

def analyze_stock(rows, name_col, price_col, vol_col, high_col, low_col,
                  indicators=None):
    """分析单只股票的全部技术信号。"""
    prices = [parse_float(r[price_col]) for r in rows if r.get(price_col)]
    volumes = [parse_float(r[vol_col]) for r in rows if r.get(vol_col)] if vol_col else []
    highs = [parse_float(r[high_col]) for r in rows if r.get(high_col)] if high_col else prices
    lows = [parse_float(r[low_col]) for r in rows if r.get(low_col)] if low_col else prices

    if len(prices) < 5:
        return None

    current = prices[-1]
    change_pct = (current - prices[-2]) / prices[-2] * 100 if len(prices) >= 2 else 0

    if indicators is None:
        indicators_all = True
    else:
        indicators_all = False

    result = {
        "current": round(current, 2),
        "change_pct": round(change_pct, 1),
        "volume": volumes[-1] if volumes else 0,
    }

    # RSI
    rsi = compute_rsi(prices, 14)
    rsi_signal = ""
    if rsi is not None:
        if rsi > 70:
            rsi_signal = "超买"
        elif rsi < 30:
            rsi_signal = "超卖"
        else:
            rsi_signal = "中性"
    result["rsi"] = rsi
    result["rsi_signal"] = rsi_signal

    # MA
    ma5 = compute_sma(prices, 5)
    ma10 = compute_sma(prices, 10)
    ma20 = compute_sma(prices, 20)
    ma_signal = ""
    if all(v is not None for v in [ma5, ma10, ma20]):
        if ma5 > ma10 > ma20:
            ma_signal = "多头排列↑"
        elif ma5 < ma10 < ma20:
            ma_signal = "空头排列↓"
        elif ma5 > ma10:
            ma_signal = "短线偏强"
        else:
            ma_signal = "短线偏弱"
    result["ma5"] = round(ma5, 2) if ma5 else None
    result["ma10"] = round(ma10, 2) if ma10 else None
    result["ma20"] = round(ma20, 2) if ma20 else None
    result["ma_signal"] = ma_signal

    # Volume
    vol_signal = ""
    if len(volumes) >= 5:
        avg_vol = sum(volumes[-5:]) / 5
        cur_vol = volumes[-1]
        if avg_vol > 0:
            vol_ratio = cur_vol / avg_vol
            if vol_ratio > 2:
                vol_signal = "放量↑↑"
            elif vol_ratio > 1.5:
                vol_signal = "放量↑"
            elif vol_ratio < 0.5:
                vol_signal = "缩量↓↓"
            else:
                vol_signal = "正常"
    result["vol_signal"] = vol_signal

    # ATR
    atr = compute_atr(highs, lows, prices, 14)
    atr_pct = round(atr / current * 100, 2) if atr and current > 0 else 0
    result["atr"] = atr
    result["atr_pct"] = atr_pct

    # MACD
    macd, hist = compute_macd(prices)
    result["macd"] = macd
    result["macd_hist"] = hist

    # 布林带
    bb_ma, bb_upper, bb_lower, bb_bandwidth, bb_pct = compute_bollinger(prices, 20, 2)
    result["bb_ma"] = bb_ma
    result["bb_upper"] = bb_upper
    result["bb_lower"] = bb_lower
    result["bb_bandwidth"] = bb_bandwidth
    result["bb_pct"] = bb_pct

    # VWAP
    vwap = compute_vwap(prices, volumes) if volumes else current
    result["vwap"] = vwap
    result["vwap_diff_pct"] = round((current - vwap) / vwap * 100, 2) if vwap and vwap > 0 else 0

    # 支撑/阻力位
    s1, r1, low_20, high_20 = find_support_resistance(prices, 20)
    result["support"] = s1
    result["resistance"] = r1
    result["support_dist_pct"] = round((current - s1) / s1 * 100, 2) if s1 > 0 else 0
    result["resistance_dist_pct"] = round((r1 - current) / current * 100, 2) if current > 0 else 0

    # 综合评分
    score, details = compute_composite_score(result)
    result["score"] = score
    result["score_details"] = details
    result["recommendation"] = recommend(score)

    return result


# ── 信号历史追踪 ─────────────────────────────────────

def compute_history(rows, name_col, price_col, vol_col, high_col, low_col):
    """逐日计算信号历史。"""
    prices = [parse_float(r[price_col]) for r in rows if r.get(price_col)]
    volumes = [parse_float(r[vol_col]) for r in rows if r.get(vol_col)] if vol_col else []
    highs = [parse_float(r[high_col]) for r in rows if r.get(high_col)] if high_col else prices
    lows = [parse_float(r[low_col]) for r in rows if r.get(low_col)] if low_col else prices
    dates = [r.get("date", r.get("日期", r.get("trade_date", ""))) for r in rows]

    history = []
    for i in range(len(prices)):
        if i < 5:
            continue
        sub_prices = prices[:i+1]
        sub_volumes = volumes[:i+1] if len(volumes) > i else []
        sub_highs = highs[:i+1] if len(highs) > i else sub_prices
        sub_lows = lows[:i+1] if len(lows) > i else sub_prices

        rsi = compute_rsi(sub_prices, 14)
        ma5 = compute_sma(sub_prices, 5)
        ma10 = compute_sma(sub_prices, 10)
        ma20 = compute_sma(sub_prices, 20)
        macd, hist = compute_macd(sub_prices)
        bb_ma, bb_upper, bb_lower, bb_bandwidth, bb_pct = compute_bollinger(sub_prices, 20, 2)

        signals = []
        if rsi and rsi < 30:
            signals.append("RSI超卖")
        if rsi and rsi > 70:
            signals.append("RSI超买")
        if all(v is not None for v in [ma5, ma10, ma20]):
            if ma5 > ma10 > ma20:
                signals.append("多头排列")
            elif ma5 < ma10 < ma20:
                signals.append("空头排列")
        if hist is not None and hist > 0:
            signals.append("MACD金叉")
        if hist is not None and hist < 0:
            signals.append("MACD死叉")

        record = {
            "date": dates[i] if i < len(dates) else f"#{i}",
            "close": round(sub_prices[-1], 2),
            "rsi": rsi,
            "ma_signal": "多头" if "多头排列" in signals else "空头" if "空头排列" in signals else "中性",
            "macd_hist": hist,
            "bb_pct": bb_pct,
            "signals": signals,
            "signal_count": len(signals),
        }
        history.append(record)

    return history


# ── 多股票扫描 ─────────────────────────────────────

def scan_stocks(rows, name_col, price_col, vol_col, high_col, low_col):
    """多股票一键扫描。"""
    stocks = defaultdict(list)
    for r in rows:
        name = r.get(name_col, "?")
        stocks[name].append(r)

    results = {}
    for name, stock_rows in stocks.items():
        result = analyze_stock(stock_rows, name_col, price_col, vol_col, high_col, low_col)
        if result:
            results[name] = result
    return results


# ── 打印格式化 ──────────────────────────────────────

def print_analysis(results):
    """打印多股票分析报告。"""
    print(f"\n📈 技术信号扫描")
    print(f"   {'='*80}")
    header = f"   {'代码':<10} {'现价':>8} {'涨跌':>7} {'RSI':>6} {'均线':<12} {'量':<7} {'布林%b':>7} {'评分':>4} {'建议'}"
    print(header)
    print(f"   {'-'*80}")
    for name in sorted(results, key=lambda n: -results[n]["score"]):
        r = results[name]
        arrow = "↑" if r['change_pct'] >= 0 else "↓"
        bb = f"{r.get('bb_pct', 'N/A')}"
        if isinstance(r.get('bb_pct'), (int, float)):
            bb = f"↓{r['bb_pct']:.1f}" if r['bb_pct'] < 0.2 else f"↑{r['bb_pct']:.1f}" if r['bb_pct'] > 0.8 else f"{r['bb_pct']:.1f}"
        print(f"   {name:<10} {r['current']:>8.2f} "
              f"{arrow}{abs(r['change_pct']):>5.1f}% "
              f"{r['rsi'] if r['rsi'] else 'N/A':>6} "
              f"{r['ma_signal']:<12} {r['vol_signal']:<7} "
              f"{bb:>7} {r['score']:>3} {r['recommendation']}")

    print(f"\n   评分明细:")
    for name in sorted(results, key=lambda n: -results[n]["score"]):
        r = results[name]
        details = "; ".join(r.get("score_details", []))
        print(f"   {name}: {r['score']}分 — {details}")


# ── 信号历史打印 ────────────────────────────────────

def print_history(history, max_rows=30):
    """打印信号历史表。"""
    print(f"\n📜 信号历史追踪")
    print(f"   {'='*65}")
    print(f"   {'日期':<12} {'收盘':>8} {'RSI':>6} {'均线':<8} {'信号数':>6}")
    print(f"   {'-'*65}")
    for h in history[-max_rows:]:
        print(f"   {h['date']:<12} {h['close']:>8.2f} "
              f"{h['rsi'] if h['rsi'] else 'N/A':>6} "
              f"{h['ma_signal']:<8} "
              f"{h['signal_count']:>6}")
    if len(history) > max_rows:
        print(f"   ... 还有 {len(history) - max_rows} 条记录")


# ── 单股票详细打印 ──────────────────────────────────

def print_single_stock(result, name=""):
    """打印单只股票的详细分析。"""
    label = f" {name}" if name else ""
    print(f"\n📈 技术信号分析{label}")
    print(f"   {'='*50}")
    print(f"   现价: {result['current']:.2f}  ({result['change_pct']:+.1f}%)")
    print(f"   成交量: {result.get('volume', 0):,.0f}")
    print(f"   综合评分: {result['score']}分 — {result['recommendation']}")
    if result.get("score_details"):
        print(f"   评分明细: {'; '.join(result['score_details'])}")

    print(f"\n   ── 技术指标 ──")
    print(f"   RSI(14): {result['rsi']} ({result['rsi_signal']})")
    print(f"   MA: 5={result['ma5']}  10={result['ma10']}  20={result['ma20']}  {result['ma_signal']}")
    if result.get("bb_ma"):
        print(f"   布林带: MA={result['bb_ma']} 上轨={result['bb_upper']} 下轨={result['bb_lower']}")
        print(f"   布林带宽: {result.get('bb_bandwidth', 'N/A')}%  %b={result.get('bb_pct', 'N/A')}")
    if result.get("vwap"):
        print(f"   VWAP: {result['vwap']} (偏差 {result.get('vwap_diff_pct', 0):+.2f}%)")
    print(f"   MACD: {result['macd']}  hist={result.get('macd_hist', 'N/A')}")
    print(f"   ATR: {result.get('atr', 'N/A')} ({result.get('atr_pct', 'N/A')}%)")
    print(f"   成交量: {result['vol_signal']}")

    if result.get("support"):
        print(f"\n   ── 支撑/阻力 ──")
        print(f"   支撑位: {result['support']} (距当前 {result.get('support_dist_pct', 0):+.1f}%)")
        print(f"   阻力位: {result['resistance']} (距当前 {result.get('resistance_dist_pct', 0):+.1f}%)")


# ── ASCII行图 ─────────────────────────────────────

def ascii_price_chart(prices, width=50, height=10):
    """简单ASCII折线图。"""
    if len(prices) < 2:
        return ""
    # 采样
    if len(prices) > width:
        step = len(prices) / width
        sampled = [prices[int(i * step)] for i in range(width)]
    else:
        sampled = prices
    lo, hi = min(sampled), max(sampled)
    if hi - lo < 0.001:
        return ""

    chart = []
    for row in range(height, 0, -1):
        threshold = lo + (hi - lo) * (row - 1) / height
        line = ""
        for p in sampled:
            if p >= threshold:
                line += "█"
            else:
                line += " "
        chart.append(f"   {threshold:>10.2f} {line}")
    chart.append(f"   {' '*10} {'─' * width}")
    chart.append(f"   {' '*10} {'>' * width}")
    return "\n".join(chart)


# ── 主入口 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Market Signals v1.1.0 — 技术信号扫描器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令说明:
  (默认)       单股票或多股票分析
  --scan       多股票一键扫描（按name列分组）
  --history    信号历史追踪（逐日信号记录）
  --chart      显示ASCII价格走势图
  --list       列出文件中的股票列表

示例:
  python3 %(prog)s --file stock.csv
  python3 %(prog)s --file portfolio.csv --scan
  python3 %(prog)s --file stock.csv --history --max-hist 60
  python3 %(prog)s --file stock.csv --chart
  python3 %(prog)s --file stock.csv --output signals.json

免责声明: 本工具仅提供技术分析参考，不构成投资建议。
        """
    )
    parser.add_argument("--file", required=True, help="价格CSV文件 (date, close, ...)")
    parser.add_argument("--name-col", default="name", help="股票名称列")
    parser.add_argument("--price-col", default="close", help="收盘价列")
    parser.add_argument("--vol-col", default="volume", help="成交量列")
    parser.add_argument("--high-col", default="high", help="最高价列")
    parser.add_argument("--low-col", default="low", help="最低价列")
    parser.add_argument("--indicators", default="all", help="指标列表 (rsi,ma,macd,...)")
    parser.add_argument("--output", help="JSON输出路径")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--list", action="store_true", help="列出股票列表")
    parser.add_argument("--scan", action="store_true", help="多股票一键扫描模式")
    parser.add_argument("--history", action="store_true", help="信号历史追踪")
    parser.add_argument("--max-hist", type=int, default=30, help="历史显示行数")
    parser.add_argument("--chart", action="store_true", help="显示ASCII价格走势图")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    rows = read_csv(args.file)
    if not rows:
        print("❌ CSV为空")
        sys.exit(1)

    cols = list(rows[0].keys())
    has_multi = args.name_col in cols

    # --list: 列出股票
    if args.list:
        names = sorted(set(r.get(args.name_col, "?") for r in rows))
        print(f"📋 股票列表 — {Path(args.file).name}")
        for n in names:
            count = sum(1 for r in rows if r.get(args.name_col) == n)
            print(f"   {n}: {count} 条记录")
        return

    # --chart: ASCII价格走势图
    if args.chart:
        prices = [parse_float(r[args.price_col]) for r in rows if r.get(args.price_col)]
        print(f"\n📈 价格走势 — {Path(args.file).name}")
        print(ascii_price_chart(prices))
        return

    # --history: 信号历史
    if args.history:
        if has_multi:
            # 取第一个股票的历史
            first_stock = sorted(set(r.get(args.name_col, "") for r in rows))[0]
            stock_rows = [r for r in rows if r.get(args.name_col) == first_stock]
            print(f"\n📜 信号历史 — {first_stock}")
            history = compute_history(stock_rows, args.name_col, args.price_col,
                                      args.vol_col, args.high_col, args.low_col)
        else:
            history = compute_history(rows, args.name_col, args.price_col,
                                      args.vol_col, args.high_col, args.low_col)
        print_history(history, args.max_hist)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                print(f"\n💾 已保存: {args.output}")
        return

    # --scan: 多股票扫描
    if args.scan or (has_multi and len(set(r.get(args.name_col, "") for r in rows)) > 1):
        results = scan_stocks(rows, args.name_col, args.price_col,
                              args.vol_col, args.high_col, args.low_col)
        if not results:
            print("❌ 未能分析任何股票")
            return

        if args.json or args.output:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_analysis(results)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"\n💾 已保存: {args.output}")
        return

    # 默认：单股票分析
    stock_rows = rows
    name = ""
    if has_multi:
        # 取第一个股票
        first_stock = sorted(set(r.get(args.name_col, "") for r in rows))[0]
        stock_rows = [r for r in rows if r.get(args.name_col) == first_stock]
        name = first_stock

    result = analyze_stock(stock_rows, args.name_col, args.price_col,
                           args.vol_col, args.high_col, args.low_col)
    if not result:
        print("❌ 数据不足，至少需要5条记录")
        sys.exit(1)

    if args.json or args.output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_single_stock(result, name)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n💾 已保存: {args.output}")


if __name__ == "__main__":
    main()
