"""
Feishu Notification Module for Fall Detection
Sends alarm notifications to Feishu using the fall-detection account.

Supports:
- Direct chat_id configuration
- Feishu chat URL configuration (auto-extracts chat_id)
"""

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Feishu API endpoints
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_SEND_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
FEISHU_WEBHOOK_PREFIX = "https://open.feishu.cn/open-apis/bot/v2/hook/"


# ---------------------------------------------------------------------------
# Standalone image upload helpers (used by webhook mode for inline rendering)
# ---------------------------------------------------------------------------

def _upload_image_to_imghost(local_path: str) -> str:
    """Upload a local image to the sm.ms anonymous image host.

    Returns the public https URL on success, or '' on any failure. Used by the
    Feishu webhook push as a fallback to obtain a clickable image URL when no
    Feishu app credentials are configured.
    """
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        import requests
        with open(local_path, "rb") as f:
            files = {"smfile": (os.path.basename(local_path), f.read(), "image/jpeg")}
        resp = requests.post("https://sm.ms/api/v2/upload", files=files, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("url"):
            return data["data"]["url"]
        if data.get("code") == "image_repeated" and data.get("images"):
            return data["images"]
        logger.warning(f"sm.ms upload non-success response: {data}")
        return ""
    except Exception as e:
        logger.error(f"Image host upload failed ({local_path}): {e}")
        return ""


def _feishu_get_tenant_token(app_id: str, app_secret: str) -> str:
    """Obtain a tenant_access_token from Feishu OpenAPI (no caching)."""
    import requests
    body = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(FEISHU_TOKEN_URL, json=body, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token error: {data}")
    return data["tenant_access_token"]


def _feishu_upload_image(app_id: str, app_secret: str, local_path: str) -> str:
    """Upload a local image to Feishu via OpenAPI and return the image_key.

    Requires a self-built Feishu app with im:resource permission. The returned
    image_key can be used in interactive card `img` elements to render the
    image inline. Returns '' on any failure.
    """
    if not local_path or not os.path.isfile(local_path):
        return ""
    try:
        import requests
        token = _feishu_get_tenant_token(app_id, app_secret)
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        with open(local_path, "rb") as f:
            file_bytes = f.read()
        files = {"image": (os.path.basename(local_path), file_bytes, "image/jpeg")}
        data = {"image_type": "message"}
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            logger.warning(f"Feishu image upload API error: {result}")
            return ""
        return result.get("data", {}).get("image_key", "")
    except Exception as e:
        logger.error(f"Feishu image upload failed ({local_path}): {e}")
        return ""


class FeishuNotifier:
    """Send fall alarm notifications to Feishu."""
    
    def __init__(self, app_id: str, app_secret: str, domain: str = "feishu"):
        """
        Initialize Feishu notifier.
        
        Args:
            app_id: Feishu app ID (e.g., cli_a923859f21cddbc8)
            app_secret: Feishu app secret
            domain: "feishu" for 飞书, "lark" for Lark
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self.base_url = "https://open.feishu.cn" if domain == "feishu" else "https://open.larksuite.com"
        self._token_cache: Dict[str, Any] = {}
    
    def _get_tenant_token(self) -> str:
        """Get or refresh tenant access token."""
        now = time.time()
        
        # Check cache
        if self._token_cache.get("token") and self._token_cache.get("expire_at", 0) > now + 60:
            return self._token_cache["token"]
        
        # Request new token
        import requests
        
        try:
            resp = requests.post(
                f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal",
                json={
                    "app_id": self.app_id,
                    "app_secret": self.app_secret
                },
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") != 0:
                raise Exception(f"Token request failed: {data.get('msg', 'unknown error')}")
            
            token = data["tenant_access_token"]
            expires_in = data.get("expire", 7200)
            
            self._token_cache = {
                "token": token,
                "expire_at": now + expires_in - 60  # Refresh 60s early
            }
            
            logger.info("Feishu token refreshed")
            return token
            
        except Exception as e:
            logger.error(f"Failed to get Feishu token: {e}")
            raise
    
    def send_text_message(self, chat_id: str, text: str, receive_id_type: str = "chat_id") -> bool:
        """
        Send a text message to a Feishu chat.
        
        Args:
            chat_id: Chat ID (open_chat_id or chat_id)
            text: Message text
            receive_id_type: "chat_id" or "open_chat_id"
            
        Returns:
            True if sent successfully, False otherwise
        """
        import requests
        
        try:
            token = self._get_tenant_token()
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "receive_id": chat_id,
                "msg_type": "text",
                "content": json.dumps({"text": text})
            }
            
            resp = requests.post(
                f"{self.base_url}/open-apis/im/v1/messages",
                params={"receive_id_type": receive_id_type},
                headers=headers,
                json=payload,
                timeout=10
            )
            
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") != 0:
                logger.error(f"Feishu send failed: {data.get('msg', 'unknown error')}")
                return False
            
            logger.info(f"Feishu message sent to {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Feishu message: {e}")
            return False
    
    def send_alarm(self, chat_id: str, alarm: Dict[str, Any], clip_path: Optional[str] = None, posture_image_path: Optional[str] = None) -> bool:
        """
        Send a formatted fall alarm notification.
        
        Args:
            chat_id: Target chat ID
            alarm: Alarm data from fall detection
            clip_path: Optional path to alarm video clip
            posture_image_path: Optional path to fall posture reference image
            
        Returns:
            True if sent successfully
        """
        import requests
        
        # Build alarm message
        fall_type = alarm.get("fall_type", "unknown")
        confidence = alarm.get("confidence", 0)
        reason = alarm.get("reason", "Unknown")
        camera_name = alarm.get("camera_name")

        # Format fall type for display
        fall_type_map = {
            "active_falling": "🔄 主动跌倒",
            "fallen_posture": "📍 倒地姿态",
            "unknown": "⚠️ 未知类型"
        }
        fall_type_cn = fall_type_map.get(fall_type, f"⚠️ {fall_type}")

        # Format confidence
        confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"

        # Camera identity line (omitted when not provided)
        camera_line = f"\n📷 摄像头：{camera_name}" if camera_name else ""

        # Build message
        text = f"""🚨 跌倒报警{camera_line}

{fall_type_cn}
置信度：{confidence_display}
原因：{reason[:100]}

时间：{time.strftime("%Y-%m-%d %H:%M:%S")}
"""

        if clip_path:
            text += f"\n视频：{clip_path}"
        
        # Send as rich text with image if posture image is provided
        if posture_image_path and os.path.isfile(posture_image_path):
            return self.send_image_message(chat_id, text, posture_image_path)
        
        return self.send_text_message(chat_id, text)
    
    def send_image_message(self, chat_id: str, text: str, image_path: str) -> bool:
        """
        Send a message with an attached image to Feishu.
        
        Args:
            chat_id: Target chat ID
            text: Message text
            image_path: Path to image file
            
        Returns:
            True if sent successfully
        """
        import requests
        
        try:
            token = self._get_tenant_token()
            
            # First upload the image to Feishu
            upload_url = f"{self.base_url}/open-apis/im/v1/images"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            with open(image_path, 'rb') as f:
                files = {'image': f}
                resp = requests.post(upload_url, headers=headers, files=files, timeout=10)
                resp.raise_for_status()
                upload_data = resp.json()
                
                if upload_data.get("code") != 0:
                    logger.error(f"Image upload failed: {upload_data.get('msg', 'unknown')}")
                    return False
                
                image_key = upload_data["data"]["image_key"]
            
            # Send message with image
            send_url = f"{self.base_url}/open-apis/im/v1/messages"
            send_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Use rich_text msg_type to combine text and image
            payload = {
                "receive_id": chat_id,
                "msg_type": "image",
                "content": json.dumps({"image_key": image_key})
            }
            
            resp = requests.post(
                send_url,
                params={"receive_id_type": "chat_id"},
                headers=send_headers,
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") != 0:
                logger.error(f"Feishu image send failed: {data.get('msg', 'unknown error')}")
                return False
            
            # Send follow-up text message
            self.send_text_message(chat_id, text)
            
            logger.info(f"Feishu image + message sent to {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Feishu image message: {e}")
            return False


def extract_chat_id_from_url(url: str) -> Optional[str]:
    """
    Extract chat_id from Feishu chat URL.
    
    Supported URL formats:
    - https://www.feishu.cn/chat/oc_xxxxxxxxxxxx
    - https://feishu.cn/chat/oc_xxxxxxxxxxxx
    - https://www.feishu.cn/chat/ou_xxxxxxxxxxxx (single chat)
    
    Args:
        url: Feishu chat URL
        
    Returns:
        chat_id (e.g., 'oc_xxxxxxxxxxxx') or None if extraction fails
    """
    if not url:
        return None
    
    # Pattern to match chat_id in URL
    patterns = [
        r'feishu\.cn/chat/([a-z]+_[a-zA-Z0-9]+)',  # www.feishu.cn or feishu.cn
        r'larksuite\.com/chat/([a-z]+_[a-zA-Z0-9]+)',  # Lark
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            chat_id = match.group(1)
            logger.info(f"Extracted chat_id '{chat_id}' from URL")
            return chat_id
    
    logger.warning(f"Failed to extract chat_id from URL: {url}")
    return None


def create_notifier_from_config() -> Optional[FeishuNotifier]:
    """
    Create Feishu notifier from OpenClaw config.
    Reads the fall-detection account credentials from openclaw2.json.
    
    Returns:
        FeishuNotifier instance or None if config not found
    """
    import json
    
    config_paths = [
        Path.home() / ".openclaw" / "openclaw2.json",
        Path.home() / ".openclaw" / "openclaw.json",
    ]
    
    for config_path in config_paths:
        if not config_path.exists():
            continue
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Look for fall-detection account
            accounts = config.get("channels", {}).get("feishu", {}).get("accounts", {})
            fall_detection = accounts.get("fall-detection", {})
            
            app_id = fall_detection.get("appId")
            app_secret = fall_detection.get("appSecret")
            domain = fall_detection.get("domain", "feishu")
            
            if app_id and app_secret:
                logger.info(f"Loaded Feishu config from {config_path}")
                return FeishuNotifier(app_id, app_secret, domain)
            
        except Exception as e:
            logger.warning(f"Failed to read config from {config_path}: {e}")
    
    logger.error("Feishu fall-detection account not found in config")
    return None


def send_webhook_alarm(
    webhook_url: str,
    alarm: Dict[str, Any],
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None,
    app_id: str = "",
    app_secret: str = "",
) -> bool:
    """
    Send fall alarm to Feishu using webhook.
    
    Args:
        webhook_url: Feishu webhook URL (e.g., https://open.feishu.cn/open-apis/bot/v2/hook/xxx)
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        app_id: Optional Feishu self-built app ID. When provided together with
            app_secret, the posture image is uploaded via OpenAPI and embedded
            INLINE inside the interactive card via image_key.
        app_secret: Paired app secret for OpenAPI image upload.
        
    Returns:
        True if sent successfully

    Image rendering strategy for the posture reference image:
      1. If app_id + app_secret are provided, upload via Feishu OpenAPI and embed
         inline using the img element of an interactive card (best UX).
      2. Otherwise, upload to sm.ms image host and display a clickable URL in
         a text card.
      3. If both fail, show the local file path as plain text.
    """
    import requests
    
    # Build alarm message
    fall_type = alarm.get("fall_type", "unknown")
    confidence = alarm.get("confidence", 0)
    reason = alarm.get("reason", "Unknown")
    camera_name = alarm.get("camera_name")

    # Format fall type for display
    fall_type_map = {
        "active_falling": "🔄 主动跌倒",
        "fallen_posture": "📍 倒地姿态",
        "unknown": "⚠️ 未知类型"
    }
    fall_type_cn = fall_type_map.get(fall_type, f"⚠️ {fall_type}")

    # Format confidence
    confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"

    # --- Attempt to get a renderable image_key ---
    image_key = ""
    posture_url = ""
    if posture_image_path and os.path.isfile(posture_image_path):
        if app_id and app_secret:
            image_key = _feishu_upload_image(app_id, app_secret, posture_image_path)
        if not image_key:
            posture_url = _upload_image_to_imghost(posture_image_path)

    if image_key:
        posture_md = "(见下方图片)"
    elif posture_url:
        posture_md = f"[查看跌倒姿态参考图]({posture_url})"
    elif posture_image_path:
        posture_md = f"`{posture_image_path}`"
    else:
        posture_md = "-"

    # Camera identity line (omitted when not provided)
    camera_line = f"\n📷 摄像头：{camera_name}" if camera_name else ""
    clip_line = f"\n🎬 视频：`{clip_path}`" if clip_path else ""

    content_md = (
        f"🚨 **跌倒报警**{camera_line}\n\n"
        f"**类型**：{fall_type_cn}\n"
        f"**置信度**：{confidence_display}\n"
        f"**原因**：{reason[:100]}\n"
        f"**时间**：{time.strftime('%Y-%m-%d %H:%M:%S')}"
        f"{clip_line}\n"
        f"**姿态参考图**：{posture_md}"
    )

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": content_md}},
    ]
    if image_key:
        elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {"tag": "plain_text", "content": "跌倒姿态参考图"},
        })

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "🚨 跌倒报警"},
                "template": "red",
            },
            "elements": elements,
        },
    }

    try:
        resp = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("StatusCode") == 0 or data.get("code") == 0 or data.get("Extra") == "":
            logger.info(f"Feishu webhook alarm sent successfully (image_key={'yes' if image_key else 'no'})")
            return True
        else:
            logger.error(f"Feishu webhook failed: {data}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send Feishu webhook alarm: {e}")
        return False


# Convenience function for direct use
def send_fall_alarm(
    chat_id: Optional[str] = None,
    chat_url: Optional[str] = None,
    webhook_url: Optional[str] = None,
    alarm: Optional[Dict[str, Any]] = None,
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None,
    app_id: str = "",
    app_secret: str = "",
) -> bool:
    """
    Send fall alarm to Feishu.
    
    Args:
        chat_id: Target Feishu chat ID (e.g., 'oc_xxxxxxxxxxxx')
        chat_url: Feishu chat URL (auto-extracts chat_id)
        webhook_url: Feishu webhook URL (e.g., https://open.feishu.cn/open-apis/bot/v2/hook/xxx)
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        app_id: Optional Feishu self-built app ID (enables inline image in webhook card)
        app_secret: Paired app secret
        
    Returns:
        True if sent successfully
        
    Priority:
        1. If webhook_url is provided, use webhook (simplest)
        2. If chat_id is provided, use API
        3. If chat_url is provided, extract chat_id from URL
    """
    # Webhook mode (priority 1)
    if webhook_url:
        logger.info(f"Using webhook URL: {webhook_url[:50]}...")
        if not alarm:
            alarm = {"alarm": True, "type": "test", "reason": "Test message"}
        return send_webhook_alarm(
            webhook_url, alarm, clip_path, posture_image_path,
            app_id=app_id, app_secret=app_secret,
        )
    
    # API mode (priority 2 & 3)
    notifier = create_notifier_from_config()
    if not notifier:
        logger.error("Failed to create Feishu notifier")
        return False
    
    # Determine target chat_id
    target_chat_id = None
    
    if chat_id:
        target_chat_id = chat_id
        logger.info(f"Using direct chat_id: {target_chat_id}")
    elif chat_url:
        target_chat_id = extract_chat_id_from_url(chat_url)
        if not target_chat_id:
            logger.error("Failed to extract chat_id from URL")
            return False
    else:
        logger.error("Either webhook_url, chat_id, or chat_url must be provided")
        return False
    
    if not alarm:
        alarm = {"alarm": True, "type": "test", "reason": "Test message"}
    
    return notifier.send_alarm(target_chat_id, alarm, clip_path, posture_image_path)
