#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load(path: Path) -> dict:
    if not path.exists():
        return {"timestamp": _now_iso(), "source": "chat", "status": "pending_replay", "items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"timestamp": _now_iso(), "source": "chat", "status": "invalid", "items": []}
    if not isinstance(data, dict):
        return {"timestamp": _now_iso(), "source": "chat", "status": "invalid", "items": []}
    if not isinstance(data.get("items"), list):
        data["items"] = []
    return data


def append(path: Path, item: dict) -> dict:
    data = load(path)
    data["timestamp"] = _now_iso()
    data["status"] = "pending_replay"
    data.setdefault("items", []).append(item)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data
