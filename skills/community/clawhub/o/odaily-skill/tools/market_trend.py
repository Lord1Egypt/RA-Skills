"""
Tool: get_crypto_market_analysis
加密市场分析 — 行情数据 + 宏观事件影响（合并版）
"""

from __future__ import annotations

from lib.market_data import MarketData
from lib.odaily_client import OdailyClient
from lib.formatters import format_number, format_pct, format_price, now_bjt

MACRO_KW: list[str] = [
    "美联储", "Fed", "CPI", "利率", "通胀", "就业", "GDP",
    "鲍威尔", "降息", "加息", "国债", "美元", "SEC",
    "监管", "ETF", "地缘", "关税", "贸易战", "FOMC",
    "PCE", "PPI", "非农", "失业率",
]


def get_crypto_market_analysis(focus: str = "overview") -> str:
    md = MarketData()
    prices = md.get_prices(
        ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX"]
    )
    gd = md.get_global_data()
    fg = md.get_fear_greed_index()
    movers = md.get_top_movers(5)
    funding = md.get_funding_rates()
    ls = md.get_long_short_ratio()

    oc = OdailyClient()
    try:
        flash = oc.get_flash_news(limit=50)
    except Exception:
        flash = []
    try:
        market_news = oc.get_market_news(limit=5)
    except Exception:
        market_news = []

    # ── Part 1: 加密市场数据 ─────────────────────────────
    L = [
        "📊 加密市场分析",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        "",
        "🌍 全局市场",
        f"  总市值: {format_number(gd.get('total_market_cap_usd', 0))} "
        f"({format_pct(gd.get('market_cap_change_24h_pct', 0))})",
        f"  24H交易量: {format_number(gd.get('total_volume_24h_usd', 0))}",
        f"  BTC市占率: {gd.get('btc_dominance', 0)}%",
        f"  恐惧贪婪: {fg['value']} {fg['emoji']} {fg['label']}",
        "",
        "💰 主流币行情",
    ]

    for p in prices:
        L.append(
            f"  {p['symbol']:<6} {format_price(p['price_usd']):>12} "
            f"{format_pct(p['change_24h_pct']):>12} "
            f"| 市值{format_number(p.get('market_cap', 0), 1)}"
        )
    L.append("")

    if funding:
        L.append("📈 合约指标")
        for sym, d in funding.items():
            r = d["funding_rate"]
            re = "🟢" if r > 0 else ("🔴" if r < 0 else "⚪")
            lsr = ls.get(sym, {})
            ls_str = f"多空比 {lsr['long_short_ratio']:.2f}" if lsr else ""
            L.append(f"  {sym}: 资金费率 {re} {r:+.4f}% | {ls_str}")
        L.append("")

    L.append("🏆 24H涨幅TOP5")
    for g in movers.get("top_gainers", [])[:5]:
        L.append(
            f"  🟢 {g['symbol']:<8} {format_pct(g['change_24h_pct']):>10} "
            f"| {format_price(g['price'])}"
        )
    L.append("")
    L.append("💀 24H跌幅TOP5")
    for lo in movers.get("top_losers", [])[:5]:
        L.append(
            f"  🔴 {lo['symbol']:<8} {format_pct(lo['change_24h_pct']):>10} "
            f"| {format_price(lo['price'])}"
        )
    L.append("")

    # ── Part 2: 宏观事件影响分析 ─────────────────────────
    macro_news = [
        f for f in flash
        if any(k in (f.get("title", "") + f.get("description", "")) for k in MACRO_KW)
    ]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "🏦 宏观事件影响分析",
        "",
    ]

    if macro_news:
        L.append("📰 近期宏观相关快讯")
        for n in macro_news[:10]:
            L.append(f"  • {n['title']}")
            if n.get("url"):
                L.append(f"    🔗 {n['url']}")
        L.append("")
    else:
        L += ["📰 近期无明显宏观相关快讯", ""]

    # ── Part 3: Odaily 行情播报 ───────────────────────────
    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "📡 Odaily 行情播报",
        "",
    ]
    if market_news:
        for i, n in enumerate(market_news, 1):
            L.append(f"  {i}. {n['title']}")
            if n.get("description") and n["description"] != n["title"]:
                L.append(f"     {n['description'][:120]}{'…' if len(n['description']) > 120 else ''}")
            if n.get("published_at"):
                L.append(f"     ⏱ {n['published_at']}")
            if n.get("url"):
                L.append(f"     🔗 {n['url']}")
            L.append("")
    else:
        L += ["  暂无行情播报数据", ""]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 请基于以上数据综合分析:",
        "  1. 当前市场走势判断（多空方向、强弱格局）",
        "  2. 宏观环境对加密市场的影响方向",
        "  3. 近期需要关注的风险点",
        "  4. 简要操作参考",
        "",
        "⚠️ 以上为实时数据，分析仅供参考，不构成投资建议",
    ]
    return "\n".join(L)


# 保持向后兼容
def get_market_trend_analysis(focus: str = "overview") -> str:
    return get_crypto_market_analysis(focus=focus)
