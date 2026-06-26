"""
Tool: analyze_macro_impact
宏观经济事件对加密市场影响分析
收集数据 + 筛选宏观相关快讯，交给 Claude 做深度分析
"""

from __future__ import annotations

from lib.market_data import MarketData
from lib.odaily_client import OdailyClient
from lib.formatters import format_number, format_pct, format_price, now_bjt

MACRO_KW: dict[str, list[str]] = {
    "all": [
        "美联储", "Fed", "CPI", "利率", "通胀", "就业", "GDP",
        "鲍威尔", "降息", "加息", "国债", "美元", "SEC",
        "监管", "ETF", "地缘", "关税", "贸易战",
    ],
    "fed": ["美联储", "Fed", "鲍威尔", "利率", "降息", "加息", "FOMC"],
    "inflation": ["CPI", "通胀", "PCE", "PPI", "物价"],
    "employment": ["就业", "非农", "失业率", "初请"],
    "geopolitical": ["地缘", "战争", "制裁", "关税", "贸易"],
}


def analyze_macro_impact(event_type: str = "all") -> str:
    md = MarketData()
    prices = md.get_prices(["BTC", "ETH", "SOL"])
    gd = md.get_global_data()
    fg = md.get_fear_greed_index()
    funding = md.get_funding_rates()

    kw = MACRO_KW.get(event_type, MACRO_KW["all"])
    try:
        flash = OdailyClient().get_flash_news(limit=50)
        macro_news = [
            f
            for f in flash
            if any(
                k in (f.get("title", "") + f.get("description", ""))
                for k in kw
            )
        ]
    except Exception:
        macro_news = []

    L = [
        "🏦 宏观事件影响分析",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        f"📋 分析范围: {event_type}",
        "",
        "📊 当前市场状态",
    ]

    for p in prices:
        L.append(
            f"  {p['symbol']}: {format_price(p['price_usd'])} "
            f"({format_pct(p['change_24h_pct'])})"
        )
    L.append(f"  总市值: {format_number(gd.get('total_market_cap_usd', 0))}")
    L.append(f"  市值变化: {format_pct(gd.get('market_cap_change_24h_pct', 0))}")
    L.append(f"  恐惧贪婪: {fg['value']} {fg['emoji']} {fg['label']}")
    L.append(f"  BTC市占率: {gd.get('btc_dominance', 0)}%")
    L.append("")

    if funding:
        L.append("📈 合约市场反应")
        for sym, d in funding.items():
            L.append(f"  {sym} 资金费率: {d['funding_rate']:+.4f}%")
        L.append("")

    if macro_news:
        L.append("📰 近期宏观相关快讯")
        for n in macro_news[:10]:
            L.append(f"  • {n['title']}")
            if n.get("url"):
                L.append(f"    🔗 {n['url']}")
        L.append("")
    else:
        L += ["📰 近期无明显宏观相关快讯", ""]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 请基于以上数据分析:",
        "  1. 当前宏观环境对加密市场的影响方向",
        "  2. 近期需要关注的宏观风险点",
        "  3. 不同情景下的市场反应预判",
        "  4. 基于宏观面的操作建议",
        "",
        "⚠️ 宏观分析仅供参考，市场存在不确定性",
    ]
    return "\n".join(L)
