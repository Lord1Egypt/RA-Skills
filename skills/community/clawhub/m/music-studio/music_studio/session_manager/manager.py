"""
Session Manager — 会话历史管理，支持多会话、消息记录、自动清理。
会话数据存在 output/sessions/ 目录下。
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any

from music_studio import config


SESSIONS_DIR = lambda: config.get_output_dir() / "sessions"
SESSIONS_INDEX = lambda: SESSIONS_DIR() / "sessions.json"
ACTIVE_FILE = lambda: SESSIONS_DIR() / ".active"


def _ensure_dir() -> None:
    SESSIONS_DIR().mkdir(parents=True, exist_ok=True)


def _read_index() -> dict[str, Any]:
    _ensure_dir()
    if not SESSIONS_INDEX().exists():
        return {"sessions": []}
    with open(SESSIONS_INDEX()) as f:
        return json.load(f)


def _write_index(data: dict[str, Any]) -> None:
    _ensure_dir()
    with open(SESSIONS_INDEX(), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _session_path(sid: str) -> Path:
    return SESSIONS_DIR() / f"{sid}.json"


def _read_session(sid: str) -> dict[str, Any]:
    p = _session_path(sid)
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def _write_session(sid: str, data: dict[str, Any]) -> None:
    _ensure_dir()
    p = _session_path(sid)
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _touch_index(sid: str, entry: dict[str, Any]) -> None:
    idx = _read_index()
    sessions = idx.get("sessions", [])
    for i, s in enumerate(sessions):
        if s["id"] == sid:
            sessions[i] = entry
            break
    else:
        sessions.insert(0, entry)
    _write_index({"sessions": sessions})


def _remove_from_index(sid: str) -> None:
    idx = _read_index()
    idx["sessions"] = [s for s in idx.get("sessions", []) if s["id"] != sid]
    _write_index(idx)


def clean_expired(max_age_days: int = 30) -> int:
    idx = _read_index()
    cutoff = datetime.now().astimezone() - timedelta(days=max_age_days)
    surviving = []
    removed = 0

    for entry in idx.get("sessions", []):
        updated = entry.get("updated", "")
        try:
            updated_dt = datetime.fromisoformat(updated)
        except Exception:
            updated_dt = cutoff

        if updated_dt >= cutoff:
            surviving.append(entry)
        else:
            p = _session_path(entry["id"])
            if p.exists():
                p.unlink()
            if get_active_id() == entry["id"]:
                clear_active()
            removed += 1

    _write_index({"sessions": surviving})
    return removed


def list_sessions(limit: int = 20) -> list[dict[str, Any]]:
    clean_expired()
    idx = _read_index()
    return idx.get("sessions", [])[:limit]


def get_session(sid: str) -> dict[str, Any]:
    return _read_session(sid)


def delete_session(sid: str) -> bool:
    if _session_path(sid).exists():
        _session_path(sid).unlink()
    _remove_from_index(sid)
    if get_active_id() == sid:
        clear_active()
    return True


def create_session(s_type: str = "general", title: Optional[str] = None) -> dict[str, Any]:
    clean_expired()
    sid = str(uuid.uuid4())
    now = _now()
    session = {
        "id": sid,
        "type": s_type,
        "title": title or f"{s_type}-{now[5:16]}",
        "created": now,
        "updated": now,
        "messages": [],
        "state": "idle",
        "step": 0,
        "params": {},
    }
    _write_session(sid, session)
    _touch_index(sid, {
        "id": sid,
        "type": s_type,
        "title": session["title"],
        "created": now,
        "updated": now,
    })
    _set_active(sid)
    return session


def append_message(sid: str, role: str, content: str) -> None:
    session = _read_session(sid)
    now = _now()
    session.setdefault("messages", []).append({
        "role": role,
        "content": content,
        "time": now,
    })
    session["updated"] = now
    _write_session(sid, session)

    idx = _read_index()
    for entry in idx.get("sessions", []):
        if entry["id"] == sid:
            entry["updated"] = now
            if "title" not in entry:
                entry["title"] = session.get("title", "")
            break
    _write_index(idx)


def update_session_state(sid: str, state: str, step: int, params: dict[str, Any]) -> None:
    session = _read_session(sid)
    session["state"] = state
    session["step"] = step
    session["params"] = params
    session["updated"] = _now()
    _write_session(sid, session)


def _set_active(sid: str) -> None:
    _ensure_dir()
    ACTIVE_FILE().write_text(sid)


def get_active_id() -> Optional[str]:
    if not ACTIVE_FILE().exists():
        return None
    sid = ACTIVE_FILE().read_text().strip()
    if not sid or not _session_path(sid).exists():
        return None
    return sid


def get_active() -> dict[str, Any]:
    sid = get_active_id()
    if not sid:
        return {}
    return _read_session(sid)


def clear_active() -> None:
    if ACTIVE_FILE().exists():
        ACTIVE_FILE().unlink()


def resume_session(sid: str) -> dict[str, Any]:
    clean_expired()
    session = _read_session(sid)
    if not session:
        raise ValueError(f"会话 {sid} 不存在")
    _set_active(sid)
    return session
