#!/usr/bin/env python3
"""Send Telegram notifications for pet reminders using env/config resolution."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR.parent / "config.json"


def ts() -> str:
    return datetime.utcnow().isoformat()


def read_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def deep_find_bot_token(value):
    if isinstance(value, dict):
        token = value.get("botToken")
        if isinstance(token, str) and token.strip():
            return token.strip()
        for child in value.values():
            hit = deep_find_bot_token(child)
            if hit:
                return hit
    elif isinstance(value, list):
        for child in value:
            hit = deep_find_bot_token(child)
            if hit:
                return hit
    return ""


def resolve_config() -> dict:
    cfg_path = Path(os.environ.get("PET_ME_CONFIG_FILE", str(DEFAULT_CONFIG))).expanduser()
    return read_json(cfg_path)


def resolve_chat_id(config: dict, cli_chat_id: str | None) -> str:
    if cli_chat_id:
        return cli_chat_id
    return (
        os.environ.get("PET_ME_TELEGRAM_CHAT_ID", "")
        or os.environ.get("TELEGRAM_CHAT_ID", "")
        or str(config.get("reminder", {}).get("telegramChatId", ""))
        or str(config.get("telegramChatId", ""))
    )


def resolve_bot_token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if token:
        return token

    try:
        out = subprocess.check_output(
            ["systemctl", "--user", "show-environment"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        for line in out.splitlines():
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass

    openclaw = read_json(Path.home() / ".openclaw" / "openclaw.json")
    return deep_find_bot_token(openclaw)


def send_via_api(bot_token: str, chat_id: str, message: str) -> bool:
    payload = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": "true",
            "disable_notification": "false",
        }
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        req = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:  # nosec B310
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        if data.get("ok") is True:
            print(f"[{ts()}] ✅ Sent via Telegram API")
            return True
        print(f"[{ts()}] ⚠️ Telegram API error: {data}")
        return False
    except Exception as exc:
        print(f"[{ts()}] ⚠️ Telegram API send failed: {exc}")
        return False


def send_via_telegram_send(message: str) -> bool:
    try:
        result = subprocess.run(
            ["telegram-send", "--format", "markdown", message],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode == 0:
            print(f"[{ts()}] ✅ Sent via telegram-send")
            return True
        print(f"[{ts()}] ⚠️ telegram-send failed: {result.stderr.strip()}")
    except FileNotFoundError:
        print(f"[{ts()}] telegram-send not installed")
    except Exception as exc:
        print(f"[{ts()}] ⚠️ telegram-send error: {exc}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Send pet-me-master Telegram notification")
    parser.add_argument("message", help="Message text")
    parser.add_argument("--chat-id", dest="chat_id", help="Optional explicit Telegram chat ID")
    args = parser.parse_args()

    config = resolve_config()
    chat_id = resolve_chat_id(config, args.chat_id)
    bot_token = resolve_bot_token()

    if not chat_id:
        print(
            "ERROR: Telegram chat ID missing. Set PET_ME_TELEGRAM_CHAT_ID/TELEGRAM_CHAT_ID or config reminder.telegramChatId.",
            file=sys.stderr,
        )
        return 1

    print(f"[{ts()}] Attempting notification to chat {chat_id}...")

    if bot_token and send_via_api(bot_token, chat_id, args.message):
        return 0

    if send_via_telegram_send(args.message):
        return 0

    print(f"[{ts()}] ❌ All notification methods failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
