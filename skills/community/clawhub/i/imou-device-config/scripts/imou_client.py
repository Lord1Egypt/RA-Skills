#!/usr/bin/env python3
"""
Imou Open API client for device config (security: plan, sensitivity, privacy)
and IoT thing-model (property get/set, service invoke).

Provides: accessToken, get/set device camera status (enable), alarm plan get/set,
set alarm sensitivity; getProductModel, getIotDeviceProperties, setIotDeviceProperties,
iotDeviceControl. All requests include header Client-Type: OpenClaw.
"""

import hashlib
import json
import os
import time
import uuid
import requests

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
    :param method: API method name.
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


def get_device_camera_status(
    token: str,
    device_id: str,
    channel_id: str,
    enable_type: str,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get device enable status (e.g. closeCamera for privacy, motionDetect).
    :param enable_type: e.g. 'closeCamera', 'motionDetect' (lowercase).
    :return: { "success": bool, "status": "on"|"off", "enable_type": str, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "getDeviceCameraStatus",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "enableType": str(enable_type).strip(),
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
            "status": data.get("status", "off"),
            "enable_type": data.get("enableType", enable_type),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_device_camera_status(
    token: str,
    device_id: str,
    channel_id: str,
    enable_type: str,
    enable: bool,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Set device enable status (e.g. closeCamera for privacy).
    :param enable_type: e.g. 'closeCamera', 'motionDetect'.
    :param enable: True = on, False = off.
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "deviceId": str(device_id).strip(),
        "channelId": str(channel_id).strip(),
        "enableType": str(enable_type).strip(),
        "enable": bool(enable),
    }
    try:
        out = _request("setDeviceCameraStatus", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") == "0":
            return {"success": True}
        return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def device_alarm_plan(
    token: str,
    device_id: str,
    channel_id: str,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get motion detection (alarm) plan for a channel.
    :return: { "success": bool, "channel_id": str, "rules": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "deviceAlarmPlan",
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
        return {
            "success": True,
            "channel_id": data.get("channelId", channel_id),
            "rules": data.get("rules", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def modify_device_alarm_plan(
    token: str,
    device_id: str,
    channel_id: str,
    rules: list,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Set motion detection (alarm) plan for a channel.
    :param rules: List of dicts with period, beginTime, endTime (HH:mm:ss). period e.g. "Monday" or "Monday,Wednesday,Friday".
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "modifyDeviceAlarmPlan",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "rules": rules,
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


def set_device_alarm_sensitivity(
    token: str,
    device_id: str,
    channel_id: str,
    sensitive: int,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Set motion detection sensitivity for a channel. 1=lowest, 5=highest.
    :param sensitive: Integer 1-5.
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    sensitive = max(1, min(5, int(sensitive)))
    try:
        out = _request(
            "setDeviceAlarmSensitivity",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "sensitive": sensitive,
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


# --- IoT thing-model APIs (devices with productId) ---


def get_product_model(
    token: str,
    product_id: str,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get product thing model by productId. Use to discover Property refs and Service refs.
    :return: { "success": bool, "model": dict (schema, profile, properties, services, events), "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "getProductModel",
            {"token": token, "productId": str(product_id).strip()},
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "model": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_iot_device_properties(
    token: str,
    product_id: str,
    device_id: str,
    properties: list,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get specified Property values of an IoT device. properties = list of Property ref strings.
    :return: { "success": bool, "product_id": str, "device_id": str, "properties": dict (ref->value), "status": str?, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "productId": str(product_id).strip(),
        "deviceId": str(device_id).strip(),
        "properties": [str(p).strip() for p in properties],
    }
    try:
        out = _request("getIotDeviceProperties", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {
            "success": True,
            "product_id": data.get("productId", product_id),
            "device_id": data.get("deviceId", device_id),
            "properties": data.get("properties", {}),
            "status": data.get("status"),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_iot_device_properties(
    token: str,
    product_id: str,
    device_id: str,
    properties: dict,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Set specified Property values of an IoT device. properties = dict of ref -> value.
    :return: { "success": bool, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    props_out = {}
    for k, v in properties.items():
        key = str(k).strip()
        if isinstance(v, bool):
            props_out[key] = 1 if v else 0
        else:
            props_out[key] = v
    params = {
        "token": token,
        "productId": str(product_id).strip(),
        "deviceId": str(device_id).strip(),
        "properties": props_out,
    }
    try:
        out = _request("setIotDeviceProperties", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") == "0":
            return {"success": True}
        return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def iot_device_control(
    token: str,
    product_id: str,
    device_id: str,
    ref: str,
    content: dict,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Invoke a Service on an IoT device (event/command dispatch). ref = service ref from thing model.
    content = input params as dict of param ref -> value; use {} if service has no input.
    :return: { "success": bool, "content": dict (outputData etc.), "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "productId": str(product_id).strip(),
        "deviceId": str(device_id).strip(),
        "ref": str(ref).strip(),
        "content": content if isinstance(content, dict) else {},
    }
    try:
        out = _request("iotDeviceControl", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "content": data.get("content", {})}
    except Exception as e:
        return {"success": False, "error": str(e)}
