"""
keychain_secrets.py — Secure credential loader for homebase

Priority order for each secret:
  1. macOS Keychain (via keyring library)
  2. Environment variable (set by load_dotenv or the shell)
  3. Empty string (will cause a clear error at the call site)

Usage — replace load_dotenv() calls with:
    from core.keychain_secrets import load_google_secrets
    load_google_secrets()

Migration — run once to move .env values into Keychain:
    python3 migrate_to_keychain.py
"""

import os

KEYRING_SERVICE = "openclaw-family-calendar"

# Keys stored in Keychain / env
_SECRET_KEYS = {
    "GOOGLE_CLIENT_ID":     "google-client-id",
    "GOOGLE_CLIENT_SECRET": "google-client-secret",
    "GOOGLE_REFRESH_TOKEN": "google-refresh-token",
}


_LAST_KEYRING_ERROR: str = ""
_KEYRING_IMPORT_FAILED: bool = False


def _try_keyring(keyring_key: str) -> str:
    """Attempt to read a secret from macOS Keychain. Returns '' on any failure.

    On failure, records the exception in module-level _LAST_KEYRING_ERROR so
    callers (e.g. preflight) can surface *why* the read failed instead of
    misreporting the secret as "missing." This matters in launchd-spawned
    daemon contexts where Keychain ACL or backend issues are common.

    If `import keyring` itself fails (the Python interpreter doesn't have the
    package — typically because the script was launched under
    /usr/bin/python3 instead of the homebase venv), sets _KEYRING_IMPORT_FAILED
    so callers can distinguish "environment is broken" from "credentials are
    actually missing." See also `keyring_module_available()`.
    """
    global _LAST_KEYRING_ERROR, _KEYRING_IMPORT_FAILED
    try:
        import keyring as _kr
    except ImportError as e:
        import sys as _sys
        _KEYRING_IMPORT_FAILED = True
        _LAST_KEYRING_ERROR = f"keyring module not installed in interpreter {_sys.executable}: {e}"
        return ""
    try:
        backend = type(_kr.get_keyring()).__name__
        value = _kr.get_password(KEYRING_SERVICE, keyring_key)
        if value is None:
            _LAST_KEYRING_ERROR = f"keyring backend={backend} returned None for {keyring_key}"
            return ""
        return value
    except Exception as e:
        _LAST_KEYRING_ERROR = f"{type(e).__name__}: {e}"
        return ""


def last_keyring_error() -> str:
    """Return the most recent keyring failure reason, or '' if none."""
    return _LAST_KEYRING_ERROR


def keyring_module_available() -> bool:
    """True if `import keyring` succeeds in this interpreter.

    Use this to guard credential-missing alerts: if keyring isn't even
    importable, the credentials may be perfectly fine in Keychain — we just
    can't read them from this interpreter. That's an environment bug, not
    an auth bug, and should NOT trigger user-facing "re-authenticate now"
    notifications. Cheap and idempotent: tries the import directly and
    caches the result on the module-level _KEYRING_IMPORT_FAILED flag.
    Does NOT touch _LAST_KEYRING_ERROR for the success case so callers
    that read last_keyring_error() get the truth about real read failures.
    """
    global _KEYRING_IMPORT_FAILED, _LAST_KEYRING_ERROR
    try:
        import keyring  # noqa: F401
        _KEYRING_IMPORT_FAILED = False
        return True
    except ImportError as e:
        import sys as _sys
        _KEYRING_IMPORT_FAILED = True
        _LAST_KEYRING_ERROR = f"keyring module not installed in interpreter {_sys.executable}: {e}"
        return False


def load_google_secrets() -> None:
    """
    Populate Google OAuth env vars from Keychain (preferred) or .env fallback.
    Call this instead of load_dotenv() at the top of each script.
    """
    import pathlib

    # Step 1: Try Keychain for each key
    keychain_loaded = []
    for env_key, kr_key in _SECRET_KEYS.items():
        if not os.environ.get(env_key):
            value = _try_keyring(kr_key)
            if value:
                os.environ[env_key] = value
                keychain_loaded.append(env_key)

    if len(keychain_loaded) == len(_SECRET_KEYS):
        return  # All secrets came from Keychain — .env not needed

    # Step 2: Fall back to .env file if Keychain is empty/unavailable
    skill_dir = pathlib.Path(__file__).parent.parent
    env_file  = skill_dir / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            # Manual parse as last resort
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        if k.strip() not in os.environ:
                            os.environ[k.strip()] = v.strip()


def store_secret(env_key: str, value: str) -> bool:
    """Store a single secret in macOS Keychain. Returns True on success."""
    kr_key = _SECRET_KEYS.get(env_key)
    if not kr_key:
        print(f"Unknown secret key: {env_key}")
        return False
    try:
        import keyring as _kr
        _kr.set_password(KEYRING_SERVICE, kr_key, value)
        return True
    except Exception as e:
        print(f"Keychain write failed for {env_key}: {e}")
        return False


def verify_secrets() -> list[str]:
    """Return a list of missing required secrets (for startup health checks)."""
    load_google_secrets()
    missing = []
    for env_key in _SECRET_KEYS:
        if not os.environ.get(env_key):
            missing.append(env_key)
    return missing
