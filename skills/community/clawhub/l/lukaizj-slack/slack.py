import os
import asyncio
from typing import Optional, Dict, Any, List

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")


class SlackClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://slack.com/api/chat.postMessage"
        payload = {"channel": channel, "text": text}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json=payload, timeout=30))
            data = resp.json()
            if data.get("ok"):
                return {"success": True, "ts": data.get("ts")}
            return {"success": False, "error": data.get("error", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_channels(self) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://slack.com/api/conversations.list"
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.get(url, headers=self.headers, timeout=30))
            data = resp.json()
            if data.get("ok"):
                return {"success": True, "channels": data.get("channels", [])}
            return {"success": False, "error": data.get("error", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_channel(self, name: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://slack.com/api/conversations.create"
        payload = {"name": name, "is_private": False}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json=payload, timeout=30))
            data = resp.json()
            if data.get("ok"):
                return {"success": True, "channel_id": data.get("channel", {}).get("id")}
            return {"success": False, "error": data.get("error", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}


_client = None

def _get_client():
    global _client
    if not _client and SLACK_BOT_TOKEN:
        _client = SlackClient(SLACK_BOT_TOKEN)
    return _client


async def slack_send_message(channel: str, text: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "SLACK_BOT_TOKEN not configured"}
    return await client.send_message(channel, text)


async def slack_list_channels() -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "SLACK_BOT_TOKEN not configured"}
    return await client.list_channels()


async def slack_create_channel(name: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "SLACK_BOT_TOKEN not configured"}
    return await client.create_channel(name)


TOOLS = [
    {"name": "slack_send_message", "description": "Send a message to Slack channel", "input_schema": {"type": "object", "properties": {"channel": {"type": "string", "description": "Channel ID or name"}, "text": {"type": "string", "description": "Message text"}}, "required": ["channel", "text"]}},
    {"name": "slack_list_channels", "description": "List all Slack channels"},
    {"name": "slack_create_channel", "description": "Create a new Slack channel", "input_schema": {"type": "object", "properties": {"name": {"type": "string", "description": "Channel name"}}, "required": ["name"]}},
]


if __name__ == "__main__":
    print("Slack Skill loaded")