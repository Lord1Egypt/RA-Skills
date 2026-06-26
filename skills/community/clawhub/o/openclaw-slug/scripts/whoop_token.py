#!/usr/bin/env python3
"""WHOOP token utilities.

- Store tokens in a local JSON file.
- Refresh access tokens when expired.

No third-party deps.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


OAUTH_AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
OAUTH_TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"

DEFAULT_TOKEN_PATH = os.path.expanduser("~/.config/openclaw/whoop/token.json")


class WhoopAuthError(RuntimeError):
    pass


def _mkdirp(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def token_path() -> str:
    return os.environ.get("WHOOP_TOKEN_PATH", DEFAULT_TOKEN_PATH)


def load_token(path: Optional[str] = None) -> Dict[str, Any]:
    p = path or token_path()
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_token(token: Dict[str, Any], path: Optional[str] = None) -> str:
    p = path or token_path()
    _mkdirp(p)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o600)
    except PermissionError:
        pass
    return p


def now_s() -> int:
    return int(time.time())


def is_expired(token: Dict[str, Any], skew_s: int = 60) -> bool:
    # We store expires_at (epoch seconds) when we first obtain/refresh.
    exp = token.get("expires_at")
    if not exp:
        return False
    return now_s() >= int(exp) - skew_s


def _post_form(url: str, data: Dict[str, str], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise WhoopAuthError(f"HTTP {e.code} calling {url}: {raw}") from e


def exchange_code_for_token(*, code: str, client_id: str, client_secret: str, redirect_uri: str) -> Dict[str, Any]:
    tok = _post_form(
        OAUTH_TOKEN_URL,
        {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        },
    )
    _annotate_expiry(tok)
    return tok


def refresh_access_token(*, refresh_token: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    tok = _post_form(
        OAUTH_TOKEN_URL,
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    _annotate_expiry(tok)
    return tok


def _annotate_expiry(tok: Dict[str, Any]) -> None:
    # WHOOP returns expires_in seconds.
    exp_in = tok.get("expires_in")
    if exp_in is not None:
        try:
            tok["expires_at"] = now_s() + int(exp_in)
        except Exception:
            pass


def get_access_token(*, client_id: str, client_secret: str, token_file: Optional[str] = None) -> str:
    p = token_file or token_path()
    tok = load_token(p)
    if not tok.get("access_token"):
        raise WhoopAuthError(f"No access_token found in {p}. Run whoop_oauth_login.py")

    if not is_expired(tok):
        return str(tok["access_token"])

    rt = tok.get("refresh_token")
    if not rt:
        raise WhoopAuthError("Token expired and no refresh_token available; re-run OAuth login")

    new_tok = refresh_access_token(refresh_token=str(rt), client_id=client_id, client_secret=client_secret)
    # Preserve refresh_token if WHOOP doesn't return a new one.
    if not new_tok.get("refresh_token"):
        new_tok["refresh_token"] = rt
    save_token(new_tok, p)
    return str(new_tok["access_token"])
