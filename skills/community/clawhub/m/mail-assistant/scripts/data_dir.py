"""
Email Assistant — Data directory resolution & secure credential storage.

Accounts, tokens, sync state, and auto-reply rules are stored in a
persistent data directory OUTSIDE the skill folder.

This ensures user data survives skill updates (clawhub update replaces
the skill folder entirely).

Resolution order:
1. Environment variable: EMAIL_ASSISTANT_DATA_DIR
2. OpenClaw workspace root: ~/.openclaw/workspace/.email-assistant/
3. Skill-adjacent fallback (old behavior, not recommended)

Secure storage:
- Uses system keyring (keyring library) for credential encryption
- Falls back to plaintext JSON if keyring is unavailable
- Cross-platform: Windows Credential Manager, macOS Keychain, Linux Secret Service
"""

import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_NAME = os.path.basename(SKILL_DIR)

# ── Keyring (Secure Credential Storage) ───────────────────────────────

_KEYRING_SERVICE = "email-assistant"
_HAS_KEYRING = False

try:
    import keyring as _kr
    # Test that keyring is functional (some headless Linux may have the
    # library but no backend configured)
    _kr.get_password(_KEYRING_SERVICE, "__probe__")
    _HAS_KEYRING = True
except Exception:
    _HAS_KEYRING = False


def has_keyring():
    """Check if system keyring is available and functional."""
    return _HAS_KEYRING


def secure_get(key, field="auth"):
    """
    Read a credential from the system keyring.
    Falls back to reading from account JSON if keyring is unavailable.

    Args:
        key: account_id or similar identifier (e.g. "my-163")
        field: credential field name (default "auth")
               For OAuth tokens use field="token"
    Returns:
        Plaintext credential string, or None if not found.
    """
    if _HAS_KEYRING:
        try:
            val = _kr.get_password(_KEYRING_SERVICE, f"{key}:{field}")
            if val:
                return val
        except Exception:
            pass
    return None


def secure_set(key, value, field="auth"):
    """
    Store a credential in the system keyring.
    If keyring is unavailable, the caller should store in JSON normally.

    Args:
        key: account_id (e.g. "my-163")
        value: plaintext credential string
        field: credential field name (default "auth")
    Returns:
        True if stored in keyring, False if keyring unavailable.
    """
    if _HAS_KEYRING:
        try:
            _kr.set_password(_KEYRING_SERVICE, f"{key}:{field}", value)
            return True
        except Exception:
            pass
    return False


def secure_delete(key, field="auth"):
    """
    Delete a credential from the system keyring.
    Returns True if deleted, False if not found or keyring unavailable.
    """
    if _HAS_KEYRING:
        try:
            _kr.delete_password(_KEYRING_SERVICE, f"{key}:{field}")
            return True
        except (Exception, _kr.errors.PasswordDeleteError):
            pass
    return False


def secure_get_token(account_id):
    """
    Load OAuth token dict from keyring.
    Tokens are stored as JSON string under field="token".

    Falls back to plain .token.json file if keyring unavailable.
    """
    if _HAS_KEYRING:
        try:
            raw = _kr.get_password(_KEYRING_SERVICE, f"{account_id}:token")
            if raw:
                return json.loads(raw)
        except Exception:
            pass
    return None


def secure_set_token(account_id, token_dict):
    """
    Store OAuth token dict in keyring as JSON string.
    Returns True if stored, False if keyring unavailable.
    """
    if _HAS_KEYRING:
        try:
            _kr.set_password(_KEYRING_SERVICE, f"{account_id}:token",
                             json.dumps(token_dict))
            return True
        except Exception:
            pass
    return False


def secure_delete_token(account_id):
    """
    Delete OAuth token from keyring.
    Returns True if deleted.
    """
    if _HAS_KEYRING:
        try:
            _kr.delete_password(_KEYRING_SERVICE, f"{account_id}:token")
            return True
        except (Exception, _kr.errors.PasswordDeleteError):
            pass
    return False


# ── User Consent Helper ────────────────────────────────────────────────


def confirm_action(description, args=None):
    """
    Prompt the user for consent before performing a destructive action.
    Skips the prompt if '--yes' is in args (for agent use after user has
    already consented at a higher level).

    Args:
        description: Human-readable description of the action.
        args: Optional list of CLI args; if '--yes' is present, auto-confirms.

    Returns:
        True if user confirmed (or --yes was passed), False otherwise.
    """
    # If --yes flag is present, auto-confirm
    if args and "--yes" in args:
        return True

    # For non-interactive mode (stdin not a TTY), refuse by default
    if not sys.stdin.isatty():
        print(f"[CONFIRM] {description}")
        print(f"[CONFIRM] 未检测到交互终端，操作被拒绝。若为 Agent 调用请使用 --yes 参数。",
              file=sys.stderr)
        return False

    print(f"\n⚠️  需要确认：{description}")
    try:
        answer = input("  是否继续？(y/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer in ("y", "yes", "是")


# ── Data Directory ─────────────────────────────────────────────────────


def _resolve_data_dir():
    """Resolve the persistent data directory."""
    # 1. Environment variable takes priority
    env_dir = os.environ.get("EMAIL_ASSISTANT_DATA_DIR")
    if env_dir:
        return env_dir

    # 2. OpenClaw workspace root (survives skill updates)
    workspace_root = os.path.expanduser("~/.openclaw/workspace")
    data_dir = os.path.join(workspace_root, ".email-assistant")
    if os.path.isdir(workspace_root):
        return data_dir

    # 3. Fallback: within skill directory (old behavior)
    return SKILL_DIR


DATA_DIR = _resolve_data_dir()
ACCOUNTS_DIR = os.path.join(DATA_DIR, "accounts")
SYNC_STATE_PATH = os.path.join(DATA_DIR, "sync_state.json")
RULES_PATH = os.path.join(DATA_DIR, "auto_reply_rules.json")


def ensure_data_dirs():
    """Create data directories if they don't exist."""
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)
    for path in [SYNC_STATE_PATH, RULES_PATH]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("[]" if "rules" in path else "{}")


def debug_info():
    """Print data directory info for debugging."""
    return {
        "skill_dir": SKILL_DIR,
        "data_dir": DATA_DIR,
        "accounts_dir": ACCOUNTS_DIR,
        "sync_state": SYNC_STATE_PATH,
        "rules_path": RULES_PATH,
        "keyring_available": _HAS_KEYRING,
    }
