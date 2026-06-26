"""
DingTalk (钉钉) Integration Skill for OpenClaw

Provides capabilities to:
- Send messages to DingTalk chats
- Create group chats
- Manage DingTalk workflows
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
DINGTALK_APP_ID = os.getenv("DINGTALK_APP_ID", "")
DINGTALK_APP_SECRET = os.getenv("DINGTALK_APP_SECRET", "")
DINGTALK_AGENT_ID = os.getenv("DINGTALK_AGENT_ID", "")

# DingTalk API endpoints
BASE_URL = "https://oapi.dingtalk.com"


class DingTalkClient:
    """DingTalk API Client"""

    def __init__(self, app_id: str, app_secret: str, agent_id: str = ""):
        self.app_id = app_id
        self.app_secret = app_secret
        self.agent_id = agent_id
        self._token = None
        self._token_expires = 0

    def _get_timestamp(self) -> str:
        return str(int(time.time() * 1000))

    def sign(self, timestamp: str) -> str:
        """Generate signature for DingTalk API authentication"""
        string_to_sign = f"{timestamp}\n{self.app_secret}"
        hmac_sha256 = hmac.new(
            self.app_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        )
        return hmac_sha256.hexdigest()

    def get_token(self, force_refresh: bool = False) -> Optional[str]:
        """Get access token"""
        if not force_refresh and self._token and time.time() < self._token_expires - 300:
            return self._token

        if not requests:
            return None

        try:
            response = requests.get(
                f"{BASE_URL}/gettoken",
                params={"appkey": self.app_id, "appsecret": self.app_secret},
                timeout=10
            )
            data = response.json()

            if data.get("errcode") == 0:
                self._token = data["access_token"]
                self._token_expires = data.get("expire_in", 7200) + time.time()
                return self._token
            else:
                print(f"DingTalk auth error: {data}")
                return None
        except Exception as e:
            print(f"DingTalk request error: {e}")
            return None

    def send_message(self, user_id: str, message: str, msg_type: str = "text") -> Dict[str, Any]:
        """Send message to a user"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        headers = {"Content-Type": "application/json"}

        if msg_type == "text":
            msg_body = {
                "agent_id": self.agent_id,
                "userid": user_id,
                "msgtype": "text",
                "text": {"content": message}
            }
        else:
            # Markdown message
            msg_body = {
                "agent_id": self.agent_id,
                "userid": user_id,
                "msgtype": "markdown",
                "markdown": {"title": "Notification", "text": message}
            }

        try:
            response = requests.post(
                f"{BASE_URL}/topapi/message/corpconversation_asyncsend_v2",
                params={"access_token": token},
                headers=headers,
                json=msg_body,
                timeout=10
            )
            data = response.json()

            if data.get("errcode") == 0:
                return {"success": True, "task_id": data.get("task_id")}
            else:
                return {"success": False, "error": data.get("errmsg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_chat(self, name: str, user_ids: List[str] = None) -> Dict[str, Any]:
        """Create a new group chat"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        headers = {"Content-Type": "application/json"}

        chat_data = {
            "name": name,
            "owner": user_ids[0] if user_ids else "",
            "useridlist": user_ids or []
        }

        try:
            response = requests.post(
                f"{BASE_URL}/topapi/chat/create",
                params={"access_token": token},
                headers=headers,
                json=chat_data,
                timeout=10
            )
            data = response.json()

            if data.get("errcode") == 0:
                return {"success": True, "chat_id": data["chatid"]}
            else:
                return {"success": False, "error": data.get("errmsg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_chats(self) -> Dict[str, Any]:
        """List all accessible chats"""
        token = self.get_token()
        if not token:
            return {"success": False, "error": "Failed to get access token"}

        if not requests:
            return {"success": False, "error": "requests library not available"}

        try:
            response = requests.get(
                f"{BASE_URL}/topapi/chat/list",
                params={"access_token": token},
                timeout=10
            )
            data = response.json()

            if data.get("errcode") == 0:
                chats = data.get("result", [])
                return {"success": True, "chats": chats}
            else:
                return {"success": False, "error": data.get("errmsg", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global client instance
_client = None


def _get_client() -> DingTalkClient:
    """Get or create DingTalk client"""
    global _client
    if not _client:
        if not DINGTALK_APP_ID or not DINGTALK_APP_SECRET:
            print("Warning: DINGTALK_APP_ID and DINGTALK_APP_SECRET not configured")
            return None
        _client = DingTalkClient(DINGTALK_APP_ID, DINGTALK_APP_SECRET, DINGTALK_AGENT_ID)
    return _client


async def dingtalk_send_message(user_id: str, message: str, msg_type: str = "text") -> Dict[str, Any]:
    """
    Send a text or markdown message to a DingTalk user.

    Args:
        user_id: The user ID to send message to
        message: Message content
        msg_type: Message type, text or markdown

    Returns:
        Dictionary with success status and details
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "DingTalk not configured. Set DINGTALK_APP_ID and DINGTALK_APP_SECRET."}

    # Run sync code in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: client.send_message(user_id, message, msg_type)
    )
    return result


async def dingtalk_create_chat(name: str, user_ids: List[str] = None) -> Dict[str, Any]:
    """
    Create a new DingTalk group chat.

    Args:
        name: Chat group name
        user_ids: Optional user IDs to add

    Returns:
        Dictionary with success status and chat_id
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "DingTalk not configured"}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: client.create_chat(name, user_ids)
    )
    return result


async def dingtalk_list_chats() -> Dict[str, Any]:
    """
    List all accessible DingTalk chats.

    Returns:
        Dictionary with success status and chat list
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "DingTalk not configured"}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, client.list_chats)
    return result


async def dingtalk_get_token() -> Dict[str, Any]:
    """
    Get DingTalk access token.

    Returns:
        Dictionary with token info
    """
    client = _get_client()
    if not client:
        return {"success": False, "error": "DingTalk not configured"}

    token = client.get_token(force_refresh=True)
    if token:
        return {"success": True, "token": token[:20] + "..."}
    else:
        return {"success": False, "error": "Failed to get token"}


# Tool definitions for OpenClaw
TOOLS = [
    {
        "name": "dingtalk_send_message",
        "description": "Send a text or markdown message to a DingTalk user",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user ID to send message to"},
                "message": {"type": "string", "description": "Message content"},
                "msg_type": {"type": "string", "enum": ["text", "markdown"], "description": "Message type"}
            },
            "required": ["user_id", "message"]
        }
    },
    {
        "name": "dingtalk_create_chat",
        "description": "Create a new DingTalk group chat",
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
        "name": "dingtalk_list_chats",
        "description": "List all accessible DingTalk chats"
    },
    {
        "name": "dingtalk_get_token",
        "description": "Get DingTalk access token"
    }
]


if __name__ == "__main__":
    # Test the module
    print("DingTalk Integration Skill loaded")
    print(f"Configured: {bool(DINGTALK_APP_ID and DINGTALK_APP_SECRET)}")