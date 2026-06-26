#!/usr/bin/env python3
"""paired-sms-command-hook — [DEPRECATED in v1.0.2] Legacy /sms /phone hook.

*** DEPRECATION NOTICE ***

This script is the legacy command hook from v1.0.0. It tails the agent's
session JSONL log and dispatches recognised commands. The OpenClaw safety
scanner correctly flagged this design as a "Memory and Context Poisoning"
risk: anything that lands in the agent session log (including text from
incoming SMS, ADB notification dumps, etc.) becomes a potential command
source. That is the wrong shape.

v1.0.2 ships a replacement: paired-inbox-hook. The new tool reads commands
from a dedicated, HMAC-signed inbox directory — a surface only the user
or an explicitly-trusted relay can write to. Use that instead.

IF YOU REALLY WANT THE OLD BEHAVIOUR (you do not), pass --legacy-jsonl-source
and --i-understand-the-risks. Without those flags the script refuses to run.

Original docs follow.

———

Runs alongside OpenClaw. Tails the latest agent session JSONL.
Recognized commands (in user messages):
  /sms <number> <body>     - send an SMS via paired-sms-send
  /phone <number>          - dial outbound voice call (you talk via phone earpiece)
  /phone <number> <message> - dial + speak via TTS (TRUSTED only) + SMS fail-soft (Note 9 audio block)
  /phone <number> attach <path> - dial + speak file via TTS (TRUSTED only) + SMS fail-soft (Note 9 audio block)
  /phone hangup            - end any active call
  /phone status            - show current call state

Usage (legacy, gated):
  paired-sms-command-hook --watch --legacy-jsonl-source --i-understand-the-risks
  paired-sms-command-hook --status

Reads token from ~/.config/paired-sms-watch/telegram.env (mode 600).
Logs to ${PAIRED_DATA_DIR}/sms-cmd-hook.log
Records dispatches in ${PAIRED_DATA_DIR}/sms-cmd-hook.jsonl
"""
from __future__ import annotations
import argparse
import json
import logging
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.parse
_HOME = str(Path.home())

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
LOG_DIR = Path.home() / "bt-skill-expansion"
HOOK_LOG = LOG_DIR / "sms-cmd-hook.log"
DISPATCH_LOG = LOG_DIR / "sms-cmd-hook.jsonl"
PID_FILE = Path(f"/run/user/{os.getuid()}/paired-sms-command-hook.pid")
TG_ENV_PATH = Path.home() / ".config" / "paired-sms-watch" / "telegram.env"
SMS_SEND_BIN = f"{_HOME}/bin/paired-sms-send"
PHONE_BIN = f"{_HOME}/bin/paired-call"

# Match: /sms <number> <body>
SMS_PATTERN = re.compile(
    r'(?:^|\s|\n)/sms\s+([+0-9]{6,16})\s+(.+?)(?:\n|$)',
    re.MULTILINE | re.DOTALL,
)
# Match: /phone <number>     - dial outbound (you talk via phone earpiece)
PHONE_DIAL_PATTERN = re.compile(
    r'(?:^|\s|\n)/phone\s+([+0-9]{6,16})(?:\s|\n|$)',
    re.MULTILINE,
)
# Match: /phone hangup, /phone end, /phone status
PHONE_VERB_PATTERN = re.compile(
    r'(?:^|\s|\n)/phone\s+(hangup|status|end)(?:\s|\n|$)',
    re.MULTILINE | re.IGNORECASE,
)
# Match: /phone <number> attach <path>  - dial + speak file content (TRUSTED only)
PHONE_ATTACH_PATTERN = re.compile(
    r'(?:^|\s|\n)/phone\s+([+0-9]{6,16})\s+attach\s+(\S+)(?:\s|\n|$)',
    re.MULTILINE,
)
# Match: /phone <number> <message>  - dial + speak via TTS (TRUSTED only)
# Must be tested AFTER attach (which has 'attach' as the second token).
PHONE_SAY_PATTERN = re.compile(
    r'(?:^|\s|\n)/phone\s+([+0-9]{6,16})\s+(.+?)(?:\n|$)',
    re.MULTILINE | re.DOTALL,
)
TRUSTED_NUMBERS_FILE = Path.home() / ".config" / "paired" / "trusted-numbers.conf"
SPEAK_BIN = f"{_HOME}/bin/paired-call-and-speak"
MAX_TTS_CHARS = 1500

