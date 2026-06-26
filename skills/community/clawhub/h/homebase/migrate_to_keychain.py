#!/usr/bin/env python3
"""
migrate_to_keychain.py — One-time migration of Google credentials from .env to macOS Keychain.

Run once:
    python3 migrate_to_keychain.py

After successful migration:
    - Credentials are stored securely in macOS Keychain
    - You can optionally delete or empty .env (the code will fall back to Keychain)
    - All scripts will prefer Keychain over .env automatically
"""

import os
import sys
import pathlib

SKILL_DIR = pathlib.Path(__file__).parent
ENV_FILE  = SKILL_DIR / ".env"

KEYS_TO_MIGRATE = {
    "GOOGLE_CLIENT_ID":     "google-client-id",
    "GOOGLE_CLIENT_SECRET": "google-client-secret",
    "GOOGLE_REFRESH_TOKEN": "google-refresh-token",
}
KEYRING_SERVICE = "openclaw-family-calendar"


def main():
    # 1. Check keyring is available
    try:
        import keyring  # noqa: F401
    except ImportError:
        print("ERROR: missing dependency 'keyring'. Run: pip install -e .")
        sys.exit(1)

    # 2. Load .env values
    if not ENV_FILE.exists():
        print(f"ERROR: .env not found at {ENV_FILE}")
        sys.exit(1)

    env_values = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env_values[k.strip()] = v.strip()

    # 3. Store each key in Keychain
    success = []
    failed  = []
    for env_key, kr_key in KEYS_TO_MIGRATE.items():
        value = env_values.get(env_key, "").strip()
        if not value:
            print(f"  SKIP  {env_key} — not found in .env")
            continue
        try:
            keyring.set_password(KEYRING_SERVICE, kr_key, value)
            print(f"  OK    {env_key} → Keychain ({KEYRING_SERVICE}/{kr_key})")
            success.append(env_key)
        except Exception as e:
            print(f"  FAIL  {env_key}: {e}")
            failed.append(env_key)

    print()
    if failed:
        print(f"⚠️  {len(failed)} key(s) could not be stored. .env will be used as fallback.")
    else:
        print(f"✅ {len(success)} secret(s) stored in Keychain.")
        print()
        print("You can now optionally remove credentials from .env:")
        print(f"  vim {ENV_FILE}")
        print("  (delete or blank the GOOGLE_* lines — the code will use Keychain instead)")
        print()
        print("To verify Keychain is working:")
        print("  python3 -c \"from keychain_secrets import verify_secrets; print(verify_secrets())\"")


def check_keychain():
    """
    Read each key directly from Keychain (bypassing .env fallback).
    Use this to confirm the migration actually worked.
    """
    try:
        import keyring
    except ImportError:
        print("ERROR: keyring not installed. Run: ./migrate_to_keychain.py first.")
        sys.exit(1)

    backend = type(keyring.get_keyring()).__name__
    print(f"Keychain backend: {backend}")
    if "fail" in backend.lower() or "null" in backend.lower():
        print("⚠️  WARNING: No real Keychain backend found.")
        print("   Make sure you are running this on macOS with Keychain access.")
        print("   If you're in a restricted environment (Docker/VM), Keychain is not available.")

    print()
    all_ok = True
    for env_key, kr_key in KEYS_TO_MIGRATE.items():
        value = keyring.get_password(KEYRING_SERVICE, kr_key)
        if value:
            # Show only first 4 and last 4 chars to confirm it's there without exposing it
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "****"
            print(f"  ✅  {env_key}: found in Keychain ({masked})")
        else:
            print(f"  ❌  {env_key}: NOT found in Keychain")
            all_ok = False
    print()
    if all_ok:
        print("All 3 secrets confirmed in Keychain. Migration is complete.")
    else:
        print("Some secrets are missing from Keychain. Run: ./migrate_to_keychain.py")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check_keychain()
    else:
        main()
