#!/usr/bin/env python3
"""
Mapulse Cron — 뉴스 스캔 + 영향 있으면 즉시 push
장중 30분마다 실행

crontab: */30 0-6 * * 1-5 /usr/bin/python3 /path/to/cron_news_scan.py
"""

import os
import sys
import json
import hashlib
import time
import requests

sys.path.insert(0, os.path.dirname(__file__))

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


def get_all_users():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT user_id FROM users WHERE total_calls > 0").fetchall()
    conn.close()
    return [r["user_id"] for r in rows]


def is_seen(title_hash):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT hash FROM news_seen WHERE hash=?", (title_hash,)).fetchone()
    conn.close()
    return row is not None


def mark_seen(title_hash, source, title):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO news_seen (hash, source, title, seen_at) VALUES (?,?,?,?)",
        (title_hash, source, title, time.time())
    )
    conn.commit()
    conn.close()


def send_message(chat_id, text):
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=10
        )
        return resp.json().get("ok", False)
    except:
        return False


def run():
    from news_intelligence import get_intelligence_report

    news = get_intelligence_report()
    impactful = [n for n in news if n.get("impact")]

    if not impactful:
        print("No impactful news found")
        return

    # 필터: 이미 보낸 뉴스 제외
    new_alerts = []
    for n in impactful:
        h = hashlib.md5(n["title"][:80].encode()).hexdigest()[:12]
        if not is_seen(h):
            new_alerts.append(n)
            mark_seen(h, n["source"], n["title"])

    if not new_alerts:
        print("All impactful news already sent")
        return

    # ── Push Tracker: 뉴스 이벤트 기록 ──
    try:
        from push_tracker import hook_news_alert
        from fetch_briefing import get_stock, find_trading_date
        date_str = find_trading_date()
        for n in new_alerts[:5]:
            imp = n.get("impact", {})
            affected = imp.get("affected") or imp.get("sectors", [])
            if isinstance(affected, list):
                # 뉴스가 영향 주는 종목 찾기
                from chat_query import resolve_ticker
                for sector_name in affected:
                    ticker = resolve_ticker(sector_name)
                    if ticker and ticker not in ("KOSPI", "KOSDAQ"):
                        data = get_stock(ticker, date_str)
                        if data and data.get("close"):
                            sentiment = "bearish" if imp.get("direction", "").startswith("📉") else \
                                        "bullish" if imp.get("direction", "").startswith("📈") else "neutral"
                            hook_news_alert(ticker, data["close"], n["title"][:120], sentiment, date_str)
    except Exception as _e:
        pass

    # push 메시지 구성
    lines = ["⚡ *Mapulse 뉴스 알림*", ""]
    for n in new_alerts[:5]:
        imp = n["impact"]
        linked = f"[원문]({n['link']})" if n.get("link") else ""
        direction = imp.get("direction", "📰")
        # Support both old keys (impact_kr/affected) and new keys (impact/sectors)
        impact_text = imp.get("impact_kr") or imp.get("impact", "")
        affected = imp.get("affected") or imp.get("sectors", [])
        if isinstance(affected, list):
            affected_str = " / ".join(affected)
        else:
            affected_str = str(affected)

        lines.append(f"{direction} *{n['source']}*: {n['title'][:55]}")
        if impact_text:
            lines.append(f"  {impact_text}")
        if affected_str:
            lines.append(f"  📌 {affected_str}")
        if linked:
            lines.append(f"  🔗 {linked}")
        lines.append("")

    lines.append("⚠️ 공식 확인 전 참고용")
    message = "\n".join(lines)

    # 전체 사용자 push
    users = get_all_users()
    sent = 0
    for uid in users:
        if send_message(uid, message):
            sent += 1
        time.sleep(0.5)

    print(f"News alert ({len(new_alerts)} items) sent to {sent}/{len(users)} users")


if __name__ == "__main__":
    run()
