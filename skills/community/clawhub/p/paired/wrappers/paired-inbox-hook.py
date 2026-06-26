#!/usr/bin/env python3
"""paired-inbox-hook — Signed-inbox /sms and /phone command dispatcher.

This is the v1.0.2 replacement for paired-sms-command-hook. It addresses the
"Memory and Context Poisoning" finding from the OpenClaw safety scanner by
moving the dispatch surface OFF the agent's session JSONL and ONTO a
dedicated inbox directory that only the user (or a trusted bot relay) can
write to.

Design:
  1. The daemon watches ~/.openclaw/paired/inbox/ for new files
  2. Each file is a JSON object with a separate HMAC signature
  3. The signature key lives at ~/.config/paired/inbox.key (mode 0600)
  4. Only commands with a valid signature are dispatched
  5. After dispatch (success or fail), the file is moved to ./processed/
  6. NOTHING from the agent session log is parsed or trusted as a command

Inbox file format (filename: <ulid-or-timestamp>.json):
  {
    "ts": "2026-04-30T20:30:00Z",       // ISO 8601 UTC, must be within ±5min of now
    "nonce": "<random 16+ chars>",       // for replay protection (recent set tracked)
    "command": "sms" | "phone_dial" | "phone_say" | "phone_attach" | "phone_verb",
    "number": "+447xxx...",              // for sms/phone_*
    "body": "...",                       // for sms
    "message": "...",                    // for phone_say
    "attach_path": "...",                // for phone_attach
    "verb": "hangup|status|end",         // for phone_verb
    "with_sms_fallback": false,          // OPT-IN for phone_say only
    "reply_chat_id": "...",              // optional — where to send Telegram reply
    "reply_message_id": 1234             // optional — for thread reply
  }
  (separate sidecar file <name>.sig with hex-encoded HMAC-SHA256 of the .json)

Usage:
  paired-inbox-hook --watch                # foreground daemon
  paired-inbox-hook --status               # daemon state + recent dispatches
  paired-inbox-hook --keygen               # generate inbox.key (one-time setup)
  paired-inbox-hook --put <command-json>   # sign and put a command in the inbox

Logs to ~/.paired/inbox-hook.log
Records dispatches in ~/.paired/inbox-hook.jsonl
"""
from __future__ import annotations
import argparse
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import urllib.error
import urllib.parse
import urllib.request

_HOME = Path.home()
INBOX_DIR = _HOME / ".openclaw" / "paired" / "inbox"
INBOX_PROCESSED = INBOX_DIR / "processed"
INBOX_REJECTED = INBOX_DIR / "rejected"
KEY_PATH = _HOME / ".config" / "paired" / "inbox.key"
LOG_DIR = _HOME / ".paired"
HOOK_LOG = LOG_DIR / "inbox-hook.log"
DISPATCH_LOG = LOG_DIR / "inbox-hook.jsonl"
NONCE_DB = LOG_DIR / "inbox-nonces.txt"
PID_FILE = Path(f"/run/user/{os.getuid()}/paired-inbox-hook.pid")
TG_ENV_PATH = _HOME / ".config" / "paired-sms-watch" / "telegram.env"
SMS_SEND_BIN = str(_HOME / "bin" / "paired-sms-send")
PHONE_BIN = str(_HOME / "bin" / "paired-call")
SPEAK_BIN = str(_HOME / "bin" / "paired-call-and-speak")
TRUSTED_NUMBERS_FILE = _HOME / ".config" / "paired" / "trusted-numbers.conf"
MAX_TTS_CHARS = 1500
MAX_CLOCK_SKEW = timedelta(minutes=5)
NONCE_HORIZON = 1000  # remember last N nonces for replay protection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [paired-inbox-hook] %(levelname)s: %(message)s",
)
log = logging.getLogger()


# --- Crypto / signature ---------------------------------------------------

def load_key() -> bytes:
    if not KEY_PATH.exists():
        log.error(f"inbox key missing: {KEY_PATH}")
        log.error("run 'paired-inbox-hook --keygen' to create one")
        sys.exit(2)
    if KEY_PATH.stat().st_mode & 0o077:
        log.error(f"inbox key {KEY_PATH} has overly-permissive mode "
                  f"{oct(KEY_PATH.stat().st_mode)}; expected 0600")
        sys.exit(2)
    return KEY_PATH.read_bytes().strip()


