from __future__ import annotations

from typing import Any

import requests

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


def has_session(session_cfg: dict[str, str]) -> bool:
    return bool(session_cfg.get("cookie") and session_cfg.get("token"))


def check_session(session_cfg: dict[str, str]) -> dict[str, Any]:
    if not has_session(session_cfg):
        return {
            "present": False,
            "valid": False,
            "reason": "missing cookie or token",
            "base_resp": {},
        }

    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "begin": 0,
        "count": 1,
        "query": "微信",
        "token": session_cfg["token"],
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
    }
    headers = {
        "Cookie": session_cfg["cookie"],
        "User-Agent": USER_AGENT,
        "Referer": "https://mp.weixin.qq.com/",
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return {
            "present": True,
            "valid": False,
            "reason": f"request failed: {exc}",
            "base_resp": {},
        }

    base_resp = data.get("base_resp") or {}
    ret = base_resp.get("ret")
    err_msg = base_resp.get("err_msg", "")
    valid = ret == 0
    reason = "ok" if valid else (err_msg or f"ret={ret}")
    return {
        "present": True,
        "valid": valid,
        "reason": reason,
        "base_resp": base_resp,
    }
