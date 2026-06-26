#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Musicful API client functions (requests-based).
Reads API key and base URL from environment/.env:
- MUSICFUL_API_KEY (required)
- MUSICFUL_BASE_URL (default: https://api.musicful.ai)

Functions:
- generate_lyrics(prompt, api_key=None)
- generate_music(action="auto", lyrics=None, title="", style="Happy songs", mv="MFV2.0", instrumental=0, gender="male", api_key=None)
- generate_music_with_lyrics(lyrics, style="Happy songs", title="", mv="MFV2.0", instrumental=0, gender="male", api_key=None)
- generate_music_auto(style="Happy songs", mv="MFV2.0", instrumental=0, gender="male", api_key=None)
- query_tasks(task_ids, api_key=None)
- generate_mp4(task_id, api_key=None)
"""
import os
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv
from pathlib import Path

# Resolve skill root dynamically (scripts/ -> skill root)
_SKILL_ROOT = Path(__file__).resolve().parents[1]
_ENV_PATH = _SKILL_ROOT / ".env"
# Load only the .env inside the actual skill folder (simple, unambiguous)
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH.as_posix())

BASE_URL = os.environ.get("MUSICFUL_BASE_URL", "https://api.musicful.ai")
DEFAULT_KEY = os.environ.get("MUSICFUL_API_KEY")


def _headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or DEFAULT_KEY
    if not key:
        raise RuntimeError(
            "MUSICFUL_API_KEY not configured. Edit: {} and set MUSICFUL_API_KEY=YOUR_KEY. "
            "Get/purchase a key at https://www.musicful.ai/api/authentication/interface-key/".format(
                _ENV_PATH
            )
        )
    return {"x-api-key": key, "Content-Type": "application/json"}


def generate_lyrics(prompt: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v1/lyrics"
    r = requests.post(url, json={"prompt": prompt}, headers=_headers(api_key), timeout=60)
    r.raise_for_status()
    j = r.json()
    return j.get("data", j)


def generate_music(
    action: str = "auto",
    lyrics: Optional[str] = None,
    title: str = "",
    style: str = "Happy songs",
    mv: str = "MFV2.0",
    instrumental: int = 0,
    gender: str = "male",
    prompt: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[str]:
    """Returns task id list (when available)."""
    url = f"{BASE_URL}/v1/music/generate"
    data: Dict[str, Any] = {
        "action": action,
        "style": style,
        "mv": mv,
        "instrumental": instrumental,
        "gender": gender,
    }
    if prompt:
        data["prompt"] = prompt
    if action == "custom" and lyrics:
        data["lyrics"] = lyrics
        if title:
            data["title"] = title
    r = requests.post(url, json=data, headers=_headers(api_key), timeout=120)
    r.raise_for_status()
    j = r.json()
    return j.get("data", {}).get("ids", []) or j.get("data", []) or j


def generate_music_with_lyrics(
    lyrics: str,
    style: str = "Happy songs",
    title: str = "",
    mv: str = "MFV2.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> List[str]:
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


def generate_music_auto(
    prompt: str = "",
    style: str = "Happy songs",
    mv: str = "MFV2.0",
    instrumental: int = 0,
    gender: str = "male",
    api_key: Optional[str] = None,
) -> List[str]:
    return generate_music(
        action="auto",
        lyrics=None,
        title="",
        style=style,
        mv=mv,
        instrumental=instrumental,
        gender=gender,
        prompt=prompt,
        api_key=api_key,
    )


def query_tasks(task_ids: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    ids_str = ",".join(task_ids)
    url = f"{BASE_URL}/v1/music/tasks?ids={ids_str}"
    r = requests.get(url, headers=_headers(api_key), timeout=60)
    r.raise_for_status()
    return r.json().get("data", [])


def generate_mp4(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}/v3/music/generate-mp4"
    r = requests.post(url, json={"task_id": task_id}, headers=_headers(api_key), timeout=120)
    r.raise_for_status()
    return r.json()
