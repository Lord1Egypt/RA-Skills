"""
Feishu (Lark) API helpers: auth, upload OPUS, send native voice message.
Zero external dependencies — uses only urllib.request.
"""
from __future__ import annotations

import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _post_json(url: str, payload: dict, headers: dict | None = None, timeout: int = 30) -> dict:
    """POST JSON body, return parsed JSON response."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    hdrs = {"Content-Type": "application/json; charset=utf-8"}
    if headers:
        hdrs.update(headers)
    req = Request(url, data=body, headers=hdrs, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu API error (HTTP {exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Feishu API network error: {exc.reason}") from exc


def _get_json(url: str, headers: dict | None = None, timeout: int = 30) -> dict:
    """GET request, return parsed JSON response."""
    req = Request(url, headers=headers or {}, method="GET")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu API error (HTTP {exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Feishu API network error: {exc.reason}") from exc


def _multipart_upload(url: str, fields: dict, file_field: str, file_path: Path,
                      file_name: str, headers: dict | None = None, timeout: int = 120) -> dict:
    """Multipart form-data upload using only urllib."""
    boundary = uuid.uuid4().hex
    content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    body_parts = []
    for key, value in fields.items():
        body_parts.append(
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"{key}\"\r\n\r\n"
            f"{value}\r\n".encode("utf-8")
        )

    file_data = file_path.read_bytes()
    body_parts.append(
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"{file_field}\"; filename=\"{file_name}\"\r\n"
        f"Content-Type: {content_type}\r\n\r\n".encode("utf-8")
    )
    body_parts.append(file_data)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    body = b"".join(body_parts)
    hdrs = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    if headers:
        hdrs.update(headers)

    req = Request(url, data=body, headers=hdrs, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu upload error (HTTP {exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Feishu upload network error: {exc.reason}") from exc


def get_tenant_access_token() -> str:
    """Obtain Feishu tenant_access_token using App ID / App Secret."""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError(
            "FEISHU_APP_ID or FEISHU_APP_SECRET not set.\n"
            "\n"
            "To fix this:\n"
            "  1. Go to https://open.feishu.cn/app and create an app\n"
            "  2. Copy App ID and App Secret\n"
            "  3. Add to your .env file:\n"
            "     FEISHU_APP_ID=your_app_id\n"
            "     FEISHU_APP_SECRET=your_app_secret"
        )
    payload = _post_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if payload.get("code") != 0:
        raise RuntimeError(f"Failed to get tenant_access_token: {json.dumps(payload, ensure_ascii=False)}")
    return payload["tenant_access_token"]


def upload_opus_file(opus_path: str, file_name: str = "reply.opus") -> Dict[str, Any]:
    """Upload OPUS file to Feishu, return {"file_key": ...}."""
    token = get_tenant_access_token()
    path = Path(opus_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"OPUS file not found: {path}")

    payload = _multipart_upload(
        "https://open.feishu.cn/open-apis/im/v1/files",
        fields={"file_type": "opus", "file_name": file_name},
        file_field="file",
        file_path=path,
        file_name=file_name,
        headers={"Authorization": f"Bearer {token}"},
    )
    if payload.get("code") != 0:
        raise RuntimeError(f"Feishu file upload failed: {json.dumps(payload, ensure_ascii=False)}")
    file_key = (payload.get("data") or {}).get("file_key")
    if not file_key:
        raise RuntimeError(f"No file_key in upload response: {json.dumps(payload, ensure_ascii=False)}")
    return {"file_key": file_key, "raw": payload}


def list_chats() -> list:
    """List all chats the bot has joined. Returns list of {chat_id, name, chat_mode}."""
    token = get_tenant_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    chats = []
    page_token = ""
    while True:
        url = "https://open.feishu.cn/open-apis/im/v1/chats?page_size=50"
        if page_token:
            url += f"&page_token={page_token}"
        payload = _get_json(url, headers=headers)
        if payload.get("code") != 0:
            code = payload.get("code", "?")
            msg = payload.get("msg", "") or payload.get("message", "")
            raise RuntimeError(
                f"Failed to list chats (code={code}): {msg}\n"
                f"Hint: make sure the Feishu app has 'im:chat:readonly' permission.\n"
                f"Go to https://open.feishu.cn/app → your app → Permissions → add 'im:chat:readonly'"
            )
        for item in (payload.get("data") or {}).get("items", []):
            chats.append({
                "chat_id": item.get("chat_id", ""),
                "name": item.get("name", "(unnamed)"),
                "chat_mode": item.get("chat_mode", ""),
                "description": item.get("description", ""),
            })
        if not (payload.get("data") or {}).get("has_more"):
            break
        page_token = (payload.get("data") or {}).get("page_token", "")
    return chats


def send_audio_message(chat_id: str, file_key: str) -> Dict[str, Any]:
    """Send a native voice message (audio bar) to a Feishu chat."""
    token = get_tenant_access_token()
    payload = _post_json(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        {
            "receive_id": chat_id,
            "msg_type": "audio",
            "content": json.dumps({"file_key": file_key}, ensure_ascii=False),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    if payload.get("code") != 0:
        raise RuntimeError(f"Feishu send audio failed: {json.dumps(payload, ensure_ascii=False)}")
    return payload
