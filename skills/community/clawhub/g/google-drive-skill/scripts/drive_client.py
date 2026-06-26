"""
Shared Google Drive API v3 client factory.

Usage (imported by other scripts):
    from drive_client import build_drive

Environment variables:
    GOOGLE_API_KEY              — for read-only access to public files
    GOOGLE_SERVICE_ACCOUNT_JSON — path to service-account JSON file (read+write)
"""

import os
import sys

try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
except ImportError:
    sys.exit(
        "Missing dependencies. Run:\n"
        "  pip install google-api-python-client google-auth google-auth-httplib2"
    )


SCOPES = ["https://www.googleapis.com/auth/drive"]


def build_drive(readonly: bool = False):
    """
    Return an authenticated Drive API v3 service object.

    Auth resolution order:
    1. GOOGLE_SERVICE_ACCOUNT_JSON  → service account credentials (read+write)
    2. GOOGLE_API_KEY               → API key (read-only public files only)

    Args:
        readonly: When True, accept API-key-only auth. When False, require
                  a service account for write operations.

    Returns:
        googleapiclient.discovery.Resource
    """
    sa_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    api_key = os.environ.get("GOOGLE_API_KEY")

    if sa_path:
        if not os.path.isfile(sa_path):
            sys.exit(f"Service account file not found: {sa_path}")
        creds = service_account.Credentials.from_service_account_file(
            sa_path, scopes=SCOPES
        )
        return build("drive", "v3", credentials=creds)

    if api_key and readonly:
        return build("drive", "v3", developerKey=api_key)

    if not readonly:
        sys.exit(
            "Write operation requires GOOGLE_SERVICE_ACCOUNT_JSON env var.\n"
            "Set it to the path of your service account JSON file."
        )

    sys.exit(
        "No credentials found.\n"
        "Set GOOGLE_API_KEY (read-only) or GOOGLE_SERVICE_ACCOUNT_JSON (read+write)."
    )
