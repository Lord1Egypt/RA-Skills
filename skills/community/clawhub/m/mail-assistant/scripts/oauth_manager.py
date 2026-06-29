#!/usr/bin/env python3
"""
OAuth2 Token Manager for Microsoft Graph (Outlook / M365).

Supports device-code auth flow. Stores tokens alongside account config.

Usage:
    python oauth_manager.py auth <account-config-path>
    python oauth_manager.py refresh <account-id>
    python oauth_manager.py get-token <account-id>
    python oauth_manager.py revoke <account-id>
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

# Force UTF-8 for console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import ACCOUNTS_DIR, secure_set_token, secure_get_token, secure_delete_token, has_keyring


def _load_account(account_id):
    path = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _token_path(account_id):
    return os.path.join(ACCOUNTS_DIR, f"{account_id}.token.json")


def _save_token(account_id, token_data):
    token_data["stored_at"] = time.time()
    # ⚠️ SECURITY: Try system keyring first (encrypted), fallback to JSON
    if secure_set_token(account_id, token_data):
        storage_str = "system keyring" + (" (加密)" if has_keyring() else "")
    else:
        path = _token_path(account_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)
        storage_str = path
    print(f"[OK] Token saved to {storage_str}")


def _load_token(account_id):
    # ⚠️ SECURITY: Try system keyring first (encrypted), fallback to JSON file
    token = secure_get_token(account_id)
    if token is not None:
        return token
    path = _token_path(account_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _http_post(url, data):
    """POST application/x-www-form-urlencoded data."""
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[ERROR] HTTP {e.code}: {body}", file=sys.stderr)
        return None


def _is_expired(token):
    if not token or "stored_at" not in token or "expires_in" not in token:
        return True
    elapsed = time.time() - token["stored_at"]
    return elapsed > token["expires_in"] - 60  # 60s buffer


def cmd_auth(account_config_path):
    """Start device-code auth flow for Outlook/M365."""
    if not os.path.exists(account_config_path):
        print(f"[ERROR] Account config not found: {account_config_path}", file=sys.stderr)
        sys.exit(1)

    with open(account_config_path, "r", encoding="utf-8") as f:
        account = json.load(f)

    if account.get("type") != "outlook":
        print("[ERROR] Only 'outlook' type accounts support OAuth2.", file=sys.stderr)
        sys.exit(1)

    oauth = account.get("oauth", {})
    client_id = oauth.get("client_id")
    tenant_id = oauth.get("tenant_id", "consumers")
    scopes = oauth.get("scopes", ["User.Read", "Mail.ReadWrite", "Mail.Send"])

    if not client_id:
        print("[ERROR] 'oauth.client_id' is required in account config.", file=sys.stderr)
        sys.exit(1)

    scope_str = " ".join(scopes)
    tenant = tenant_id if tenant_id else "consumers"

    # Step 1: Request device code
    device_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode"
    device_data = {"client_id": client_id, "scope": scope_str}
    device_resp = _http_post(device_url, device_data)

    if not device_resp:
        print("[ERROR] Failed to get device code.", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("MICROSOFT ACCOUNT LOGIN")
    print("=" * 60)
    print(f"\n1. Open: {device_resp['verification_uri']}")
    print(f"2. Enter code: {device_resp['user_code']}")
    print(f"\n(This code expires in {device_resp['expires_in']} seconds)")
    print("=" * 60 + "\n")

    # Step 2: Poll for token
    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": client_id,
        "device_code": device_resp["device_code"],
    }

    interval = device_resp.get("interval", 5)
    max_polls = device_resp["expires_in"] // interval

    for attempt in range(max_polls):
        time.sleep(interval)
        result = _http_post(token_url, token_data)
        if result is None:
            continue
        if "access_token" in result:
            _save_token(account["id"], result)
            print("[OK] Authentication successful!")
            return
        if result.get("error") == "authorization_pending":
            continue
        if result.get("error") == "expired_token":
            print("[ERROR] Device code expired. Run `auth` again.", file=sys.stderr)
            sys.exit(1)
        if result.get("error"):
            print(f"[ERROR] {result.get('error_description', result['error'])}", file=sys.stderr)
            sys.exit(1)

    print("[ERROR] Authentication timed out.", file=sys.stderr)
    sys.exit(1)


def cmd_refresh(account_id):
    """Refresh the OAuth2 token."""
    account = _load_account(account_id)
    token = _load_token(account_id)

    if not token or "refresh_token" not in token:
        print("[ERROR] No refresh token found. Run `auth` first.", file=sys.stderr)
        sys.exit(1)

    oauth = account.get("oauth", {})
    client_id = oauth.get("client_id")
    tenant_id = oauth.get("tenant_id", "consumers")
    tenant = tenant_id if tenant_id else "consumers"

    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": token["refresh_token"],
        "scope": " ".join(oauth.get("scopes", ["User.Read", "Mail.ReadWrite", "Mail.Send"])),
    }

    result = _http_post(token_url, data)
    if not result or "access_token" not in result:
        print("[ERROR] Token refresh failed.", file=sys.stderr)
        sys.exit(1)

    _save_token(account_id, result)
    print("[OK] Token refreshed successfully.")


def cmd_get_token(account_id):
    """Get a valid access token (auto-refreshes if needed)."""
    token = _load_token(account_id)
    if not token:
        print("[ERROR] No token found. Run `auth` first.", file=sys.stderr)
        sys.exit(1)

    if _is_expired(token) and "refresh_token" in token:
        cmd_refresh(account_id)
        token = _load_token(account_id)

    if not token or "access_token" not in token:
        print("[ERROR] Unable to get a valid token.", file=sys.stderr)
        sys.exit(1)

    print(token["access_token"])


def cmd_revoke(account_id):
    """Revoke OAuth token: send revocation request to Microsoft, then delete local file."""
    account = _load_account(account_id)
    token = _load_token(account_id)
    path = _token_path(account_id)

    oauth = account.get("oauth", {})
    client_id = oauth.get("client_id")
    tenant_id = oauth.get("tenant_id", "consumers")

    # 1. Attempt HTTP revocation before deleting local file
    if token:
        refresh_token = token.get("refresh_token")
        access_token = token.get("access_token")
        revoke_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/revoke"

        # Revoke the refresh token first (most important for long-lived access)
        if refresh_token and client_id:
            data = {"client_id": client_id, "token": refresh_token, "token_type_hint": "refresh_token"}
            result = _http_post(revoke_url, data)
            if result is not None or True:  # 200 means success (empty body), errors still print
                print(f"[INFO] Token revocation request sent to Microsoft.")
            else:
                print(f"[WARN] Could not send revocation request to Microsoft.", file=sys.stderr)

        # Also revoke access token if we have it
        if access_token and client_id:
            data = {"client_id": client_id, "token": access_token, "token_type_hint": "access_token"}
            _http_post(revoke_url, data)

    # 2. Delete token from keyring (if stored there)
    if secure_delete_token(account_id):
        print(f"[OK] Token deleted from system keyring.")

    # 3. Delete local token file (if keyring was unavailable)
    if os.path.exists(path):
        os.remove(path)
        print(f"[OK] Token file deleted: {path}")

    if not os.path.exists(path) and not secure_delete_token(account_id):
        print("[INFO] No token file found.")

    print("[INFO] To fully revoke server-side consent, also visit: https://account.live.com/consent/Manage")


def get_access_token(account_id):
    """
    Get a valid OAuth access token string (auto-refreshes if needed).
    Returns the token string, or None if unavailable.
    """
    token = _load_token(account_id)
    if not token:
        print(f"[ERROR] No token found for {account_id}. Run `auth` first.", file=sys.stderr)
        return None

    if _is_expired(token) and "refresh_token" in token:
        cmd_refresh(account_id)
        token = _load_token(account_id)

    if not token or "access_token" not in token:
        print(f"[ERROR] Unable to get a valid token for {account_id}.", file=sys.stderr)
        return None

    return token["access_token"]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    commands = {
        "auth": cmd_auth,
        "refresh": cmd_refresh,
        "get-token": cmd_get_token,
        "revoke": cmd_revoke,
    }

    if command not in commands:
        print(f"[ERROR] Unknown command: {command}", file=sys.stderr)
        print(f"  Available: {', '.join(commands.keys())}", file=sys.stderr)
        sys.exit(1)

    commands[command](arg)


if __name__ == "__main__":
    main()
