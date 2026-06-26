import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
STATE_DIR = WORKSPACE_ROOT / "state"
STATE_DIR.mkdir(exist_ok=True)
AUTH_FILE = STATE_DIR / "graph_auth.json"
LOG_FILE = STATE_DIR / "graph_ops.log"
# Default app/tenant tuned for Microsoft personal accounts.
# Override with GRAPH_CLIENT_ID / GRAPH_TENANT_ID or CLI args when needed.
DEFAULT_CLIENT_ID = os.getenv("GRAPH_CLIENT_ID", "952d1b34-682e-48ce-9c54-bac5a96cbd42")
DEFAULT_TENANT = os.getenv("GRAPH_TENANT_ID", "consumers")
DEFAULT_SCOPES = [
    "Mail.ReadWrite",
    "Mail.Send",
    "Calendars.ReadWrite",
    "Files.ReadWrite.All",
    "Contacts.ReadWrite",
    "offline_access",
]
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
TOKEN_SAFETY_MARGIN = 120  # seconds


def load_auth_state() -> Dict[str, Any]:
    if AUTH_FILE.exists():
        with AUTH_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_auth_state(data: Dict[str, Any]) -> None:
    with AUTH_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def append_log(entry: Dict[str, Any]) -> None:
    entry.setdefault("timestamp", int(time.time()))
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _authority(tenant_id: Optional[str] = None) -> str:
    tenant = tenant_id or DEFAULT_TENANT
    return f"https://login.microsoftonline.com/{tenant}"


def token_expired(token: Dict[str, Any]) -> bool:
    expires_at = token.get("expires_at")
    if not expires_at:
        return True
    return time.time() > (expires_at - TOKEN_SAFETY_MARGIN)


def _request_token(data: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
    authority = _authority(tenant_id)
    resp = requests.post(f"{authority}/oauth2/v2.0/token", data=data, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    expires_in = int(payload.get("expires_in", 3600))
    payload["expires_at"] = int(time.time()) + expires_in
    return payload


def refresh_access_token(force: bool = False) -> Dict[str, Any]:
    state = load_auth_state()
    token = state.get("token")
    if not token:
        raise RuntimeError("No token available. Run graph_auth.py device-login first.")
    if not force and not token_expired(token):
        return token
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("Refresh token missing. Re-run device login.")
    client_id = state.get("client_id", DEFAULT_CLIENT_ID)
    tenant_id = state.get("tenant_id", DEFAULT_TENANT)
    scope_str = " ".join(state.get("scopes", DEFAULT_SCOPES))
    new_token = _request_token(
        {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": scope_str,
        },
        tenant_id,
    )
    state["token"] = new_token
    save_auth_state(state)
    return new_token


def get_access_token() -> str:
    state = load_auth_state()
    token = state.get("token")
    if not token or token_expired(token):
        token = refresh_access_token(force=True)
    return token["access_token"]


def authorized_request(method: str, url: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {get_access_token()}"
    headers.setdefault("Accept", "application/json")
    if "json" in kwargs and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    kwargs["headers"] = headers
    resp = requests.request(method, url, timeout=60, **kwargs)
    if resp.status_code == 401:
        # token might be expired; refresh once
        refresh_access_token(force=True)
        headers["Authorization"] = f"Bearer {get_access_token()}"
        resp = requests.request(method, url, timeout=60, **kwargs)
    resp.raise_for_status()
    return resp


def graph_url(path: str) -> str:
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return GRAPH_BASE_URL + path


def chunk_iterable(values: Iterable[str], size: int = 10) -> Iterable[list]:
    bucket = []
    for value in values:
        bucket.append(value)
        if len(bucket) == size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


def encode_attachment(path: Path) -> Dict[str, Any]:
    data = path.read_bytes()
    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": path.name,
        "contentBytes": base64.b64encode(data).decode("utf-8"),
    }


def parse_recipients(addresses: Iterable[str]) -> Iterable[Dict[str, Dict[str, str]]]:
    for addr in addresses:
        addr = addr.strip()
        if not addr:
            continue
        yield {"emailAddress": {"address": addr}}


def cli_main(handler):
    try:
        handler()
    except requests.HTTPError as exc:
        print(f"Graph API error: {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
