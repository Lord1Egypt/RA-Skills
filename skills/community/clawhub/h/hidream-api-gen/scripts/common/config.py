from __future__ import annotations

import json
import os
from pathlib import Path

# Unified config directory (XDG Base Directory compliant)
CONFIG_DIR = Path.home() / ".config" / "openclaw"
CONFIG_FILE = CONFIG_DIR / "hidream_config.json"


def _ensure_config_dir() -> None:
    """Ensure the config directory exists with secure permissions."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        # Set directory permissions to 700 (rwx------)
        CONFIG_DIR.chmod(0o700)


def get_token() -> str | None:
    """
    Get authorization token from environment variables or config file.
    Priority:
    1. HIDREAM_AUTHORIZATION env var
    2. OPENCLAW_AUTHORIZATION env var (legacy)
    3. ~/.openclaw/.env (Fallback)
    4. ~/.config/openclaw/hidream_config.json (unified config)
    """
    # 1. Check Env
    token = os.getenv("HIDREAM_AUTHORIZATION") or os.getenv("OPENCLAW_AUTHORIZATION")
    if token:
        return token

    # 2. Check ~/.openclaw/.env (Fallback)
    openclaw_env = Path.home() / ".openclaw" / ".env"
    if openclaw_env.exists():
        try:
            with open(openclaw_env, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("HIDREAM_AUTHORIZATION="):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            val = parts[1].strip().strip("'").strip('"')
                            if val:
                                return val
        except Exception:
            pass

    # 3. Check Config File
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("authorization")
        except Exception:
            pass
    return None


def set_token(token: str) -> None:
    """Save authorization token to unified config file."""
    _ensure_config_dir()
    data = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            pass

    data["authorization"] = token
    
    # Write with restrictive permissions
    # Open file with exclusive creation if possible, or truncate
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    # Set file permissions to 600 (rw-------)
    CONFIG_FILE.chmod(0o600)
