#!/usr/bin/env python3
"""
Monarch Money One-Time Login Setup

Authenticate with Monarch Money and save a session pickle.
The session is reused by monarch.py for all subsequent API calls.

Usage:
    python3 login_setup.py
"""

import asyncio
import sys
from pathlib import Path

try:
    from monarchmoney import MonarchMoney
except ImportError:
    print("Error: monarchmoney library not installed.")
    print("Install with: pip install monarchmoney")
    sys.exit(1)


TOKEN_DIR = Path.home() / ".monarchmoney"
SESSION_FILE = TOKEN_DIR / "mm_session.pickle"


async def main():
    mm = MonarchMoney()

    if SESSION_FILE.exists():
        print(f"Existing session found at {SESSION_FILE}")
        response = input("Re-authenticate? (y/N): ").strip().lower()
        if response != "y":
            print("Using existing session. Run monarch.py to test.")
            return

    print("\n=== Monarch Money Login ===\n")

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not email or not password:
        print("Error: Email and password are required.")
        sys.exit(1)

    try:
        print("\nAuthenticating...")
        await mm.login(email, password)
        print("Login successful!")
    except Exception as e:
        error_msg = str(e).lower()
        if "mfa" in error_msg or "multi" in error_msg or "factor" in error_msg:
            print("\nMFA required. Enter your verification code.")
            mfa_code = input("MFA Code: ").strip()
            try:
                await mm.multi_factor_authenticate(email, password, mfa_code)
                print("MFA login successful!")
            except Exception as mfa_e:
                print(f"MFA authentication failed: {mfa_e}")
                sys.exit(1)
        else:
            print(f"Login failed: {e}")
            sys.exit(1)

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    mm.save_session(str(SESSION_FILE))
    print(f"\nSession saved to {SESSION_FILE}")
    print("You can now use monarch.py to query your financial data.")
    print("Sessions persist for months, re-run this only if auth expires.")


if __name__ == "__main__":
    asyncio.run(main())
