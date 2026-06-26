"""Feishu (Lark) notification channel for Kaipai AI skill."""

import json
import os
import sys
from typing import Dict, Any, Optional, Tuple

import requests


class FeishuNotifier:
    """Feishu notification channel."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Feishu notifier.

        :param config_path: Path to openclaw config file
        """
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self._token: Optional[str] = None

    def _get_credentials(self) -> Tuple[str, str]:
        """Read Feishu credentials from config."""
        with open(self.config_path) as f:
            config = json.load(f)
        feishu = config.get("channels", {}).get("feishu", {})
        accounts = feishu.get("accounts", {})
        if accounts:
            main_acct = accounts.get("main", accounts.get("default", list(accounts.values())[0] if accounts else {}))
            app_id = main_acct.get("appId", "")
            app_secret = main_acct.get("appSecret", "")
        else:
            app_id = feishu.get("appId", "")
            app_secret = feishu.get("appSecret", "")
        if not app_id or not app_secret:
            raise ValueError("Feishu credentials not found in ~/.openclaw/openclaw.json")
        return app_id, app_secret

    def _get_token(self) -> str:
        """Get tenant access token."""
        if self._token:
            return self._token
        app_id, app_secret = self._get_credentials()
        resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": app_id, "app_secret": app_secret},
        )
        resp.raise_for_status()
        self._token = resp.json()["tenant_access_token"]
        return self._token

    def _normalize_recipient(self, to: str) -> Tuple[str, str]:
        """Return (receive_id, receive_id_type) with chat:/user: stripped."""
        if to.startswith("chat:"):
            to = to[5:]
        elif to.startswith("user:"):
            to = to[5:]
        if to.startswith("oc_"):
            return to, "chat_id"
        return to, "open_id"

    def _upload_image(self, image_source: str) -> str:
        """Upload image, return image_key."""
        token = self._get_token()

        if image_source.startswith("http"):
            print(f"[feishu] Downloading image: {image_source}", file=sys.stderr)
            img_resp = requests.get(image_source, timeout=(15, 60))
            img_resp.raise_for_status()
            img_data = img_resp.content
            filename = image_source.split("?")[0].split("/")[-1] or "image.jpg"
        else:
            with open(image_source, "rb") as f:
                img_data = f.read()
            filename = os.path.basename(image_source)

        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "jpg"
        content_type_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
            "gif": "image/gif",
        }
        content_type = content_type_map.get(ext, "image/jpeg")

        resp = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/images",
            headers={"Authorization": f"Bearer {token}"},
            data={"image_type": "message"},
            files={"image": (filename, img_data, content_type)},
            timeout=(15, 60),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Image upload failed: {result}")
        return result["data"]["image_key"]

    def _upload_video(self, video_path: str, duration_ms: Optional[int] = None) -> str:
        """Upload video file, return file_key."""
        token = self._get_token()
        data: Dict[str, Any] = {"file_type": "mp4", "file_name": os.path.basename(video_path)}
        if duration_ms:
            data["duration"] = str(int(duration_ms))

        with open(video_path, "rb") as f:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/im/v1/files",
                headers={"Authorization": f"Bearer {token}"},
                data=data,
                files={"file": (os.path.basename(video_path), f, "video/mp4")},
                timeout=(15, 120),
            )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Video upload failed: {result}")
        return result["data"]["file_key"]

    def _send_image_message(self, receive_id: str, receive_id_type: str, image_key: str) -> str:
        """Send image message."""
        token = self._get_token()
        resp = requests.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "receive_id": receive_id,
                "msg_type": "image",
                "content": json.dumps({"image_key": image_key}),
            },
            timeout=(15, 30),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Send failed: {result}")
        return result["data"]["message_id"]

    def _send_media_message(
        self, receive_id: str, receive_id_type: str, file_key: str, image_key: Optional[str] = None
    ) -> str:
        """Send media message (video)."""
        token = self._get_token()
        content: Dict[str, Any] = {"file_key": file_key}
        if image_key:
            content["image_key"] = image_key

        resp = requests.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "receive_id": receive_id,
                "msg_type": "media",
                "content": json.dumps(content),
            },
            timeout=(15, 30),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Send failed: {result}")
        return result["data"]["message_id"]

    def _send_text_message(self, receive_id: str, receive_id_type: str, text: str) -> str:
        """Send plain text message."""
        token = self._get_token()
        resp = requests.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "receive_id": receive_id,
                "msg_type": "text",
                "content": json.dumps({"text": text}),
            },
            timeout=(15, 30),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Text send failed: {result}")
        return result["data"]["message_id"]

    def send_image(self, image_source: str, recipient: str, caption: str = "") -> Dict[str, Any]:
        """Send image notification."""
        receive_id, receive_id_type = self._normalize_recipient(recipient)
        image_key = self._upload_image(image_source)
        message_id = self._send_image_message(receive_id, receive_id_type, image_key)

        result = {
            "status": "ok",
            "message_id": message_id,
            "image_key": image_key,
        }

        if caption:
            try:
                text_id = self._send_text_message(receive_id, receive_id_type, caption)
                result["text_message_id"] = text_id
            except Exception as e:
                result["text_error"] = str(e)

        return result

    def send_video(
        self,
        video_path: str,
        recipient: str,
        video_url: str = "",
        cover_url: str = "",
        duration: int = 0,
        caption: str = "",
    ) -> Dict[str, Any]:
        """Send video notification."""
        receive_id, receive_id_type = self._normalize_recipient(recipient)

        # Upload video
        print(f"[feishu] Uploading video: {video_path}", file=sys.stderr)
        file_key = self._upload_video(video_path, duration)
        print(f"[feishu] Video file_key: {file_key}", file=sys.stderr)

        # Upload cover if provided
        image_key = None
        if cover_url:
            print(f"[feishu] Uploading cover: {cover_url}", file=sys.stderr)
            image_key = self._upload_image(cover_url)
            print(f"[feishu] Cover image_key: {image_key}", file=sys.stderr)

        # Send media message
        media_message_id = None
        media_error = None
        try:
            media_message_id = self._send_media_message(
                receive_id, receive_id_type, file_key, image_key
            )
            print(f"[feishu] Media message_id: {media_message_id}", file=sys.stderr)
        except Exception as exc:
            media_error = str(exc)
            print(f"[feishu] Media send error: {media_error}", file=sys.stderr)

        # Send video URL if provided
        text_message_id = None
        text_error = None
        if video_url:
            link_text = f"视频下载：[链接]({video_url})"
            if caption:
                link_text = f"{caption}\n\n{link_text}"
            try:
                text_message_id = self._send_text_message(receive_id, receive_id_type, link_text)
                print(f"[feishu] Text message_id: {text_message_id}", file=sys.stderr)
            except Exception as exc:
                text_error = str(exc)
                print(f"[feishu] Text send error: {text_error}", file=sys.stderr)

        ok = bool(media_message_id or text_message_id)

        result = {
            "status": "ok" if ok else "failed",
            "message_id": media_message_id,
            "media_message_id": media_message_id,
            "text_message_id": text_message_id,
            "file_key": file_key,
            "image_key": image_key,
        }
        if media_error:
            result["media_error"] = media_error
        if text_error:
            result["text_error"] = text_error

        return result
