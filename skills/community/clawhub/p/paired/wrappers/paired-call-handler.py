#!/usr/bin/env python3
"""paired-call-handler — Decide what to do when an incoming call arrives.

Called by paired-call-watch via its --hook mechanism. Receives BTCALL_* env vars.

Logic:
  1. If caller is on the trusted-numbers list:
       a. Hang up the call (so the caller doesn't keep ringing)
       b. Send an SMS reply: "Hi, Agent bot here. the user is unavailable to take a
          call right now. SMS me 'Hi Agent, ...' if you need a question
          answered, or text me normally and the user will reply when free."
       c. Post Telegram notification with caller info + what was sent
       d. Return exit code 1 (let paired-call-watch know we handled it; don't
          auto-answer because we already hung up)
  2. If NOT on trusted list:
       a. Do nothing
       b. Return exit code 1 (just notify — current paired-call-watch-tg-hook handles
          the actual notification independently)

Exit codes match the paired-call-watch hook contract:
  0 = answer the call
  1 = ignore (let it ring)
  2 = hang up

We mostly return 1 because we either:
  - Already hung up programmatically (trusted path), and don't want a second hangup
  - Or genuinely want it to keep ringing (untrusted path)

Logs: ${PAIRED_DATA_DIR}/call-handler.log
Config: ${HOME}/.config/paired/trusted-numbers.conf (shared with paired-respond)

Cooldown protects against retry storms — same caller within 60s gets 1 SMS,
not 5.
"""
from __future__ import annotations
import json
import logging
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
_HOME = str(Path.home())

LOG_DIR = Path.home() / "bt-skill-expansion"
LOG_FILE = LOG_DIR / "call-handler.log"
TG_ENV = Path.home() / ".config" / "paired-sms-watch" / "telegram.env"
TRUSTED_NUMBERS_FILE = Path(f"{_HOME}/.config/paired/trusted-numbers.conf")

SMS_SEND_BIN = f"{_HOME}/bin/paired-sms-send"
BT_CALL_BIN = f"{_HOME}/bin/paired-call"

# Cooldown for outbound SMS replies: don't spam the same caller if they call
# repeatedly. Tracked in its own DB to not interfere with SMS cooldown.
CALL_COOLDOWN_SECONDS = 60
COOLDOWN_DB = LOG_DIR / "call-handler-cooldown.db"

AUTO_REPLY_TEMPLATE = (
    "Hi, Agent bot here. Agent is unavailable ({when}). "
    "Text 'Hi Agent, <question>' for an instant answer, "
    "or message and Agent will get back to you."
)


def build_auto_reply() -> str:
    """Build the auto-reply with a current local time stamp."""
    # UK local time, 24h format. The phone owner is GB-based.
    when = time.strftime("%H:%M %a %d %b", time.localtime())
    return AUTO_REPLY_TEMPLATE.format(when=when)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [paired-call-handler] %(levelname)s: %(message)s",
)
log = logging.getLogger()


def normalize_uk(num: str) -> str:
    if not num:
        return ""
    n = num.strip().replace(" ", "").replace("-", "")
    if n.startswith("+44"):
        return "0" + n[3:]
    if n.startswith("0044"):
        return "0" + n[4:]
    if n.startswith("44") and len(n) == 12:
        return "0" + n[2:]
    return n


def load_trusted() -> set:
    if not TRUSTED_NUMBERS_FILE.exists():
        return set()
    out = set()
    try:
        for line in TRUSTED_NUMBERS_FILE.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            n = normalize_uk(line)
            if n:
                out.add(n)
    except OSError as e:
        log.warning(f"trusted-list read failed: {e}")
    return out


def check_and_set_cooldown(sender_norm: str) -> tuple[bool, float]:
    """Returns (allowed, seconds_remaining)."""
    COOLDOWN_DB.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    entries = {}
    if COOLDOWN_DB.exists():
        try:
            for line in COOLDOWN_DB.read_text().splitlines():
                line = line.strip()
                if not line or "\t" not in line:
                    continue
                num, ts = line.split("\t", 1)
                try:
                    entries[num] = float(ts)
                except ValueError:
                    continue
        except OSError:
            pass

    cutoff = now - 86400
    entries = {k: v for k, v in entries.items() if v > cutoff}

    last = entries.get(sender_norm, 0)
    if now - last < CALL_COOLDOWN_SECONDS:
        return False, CALL_COOLDOWN_SECONDS - (now - last)

    entries[sender_norm] = now
    try:
        tmp = str(COOLDOWN_DB) + ".tmp"
        with open(tmp, "w") as f:
            for k, v in entries.items():
                f.write(f"{k}\t{v}\n")
        os.replace(tmp, COOLDOWN_DB)
    except OSError as e:
        log.warning(f"cooldown DB write failed: {e}")
    return True, 0.0


