#!/usr/bin/env python3
import json
import os
from pathlib import Path

DEFAULT_CONN_FILE = Path(__file__).resolve().parent / "connections.json"
SENSITIVE_KEYS = {"password", "token", "secret", "phone", "email"}


from typing import Optional


def load_connections(path: Optional[str] = None) -> dict:
    target = Path(path) if path else DEFAULT_CONN_FILE
    if not target.exists():
        return {}
    with target.open("r", encoding="utf-8") as f:
        return json.load(f)


def pick_profile(connections: dict, profile: str) -> dict:
    if profile not in connections:
        raise ValueError(f"Profile not found: {profile}")
    return connections[profile]


def coalesce(*values):
    for v in values:
        if v is not None and v != "":
            return v
    return None


def mask_sensitive(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if str(k).lower() in SENSITIVE_KEYS:
                out[k] = "***"
            else:
                out[k] = mask_sensitive(v)
        return out
    if isinstance(obj, list):
        return [mask_sensitive(x) for x in obj]
    return obj


def to_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def env_int(name: str, default=None):
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return int(v)
