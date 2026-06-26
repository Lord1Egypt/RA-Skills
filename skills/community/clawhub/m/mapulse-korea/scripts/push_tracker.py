#!/usr/bin/env python3
"""
Mapulse — 推送事件追踪 (Push Event Tracker)

功能:
  1. 记录每次推送事件（股票、价格、事件类型、情绪方向）
  2. 定时回填 +1d/+3d/+7d 收盘价
  3. 提供聚合统计面板
  4. 单条推送后续追踪查询

合规设计:
  - 展示"事件推送的事后验证"，不展示"预测准确率"
  - 纯事实数据，不做对/错判断
  - 让用户自行评估工具价值

用法:
  python3 push_tracker.py backfill          # 回填价格数据
  python3 push_tracker.py stats             # 30天统计面板
  python3 push_tracker.py track 005930      # 查看该股票推送追踪
  python3 push_tracker.py demo              # 演示

crontab (每天收盘后):
  0 7 * * 1-5 cd /path/to/scripts && python3 push_tracker.py backfill
"""

import os
import sys
import json
import time
import sqlite3
import datetime
import logging

sys.path.insert(0, os.path.dirname(__file__))

logger = logging.getLogger("push_tracker")

DB_PATH = os.environ.get("MAPULSE_DB",
    os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


# ═══════════════════════════════════════════
#  Schema
# ═══════════════════════════════════════════

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_push_tracking():
    """建表"""
    conn = _conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS push_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- 推送基本信息
            ticker TEXT NOT NULL,
            stock_name TEXT DEFAULT '',
            push_time TEXT NOT NULL,           -- ISO format
            push_date TEXT NOT NULL,           -- YYYY-MM-DD (trading date)

            -- 推送时的价格快照
            push_price REAL NOT NULL,          -- 推送时收盘价
            push_change_pct REAL DEFAULT 0,    -- 推送当日涨跌幅

            -- 事件分类
            event_type TEXT NOT NULL,          -- price_spike|price_drop|dart|news|forum_buzz|crash_alert
            event_detail TEXT DEFAULT '',      -- 事件描述
            sentiment TEXT DEFAULT 'neutral',  -- bullish|bearish|neutral

            -- 后续追踪价格 (由 backfill 填入)
            price_1d REAL,                     -- +1 trading day 收盘价
            price_3d REAL,                     -- +3 trading days
            price_7d REAL,                     -- +7 trading days
            change_1d REAL,                    -- +1d 相对推送价格的变化%
            change_3d REAL,                    -- +3d
            change_7d REAL,                    -- +7d

            -- 论坛情绪追踪 (可选)
            forum_sentiment_push TEXT DEFAULT '',    -- 推送时论坛情绪 JSON
            forum_sentiment_3d TEXT DEFAULT '',      -- +3d 论坛情绪

            -- 状态
            status TEXT DEFAULT 'pending',     -- pending|partial|complete
            backfill_attempts INTEGER DEFAULT 0,

            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_pe_ticker ON push_events(ticker);
        CREATE INDEX IF NOT EXISTS idx_pe_date ON push_events(push_date);
        CREATE INDEX IF NOT EXISTS idx_pe_status ON push_events(status);
        CREATE INDEX IF NOT EXISTS idx_pe_type ON push_events(event_type);
    """)
    conn.commit()
    conn.close()


init_push_tracking()


# ═══════════════════════════════════════════
#  1. 记录推送事件
# ═══════════════════════════════════════════

def record_push_event(
    ticker: str,
    push_price: float,
    event_type: str,
    push_change_pct: float = 0.0,
    event_detail: str = "",
    sentiment: str = "neutral",
    push_date: str = None,
    stock_name: str = None,
    forum_sentiment: dict = None,
):
    """
    记录一次推送事件。
    在每次向用户推送消息时调用。

    event_type: price_spike|price_drop|dart|news|forum_buzz|crash_alert
    sentiment: bullish|bearish|neutral
    """
    from fetch_briefing import STOCK_NAMES, find_trading_date

    if not push_date:
        push_date = find_trading_date()
    if not stock_name:
        stock_name = STOCK_NAMES.get(ticker, ticker)

    push_time = datetime.datetime.now().isoformat()

    conn = _conn()
    conn.execute("""
        INSERT INTO push_events
            (ticker, stock_name, push_time, push_date, push_price, push_change_pct,
             event_type, event_detail, sentiment, forum_sentiment_push, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (
        ticker, stock_name, push_time, push_date, push_price, push_change_pct,
        event_type, event_detail, sentiment,
        json.dumps(forum_sentiment) if forum_sentiment else "",
    ))
    conn.commit()
    push_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    logger.info(f"Push event recorded: #{push_id} {stock_name} {event_type} @{push_price}")
    return push_id


# ═══════════════════════════════════════════
#  2. 回填价格 (cron job)
# ═══════════════════════════════════════════

def _get_trading_dates_after(base_date_str, count):
    """获取 base_date 之后的 N 个交易日"""
    from pykrx import stock as krx

    base = datetime.datetime.strptime(base_date_str, "%Y-%m-%d")
    dates = []
    for i in range(1, count * 3):  # 扫描足够多的自然日
        d = base + datetime.timedelta(days=i)
        ds = d.strftime("%Y%m%d")
        try:
            df = krx.get_market_ohlcv(ds, ds, "005930")
            if df is not None and len(df) > 0 and float(df.iloc[0]["거래량"]) > 0:
                dates.append(d.strftime("%Y-%m-%d"))
                if len(dates) >= count:
                    break
        except:
            pass
        time.sleep(0.05)
    return dates


def _get_close_price(ticker, date_str):
    """获取指定日期收盘价"""
    from fetch_briefing import get_stock
    data = get_stock(ticker, date_str)
    if data and data.get("close"):
        return float(data["close"])
    return None


def backfill_prices():
    """
    回填所有 pending/partial 事件的后续价格。
    每天收盘后运行一次。
    """
    conn = _conn()
    events = conn.execute("""
        SELECT * FROM push_events
        WHERE status IN ('pending', 'partial')
        ORDER BY push_date ASC
    """).fetchall()
    conn.close()

    if not events:
        print("No pending events to backfill")
        return 0

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    updated = 0

    for ev in events:
        ev = dict(ev)
        push_date = ev["push_date"]
        ticker = ev["ticker"]

        # 获取推送后的交易日列表
        trading_dates = _get_trading_dates_after(push_date, 7)
        if not trading_dates:
            continue

        changes = {}
        new_status = ev["status"]

        # +1d
        if ev["price_1d"] is None and len(trading_dates) >= 1:
            price = _get_close_price(ticker, trading_dates[0])
            if price:
                changes["price_1d"] = price
                changes["change_1d"] = round((price - ev["push_price"]) / ev["push_price"] * 100, 2)
                new_status = "partial"

        # +3d
        if ev["price_3d"] is None and len(trading_dates) >= 3:
            price = _get_close_price(ticker, trading_dates[2])
            if price:
                changes["price_3d"] = price
                changes["change_3d"] = round((price - ev["push_price"]) / ev["push_price"] * 100, 2)
                new_status = "partial"

        # +7d
        if ev["price_7d"] is None and len(trading_dates) >= 7:
            price = _get_close_price(ticker, trading_dates[6])
            if price:
                changes["price_7d"] = price
                changes["change_7d"] = round((price - ev["push_price"]) / ev["push_price"] * 100, 2)

        # 完成状态判断
        all_filled = all([
            changes.get("price_1d") or ev["price_1d"],
            changes.get("price_3d") or ev["price_3d"],
            changes.get("price_7d") or ev["price_7d"],
        ])
        if all_filled:
            new_status = "complete"

        if changes:
            conn2 = _conn()
            sets = [f"{k}=?" for k in changes]
            sets.append("status=?")
            sets.append("backfill_attempts=backfill_attempts+1")
            sets.append("updated_at=datetime('now')")
            vals = list(changes.values()) + [new_status, ev["id"]]
            conn2.execute(
                f"UPDATE push_events SET {','.join(sets)} WHERE id=?", vals
            )
            conn2.commit()
            conn2.close()
            updated += 1
            logger.info(f"Backfilled #{ev['id']} {ev['stock_name']}: {list(changes.keys())}")

        time.sleep(0.1)  # Rate limit pykrx

    print(f"Backfilled {updated}/{len(events)} events")
    return updated


# ═══════════════════════════════════════════
#  3. 统计面板
# ═══════════════════════════════════════════

def get_stats(days=30):
    """
    聚合统计：过去 N 天推送回顾
    返回 dict，可格式化为 Telegram 消息
    """
    conn = _conn()
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    # 总推送数
    total = conn.execute(
        "SELECT COUNT(*) FROM push_events WHERE push_date >= ?", (cutoff,)
    ).fetchone()[0]

    # 按事件类型
    type_counts = {}
    for row in conn.execute(
        "SELECT event_type, COUNT(*) as cnt FROM push_events WHERE push_date >= ? GROUP BY event_type",
        (cutoff,)
    ).fetchall():
        type_counts[row["event_type"]] = row["cnt"]

    # 有追踪数据的事件（至少有 +1d）
    tracked = conn.execute("""
        SELECT * FROM push_events
        WHERE push_date >= ? AND change_1d IS NOT NULL
    """, (cutoff,)).fetchall()

    # 分析追踪结果
    def classify_continuation(change, push_change):
        """判断事件后续：同方向延续 / 反转 / 无显著变化"""
        if abs(change) < 0.5:
            return "flat"
        if push_change < 0:  # 推送时下跌
            return "continue" if change < -0.5 else "reverse"
        elif push_change > 0:  # 推送时上涨
            return "continue" if change > 0.5 else "reverse"
        else:
            return "flat"

    # +1d 统计
    d1_stats = {"continue": 0, "reverse": 0, "flat": 0, "total": 0}
    d3_stats = {"continue": 0, "reverse": 0, "flat": 0, "total": 0}
    d7_stats = {"continue": 0, "reverse": 0, "flat": 0, "total": 0}

    # 情绪 vs 实际 交叉分析
    sentiment_vs_actual = {
        "bearish_down": 0, "bearish_up": 0,
        "bullish_up": 0, "bullish_down": 0,
        "neutral": 0,
    }

    for ev in tracked:
        ev = dict(ev)

        if ev["change_1d"] is not None:
            d1_stats["total"] += 1
            d1_stats[classify_continuation(ev["change_1d"], ev["push_change_pct"])] += 1

        if ev.get("change_3d") is not None:
            d3_stats["total"] += 1
            d3_stats[classify_continuation(ev["change_3d"], ev["push_change_pct"])] += 1

        if ev.get("change_7d") is not None:
            d7_stats["total"] += 1
            d7_stats[classify_continuation(ev["change_7d"], ev["push_change_pct"])] += 1

        # 情绪交叉
        sent = ev.get("sentiment", "neutral")
        if sent == "bearish":
            if ev["change_3d"] is not None:
                if ev["change_3d"] < -0.5:
                    sentiment_vs_actual["bearish_down"] += 1
                elif ev["change_3d"] > 0.5:
                    sentiment_vs_actual["bearish_up"] += 1
        elif sent == "bullish":
            if ev["change_3d"] is not None:
                if ev["change_3d"] > 0.5:
                    sentiment_vs_actual["bullish_up"] += 1
                elif ev["change_3d"] < -0.5:
                    sentiment_vs_actual["bullish_down"] += 1
        else:
            sentiment_vs_actual["neutral"] += 1

    # 最近 5 条有追踪的推送
    recent = conn.execute("""
        SELECT * FROM push_events
        WHERE push_date >= ? AND change_1d IS NOT NULL
        ORDER BY push_time DESC LIMIT 5
    """, (cutoff,)).fetchall()

    conn.close()

    return {
        "days": days,
        "total_pushes": total,
        "type_counts": type_counts,
        "d1_stats": d1_stats,
        "d3_stats": d3_stats,
        "d7_stats": d7_stats,
        "sentiment_vs_actual": sentiment_vs_actual,
        "recent_tracked": [dict(r) for r in recent],
    }


def format_stats(stats, lang="ko"):
    """格式化统计面板为 Telegram Markdown"""
    s = stats

    def pct(n, total):
        return f"{n/total*100:.0f}%" if total > 0 else "—"

    # 事件类型翻译
    type_labels = {
        "price_spike": "📈 급등",
        "price_drop": "📉 급락",
        "dart": "📋 DART 공시",
        "news": "📰 뉴스",
        "forum_buzz": "💬 포럼 이상",
        "crash_alert": "🚨 폭락 알림",
    }
    if lang == "zh":
        type_labels = {
            "price_spike": "📈 急涨",
            "price_drop": "📉 急跌",
            "dart": "📋 DART公告",
            "news": "📰 新闻",
            "forum_buzz": "💬 论坛异常",
            "crash_alert": "🚨 暴跌预警",
        }

    lines = []

    if lang == "zh":
        lines.append(f"📊 *过去 {s['days']} 天推送回顾*\n")
        lines.append(f"推送总数：{s['total_pushes']} 条")
    else:
        lines.append(f"📊 *지난 {s['days']}일 추송 리뷰*\n")
        lines.append(f"추송 총수: {s['total_pushes']}건")

    # 事件类型分布
    for etype, count in s["type_counts"].items():
        label = type_labels.get(etype, etype)
        lines.append(f"  {label}: {count}건")

    lines.append("")

    # 后续追踪统计
    d1 = s["d1_stats"]
    d3 = s["d3_stats"]
    d7 = s["d7_stats"]

    if lang == "zh":
        lines.append("*事件后续追踪（纯事实，非预测）：*")
    else:
        lines.append("*이벤트 후속 추적 (사실 기반, 예측 아님):*")

    if d1["total"] > 0:
        if lang == "zh":
            lines.append(f"· 推送后 1天：同方向延续 {pct(d1['continue'], d1['total'])}，"
                         f"反转 {pct(d1['reverse'], d1['total'])}，"
                         f"无显著变化 {pct(d1['flat'], d1['total'])}")
        else:
            lines.append(f"· 추송 후 1일: 같은 방향 {pct(d1['continue'], d1['total'])}, "
                         f"반전 {pct(d1['reverse'], d1['total'])}, "
                         f"변동 없음 {pct(d1['flat'], d1['total'])}")

    if d3["total"] > 0:
        if lang == "zh":
            lines.append(f"· 推送后 3天：同方向延续 {pct(d3['continue'], d3['total'])}，"
                         f"反转 {pct(d3['reverse'], d3['total'])}，"
                         f"无显著变化 {pct(d3['flat'], d3['total'])}")
        else:
            lines.append(f"· 추송 후 3일: 같은 방향 {pct(d3['continue'], d3['total'])}, "
                         f"반전 {pct(d3['reverse'], d3['total'])}, "
                         f"변동 없음 {pct(d3['flat'], d3['total'])}")

    if d7["total"] > 0:
        if lang == "zh":
            lines.append(f"· 推送后 7天：同方向延续 {pct(d7['continue'], d7['total'])}，"
                         f"反转 {pct(d7['reverse'], d7['total'])}，"
                         f"无显著变化 {pct(d7['flat'], d7['total'])}")
        else:
            lines.append(f"· 추송 후 7일: 같은 방향 {pct(d7['continue'], d7['total'])}, "
                         f"반전 {pct(d7['reverse'], d7['total'])}, "
                         f"변동 없음 {pct(d7['flat'], d7['total'])}")

    # 情绪 vs 实际
    sv = s["sentiment_vs_actual"]
    has_sentiment = any(v > 0 for k, v in sv.items() if k != "neutral")
    if has_sentiment:
        lines.append("")
        if lang == "zh":
            lines.append("*论坛情绪 vs 实际走势：*")
            if sv["bearish_down"]:
                lines.append(f"· 偏空情绪 + 实际下跌：{sv['bearish_down']}次")
            if sv["bearish_up"]:
                lines.append(f"· 偏空情绪 + 实际上涨：{sv['bearish_up']}次")
            if sv["bullish_up"]:
                lines.append(f"· 偏多情绪 + 实际上涨：{sv['bullish_up']}次")
            if sv["bullish_down"]:
                lines.append(f"· 偏多情绪 + 实际下跌：{sv['bullish_down']}次")
        else:
            lines.append("*포럼 감성 vs 실제 추이:*")
            if sv["bearish_down"]:
                lines.append(f"· 약세 감성 + 실제 하락: {sv['bearish_down']}건")
            if sv["bearish_up"]:
                lines.append(f"· 약세 감성 + 실제 상승: {sv['bearish_up']}건")
            if sv["bullish_up"]:
                lines.append(f"· 강세 감성 + 실제 상승: {sv['bullish_up']}건")
            if sv["bullish_down"]:
                lines.append(f"· 강세 감성 + 실제 하락: {sv['bullish_down']}건")

    # 最近追踪
    if s["recent_tracked"]:
        lines.append("")
        if lang == "zh":
            lines.append("*最近追踪事件：*")
        else:
            lines.append("*최근 추적 이벤트:*")
        for ev in s["recent_tracked"][:5]:
            arrow_1d = f"{ev['change_1d']:+.1f}%" if ev.get("change_1d") is not None else "—"
            arrow_3d = f"{ev['change_3d']:+.1f}%" if ev.get("change_3d") is not None else "—"
            arrow_7d = f"{ev['change_7d']:+.1f}%" if ev.get("change_7d") is not None else "—"
            lines.append(
                f"  {ev['stock_name']} ({ev['push_date']}): "
                f"1d {arrow_1d} | 3d {arrow_3d} | 7d {arrow_7d}"
            )

    lines.append("")
    if lang == "zh":
        lines.append("⚠️ 以上为历史事件统计，不构成未来预测或投资建议。")
    else:
        lines.append("⚠️ 위 내용은 과거 이벤트 통계이며, 미래 예측이나 투자 조언이 아닙니다.")

    return "\n".join(lines)


# ═══════════════════════════════════════════
#  4. 单条推送追踪
# ═══════════════════════════════════════════

def get_ticker_tracking(ticker, limit=10):
    """查询某只股票的所有推送追踪记录"""
    conn = _conn()
    rows = conn.execute("""
        SELECT * FROM push_events
        WHERE ticker = ?
        ORDER BY push_date DESC
        LIMIT ?
    """, (ticker, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def format_ticker_tracking(ticker, events, lang="ko"):
    """格式化单只股票的追踪记录"""
    from fetch_briefing import STOCK_NAMES

    name = STOCK_NAMES.get(ticker, ticker)

    if not events:
        if lang == "zh":
            return f"📊 {name} ({ticker}) — 暂无推送记录"
        return f"📊 {name} ({ticker}) — 추송 기록 없음"

    lines = []
    if lang == "zh":
        lines.append(f"📊 *{name} 推送追踪*\n")
    else:
        lines.append(f"📊 *{name} 추송 추적*\n")

    type_emoji = {
        "price_spike": "📈", "price_drop": "📉",
        "dart": "📋", "news": "📰",
        "forum_buzz": "💬", "crash_alert": "🚨",
    }

    for ev in events:
        emoji = type_emoji.get(ev["event_type"], "📌")
        lines.append(f"{emoji} {ev['push_date']} | ₩{ev['push_price']:,.0f} ({ev['push_change_pct']:+.1f}%)")
        if lang == "zh":
            lines.append(f"  事件: {ev['event_detail'][:60] or ev['event_type']}")
        else:
            lines.append(f"  이벤트: {ev['event_detail'][:60] or ev['event_type']}")

        # 后续价格
        parts = []
        if ev.get("change_1d") is not None:
            parts.append(f"1d: {ev['change_1d']:+.1f}%")
        if ev.get("change_3d") is not None:
            parts.append(f"3d: {ev['change_3d']:+.1f}%")
        if ev.get("change_7d") is not None:
            parts.append(f"7d: {ev['change_7d']:+.1f}%")

        if parts:
            if lang == "zh":
                lines.append(f"  后续: {' | '.join(parts)}")
            else:
                lines.append(f"  후속: {' | '.join(parts)}")
        else:
            if lang == "zh":
                lines.append(f"  后续: 追踪中...")
            else:
                lines.append(f"  후속: 추적 중...")
        lines.append("")

    if lang == "zh":
        lines.append("⚠️ 历史数据回顾，不构成投资建议。")
    else:
        lines.append("⚠️ 과거 데이터 리뷰이며, 투자 조언이 아닙니다.")

    return "\n".join(lines)


# ═══════════════════════════════════════════
#  5. 推送钩子 — 集成到现有推送管道
# ═══════════════════════════════════════════

def hook_crash_alert(ticker, change_pct, close_price, date_str=None):
    """暴跌预警推送时调用"""
    sentiment = "bearish" if change_pct < 0 else "bullish"
    event_type = "crash_alert" if change_pct < -3 else "price_drop" if change_pct < 0 else "price_spike"
    return record_push_event(
        ticker=ticker,
        push_price=close_price,
        event_type=event_type,
        push_change_pct=change_pct,
        event_detail=f"{'급락' if change_pct < 0 else '급등'} {change_pct:+.1f}%",
        sentiment=sentiment,
        push_date=date_str,
    )


def hook_news_alert(ticker, close_price, news_title, sentiment="neutral", date_str=None):
    """新闻推送时调用"""
    return record_push_event(
        ticker=ticker,
        push_price=close_price,
        event_type="news",
        event_detail=news_title[:120],
        sentiment=sentiment,
        push_date=date_str,
    )


def hook_dart_alert(ticker, close_price, dart_title, date_str=None):
    """DART公告推送时调用"""
    return record_push_event(
        ticker=ticker,
        push_price=close_price,
        event_type="dart",
        event_detail=dart_title[:120],
        push_date=date_str,
    )


def hook_forum_alert(ticker, close_price, forum_detail, sentiment="neutral", date_str=None, forum_data=None):
    """论坛异常推送时调用"""
    return record_push_event(
        ticker=ticker,
        push_price=close_price,
        event_type="forum_buzz",
        event_detail=forum_detail[:120],
        sentiment=sentiment,
        push_date=date_str,
        forum_sentiment=forum_data,
    )


# ═══════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════

def demo():
    """演示：用历史数据插入几条测试记录"""
    print("\n  📊 Push Tracker Demo\n")

    # 用实际市场数据创建几条测试记录
    from fetch_briefing import find_trading_date, get_stock, STOCK_NAMES

    date_str = find_trading_date()
    test_tickers = ["005930", "000660", "035720"]

    for ticker in test_tickers:
        data = get_stock(ticker, date_str)
        if data:
            evt = "price_drop" if data["change_pct"] < 0 else "price_spike"
            sent = "bearish" if data["change_pct"] < -1 else ("bullish" if data["change_pct"] > 1 else "neutral")
            pid = record_push_event(
                ticker=ticker,
                push_price=data["close"],
                event_type=evt,
                push_change_pct=data["change_pct"],
                event_detail=f"{'급락' if data['change_pct'] < 0 else '급등'} {data['change_pct']:+.1f}%",
                sentiment=sent,
                push_date=date_str,
            )
            print(f"  ✅ Recorded: {STOCK_NAMES.get(ticker)} #{pid}")

    # 显示统计
    print()
    stats = get_stats(30)
    print(format_stats(stats, "ko"))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "demo":
        demo()
    elif sys.argv[1] == "backfill":
        backfill_prices()
    elif sys.argv[1] == "stats":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        stats = get_stats(days)
        print(format_stats(stats, "ko"))
    elif sys.argv[1] == "track" and len(sys.argv) > 2:
        ticker = sys.argv[2]
        events = get_ticker_tracking(ticker)
        print(format_ticker_tracking(ticker, events, "ko"))
    else:
        print(__doc__)
