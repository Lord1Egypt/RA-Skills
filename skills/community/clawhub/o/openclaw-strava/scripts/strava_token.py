#!/usr/bin/env python3
"""Strava token utilities (OAuth2).

No third-party deps.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


AUTH_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"

DEFAULT_TOKEN_PATH = os.path.expanduser("~/.config/openclaw/strava/token.json")


class StravaAuthError(RuntimeError):
    pass


def token_path() -> str:
    return os.environ.get("STRAVA_TOKEN_PATH", DEFAULT_TOKEN_PATH)


def _mkdirp(p: str) -> None:
    Path(p).parent.mkdir(parents=True, exist_ok=True)


def now_s() -> int:
    return int(time.time())


def load_token(path: Optional[str] = None) -> Dict[str, Any]:
    p = path or token_path()
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_token(tok: Dict[str, Any], path: Optional[str] = None) -> str:
    p = path or token_path()
    _mkdirp(p)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tok, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o600)
    except PermissionError:
        pass
    return p


def is_expired(tok: Dict[str, Any], skew_s: int = 60) -> bool:
    # Strava returns expires_at (epoch seconds)
    exp = tok.get("expires_at")
    if exp is None:
        return False
    try:
        return now_s() >= int(exp) - skew_s
    except Exception:
        return False


def _post_form(url: str, data: Dict[str, str]) -> Dict[str, Any]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise StravaAuthError(f"HTTP {e.code} calling {url}: {raw}") from e


def exchange_code_for_token(*, code: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    return _post_form(
        TOKEN_URL,
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
    )


def refresh_access_token(*, refresh_token: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    return _post_form(
        TOKEN_URL,
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )


def get_access_token(*, client_id: str, client_secret: str, token_file: Optional[str] = None) -> str:
    p = token_file or token_path()
    tok = load_token(p)
    if not tok.get("access_token"):
        raise StravaAuthError(f"No access_token found in {p}. Run strava_oauth_login.py")
    if not is_expired(tok):
        return str(tok["access_token"])

    rt = tok.get("refresh_token")
    if not rt:
        raise StravaAuthError("Token expired and no refresh_token available; re-run OAuth login")

    new_tok = refresh_access_token(refresh_token=str(rt), client_id=client_id, client_secret=client_secret)
    if not new_tok.get("refresh_token"):
        new_tok["refresh_token"] = rt
    save_token(new_tok, p)
    return str(new_tok["access_token"])
