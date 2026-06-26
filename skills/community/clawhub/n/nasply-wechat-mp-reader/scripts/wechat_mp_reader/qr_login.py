from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path
from typing import Any

import requests

from session_store import save_session_file

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

STATE_PATH = Path(__file__).resolve().parents[1] / "cache" / "login-state.json"
QR_IMAGE_PATH = Path(__file__).resolve().parents[1] / "cache" / "wechat-login-qr-real.png"
BASE_URL = "https://mp.weixin.qq.com"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _save_state(data: dict[str, Any]) -> str:
    _ensure_parent(STATE_PATH)
    STATE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(STATE_PATH)


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _new_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": f"{BASE_URL}/",
        }
    )
    return session


def _generate_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")


def _get_cookie_value(session: requests.Session, name: str) -> str:
    values = [cookie.value for cookie in session.cookies if cookie.name == name]
    return values[-1] if values else ""


def _extract_qr_info(session: requests.Session, html_content: str) -> dict[str, str]:
    qr_pattern = r'(https?:\/\/mp\.weixin\.qq\.com\/cgi-bin\/loginqrcode\?action=getqrcode&param=\d+)'
    uuid_pattern = r'(?:"|\')uuid(?:"|\')\s*:\s*(?:"|\')([^"\']+)(?:"|\')'
    qr_match = re.search(qr_pattern, html_content)
    uuid_match = re.search(uuid_pattern, html_content)
    if qr_match and uuid_match:
        return {"qr_url": qr_match.group(1), "uuid": uuid_match.group(1)}

    uuid_value = _start_login(session)
    if not uuid_value:
        uuid_value = _generate_uuid()
    timestamp = int(time.time() * 1000)
    qr_url = f"{BASE_URL}/cgi-bin/scanloginqrcode?action=getqrcode&uuid={uuid_value}&random={timestamp}"
    return {"qr_url": qr_url, "uuid": uuid_value}


def _start_login(session: requests.Session) -> str:
    session.cookies.set("uuid", _generate_uuid(), domain="mp.weixin.qq.com", path="/")
    token = _get_cookie_value(session, "token")
    data = {
        "fingerprint": _generate_uuid(),
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "redirect_url": f"/cgi-bin/settingpage?t=setting/index&action=index&token={token}&lang=zh_CN",
        "login_type": "3",
    }
    resp = session.post(f"{BASE_URL}/cgi-bin/bizlogin?action=startlogin", data=data, timeout=20)
    resp.raise_for_status()
    return _get_cookie_value(session, "uuid") or resp.headers.get("X-UUID") or ""


def _save_qr_image(session: requests.Session, qr_url: str) -> str | None:
    try:
        _ensure_parent(QR_IMAGE_PATH)
        resp = session.get(
            qr_url,
            headers={
                "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "Referer": f"{BASE_URL}/",
            },
            timeout=20,
        )
        resp.raise_for_status()
        if not resp.content:
            return None
        QR_IMAGE_PATH.write_bytes(resp.content)
        return str(QR_IMAGE_PATH)
    except Exception:
        return None


def login_start() -> dict[str, Any]:
    session = _new_session()
    resp = session.get(f"{BASE_URL}/", timeout=20)
    resp.raise_for_status()
    qr_info = _extract_qr_info(session, resp.text)
    qr_image_path = _save_qr_image(session, qr_info["qr_url"])
    state = {
        "uuid": qr_info["uuid"],
        "qr_url": qr_info["qr_url"],
        "qr_image_path": qr_image_path,
        "created_at": int(time.time()),
        "cookies": requests.utils.dict_from_cookiejar(session.cookies),
    }
    state_path = _save_state(state)
    return {
        "started": True,
        "uuid": qr_info["uuid"],
        "qr_url": qr_info["qr_url"],
        "qr_image_path": qr_image_path,
        "state_path": state_path,
    }


def _session_from_state(state: dict[str, Any]) -> requests.Session:
    session = _new_session()
    cookies = state.get("cookies") or {}
    if cookies:
        session.cookies.update(cookies)
    return session


def _check_login_status(session: requests.Session, state: dict[str, Any]) -> dict[str, Any]:
    fingerprint = _get_cookie_value(session, "fingerprint") or _generate_uuid()
    params = {
        "action": "ask",
        "fingerprint": fingerprint,
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1,
    }
    resp = session.get(f"{BASE_URL}/cgi-bin/scanloginqrcode", params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    status = data.get("status", 0)
    if "invalid session" in str(data):
        return {"status": "invalid-session", "raw": data}
    if status in (1, 3):
        return {"status": "success", "raw": data}
    if status in (2, 4):
        return {"status": "scanned", "raw": data}
    return {"status": "waiting", "raw": data}


def _extract_login_info(session: requests.Session) -> dict[str, str]:
    login_data = {
        "userlang": "zh_CN",
        "redirect_url": "",
        "cookie_forbidden": "0",
        "cookie_cleaned": "0",
        "plugin_used": "0",
        "login_type": "3",
        "fingerprint": _get_cookie_value(session, "fingerprint") or _generate_uuid(),
        "token": "",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
    }
    resp = session.post(f"{BASE_URL}/cgi-bin/bizlogin?action=login", data=login_data, timeout=20)
    resp.raise_for_status()
    token_match = re.search(r'token=([^&\s"\']+)', resp.text)
    token = token_match.group(1) if token_match else _get_cookie_value(session, "token")
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    return {"token": token, "cookie": cookies_str}


def login_status(session_path: str | None = None) -> dict[str, Any]:
    state = load_state()
    if not state:
        return {"started": False, "status": "missing-state", "message": "login state not found"}
    session = _session_from_state(state)
    result = _check_login_status(session, state)
    out = {
        "started": True,
        "status": result["status"],
        "raw": result["raw"],
    }
    if result["status"] == "success":
        session_data = _extract_login_info(session)
        if session_data.get("cookie") and session_data.get("token"):
            saved_path = save_session_file(session_data, session_path)
            out["saved"] = True
            out["session_path"] = saved_path
            out["session"] = {
                "present": True,
                "valid": None,
                "reason": "fresh session captured",
                "cookie_len": len(session_data["cookie"]),
                "token_len": len(session_data["token"]),
            }
        else:
            out["saved"] = False
            out["message"] = "login succeeded but token/cookie extraction failed"
    return out