# Owner-only — only this sender_id is honored
ALLOWED_SENDER_ID = "${TELEGRAM_OWNER_CHAT_ID}"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [bt-sms-cmd-hook] %(levelname)s: %(message)s",
)
log = logging.getLogger()


def load_telegram_env() -> tuple[str | None, str | None]:
    """Return (bot_token, chat_id) from ~/.config/paired-sms-watch/telegram.env."""
    if not TG_ENV_PATH.exists():
        return None, None
    token = chat = None
    try:
        for line in TG_ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k.strip() == "TG_BOT_TOKEN":
                token = v
            elif k.strip() == "TG_CHAT_ID":
                chat = v
    except OSError as e:
        log.error(f"failed to read {TG_ENV_PATH}: {e}")
    return token, chat


def telegram_send(token: str, chat_id: str, text: str,
                  reply_to: int | None = None) -> bool:
    """Send a message via Telegram API. Returns True on success."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            r = json.loads(body)
            return bool(r.get("ok"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError) as e:
        log.error(f"telegram_send failed: {e}")
        return False


def latest_session_path() -> Path | None:
    """Find the most recently modified session JSONL."""
    if not SESSIONS_DIR.exists():
        return None
    candidates = [c for c in SESSIONS_DIR.glob("*.jsonl") if not c.name.endswith(".trajectory.jsonl")]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def normalize_uk(num: str) -> str:
    """Normalize a UK number to digits-only, no leading + or 00. Mirrors trusted list rules."""
    n = num.strip().replace(" ", "").replace("-", "")
    if n.startswith("+44"):
        n = "0" + n[3:]
    elif n.startswith("0044"):
        n = "0" + n[4:]
    elif n.startswith("44") and len(n) == 12:
        n = "0" + n[2:]
    return n


def load_trusted_numbers() -> set[str]:
    """Read trusted-numbers.conf, return set of normalized numbers."""
    s = set()
    if not TRUSTED_NUMBERS_FILE.exists():
        return s
    try:
        for line in TRUSTED_NUMBERS_FILE.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            # trusted file may have trailing comment after the number, already split above
            tok = line.split()[0] if line.split() else ""
            if tok:
                s.add(normalize_uk(tok))
    except OSError as e:
        log.warning(f"failed to read trusted file: {e}")
    return s


def is_trusted(number: str) -> bool:
    return normalize_uk(number) in load_trusted_numbers()


def fire_failsoft_sms(number: str, message: str) -> dict:
    """Send the same message via SMS as a fail-soft for /phone <num> <msg>.
    Hardware/OS block on Samsung Note 9 prevents 3rd-party TTS from mixing into
    active voice calls, so we always back up the spoken message with an SMS.
    Returns {"ok": bool, "info": str}.
    """
    # Cap SMS body to avoid huge multi-segment SMS for long attachments.
    sms_body = message[:300] + ("..." if len(message) > 300 else "")
    try:
        proc = subprocess.run(
            [SMS_SEND_BIN, "--auto-unlock", "--relock", number, sms_body],
            capture_output=True, text=True, timeout=90,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "info": "sms timeout"}
    except OSError as e:
        return {"ok": False, "info": f"sms exec failed: {e}"}
    if proc.returncode != 0:
        return {"ok": False, "info": f"sms rc={proc.returncode} stderr={(proc.stderr or '')[:120]}"}
    return {"ok": True, "info": "sms delivered"}


def parse_message_line(line: str) -> dict | None:
    """Parse a session JSONL line. Returns the message dict if it's a user message
    that matches a command pattern. Otherwise None.

    Returns dict with key "command" being one of: "sms", "phone_dial", "phone_verb".
    """
    try:
        e = json.loads(line)
    except json.JSONDecodeError:
        return None
    msg = e.get("message")
    if not isinstance(msg, dict):
        return None
    if msg.get("role") != "user":
        return None
    content = msg.get("content")
    if not isinstance(content, list):
        return None
    # Concatenate text parts
    full_text = ""
    for c in content:
        if isinstance(c, dict) and "text" in c:
            full_text += c["text"] + "\n"

    # Common metadata
    mid_match = re.search(r'"message_id":\s*"?(\d+)"?', full_text)
    sender_match = re.search(r'"sender_id":\s*"?(\d+)"?', full_text)
    base = {
        "session_event_id": e.get("id"),
        "session_event_ts": e.get("timestamp"),
        "telegram_message_id": int(mid_match.group(1)) if mid_match else None,
        "sender_id": sender_match.group(1) if sender_match else None,
    }

    # Try /sms first
    sms_match = SMS_PATTERN.search(full_text)
    if sms_match:
        return {
            **base,
            "command": "sms",
            "number": sms_match.group(1).strip(),
            "body": sms_match.group(2).strip(),
        }

    # Then /phone <num> attach <path>  (TRUSTED only)
    attach_match = PHONE_ATTACH_PATTERN.search(full_text)
    if attach_match:
        return {
            **base,
            "command": "phone_attach",
            "number": attach_match.group(1).strip(),
            "attach_path": attach_match.group(2).strip(),
        }

    # Then /phone <verb>  (must precede the say/dial patterns since they\'d also match)
    verb_match = PHONE_VERB_PATTERN.search(full_text)
    if verb_match:
        return {
            **base,
            "command": "phone_verb",
            "verb": verb_match.group(1).strip().lower(),
        }

    # Then /phone <num> <message>  (TRUSTED only) - must precede dial-only
    say_match = PHONE_SAY_PATTERN.search(full_text)
    if say_match:
        candidate_msg = say_match.group(2).strip()
        # If the "message" is a single token that looks like a verb only, fall through
        if candidate_msg and not candidate_msg.lower() in ("hangup", "status", "end"):
            return {
                **base,
                "command": "phone_say",
                "number": say_match.group(1).strip(),
                "message": candidate_msg,
            }

    # Then /phone <number>
    dial_match = PHONE_DIAL_PATTERN.search(full_text)
    if dial_match:
        return {
            **base,
            "command": "phone_dial",
            "number": dial_match.group(1).strip(),
        }

    return None


def append_dispatch_log(record: dict) -> None:
    try:
        DISPATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DISPATCH_LOG.open("a") as f:
            f.write(json.dumps(record) + "\n")
    except OSError as e:
        log.warning(f"dispatch log write failed: {e}")


def dispatch_sms(parsed: dict, token: str, chat_id: str) -> dict:
    """Run paired-sms-send and reply via Telegram. Returns full record."""
    record = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        **parsed,
        "result": None,
        "telegram_replied": False,
    }
    if parsed.get("sender_id") != ALLOWED_SENDER_ID:
        log.warning(
            f"REJECTED /sms from sender_id={parsed.get('sender_id')} "
            f"(only {ALLOWED_SENDER_ID} is allowed)")
        record["result"] = {"ok": False, "error": "sender_not_allowed"}
        append_dispatch_log(record)
        return record

    log.info(f"DISPATCH /sms: number={parsed['number']} body={parsed['body'][:60]!r}")
    try:
        p = subprocess.run(
            [SMS_SEND_BIN, parsed["number"], parsed["body"], "--json", "--auto-unlock", "--relock"],
            capture_output=True, text=True, timeout=45,
        )
        try:
            result = json.loads(p.stdout) if p.stdout.strip() else {"ok": False, "error": "no_output"}
        except json.JSONDecodeError:
            result = {"ok": False, "error": "json_decode_error", "raw_stdout": p.stdout[:300]}
        if p.returncode != 0:
            result.setdefault("exit_code", p.returncode)
            result.setdefault("stderr", p.stderr.strip()[:200])
    except subprocess.TimeoutExpired:
        result = {"ok": False, "error": "timeout"}
    except OSError as e:
        result = {"ok": False, "error": f"exec_failed: {e}"}

    record["result"] = result

    if result.get("ok"):
        reply = (f"✅ SMS sent to {parsed['number']}\n"
                 f"Body: {parsed['body'][:120]}")
    else:
        err = result.get("error", "unknown")
        msg = result.get("message", "")
        if err == "keyguard_locked":
            reply = ("❌ Phone is locked.\n"
                     "Unlock the phone (enter PIN) and try again.")
        elif err == "compose_did_not_appear":
            reply = ("❌ Messages app didn't open in time. "
                     "Try unlocking the phone first.")
        elif err == "send_button_not_found":
            reply = ("❌ Couldn't find Send button on phone screen. "
                     "Phone may be locked or in an unexpected state.")
        elif err == "verification_failed":
            reply = (f"⚠️ Send tap fired but message not yet in sent folder. "
                     f"Check phone manually for {parsed['number']}.")
        else:
            reply = f"❌ SMS failed: {err}\n{msg[:120]}"

    sent = telegram_send(
        token, chat_id, reply,
        reply_to=parsed.get("telegram_message_id"),
    )
    record["telegram_replied"] = sent
    if not sent:
        log.error("Failed to send Telegram reply for /sms")

    append_dispatch_log(record)
    return record


def dispatch_phone(parsed: dict, token: str, chat_id: str) -> dict:
    """Run paired-call (dial/hangup/status) and reply via Telegram."""
    record = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        **parsed,
        "result": None,
        "telegram_replied": False,
    }
    if parsed.get("sender_id") != ALLOWED_SENDER_ID:
        sender = parsed.get("sender_id")
        log.warning(
            f"REJECTED /phone from sender_id={sender} "
            f"(only {ALLOWED_SENDER_ID} is allowed)")
        record["result"] = {"ok": False, "error": "sender_not_allowed"}
        append_dispatch_log(record)
        return record

    cmd_type = parsed.get("command")
    success_reply = None

    if cmd_type == "phone_dial":
        number = parsed["number"]
        log.info(f"DISPATCH /phone dial: {number}")
        argv = [PHONE_BIN, "dial", number, "--json"]
        timeout = 30
        success_reply = (
            f"📞 Calling {number}\n"
            f"The phone is ringing now. Pick it up to talk."
        )
    elif cmd_type == "phone_verb":
        verb = parsed["verb"]
        if verb in ("hangup", "end"):
            log.info("DISPATCH /phone hangup")
            argv = [PHONE_BIN, "hangup", "--json"]
            timeout = 15
            success_reply = "📞 Hung up"
        elif verb == "status":
            log.info("DISPATCH /phone status")
            argv = [PHONE_BIN, "status", "--json"]
            timeout = 10
        else:
            record["result"] = {"ok": False, "error": f"unknown_verb: {verb}"}
            append_dispatch_log(record)
            return record
    elif cmd_type == "phone_say":
        number = parsed["number"]
        message = parsed["message"]
        if not is_trusted(number):
            log.warning(f"REJECTED /phone say to UNTRUSTED number {number}")
            record["result"] = {"ok": False, "error": "recipient_not_trusted"}
            reply = (
                f"🔒 /phone {number} <message> requires a TRUSTED recipient.\n"
                f"Add via: paired-trusted add {number}\n"
                f"For non-trusted: use /sms {number} ..."
            )
            sent = telegram_send(token, chat_id, reply, reply_to=parsed.get("telegram_message_id"))
            record["telegram_replied"] = sent
            append_dispatch_log(record)
            return record
        if len(message) > MAX_TTS_CHARS:
            log.warning(f"Message too long ({len(message)} > {MAX_TTS_CHARS}); truncating")
            message = message[:MAX_TTS_CHARS] + "..."
        log.info(f"DISPATCH /phone say: number={number} msg={message[:60]!r}")
        argv = [SPEAK_BIN, number, message, "--json"]
        timeout = 60
        success_reply = (
            f"📞🗣 Calling {number} and speaking message:\n"
            f"  \"{message[:120]}\""
        )
    elif cmd_type == "phone_attach":
        number = parsed["number"]
        attach_path = parsed["attach_path"]
        if not is_trusted(number):
            log.warning(f"REJECTED /phone attach to UNTRUSTED number {number}")
            reply = (
                f"🔒 /phone {number} attach requires a TRUSTED recipient.\n"
                f"Add via: paired-trusted add {number}"
            )
            sent = telegram_send(token, chat_id, reply, reply_to=parsed.get("telegram_message_id"))
            record["result"] = {"ok": False, "error": "recipient_not_trusted"}
            record["telegram_replied"] = sent
            append_dispatch_log(record)
            return record
        # Validate attach path exists, is a file, and is readable
        try:
            ap = Path(attach_path)
            if not ap.is_file():
                raise FileNotFoundError(f"not a file: {attach_path}")
            content = ap.read_text(encoding="utf-8", errors="replace").strip()
        except Exception as e:
            log.error(f"attach read failed: {e}")
            reply = f"❌ Cannot read attachment: {e}"
            sent = telegram_send(token, chat_id, reply, reply_to=parsed.get("telegram_message_id"))
            record["result"] = {"ok": False, "error": f"attach_read_failed: {e}"}
            record["telegram_replied"] = sent
            append_dispatch_log(record)
            return record
        if not content:
            reply = "❌ Attachment is empty"
            sent = telegram_send(token, chat_id, reply, reply_to=parsed.get("telegram_message_id"))
            record["result"] = {"ok": False, "error": "attach_empty"}
            record["telegram_replied"] = sent
            append_dispatch_log(record)
            return record
        if len(content) > MAX_TTS_CHARS:
            log.info(f"Attachment {ap.name} is {len(content)} chars; truncating to {MAX_TTS_CHARS}")
            content = content[:MAX_TTS_CHARS] + "..."
        log.info(f"DISPATCH /phone attach: number={number} file={ap.name} ({len(content)} chars)")
        argv = [SPEAK_BIN, number, content, "--json"]
        timeout = 60
        success_reply = (
            f"📞📎 Calling {number} and speaking content of {ap.name} "
            f"({len(content)} chars)"
        )
    else:
        record["result"] = {"ok": False, "error": "unknown_phone_command"}
        append_dispatch_log(record)
        return record

    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        try:
            result = json.loads(proc.stdout) if proc.stdout.strip() else {"ok": False, "error": "no_output"}
        except json.JSONDecodeError:
            result = {"ok": False, "error": "json_decode_error", "raw_stdout": proc.stdout[:300]}
        if proc.returncode != 0:
            result.setdefault("exit_code", proc.returncode)
            result.setdefault("stderr", proc.stderr.strip()[:200])
    except subprocess.TimeoutExpired:
        result = {"ok": False, "error": "timeout"}
    except OSError as ex:
        result = {"ok": False, "error": f"exec_failed: {ex}"}

    record["result"] = result

    # Fail-soft: for /phone <num> <msg> and /phone <num> attach, the call+TTS may
    # silently fail on Samsung Note 9 due to AUDIOFOCUS_LOCK held by Telecom during
    # MODE_IN_CALL. Always back up with SMS so the recipient is guaranteed to
    # receive the message, even if they never hear it spoken.
    sms_failsoft_result = None
    if cmd_type in ("phone_say", "phone_attach"):
        # Determine the message that was supposed to be spoken
        if cmd_type == "phone_say":
            sms_msg = parsed["message"]
        else:
            # For attach, re-derive the content from the file (already validated above)
            try:
                sms_msg = Path(parsed["attach_path"]).read_text(encoding="utf-8", errors="replace").strip()
            except Exception:
                sms_msg = f"[Attachment: {parsed['attach_path']}]"
        log.info(f"FAIL-SOFT: firing SMS to {parsed['number']} (msg {len(sms_msg)} chars)")
        sms_failsoft_result = fire_failsoft_sms(parsed["number"], sms_msg)
        record["sms_failsoft"] = sms_failsoft_result
        log.info(f"FAIL-SOFT SMS: ok={sms_failsoft_result.get('ok')} info={sms_failsoft_result.get('info')}")

    if result.get("ok"):
        if cmd_type == "phone_verb" and parsed.get("verb") == "status":
            parsed_status = result.get("parsed", {})
            calls = parsed_status.get("calls") or []
            modem = parsed_status.get("modem", "?")
            if not calls:
                reply = f"📞 No active calls.\nModem: {modem}"
            else:
                lines = ["📞 Active calls:"]
                for c in calls:
                    lines.append(f"  - {c}")
                reply = "\n".join(lines)
        else:
            reply = success_reply or "✅ Done"
            # Annotate phone_say / phone_attach replies with the SMS fail-soft result
            if cmd_type in ("phone_say", "phone_attach") and sms_failsoft_result is not None:
                if sms_failsoft_result.get("ok"):
                    reply += "\n📨 SMS fail-soft: delivered (guaranteed receipt; speech may be silent due to Samsung audio policy)"
                else:
                    reply += f"\n⚠️ SMS fail-soft FAILED: {sms_failsoft_result.get('info', 'unknown')}"
    else:
        err = result.get("error", "unknown")
        action = cmd_type.replace("phone_", "")
        if cmd_type == "phone_verb":
            action = parsed.get("verb", "?")
        reply = f"❌ /phone {action} failed: {err}"
        if result.get("stderr"):
            reply += f"\n{result['stderr'][:120]}"

    sent = telegram_send(token, chat_id, reply, reply_to=parsed.get("telegram_message_id"))
    record["telegram_replied"] = sent
    if not sent:
        log.error("Failed to send Telegram reply for /phone")

    append_dispatch_log(record)
    return record


def cmd_status() -> int:
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if Path(f"/proc/{pid}").is_dir():
                print(f"paired-sms-command-hook is running (pid {pid})")
            else:
                print(f"pid file exists ({pid}) but process gone (stale)")
        except (OSError, ValueError):
            print("pid file unreadable")
    else:
        print("paired-sms-command-hook is NOT running")
    if DISPATCH_LOG.exists():
        try:
            lines = DISPATCH_LOG.read_text().splitlines()
            print(f"\nDispatch log: {DISPATCH_LOG} ({len(lines)} dispatches)")
            for ln in lines[-3:]:
                try:
                    r = json.loads(ln)
                    res = r.get("result", {})
                    cmd = r.get("command", "sms")
                    target = r.get("number") or r.get("verb", "?")
                    print(f"  {r.get('received_at','?')[:19]}  "
                          f"{cmd:11} -> {target}  "
                          f"ok={res.get('ok')}  err={res.get('error','-')}")
                except json.JSONDecodeError:
                    pass
        except OSError:
            pass
    return 0


def cmd_watch() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))
    except OSError:
        pass

    fh = logging.FileHandler(HOOK_LOG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [bt-sms-cmd-hook] %(levelname)s: %(message)s"))
    log.addHandler(fh)

    token, chat_id = load_telegram_env()
    if not token or not chat_id:
        log.error(f"Missing TG_BOT_TOKEN or TG_CHAT_ID in {TG_ENV_PATH}")
        return 1
    log.info(f"Hook started. Watching {SESSIONS_DIR}")
    log.info(f"Allowed sender: {ALLOWED_SENDER_ID}")
    log.info("Recognized commands: /sms <num> <body>, /phone <num>, /phone <num> <msg> [trusted+SMS-failsoft], /phone <num> attach <path> [trusted+SMS-failsoft], /phone hangup, /phone status")

    stop = {"flag": False}

    def shutdown(signum, frame):
        log.info(f"Caught signal {signum}, shutting down")
        stop["flag"] = True
        try:
            PID_FILE.unlink(missing_ok=True)
        except OSError:
            pass

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    current_session: Path | None = None
    last_offset = 0
    seen_event_ids: set[str] = set()

    while not stop["flag"]:
        try:
            session = latest_session_path()
            if session is None:
                time.sleep(2)
                continue
            if session != current_session:
                current_session = session
                last_offset = session.stat().st_size
                log.info(f"Tracking session: {session.name} from offset {last_offset}")

            try:
                size = session.stat().st_size
            except OSError:
                time.sleep(1)
                continue
            if size > last_offset:
                with session.open("rb") as f:
                    f.seek(last_offset)
                    chunk = f.read()
                    last_offset = f.tell()
                text = chunk.decode("utf-8", errors="replace")
                for line in text.splitlines():
                    if not line.strip():
                        continue
                    parsed = parse_message_line(line)
                    if parsed is None:
                        continue
                    eid = parsed.get("session_event_id")
                    if eid and eid in seen_event_ids:
                        continue
                    if eid:
                        seen_event_ids.add(eid)
                    if len(seen_event_ids) > 500:
                        seen_event_ids = set(list(seen_event_ids)[-200:])

                    cmd_type = parsed.get("command", "sms")
                    log.info(f"Found /{cmd_type} event: msg_id={parsed.get('telegram_message_id')}")
                    if cmd_type == "sms":
                        dispatch_sms(parsed, token, chat_id)
                    elif cmd_type in ("phone_dial", "phone_verb", "phone_say", "phone_attach"):
                        dispatch_phone(parsed, token, chat_id)
                    else:
                        log.warning(f"Unknown command type: {cmd_type}")
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.exception(f"watch loop error: {e}")
            time.sleep(5)

    try:
        PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass
    log.info("Exited.")
    return 0


def main():
    p = argparse.ArgumentParser(
        description="DEPRECATED legacy /sms /phone hook. Use paired-inbox-hook instead.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--watch", action="store_true", help="Foreground daemon")
    g.add_argument("--status", action="store_true")
    p.add_argument("--legacy-jsonl-source", action="store_true",
                   help="Required to run the deprecated JSONL-tail mode")
    p.add_argument("--i-understand-the-risks", action="store_true",
                   help="Acknowledge the prompt-injection risk of session-log dispatch")
    args = p.parse_args()

    if args.status:
        return cmd_status()

    # Refuse --watch unless both opt-in flags supplied.
    if not (args.legacy_jsonl_source and args.i_understand_the_risks):
        sys.stderr.write(
            "\nREFUSING TO RUN. This script is deprecated as of v1.0.2.\n"
            "Reason: dispatching commands from the agent session JSONL is a\n"
            "prompt-injection surface (session contents are not trusted input).\n"
            "\n"
            "Use the replacement instead:\n"
            "  paired-inbox-hook --keygen      # one-time, generates HMAC key\n"
            "  paired-inbox-hook --watch       # daemon (signed inbox source)\n"
            "\n"
            "If you really need the legacy behaviour, pass:\n"
            "  --legacy-jsonl-source --i-understand-the-risks\n"
            "\n")
        return 2

    log.warning("Running legacy JSONL-source mode. This is deprecated and unsafe.")
    log.warning("Migrate to paired-inbox-hook as soon as possible.")
    return cmd_watch()


if __name__ == "__main__":
    sys.exit(main())
