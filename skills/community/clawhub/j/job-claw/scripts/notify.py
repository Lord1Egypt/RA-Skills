#!/usr/bin/env python3
"""
JobClaw Notifier

Sends job search summary notifications.

Supports:
  - OpenClaw (openclaw message send) — if running inside OpenClaw
  - Telegram Bot API (direct HTTP)
  - Print to stdout (fallback)

Usage:
    from notify import send_summary
    send_summary(config, stats, coding_added, noncoding_added, top_coding, top_noncoding)
"""

import json
import os
import subprocess
import urllib.request
import urllib.parse
from datetime import date
from pathlib import Path


def send_summary(
    config: dict,
    total_jobs: int,
    new_today: int,
    coding_added: int = 0,
    noncoding_added: int = 0,
    top_coding: str = "None",
    top_noncoding: str = "None",
    archived: int = 0,
):
    """Send the daily summary notification."""
    notif_cfg = config.get("notifications", {})
    if not notif_cfg.get("enabled"):
        print("[notify] Notifications disabled. Summary:")
        _print_summary(total_jobs, new_today, coding_added, noncoding_added, top_coding, top_noncoding)
        return

    message = _build_message(
        total_jobs, new_today, coding_added, noncoding_added, top_coding, top_noncoding, archived
    )

    # Try OpenClaw first (if openclaw CLI is available)
    openclaw_channel = notif_cfg.get("openclaw_channel")
    openclaw_account = notif_cfg.get("openclaw_account")
    target_id = notif_cfg.get("telegram_chat_id")

    if openclaw_channel and target_id:
        sent = _send_openclaw(message, openclaw_channel, openclaw_account, target_id)
        if sent:
            print("[notify] Sent via OpenClaw.")
            return

    # Try Telegram Bot API
    bot_token = notif_cfg.get("telegram_bot_token")
    chat_id = notif_cfg.get("telegram_chat_id")

    if bot_token and chat_id:
        sent = _send_telegram(message, bot_token, chat_id)
        if sent:
            print("[notify] Sent via Telegram Bot API.")
            return

    # Fallback: print
    print("[notify] No notification method available. Summary:")
    _print_summary(total_jobs, new_today, coding_added, noncoding_added, top_coding, top_noncoding)


def _build_message(
    total_jobs: int,
    new_today: int,
    coding_added: int,
    noncoding_added: int,
    top_coding: str,
    top_noncoding: str,
    archived: int = 0,
) -> str:
    today = date.today().strftime("%b %d")
    lines = [
        f"📊 JobClaw Daily Summary — {today}",
        "",
    ]

    if coding_added > 0:
        lines.append(f"💻 Coding Jobs: {coding_added} new")
        if top_coding and top_coding != "None":
            lines.append(f"   Top: {top_coding}")
    else:
        lines.append("💻 Coding Jobs: none new")

    lines.append("")

    if noncoding_added > 0:
        lines.append(f"🎯 Non-Coding Jobs: {noncoding_added} new")
        if top_noncoding and top_noncoding != "None":
            lines.append(f"   Top: {top_noncoding}")
    else:
        lines.append("🎯 Non-Coding Jobs: none new")

    lines.append("")
    lines.append("───")
    lines.append(f"📈 Total in tracker: {total_jobs}")
    lines.append(f"🆕 New today: {new_today}")
    if archived > 0:
        lines.append(f"🗂 Auto-archived: {archived} expired")

    return "\n".join(lines)


def _send_openclaw(message: str, channel: str, account: str, target: str) -> bool:
    """Send via openclaw CLI (requires OpenClaw to be installed)."""
    # Find openclaw binary
    openclaw_paths = [
        "/home/" + os.environ.get("USER", "") + "/.npm-global/bin/openclaw",
        "/usr/local/bin/openclaw",
        "openclaw",
    ]
    openclaw_bin = None
    for p in openclaw_paths:
        if os.path.exists(p):
            openclaw_bin = p
            break

    if not openclaw_bin:
        # Try via PATH
        result = subprocess.run(["which", "openclaw"], capture_output=True, text=True)
        if result.returncode == 0:
            openclaw_bin = result.stdout.strip()

    if not openclaw_bin:
        return False

    cmd = [openclaw_bin, "message", "send", "--channel", channel, "--target", target, "--message", message]
    if account:
        cmd += ["--account", account]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"[notify] OpenClaw send failed: {e}")
        return False


def _send_telegram(message: str, bot_token: str, chat_id: str) -> bool:
    """Send via Telegram Bot API directly."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"[notify] Telegram send failed: {e}")
        return False


def _print_summary(total_jobs, new_today, coding_added, noncoding_added, top_coding, top_noncoding):
    print(f"""
  📊 JobClaw Daily Summary
  ─────────────────────────
  💻 Coding:     {coding_added} new  |  Top: {top_coding}
  🎯 Non-coding: {noncoding_added} new  |  Top: {top_noncoding}
  📈 Total:      {total_jobs}  |  New today: {new_today}
""")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test JobClaw notifications")
    parser.add_argument("--test", action="store_true", help="Send a test notification")
    args = parser.parse_args()

    if args.test:
        env_dir = os.environ.get("JOBCLAW_DIR", str(Path.home() / "Documents" / "JobClaw"))
        config_path = Path(env_dir) / "config.json"
        if not config_path.exists():
            print("Config not found. Run setup.py first.")
            exit(1)
        with open(config_path) as f:
            cfg = json.load(f)

        send_summary(
            config=cfg,
            total_jobs=42,
            new_today=5,
            coding_added=3,
            noncoding_added=2,
            top_coding="DeepMind — Research Scientist (Score: 92)",
            top_noncoding="GSK — Health AI Scientist (Score: 88)",
        )
