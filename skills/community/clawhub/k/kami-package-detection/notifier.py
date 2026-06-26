"""
Notification Module for Package Detection
Sends alarm notifications via Feishu Webhook, Telegram Bot API, and Discord Webhook/Bot API.
Supports attaching alarm snapshot images to notifications.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


# ── Image upload helpers ─────────────────────────────────────────────────────
def _upload_image_to_imghost(local_path: str) -> str:
    """Upload a local image to sm.ms anonymous image host.

    Returns the public https URL on success, or '' on failure.
    Used as a fallback when Feishu OpenAPI image upload is unavailable.
    """
    import requests as _req
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        with open(local_path, "rb") as f:
            files = {"smfile": (os.path.basename(local_path), f.read(), "image/jpeg")}
        resp = _req.post("https://sm.ms/api/v2/upload", files=files, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("url"):
            return data["data"]["url"]
        if data.get("code") == "image_repeated" and data.get("images"):
            return data["images"]
        logger.warning(f"sm.ms upload non-success: {data}")
        return ""
    except Exception as e:
        logger.error(f"Image host upload failed ({local_path}): {e}")
        return ""


def _feishu_get_tenant_token(app_id: str, app_secret: str) -> str:
    """Obtain a tenant_access_token from Feishu OpenAPI."""
    import requests as _req
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = {"app_id": app_id, "app_secret": app_secret}
    resp = _req.post(url, json=body, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token error: {data}")
    return data["tenant_access_token"]


def _feishu_upload_image(app_id: str, app_secret: str, local_path: str) -> str:
    """Upload a local image to Feishu via OpenAPI and return the image_key.

    Requires a Feishu app with im:resource permission. The returned image_key
    can be used in interactive card img elements to render inline.
    """
    import requests as _req
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        token = _feishu_get_tenant_token(app_id, app_secret)
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        with open(local_path, "rb") as f:
            file_bytes = f.read()
        files = {"image": (os.path.basename(local_path), file_bytes, "image/jpeg")}
        data = {"image_type": "message"}
        headers = {"Authorization": f"Bearer {token}"}
        resp = _req.post(url, headers=headers, data=data, files=files, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            logger.warning(f"Feishu image upload API error: {result}")
            return ""
        return result.get("data", {}).get("image_key", "")
    except Exception as e:
        logger.error(f"Feishu image upload failed ({local_path}): {e}")
        return ""


# ── Feishu Webhook ────────────────────────────────────────────────────────────
def send_feishu_alarm(webhook_url: str, alarm: Dict[str, Any],
                     app_id: str = "", app_secret: str = "") -> bool:
    """Send package alarm to Feishu using webhook with optional image.

    Image rendering strategy (same as suspicious-person skill):
      1. If app_id + app_secret provided, upload snapshot via OpenAPI (inline img).
      2. Fallback: upload to sm.ms and show clickable URL.
      3. Final fallback: show local file path as text.
    """
    import requests

    class_name = alarm.get("class_name", "package")
    confidence = alarm.get("confidence", 0)
    camera_name = alarm.get("camera_name")
    snapshot = alarm.get("snapshot", "")

    confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"
    camera_line = f"\n**📷 摄像头**: {camera_name}" if camera_name else ""

    # --- Attempt to get a renderable image ---
    image_key = ""
    image_url = ""
    if snapshot and app_id and app_secret:
        image_key = _feishu_upload_image(app_id, app_secret, snapshot)
    if not image_key and snapshot:
        image_url = _upload_image_to_imghost(snapshot)

    # Build snapshot display text
    if image_key:
        snap_md = "(见下方图片)"
    elif image_url:
        snap_md = f"[查看快照]({image_url})"
    elif snapshot:
        snap_md = f"`{snapshot}`"
    else:
        snap_md = "-"

    content_md = (
        f"**📦 包裹检测报警**{camera_line}\n"
        f"**检测到**: {class_name}\n"
        f"**置信度**: {confidence_display}\n"
        f"**时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**快照**: {snap_md}"
    )

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": content_md}},
    ]
    if image_key:
        elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {"tag": "plain_text", "content": "包裹检测快照"},
        })
    elements.append({"tag": "hr"})
    elements.append({"tag": "note", "elements": [
        {"tag": "plain_text", "content": "Kami Package Detection System"}
    ]})

    try:
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": "📦 包裹检测报警"},
                    "template": "blue",
                },
                "elements": elements,
            },
        }
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("StatusCode") == 0 or data.get("code") == 0 or data.get("Extra") == "":
            logger.info("Feishu webhook alarm sent successfully (with image card)")
            return True
        else:
            logger.error(f"Feishu webhook failed: {data}")
            return False
    except Exception as e:
        logger.error(f"Failed to send Feishu webhook alarm: {e}")
        return False


# ── Telegram Bot API ──────────────────────────────────────────────────────────
TELEGRAM_API_URL = "https://api.telegram.org/bot"


def send_telegram_alarm(bot_token: str, chat_id: str, alarm: Dict[str, Any]) -> bool:
    """Send package alarm to Telegram using Bot API.

    If snapshot file exists, uses sendPhoto for inline image display;
    otherwise falls back to sendMessage with text only.
    """
    import requests

    class_name = alarm.get("class_name", "package")
    confidence = alarm.get("confidence", 0)
    camera_name = alarm.get("camera_name")
    snapshot = alarm.get("snapshot", "")

    confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"
    camera_line = f"\n📷 <b>Camera</b>: {camera_name}" if camera_name else ""

    from html import escape as html_escape
    text = (
        f"<b>📦 包裹检测报警</b>{camera_line}\n\n"
        f"<b>检测到</b>: {html_escape(class_name)}\n"
        f"<b>置信度</b>: {confidence_display}\n"
        f"<b>时间</b>: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        # If snapshot exists, send via sendPhoto for inline image
        if snapshot and os.path.isfile(snapshot):
            url = f"{TELEGRAM_API_URL}{bot_token}/sendPhoto"
            with open(snapshot, "rb") as f:
                file_bytes = f.read()
            files = {"photo": (os.path.basename(snapshot), file_bytes, "image/jpeg")}
            data = {
                "chat_id": chat_id,
                "caption": text,
                "parse_mode": "HTML",
            }
            resp = requests.post(url, data=data, files=files, timeout=10)
        else:
            # Fallback: text-only message
            if snapshot:
                text += f"\n<b>快照</b>: <code>{html_escape(snapshot)}</code>"
            url = f"{TELEGRAM_API_URL}{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
            resp = requests.post(url, json=payload, timeout=10)

        resp.raise_for_status()
        data = resp.json()

        if not data.get("ok"):
            logger.error(f"Telegram send failed: {data.get('description', 'unknown error')}")
            return False

        logger.info(f"Telegram message sent to {chat_id} (with image: {bool(snapshot and os.path.isfile(snapshot))})")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


# ── Discord Webhook / Bot API ─────────────────────────────────────────────────
DISCORD_API_BASE = "https://discord.com/api/v10"


def send_discord_webhook_alarm(webhook_url: str, alarm: Dict[str, Any]) -> bool:
    """Send package alarm to Discord using webhook.

    If snapshot file exists, attaches it via multipart so the image renders
    inline inside the embed (no public URL required).
    """
    import requests

    class_name = alarm.get("class_name", "package")
    confidence = alarm.get("confidence", 0)
    camera_name = alarm.get("camera_name")
    snapshot = alarm.get("snapshot", "")

    confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"

    fields = []
    if camera_name:
        fields.append({"name": "Camera", "value": camera_name, "inline": True})
    fields.extend([
        {"name": "Detected", "value": class_name, "inline": True},
        {"name": "Confidence", "value": confidence_display, "inline": True},
        {"name": "Time", "value": time.strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
    ])

    embed = {
        "title": "📦 Package Detection Alert",
        "description": "**A package/delivery has been detected!**",
        "color": 0x3498DB,
        "fields": fields,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "footer": {"text": "Kami Package Detection System"},
    }

    try:
        headers = {"User-Agent": "KamiPackageDetection/2.0"}
        # Attach snapshot inline if available
        if snapshot and os.path.isfile(snapshot):
            filename = os.path.basename(snapshot)
            embed["image"] = {"url": f"attachment://{filename}"}
            payload = {"embeds": [embed]}
            with open(snapshot, "rb") as f:
                file_bytes = f.read()
            files = {"files[0]": (filename, file_bytes, "image/jpeg")}
            data = {"payload_json": json.dumps(payload, ensure_ascii=False)}
            resp = requests.post(webhook_url, data=data, files=files,
                                 headers=headers, timeout=10)
        else:
            payload = {"embeds": [embed]}
            headers["Content-Type"] = "application/json; charset=utf-8"
            resp = requests.post(webhook_url, json=payload,
                                 headers=headers, timeout=10)
        resp.raise_for_status()
        logger.info(f"Discord webhook alarm sent successfully (with image: {bool(snapshot and os.path.isfile(snapshot))})")
        return True
    except Exception as e:
        logger.error(f"Failed to send Discord webhook alarm: {e}")
        return False


def send_discord_bot_alarm(bot_token: str, channel_id: str, alarm: Dict[str, Any]) -> bool:
    """Send package alarm to Discord using Bot API.

    If snapshot file exists, attaches it via multipart so the image renders
    inline inside the embed.
    """
    import requests

    class_name = alarm.get("class_name", "package")
    confidence = alarm.get("confidence", 0)
    camera_name = alarm.get("camera_name")
    snapshot = alarm.get("snapshot", "")

    confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"

    fields = []
    if camera_name:
        fields.append({"name": "Camera", "value": camera_name, "inline": True})
    fields.extend([
        {"name": "Detected", "value": class_name, "inline": True},
        {"name": "Confidence", "value": confidence_display, "inline": True},
        {"name": "Time", "value": time.strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
    ])

    embed = {
        "title": "📦 Package Detection Alert",
        "description": "**A package/delivery has been detected!**",
        "color": 0x3498DB,
        "fields": fields,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "footer": {"text": "Kami Package Detection System"},
    }

    try:
        headers = {"Authorization": f"Bot {bot_token}",
                   "User-Agent": "KamiPackageDetection/2.0"}
        # Attach snapshot inline if available
        if snapshot and os.path.isfile(snapshot):
            filename = os.path.basename(snapshot)
            embed["image"] = {"url": f"attachment://{filename}"}
            payload = {"embeds": [embed]}
            with open(snapshot, "rb") as f:
                file_bytes = f.read()
            files = {"files[0]": (filename, file_bytes, "image/jpeg")}
            data = {"payload_json": json.dumps(payload, ensure_ascii=False)}
            resp = requests.post(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                headers=headers, data=data, files=files, timeout=10)
        else:
            headers["Content-Type"] = "application/json; charset=utf-8"
            payload = {"embeds": [embed]}
            resp = requests.post(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Discord bot alarm sent to channel {channel_id} (with image: {bool(snapshot and os.path.isfile(snapshot))})")
        return True
    except Exception as e:
        logger.error(f"Failed to send Discord bot alarm: {e}")
        return False


# ── Unified alarm dispatcher ──────────────────────────────────────────────────
def dispatch_alarm(alarm: Dict[str, Any], cfg: dict,
                   log: Optional[logging.Logger] = None):
    """Send alarm to all configured notification channels.

    The alarm dict should contain a 'snapshot' key with the local file path
    of the annotated image. Each channel function will attach it inline.
    """
    log = log or logger

    # Feishu
    try:
        webhook_url = cfg.get("feishu_webhook_url")
        if webhook_url:
            log.info("Sending Feishu alarm via webhook")
            send_feishu_alarm(
                webhook_url, alarm,
                app_id=cfg.get("feishu_app_id", ""),
                app_secret=cfg.get("feishu_app_secret", ""),
            )
        else:
            log.debug("Feishu webhook_url not configured, skipping")
    except Exception as e:
        log.error(f"Failed to send Feishu alarm: {e}")

    # Telegram
    try:
        chat_id = cfg.get("telegram_chat_id")
        bot_token = cfg.get("telegram_bot_token")
        if chat_id and bot_token:
            log.info(f"Sending Telegram alarm to {chat_id}")
            send_telegram_alarm(bot_token, chat_id, alarm)
        else:
            log.debug("Telegram not fully configured, skipping")
    except Exception as e:
        log.error(f"Failed to send Telegram alarm: {e}")

    # Discord
    try:
        bot_token = cfg.get("discord_bot_token")
        channel_id = cfg.get("discord_channel_id")
        webhook_url = cfg.get("discord_webhook_url")

        if bot_token and channel_id:
            log.info(f"Sending Discord alarm via Bot API to channel {channel_id}")
            send_discord_bot_alarm(bot_token, channel_id, alarm)
        elif webhook_url:
            log.info("Sending Discord alarm via webhook")
            send_discord_webhook_alarm(webhook_url, alarm)
        else:
            log.debug("Discord not configured, skipping")
    except Exception as e:
        log.error(f"Failed to send Discord alarm: {e}")
