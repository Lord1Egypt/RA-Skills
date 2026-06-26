#!/usr/bin/env python3
"""Withings token utilities (OAuth2).

Withings uses OAuth2 and a token endpoint at wbsapi.withings.net.
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


# Auth docs live at https://developer.withings.com/
AUTH_URL = "https://account.withings.com/oauth2_user/authorize2"
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"

DEFAULT_TOKEN_PATH = os.path.expanduser("~/.config/openclaw/withings/token.json")


class WithingsAuthError(RuntimeError):
    pass


def token_path() -> str:
    return os.environ.get("WITHINGS_TOKEN_PATH", DEFAULT_TOKEN_PATH)


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
        # Withings returns expires_in, we store expires_at.
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
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise WithingsAuthError(f"HTTP {e.code} calling {url}: {raw}") from e


def _annotate_expiry(tok: Dict[str, Any]) -> None:
    exp_in = tok.get("expires_in")
    if exp_in is not None:
        try:
            tok["expires_at"] = now_s() + int(exp_in)
        except Exception:
            pass


def exchange_code_for_token(*, code: str, client_id: str, client_secret: str, redirect_uri: str) -> Dict[str, Any]:
    # Withings uses action=requesttoken
    tok = _post_form(
        TOKEN_URL,
        {
            "action": "requesttoken",
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    _annotate_expiry(tok)
    return tok


def refresh_access_token(*, refresh_token: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    tok = _post_form(
        TOKEN_URL,
        {
            "action": "requesttoken",
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        },
    )
    _annotate_expiry(tok)
    return tok


def get_access_token(*, client_id: str, client_secret: str, token_file: Optional[str] = None) -> str:
    p = token_file or token_path()
    tok = load_token(p)
    # Withings token response often wraps in {status, body:{access_token...}}
    body = tok.get("body") if isinstance(tok, dict) else None
    if isinstance(body, dict):
        token_container = body
    else:
        token_container = tok

    access = token_container.get("access_token")
    if not access:
        raise WithingsAuthError(f"No access_token found in {p}. Run withings_oauth_login.py")

    # expires_at may be at top-level or inside body; normalize.
    exp = token_container.get("expires_at") or tok.get("expires_at")
    if exp:
        tok["expires_at"] = exp

    if not is_expired(tok):
        return str(access)

    rt = token_container.get("refresh_token")
    if not rt:
        raise WithingsAuthError("Token expired and no refresh_token available; re-run OAuth login")

    new_tok = refresh_access_token(refresh_token=str(rt), client_id=client_id, client_secret=client_secret)
    # Preserve refresh_token if absent.
    nb = new_tok.get("body") if isinstance(new_tok, dict) else None
    if isinstance(nb, dict) and not nb.get("refresh_token"):
        nb["refresh_token"] = rt
    save_token(new_tok, p)

    nb2 = new_tok.get("body") if isinstance(new_tok, dict) else None
    if isinstance(nb2, dict) and nb2.get("access_token"):
        return str(nb2["access_token"])
    return str(new_tok.get("access_token"))
