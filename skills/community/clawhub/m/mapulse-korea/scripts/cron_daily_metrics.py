#!/usr/bin/env python3
"""
Mapulse — Daily usage stats report
Sends a usage summary to OPS_CHAT_IDS (your own Telegram user ID).

Env:
  TELEGRAM_BOT_TOKEN  — required
  MAPULSE_DB          — optional (default: data/mapulse.db)
  OPS_CHAT_IDS        — comma-separated Telegram user IDs to receive the report

crontab:
  0 8 * * * python3 cron_daily_metrics.py
"""

import os
import sys
import sqlite3
import requests
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))

DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OPS_CHAT_IDS = [x.strip() for x in os.environ.get("OPS_CHAT_IDS", "").split(",") if x.strip()]

KST = timezone(timedelta(hours=9))


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def collect_metrics():
    """Collect usage metrics."""
    conn = get_conn()
    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yesterday_utc = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    week_ago_utc = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

    m = {}
    m["total_users"] = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    m["active_users"] = conn.execute("SELECT COUNT(*) as c FROM users WHERE total_calls > 0").fetchone()["c"]
    m["new_today"] = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE created_at >= ?",
        (today_utc + " 00:00:00",)
    ).fetchone()["c"]
    m["new_yesterday"] = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE created_at >= ? AND created_at < ?",
        (yesterday_utc + " 00:00:00", today_utc + " 00:00:00")
    ).fetchone()["c"]
    m["new_7d"] = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE created_at >= ?",
        (week_ago_utc + " 00:00:00",)
    ).fetchone()["c"]
    m["watchlist_users"] = conn.execute(
        "SELECT COUNT(DISTINCT user_id) as c FROM watchlist"
    ).fetchone()["c"]

    conn.close()
    return m


def format_report(m):
    """Format daily report (HTML)."""
    date_str = datetime.now(KST).strftime("%Y-%m-%d (%a)")
    return (
        f"📊 <b>Mapulse Daily Stats</b>\n"
        f"📅 {date_str}\n\n"
        f"<b>👥 Users</b>\n"
        f"  Total: {m['total_users']}\n"
        f"  Active: {m['active_users']}\n"
        f"  Yesterday new: {m['new_yesterday']} | Today: {m['new_today']}\n"
        f"  7-day new: {m['new_7d']}\n\n"
        f"<b>📋 Engagement</b>\n"
        f"  Users with watchlist: {m['watchlist_users']}\n"
    )


def send_report(text):
    """Send to configured chat IDs."""
    if not BOT_TOKEN:
        print("[DRY RUN] Would send:")
        print(text)
        return

    if not OPS_CHAT_IDS:
        print("[SKIP] No OPS_CHAT_IDS configured")
        return

    for chat_id in OPS_CHAT_IDS:
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=15,
            )
            result = resp.json()
            if result.get("ok"):
                print(f"✅ Report sent to {chat_id}")
            else:
                print(f"❌ Send to {chat_id} failed: {result}")
        except Exception as e:
            print(f"❌ Error sending to {chat_id}: {e}")


if __name__ == "__main__":
    print(f"[{datetime.now()}] Collecting daily metrics...")
    m = collect_metrics()
    text = format_report(m)
    print(text)
    send_report(text)
