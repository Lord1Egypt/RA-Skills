#!/usr/bin/env python3
"""
Imou Open API client for device management.

Provides: accessToken, listDeviceDetailsByPage, listDeviceDetailsByIds, modifyDeviceName.
All requests include header Client-Type: OpenClaw.
"""

import hashlib
import json
import os
import time
import uuid
import requests

# Default base URL for Imou Open API
DEFAULT_BASE_URL = "https://openapi.lechange.cn"
OPENCLAW_HEADER = "Client-Type"
OPENCLAW_HEADER_VALUE = "OpenClaw"


def _get_base_url():
    return os.environ.get("IMOU_BASE_URL", "").strip() or DEFAULT_BASE_URL


def _build_sign(time_sec: int, nonce: str, app_secret: str) -> str:
    """Build sign: MD5 of 'time:{time},nonce:{nonce},appSecret:{app_secret}' (UTF-8), 32-char lowercase hex."""
    raw = f"time:{time_sec},nonce:{nonce},appSecret:{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _request(method: str, params: dict, app_id: str, app_secret: str, base_url: str = None) -> dict:
    """
    Send one Open API request.
    :param method: API method name (e.g. 'accessToken', 'listDeviceDetailsByPage').
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


def list_device_details_by_page(
    token: str,
    page: int = 1,
    page_size: int = 10,
    source: str = "bindAndShare",
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Paginated list of devices under the account.
    :param token: accessToken.
    :param page: Page index (from 1).
    :param page_size: Page size (1-50).
    :param source: bind | share | bindAndShare.
    :param app_id, app_secret, base_url: Used for signed request; required if calling API directly.
    :return: { "success": bool, "count": int, "device_list": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    # Protocol: token, pageSize (1-50), page (from 1), source (bind|share|bindAndShare)
    page_size = max(1, min(50, page_size))
    page = max(1, page)
    try:
        out = _request(
            "listDeviceDetailsByPage",
            {
                "token": token,
                "pageSize": page_size,
                "page": page,
                "source": source,
            },
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {
            "success": True,
            "count": data.get("count", 0),
            "device_list": data.get("deviceList", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_device_details_by_ids(
    token: str,
    device_ids: list,
    channel_ids: list = None,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get device details by serial(s). Optionally filter by channel IDs per device.
    Protocol: deviceList items are { "deviceId": "<serial>", "channelId": ["0"] }; omit channelId to get all channels.
    :param token: accessToken.
    :param device_ids: List of device serial strings.
    :param channel_ids: Optional list of channel IDs (e.g. ["0"]); if None, all channels returned.
    :return: { "success": bool, "count": int, "device_list": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    device_list_param = []
    for did in device_ids:
        item = {"deviceId": str(did).strip()}
        if channel_ids is not None:
            item["channelId"] = [str(c).strip() for c in channel_ids]
        device_list_param.append(item)
    try:
        out = _request(
            "listDeviceDetailsByIds",
            {"token": token, "deviceList": device_list_param},
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {
            "success": True,
            "count": data.get("count", 0),
            "device_list": data.get("deviceList", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def modify_device_name(
    token: str,
    device_id: str,
    name: str,
    channel_id: str = None,
    product_id: str = None,
    sub_device_id: str = None,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Modify device or channel name. Protocol: token, deviceId, name required; channelId, productId, subDeviceId optional.
    When device info exists (e.g. from list_device_details_by_page or list_device_details_by_ids), productId must be
    included in the request if present on the device object.
    :param token: accessToken.
    :param device_id: Device serial (deviceId).
    :param name: New name (max 64 chars).
    :param channel_id: If empty/None, set device name; otherwise set channel name. Optional per API.
    :param product_id: Optional per API; must be carried when device exists and has productId (e.g. from list/get).
    :param sub_device_id: Required when renaming a sub-device per API.
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "deviceId": str(device_id).strip(),
        "name": (name or "").strip()[:64],
    }
    if channel_id is not None and str(channel_id).strip() != "":
        params["channelId"] = str(channel_id).strip()
    if product_id is not None and str(product_id).strip() != "":
        params["productId"] = str(product_id).strip()
    if sub_device_id is not None and str(sub_device_id).strip() != "":
        params["subDeviceId"] = str(sub_device_id).strip()
    try:
        out = _request("modifyDeviceName", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") == "0":
            return {"success": True}
        return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
    except Exception as e:
        return {"success": False, "error": str(e)}