def sign(payload: bytes, key: bytes) -> str:
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify(payload: bytes, key: bytes, signature: str) -> bool:
    expected = sign(payload, key)
    return hmac.compare_digest(expected, signature.strip().lower())


def keygen() -> int:
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if KEY_PATH.exists():
        log.error(f"refusing to overwrite existing key {KEY_PATH}")
        return 1
    KEY_PATH.write_bytes(secrets.token_hex(32).encode())
    KEY_PATH.chmod(0o600)
    log.info(f"created {KEY_PATH} (mode 0600). Keep it secret.")
    print(f"Inbox HMAC key created at {KEY_PATH}")
    print("To use: any process that signs commands (e.g. your Telegram relay)")
    print("must read this file and HMAC-SHA256 each command JSON before")
    print("dropping it in the inbox.")
    return 0


# --- Nonce tracking (replay protection) ----------------------------------

def load_nonces() -> set[str]:
    if not NONCE_DB.exists():
        return set()
    try:
        return set(NONCE_DB.read_text().splitlines())
    except OSError:
        return set()


def remember_nonce(nonce: str, recent: set[str]) -> None:
    recent.add(nonce)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Trim
    if len(recent) > NONCE_HORIZON:
        # Keep most recent N — without timestamps, just sample
        keep = list(recent)[-NONCE_HORIZON:]
        NONCE_DB.write_text("\n".join(keep) + "\n")
    else:
        with NONCE_DB.open("a") as f:
            f.write(nonce + "\n")


# --- Telegram replies (optional) -----------------------------------------

def load_telegram_env() -> tuple[str | None, str | None]:
    if not TG_ENV_PATH.exists():
        return None, None
    token = chat = None
    try:
        for line in TG_ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
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
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            r = json.loads(resp.read().decode("utf-8"))
            return bool(r.get("ok"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError,
            json.JSONDecodeError) as e:
        log.error(f"telegram_send failed: {e}")
        return False


# --- Trust gating ---------------------------------------------------------

def normalize_uk(num: str) -> str:
    n = num.strip().replace(" ", "").replace("-", "")
    if n.startswith("+44"):
        n = "0" + n[3:]
    elif n.startswith("0044"):
        n = "0" + n[4:]
    elif n.startswith("44") and len(n) == 12:
        n = "0" + n[2:]
    return n


def load_trusted_numbers() -> set[str]:
    s = set()
    if not TRUSTED_NUMBERS_FILE.exists():
        return s
    try:
        for line in TRUSTED_NUMBERS_FILE.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            tok = line.split()[0] if line.split() else ""
            if tok:
                s.add(normalize_uk(tok))
    except OSError as e:
        log.warning(f"failed to read trusted file: {e}")
    return s


def is_trusted(number: str) -> bool:
    return normalize_uk(number) in load_trusted_numbers()


# --- Dispatch -------------------------------------------------------------

def dispatch_sms(cmd: dict) -> dict:
    if not is_trusted(cmd["number"]) and not cmd.get("confirmed"):
        return {"ok": False, "error": "number_not_trusted",
                "hint": "add to ~/.config/paired/trusted-numbers.conf, "
                        "or set 'confirmed': true in the command"}
    log.info(f"DISPATCH /sms: number={cmd['number']} "
             f"body={cmd.get('body', '')[:60]!r}")
    try:
        p = subprocess.run(
            [SMS_SEND_BIN, cmd["number"], cmd.get("body", ""), "--json",
             "--auto-unlock", "--relock"],
            capture_output=True, text=True, timeout=45,
        )
        try:
            return json.loads(p.stdout) if p.stdout.strip() else \
                {"ok": False, "error": "no_output"}
        except json.JSONDecodeError:
            return {"ok": False, "error": "json_decode_error"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}


def dispatch_phone_dial(cmd: dict) -> dict:
    if not is_trusted(cmd["number"]) and not cmd.get("confirmed"):
        return {"ok": False, "error": "number_not_trusted"}
    log.info(f"DISPATCH /phone dial: number={cmd['number']}")
    try:
        p = subprocess.run(
            [PHONE_BIN, "dial", cmd["number"], "--json"],
            capture_output=True, text=True, timeout=30,
        )
        try:
            return json.loads(p.stdout) if p.stdout.strip() else \
                {"ok": False, "error": "no_output"}
        except json.JSONDecodeError:
            return {"ok": False, "error": "json_decode_error"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}


def dispatch_phone_say(cmd: dict) -> dict:
    if not is_trusted(cmd["number"]):
        return {"ok": False, "error": "number_not_trusted"}
    msg = cmd.get("message", "")[:MAX_TTS_CHARS]
    fallback = bool(cmd.get("with_sms_fallback", False))  # OPT-IN
    log.info(f"DISPATCH /phone say: number={cmd['number']} "
             f"msg={msg[:60]!r} fallback={fallback}")
    args = [SPEAK_BIN, cmd["number"], msg]
    if fallback:
        args.append("--with-sms-fallback")
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=120)
        try:
            return json.loads(p.stdout) if p.stdout.strip() else \
                {"ok": p.returncode == 0,
                 "output": p.stdout[:200], "stderr": p.stderr[:200]}
        except json.JSONDecodeError:
            return {"ok": p.returncode == 0,
                    "output": p.stdout[:200], "stderr": p.stderr[:200]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}


