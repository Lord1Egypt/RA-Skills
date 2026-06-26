import json
import os
import time
from pathlib import Path

def config_dir() -> Path:
    return Path(os.getenv("GMAIL_NO_SEND_CONFIG", Path.home() / ".config" / "gmail-no-send"))


def token_path() -> Path:
    return config_dir() / "token.json"


def audit_log_path() -> Path:
    return config_dir() / "audit.log"


def ensure_config_dir():
    config_dir().mkdir(parents=True, exist_ok=True)


def audit_log(action: str, payload: dict | None = None):
    ensure_config_dir()
    entry = {
        "ts": int(time.time()),
        "action": action,
        "payload": payload or {},
    }
    with audit_log_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
