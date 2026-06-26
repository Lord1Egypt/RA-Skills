"""
Nex HealthCheck - Alert notifications
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import urllib.request
import urllib.parse
import json
from config import StatusLevel, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_alert(message, token=None, chat_id=None):
    """Send alert via Telegram. Returns True if successful."""
    token = token or TELEGRAM_BOT_TOKEN
    chat_id = chat_id or TELEGRAM_CHAT_ID

    if not token or not chat_id:
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }).encode("utf-8")

        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req, timeout=10)
        return response.getcode() == 200
    except Exception as e:
        print(f"Telegram alert failed: {e}")
        return False


def format_status_emoji(status):
    """Convert status to emoji."""
    if status == StatusLevel.OK.value or status == "ok":
        return "🟢"
    elif status == StatusLevel.WARNING.value or status == "warning":
        return "🟡"
    elif status == StatusLevel.CRITICAL.value or status == "critical":
        return "🔴"
    else:
        return "⚪"


def format_dashboard_message(results):
    """Format results for Telegram dashboard."""
    message = "🏥 *Health Dashboard*\n"
    message += "─" * 40 + "\n"

    # Group by status
    ok = [r for r in results if r.get("status") == StatusLevel.OK.value]
    warning = [r for r in results if r.get("status") == StatusLevel.WARNING.value]
    critical = [r for r in results if r.get("status") == StatusLevel.CRITICAL.value]

    if critical:
        message += f"🔴 *Critical ({len(critical)})*\n"
        for r in critical:
            message += f"  • {r.get('service_name', 'Unknown')}\n"
            message += f"    {r.get('message', 'No details')}\n"

    if warning:
        message += f"🟡 *Warning ({len(warning)})*\n"
        for r in warning:
            message += f"  • {r.get('service_name', 'Unknown')}\n"
            message += f"    {r.get('message', 'No details')}\n"

    if ok:
        message += f"🟢 *Healthy ({len(ok)})*\n"
        for r in ok[:5]:  # Show first 5
            message += f"  • {r.get('service_name', 'Unknown')}\n"
        if len(ok) > 5:
            message += f"  ... and {len(ok) - 5} more\n"

    message += "─" * 40 + "\n"
    total = len(results)
    healthy = len(ok)
    message += f"{healthy}/{total} healthy\n"

    return message


def format_incident_alert(service, old_status, new_status):
    """Format incident alert for status change."""
    emoji_old = format_status_emoji(old_status)
    emoji_new = format_status_emoji(new_status)

    message = f"{emoji_old} → {emoji_new} *{service.get('name', 'Unknown')}*\n"
    message += f"Status changed from {old_status} to {new_status}\n"
    message += f"Check type: {service.get('check_type', '?')}\n"
    message += f"Target: {service.get('target', '?')}\n"

    return message


def should_alert(service_id, new_status, last_status=None):
    """Debounce logic: avoid alert storms. Alert on state changes."""
    # In a full implementation, this would check the last_status
    # For now, alert on any non-OK status change
    if last_status and last_status == new_status:
        return False
    if new_status != StatusLevel.OK.value and new_status != "ok":
        return True
    return False
