from __future__ import annotations

import json
import platform
import secrets
import urllib.error
import urllib.request


def _post_json(url: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))


def start_task_session(config: dict) -> dict:
    payload = {
        "skill_version": config.get("skill_version") or "1.0.0",
        "lang": config.get("lang", "zh"),
        "platform": platform.system().lower(),
        "client_nonce": secrets.token_hex(8),
    }
    if str(config.get("skill_version") or "").startswith("2."):
        url = f"{config['api_base'].rstrip('/')}/api/v2/session/start"
    else:
        url = f"{config['api_base'].rstrip('/')}/api/session/start"
    return _post_json(url, payload)


def end_task_session(config: dict) -> dict | None:
    session = config.get("task_session")
    if not session:
        return None
    if str(config.get("skill_version") or "").startswith("2."):
        return None

    payload = {
        "session_id": session.get("session_id"),
        "ticket": session.get("ticket"),
    }
    url = f"{config['api_base'].rstrip('/')}/api/session/end"
    try:
        return _post_json(url, payload)
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None
