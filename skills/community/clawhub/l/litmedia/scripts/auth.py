#!/usr/bin/env python3
"""LitMedia Device Authorization CLI (OAuth 2.0 Device Flow).

Uses the remote LitMedia OAuth service — no local server required.

  python auth.py login   — Full flow: init → open browser → poll → save credentials
  python auth.py poll    — Resume polling a previously started login (recovery only)
  python auth.py status  — Check current login state
  python auth.py logout  — Remove saved credentials

Usage:
    python auth.py login
    python auth.py status
    python auth.py logout
"""

import argparse
import json
import os
import sys
import time
import webbrowser
import hashlib
import platform
from datetime import datetime, timezone
from pathlib import Path
from shared.client import LitMediaClient, LitMediaError

import requests

OAUTH_BASE_URL = os.environ.get(
    "LITMEDIA_OAUTH_URL", "https://litvideo-api.litmedia.ai"
)
# CLIENT_ID = os.environ.get("LITMEDIA_CLIENT_ID", "litmedia-12393716298443")

DEFAULT_SCOPE = "read:profile read:billing read:apikey"

CRED_FILE = Path.home() / ".LitMedia" / "credentials.json"
PENDING_FILE = Path.home() / ".LitMedia" / "pending_device.json"
LOGIN_TIMEOUT = 600  # 10 minutes, matching server-side expiry


# ---------------------------------------------------------------------------
# Credential file helpers
# ---------------------------------------------------------------------------

def _get_pc_fingerprint() -> str:
    """Generate a unique fingerprint for this PC based on hardware info.
    
    The fingerprint will be the same for the same username on the same machine.
    Uses a combination of:
    - Username (ensures same user gets same fingerprint)
    - Machine name
    - Platform
    - Architecture
    - MAC address (if available)
    
    Returns:
        A hashed string representing the PC fingerprint
    """
    # Collect hardware and system information
    fingerprint_data = {
        "username": os.getenv("USERNAME" if os.name == "nt" else "USER"),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "processor": platform.processor(),

    }
    
    print(fingerprint_data)
    # # Try to get MAC address (optional, may not be available on all systems)
    # try:
    #     import uuid
    #     mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
    #                         for elements in range(0, 2 * 6, 2)][::-1])
    #     fingerprint_data["mac"] = mac_addr
    # except Exception:
    #     pass
    
    # Create a deterministic string representation
    fingerprint_string = "|".join([
        f"{key}={fingerprint_data.get(key, '')}"
        for key in sorted(fingerprint_data.keys())
    ])
    
    # Generate SHA-256 hash and format as client ID
    hash_object = hashlib.sha256(fingerprint_string.encode('utf-8'))
    fingerprint_hash = hash_object.hexdigest()
    
    return f"litmedia-skill-{fingerprint_hash[:16]}"

CLIENT_ID = os.environ.get("LITMEDIA_CLIENT_ID", _get_pc_fingerprint())

