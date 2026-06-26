#!/usr/bin/env python3
"""Fitbit token utilities (OAuth2).

No third-party deps.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
TOKEN_URL = "https://api.fitbit.com/oauth2/token"

DEFAULT_TOKEN_PATH = os.path.expanduser("~/.config/openclaw/fitbit/token.json")


class FitbitAuthError(RuntimeError):
    pass


def token_path() -> str:
    return os.environ.get("FITBIT_TOKEN_PATH", DEFAULT_TOKEN_PATH)


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
    exp = tok.get("expires_at")
    if exp is None:
        return False
    try:
        return now_s() >= int(exp) - skew_s
    except Exception:
        return False


def _basic_auth(client_id: str, client_secret: str) -> str:
    raw = f"{client_id}:{client_secret}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def _post_form(url: str, data: Dict[str, str], headers: Dict[str, str]) -> Dict[str, Any]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise FitbitAuthError(f"HTTP {e.code} calling {url}: {raw}") from e


def exchange_code_for_token(*, code: str, redirect_uri: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    tok = _post_form(
        TOKEN_URL,
        {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        {"Authorization": f"Basic {_basic_auth(client_id, client_secret)}"},
    )
    _annotate(tok)
    return tok


def refresh_access_token(*, refresh_token: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    tok = _post_form(
        TOKEN_URL,
        {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        {"Authorization": f"Basic {_basic_auth(client_id, client_secret)}"},
    )
    _annotate(tok)
    return tok


def _annotate(tok: Dict[str, Any]) -> None:
    exp_in = tok.get("expires_in")
    if exp_in is not None:
        try:
            tok["expires_at"] = now_s() + int(exp_in)
        except Exception:
            pass


def get_access_token(*, client_id: str, client_secret: str, token_file: Optional[str] = None) -> str:
    p = token_file or token_path()
    tok = load_token(p)
    access = tok.get("access_token")
    if not access:
        raise FitbitAuthError(f"No access_token found in {p}. Run fitbit_oauth_login.py")
    if not is_expired(tok):
        return str(access)

    rt = tok.get("refresh_token")
    if not rt:
        raise FitbitAuthError("Token expired and no refresh_token available; re-run OAuth login")

    new_tok = refresh_access_token(refresh_token=str(rt), client_id=client_id, client_secret=client_secret)
    if not new_tok.get("refresh_token"):
        new_tok["refresh_token"] = rt
    save_token(new_tok, p)
    return str(new_tok["access_token"])
