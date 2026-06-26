#!/usr/bin/env python3
"""Shared helpers for ClawHub skill CLI clients."""

import json
import os
import socket
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


def load_env_file(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        print(f"[ERROR] Missing required env: {name}")
        sys.exit(1)
    return value


def get_request_timeout_seconds(default: float = 30.0) -> float:
    raw = os.getenv("REQUEST_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except ValueError:
        return default


def post_json(url: str, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=get_request_timeout_seconds()) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": {"status": e.code, "body": body}}
    except urllib.error.URLError as e:
        return {"error": {"status": "NETWORK", "body": str(e)}}
    except (TimeoutError, socket.timeout) as e:
        return {"error": {"status": "TIMEOUT", "body": str(e)}}
    except Exception as e:
        return {"error": {"status": "UNKNOWN", "body": str(e)}}


def has_error(data: Dict[str, Any]) -> bool:
    return isinstance(data, dict) and isinstance(data.get("error"), dict)


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def load_session(path: str = ".session.json") -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_session(data: Dict[str, Any], path: str = ".session.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
