import os
import asyncio
from typing import Optional, Dict, Any

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")


class GmailClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages.send"
        import base64
        import json
        msg = f"From: me\r\nTo: {to}\r\nSubject: {subject}\r\n\r\n{body}"
        encoded = base64.urlsafe_b64encode(msg.encode("utf-8")).decode("utf-8")
        payload = {"raw": encoded}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
            if resp.status_code == 200:
                return {"success": True, "message_id": resp.json().get("id")}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_messages(self, max_results: int = 10) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.get(url, params={"maxResults": max_results}, timeout=30))
            if resp.status_code == 200:
                return {"success": True, "messages": resp.json().get("messages", [])}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_label(self, name: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://gmail.googleapis.com/gmail/v1/users/me/labels"
        payload = {"name": name, "labelListVisibility": "labelShow", "messageListVisibility": "labelShow"}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
            if resp.status_code == 200:
                return {"success": True, "label_id": resp.json().get("id")}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}


_client = None

def _get_client():
    global _client
    if not _client and GMAIL_CLIENT_ID:
        _client = GmailClient(GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET)
    return _client


async def gmail_send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "GMAIL_CLIENT_ID not configured"}
    return await client.send_email(to, subject, body)


async def gmail_list_messages(max_results: int = 10) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "GMAIL_CLIENT_ID not configured"}
    return await client.list_messages(max_results)


async def gmail_create_label(name: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "GMAIL_CLIENT_ID not configured"}
    return await client.create_label(name)


TOOLS = [
    {"name": "gmail_send_email", "description": "Send an email", "input_schema": {"type": "object", "properties": {"to": {"type": "string", "description": "Recipient email"}, "subject": {"type": "string", "description": "Email subject"}, "body": {"type": "string", "description": "Email body"}}, "required": ["to", "subject", "body"]}},
    {"name": "gmail_list_messages", "description": "List recent emails", "input_schema": {"type": "object", "properties": {"max_results": {"type": "integer", "description": "Max results"}}}},
    {"name": "gmail_create_label", "description": "Create a label", "input_schema": {"type": "object", "properties": {"name": {"type": "string", "description": "Label name"}}, "required": ["name"]}},
]


if __name__ == "__main__":
    print("Gmail Skill loaded")