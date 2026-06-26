#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bootstrap Gusnais API config using only CLIENT_ID and CLIENT_SECRET.

Usage:
  1) Export CLIENT_ID and CLIENT_SECRET.
  2) Run once to get authorize_url.
  3) Complete OAuth in browser and export OAUTH_CODE.
  4) Run again to exchange token and verify identity via /api/v3/users/me.
  5) (Optional) set TOKEN_STORE_PATH to persist refreshable token store JSON.
"""

import json
import os
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Optional

import requests

SITE = "https://gusnais.com"
AUTHORIZE_PATH = "/oauth/authorize"
TOKEN_PATH = "/oauth/token"
REVOKE_PATH = "/oauth/revoke"
API_BASE = "/api/v3"


class BootError(Exception):
    pass


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise BootError(f"missing env: {name}")
    return value


def build_authorize_url(client_id: str, redirect_uri: str, state: str, scope: str = "") -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
    }
    if scope:
        params["scope"] = scope
    return f"{SITE}{AUTHORIZE_PATH}?{urllib.parse.urlencode(params)}"


def post_token(data: Dict[str, str]) -> Dict[str, Any]:
    res = requests.post(f"{SITE}{TOKEN_PATH}", data=data, timeout=20)
    if res.status_code >= 400:
        raise BootError(f"token request failed: {res.status_code} {res.text[:300]}")
    payload = res.json()
    if "access_token" not in payload:
        raise BootError("token response missing access_token")
    return payload


def exchange_code(client_id: str, client_secret: str, code: str, redirect_uri: str) -> Dict[str, Any]:
    return post_token(
        {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
    )


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> Dict[str, Any]:
    return post_token(
        {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
    )


def api_get(path: str, access_token: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Any:
    url = f"{SITE}{API_BASE}{path}"
    query = dict(params or {})
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
        # compatibility with Homeland API docs
        query["access_token"] = access_token

    res = requests.get(url, params=query, headers=headers, timeout=20)
    if res.status_code >= 400:
        raise BootError(f"GET {path} failed: {res.status_code} {res.text[:300]}")
    return res.json()


def extract_identity(me_payload: Any) -> Dict[str, Any]:
    """Normalize /users/me payload variants to a flat identity dict."""

    def pick_fields(obj: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(obj, dict):
            return None
        keys = {"id", "login", "name", "email"}
        if keys.intersection(obj.keys()):
            return {
                "id": obj.get("id"),
                "login": obj.get("login"),
                "name": obj.get("name"),
                "email": obj.get("email"),
            }
        return None

    # Most common cases
    for key in ("user", "data", "profile", "attributes"):
        picked = pick_fields(me_payload.get(key) if isinstance(me_payload, dict) else None)
        if picked:
            return picked

    # Flat payload fallback
    picked = pick_fields(me_payload)
    if picked:
        return picked

    # Heuristic: first nested dict containing at least one identity field
    if isinstance(me_payload, dict):
        for value in me_payload.values():
            picked = pick_fields(value)
            if picked:
                return picked

    return {"id": None, "login": None, "name": None, "email": None}


def write_token_store(
    token_store_path: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    token_data: Dict[str, Any],
) -> None:
    """Persist OAuth tokens for long-lived refresh flow."""

    now = int(time.time())
    expires_in = int(token_data.get("expires_in") or 0)
    payload = {
        "site": SITE,
        "api_base": f"{SITE}{API_BASE}",
        "oauth": {
            "authorize_endpoint": f"{SITE}{AUTHORIZE_PATH}",
            "token_endpoint": f"{SITE}{TOKEN_PATH}",
            "revoke_endpoint": f"{SITE}{REVOKE_PATH}",
        },
        "client": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        },
        "token": {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),
            "token_type": token_data.get("token_type"),
            "scope": token_data.get("scope"),
            "expires_in": expires_in,
            "expires_at": (now + expires_in) if expires_in > 0 else None,
            "created_at": token_data.get("created_at", now),
        },
    }

    path = Path(token_store_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(path, 0o600)


def main() -> None:
    client_id = env_required("CLIENT_ID")
    client_secret = env_required("CLIENT_SECRET")

    redirect_uri = os.getenv("REDIRECT_URI", "urn:ietf:wg:oauth:2.0:oob")
    state = os.getenv("OAUTH_STATE", "gusnais-state")
    scope = os.getenv("OAUTH_SCOPE", "")
    code = os.getenv("OAUTH_CODE", "").strip()
    token_store_path = os.getenv("TOKEN_STORE_PATH", "").strip()

    output: Dict[str, Any] = {
        "site": SITE,
        "oauth": {
            "authorize_endpoint": f"{SITE}{AUTHORIZE_PATH}",
            "token_endpoint": f"{SITE}{TOKEN_PATH}",
            "revoke_endpoint": f"{SITE}{REVOKE_PATH}",
        },
        "api_base": f"{SITE}{API_BASE}",
        "authorize_url": build_authorize_url(client_id, redirect_uri, state, scope),
        "token_ready": False,
    }

    if not code:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    token_data = exchange_code(client_id, client_secret, code, redirect_uri)
    access_token = token_data["access_token"]
    me = api_get("/users/me", access_token=access_token)

    output["token_ready"] = True
    output["identity"] = extract_identity(me)
    output["token_meta"] = {
        "expires_in": token_data.get("expires_in"),
        "has_refresh_token": bool(token_data.get("refresh_token")),
        "token_type": token_data.get("token_type"),
    }

    if token_store_path:
        write_token_store(token_store_path, client_id, client_secret, redirect_uri, token_data)
        output["token_store"] = token_store_path

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except BootError as err:
        print(json.dumps({"ok": False, "error": str(err)}, ensure_ascii=False))
        raise SystemExit(1)