def _save_credentials(data: dict) -> None:
    """Persist user credentials returned by the OAuth APPROVED response."""
    CRED_FILE.parent.mkdir(parents=True, exist_ok=True)

    api_keys = data.get("api_keys", [])
    api_key = api_keys[0] if api_keys else ""

    creds = {
        "uid": data.get("uid", ""),
        "api_key": api_key,
        "email": data.get("email", ""),
        "name": data.get("name", ""),
        "team_id": data.get("team_id", ""),
        "role": data.get("role", ""),
        "charge_type": data.get("charge_type", ""),
        "remain_credit": data.get("remain_credit"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if data.get("access_token"):
        creds["access_token"] = data["access_token"]
        creds["token_type"] = data.get("token_type", "Bearer")

    CRED_FILE.write_text(json.dumps(creds, indent=2))
    CRED_FILE.chmod(0o600)


def _load_credentials() -> dict | None:
    if not CRED_FILE.exists():
        return None
    try:
        return json.loads(CRED_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _delete_credentials() -> bool:

    if CRED_FILE.exists():
        if _device_unint():
            CRED_FILE.unlink()
            return True
        
    return False


def _mask_key(key: str) -> str:
    if len(key) <= 8:
        return "***"
    return key[:4] + "..." + key[-4:]


# ---------------------------------------------------------------------------
# Core polling logic (shared by login and poll)
# ---------------------------------------------------------------------------

def _poll_for_approval(device_code: str, token_endpoint: str, interval: int) -> None:
    """Poll token_endpoint until APPROVED, DENIED, EXPIRED, or timeout.

    On APPROVED: saves credentials and cleans up pending file.
    On failure:  prints error to stderr and calls sys.exit(1).
    """
    print("Waiting for authorization (Ctrl+C to cancel)...", file=sys.stderr)

    poll_interval = interval
    start = time.time()

    try:
        while time.time() - start < LOGIN_TIMEOUT:
            time.sleep(poll_interval)
            elapsed = int(time.time() - start)
            print(f"  [{elapsed}s] checking...", file=sys.stderr, end="\r")

            try:
                resp = requests.post(
                    token_endpoint,
                    json={"token": device_code},
                    headers={"Monimaster-Device-Type": "110"},
                    timeout=10,
                )

            except requests.RequestException:
                continue

            if resp.status_code == 200:
                result = resp.json()
                print(f"token_endpoint resp: {result}")

                respo_data = result.get("data", {})
                status = respo_data.get("status", "")

                if status in ("INITIATED", "PENDING"):
                    poll_interval = result.get("interval", poll_interval)
                    continue

                if status == "APPROVED":
                    _save_credentials(respo_data)
                    PENDING_FILE.unlink(missing_ok=True)

                    api_keys = respo_data.get("api_keys", [])
                    api_key = api_keys[0] if api_keys else "(none)"

                    print()
                    print()
                    print("  Logged in successfully!")
                    print(f"  uid:         {respo_data.get('uid', '')}")
                    print(f"  email:       {respo_data.get('email', '')}")
                    print(f"  name:        {respo_data.get('name', '')}")
                    print(f"  api_key:     {_mask_key(api_key)}")
                    print(f"  charge_type: {respo_data.get('charge_type', '')}")
                    print(f"  Saved to:    {CRED_FILE}")
                    print()
                    return

            if resp.status_code == 403:
                print(
                    "\nAuthorization denied: the user rejected the request.",
                    file=sys.stderr,
                )
                PENDING_FILE.unlink(missing_ok=True)
                sys.exit(1)

            if resp.status_code == 410:
                print(
                    "\nSession expired. Run `auth.py login` to start a new session.",
                    file=sys.stderr,
                )
                PENDING_FILE.unlink(missing_ok=True)
                sys.exit(1)

            if resp.status_code == 404:
                print(
                    "\nError: device code not found. Run `auth.py login` again.",
                    file=sys.stderr,
                )
                PENDING_FILE.unlink(missing_ok=True)
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nPolling cancelled.", file=sys.stderr)
        sys.exit(130)

    print(
        f"\nTimeout: no authorization received within {LOGIN_TIMEOUT}s.",
        file=sys.stderr,
    )
    PENDING_FILE.unlink(missing_ok=True)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_login(args) -> None:
    """Full login flow: init device code → open browser → poll until done."""
    try:

        _delete_credentials()

        resp = requests.post(
            f"{OAUTH_BASE_URL}/oauth/api/device/init",
            json={
                "client_id": CLIENT_ID
            },
            headers={"Monimaster-Device-Type": "110"},
            timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: could not reach OAuth server: {e}", file=sys.stderr)
        sys.exit(1)
    respose = resp.json()
    data = respose.get("data")
    print(f"init resp: {respose}")

    device_code = data["device_code"]
    verification_url = data.get("verification_uri_complete") or data.get("verification_uri", "")
    token_endpoint = data.get("token_endpoint", "")
    interval = data.get("interval", 2)
    expires_in = max(data.get("expires_in", 600), 600)

    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps({
        "device_code": device_code,
        "token_endpoint": token_endpoint,
        "interval": interval,
        "expires_in": expires_in,
        "verification_uri_complete": verification_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))

    print()
    print("  Authorization page opened in your browser.")
    print(f"  URL: {verification_url}")
    print(f"  Please log in (if needed) and click 'Authorize'.")
    print(f"  Session expires in {expires_in // 60} minutes.")
    print()

    webbrowser.open(verification_url)

    _poll_for_approval(device_code, token_endpoint, interval)


def cmd_poll(args) -> None:
    """Resume polling a previously started login (recovery if login was interrupted)."""
    if not PENDING_FILE.exists():
        print(
            "Error: no pending login found. Run `auth.py login` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        pending = json.loads(PENDING_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: could not read pending device file: {e}", file=sys.stderr)
        sys.exit(1)

    _poll_for_approval(
        pending["device_code"],
        pending["token_endpoint"],
        pending.get("interval", 2),
    )


def cmd_logout(args) -> None:
    if _delete_credentials():
        print(f"Logged out. Removed {CRED_FILE}")
    else:
        print("Not logged in (no credentials file found).")


def cmd_status(args) -> None:
    creds = _load_credentials()
    if creds is None:
        print("Not logged in.")
        print("Run: python auth.py login")
        sys.exit(1)

    uid = creds.get("uid", "(unknown)")
    api_key = creds.get("api_key", "")
    email = creds.get("email", "")
    name = creds.get("name", "")
    charge_type = creds.get("charge_type", "")
    created_at = creds.get("created_at", "(unknown)")

    print("Logged in")
    print(f"  uid:         {uid}")
    if name:
        print(f"  name:        {name}")
    if email:
        print(f"  email:       {email}")
    print(f"  api_key:     {_mask_key(api_key)}")
    if charge_type:
        print(f"  charge_type: {charge_type}")
    print(f"  authorized:  {created_at}")
    print(f"  file:        {CRED_FILE}")


def _device_unint() -> bool:
    """Unbind device account"""
    try:
        client = LitMediaClient()
        result = client.post_nocheck("/user/get-unbind-device")
        # print(f"unbind-device resp: {result}")
        
        code = result.get("code", 0)
        data = result.get("data", False)
        
        if code == 1053 or (code == 200 and data is True):
            # print("Device unbind success")
            return True
        else:
            print(f"Device unbind failed: {result.get('msg', 'Unknown error')}")
            return False
            
    except requests.RequestException as e:
        print(f"Error: could not reach OAuth server: {e}")
        return False
    except Exception as e:
        print(f"Error during device unbind: {e}")
        return False


def cmd_account_switch(args) -> None:
    """Switch account"""
    # print("Switching account...")
    # _device_unint()
    _delete_credentials()
    cmd_login(args)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LitMedia Device Authorization — log in via browser and save credentials.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Subcommands:
  login   Full flow: open browser → wait for authorization → save credentials
  poll    Resume a previously interrupted login (recovery only)
  logout  Remove saved credentials
  status  Show current login state
  accountswitch  Account switching

Examples:
  python auth.py login     # complete login flow (opens browser, waits, saves)
  python auth.py status    # check if logged in
  python auth.py logout    # remove credentials
  python auth.py accountswitch    # Account switching
""",
    )
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    sub.add_parser("login",  help="Open browser for authorization, wait, save credentials")
    sub.add_parser("poll",   help="Resume a previously interrupted login")
    sub.add_parser("logout", help="Remove saved credentials")
    sub.add_parser("status", help="Show current login state")
    sub.add_parser("accountswitch", help="Account switching")

    args = parser.parse_args()

    handlers = {
        "login": cmd_login,
        "poll": cmd_poll,
        "logout": cmd_logout,
        "status": cmd_status,
        "accountswitch": cmd_account_switch,
    }
    handlers[args.subcommand](args)


if __name__ == "__main__":
    main()
