#!/bin/bash
# ============================================================
# NOT USED BY DEFAULT SETUP — THIS IS AN OPTIONAL HELPER ONLY
# setup.sh does NOT call this script. Most users don't need it.
# Use this ONLY if you want clawhub.ai to provide your Google
# OAuth credentials.json instead of downloading it yourself from
# Google Cloud Console.
# ============================================================
#
# Proactive Claw — OPT-IN clawhub.ai OAuth credential provisioning
#
# WHAT THIS DOES:
#   Downloads your Google OAuth credentials.json from clawhub.ai using a
#   clawhub_token you have set in config.json.
#
# WHAT IS FETCHED:
#   Only the Google OAuth client definition (credentials.json) — the same file
#   you would download from Google Cloud Console. This is NOT your token.json,
#   NOT your calendar data, and NOT any personal information.
#
# WHAT IS NOT FETCHED:
#   - token.json (your Google access token — generated locally, never leaves your machine)
#   - Any calendar events or personal data
#
# HOW TO VERIFY:
#   After running this script, inspect the downloaded file:
#     cat ~/.openclaw/workspace/skills/proactive-claw/credentials.json
#   It should contain only: {"installed": {"client_id": "...", "client_secret": "...", ...}}
#   No personal data. You can revoke the OAuth client at any time in Google Cloud Console.
#
# HOW TO OPT IN:
#   1. Set clawhub_token in your config.json (from clawhub.ai/settings/integrations)
#   2. Set clawhub_oauth_allow_remote_fetch=true in config.json
#   3. Set clawhub_credentials_sha256 in config.json (SHA-256 pin from trusted source)
#   4. Run: bash scripts/optional/setup_clawhub_oauth.sh
#   5. Then run: bash scripts/setup.sh (for the rest of setup)
#
# This script is NOT called by setup.sh. It is a separate, explicit opt-in.

set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/proactive-claw"
CONFIG="$SKILL_DIR/config.json"
CREDS="$SKILL_DIR/credentials.json"

echo "🔑 Proactive Claw — clawhub OAuth credential provisioning"
echo "=========================================================="
echo ""
echo "This will download credentials.json from clawhub.ai."
echo "Only the OAuth client definition is fetched — never your token or calendar data."
echo ""

if [ ! -f "$CONFIG" ]; then
  echo "❌ config.json not found. Run scripts/setup.sh first to create it."
  exit 1
fi

if [ -f "$CREDS" ]; then
  echo "ℹ️  credentials.json already exists at $CREDS"
  echo "   Delete it first if you want to re-download."
  exit 0
fi

python3 - << 'PYEOF'
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

SKILL_DIR = Path.home() / ".openclaw/workspace/skills/proactive-claw"
CONFIG_FILE = SKILL_DIR / "config.json"
CREDS_FILE = SKILL_DIR / "credentials.json"
MAX_RESPONSE_BYTES = 128 * 1024  # hard cap for safety

with open(CONFIG_FILE) as f:
    config = json.load(f)

token = config.get("clawhub_token", "").strip()
if not token:
    print("❌ clawhub_token not set in config.json")
    print("   Get your token at: https://clawhub.ai/settings/integrations")
    sys.exit(1)

allow_remote = bool(config.get("clawhub_oauth_allow_remote_fetch", False))
if not allow_remote:
    print("❌ Remote credential fetch is disabled by policy.")
    print("   Set clawhub_oauth_allow_remote_fetch=true in config.json to opt in.")
    sys.exit(1)

expected_sha = str(config.get("clawhub_credentials_sha256", "")).strip().lower()
if not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
    print("❌ clawhub_credentials_sha256 is missing or invalid.")
    print("   Set a 64-char lowercase hex SHA-256 pin in config.json.")
    print("   Refusing to download unpinned remote credentials.")
    sys.exit(1)

print(f"🌐 Contacting clawhub.ai to fetch Google OAuth client definition...")
print(f"   Endpoint: https://clawhub.ai/api/oauth/google-calendar-credentials")
print(f"   Method: GET (read-only)")
print()

try:
    req = urllib.request.Request(
        "https://clawhub.ai/api/oauth/google-calendar-credentials",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        cl = response.headers.get("Content-Length")
        if cl and int(cl) > MAX_RESPONSE_BYTES:
            print(f"❌ Response too large ({cl} bytes).")
            sys.exit(1)
        payload = response.read(MAX_RESPONSE_BYTES + 1)

    if len(payload) > MAX_RESPONSE_BYTES:
        print(f"❌ Response exceeds {MAX_RESPONSE_BYTES} byte safety limit.")
        sys.exit(1)

    resp = json.loads(payload.decode("utf-8"))
    creds_data = resp.get("credentials") if isinstance(resp, dict) else None
    if not creds_data:
        print("❌ No credentials returned from clawhub.")
        print("   Connect Google Calendar at https://clawhub.ai/settings/integrations first.")
        sys.exit(1)

    # Strict shape checks: only expected OAuth client schema is accepted.
    if not isinstance(creds_data, dict):
        print("❌ Invalid credentials payload type.")
        sys.exit(1)
    top_keys = set(creds_data.keys())
    if top_keys != {"installed"}:
        print("❌ Invalid credentials payload shape: expected top-level key {'installed'}.")
        sys.exit(1)
    installed = creds_data.get("installed")
    if not isinstance(installed, dict):
        print("❌ Invalid credentials payload: 'installed' must be an object.")
        sys.exit(1)
    allowed_installed_keys = {
        "client_id",
        "project_id",
        "auth_uri",
        "token_uri",
        "auth_provider_x509_cert_url",
        "client_secret",
        "redirect_uris",
    }
    unknown_keys = sorted(set(installed.keys()) - allowed_installed_keys)
    if unknown_keys:
        print(f"❌ Invalid credentials payload: unexpected keys in 'installed': {unknown_keys}")
        sys.exit(1)
    if not isinstance(installed.get("redirect_uris"), list):
        print("❌ Invalid credentials payload: redirect_uris must be a list.")
        sys.exit(1)

    # Pin verification: canonical JSON hash must match config pin.
    canonical = json.dumps(creds_data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual_sha = hashlib.sha256(canonical).hexdigest()
    if actual_sha != expected_sha:
        print("❌ SHA-256 pin mismatch for downloaded credentials.")
        print(f"   expected: {expected_sha}")
        print(f"   actual:   {actual_sha}")
        print("   Refusing to write credentials.json.")
        sys.exit(1)

    fd = os.open(str(CREDS_FILE), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(creds_data, f, indent=2)

    print(f"✅ credentials.json downloaded to {CREDS_FILE}")
    print(f"✅ SHA-256 verified: {actual_sha}")
    print()
    print("To verify the downloaded file contains only the OAuth client definition:")
    print(f"  cat {CREDS_FILE}")
    print()
    print("Next step: run bash scripts/setup.sh to complete setup.")
except Exception as e:
    print(f"❌ Failed to fetch credentials: {e}")
    print("   Alternative: download credentials.json manually from Google Cloud Console")
    print("   (see SKILL.md Setup section, Option B)")
    sys.exit(1)
PYEOF
