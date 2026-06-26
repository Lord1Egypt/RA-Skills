import base64
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

BASE = "https://api.imgur.com/3"


def _auth_headers(access_token: Optional[str] = None, client_id: Optional[str] = None) -> Dict[str, str]:
    token = access_token or os.getenv("IMGUR_ACCESS_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    cid = client_id or os.getenv("IMGUR_CLIENT_ID")
    if not cid:
        raise RuntimeError(
            "Set IMGUR_CLIENT_ID (anonymous) or IMGUR_ACCESS_TOKEN (authenticated)."
        )
    return {"Authorization": f"Client-ID {cid}"}


def _unwrap(resp: requests.Response) -> Dict[str, Any]:
    try:
        body = resp.json()
    except ValueError:
        resp.raise_for_status()
        raise RuntimeError(f"Non-JSON response ({resp.status_code})")
    if not body.get("success", False):
        err = body.get("data", {}).get("error") or body.get("data") or body
        raise RuntimeError(f"Imgur API error ({resp.status_code}): {err}")
    return body.get("data", {})


def upload_image(
    source: str,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    album: Optional[str] = None,
    access_token: Optional[str] = None,
    client_id: Optional[str] = None,
    timeout: float = 60.0,
) -> Dict[str, Any]:
    headers = _auth_headers(access_token, client_id)
    data: Dict[str, Any] = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if album:
        data["album"] = album

    files = None
    if source.startswith("http://") or source.startswith("https://"):
        data["type"] = "url"
        data["image"] = source
    else:
        path = Path(source).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Not a file: {path}")
        data["type"] = "base64"
        data["image"] = base64.b64encode(path.read_bytes()).decode("ascii")

    resp = requests.post(f"{BASE}/image", headers=headers, data=data, files=files, timeout=timeout)
    return _unwrap(resp)


def get_image(image_hash: str, *, access_token: Optional[str] = None, client_id: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    headers = _auth_headers(access_token, client_id)
    resp = requests.get(f"{BASE}/image/{image_hash}", headers=headers, timeout=timeout)
    return _unwrap(resp)


def delete_image(delete_hash_or_id: str, *, access_token: Optional[str] = None, client_id: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    headers = _auth_headers(access_token, client_id)
    resp = requests.delete(f"{BASE}/image/{delete_hash_or_id}", headers=headers, timeout=timeout)
    return _unwrap(resp)


def create_album(
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    privacy: Optional[str] = None,
    image_ids: Optional[List[str]] = None,
    access_token: Optional[str] = None,
    client_id: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    headers = _auth_headers(access_token, client_id)
    data: Dict[str, Any] = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if privacy:
        data["privacy"] = privacy
    if image_ids:
        data["ids[]"] = image_ids
    resp = requests.post(f"{BASE}/album", headers=headers, data=data, timeout=timeout)
    return _unwrap(resp)


def add_to_album(
    album_hash: str,
    image_ids: List[str],
    *,
    access_token: Optional[str] = None,
    client_id: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    headers = _auth_headers(access_token, client_id)
    resp = requests.post(
        f"{BASE}/album/{album_hash}/add",
        headers=headers,
        data={"ids[]": image_ids},
        timeout=timeout,
    )
    return _unwrap(resp)
