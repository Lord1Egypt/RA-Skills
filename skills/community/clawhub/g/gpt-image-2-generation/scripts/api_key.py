"""Shared helpers for locating, loading and persisting the WellAPI key."""
from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

ENV_VAR = "WELLAPI_API_KEY"
APP_DIR_NAME = "gpt-image-2-generation"
REGISTER_URL = "https://wellapi.ai/register?channel=c_qqn3vdvc"


def config_dir() -> Path:
    """Return the per-user config directory for this skill.

    Uses ``$XDG_CONFIG_HOME`` when set, otherwise ``~/.config`` on every
    platform (works on Windows too because ``Path.home()`` resolves to the
    user profile).
    """
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        return Path(base) / APP_DIR_NAME
    return Path.home() / ".config" / APP_DIR_NAME


def config_file() -> Path:
    return config_dir() / "config.json"


def load_api_key() -> str | None:
    """Resolve the API key from env var first, then the local config file."""
    key = os.environ.get(ENV_VAR)
    if key:
        return key.strip()

    path = config_file()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        value = data.get("api_key")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def save_api_key(api_key: str) -> Path:
    """Persist the API key to the per-user config file with 0600 perms."""
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("API key is empty.")

    directory = config_dir()
    directory.mkdir(parents=True, exist_ok=True)

    path = config_file()
    payload = {"api_key": api_key}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Best-effort restrict permissions; on Windows chmod is a no-op for these
    # bits but the user profile is already access-controlled.
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass

    return path


def missing_key_message() -> str:
    return (
        "请粘贴你的 WellAPI API Key。\n"
        f"如果还没有，请前往 {REGISTER_URL} 注册后领取免费 API Key。\n"
        "Please paste your WellAPI API Key.\n"
        f"If you don't have one yet, register at {REGISTER_URL} to get a free key."
    )


def require_api_key() -> str:
    key = load_api_key()
    if not key:
        print(missing_key_message(), file=sys.stderr)
        sys.exit(2)
    return key
