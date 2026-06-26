#!/usr/bin/env python3
"""Fetch unread Gmail from yesterday and today, print as JSON."""
import html as _html
import imaplib
import json
import os
import re
from datetime import date, datetime, timedelta
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
# Priority 1: individual environment variables (no file read needed)
_env_host     = os.environ.get("IMAP_HOST", "").strip()
_env_port     = os.environ.get("IMAP_PORT", "").strip()
_env_username = os.environ.get("IMAP_USERNAME", "").strip()
_env_password = os.environ.get("IMAP_PASSWORD", "").strip()
_env_maxchars = os.environ.get("IMAP_MAX_BODY_CHARS", "").strip()

if _env_username and _env_password:
    # Credentials supplied entirely via env — no config file required
    IMAP_HOST = _env_host or "imap.gmail.com"
    IMAP_PORT = int(_env_port) if _env_port else 993
    USERNAME  = _env_username
    PASSWORD  = _env_password
    MAX_CHARS = min(int(_env_maxchars) if _env_maxchars else 2000, 2000)
else:
    # Priority 2: config file (EMAIL_CONFIG_PATH or default location)
    # The config file should contain ONLY the email fields listed in SKILL.md.
    config_path_env = os.environ.get("EMAIL_CONFIG_PATH", "").strip()
    if config_path_env:
        config_path = Path(config_path_env).expanduser()
    else:
        config_path = Path.home() / ".config" / "gmail-summarize" / "config.json"
    cfg = json.loads(config_path.read_text())
    email_cfg = cfg.get("email", {})

    IMAP_HOST = _env_host     or email_cfg.get("imapHost", "imap.gmail.com")
    IMAP_PORT = int(_env_port) if _env_port else int(email_cfg.get("imapPort", 993))
    USERNAME  = _env_username or email_cfg.get("imapUsername", "")
    PASSWORD  = _env_password or email_cfg.get("imapPassword", "")
    MAX_CHARS = min(int(_env_maxchars) if _env_maxchars else int(email_cfg.get("maxBodyChars", 2000)), 2000)

# ── Helpers ───────────────────────────────────────────────────────────────────
IMAP_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

def fmt_imap_date(d: date) -> str:
    return f"{d.day:02d}-{IMAP_MONTHS[d.month-1]}-{d.year}"

def decode_hdr(v: str) -> str:
    try:
        return str(make_header(decode_header(v or "")))
    except Exception:
        return v or ""

def html_to_text(h: str) -> str:
    h = re.sub(r"<br\s*/?>", "\n", h, flags=re.I)
    h = re.sub(r"</p>", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    return _html.unescape(h)

def extract_body(msg) -> str:
    if msg.is_multipart():
        plains, htmls = [], []
        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                continue
            ct = part.get_content_type()
            try:
                payload = part.get_content()
            except Exception:
                b = part.get_payload(decode=True) or b""
                payload = b.decode(part.get_content_charset() or "utf-8", errors="replace")
            if not isinstance(payload, str):
                continue
            if ct == "text/plain":
                plains.append(payload)
            elif ct == "text/html":
                htmls.append(payload)
        if plains:
            return "\n\n".join(plains).strip()
        if htmls:
            return html_to_text("\n\n".join(htmls)).strip()
        return ""
    try:
        payload = msg.get_content()
    except Exception:
        b = msg.get_payload(decode=True) or b""
        payload = b.decode(msg.get_content_charset() or "utf-8", errors="replace")
    if not isinstance(payload, str):
        return ""
    if msg.get_content_type() == "text/html":
        return html_to_text(payload).strip()
    return payload.strip()

# ── Date range ────────────────────────────────────────────────────────────────
today     = date.today()
yesterday = today - timedelta(days=1)
tomorrow  = today + timedelta(days=1)

# Python-side cutoff: yesterday 00:00:00 local time (naive)
cutoff_dt = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)

# ── Fetch via IMAP ────────────────────────────────────────────────────────────
client = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
client.login(USERNAME, PASSWORD)
client.select("INBOX")

# Use SINCE one day earlier as a wide net to compensate for UTC offset,
# then filter precisely on the Python side.
# X-GM-RAW restricts results to Gmail's Primary category only.
wide_since = yesterday - timedelta(days=1)
_, data = client.search(None,
    "SINCE", fmt_imap_date(wide_since),
    "BEFORE", fmt_imap_date(tomorrow),
    "UNSEEN",
    "X-GM-RAW", "category:primary",
)
ids = data[0].split() if data and data[0] else []

results = []
for imap_id in ids:
    _, fetched = client.fetch(imap_id, "(BODY.PEEK[] UID)")
    if not fetched:
        continue
    raw = next((bytes(x[1]) for x in fetched if isinstance(x, tuple) and len(x) >= 2), None)
    if not raw:
        continue

    parsed = BytesParser(policy=policy.default).parsebytes(raw)
    sender  = parseaddr(parsed.get("From", ""))[1].strip().lower()
    subject = decode_hdr(parsed.get("Subject", ""))
    date_str = parsed.get("Date", "")
    body    = extract_body(parsed)[:MAX_CHARS] or "(empty)"

    # ── Python-side date filter (precise, timezone-aware) ────────────────────
    try:
        msg_dt = parsedate_to_datetime(date_str)          # aware datetime
        msg_local = msg_dt.astimezone().replace(tzinfo=None)  # convert to local naive
        if msg_local < cutoff_dt:
            continue  # older than yesterday 00:00 local → skip
    except Exception:
        pass  # if date unparseable, include it rather than silently drop

    results.append({
        "sender":  sender,
        "subject": subject,
        "date":    date_str,
        "body":    body,
    })

client.logout()
output = json.dumps(results, ensure_ascii=False, indent=2)
# Guard: exec tool has a 10,000-char output limit; truncate gracefully if needed.
if len(output) > 9000:
    output = json.dumps(results, ensure_ascii=False, separators=(",", ":"))
print(output)
