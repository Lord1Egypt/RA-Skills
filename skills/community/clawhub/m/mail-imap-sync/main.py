import imaplib
import os
import json
import re
import html2text
import tempfile
from datetime import datetime, timedelta, timezone
from email import message_from_bytes
from email.header import decode_header, make_header
from concurrent.futures import ThreadPoolExecutor
from dateutil import parser as dtparser
from zoneinfo import ZoneInfo

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "emails")
STATE_FILE = os.path.join(SCRIPT_DIR, "state.json")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

LOCAL_TZ = ZoneInfo("Asia/Taipei")

# ======================
# JSON 安全
# ======================
def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_atomic(path, data):
    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

# ======================
# 工具
# ======================
def decode_str(s):
    if not s:
        return ""
    return str(make_header(decode_header(s)))

def html_to_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html)

def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', "_", s)[:50]

# ======================
# 时间标准化（🔥核心）【
# ======================
def normalize_email_date(date_str):
    try:
        dt = dtparser.parse(date_str)

        # 如果没有时区，默认当 UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # 北京时间（Asia/Shanghai）
        beijing_tz = ZoneInfo("Asia/Shanghai")
        local_dt = dt.astimezone(beijing_tz)

        return {
            "dt": local_dt.replace(tzinfo=None),  # 用于比较
            "iso": local_dt.isoformat(),          # 标准格式
            "readable": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(local_dt.timestamp())
        }

    except:
        now = datetime.now(ZoneInfo("Asia/Shanghai"))
        return {
            "dt": now.replace(tzinfo=None),
            "iso": now.isoformat(),
            "readable": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(now.timestamp())
        }

# ======================
# IMAP
# ======================
class IMAPClient:
    def __init__(self, host, user, password):
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login(user, password)
        self.mail.select("INBOX")

    def uidnext(self):
        typ, data = self.mail.status("INBOX", "(UIDNEXT)")
        if typ != "OK":
            return None
        m = re.search(rb"UIDNEXT\s+(\d+)", data[0])
        return int(m.group(1)) if m else None

    def search_since(self, since_str):
        typ, data = self.mail.uid("search", None, f'SINCE "{since_str}"')
        if typ != "OK":
            return []
        return data[0].split()

    def fetch_new(self, last_uid):
        typ, data = self.mail.uid("search", None, f"UID {last_uid+1}:*")
        if typ != "OK":
            return []
        return data[0].split()

    def fetch_email(self, uid):
        typ, data = self.mail.uid("fetch", str(uid), "(BODY.PEEK[])")
        if typ == "OK":
            return data[0][1]
        return b""

    def logout(self):
        try:
            self.mail.logout()
        except:
            pass

# ======================
# 解析
# ======================
def parse_email(raw):
    msg = message_from_bytes(raw)

    subject = decode_str(msg.get("Subject"))
    from_ = decode_str(msg.get("From"))
    date = msg.get("Date", "")
    message_id = msg.get("Message-ID", "")

    time_info = normalize_email_date(date)

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
            elif ctype == "text/html":
                html = part.get_payload(decode=True).decode(errors="ignore")
                body = html_to_text(html)
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return {
        "subject": subject,
        "from": from_,
        "date": date,
        "body": body,
        "message_id": message_id,
        "time": time_info
    }

# ======================
# 保存
# ======================
def save_email(data, uid, account):
    dt = data["time"]["dt"]

    path = os.path.join(BASE_DIR, account, str(dt.year), f"{dt.month:02d}", f"{dt.day:02d}")
    os.makedirs(path, exist_ok=True)

    title = sanitize(data["subject"] or "无标题")
    msg_id = sanitize(data["message_id"] or str(uid))

    filename = f"{uid}_{msg_id}_{title}.md"
    full = os.path.join(path, filename)

    if os.path.exists(full):
        return None

    content = f"""# {data['subject']}

From: {data['from']}
Date(raw): {data['date']}
Date(local): {data['time']['readable']}
Date(ISO): {data['time']['iso']}
Timestamp: {data['time']['timestamp']}

UID: {uid}
Message-ID: {data['message_id']}
Account: {account}

---

{data['body']}
"""

    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

    return full

# ======================
# 核心逻辑
# ======================
def process_account(acc, state):
    name = acc["name"]
    key = acc["user"]

    acc_state = state["accounts"].setdefault(key, {
        "last_uid": 0,
        "initialized": False
    })

    client = IMAPClient(acc["imap_host"], acc["user"], acc["pass"])

    if acc_state["initialized"] and acc_state["last_uid"] == 0:
        uidnext = client.uidnext()
        if uidnext:
            acc_state["last_uid"] = uidnext - 1

    mode = acc.get("mode", "init")
    results = []

    if not acc_state["initialized"]:

        max_uid = 0

        if mode != "init":
            if mode == "recent":
                cutoff = (datetime.now(LOCAL_TZ) - timedelta(days=acc.get("recent_days", 7))).replace(tzinfo=None)
            else:
                cutoff = normalize_email_date(acc.get("since"))["dt"]

            since_str = cutoff.strftime("%d-%b-%Y")
            uids = client.search_since(since_str)

            for uid in uids:
                uid_int = int(uid)
                raw = client.fetch_email(uid_int)
                data = parse_email(raw)

                if data["time"]["dt"] < cutoff:
                    continue

                if save_email(data, uid_int, name):
                    results.append(uid_int)

                max_uid = max(max_uid, uid_int)

        else:
            uidnext = client.uidnext()
            if uidnext:
                max_uid = uidnext - 1

        acc_state["last_uid"] = max_uid
        acc_state["initialized"] = True

        client.logout()
        return results

    # 增量
    uids = client.fetch_new(acc_state["last_uid"])
    max_uid = acc_state["last_uid"]

    for uid in uids:
        uid_int = int(uid)
        raw = client.fetch_email(uid_int)
        data = parse_email(raw)

        if save_email(data, uid_int, name):
            results.append(uid_int)

        max_uid = max(max_uid, uid_int)

    acc_state["last_uid"] = max_uid
    client.logout()

    return results

# ======================
# 主入口
# ======================
def run():
    config = load_json(CONFIG_FILE, {})
    state = load_json(STATE_FILE, {"accounts": {}})

    all_results = []

    try:
        with ThreadPoolExecutor(max_workers=len(config["accounts"])) as pool:
            futures = [pool.submit(process_account, acc, state) for acc in config["accounts"]]

            for f in futures:
                all_results.extend(f.result())

    finally:
        save_json_atomic(STATE_FILE, state)

    print(f"\n📊 同步完成: {len(all_results)} 封")


if __name__ == "__main__":
    run()