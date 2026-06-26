"""
Feishu (飞书) Integration Skill for OpenClaw

Provides capabilities to:
- Send messages to Feishu chats
- Create group chats
- List accessible chats
- Manage feishu workflows
"""

import os
import json
import hashlib
import hmac
import time
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    requests = None

# Environment configuration
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN", "")

# Feishu API endpoints
BASE_URL = "https://open.feishu.cn/open-apis"
AUTH_URL = f"{BASE_URL}/authen/v1"
MESSAGE_URL = f"{BASE_URL}/im/v1"
CHAT_URL = f"{BASE_URL}/im/v1/chats"


class FeishuClient:
    """Feishu API Client"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None
        self._token_expires = 0

    def _get_timestamp(self) -> str:
        return str(int(time.time()))

    def _sign(self, timestamp: str) -> str:
        """Generate signature for Feishu API authentication"""
        string_to_sign = f"{timestamp}{self.app_secret}"
        hmac_sha256 = hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        )
        return hmac_sha256.hexdigest()

    def get_token(self, force_refresh: bool = False) -> Optional[str]:
        """Get tenant access token"""
        if not force_refresh and self._token and time.time() < self._token_expires - 300:
            return self._token

        if not requests:
            return None

        timestamp = self._get_timestamp()
        sign = self._sign(timestamp)

        headers = {
            "Content-Type": "application/json",
            "x-llb-corp-id": self.app_id,
            "x-llb-timestamp": timestamp,
            "x-llb-sign": sign
        }

        try:
            response = requests.post(
                f"{AUTH_URL}/access_token",
                headers=headers,
                json={"grant_type": "client_credentials", "app_id": self.app_id, "app_secret": self.app_secret},
                timeout=10
            )
            data = response.json()

            if data.get("code") == 0:
                self._token = data["data"]["tenant_access_token"]
                self._token_expires = data["data"]["expire"] + time.time()
                return self._token
            else:
                print(f"Feishu auth error: {data}")
                return None
        except Exception as e:
            print(f"Feishu request error: {e}")
            return None

    def send_message(self, chat_id: str, message: str, msg_type: str = "text") -> Dict[str, Any]:
        """Send message to a chat"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        if msg_type == "text":
            msg_body = {
                "msg_type": "text",
                "content": json.dumps({"text": message})
            }
        else:
            # Card message
            msg_body = {
                "msg_type": "interactive",
                "content": json.dumps({
                    "config": {"wide_screen_mode": True},
                    "header": {"title": {"tag": "plain_text", "content": "Notification"}},
                    "elements": [
                        {"tag": "markdown", "content": message}
                    ]
                })
            }

        try:
            response = requests.post(
                f"{MESSAGE_URL}/messages?receive_id_type=chat_id",
                headers=headers,
                json={"receive_id": chat_id, **msg_body},
                timeout=10
            )
            data = response.json()

            if data.get("code") == 0:
                return {"success": True, "message_id": data["data"]["message_id"]}
            else:
                return {"success": False, "error": data.get("msg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_chat(self, name: str, user_ids: List[str] = None) -> Dict[str, Any]:
        """Create a new group chat"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        chat_data = {
            "name": name,
            "user_id_list": user_ids or []
        }

        try:
            response = requests.post(
                CHAT_URL,
                headers=headers,
                json=chat_data,
                timeout=10
            )
            data = response.json()

            if data.get("code") == 0:
                return {"success": True, "chat_id": data["data"]["chat_id"]}
            else:
                return {"success": False, "error": data.get("msg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_chats(self) -> Dict[str, Any]:
        """List all accessible chats"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(
                CHAT_URL,
                headers=headers,
                timeout=10
            )
            data = response.json()

            if data.get("code") == 0:
                chats = data["data"]["items"]
                return {"success": True, "chats": chats}
            else:
                return {"success": False, "error": data.get("msg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global client instance
_client = None


def _get_client() -> FeishuClient:
    """Get or create Feishu client"""
    global _client
    if not _client:
        if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
            print("Warning: FEISHU_APP_ID and FEISHU_APP_SECRET not configured")
            return None
        _client = FeishuClient(FEISHU_APP_ID, FEISHU_APP_SECRET)
    return _client


async def feishu_send_message(chat_id: str, message: str, msg_type: str = "text") -> Dict[str, Any]:
    """
    Send a text or card message to a Feishu chat.

    Args:
        chat_id: The chat ID to send message to
        message: Message content
        msg_type: Message type, text or card

    Returns:
        Dictionary with success status and details
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "Feishu not configured. Set FEISHU_APP_ID and FEISHU_APP_SECRET."}

    # Run sync code in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: client.send_message(chat_id, message, msg_type)
    )
    return result


async def feishu_create_chat(name: str, user_ids: List[str] = None) -> Dict[str, Any]:
    """
    Create a new Feishu group chat.

    Args:
        name: Chat group name
        user_ids: Optional user IDs to add

    Returns:
        Dictionary with success status and chat_id
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "Feishu not configured"}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: client.create_chat(name, user_ids)
    )
    return result


async def feishu_list_chats() -> Dict[str, Any]:
    """
    List all accessible Feishu chats.

    Returns:
        Dictionary with success status and chat list
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "Feishu not configured"}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, client.list_chats)
    return result


async def feishu_get_token() -> Dict[str, Any]:
    """
    Get Feishu tenant access token.

    Returns:
        Dictionary with token info
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "Feishu not configured"}

    token = client.get_token(force_refresh=True)
    if token:
        return {"success": True, "token": token[:20] + "..."}
    else:
        return {"success": False, "error": "Failed to get token"}


# Tool definitions for OpenClaw
TOOLS = [
    {
        "name": "feishu_send_message",
        "description": "Send a text or card message to a Feishu chat",
        "input_schema": {
            "type": "object",
            "properties": {
                "chat_id": {"type": "string", "description": "The chat ID to send message to"},
                "message": {"type": "string", "description": "Message content"},
                "msg_type": {"type": "string", "enum": ["text", "card"], "description": "Message type"}
            },
            "required": ["chat_id", "message"]
        }
    },
    {
        "name": "feishu_create_chat",
        "description": "Create a new Feishu group chat",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Chat group name"},
                "user_ids": {"type": "array", "items": {"type": "string"}, "description": "User IDs to add"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "feishu_list_chats",
        "description": "List all accessible Feishu chats"
    },
    {
        "name": "feishu_get_token",
        "description": "Get Feishu tenant access token"
    }
]


if __name__ == "__main__":
    # Test the module
    print("Feishu Integration Skill loaded")
    print(f"Configured: {bool(FEISHU_APP_ID and FEISHU_APP_SECRET)}")