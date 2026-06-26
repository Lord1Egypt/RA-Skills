"""
Discord Notification Module for Fall Detection
Sends alarm notifications to Discord.

Supports:
- Webhook URL configuration (simplest method, push-only)
- Bot Token + Channel ID configuration (two-way capable)
- Rich embeds for formatted messages
- Optional video clip attachment
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Discord API endpoint (both domains are valid)
DISCORD_WEBHOOK_PREFIXES = [
    "https://discord.com/api/webhooks/",
    "https://discordapp.com/api/webhooks/",
]


class DiscordNotifier:
    """Send fall alarm notifications to Discord."""
    
    def __init__(self, webhook_url: str):
        """
        Initialize Discord notifier.
        
        Args:
            webhook_url: Discord webhook URL 
                (e.g., https://discord.com/api/webhooks/123456789/abcdefghijklmnop)
        """
        self.webhook_url = webhook_url
    
    def send_embed_message(
        self, 
        title: str, 
        description: str, 
        color: int = 0xFF0000,
        fields: Optional[list] = None,
        footer: Optional[str] = None
    ) -> bool:
        """
        Send a formatted embed message to Discord.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (RGB integer, e.g., 0xFF0000 for red)
            fields: Optional list of field dicts [{name, value, inline}]
            footer: Optional footer text
            
        Returns:
            True if sent successfully, False otherwise
        """
        import requests
        
        try:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }]
            }
            
            if fields:
                payload["embeds"][0]["fields"] = fields
            
            if footer:
                payload["embeds"][0]["footer"] = {"text": footer}
            
            resp = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            
            logger.info(f"Discord message sent to webhook")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord message: {e}")
            return False
    
    def send_alarm(
        self, 
        alarm: Dict[str, Any], 
        clip_path: Optional[str] = None,
        posture_image_path: Optional[str] = None
    ) -> bool:
        """
        Send a formatted fall alarm notification as an embed.
        
        Args:
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
            "active_falling": "🔄 Active Falling",
            "fallen_posture": "📍 Fallen Posture",
            "unknown": "⚠️ Unknown Type"
        }
        fall_type_cn = fall_type_map.get(fall_type, f"⚠️ {fall_type}")

        # Format confidence
        confidence_display = f"{confidence * 100:.0f}%" if confidence else "N/A"

        # Build embed fields
        fields = []
        if camera_name:
            fields.append({"name": "Camera", "value": camera_name, "inline": True})
        fields.extend([
            {"name": "Type", "value": fall_type_cn, "inline": True},
            {"name": "Confidence", "value": confidence_display, "inline": True},
            {"name": "Time", "value": time.strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
            {"name": "Reason", "value": reason[:200] or "Unknown", "inline": False},
        ])
        
        if clip_path:
            fields.append({
                "name": "Video Clip", 
                "value": f"`{clip_path}`", 
                "inline": False
            })
        
        # Send embed with image if provided
        if posture_image_path and os.path.isfile(posture_image_path):
            return self.send_embed_with_image(
                title="🚨 Fall Detection Alert",
                description="**A fall event has been detected!**",
                color=0xFF0000,  # Red
                fields=fields,
                footer="Kami Fall Detection System",
                image_path=posture_image_path
            )
        
        # Send embed with red color for alarm
        return self.send_embed_message(
            title="🚨 Fall Detection Alert",
            description="**A fall event has been detected!**",
            color=0xFF0000,  # Red
            fields=fields,
            footer="Kami Fall Detection System"
        )
    
    def send_embed_with_image(
        self,
        title: str,
        description: str,
        color: int = 0xFF0000,
        fields: Optional[list] = None,
        footer: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> bool:
        """
        Send an embed message with an attached image file.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (RGB integer)
            fields: Optional list of field dicts
            footer: Optional footer text
            image_path: Path to image file to attach
            
        Returns:
            True if sent successfully
        """
        import requests
        
        try:
            # Build payload
            payload = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }]
            }
            
            if fields:
                payload["embeds"][0]["fields"] = fields
            
            if footer:
                payload["embeds"][0]["footer"] = {"text": footer}
            
            # Send with file attachment
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'payload_json': json.dumps(payload)}
                
                resp = requests.post(
                    self.webhook_url,
                    files=files,
                    data=data,
                    timeout=30
                )
                resp.raise_for_status()
            
            logger.info(f"Discord message with image sent to webhook")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord image message: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify webhook works."""
        return self.send_embed_message(
            title="✅ Fall Detection - Test",
            description="Discord notifications are configured correctly!",
            color=0x00FF00,  # Green
            footer="Kami Fall Detection System"
        )


def validate_webhook_url(url: str) -> bool:
    """
    Validate Discord webhook URL format.
    
    Args:
        url: Webhook URL to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not url:
        return False
    
    # Basic format check - support both discord.com and discordapp.com
    matched_prefix = None
    for prefix in DISCORD_WEBHOOK_PREFIXES:
        if url.startswith(prefix):
            matched_prefix = prefix
            break
    
    if not matched_prefix:
        return False
    
    # Should have format: https://discord[app].com/api/webhooks/{webhook_id}/{token}
    parts = url.replace(matched_prefix, "").split("/")
    if len(parts) != 2:
        return False
    
    webhook_id, token = parts
    if not webhook_id or not token:
        return False
    
    return True


