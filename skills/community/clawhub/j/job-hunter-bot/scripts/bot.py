#!/usr/bin/env python3
"""
Job Hunter Telegram Bot - sends scored jobs with inline action buttons.
Configure in config.json. Run: python3 bot.py
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


class JobBot:
    def __init__(self):
        with open(CONFIG_PATH) as f:
            self.config = json.load(f)
        self.token = self.config["telegram_bot_token"]
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.authorized = set(self.config.get("authorized_users", [self.config["telegram_user_id"]]))
        self.profile = self.config.get("candidate", {})
        self.last_update_id = 0

    def _post(self, method, payload):
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{self.api}/{method}", data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read())
        except Exception as e:
            print(f"  API error ({method}): {e}")
            return None

    def send(self, chat_id, text, buttons=None):
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if buttons:
            payload["reply_markup"] = {"inline_keyboard": buttons}
        return self._post("sendMessage", payload)

    def answer_callback(self, callback_id, text=""):
        return self._post("answerCallbackQuery", {
            "callback_query_id": callback_id, "text": text
        })

    def get_db(self):
        return sqlite3.connect(DB_PATH)

    def send_job_card(self, chat_id, job):
        """Send a single job as a card with buttons."""
        j = dict(zip(["job_id", "title", "company", "location", "url",
                       "description", "requirements", "required_years"], job))
        s = score_job(j["title"], j["company"], j["location"],
                      j["description"], j["requirements"],
                      j["required_years"] or 0, self.profile)

        emoji = {"APPLY": "🟢", "REVIEW": "🟡", "SKIP": "🔴"}
        yr = j["required_years"] or 0
        yr_text = "No experience required" if yr == 0 else f"{yr} years exp."

        msg = (
            f"{emoji.get(s['recommendation'], '⚪')} <b>{s['score']}%</b> - "
            f"<b>{j['title']}</b>\n"
            f"🏢 {j['company']}\n"
            f"📍 {j['location']}\n"
            f"⏱ {yr_text}"
        )

        buttons = [
            [{"text": "📋 Details", "callback_data": f"details_{j['job_id']}"},
             {"text": "✅ Apply", "callback_data": f"apply_{j['job_id']}"}],
        ]
        if j.get("url"):
            buttons.append([{"text": "🔗 LinkedIn", "url": j["url"]}])
        buttons.append([{"text": "🗑️ Remove", "callback_data": f"remove_{j['job_id']}"}])

        self.send(chat_id, msg, buttons)

    def handle_command(self, chat_id, text):
        cmd = text.strip().split("@")[0].lower()
        conn = self.get_db()
        c = conn.cursor()

        if cmd == "/top":
            c.execute("SELECT job_id, title, company, location, url, description, requirements, required_years FROM jobs WHERE status != 'removed' ORDER BY title")
            rows = c.fetchall()
            top = []
            for r in rows:
                s = score_job(r[1], r[2], r[3], r[5], r[6], r[7] or 0, self.profile)
                if s["score"] >= 60:
                    top.append((s["score"], r))
            top.sort(key=lambda x: x[0], reverse=True)
            if not top:
                self.send(chat_id, "No top jobs found (score >= 60%).")
            else:
                self.send(chat_id, f"🏆 <b>Top {len(top)} jobs:</b>")
                for _, job in top[:15]:
                    self.send_job_card(chat_id, job)
                    time.sleep(0.3)

        elif cmd == "/jobs":
            c.execute("SELECT COUNT(*) FROM jobs WHERE status != 'removed'")
            count = c.fetchone()[0]
            self.send(chat_id, f"📊 Total jobs: {count}\nUse /top for best matches.")

        elif cmd == "/search":
            self.send(chat_id, "🔍 Searching LinkedIn...")
            from linkedin_scraper import scrape_and_store
            new = scrape_and_store()
            self.send(chat_id, f"✅ Search done! {new} new jobs found.\nUse /top to see best matches.")

        elif cmd == "/stats":
            c.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
            stats = dict(c.fetchall())
            total = sum(stats.values())
            msg = f"📊 <b>Stats</b>\nTotal: {total}\n"
            for status, count in sorted(stats.items()):
                msg += f"- {status}: {count}\n"
            self.send(chat_id, msg)

        elif cmd == "/help":
            self.send(chat_id,
                "<b>Commands:</b>\n"
                "/top - Top matching jobs\n"
                "/jobs - Job count\n"
                "/search - Search LinkedIn now\n"
                "/stats - Statistics\n"
                "/help - This message")

        else:
            self.send(chat_id, "Unknown command. Try /help")

        conn.close()

    def handle_callback(self, callback):
        data = callback.get("data", "")
        chat_id = callback["message"]["chat"]["id"]
        cb_id = callback["id"]

        if data.startswith("details_"):
            job_id = data.replace("details_", "")
            conn = self.get_db()
            c = conn.cursor()
            c.execute("SELECT title, company, location, description, requirements, required_years FROM jobs WHERE job_id = ?", (job_id,))
            row = c.fetchone()
            conn.close()
            if row:
                s = score_job(row[0], row[1], row[2], row[3], row[4], row[5] or 0, self.profile)
                msg = f"<b>{row[0]}</b> @ {row[1]}\n📍 {row[2]}\n\n"
                msg += f"<b>Score: {s['score']}%</b>\n"
                for b in s["breakdown"]:
                    msg += f"- {b}\n"
                if row[3]:
                    desc = row[3][:1500]
                    msg += f"\n<b>Description:</b>\n{desc}"
                self.send(chat_id, msg)
            self.answer_callback(cb_id, "Details loaded")

        elif data.startswith("apply_"):
            job_id = data.replace("apply_", "")
            conn = self.get_db()
            conn.execute("UPDATE jobs SET status = 'applied' WHERE job_id = ?", (job_id,))
            conn.commit()
            conn.close()
            self.answer_callback(cb_id, "Marked as applied!")
            self.send(chat_id, f"✅ Job {job_id} marked as applied!")

        elif data.startswith("remove_"):
            job_id = data.replace("remove_", "")
            conn = self.get_db()
            conn.execute("UPDATE jobs SET status = 'removed' WHERE job_id = ?", (job_id,))
            conn.commit()
            conn.close()
            self.answer_callback(cb_id, "Removed")

    def run(self):
        print("🤖 Job Hunter Bot started! Listening...")
        while True:
            try:
                result = self._post("getUpdates", {
                    "offset": self.last_update_id + 1, "timeout": 30
                })
                if not result or not result.get("ok"):
                    time.sleep(5)
                    continue

                for update in result.get("result", []):
                    self.last_update_id = update["update_id"]

                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        user_id = msg["from"]["id"]
                        text = msg.get("text", "")

                        if user_id not in self.authorized:
                            continue
                        if text.startswith("/"):
                            self.handle_command(chat_id, text)

                    elif "callback_query" in update:
                        cb = update["callback_query"]
                        if cb["from"]["id"] in self.authorized:
                            self.handle_callback(cb)

            except KeyboardInterrupt:
                print("\nBot stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)


if __name__ == "__main__":
    bot = JobBot()
    bot.run()
