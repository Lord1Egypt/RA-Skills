#!/usr/bin/env python3
"""
Mapulse — 뉴스 수집 + 점수화 (push 하지 않음)
하루 3회 실행: 07:30, 13:30, 20:00 KST
수집한 뉴스를 news_digest 테이블에 저장 → 고정 push에서 참조

crontab (CST = KST - 1h):
  30 6  * * 1-5  → KST 07:30 (morning push용)
  30 12 * * 1-5  → KST 13:30 (afternoon push용)
  0  19 * * 1-5  → KST 20:00 (evening push용)
"""

import os
import sys
import hashlib
import time
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_news_digest_table():
    """news_digest 테이블 생성"""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS news_digest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT DEFAULT '',
            category TEXT DEFAULT '',
            level TEXT DEFAULT '',
            impact_direction TEXT DEFAULT '',
            impact_text TEXT DEFAULT '',
            impact_sectors TEXT DEFAULT '',
            score INTEGER DEFAULT 0,
            batch_time TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_digest_batch ON news_digest(batch_time);
        CREATE INDEX IF NOT EXISTS idx_digest_score ON news_digest(score DESC);
    """)
    conn.commit()
    conn.close()


def score_news(item):
    """뉴스 중요도 점수화 (0-100)"""
    score = 30  # base

    # Impact가 있으면 +30
    if item.get("impact"):
        score += 30
        direction = item["impact"].get("direction", "")
        if "🔴" in direction:
            score += 10  # negative news gets attention
        if "🟢" in direction:
            score += 5

    # L0 (공식) = +20
    if item.get("level") == "L0":
        score += 20

    # 한국 프리미엄 = +10
    if item.get("category") == "kr_premium":
        score += 10

    # Title length / specificity heuristic
    title = item.get("title", "")
    if any(kw in title.lower() for kw in ["breaking", "urgent", "속보", "긴급", "just in"]):
        score += 15

    return min(score, 100)


def run():
    """뉴스 수집 → 점수화 → news_digest 저장"""
    init_news_digest_table()

    from news_intelligence import get_intelligence_report

    print(f"[{datetime.now()}] Starting news aggregation...")
    news = get_intelligence_report()
    print(f"  Collected {len(news)} items")

    if not news:
        print("  No news found, exiting.")
        return

    batch_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_conn()

    new_count = 0
    for item in news:
        h = hashlib.md5(item["title"][:80].encode()).hexdigest()[:12]

        # 중복 체크 (news_digest + news_seen 모두)
        existing = conn.execute("SELECT hash FROM news_digest WHERE hash=?", (h,)).fetchone()
        if existing:
            continue

        impact = item.get("impact") or {}
        s = score_news(item)

        conn.execute(
            """INSERT OR IGNORE INTO news_digest
               (hash, source, title, link, category, level,
                impact_direction, impact_text, impact_sectors,
                score, batch_time)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                h,
                item.get("source", ""),
                item.get("title", ""),
                item.get("link", ""),
                item.get("category", ""),
                item.get("level", ""),
                impact.get("direction", ""),
                impact.get("impact", ""),
                json.dumps(impact.get("sectors", []), ensure_ascii=False) if impact.get("sectors") else "",
                s,
                batch_time,
            )
        )
        new_count += 1

    # news_seen 에도 마킹 (기존 호환)
    for item in news:
        h = hashlib.md5(item["title"][:80].encode()).hexdigest()[:12]
        conn.execute(
            "INSERT OR IGNORE INTO news_seen (hash, source, title, seen_at) VALUES (?,?,?,?)",
            (h, item.get("source", ""), item.get("title", ""), time.time())
        )

    conn.commit()

    # 오래된 digest 정리 (7일 이전)
    conn.execute("DELETE FROM news_digest WHERE created_at < datetime('now', '-7 days')")
    conn.commit()
    conn.close()

    print(f"  Saved {new_count} new items to news_digest (batch: {batch_time})")
    print(f"  Done.")


if __name__ == "__main__":
    run()
