#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopMediai API client functions (requests-based).
Reads API key and base URL from environment/.env:
- TOPMEDIAI_API_KEY (required)
- TOPMEDIAI_BASE_URL (default: https://api.topmediai.com)
"""
import os
from typing import List, Dict, Any, Optional, NoReturn
import requests
from dotenv import load_dotenv
from pathlib import Path

# Resolve skill root dynamically (scripts/ -> skill root)
_SKILL_ROOT = Path(__file__).resolve().parents[1]
_ENV_PATH = _SKILL_ROOT / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH.as_posix())

BASE_URL = os.environ.get("TOPMEDIAI_BASE_URL", "https://api.topmediai.com")
DEFAULT_KEY = os.environ.get("TOPMEDIAI_API_KEY")
DEBUG_MODE = str(os.environ.get("TOPMEDIAI_DEBUG", "0")).lower() in {"1", "true", "yes", "on"}
PURCHASE_URL = "https://www.topmediai.com/api/payment/subscription/"
_INSUFFICIENT_HINTS = (
    "权益不足",
    "insufficient",
    "insufficient balance",
    "insufficient quota",
    "quota exceeded",
    "credit",
    "subscription",
    "benefits",
)


def _contains_insufficient_benefits_text(value: Any) -> bool:
    text = str(value).lower()
    return any(hint in text for hint in _INSUFFICIENT_HINTS)


def _with_purchase_link_if_needed(payload: Any) -> Any:
    if isinstance(payload, dict) and _contains_insufficient_benefits_text(payload):
        out = dict(payload)
        out["purchase_url"] = PURCHASE_URL
        return out
    if isinstance(payload, list) and _contains_insufficient_benefits_text(payload):
        return {"purchase_url": PURCHASE_URL, "data": payload}
    return payload


def _extract_data_with_purchase_link(payload: Any) -> Any:
    if isinstance(payload, dict):
        data = payload.get("data", payload)
        if _contains_insufficient_benefits_text(payload):
            if isinstance(data, dict):
                out = dict(data)
                out["purchase_url"] = PURCHASE_URL
                return out
            return {"purchase_url": PURCHASE_URL, "data": data}
        return _with_purchase_link_if_needed(data)
    return _with_purchase_link_if_needed(payload)

def _mask_key(value: Optional[str]) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}***{value[-4:]}"


def _debug_request(method: str, url: str, headers: Dict[str, str], payload: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None):
    if not DEBUG_MODE:
        return
    safe_headers = dict(headers)
    if "x-api-key" in safe_headers:
        safe_headers["x-api-key"] = _mask_key(str(safe_headers.get("x-api-key")))
    info: Dict[str, Any] = {"debug": {"method": method, "url": url, "headers": safe_headers}}
    if payload is not None:
        info["debug"]["payload"] = payload
    if params is not None:
        info["debug"]["params"] = params
    print(info)


def _raise_as_runtime_error(e: Exception, method: str, url: str) -> NoReturn:
    detail = str(e)
    if isinstance(e, requests.HTTPError) and getattr(e, "response", None) is not None:
        resp = e.response
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        payload = _with_purchase_link_if_needed(body)
        detail = f"HTTP {resp.status_code}: {payload}"
    elif _contains_insufficient_benefits_text(detail):
        detail = f"{detail} | purchase_url={PURCHASE_URL}"
    msg = f"TopMediai request failed: {method} {url}: {type(e).__name__}: {detail}"
    raise RuntimeError(msg)


def _headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or DEFAULT_KEY
    if not key:
        raise RuntimeError(
            "TOPMEDIAI_API_KEY not configured. Edit: {} and set TOPMEDIAI_API_KEY=YOUR_KEY."
            "Get/purchase a key at https://www.topmediai.com/api/basic-information/interface-key/".format(_ENV_PATH)
        )
    return {"x-api-key": key, "Content-Type": "application/json"}


def generate_lyrics(prompt: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/lyrics"
    headers = _headers(api_key)
    payload = {"prompt": prompt}
    _debug_request("POST", url, headers=headers, payload=payload)
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        j = r.json()
        return _extract_data_with_purchase_link(j)
    except Exception as e:
        _raise_as_runtime_error(e, "POST", url)


def generate_music(
    action: str = "auto",
    prompt: Optional[str] = None,
    lyrics: Optional[str] = None,
    title: str = "",
    style: str = "Pop",
    mv: str = "v5.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    url = f"{BASE_URL}/v3/music/generate"
    data: Dict[str, Any] = {
        "action": action,
        "mv": mv,
        "instrumental": int(instrumental),
        "style": style,
        "gender": gender,
    }
    if prompt:
        data["prompt"] = prompt
    if action == "custom" and lyrics:
        data["lyrics"] = lyrics
        if title:
            data["title"] = title

    headers = _headers(api_key)
    _debug_request("POST", url, headers=headers, payload=data)
    try:
        r = requests.post(url, json=data, headers=headers, timeout=120)
        r.raise_for_status()
        j = r.json()
        return _extract_data_with_purchase_link(j)
    except Exception as e:
        _raise_as_runtime_error(e, "POST", url)


def generate_music_auto(
    prompt: str,
    style: str = "Pop",
    mv: str = "v5.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    return generate_music(
        action="auto",
        prompt=prompt,
        style=style,
        mv=mv,
        instrumental=instrumental,
        gender=gender,
        api_key=api_key,
    )


def generate_music_with_lyrics(
    lyrics: str,
    title: str = "",
    style: str = "Pop",
    mv: str = "v5.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    return generate_music(
        action="custom",
        lyrics=lyrics,
        title=title,
        style=style,
        mv=mv,
        instrumental=instrumental,
        gender=gender,
        api_key=api_key,
    )


def _extract_task_ids(data: Any) -> List[str]:
    ids: List[str] = []
    if isinstance(data, dict):
        if isinstance(data.get("ids"), list):
            ids.extend([str(x) for x in data.get("ids", []) if x is not None])
        for key in ("id", "task_id"):
            if data.get(key) is not None:
                ids.append(str(data.get(key)))
        if isinstance(data.get("tasks"), list):
            for item in data.get("tasks", []):
                if isinstance(item, dict):
                    v = item.get("id") or item.get("task_id")
                    if v is not None:
                        ids.append(str(v))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                v = item.get("id") or item.get("task_id")
                if v is not None:
                    ids.append(str(v))
            elif item is not None:
                ids.append(str(item))

    # de-duplicate keep order
    seen = set()
    uniq = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return uniq


def submit_and_extract_ids(
    action: str = "auto",
    prompt: Optional[str] = None,
    lyrics: Optional[str] = None,
    title: str = "",
    style: str = "Pop",
    mv: str = "v5.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> List[str]:
    data = generate_music(
        action=action,
        prompt=prompt,
        lyrics=lyrics,
        title=title,
        style=style,
        mv=mv,
        instrumental=instrumental,
        gender=gender,
        api_key=api_key,
    )
    return _extract_task_ids(data)


def query_tasks(task_ids: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    ids_str = ",".join([str(x) for x in task_ids if x is not None])
    url = f"{BASE_URL}/v3/music/tasks?ids={ids_str}"
    headers = _headers(api_key)
    _debug_request("GET", url, headers=headers)
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        j = r.json()
        data = _extract_data_with_purchase_link(j)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and data.get("purchase_url"):
            raise RuntimeError(f"权益不足，请购买后重试：{data.get('purchase_url')}")
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            return data.get("data", [])
        return []
    except Exception as e:
        _raise_as_runtime_error(e, "GET", url)


def generate_mp4(song_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v3/music/generate-mp4"
    params = {"song_id": song_id}
    headers = _headers(api_key)
    _debug_request("POST", url, headers=headers, params=params)
    try:
        r = requests.post(url, params=params, headers=headers, timeout=300)
        r.raise_for_status()
        j = r.json()
        return _extract_data_with_purchase_link(j)
    except Exception as e:
        _raise_as_runtime_error(e, "POST", url)