def send_webhook_alarm(
    webhook_url: str,
    alarm: Dict[str, Any],
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None
) -> bool:
    """
    Send fall alarm to Discord using webhook.
    
    Args:
        webhook_url: Discord webhook URL
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        
    Returns:
        True if sent successfully
    """
    if not validate_webhook_url(webhook_url):
        logger.error(f"Invalid Discord webhook URL format")
        return False
    
    notifier = DiscordNotifier(webhook_url)
    return notifier.send_alarm(alarm, clip_path, posture_image_path)


def send_test_notification(webhook_url: str) -> bool:
    """
    Send a test notification to verify Discord webhook.
    
    Args:
        webhook_url: Discord webhook URL
        
    Returns:
        True if sent successfully
    """
    if not validate_webhook_url(webhook_url):
        logger.error(f"Invalid Discord webhook URL format")
        return False
    
    notifier = DiscordNotifier(webhook_url)
    return notifier.send_test_message()


# Convenience function for direct use
def send_fall_alarm(
    webhook_url: Optional[str] = None,
    alarm: Optional[Dict[str, Any]] = None,
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None
) -> bool:
    """
    Send fall alarm to Discord.
    
    Args:
        webhook_url: Discord webhook URL
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        
    Returns:
        True if sent successfully
    """
    if not webhook_url:
        logger.error("Discord webhook_url is required")
        return False
    
    if not alarm:
        alarm = {"alarm": True, "type": "test", "reason": "Test message"}
    
    return send_webhook_alarm(webhook_url, alarm, clip_path, posture_image_path)


# ─────────────────────────────────────────────────────────────────────────────
# Discord Bot API Support (Two-Way Communication)
# ─────────────────────────────────────────────────────────────────────────────

DISCORD_API_BASE = "https://discord.com/api/v10"


class DiscordBotNotifier:
    """Send fall alarm notifications to Discord using Bot API."""
    
    def __init__(self, bot_token: str, channel_id: str):
        """
        Initialize Discord bot notifier.
        
        Args:
            bot_token: Discord bot token (e.g., MTUwNzI2MTY4MTQ1NjExOTgxMQ.G13TXv.xxx)
            channel_id: Discord channel ID (numeric string)
        """
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.api_base = DISCORD_API_BASE
        self.headers = {"Authorization": f"Bot {bot_token}"}
    
    def send_embed_message(
        self,
        title: str,
        description: str,
        color: int = 0xFF0000,
        fields: Optional[list] = None,
        footer: Optional[str] = None
    ) -> bool:
        """
        Send a formatted embed message to Discord channel via Bot API.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (RGB integer)
            fields: Optional list of field dicts
            footer: Optional footer text
            
        Returns:
            True if sent successfully, False otherwise
        """
        import requests
        
        try:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }]
            }
            
            if fields:
                payload["embeds"][0]["fields"] = fields
            
            if footer:
                payload["embeds"][0]["footer"] = {"text": footer}
            
            resp = requests.post(
                f"{self.api_base}/channels/{self.channel_id}/messages",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            resp.raise_for_status()
            
            logger.info(f"Discord bot message sent to channel {self.channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord bot message: {e}")
            return False
    
    def send_alarm(
        self,
        alarm: Dict[str, Any],
        clip_path: Optional[str] = None,
        posture_image_path: Optional[str] = None
    ) -> bool:
        """
        Send a formatted fall alarm notification via Bot API.
        
        Args:
            alarm: Alarm data dict
            clip_path: Optional path to alarm video clip
            posture_image_path: Optional path to fall posture reference image
            
        Returns:
            True if sent successfully
        """
        import requests
        
        fall_type = alarm.get("fall_type", "unknown")
        confidence = alarm.get("confidence", 0)
        reason = alarm.get("reason", "Unknown reason")
        timestamp = alarm.get("_ts", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        camera_name = alarm.get("camera_name")

        # Build embed fields
        fields = []
        if camera_name:
            fields.append({"name": "Camera", "value": camera_name, "inline": True})
        fields.extend([
            {"name": "Fall Type", "value": fall_type, "inline": True},
            {"name": "Confidence", "value": f"{confidence*100:.0f}%", "inline": True},
            {"name": "Time", "value": timestamp, "inline": False},
            {"name": "Details", "value": reason, "inline": False},
        ])
        
        if clip_path and Path(clip_path).exists():
            fields.append({
                "name": "Video Clip",
                "value": f"Saved: `{Path(clip_path).name}`",
                "inline": False
            })
        
        # Send via embed with image if provided
        if posture_image_path and os.path.isfile(posture_image_path):
            return self.send_embed_with_image(
                title="🚨 Fall Detected!",
                description="A fall event has been detected by the monitoring system.",
                color=0xFF0000,
                fields=fields,
                footer="Kami Fall Detection System",
                image_path=posture_image_path
            )
        
        # Send via embed
        return self.send_embed_message(
            title="🚨 Fall Detected!",
            description="A fall event has been detected by the monitoring system.",
            color=0xFF0000,
            fields=fields,
            footer="Kami Fall Detection System"
        )
    
    def send_embed_with_image(
        self,
        title: str,
        description: str,
        color: int = 0xFF0000,
        fields: Optional[list] = None,
        footer: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> bool:
        """
        Send an embed message with an attached image file via Bot API.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (RGB integer)
            fields: Optional list of field dicts
            footer: Optional footer text
            image_path: Path to image file to attach
            
        Returns:
            True if sent successfully
        """
        import requests
        
        try:
            # Build payload
            payload = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }]
            }
            
            if fields:
                payload["embeds"][0]["fields"] = fields
            
            if footer:
                payload["embeds"][0]["footer"] = {"text": footer}
            
            # Send with file attachment
            url = f"{DISCORD_API_BASE}/channels/{self.channel_id}/messages"
            
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'payload_json': json.dumps(payload)}
                
                resp = requests.post(
                    url,
                    headers=self.headers,
                    files=files,
                    data=data,
                    timeout=30
                )
                resp.raise_for_status()
            
            logger.info(f"Discord bot message with image sent to channel {self.channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord bot image message: {e}")
            return False