def dispatch_phone_verb(cmd: dict) -> dict:
    verb = cmd.get("verb", "").lower()
    if verb in ("hangup", "end"):
        sub = "hangup"
    elif verb == "status":
        sub = "status"
    else:
        return {"ok": False, "error": f"unknown_verb: {verb}"}
    log.info(f"DISPATCH /phone {sub}")
    try:
        p = subprocess.run(
            [PHONE_BIN, sub, "--json"],
            capture_output=True, text=True, timeout=15,
        )
        try:
            return json.loads(p.stdout) if p.stdout.strip() else \
                {"ok": True}
        except json.JSONDecodeError:
            return {"ok": True, "output": p.stdout[:200]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}


DISPATCHERS = {
    "sms": dispatch_sms,
    "phone_dial": dispatch_phone_dial,
    "phone_say": dispatch_phone_say,
    "phone_verb": dispatch_phone_verb,
}


# --- Inbox processing -----------------------------------------------------

def append_dispatch_log(record: dict) -> None:
    try:
        DISPATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DISPATCH_LOG.open("a") as f:
            f.write(json.dumps(record) + "\n")
    except OSError as e:
        log.warning(f"dispatch log write failed: {e}")


def process_inbox_file(json_path: Path, key: bytes,
                       recent_nonces: set[str]) -> None:
    sig_path = json_path.with_suffix(json_path.suffix + ".sig")
    if not sig_path.exists():
        log.warning(f"reject {json_path.name}: missing .sig sidecar")
        json_path.replace(INBOX_REJECTED / json_path.name)
        return

    raw = json_path.read_bytes()
    sigtxt = sig_path.read_text().strip()

    if not verify(raw, key, sigtxt):
        log.warning(f"reject {json_path.name}: signature mismatch")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return

    try:
        cmd = json.loads(raw)
    except json.JSONDecodeError as e:
        log.warning(f"reject {json_path.name}: invalid JSON ({e})")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return

    # Clock skew check
    try:
        ts = datetime.fromisoformat(cmd["ts"].replace("Z", "+00:00"))
        if abs(datetime.now(timezone.utc) - ts) > MAX_CLOCK_SKEW:
            log.warning(f"reject {json_path.name}: stale timestamp {cmd['ts']}")
            json_path.replace(INBOX_REJECTED / json_path.name)
            sig_path.replace(INBOX_REJECTED / sig_path.name)
            return
    except (KeyError, ValueError) as e:
        log.warning(f"reject {json_path.name}: bad ts ({e})")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return

    # Nonce / replay check
    nonce = cmd.get("nonce", "")
    if not nonce or len(nonce) < 16:
        log.warning(f"reject {json_path.name}: missing/short nonce")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return
    if nonce in recent_nonces:
        log.warning(f"reject {json_path.name}: replay (nonce already used)")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return
    remember_nonce(nonce, recent_nonces)

    # Dispatch
    cmd_type = cmd.get("command")
    fn = DISPATCHERS.get(cmd_type)
    if not fn:
        log.warning(f"reject {json_path.name}: unknown command {cmd_type!r}")
        json_path.replace(INBOX_REJECTED / json_path.name)
        sig_path.replace(INBOX_REJECTED / sig_path.name)
        return

    result = fn(cmd)
    record = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "filename": json_path.name,
        "command": cmd_type,
        "number": cmd.get("number"),
        "result": result,
    }
    append_dispatch_log(record)

    # Optional Telegram reply
    reply_chat = cmd.get("reply_chat_id")
    reply_to = cmd.get("reply_message_id")
    if reply_chat:
        token, _ = load_telegram_env()
        if token:
            ok = bool(result.get("ok"))
            text = ("✅ " if ok else "❌ ") + json.dumps(result)[:300]
            telegram_send(token, str(reply_chat), text, reply_to)

    # Move to processed
    json_path.replace(INBOX_PROCESSED / json_path.name)
    sig_path.replace(INBOX_PROCESSED / sig_path.name)


