#!/usr/bin/env python3
"""
Enable Banking — Session Renewal
Renews an expired or expiring session for an existing mandant.

Usage:
    python renew.py --mandant-id mueller
    python renew.py --mandant-id mueller --code <auth-code>
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add parent to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.auth import (
    load_config,
    generate_jwt,
    api_request,
    load_mandant,
    save_mandant,
    PENDING_DIR,
)


# ---------------------------------------------------------------------------
# Auth flow (same as onboard)
# ---------------------------------------------------------------------------

def start_auth(config: dict, token: str, bank_name: str, country: str, psu_type: str, callback_url: str) -> dict | None:
    """POST /auth to get redirect URL and state."""
    payload = {
        "aspsp": {
            "name": bank_name,
            "country": country,
        },
        "state": f"openclaw-renew-{int(time.time())}",
        "redirect_url": callback_url,
        "psu_type": psu_type,
        "app": {
            "name": "FinRobotics",
            "description": "Bank data integration for tax advisors",
        },
        "accounts": [{"iban": None}],
        "scopes": ["aiia.accounts", "aiia.balances", "aiia.transactions"],
    }
    return api_request("POST", "/auth", token, json=payload)


def create_session(token: str, code: str) -> dict | None:
    """POST /sessions with authorization code."""
    return api_request("POST", "/sessions", token, json={"code": code})


def poll_for_callback(state: str, timeout: int = 300, interval: int = 2) -> str | None:
    """Poll pending_callbacks/{state}.json until code appears or timeout."""
    path = PENDING_DIR / f"{state}.json"
    deadline = time.time() + timeout
    print(f"⏳ Waiting for callback (state={state}, timeout={timeout}s)...", file=sys.stderr)

    while time.time() < deadline:
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            code = data.get("code")
            if code:
                path.unlink(missing_ok=True)
                return code
        time.sleep(interval)

    print(f"❌ Timeout waiting for callback ({timeout}s)", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Enable Banking — Session Renewal")
    parser.add_argument("--mandant-id", required=True, help="Mandant to renew")
    parser.add_argument("--code", help="Manual auth code (skip callback polling)")
    parser.add_argument("--callback-url", help="Override callback URL")
    args = parser.parse_args()

    # Load existing mandant
    mandant = load_mandant(args.mandant_id)
    bank_name = mandant["bank"]
    country = mandant.get("country", "DE")
    psu_type = mandant.get("psuType", "personal")

    print(f"🔄 Renewing session for mandant '{args.mandant_id}'", file=sys.stderr)
    print(f"   Bank: {bank_name} ({country})", file=sys.stderr)
    print(f"   Current session: {mandant.get('sessionId', 'N/A')[:16]}...", file=sys.stderr)

    config = load_config()
    token = generate_jwt(config)
    callback_url = args.callback_url or config.get("redirectUrl", "https://enablebanking.com/cp/ob-redirect")

    if args.code:
        # --- Manual code flow ---
        print(f"📡 Creating session with provided code...", file=sys.stderr)
        session_result = create_session(token, args.code)
        if not session_result:
            print("❌ Session creation failed", file=sys.stderr)
            sys.exit(1)
    else:
        # --- Auth flow with callback polling ---
        print(f"🔐 Starting authorization flow...", file=sys.stderr)
        auth_result = start_auth(config, token, bank_name, country, psu_type, callback_url)
        if not auth_result:
            print("❌ Auth flow failed", file=sys.stderr)
            sys.exit(1)

        redirect_url = auth_result.get("url") or auth_result.get("redirect_url")
        state = auth_result.get("state", "")

        if not redirect_url:
            print(f"❌ No redirect URL in response: {auth_result}", file=sys.stderr)
            sys.exit(1)

        print(f"\n🔗 Authorization URL:", file=sys.stderr)
        print(redirect_url)  # stdout
        print(f"\nState: {state}", file=sys.stderr)

        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        code = poll_for_callback(state, timeout=300)
        if not code:
            print("❌ No authorization code received", file=sys.stderr)
            sys.exit(1)

        print(f"✅ Authorization code received", file=sys.stderr)

        token = generate_jwt(config)  # Refresh
        session_result = create_session(token, code)
        if not session_result:
            print("❌ Session creation failed", file=sys.stderr)
            sys.exit(1)

    # --- Update mandant ---
    session_id = session_result.get("session_id") or session_result.get("id")
    if not session_id:
        print(f"❌ No session_id in response: {list(session_result.keys())}", file=sys.stderr)
        sys.exit(1)

    # Extract accounts
    raw_accounts = session_result.get("accounts", [])
    accounts = []
    for acc in raw_accounts:
        accounts.append({
            "uid": acc.get("uid") or acc.get("id") or acc.get("resource_id", ""),
            "iban": acc.get("iban", ""),
            "name": acc.get("account_holder_name") or acc.get("name", ""),
            "currency": acc.get("currency", "EUR"),
            "product": acc.get("product", ""),
        })

    valid_until = session_result.get("valid_until") or session_result.get("expires_at", "")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Backup old session info
    old_session = mandant.get("sessionId", "")
    old_valid = mandant.get("validUntil", "")

    # Update mandant
    mandant["sessionId"] = session_id
    mandant["validUntil"] = valid_until
    mandant["accounts"] = accounts if accounts else mandant.get("accounts", [])
    mandant["renewedAt"] = now
    mandant["previousSession"] = {
        "sessionId": old_session,
        "validUntil": old_valid,
    }

    save_mandant(args.mandant_id, mandant)

    print(json.dumps(mandant, indent=2, ensure_ascii=False))
    print(f"\n🎉 Session renewed for '{args.mandant_id}': {len(mandant.get('accounts', []))} account(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