def send_fall_alarm_bot(
    bot_token: str,
    channel_id: str,
    alarm: Optional[Dict[str, Any]] = None,
    clip_path: Optional[str] = None,
    posture_image_path: Optional[str] = None
) -> bool:
    """
    Send fall alarm to Discord using Bot API.
    
    Args:
        bot_token: Discord bot token
        channel_id: Discord channel ID
        alarm: Alarm data from fall detection
        clip_path: Optional path to alarm video clip
        posture_image_path: Optional path to fall posture reference image
        
    Returns:
        True if sent successfully
    """
    if not bot_token or not channel_id:
        logger.error("Discord bot_token and channel_id are required")
        return False
    
    notifier = DiscordBotNotifier(bot_token, channel_id)
    
    if not alarm:
        alarm = {"alarm": True, "type": "test", "reason": "Test message"}
    
    return notifier.send_alarm(alarm, clip_path, posture_image_path)


def get_discord_notifier(config: dict):
    """
    Get appropriate Discord notifier based on config.
    Prefers bot API if available, falls back to webhook.
    
    Args:
        config: Configuration dict
        
    Returns:
        DiscordNotifier, DiscordBotNotifier, or None
    """
    bot_token = config.get("discord_bot_token")
    channel_id = config.get("discord_channel_id")
    webhook_url = config.get("discord_webhook_url")
    
    if bot_token and channel_id:
        logger.info("Using Discord Bot API for notifications")
        return DiscordBotNotifier(bot_token, channel_id)
    elif webhook_url:
        logger.info("Using Discord Webhook for notifications")
        return DiscordNotifier(webhook_url)
    else:
        logger.warning("No Discord notification method configured")
        return None


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
    
    # Replace with your actual credentials for testing
    test_webhook = "YOUR_DISCORD_WEBHOOK_URL"
    test_bot_token = "YOUR_BOT_TOKEN"
    test_channel_id = "YOUR_CHANNEL_ID"
    
    if test_webhook != "YOUR_DISCORD_WEBHOOK_URL":
        print(f"Testing Discord webhook notification...")
        result = send_fall_alarm(
            webhook_url=test_webhook,
            alarm=test_alarm
        )
        print(f"Webhook Result: {'Success' if result else 'Failed'}")
    
    if test_bot_token != "YOUR_BOT_TOKEN" and test_channel_id != "YOUR_CHANNEL_ID":
        print(f"Testing Discord bot notification...")
        result = send_fall_alarm_bot(
            bot_token=test_bot_token,
            channel_id=test_channel_id,
            alarm=test_alarm
        )
        print(f"Bot Result: {'Success' if result else 'Failed'}")
    
    if test_webhook == "YOUR_DISCORD_WEBHOOK_URL" and test_bot_token == "YOUR_BOT_TOKEN":
        print("Please set test credentials to run tests")
