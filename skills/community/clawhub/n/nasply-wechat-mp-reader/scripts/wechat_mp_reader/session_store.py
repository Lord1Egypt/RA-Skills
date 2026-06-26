from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_SESSION_PATH = Path(__file__).resolve().parents[1] / "cache" / "session.json"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_session_file(path: str | None = None) -> dict[str, str]:
    target = Path(path) if path else DEFAULT_SESSION_PATH
    if not target.exists():
        return {"cookie": "", "token": ""}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return {"cookie": "", "token": ""}
    return {
        "cookie": str(data.get("cookie", "") or "").strip(),
        "token": str(data.get("token", "") or "").strip(),
    }


def save_session_file(session: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else DEFAULT_SESSION_PATH
    _ensure_parent(target)
    data = {
        "cookie": str(session.get("cookie", "") or "").strip(),
        "token": str(session.get("token", "") or "").strip(),
    }
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def load_session_from_env() -> dict[str, str]:
    return {
        "cookie": os.environ.get("WECHAT_MP_COOKIE", "").strip(),
        "token": os.environ.get("WECHAT_MP_TOKEN", "").strip(),
    }


def resolve_session(path: str | None = None) -> dict[str, str]:
    env = load_session_from_env()
    if env["cookie"] and env["token"]:
        return env
    return load_session_file(path)
