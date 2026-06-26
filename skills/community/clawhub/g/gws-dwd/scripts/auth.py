#!/usr/bin/env python3
"""Shared auth module for GWS skill — service account + domain-wide delegation."""

import json
import os
import sys
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build

DEFAULT_KEY_PATH = os.path.expanduser("~/.config/gws/service-account.json")
DEFAULT_ADMIN_EMAIL = os.environ.get("GWS_ADMIN_EMAIL", "")
DEFAULT_DOMAIN = os.environ.get("GWS_DOMAIN", "")

# Scope sets by API
SCOPES = {
    "vault": ["https://www.googleapis.com/auth/ediscovery"],
    "reports": [
        "https://www.googleapis.com/auth/admin.reports.audit.readonly",
        "https://www.googleapis.com/auth/admin.reports.usage.readonly",
    ],
    "directory": [
        "https://www.googleapis.com/auth/admin.directory.user.readonly",
        "https://www.googleapis.com/auth/admin.directory.group.readonly",
        "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
    ],
    "gmail": ["https://www.googleapis.com/auth/gmail.readonly"],
    "drive": ["https://www.googleapis.com/auth/drive.readonly"],
    "calendar": ["https://www.googleapis.com/auth/calendar.readonly"],
    "sheets": ["https://www.googleapis.com/auth/spreadsheets.readonly"],
    "docs": ["https://www.googleapis.com/auth/documents.readonly"],
    "people": [
        "https://www.googleapis.com/auth/contacts.readonly",
        "https://www.googleapis.com/auth/directory.readonly",
    ],
}

# API service names and versions
API_INFO = {
    "vault": ("vault", "v1"),
    "reports": ("admin", "reports_v1"),
    "directory": ("admin", "directory_v1"),
    "gmail": ("gmail", "v1"),
    "drive": ("drive", "v3"),
    "calendar": ("calendar", "v3"),
    "sheets": ("sheets", "v4"),
    "docs": ("docs", "v1"),
    "people": ("people", "v1"),
}


def get_credentials(
    api: str,
    impersonate: Optional[str] = None,
    key_path: Optional[str] = None,
) -> service_account.Credentials:
    """Get delegated credentials for a given API.

    Args:
        api: API name (vault, reports, directory, gmail, drive, calendar, sheets, docs, chat, people)
        impersonate: Email to impersonate via DWD. Defaults to admin email.
        key_path: Path to service account JSON key. Defaults to ~/.config/gws/service-account.json.

    Returns:
        Delegated credentials ready for API calls.
    """
    if api not in SCOPES:
        raise ValueError(f"Unknown API: {api}. Valid: {', '.join(SCOPES.keys())}")

    key_file = key_path or os.environ.get("GWS_SERVICE_ACCOUNT_PATH", DEFAULT_KEY_PATH)
    subject = impersonate or DEFAULT_ADMIN_EMAIL

    credentials = service_account.Credentials.from_service_account_file(
        key_file,
        scopes=SCOPES[api],
        subject=subject,
    )
    return credentials


def get_service(
    api: str,
    impersonate: Optional[str] = None,
    key_path: Optional[str] = None,
):
    """Build an API service client with delegated credentials.

    Args:
        api: API name (vault, reports, directory, gmail, drive, calendar, sheets, docs, chat, people)
        impersonate: Email to impersonate via DWD. Defaults to admin email.
        key_path: Path to service account JSON key.

    Returns:
        Google API service client.
    """
    credentials = get_credentials(api, impersonate, key_path)
    service_name, version = API_INFO[api]
    return build(service_name, version, credentials=credentials)


if __name__ == "__main__":
    # Quick test: verify auth works
    api = sys.argv[1] if len(sys.argv) > 1 else "vault"
    try:
        service = get_service(api)
        print(json.dumps({"status": "ok", "api": api, "service_account": DEFAULT_KEY_PATH}))
    except Exception as e:
        print(json.dumps({"status": "error", "api": api, "error": str(e)}))
        sys.exit(1)