def hangup_call() -> tuple[bool, str]:
    """End the current call via paired-call hangup."""
    if not Path(BT_CALL_BIN).exists():
        return False, f"binary missing: {BT_CALL_BIN}"
    try:
        proc = subprocess.run(
            [BT_CALL_BIN, "hangup"],
            capture_output=True, text=True, timeout=15,
        )
    except subprocess.TimeoutExpired:
        return False, "hangup timeout"
    except OSError as e:
        return False, f"exec failed: {e}"
    if proc.returncode != 0:
        return False, f"rc={proc.returncode} stderr={(proc.stderr or '')[:120]!r}"
    return True, "hung up"


def send_sms(number: str, body: str) -> tuple[bool, str]:
    """Send an SMS via paired-sms-send with auto-unlock + relock."""
    if not Path(SMS_SEND_BIN).exists():
        return False, f"binary missing: {SMS_SEND_BIN}"
    try:
        proc = subprocess.run(
            [SMS_SEND_BIN, "--auto-unlock", "--relock", number, body],
            capture_output=True, text=True, timeout=90,
        )
    except subprocess.TimeoutExpired:
        return False, "sms-send timeout"
    except OSError as e:
        return False, f"exec failed: {e}"

    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        return False, f"rc={proc.returncode} stderr={(proc.stderr or '')[:120]!r}"
    try:
        last_line = out.splitlines()[-1] if out else ""
        result = json.loads(last_line)
        if result.get("ok"):
            return True, f"sent (verify={result.get('verify', '?')})"
        return False, f"not-ok: {result.get('error', 'unknown')[:120]}"
    except (json.JSONDecodeError, IndexError):
        return True, "sent (no json out)"


def load_telegram_env() -> tuple[str | None, str | None]:
    if not TG_ENV.exists():
        return None, None
    token = chat = None
    try:
        for line in TG_ENV.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k.strip() == "TG_BOT_TOKEN":
                token = v
            elif k.strip() == "TG_CHAT_ID":
                chat = v
    except OSError:
        pass
    return token, chat


def telegram_send(token: str, chat_id: str, text: str) -> bool:
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return bool(json.loads(resp.read().decode("utf-8")).get("ok"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError) as e:
        log.error(f"telegram send failed: {e}")
        return False


def md_escape(s: str) -> str:
    return (s or "").replace("`", "'").replace("_", "\\_").replace("*", "\\*")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [paired-call-handler] %(levelname)s: %(message)s"))
    log.addHandler(fh)

    number = os.environ.get("BTCALL_NUMBER", "").strip()
    line_id = os.environ.get("BTCALL_LINE_ID", "").strip()
    name = os.environ.get("BTCALL_NAME", "").strip()
    call_type = os.environ.get("BTCALL_TYPE", "").strip()
    timestamp = os.environ.get("BTCALL_TIMESTAMP", "").strip()

    raw = number or line_id
    log.info(f"Triggered: type={call_type} number={raw!r} name={name!r} ts={timestamp}")

    if call_type != "incoming":
        log.info(f"Not an incoming call (type={call_type}); ignoring")
        return 1

    if not raw:
        log.info("No caller ID — withheld or unknown; ignoring (let it ring)")
        return 1

    normalized = normalize_uk(raw)
    trusted = load_trusted()
    log.info(f"Caller normalized to {normalized!r}; trusted-list size={len(trusted)}")

    if normalized not in trusted:
        log.info(f"Caller {normalized} NOT trusted — letting it ring (no action)")
        return 1

    log.info(f"TRUSTED caller {normalized}: hangup + auto-SMS")

    # Cooldown — don't fire repeatedly for the same caller within 60s
    allowed, wait = check_and_set_cooldown(normalized)
    if not allowed:
        log.warning(f"COOLDOWN: {normalized} hit again within {CALL_COOLDOWN_SECONDS}s "
                    f"({wait:.1f}s remaining) — ignoring this ring")
        return 1

    # Step 1: hang up the call
    hung, hangup_info = hangup_call()
    log.info(f"Hangup: ok={hung} info={hangup_info}")

    # Step 2: send SMS reply
    reply_body = build_auto_reply()
    sms_ok, sms_info = send_sms(raw, reply_body)
    log.info(f"SMS reply: ok={sms_ok} info={sms_info}")

    # Step 3: Telegram notification (transparency)
    token, chat_id = load_telegram_env()
    if token and chat_id:
        safe_caller = md_escape(name or raw)
        safe_raw = md_escape(raw)
        safe_reply = md_escape(reply_body)
        safe_hangup = md_escape(hangup_info)
        safe_sms = md_escape(sms_info)

        status_emoji = "✅" if (hung and sms_ok) else "⚠️"
        msg = (
            f"📞 *Trusted caller — auto-handled* {status_emoji}\n"
            f"From: {safe_caller} ({safe_raw})\n\n"
            f"*Action:*\n"
            f"• Hangup: {'✅' if hung else '❌'} {safe_hangup}\n"
            f"• SMS reply: {'✅' if sms_ok else '❌'} {safe_sms}\n\n"
            f"*Reply sent:*\n{safe_reply}"
        )
        sent = telegram_send(token, chat_id, msg)
        log.info(f"Telegram alert: ok={sent}")

    # Always return 1 — we already hung up programmatically (or chose not to act)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log.exception(f"unhandled: {e}")
        sys.exit(1)
