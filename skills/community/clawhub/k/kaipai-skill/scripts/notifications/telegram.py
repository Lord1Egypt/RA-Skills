"""Optional Telegram delivery for image and video results."""

import json
import os
import sys
from typing import Dict, Any, Optional, Tuple

import requests
from .base import MissingCredentialsError, validate_duration_ms
import shlex
from pathlib import Path


def delivery_instructions(base_dir, recipient, *, is_video):
    """Generate Telegram worker steps without exposing the bot token."""
    script = Path(base_dir) / "scripts" / ("telegram_send_video.py" if is_video else "telegram_send_image.py")
    command = f"python3 {shlex.quote(str(script))}"
    target = shlex.quote(recipient)
    if not is_video:
        return f"  2. Send via Telegram (TELEGRAM_BOT_TOKEN from environment): {command} --image '<result_url>' --to {target}"
    return (
        "  2. Download and send the native video via Telegram (TELEGRAM_BOT_TOKEN from environment):\n"
        "     curl -fL -o /tmp/vmake_result.mp4 '<primary_result_url_or_output_urls[0]>'\n"
        f"     {command} --video /tmp/vmake_result.mp4 --to {target} "
        "--video-url '<primary_result_url_or_output_urls[0]>' "
        "[--cover-url '<optional_thumb_url>'] [--duration <seconds>]\n"
        "     --video-url always sends a second text link. About 50 MB limit; send the link for larger files."
    )


TELEGRAM_API_BASE = "https://api.telegram.org"
CONNECT_TIMEOUT = 15
UPLOAD_TIMEOUT = 180


