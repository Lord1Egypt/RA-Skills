#!/usr/bin/env python3
"""
reauth_google.py — Re-authenticate with Google and save a fresh refresh token.

Run this whenever you see "invalid_grant: Token has been expired or revoked."

What it does:
  1. Reads your existing GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET from .env
  2. Opens your browser to Google's OAuth consent screen
  3. After you approve, captures the new refresh token
  4. Writes it back to .env  (replaces the old GOOGLE_REFRESH_TOKEN)
  5. Also stores it in macOS Keychain via keychain_secrets.py

Scopes granted:
  - gmail.readonly          (school email monitor)
  - calendar                (family calendar read + write)

Usage:
    cd ~/.openclaw/workspace/skills/homebase
    python core/reauth_google.py
"""

import os
import sys
import pathlib
import re

SKILL_DIR = pathlib.Path(__file__).parent.parent
ENV_FILE  = SKILL_DIR / ".env"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env_file() -> dict:
    """Parse .env file into a dict."""
    values = {}
    if not ENV_FILE.exists():
        return values
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                values[k.strip()] = v.strip()
    return values


def update_env_file(key: str, new_value: str):
    """Replace or append a key=value line in .env."""
    if not ENV_FILE.exists():
        ENV_FILE.write_text(f"{key}={new_value}\n")
        return

    content = ENV_FILE.read_text()
    pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)

    if pattern.search(content):
        content = pattern.sub(f"{key}={new_value}", content)
    else:
        content = content.rstrip("\n") + f"\n{key}={new_value}\n"

    ENV_FILE.write_text(content)


def store_in_keychain(refresh_token: str) -> bool:
    """Write the new refresh token to macOS Keychain."""
    try:
        from core.keychain_secrets import store_secret
        ok = store_secret("GOOGLE_REFRESH_TOKEN", refresh_token)
        return ok
    except Exception as e:
        print(f"  ⚠️  Keychain write failed (non-fatal): {e}")
        return False


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("─" * 60)
    print("  Google OAuth Re-authentication")
    print("─" * 60)
    print()

    # 1. Load existing client credentials — Keychain first, then .env
    try:
        from core.keychain_secrets import load_google_secrets
        load_google_secrets()
    except Exception as e:
        print(f"  ⚠️  Keychain load skipped: {e}")

    env = load_env_file()
    client_id     = env.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = env.get("GOOGLE_CLIENT_SECRET", "").strip()

    # Fall back to environment (set by load_google_secrets or shell)
    if not client_id:
        client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    if not client_secret:
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("ERROR: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in .env")
        print(f"  Looked in: {ENV_FILE}")
        print()
        print("  Make sure your .env file has:")
        print("    GOOGLE_CLIENT_ID=<your client id>")
        print("    GOOGLE_CLIENT_SECRET=<your client secret>")
        sys.exit(1)

    print(f"✓ Client ID found: {client_id[:20]}...")
    print()

    # 2. Check google-auth-oauthlib is available
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("ERROR: missing dependency 'google-auth-oauthlib'.")
        print("  Run: pip install -e .")
        sys.exit(1)

    # 3. Build client config dict (same format as client_secret.json)
    client_config = {
        "installed": {
            "client_id":     client_id,
            "client_secret": client_secret,
            "redirect_uris": ["http://localhost"],
            "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
            "token_uri":     "https://oauth2.googleapis.com/token",
        }
    }

    print("Opening browser for Google sign-in...")
    print()
    print("Scopes being requested:")
    for s in SCOPES:
        print(f"  • {s.split('/')[-1]}")
    print()
    print("After you approve, come back here — the token will be saved automatically.")
    print()

    # 4. Run the local OAuth flow
    try:
        flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
        # run_local_server opens browser, listens on a free port, captures the code
        creds = flow.run_local_server(
            port=49402,
            prompt="consent",       # force consent screen so we always get refresh_token
            access_type="offline",
            open_browser=True,
        )
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR during OAuth flow: {e}")
        sys.exit(1)

    refresh_token = creds.refresh_token
    if not refresh_token:
        print("ERROR: No refresh token returned.")
        print("  This can happen if the app was previously authorized.")
        print("  Go to https://myaccount.google.com/permissions, revoke access,")
        print("  and run this script again.")
        sys.exit(1)

    print()
    print("✓ New refresh token obtained.")
    print()

    # 5. Save to .env
    update_env_file("GOOGLE_REFRESH_TOKEN", refresh_token)
    print(f"✓ Saved to {ENV_FILE}")

    # 6. Save to Keychain
    if store_in_keychain(refresh_token):
        print("✓ Saved to macOS Keychain")
    else:
        print("  (Keychain skipped — .env is the active source)")

    print()
    print("─" * 60)
    print("  Done! All services should work again immediately.")
    print()
    print("  To verify:")
    print("    python3 features/briefing/briefing_preflight.py")
    print("─" * 60)


if __name__ == "__main__":
    main()
