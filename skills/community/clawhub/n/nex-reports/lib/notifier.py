"""
Nex Reports - Notifications
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import REPORTS_DIR, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message: str, token: Optional[str] = None, chat_id: Optional[str] = None) -> bool:
    """
    Send message to Telegram.
    Uses env TELEGRAM_TOKEN and TELEGRAM_CHAT_ID if not provided.
    Returns True on success.
    """
    token = token or TELEGRAM_TOKEN
    chat_id = chat_id or TELEGRAM_CHAT_ID

    if not token or not chat_id:
        print("Error: Telegram token and chat_id required")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("ok", False)
    except urllib.error.URLError as e:
        print(f"Telegram request failed: {e}")
        return False
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def save_to_file(content: str, filename: Optional[str] = None) -> str:
    """
    Save report content to file.
    Returns path to saved file.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if not filename:
        now = datetime.now()
        filename = f"report_{now.strftime('%Y%m%d_%H%M%S')}.md"

    filepath = REPORTS_DIR / filename
    filepath.write_text(content, encoding="utf-8")

    return str(filepath)


def save_report(
    content: str,
    format_type: str,
    title: str,
    output_target: str = "file",
    telegram_token: Optional[str] = None,
    telegram_chat_id: Optional[str] = None,
) -> Optional[str]:
    """
    Save and/or send report based on output_target.
    output_target: "file", "telegram", "both"
    Returns output path if saved to file, None if sent only to Telegram.
    """
    output_path = None

    # Determine file extension
    ext_map = {
        "telegram": "txt",
        "markdown": "md",
        "html": "html",
        "json": "json",
    }
    ext = ext_map.get(format_type, "txt")

    # Save to file
    if output_target in ("file", "both"):
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        output_path = save_to_file(content, filename)
        print(f"Report saved: {output_path}")

    # Send to Telegram
    if output_target in ("telegram", "both"):
        success = send_telegram(content, telegram_token, telegram_chat_id)
        if success:
            print("Report sent to Telegram")
        else:
            print("Failed to send Telegram message")

    return output_path