class TelegramNotifier:
    """Telegram notification channel."""

    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Telegram notifier.

        :param bot_token: Bot token (or from TELEGRAM_BOT_TOKEN env var)
        """
        self._token = bot_token

    def _get_token(self) -> str:
        """Get bot token from env or constructor."""
        if self._token:
            return self._token
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            raise MissingCredentialsError(
                "TELEGRAM_BOT_TOKEN environment variable is not set",
                '未设置 Telegram Bot Token，请先设置 TELEGRAM_BOT_TOKEN 环境变量再运行脚本',
            )
        return token

    def _send_photo(
        self, chat_id: str, image_source: str, caption: str = ""
    ) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Return a photo result plus errors with the legacy sender's JSON details."""
        token = self._get_token()
        print(f"[telegram] Sending image: {image_source}", file=sys.stderr)

        data: Dict[str, Any] = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption

        if image_source.startswith("http"):
            print(f"[telegram] Downloading image: {image_source}", file=sys.stderr)
            r = requests.get(image_source, timeout=(CONNECT_TIMEOUT, 60))
            r.raise_for_status()
            img_bytes = r.content
            filename = image_source.split("?")[0].split("/")[-1] or "image.jpg"
            files = {"photo": (filename, img_bytes, "image/jpeg")}
            resp = requests.post(
                f"{TELEGRAM_API_BASE}/bot{token}/sendPhoto",
                data=data,
                files=files,
                timeout=(CONNECT_TIMEOUT, UPLOAD_TIMEOUT),
            )
        else:
            if not os.path.isfile(image_source):
                message = f"Image file not found: {image_source}"
                return None, {"error": message, "error_details": {"error": message}}
            with open(image_source, "rb") as f:
                files = {"photo": (os.path.basename(image_source), f, "image/jpeg")}
                resp = requests.post(
                    f"{TELEGRAM_API_BASE}/bot{token}/sendPhoto",
                    data=data,
                    files=files,
                    timeout=(CONNECT_TIMEOUT, UPLOAD_TIMEOUT),
                )

        if resp.status_code != 200:
            body = {}
            try:
                body = resp.json()
            except Exception:
                pass
            err = body.get("description", resp.text[:200])
            return None, {
                "error": f"HTTP {resp.status_code}: {err}",
                "error_details": {
                    "error": f"Telegram API error: HTTP {resp.status_code}",
                    "description": err,
                },
            }

        result = resp.json()
        if not result.get("ok"):
            description = result.get("description", "unknown error")
            return None, {
                "error": description,
                "error_details": {"error": "Telegram sendPhoto failed", "description": description},
            }

        return result["result"], None

    def _send_video(
        self,
        chat_id: str,
        video_path: str,
        cover_url: str = "",
        duration_seconds: int = 0,
        caption: str = "",
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """Send video; returns (message dict, error string)."""
        token = self._get_token()
        print(f"[telegram] Sending video: {video_path}", file=sys.stderr)

        data: Dict[str, Any] = {"chat_id": chat_id}
        if duration_seconds:
            data["duration"] = duration_seconds
        if caption:
            data["caption"] = caption
        data["supports_streaming"] = True

        files: Dict[str, Any] = {}

        with open(video_path, "rb") as vf:
            files["video"] = (os.path.basename(video_path), vf, "video/mp4")

            if cover_url:
                try:
                    print(f"[telegram] Downloading thumbnail: {cover_url}", file=sys.stderr)
                    r = requests.get(cover_url, timeout=(CONNECT_TIMEOUT, 30))
                    if r.status_code == 200:
                        files["thumbnail"] = ("cover.jpg", r.content, "image/jpeg")
                    else:
                        print(
                            f"[telegram] Thumbnail download failed (HTTP {r.status_code}), skipping",
                            file=sys.stderr,
                        )
                except Exception as exc:
                    print(f"[telegram] Thumbnail download error: {exc}, skipping", file=sys.stderr)

            resp = requests.post(
                f"{TELEGRAM_API_BASE}/bot{token}/sendVideo",
                data=data,
                files=files,
                timeout=(CONNECT_TIMEOUT, UPLOAD_TIMEOUT),
            )

        if resp.status_code != 200:
            body = {}
            try:
                body = resp.json()
            except Exception:
                pass
            err = body.get("description", resp.text[:200])
            return None, err or f"HTTP {resp.status_code}"

        result = resp.json()
        if not result.get("ok"):
            return None, result.get("description", "unknown error")

        return result["result"], None

    def _send_text_message(self, chat_id: str, text: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Send plain text message."""
        token = self._get_token()
        print("[telegram] Sending text message", file=sys.stderr)
        resp = requests.post(
            f"{TELEGRAM_API_BASE}/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=(CONNECT_TIMEOUT, 30),
        )
        if resp.status_code != 200:
            body = {}
            try:
                body = resp.json()
            except Exception:
                pass
            err = body.get("description", resp.text[:200])
            return None, err or f"HTTP {resp.status_code}"

        result = resp.json()
        if not result.get("ok"):
            return None, result.get("description", "unknown error")

        return result["result"], None

    def send_image(self, image_source: str, recipient: str, caption: str = "") -> Dict[str, Any]:
        """Send image notification."""
        msg, err = self._send_photo(recipient, image_source, caption)

        if err:
            return {
                "status": "failed",
                **err,
            }

        return {
            "status": "ok",
            "message_id": msg.get("message_id") if msg else None,
            "chat_id": msg.get("chat", {}).get("id") if msg else None,
        }

    def send_video(
        self,
        video_path: str,
        recipient: str,
        video_url: str = "",
        cover_url: str = "",
        duration: int = 0,
        caption: str = "",
        *,
        duration_ms: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Keep legacy seconds; convert explicit milliseconds to whole seconds, rounding up."""
        validate_duration_ms(duration, duration_ms)
        if duration_ms is not None:
            duration = (duration_ms + 999) // 1000
        video_url = (video_url or "").strip()
        video_msg, video_err = self._send_video(
            chat_id=recipient,
            video_path=video_path,
            cover_url=cover_url,
            duration_seconds=duration,
            caption=caption,
        )

        text_msg = None
        text_err = None
        if video_url:
            link_text = f"Video download:\n{video_url}"
            text_msg, text_err = self._send_text_message(recipient, link_text)

        if video_url:
            ok = bool((video_msg is not None) or (text_msg is not None))
        else:
            ok = video_msg is not None

        result: Dict[str, Any] = {
            "status": "ok" if ok else "failed",
            "message_id": video_msg.get("message_id") if video_msg else None,
            "chat_id": (video_msg or text_msg or {}).get("chat", {}).get("id"),
            "text_message_id": text_msg.get("message_id") if text_msg else None,
        }
        if video_err:
            result["video_error"] = video_err
        if text_err:
            result["text_error"] = text_err

        return result
