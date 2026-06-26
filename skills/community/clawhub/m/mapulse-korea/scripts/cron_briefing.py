#!/usr/bin/env python3
"""
Mapulse Cron — 매일 아침 시황 + 주요 뉴스 자동 push
KST 22:00 (UTC 13:00) 실행 — 미국 시장 개장 후, 사용자 취침 전 최적 타이밍

crontab: 0 13 * * 1-5 /usr/bin/python3 /path/to/cron_briefing.py
"""

import os
import sys
import json
import requests
import time

sys.path.insert(0, os.path.dirname(__file__))

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


def get_all_users():
    """모든 활성 사용자"""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT user_id FROM users WHERE total_calls > 0").fetchall()
    conn.close()
    return [r["user_id"] for r in rows]


def send_message(chat_id, text):
    """텔레그램 메시지 전송"""
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
    from chat_query import process_query_fast
    from fetch_briefing import find_trading_date, get_stock, STOCK_NAMES, fmt_arrow

    date_str = find_trading_date()

    # 1. 시장 전체 브리핑
    market_brief = process_query_fast("코스피 시황")

    # 2. 사용자별 개인화 push
    users = get_all_users()
    sent = 0

    for uid in users:
        try:
            # 사용자 watchlist 확인
            watchlist = get_user_watchlist(uid)

            lines = [f"🌙 *Mapulse 이브닝 브리핑*\n"]

            if watchlist:
                lines.append("*📋 관심 종목:*")
                for ticker in watchlist:
                    data = get_stock(ticker, date_str)
                    if data:
                        name = STOCK_NAMES.get(ticker, ticker)
                        arrow = fmt_arrow(data["change_pct"])
                        lines.append(f"  {arrow} {name}: ₩{data['close']:,} ({data['change_pct']:+.1f}%)")
                lines.append("")

            lines.append(market_brief)

            # Personalized portfolio impact
            if watchlist:
                watchlist_data = []
                for t in watchlist:
                    d = get_stock(t, date_str)
                    if d:
                        watchlist_data.append(d)
                if watchlist_data:
                    try:
                        from llm import call_llm, MODEL_FAST
                        stock_summary = "\n".join([
                            f"{STOCK_NAMES.get(d['ticker'], d['ticker'])}: {d['change_pct']:+.1f}%"
                            for d in watchlist_data
                        ])
                        impact = call_llm(
                            messages=[{
                                "role": "system",
                                "content": "You are Mapulse, a Korean stock analyst. Given a user's watchlist, provide 3-5 lines of personalized impact in Korean: which stocks need attention, sector patterns, and one action for tomorrow. Be specific with levels."
                            }, {
                                "role": "user",
                                "content": f"관심종목 실적:\n{stock_summary}\n\n포트폴리오 영향과 내일 행동 지침:"
                            }],
                            model=MODEL_FAST, max_tokens=300, temperature=0.2,
                        )
                        if impact:
                            lines.append("\n📌 *내 포트폴리오 영향:*")
                            lines.append(impact)
                    except:
                        pass

            message = "\n".join(lines)
            if send_message(uid, message):
                sent += 1
        except:
            pass
        time.sleep(0.5)

    print(f"Morning briefing sent to {sent}/{len(users)} users")


def get_user_watchlist(user_id):
    """사용자 watchlist 조회"""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT ticker FROM watchlist WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [r["ticker"] for r in rows]


if __name__ == "__main__":
    run()
