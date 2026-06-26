#!/usr/bin/env python3
"""
Mapulse — Day-2 사용자 프로필 설문
매일 10:00 KST 실행

- 어제 가입한 유저 중 profile_complete=0 인 유저에게
  push 설정 질문 1개 전송
- 응답은 bot handler에서 처리 (callback_query)

crontab (CST = KST - 1h):
  0 9 * * * → KST 10:00
"""

import os
import sys
import sqlite3
import time
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_tables():
    """user_profile 테이블 존재 확인"""
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id TEXT PRIMARY KEY,
            focus_type TEXT DEFAULT '',
            focus_stocks TEXT DEFAULT '',
            push_preference TEXT DEFAULT 'standard',
            prefer_panorama INTEGER DEFAULT 1,
            profile_complete INTEGER DEFAULT 0,
            profile_asked_at TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def find_day2_users():
    """어제 가입 + profile 미완료 유저 찾기"""
    conn = get_conn()

    # 어제 날짜 범위 (UTC 기준)
    now = datetime.utcnow()
    yesterday_start = (now - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    yesterday_end = (now - timedelta(days=1)).strftime("%Y-%m-%d 23:59:59")

    # users 테이블에서 어제 생성된 유저
    users = conn.execute(
        """SELECT u.user_id, u.first_name
           FROM users u
           WHERE u.created_at BETWEEN ? AND ?""",
        (yesterday_start, yesterday_end)
    ).fetchall()

    targets = []
    for u in users:
        uid = u["user_id"]
        # user_profile 확인
        profile = conn.execute(
            "SELECT profile_complete, profile_asked_at FROM user_profile WHERE user_id=?",
            (uid,)
        ).fetchone()

        if profile and profile["profile_complete"] == 1:
            continue  # 이미 완료
        if profile and profile["profile_asked_at"]:
            continue  # 이미 질문 보냄

        targets.append({"user_id": uid, "first_name": u["first_name"] or ""})

    conn.close()
    return targets


def send_survey(chat_id, first_name=""):
    """Day-2 설문 전송"""
    name = first_name or "User"

    text = (
        f"🎯 {name}님, Mapulse를 더 맞춤화하고 싶어요!\n\n"
        f"어떤 알림을 받고 싶으세요?\n\n"
        f"1️⃣ 중요한 뉴스만 (하루 3회)\n"
        f"2️⃣ 기본 추송 (하루 4회)\n"
        f"3️⃣ 관심 종목 변동 알림 포함\n\n"
        f"번호를 보내주세요!"
    )

    if not TOKEN:
        print(f"  [DRY] Would send to {chat_id}: {text[:60]}...")
        return True

    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
            },
            timeout=10
        )
        return resp.json().get("ok", False)
    except Exception as e:
        print(f"  Send error to {chat_id}: {e}")
        return False


def mark_asked(user_id):
    """설문 보냈음을 기록"""
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
    conn.execute(
        "UPDATE user_profile SET profile_asked_at=datetime('now'), updated_at=datetime('now') WHERE user_id=?",
        (user_id,)
    )
    conn.commit()
    conn.close()


def handle_day2_response(user_id, text):
    """
    Day-2 설문 응답 처리 (bot handler에서 호출)
    Returns: 응답 메시지 문자열 or None (설문 대상 아님)
    """
    conn = get_conn()
    profile = conn.execute(
        "SELECT profile_complete, profile_asked_at FROM user_profile WHERE user_id=?",
        (user_id,)
    ).fetchone()
    conn.close()

    # 설문 보낸 적 없거나 이미 완료 → None
    if not profile or not profile["profile_asked_at"] or profile["profile_complete"] == 1:
        return None

    tl = text.strip().lower()

    pref_map = {
        "1": "important_only",
        "1️⃣": "important_only",
        "2": "standard",
        "2️⃣": "standard",
        "3": "all",
        "3️⃣": "all",
    }

    pref = pref_map.get(tl)
    if not pref:
        return None  # 설문 응답이 아님 → 일반 처리

    conn = get_conn()
    conn.execute(
        """UPDATE user_profile
           SET push_preference=?, profile_complete=1, updated_at=datetime('now')
           WHERE user_id=?""",
        (pref, user_id)
    )
    conn.commit()
    conn.close()

    labels = {
        "important_only": "중요한 뉴스만 (하루 3회)",
        "standard": "기본 추송 (하루 4회)",
        "all": "관심 종목 변동 알림 포함",
    }

    return (
        f"✅ 알림 설정 완료!\n\n"
        f"📬 *{labels[pref]}*\n\n"
        f"설정은 언제든 변경 가능합니다.\n"
        f"궁금한 종목이 있으면 바로 물어보세요! 🚀"
    )


def run():
    """메인 실행: day-2 유저 찾아서 설문 전송"""
    init_tables()

    print(f"[{datetime.now()}] Day-2 survey scan...")
    targets = find_day2_users()

    if not targets:
        print("  No day-2 users to survey.")
        return

    print(f"  Found {len(targets)} day-2 users")

    sent = 0
    for u in targets:
        uid = u["user_id"]
        if send_survey(uid, u["first_name"]):
            mark_asked(uid)
            sent += 1
            print(f"  ✓ Sent survey to {uid}")
        time.sleep(0.5)

    print(f"  Done: {sent}/{len(targets)} surveys sent.")


if __name__ == "__main__":
    run()
