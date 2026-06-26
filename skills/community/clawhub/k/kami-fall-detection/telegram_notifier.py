"""
Telegram Notification Module for Fall Detection
Sends alarm notifications to Telegram using Bot API.

Supports:
- Direct chat_id configuration
- Webhook-style direct API calls
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Telegram API endpoint
TELEGRAM_API_URL = "https://api.telegram.org/bot"


class TelegramNotifier:
    """Send fall alarm notifications to Telegram."""
    
    def __init__(self, bot_token: str):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token (e.g., 123456:ABC-DEF1234...)
        """
        self.bot_token = bot_token
        self.api_url = f"{TELEGRAM_API_URL}{bot_token}"
    
    def send_text_message(self, chat_id: str, text: str) -> bool:
        """
        Send a text message to a Telegram chat.
        
        Args:
            chat_id: Telegram chat ID (numeric string or @username)
            text: Message text (supports Markdown)
            
        Returns:
            True if sent successfully, False otherwise
        """
        import requests
        
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            
            resp = requests.post(
                f"{self.api_url}/sendMessage",
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("ok"):
                logger.error(f"Telegram send failed: {data.get('description', 'unknown error')}")
                return False
            
            logger.info(f"Telegram message sent to {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def send_alarm(self, chat_id: str, alarm: Dict[str, Any], clip_path: Optional[str] = None, posture_image_path: Optional[str] = None) -> bool:
        """
        Send a formatted fall alarm notification.
        
        Args:
            chat_id: Target Telegram chat ID
            alarm: Alarm data from fall detection
            clip_path: Optional path to alarm video clip
            posture_image_path: Optional path to fall posture reference image
            
        Returns:
            True if sent successfully
        """
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
        camera_line = f"\n📷 *Camera*: {camera_name}" if camera_name else ""

        # Build message (Markdown format)
        text = f"""🚨 *跌倒报警*{camera_line}

{fall_type_cn}
置信度：{confidence_display}
原因：{reason[:100]}

时间：{time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        if clip_path:
            text += f"\n视频：`{clip_path}`"
        
        # Send image first if provided, then text
        if posture_image_path and os.path.isfile(posture_image_path):
            self.send_image(chat_id, posture_image_path, text)
            return True
        
        return self.send_text_message(chat_id, text)
    
    def send_image(self, chat_id: str, image_path: str, caption: Optional[str] = None) -> bool:
        """
        Send an image to Telegram chat.
        
        Args:
            chat_id: Target chat ID
            image_path: Path to image file
            caption: Optional caption for the image
            
        Returns:
            True if sent successfully
        """
        import requests
        
        try:
            url = f"{self.api_url}/sendPhoto"
            
            with open(image_path, 'rb') as f:
                files = {'photo': f}
                data = {
                    'chat_id': chat_id,
                    'parse_mode': 'Markdown'
                }
                if caption:
                    data['caption'] = caption
                
                resp = requests.post(url, files=files, data=data, timeout=30)
                resp.raise_for_status()
                result = resp.json()
                
                if not result.get("ok"):
                    logger.error(f"Telegram image send failed: {result.get('description', 'unknown error')}")
                    return False
                
                logger.info(f"Telegram image sent to {chat_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send Telegram image: {e}")
            return False


def get_bot_token_from_config() -> Optional[str]:
    """
    Get Telegram bot token from OpenClaw config.
    
    Returns:
        Bot token or None if not found
    """
    config_paths = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path.home() / ".openclaw" / "openclaw2.json",
    ]
    
    for config_path in config_paths:
        if not config_path.exists():
            continue
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Check for telegram channel config
            telegram_config = config.get("channels", {}).get("telegram", {})
            
            # Direct token
            token = telegram_config.get("token")
            if token and isinstance(token, str):
                logger.info(f"Loaded Telegram token from {config_path}")
                return token
            
            # SecretRef token
            if isinstance(token, dict):
                source = token.get("source")
                if source == "env":
                    import os
                    env_id = token.get("id")
                    env_token = os.environ.get(env_id)
                    if env_token:
                        logger.info(f"Loaded Telegram token from env {env_id}")
                        return env_token
            
        except Exception as e:
            logger.warning(f"Failed to read config from {config_path}: {e}")
    
    return None


def send_webhook_alarm(
    bot_token: str,
    chat_id: str,
    alarm: Dict[str, Any],
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None
) -> bool:
    """
    Send fall alarm to Telegram using Bot API (webhook-style).
    
    Args:
        bot_token: Telegram bot token
        chat_id: Target Telegram chat ID (numeric user ID)
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        
    Returns:
        True if sent successfully
    """
    notifier = TelegramNotifier(bot_token)
    return notifier.send_alarm(chat_id, alarm, clip_path, posture_image_path)


def send_fall_alarm(
    chat_id: Optional[str] = None,
    bot_token: Optional[str] = None,
    alarm: Optional[Dict[str, Any]] = None,
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None
) -> bool:
    """
    Send fall alarm to Telegram.
    
    Args:
        chat_id: Target Telegram chat ID (e.g., '123456789')
        bot_token: Telegram bot token (auto-loads from config if not provided)
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        
    Returns:
        True if sent successfully
    """
    # Get bot token from config if not provided
    if not bot_token:
        bot_token = get_bot_token_from_config()
        if not bot_token:
            logger.error("Telegram bot token not found in config")
            return False
    
    # Validate chat_id
    if not chat_id:
        logger.error("chat_id is required for Telegram notification")
        return False
    
    if not alarm:
        alarm = {"alarm": True, "type": "test", "reason": "Test message"}
    
    return send_webhook_alarm(bot_token, chat_id, alarm, clip_path, posture_image_path)


# Test function
if __name__ == "__main__":
    # Test notification
    test_alarm = {
        "alarm": True,
        "type": "fall",
        "fall_type": "fallen_posture",
        "confidence": 0.95,
        "reason": "Test alarm - Person detected lying on floor"
    }
    
    # Load token from config
    token = get_bot_token_from_config()
    if token:
        print(f"Testing Telegram notification with token: {token[:20]}...")
        # Replace with your actual chat ID for testing
        result = send_fall_alarm(
            chat_id="YOUR_CHAT_ID",  # Replace with your Telegram user ID
            bot_token=token,
            alarm=test_alarm
        )
        print(f"Result: {'Success' if result else 'Failed'}")
    else:
        print("Telegram token not found in config")