def watch_inbox() -> int:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    INBOX_PROCESSED.mkdir(parents=True, exist_ok=True)
    INBOX_REJECTED.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    key = load_key()
    recent_nonces = load_nonces()

    log.info(f"watching {INBOX_DIR}")
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))

    stop = False

    def _shutdown(*_a):
        nonlocal stop
        stop = True
        log.info("shutting down")

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    try:
        while not stop:
            for p in sorted(INBOX_DIR.glob("*.json")):
                if not p.is_file():
                    continue
                if p.parent != INBOX_DIR:  # skip processed/, rejected/
                    continue
                try:
                    process_inbox_file(p, key, recent_nonces)
                except Exception:
                    log.exception(f"failure processing {p}")
                    try:
                        p.replace(INBOX_REJECTED / p.name)
                    except OSError:
                        pass
            time.sleep(0.5)
    finally:
        try:
            PID_FILE.unlink()
        except OSError:
            pass
    return 0


# --- CLI: --put helper ---------------------------------------------------

def put_command(payload_str: str) -> int:
    """Sign a command JSON and drop it in the inbox. Used by the Telegram
    relay or by the user manually for testing."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    key = load_key()

    try:
        cmd = json.loads(payload_str)
    except json.JSONDecodeError as e:
        log.error(f"invalid JSON: {e}")
        return 2

    # Auto-fill missing ts/nonce so callers can be lazy
    cmd.setdefault("ts", datetime.now(timezone.utc).isoformat()
                   .replace("+00:00", "Z"))
    cmd.setdefault("nonce", secrets.token_hex(16))

    raw = json.dumps(cmd, separators=(",", ":")).encode("utf-8")
    sig = sign(raw, key)

    fname = f"{int(time.time() * 1000)}-{secrets.token_hex(4)}.json"
    json_path = INBOX_DIR / fname
    sig_path = INBOX_DIR / (fname + ".sig")

    json_path.write_bytes(raw)
    sig_path.write_text(sig + "\n")
    log.info(f"queued {json_path.name}")
    print(json_path.name)
    return 0


def show_status() -> int:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    INBOX_PROCESSED.mkdir(parents=True, exist_ok=True)
    INBOX_REJECTED.mkdir(parents=True, exist_ok=True)
    pid_alive = False
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            pid_alive = True
        except (OSError, ValueError):
            pid_alive = False
    pending = len(list(INBOX_DIR.glob("*.json"))) - \
              len(list(INBOX_PROCESSED.glob("*.json"))) - \
              len(list(INBOX_REJECTED.glob("*.json")))
    print(f"daemon running:    {pid_alive}")
    print(f"pid file:          {PID_FILE}")
    print(f"inbox dir:         {INBOX_DIR}")
    print(f"pending:           {max(0, pending)}")
    print(f"processed (total): {len(list(INBOX_PROCESSED.glob('*.json')))}")
    print(f"rejected (total):  {len(list(INBOX_REJECTED.glob('*.json')))}")
    print(f"key present:       {KEY_PATH.exists()}")
    if KEY_PATH.exists():
        mode = oct(KEY_PATH.stat().st_mode)[-3:]
        print(f"key mode:          {mode} (must be 600)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Signed-inbox /sms /phone command dispatcher")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--watch", action="store_true",
                   help="run inbox watcher in foreground")
    g.add_argument("--status", action="store_true",
                   help="show daemon and inbox state")
    g.add_argument("--keygen", action="store_true",
                   help="generate ~/.config/paired/inbox.key (one-time)")
    g.add_argument("--put", metavar="JSON",
                   help="sign and queue a command JSON in the inbox")
    args = ap.parse_args()

    if args.keygen:
        return keygen()
    if args.status:
        return show_status()
    if args.put:
        return put_command(args.put)
    if args.watch:
        return watch_inbox()
    return 1


if __name__ == "__main__":
    sys.exit(main())
