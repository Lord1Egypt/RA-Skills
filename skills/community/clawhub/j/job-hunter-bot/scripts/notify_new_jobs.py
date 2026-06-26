#!/usr/bin/env python3
"""
Notify users about new jobs via Telegram bot.
Scores each new job, sends good ones (score >= 50) with action buttons.
"""
import json
import sqlite3
import urllib.request
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scorer import score_job, load_profile

CONFIG_PATH = Path(__file__).parent / "config.json"
DB_PATH = Path(__file__).parent / "jobs.db"


def send_telegram(token, chat_id, text, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  Send error: {e}")
        return None


def notify_new_jobs(min_score=50):
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    token = config["telegram_bot_token"]
    notify_users = config.get("notify_users", [config["telegram_user_id"]])
    profile = config.get("candidate", {})

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT job_id, title, company, location, url, description,
               requirements, required_years
        FROM jobs WHERE status = 'new' ORDER BY found_date DESC
    """)
    rows = c.fetchall()

    if not rows:
        print("No new jobs.")
        return 0

    good_jobs = []
    for row in rows:
        j = dict(zip(["job_id", "title", "company", "location", "url",
                       "description", "requirements", "required_years"], row))
        s = score_job(j["title"], j["company"], j["location"],
                      j["description"], j["requirements"],
                      j["required_years"] or 0, profile)
        j.update(s)
        if j["score"] >= min_score:
            good_jobs.append(j)

    good_jobs.sort(key=lambda x: x["score"], reverse=True)

    if not good_jobs:
        for uid in notify_users:
            send_telegram(token, uid,
                f"🔍 Search done. {len(rows)} new jobs, none above {min_score}%.")
        # Mark as skipped
        for row in rows:
            c.execute("UPDATE jobs SET status = 'skipped' WHERE job_id = ?", (row[0],))
        conn.commit()
        conn.close()
        return 0

    for uid in notify_users:
        send_telegram(token, uid,
            f"🆕 <b>{len(good_jobs)} new matches!</b> (from {len(rows)} found)")
        time.sleep(0.3)

    sent_ids = []
    emoji = {"APPLY": "🟢", "REVIEW": "🟡", "SKIP": "🔴"}
    for j in good_jobs:
        yr = j["required_years"] or 0
        yr_text = "No exp. required" if yr == 0 else f"{yr} years exp."
        msg = (
            f"{emoji.get(j['recommendation'], '⚪')} <b>{j['score']}%</b> - "
            f"<b>{j['title']}</b>\n"
            f"🏢 {j['company']}\n📍 {j['location']}\n⏱ {yr_text}"
        )
        buttons = [
            [{"text": "📋 Details", "callback_data": f"details_{j['job_id']}"},
             {"text": "✅ Apply", "callback_data": f"apply_{j['job_id']}"}],
        ]
        if j.get("url"):
            buttons.append([{"text": "🔗 LinkedIn", "url": j["url"]}])
        buttons.append([{"text": "🗑️ Remove", "callback_data": f"remove_{j['job_id']}"}])

        for uid in notify_users:
            send_telegram(token, uid, msg, buttons)
        sent_ids.append(j["job_id"])
        time.sleep(0.5)

    for jid in sent_ids:
        c.execute("UPDATE jobs SET status = 'sent' WHERE job_id = ?", (jid,))
    skip_ids = [r[0] for r in rows if r[0] not in sent_ids]
    for jid in skip_ids:
        c.execute("UPDATE jobs SET status = 'skipped' WHERE job_id = ?", (jid,))
    conn.commit()
    conn.close()

    print(f"Sent {len(sent_ids)} jobs, skipped {len(skip_ids)}.")
    return len(sent_ids)


if __name__ == "__main__":
    score = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    notify_new_jobs(min_score=score)
