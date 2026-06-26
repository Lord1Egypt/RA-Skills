from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .utils import token_path, ensure_config_dir, audit_log

# Gmail scopes - no send endpoints used by this tool
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]


def load_credentials() -> Optional[Credentials]:
    tp = token_path()
    if tp.exists():
        return Credentials.from_authorized_user_file(str(tp), SCOPES)
    return None


def save_credentials(creds: Credentials):
    ensure_config_dir()
    token_path().write_text(creds.to_json())


def authenticate(client_secret: str, account: str, force: bool = False) -> Credentials:
    audit_log("auth.start", {"account": account})
    creds = load_credentials()
    if creds and creds.valid and not force:
        audit_log("auth.cached", {"account": account})
        return creds

    if creds and creds.expired and creds.refresh_token and not force:
        creds.refresh(Request())
        save_credentials(creds)
        audit_log("auth.refreshed", {"account": account})
        return creds

    if not os.path.exists(client_secret):
        raise FileNotFoundError(f"Client secret not found: {client_secret}")

    flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
    creds = flow.run_local_server(port=0)
    save_credentials(creds)
    audit_log("auth.complete", {"account": account})
    return creds
