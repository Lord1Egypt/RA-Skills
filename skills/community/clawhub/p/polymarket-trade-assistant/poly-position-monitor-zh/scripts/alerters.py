#!/usr/bin/env python3
"""
Alert handlers for Polymarket position monitoring.

Provides Console, Telegram, and Email alert delivery with a common AlertHandler
interface. Each handler receives structured alert dicts and formats them for
its channel.

Alert dict structure:
    {
        "type": "CRITICAL" | "ALERT" | "WARNING" | "INFO",
        "category": "price" | "volume" | "position" | "whale" | "order" | "system",
        "market": str,
        "message": str,
        "data": dict,
        "timestamp": str (ISO format)
    }
"""

import json
import os
import smtplib
import urllib.request
import urllib.parse
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ALERT_EMOJI = {
    "CRITICAL": "\U0001f534",  # 🔴
    "ALERT": "\U0001f7e1",     # 🟡
    "WARNING": "\u26a0\ufe0f", # ⚠️
    "INFO": "\u2139\ufe0f",    # ℹ️
}

CATEGORY_LABEL = {
    "price": "价格波动",
    "volume": "成交量异动",
    "position": "仓位变化",
    "whale": "监控地址活动",
    "order": "挂单变化",
    "system": "系统",
}


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    DIM = "\033[2m"
    MAGENTA = "\033[95m"


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class AlertHandler(ABC):
    @abstractmethod
    def handle(self, alert: dict) -> None:
        ...


# ---------------------------------------------------------------------------
# Console
# ---------------------------------------------------------------------------

class ConsoleAlertHandler(AlertHandler):
    """Print alerts to terminal with color coding."""

    TYPE_STYLES = {
        "CRITICAL": (Colors.RED + Colors.BOLD, "CRITICAL"),
        "ALERT": (Colors.MAGENTA + Colors.BOLD, "ALERT"),
        "WARNING": (Colors.YELLOW, "WARNING"),
        "INFO": (Colors.DIM, "INFO"),
    }

    def handle(self, alert: dict) -> None:
        alert_type = alert.get("type", "INFO")
        style, label = self.TYPE_STYLES.get(alert_type, (Colors.RESET, alert_type))
        ts = alert.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
            time_str = dt.strftime("%H:%M:%S")
        except (ValueError, TypeError):
            time_str = ts[:8] if ts else "??:??:??"

        category = alert.get("category", "")
        cat_label = CATEGORY_LABEL.get(category, category)
        market = alert.get("market", "")
        msg = alert.get("message", "")

        parts = [f"{style}[{time_str}] {label}"]
        if cat_label:
            parts.append(f"| {cat_label}")
        if market:
            parts.append(f"| {market}")
        print(f"{' '.join(parts)}{Colors.RESET}")
        if msg:
            print(f"  {style}{msg}{Colors.RESET}")


# ---------------------------------------------------------------------------
# File (JSON lines)
# ---------------------------------------------------------------------------

class FileAlertHandler(AlertHandler):
    """Append alerts as JSON lines to a log file."""

    def __init__(self, log_path: str):
        self.log_path = os.path.expanduser(log_path)
        os.makedirs(os.path.dirname(os.path.abspath(self.log_path)) or ".", exist_ok=True)

    def handle(self, alert: dict) -> None:
        line = json.dumps(alert, ensure_ascii=False) + "\n"
        with open(self.log_path, "a") as f:
            f.write(line)


# ---------------------------------------------------------------------------
# Telegram Bot
# ---------------------------------------------------------------------------

