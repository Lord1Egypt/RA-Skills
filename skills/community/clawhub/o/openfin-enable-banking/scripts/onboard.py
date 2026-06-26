#!/usr/bin/env python3
"""
Enable Banking — Mandant Onboarding
Connects a new mandant to their bank via PSD2 OAuth2.

Usage:
    python onboard.py --bank "Sparkasse Karlsruhe" --country DE --mandant-id mueller
    python onboard.py --bank "Sparkasse Karlsruhe" --mandant-id mueller --code <auth-code>
    python onboard.py --list-banks --country DE
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
    save_mandant,
    PENDING_DIR,
    SKILL_DIR,
)


# ---------------------------------------------------------------------------
# Bank listing
# ---------------------------------------------------------------------------

def list_banks(token: str, country: str) -> list:
    """Fetch available banks (ASPSPs) for a country."""
    result = api_request("GET", f"/aspsps?country={country}", token)
    if result is None:
        return []
    return result if isinstance(result, list) else result.get("aspsps", [])


# ---------------------------------------------------------------------------
# Auth flow
# ---------------------------------------------------------------------------

def start_auth(config: dict, token: str, bank_name: str, country: str, psu_type: str, callback_url: str) -> dict | None:
    """POST /auth to get redirect URL and state."""
    payload = {
        "aspsp": {
            "name": bank_name,
            "country": country,
        },
        "state": f"openclaw-{int(time.time())}",
        "redirect_url": callback_url,
        "psu_type": psu_type,
        "app": {
            "name": "FinRobotics",
            "description": "Bank data integration for tax advisors",
        },
        "accounts": [{"iban": None}],  # Request all accounts
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
                # Clean up
                path.unlink(missing_ok=True)
                return code
        time.sleep(interval)

    print(f"❌ Timeout waiting for callback ({timeout}s)", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Session processing
# ---------------------------------------------------------------------------

def process_session(session_result: dict, mandant_id: str, bank_name: str, country: str, psu_type: str) -> dict:
    """Process session result and save mandant file."""
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

    # Calculate valid_until from session
    valid_until = session_result.get("valid_until") or session_result.get("expires_at", "")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    mandant_data = {
        "mandantId": mandant_id,
        "bank": bank_name,
        "country": country,
        "psuType": psu_type,
        "sessionId": session_id,
        "accounts": accounts,
        "validUntil": valid_until,
        "createdAt": now,
        "lastFetch": None,
    }

    save_mandant(mandant_id, mandant_data)
    return mandant_data


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Enable Banking — Mandant Onboarding")
    parser.add_argument("--mandant-id", help="Unique mandant identifier (required for onboarding)")
    parser.add_argument("--bank", help="Bank name (partial match)")
    parser.add_argument("--country", default="DE", help="Country code (default: DE)")
    parser.add_argument("--psu-type", default="personal", choices=["personal", "business"], help="PSU type")
    parser.add_argument("--code", help="Manual auth code (skip callback polling)")
    parser.add_argument("--callback-url", help="Override callback URL")
    parser.add_argument("--list-banks", action="store_true", help="List available banks and exit")
    args = parser.parse_args()

    config = load_config()
    token = generate_jwt(config)

    # --- List banks mode ---
    if args.list_banks:
        country = args.country.upper()
        banks = list_banks(token, country)
        if not banks:
            print(f"No banks found for {country}", file=sys.stderr)
            sys.exit(0)

        print(f"\n🏦 Available banks — {country}\n", file=sys.stderr)
        for i, bank in enumerate(banks, 1):
            name = bank.get("name", "Unknown")
            sandbox = "🟡 sandbox" if bank.get("sandboxMode") else "🟢 live"
            print(f"  {i:3}. {name} — {sandbox}", file=sys.stderr)
        print(f"\n  Total: {len(banks)} banks", file=sys.stderr)
        sys.exit(0)

    # --- Onboarding mode ---
    if not args.mandant_id:
        print("❌ --mandant-id is required", file=sys.stderr)
        sys.exit(1)
    if not args.bank:
        print("❌ --bank is required", file=sys.stderr)
        sys.exit(1)

    # Check if mandant already exists
    mandant_path = SKILL_DIR / "mandanten" / f"{args.mandant_id}.json"
    if mandant_path.exists():
        print(f"⚠️  Mandant '{args.mandant_id}' already exists. Use renew.py to refresh session.", file=sys.stderr)
        sys.exit(1)

    # Find bank
    banks = list_banks(token, args.country.upper())
    matches = [b for b in banks if args.bank.lower() in b.get("name", "").lower()]

    if len(matches) == 0:
        print(f"❌ No bank found matching '{args.bank}'", file=sys.stderr)
        sys.exit(1)
    elif len(matches) > 1:
        # Try exact match first
        exact = [b for b in matches if b.get("name", "").lower() == args.bank.lower()]
        if len(exact) == 1:
            matches = exact
        else:
            print(f"⚠️  Multiple matches for '{args.bank}':", file=sys.stderr)
            for m in matches[:10]:
                print(f"    - {m['name']}", file=sys.stderr)
            print("  Be more specific.", file=sys.stderr)
            sys.exit(1)

    selected_bank = matches[0]
    bank_name = selected_bank["name"]
    bank_country = selected_bank.get("country", args.country.upper())

    print(f"✅ Bank: {bank_name}", file=sys.stderr)

    # Determine callback URL
    callback_url = args.callback_url or config.get("redirectUrl", "https://enablebanking.com/cp/ob-redirect")

    if args.code:
        # --- Manual code flow ---
        print(f"📡 Creating session with provided code...", file=sys.stderr)
        # Regenerate token in case it's needed fresh
        token = generate_jwt(config)
        session_result = create_session(token, args.code)
        if not session_result:
            print("❌ Session creation failed", file=sys.stderr)
            sys.exit(1)

        mandant_data = process_session(session_result, args.mandant_id, bank_name, bank_country, args.psu_type)
        print(json.dumps(mandant_data, indent=2, ensure_ascii=False))
        print(f"\n🎉 Mandant '{args.mandant_id}' onboarded: {len(mandant_data['accounts'])} account(s)", file=sys.stderr)
    else:
        # --- Auth flow with callback polling ---
        print(f"🔐 Starting authorization flow...", file=sys.stderr)
        auth_result = start_auth(config, token, bank_name, bank_country, args.psu_type, callback_url)
        if not auth_result:
            print("❌ Auth flow failed", file=sys.stderr)
            sys.exit(1)

        redirect_url = auth_result.get("url") or auth_result.get("redirect_url")
        state = auth_result.get("state", "")

        if not redirect_url:
            print(f"❌ No redirect URL in response: {auth_result}", file=sys.stderr)
            sys.exit(1)

        # Output the URL for the agent to forward
        print(f"\n🔗 Authorization URL:", file=sys.stderr)
        print(redirect_url)  # stdout — agent can capture this
        print(f"\nState: {state}", file=sys.stderr)

        # Poll for callback
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        code = poll_for_callback(state, timeout=300)
        if not code:
            print("❌ No authorization code received", file=sys.stderr)
            sys.exit(1)

        print(f"✅ Authorization code received", file=sys.stderr)

        # Create session
        print(f"📡 Creating session...", file=sys.stderr)
        token = generate_jwt(config)  # Refresh token
        session_result = create_session(token, code)
        if not session_result:
            print("❌ Session creation failed", file=sys.stderr)
            sys.exit(1)

        mandant_data = process_session(session_result, args.mandant_id, bank_name, bank_country, args.psu_type)
        print(json.dumps(mandant_data, indent=2, ensure_ascii=False))
        print(f"\n🎉 Mandant '{args.mandant_id}' onboarded: {len(mandant_data['accounts'])} account(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
