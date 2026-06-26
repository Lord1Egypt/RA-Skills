#!/usr/bin/env python3
"""
Imou Open API client for device operations.

Provides: accessToken, setDeviceSnapEnhanced (snapshot URL), controlMovePTZ.
All requests include header Client-Type: OpenClaw.
"""

import hashlib
import os
import time
import uuid
import requests

DEFAULT_BASE_URL = "https://openapi.lechange.cn"
OPENCLAW_HEADER = "Client-Type"
OPENCLAW_HEADER_VALUE = "OpenClaw"

# PTZ operation codes (per API doc)
PTZ_UP = "0"
PTZ_DOWN = "1"
PTZ_LEFT = "2"
PTZ_RIGHT = "3"
PTZ_UP_LEFT = "4"
PTZ_DOWN_LEFT = "5"
PTZ_UP_RIGHT = "6"
PTZ_DOWN_RIGHT = "7"
PTZ_ZOOM_IN = "8"
PTZ_ZOOM_OUT = "9"
PTZ_STOP = "10"


def _get_base_url():
    return os.environ.get("IMOU_BASE_URL", "").strip() or DEFAULT_BASE_URL


def _build_sign(time_sec: int, nonce: str, app_secret: str) -> str:
    """Build sign: MD5 of 'time:{time},nonce:{nonce},appSecret:{app_secret}' (UTF-8), 32-char lowercase hex."""
    raw = f"time:{time_sec},nonce:{nonce},appSecret:{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _request(method: str, params: dict, app_id: str, app_secret: str, base_url: str = None) -> dict:
    """
    Send one Open API request.
    :param method: API method name (e.g. 'accessToken', 'setDeviceSnapEnhanced', 'controlMovePTZ').
    :param params: Request params object.
    :param app_id: App ID.
    :param app_secret: App secret for sign.
    :param base_url: Optional base URL; uses env IMOU_BASE_URL or default if None.
    :return: Full response body as dict; check result.code for '0'.
    """
    base = base_url or _get_base_url()
    url = f"{base.rstrip('/')}/openapi/{method}"
    time_sec = int(time.time())
    nonce = uuid.uuid4().hex
    sign = _build_sign(time_sec, nonce, app_secret)
    body = {
        "system": {
            "ver": "1.0",
            "appId": app_id,
            "sign": sign,
            "time": time_sec,
            "nonce": nonce,
        },
        "id": str(uuid.uuid4()),
        "params": params,
    }
    headers = {
        "Content-Type": "application/json",
        OPENCLAW_HEADER: OPENCLAW_HEADER_VALUE,
    }
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_access_token(app_id: str, app_secret: str, base_url: str = None) -> dict:
    """
    Get admin accessToken.
    :return: { "success": bool, "access_token": str, "expire_time": int (seconds), "error": str? }
    """
    try:
        out = _request("accessToken", {}, app_id, app_secret, base_url)
        res = out.get("result", {})
        code = res.get("code")
        if code == "0":
            data = res.get("data", {})
            return {
                "success": True,
                "access_token": data.get("accessToken", ""),
                "expire_time": int(data.get("expireTime", 0)),
            }
        return {
            "success": False,
            "error": res.get("msg", "Unknown error"),
            "code": code,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_device_snap_enhanced(
    token: str,
    device_id: str,
    channel_id: str,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Device snapshot (enhanced). Returns a downloadable image URL valid for 2 hours.
    Request interval should be >= 1 second per device.
    :param token: accessToken.
    :param device_id: Device serial (deviceId).
    :param channel_id: Channel ID (e.g. "0").
    :return: { "success": bool, "url": str, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "setDeviceSnapEnhanced",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
            },
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "url": data.get("url", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def control_move_ptz(
    token: str,
    device_id: str,
    channel_id: str,
    operation: str,
    duration: int,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    PTZ move control. Device must support PT or PTZ capability.
    :param token: accessToken.
    :param device_id: Device serial (deviceId).
    :param channel_id: Channel ID (e.g. "0").
    :param operation: "0"=up, "1"=down, "2"=left, "3"=right, "4"=up-left, "5"=down-left, "6"=up-right, "7"=down-right, "8"=zoom in, "9"=zoom out, "10"=stop.
    :param duration: Move duration in milliseconds.
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "controlMovePTZ",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "operation": str(operation).strip(),
                "duration": str(int(duration)),
            },
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") == "0":
            return {"success": True}
        return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
    except Exception as e:
        return {"success": False, "error": str(e)}
