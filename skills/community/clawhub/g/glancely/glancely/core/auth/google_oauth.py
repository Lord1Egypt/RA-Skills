"""Google OAuth flow for glancely.

User-brings-own-client model:
  1. User creates an OAuth Desktop client in Google Cloud Console.
  2. Downloads credentials.json → puts it at ~/.glancely/credentials.json
  3. First call to get_calendar_service() opens a browser, user grants scopes,
     token is cached at ~/.glancely/token.json.
  4. Subsequent calls refresh the token automatically.

This deliberately does not ship a shared OAuth client — keeps verification
burden off the maintainer.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CONFIG_DIR = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely"))
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"
TOKEN_PATH = CONFIG_DIR / "token.json"


class AuthSetupError(RuntimeError):
    pass


def _load_credentials() -> Credentials:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    creds: Credentials | None = None
    if TOKEN_PATH.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        return creds

    if not CREDENTIALS_PATH.is_file():
        raise AuthSetupError(
            f"Missing OAuth client at {CREDENTIALS_PATH}.\n"
            f"  1. Go to https://console.cloud.google.com/apis/credentials\n"
            f"  2. Create OAuth client ID → Desktop app\n"
            f"  3. Download the JSON, save as {CREDENTIALS_PATH}\n"
            f"  4. Re-run install.sh (or this command)."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True, prompt="consent")
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def get_calendar_service():
    creds = _load_credentials()
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def bootstrap_interactive() -> dict:
    """Used by install.sh: forces the OAuth flow and reports status."""
    try:
        service = get_calendar_service()
    except AuthSetupError as exc:
        return {"ok": False, "reason": str(exc)}

    profile = service.calendarList().list(maxResults=1).execute()
    return {
        "ok": True,
        "credentials_path": str(CREDENTIALS_PATH),
        "token_path": str(TOKEN_PATH),
        "calendars_found": len(profile.get("items", [])),
    }


if __name__ == "__main__":
    import json
    result = bootstrap_interactive()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else 1)
