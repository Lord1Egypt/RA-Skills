"""
Tool: scan_whale_tail_trades
预测市场异动 + 巨鲸尾盘跟单

核心逻辑:
1. 获取 Polymarket 大额交易 (>$10,000)
2. 筛选 price > 0.95 为尾盘（巨鲸高确定性押注）
3. 始终输出 Top 10 高确定性尾盘（按金额降序）
4. 可选存入 Supabase 做持久化去重

Args:
    min_size: 最小交易金额（默认 10000 USDC）
    min_price: 尾盘最低价格阈值（默认 0.95）

Returns:
    str: 格式化的巨鲸尾盘扫描报告（Top 10）
"""

from __future__ import annotations

from lib.polymarket_client import PolymarketClient
from lib.odaily_client import OdailyClient
from lib.supabase_client import SupabaseClient
from lib.formatters import now_bjt


def scan_whale_tail_trades(
    min_size: float = 10000,
    min_price: float = 0.95,
) -> str:
    pm = PolymarketClient()
    all_trades = pm.get_whale_trades(min_size=min_size, limit=100)

    if not all_trades:
        return (
            "🎯 预测市场异动 + 巨鲸尾盘跟单\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ {now_bjt()}\n\n"
            "暂无符合条件的大额交易数据。"
        )

    tail = pm.filter_tail_trades(all_trades, min_price=min_price)
    non_tail = sorted(
        [t for t in all_trades if t["price"] < min_price],
        key=lambda x: x["size"],
        reverse=True,
    )

    _try_save_to_supabase(all_trades)

    L = [
        "🎯 预测市场异动 + 巨鲸尾盘跟单",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        "",
    ]

    # ── Polymarket 预测市场快讯 Top 5 ────────────────────
    oc = OdailyClient()
    pm_news = oc.get_polymarket_news(limit=5)
    L += ["📡 Polymarket预测市场", ""]
    if pm_news:
        for i, n in enumerate(pm_news, 1):
            L.append(f"  {i}. {n['title']}")
            if n.get("description"):
                L.append(f"     {n['description'][:100]}{'…' if len(n['description']) > 100 else ''}")
            if n.get("published_at"):
                L.append(f"     ⏱ {n['published_at']}")
            if n.get("url"):
                L.append(f"     🔗 {n['url']}")
            L.append("")
    else:
        L += ["  暂无预测市场快讯", ""]

    # ── 巨鲸尾盘 ──────────────────────────────────────────
    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    if tail:
        L += [
            "🎯 Top 10 高确定性尾盘交易",
            "",
        ]
        L.append(f"  {'排序':<4} {'事件(中文概括)':<45} {'方向':<8} {'金额':>10}  {'市场价':>6}  巨鲸")
        L.append(f"  {'─'*4} {'─'*45} {'─'*8} {'─'*10}  {'─'*6}  {'─'*16}")
        for i, t in enumerate(tail[:10], 1):
            se = "🟢 YES" if t["side"].upper() == "BUY" else "🔴 NO"
            market_price = f"${t['price']:.3f}"
            size_str = f"${t['size']:,.0f}"
            name = t['name'][:16]
            title = t['title'][:45]
            L.append(f"  {i:<4} {title:<45} {se:<8} {size_str:>10}  {market_price:>6}  {name}")
        L.append("")
        # 附链接列表
        L.append("  🔗 相关链接:")
        seen_slugs: set = set()
        for t in tail[:10]:
            slug = t.get("event_slug", "")
            if slug and slug not in seen_slugs:
                seen_slugs.add(slug)
                L.append(f"     https://polymarket.com/event/{slug}")
        L.append("")

        tv = sum(t["size"] for t in tail[:10])
        yc = sum(1 for t in tail[:10] if t["side"].upper() == "BUY")
        total_tv = sum(t["size"] for t in tail)
        L.append(f"  📊 Top10汇总: 总额${tv:,.0f}")
        L.append(f"     YES: {yc}笔 | NO: {10 - yc if len(tail) >= 10 else len(tail) - yc}笔")
        if len(tail) > 10:
            L.append(f"     （全部{len(tail)}笔尾盘总额${total_tv:,.0f}）")
        L.append("")
    else:
        L += [
            f"⚠️ 当前无高确定性尾盘交易 (price ≥ {min_price})",
            "",
        ]

    if non_tail[:5]:
        L += [
            "━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📋 其他大额交易参考 (price < {min_price})",
            "",
        ]
        for t in non_tail[:5]:
            se = "🟢" if t["side"].upper() == "BUY" else "🔴"
            L.append(
                f"  {se} ${t['size']:,.0f} @ {t['price'] * 100:.1f}% "
                f"| {t['title'][:50]}"
            )
        L.append("")

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 尾盘交易(price>0.95)代表巨鲸对事件结果高度确信",
        "   可作为信息参考，但请独立判断",
        "⚠️ 以上数据不构成投资建议",
    ]
    return "\n".join(L)


def _try_save_to_supabase(trades: list[dict]):
    """尝试存入 Supabase（可选）"""
    try:
        sb = SupabaseClient()
        if not sb.available:
            return
        existing = sb.get_existing_trade_hashes()
        new = [
            {
                "transaction_hash": t["transaction_hash"],
                "proxy_wallet": t.get("proxy_wallet", ""),
                "name": t.get("name"),
                "side": t.get("side", ""),
                "size": t["size"],
                "price": t["price"],
                "outcome": t.get("outcome"),
                "title": t.get("title", ""),
                "slug": t.get("slug", ""),
                "event_slug": t.get("event_slug"),
                "icon": t.get("icon"),
                "timestamp": t.get("timestamp", 0),
            }
            for t in trades
            if t.get("transaction_hash")
            and t["transaction_hash"] not in existing
        ]
        if new:
            sb.insert_whale_trades(new)
    except Exception:
        pass
