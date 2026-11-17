"""
WeChat API wrapper — token, image upload, material upload.
"""

import time
import mimetypes
import requests
from pathlib import Path
from dataclasses import dataclass

_token_cache: dict = {}


@dataclass
class TokenResult:
    access_token: str
    expires_at: float


def get_access_token(appid: str, secret: str, force_refresh: bool = False) -> str:
    """Get access_token with caching (5 min buffer)."""
    now = time.time()
    if not force_refresh and appid in _token_cache:
        cached: TokenResult = _token_cache[appid]
        if now < cached.expires_at:
            return cached.access_token

    resp = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": appid,
            "secret": secret,
        },
    )
    data = resp.json()
    if "access_token" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise ValueError(f"WeChat API error: errcode={errcode}, errmsg={errmsg}")

    access_token = data["access_token"]
    expires_in = data.get("expires_in", 7200)
    _token_cache[appid] = TokenResult(
        access_token=access_token,
        expires_at=now + expires_in - 300,
    )
    return access_token


def _guess_content_type(file_path: str) -> str:
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def upload_image(access_token: str, image_path: str) -> str:
    """Upload image for article content. Returns mmbiz URL."""
    path = Path(image_path)
    content_type = _guess_content_type(image_path)
    with open(path, "rb") as f:
        resp = requests.post(
            "https://api.weixin.qq.com/cgi-bin/media/uploadimg",
            params={"access_token": access_token},
            files={"media": (path.name, f, content_type)},
        )
    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"upload_image: non-JSON response (HTTP {resp.status_code}): {resp.text[:200]}")
    if "url" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise ValueError(f"upload_image error: errcode={errcode}, errmsg={errmsg}")
    return data["url"]


def upload_thumb(access_token: str, image_path: str) -> str:
    """Upload cover image as permanent material. Returns media_id."""
    path = Path(image_path)
    content_type = _guess_content_type(image_path)
    with open(path, "rb") as f:
        resp = requests.post(
            "https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={"access_token": access_token, "type": "image"},
            files={"media": (path.name, f, content_type)},
        )
    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"upload_thumb: non-JSON response (HTTP {resp.status_code}): {resp.text[:200]}")
    if "media_id" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise ValueError(f"upload_thumb error: errcode={errcode}, errmsg={errmsg}")
    return data["media_id"]


def delete_draft(access_token: str, media_id: str) -> dict:
    """Delete a draft by media_id."""
    import json
    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/delete",
        params={"access_token": access_token},
        data=json.dumps({"media_id": media_id}).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        return resp.json()
    except Exception:
        # Some responses are empty or non-JSON; treat as success if status is 200
        if resp.status_code == 200:
            return {"errcode": 0, "errmsg": "ok (empty response)"}
        return {"errcode": -1, "errmsg": f"HTTP {resp.status_code}: {resp.text[:200]}"}
