"""
Tool: analyze_token_trend
代币多周期趋势分析 — 1H / 4H / 1D / 1W
"""

from __future__ import annotations

from lib.market_data import MarketData
from lib.technical_analysis import analyze_trend
from lib.formatters import format_price, now_bjt


def analyze_token_trend(symbol: str, timeframe: str = "all") -> str:
    symbol = symbol.upper().strip()
    md = MarketData()

    prices = md.get_prices([symbol])
    cur = prices[0]["price_usd"] if prices else 0

    tfs = [timeframe] if timeframe != "all" else ["1h", "4h", "1d", "1w"]

    L = [
        f"📉 代币趋势分析 | {symbol}",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        f"📍 当前价格: {format_price(cur)}",
        "",
    ]

    analyses: list[dict] = []
    for tf in tfs:
        try:
            klines = md.get_klines(symbol, interval=tf, limit=200)
            if not klines or len(klines) < 30:
                L.append(f"⚠️ {tf} 周期数据不足")
                continue
            a = analyze_trend(klines, tf)
            if "error" in a:
                L.append(f"⚠️ {tf}: {a['error']}")
                continue
            analyses.append(a)
        except Exception as e:
            L.append(f"⚠️ {tf} 分析失败: {str(e)[:50]}")

    if not analyses:
        L.append("❌ 无法获取有效K线数据")
        return "\n".join(L)

    tfl = {"1h": "🕐 1H", "4h": "🕓 4H", "1d": "📅 1D", "1w": "📆 1W"}

    L.append("┌────────┬──────────────┬──────────┬───────────┐")
    L.append("│  周期   │    趋势       │ 变盘价格  │ 变盘时间   │")
    L.append("├────────┼──────────────┼──────────┼───────────┤")
    for a in analyses:
        lab = tfl.get(a["timeframe"], a["timeframe"])
        ts = f"{a['trend_label']}{a['trend_emoji']}"
        pp = format_price(a["pivot_price"])
        pt = a["pivot_time"]
        L.append(f"│ {lab:<6} │ {ts:<12} │ {pp:<8} │ {pt:<9} │")
    L.append("└────────┴──────────────┴──────────┴───────────┘")
    L.append("")

    p0 = analyses[0]
    L.append("📊 关键价位:")
    L.append(
        f"  上方阻力: {' → '.join(format_price(r) for r in p0['resistance'])}"
    )
    L.append(
        f"  下方支撑: {' → '.join(format_price(s) for s in p0['support'])}"
    )
    L.append("")

    L.append("📈 技术指标:")
    L.append(f"  RSI(14): {p0.get('rsi_14', 'N/A')}")
    L.append(f"  MACD: {p0.get('macd_signal', 'N/A')}")
    L.append(f"  置信度: {p0.get('confidence', 'N/A')}%")
    L.append("")

    L.append("📋 各周期评分:")
    for a in analyses:
        lab = tfl.get(a["timeframe"], a["timeframe"])
        sc = a.get("score", 0)
        bl = 10
        fi = int(max(0, min(bl, (sc + 100) / 200 * bl)))
        bar = "▓" * fi + "░" * (bl - fi)
        L.append(f"  {lab} [{bar}] {sc:+.1f}")
    L.append("")

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 以上为技术分析数据，请结合基本面给出综合判断",
        "⚠️ 技术分析仅供参考，不构成投资建议",
    ]
    return "\n".join(L)
