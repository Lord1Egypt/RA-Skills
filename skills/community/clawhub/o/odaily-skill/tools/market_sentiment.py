"""
Tool: get_market_sentiment
CSI 综合情绪指标 — 恐惧贪婪 + 资金费率 + 多空比 + 动量

Args:
    无

Returns:
    str: CSI 综合情绪指标报告，含各子指标评分和 AI 解读提示
"""

from __future__ import annotations

from lib.market_data import MarketData
from lib.formatters import now_bjt


def get_market_sentiment() -> str:
    md = MarketData()
    fg = md.get_fear_greed_index()
    funding = md.get_funding_rates()
    ls = md.get_long_short_ratio()
    prices = md.get_prices(["BTC", "ETH"])

    # ── CSI 计算 ──────────────────────────────────────────
    comps: dict[str, float] = {}
    wsum = 0.0
    wtot = 0.0

    component_names: dict[str, str] = {
        "fear_greed": "恐惧贪婪",
        "funding_rate": "资金费率",
        "long_short": "多空比",
        "price_momentum": "价格动量",
    }

    # 恐惧贪婪 (35%)
    fg_val = fg.get("value", 50)
    comps["fear_greed"] = float(fg_val)
    wsum += fg_val * 0.35
    wtot += 0.35

    # 资金费率 (25%)
    btc_fr = funding.get("BTC", {}).get("funding_rate", 0)
    fr_s = max(0, min(100, (btc_fr + 0.1) / 0.2 * 100))
    comps["funding_rate"] = round(fr_s, 1)
    wsum += fr_s * 0.25
    wtot += 0.25

    # 多空比 (25%)
    btc_ls = ls.get("BTC", {}).get("long_short_ratio", 1.0)
    ls_s = max(0, min(100, (btc_ls - 0.5) / 1.5 * 100))
    comps["long_short"] = round(ls_s, 1)
    wsum += ls_s * 0.25
    wtot += 0.25

    # 价格动量 (15%)
    btc_chg = next(
        (p["change_24h_pct"] for p in prices if p["symbol"] == "BTC"), 0
    )
    ch_s = max(0, min(100, (btc_chg + 10) / 20 * 100))
    comps["price_momentum"] = round(ch_s, 1)
    wsum += ch_s * 0.15
    wtot += 0.15

    csi = round(wsum / wtot if wtot else 50, 2)

    if csi >= 90:
        cl, ce = "极端多头市场（逃顶）", "🤯"
    elif csi >= 75:
        cl, ce = "强势多头", "🤑"
    elif csi >= 60:
        cl, ce = "多头市场", "😏"
    elif csi >= 50:
        cl, ce = "情绪回升", "🤗"
    elif csi >= 40:
        cl, ce = "情绪冷却", "😐"
    elif csi >= 25:
        cl, ce = "空头市场", "😰"
    elif csi >= 10:
        cl, ce = "强势空头", "😱"
    else:
        cl, ce = "极端空头市场（抄底）", "💀"

    if btc_chg > 3:
        intra = "强势上攻 🚀"
    elif btc_chg > 1:
        intra = "温和上涨 📈"
    elif btc_chg > -1:
        intra = "横盘整理 ➡️"
    elif btc_chg > -3:
        intra = "温和下跌 📉"
    else:
        intra = "恐慌下跌 💀"

    bl = 20
    fi = int(csi / 100 * bl)
    bar = "▓" * fi + "░" * (bl - fi)

    L = [
        "🌍 全市场投资者情绪指标",
        "════════════════════════════",
        f"⏰ 报告时间: {now_bjt()}",
        "────────────────────────────",
        "",
        f"🏦 CSI: {csi}% {ce} {cl}",
        "",
        f"  [{bar}] {csi}%",
        "  0%                50%              100%",
        "",
        "  CSI用于衡量趋势级别的投资者情绪",
        "   · 超过90%: 极端多头市场（逃顶）🤯",
        "   · 处于50-90%: 多头市场（划水）😏",
        "   · 处于50-10%: 空头市场（等待）😰",
        "   · 低于10%: 极端空头市场（抄底）💀",
        "",
        "────────────────────────────",
        "",
        f"🌡️ 日内情绪: {intra}",
        f"😱 恐惧贪婪指数: {fg['value']} {fg['emoji']} {fg['label']}",
        "",
        "💰 资金费率:",
    ]

    for sym, d in funding.items():
        r = d["funding_rate"]
        re = "🟢" if r > 0 else ("🔴" if r < 0 else "⚪")
        dr = "多头付费→偏多" if r > 0 else "空头付费→偏空"
        L.append(f"  {sym}: {re} {r:+.4f}% ({dr})")
    L.append("")

    L.append("📊 多空比:")
    for sym, d in ls.items():
        L.append(
            f"  {sym}: 多 {d['long_short_ratio']:.2f} : 空 1.00 "
            f"(多{d['long_account_pct']}% / 空{d['short_account_pct']}%)"
        )
    L.append("")

    L.append("📋 CSI 评分明细:")
    for key, val in comps.items():
        name = component_names.get(key, key)
        ml = 10
        mf = int(val / 100 * ml)
        mb = "▓" * mf + "░" * (ml - mf)
        L.append(f"  {name:<8} [{mb}] {val:.1f}")
    L.append("")

    L += [
        "════════════════════════════",
        "💡 以上为实时情绪数据，请给出综合解读和操作建议",
        "⚠️ 情绪指标仅供参考，不构成投资建议",
    ]
    return "\n".join(L)