class TelegramAlertHandler(AlertHandler):
    """Send alerts via Telegram Bot HTTP API (no extra dependencies)."""

    API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self, bot_token: str, chat_id: str, min_level: str = "WARNING"):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self._level_order = {"INFO": 0, "WARNING": 1, "ALERT": 2, "CRITICAL": 3}
        self._min_level = self._level_order.get(min_level, 1)

    def _format_message(self, alert: dict) -> str:
        alert_type = alert.get("type", "INFO")
        emoji = ALERT_EMOJI.get(alert_type, "")
        category = alert.get("category", "")
        cat_label = CATEGORY_LABEL.get(category, category)
        market = alert.get("market", "")
        msg = alert.get("message", "")
        ts = alert.get("timestamp", "")

        try:
            dt = datetime.fromisoformat(ts)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except (ValueError, TypeError):
            time_str = ts

        lines = [f"{emoji} *{alert_type}*"]
        if cat_label:
            lines[0] += f" | {cat_label}"
        if market:
            lines.append(f"市场: {market}")
        if msg:
            lines.append(msg)

        data = alert.get("data", {})
        if data.get("current_price") is not None:
            lines.append(f"当前价格: {data['current_price']:.4f}")
        if data.get("change_pct") is not None:
            lines.append(f"变化: {data['change_pct']:+.2%}")
        if data.get("threshold") is not None:
            lines.append(f"阈值: {data['threshold']:.0%}")

        lines.append(f"\n_{time_str}_")
        return "\n".join(lines)

    def handle(self, alert: dict) -> None:
        level = self._level_order.get(alert.get("type", "INFO"), 0)
        if level < self._min_level:
            return

        text = self._format_message(alert)
        payload = json.dumps({
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }).encode("utf-8")

        url = self.API_URL.format(token=self.bot_token)
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    print(f"[WARN] Telegram send failed: HTTP {resp.status}", flush=True)
        except Exception as e:
            print(f"[WARN] Telegram send failed: {e}", flush=True)


# ---------------------------------------------------------------------------
# Email (SMTP)
# ---------------------------------------------------------------------------

class EmailAlertHandler(AlertHandler):
    """Send alerts via SMTP email."""

    def __init__(self, smtp_host: str, smtp_port: int, username: str,
                 password: str, to_addr: str, from_addr: str = None,
                 min_level: str = "ALERT"):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.to_addr = to_addr
        self.from_addr = from_addr or username
        self._level_order = {"INFO": 0, "WARNING": 1, "ALERT": 2, "CRITICAL": 3}
        self._min_level = self._level_order.get(min_level, 2)

    def handle(self, alert: dict) -> None:
        level = self._level_order.get(alert.get("type", "INFO"), 0)
        if level < self._min_level:
            return

        alert_type = alert.get("type", "INFO")
        category = alert.get("category", "")
        cat_label = CATEGORY_LABEL.get(category, category)
        market = alert.get("market", "")
        msg = alert.get("message", "")

        subject = f"[Polymarket {alert_type}] {cat_label}"
        if market:
            subject += f" - {market}"

        body_parts = [
            f"Alert Type: {alert_type}",
            f"Category: {cat_label}",
            f"Market: {market}",
            f"Time: {alert.get('timestamp', 'N/A')}",
            "",
            msg,
        ]
        data = alert.get("data", {})
        if data:
            body_parts.append("")
            body_parts.append("Details:")
            for k, v in data.items():
                body_parts.append(f"  {k}: {v}")

        body = "\n".join(body_parts)

        message = MIMEMultipart()
        message["From"] = self.from_addr
        message["To"] = self.to_addr
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_addr, [self.to_addr], message.as_string())
        except Exception as e:
            print(f"[WARN] Email send failed: {e}", flush=True)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def build_handlers(config: dict) -> list[AlertHandler]:
    """Create alert handlers from a config dict."""
    handlers: list[AlertHandler] = [ConsoleAlertHandler()]

    notif = config.get("notifications", {})
    monitor_cfg = config.get("monitor", {})

    state_dir = os.path.expanduser(monitor_cfg.get("state_dir", "~/polymarket-monitoring"))
    log_path = os.path.join(state_dir, "alerts.jsonl")
    handlers.append(FileAlertHandler(log_path))

    tg = notif.get("telegram", {})
    if tg.get("enabled") and tg.get("bot_token") and tg.get("chat_id"):
        handlers.append(TelegramAlertHandler(
            bot_token=tg["bot_token"],
            chat_id=str(tg["chat_id"]),
            min_level=tg.get("min_level", "WARNING"),
        ))

    em = notif.get("email", {})
    if em.get("enabled") and em.get("username") and em.get("password"):
        handlers.append(EmailAlertHandler(
            smtp_host=em.get("smtp_host", "smtp.gmail.com"),
            smtp_port=em.get("smtp_port", 587),
            username=em["username"],
            password=em["password"],
            to_addr=em.get("to", em["username"]),
            from_addr=em.get("from", em["username"]),
            min_level=em.get("min_level", "ALERT"),
        ))

    return handlers


def emit(handlers: list[AlertHandler], alert_type: str, category: str,
         market: str, message: str, data: dict = None) -> dict:
    """Convenience function to build and dispatch an alert."""
    alert = {
        "type": alert_type,
        "category": category,
        "market": market,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    for h in handlers:
        h.handle(alert)
    return alert
