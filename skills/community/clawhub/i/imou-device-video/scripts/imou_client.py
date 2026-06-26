#!/usr/bin/env python3
"""
Imou Open API client for device video.

Provides: accessToken, bind_device_live, live_list, create_device_record_hls,
query_local_records, query_cloud_records. All requests include header Client-Type: OpenClaw.
"""

import hashlib
import os
import time
import uuid
import requests

DEFAULT_BASE_URL = "https://openapi.lechange.cn"
OPENCLAW_HEADER = "Client-Type"
OPENCLAW_HEADER_VALUE = "OpenClaw"

# LV1001: live address already exists; get HLS from liveList
CODE_LIVE_ALREADY_EXISTS = "LV1001"


def _get_base_url():
    return os.environ.get("IMOU_BASE_URL", "").strip() or DEFAULT_BASE_URL


def _build_sign(time_sec: int, nonce: str, app_secret: str) -> str:
    """Build sign: MD5 of 'time:{time},nonce:{nonce},appSecret:{app_secret}' (UTF-8), 32-char lowercase hex."""
    raw = f"time:{time_sec},nonce:{nonce},appSecret:{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _request(method: str, params: dict, app_id: str, app_secret: str, base_url: str = None) -> dict:
    """
    Send one Open API request.
    :param method: API method name (e.g. 'accessToken', 'bindDeviceLive').
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


def bind_device_live(
    token: str,
    device_id: str,
    channel_id: str,
    stream_id: int = 0,
    live_mode: str = "proxy",
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Create device live source. Returns HLS in data.streams[].hls.
    If result.code is LV1001 (live already exists), caller should use live_list to get existing HLS.
    :param token: accessToken.
    :param device_id: Device serial.
    :param channel_id: Channel ID (e.g. "0").
    :param stream_id: 0 main stream, 1 sub stream.
    :param live_mode: "proxy" or omit.
    :return: { "success": bool, "code": str?, "hls": str?, "streams": list?, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "deviceId": str(device_id).strip(),
        "channelId": str(channel_id).strip(),
        "streamId": 0 if stream_id not in (0, 1) else stream_id,
    }
    if live_mode:
        params["liveMode"] = live_mode
    try:
        out = _request("bindDeviceLive", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        code = res.get("code")
        if code == "0":
            data = res.get("data", {})
            streams = data.get("streams") or []
            hls = None
            for s in streams:
                if s.get("streamId") == (0 if stream_id not in (0, 1) else stream_id):
                    hls = s.get("hls")
                    break
            if not hls and streams:
                hls = streams[0].get("hls")
            return {"success": True, "hls": hls, "streams": streams}
        if code == CODE_LIVE_ALREADY_EXISTS:
            return {"success": False, "code": code, "error": res.get("msg", "Live already exists")}
        return {"success": False, "code": code, "error": res.get("msg", "Unknown error")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def live_list(
    token: str,
    query_range: str = "1-100",
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get live list. queryRange format "1-N" (e.g. "1-100").
    :return: { "success": bool, "count": int, "lives": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "liveList",
            {"token": token, "queryRange": str(query_range).strip()},
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
            "lives": data.get("lives", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_live_hls(
    token: str,
    device_id: str,
    channel_id: str,
    stream_id: int = 0,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Get live HLS URL for device/channel. Creates live via bindDeviceLive; if LV1001, fetches from liveList.
    :return: { "success": bool, "hls": str?, "error": str? }
    """
    r = bind_device_live(
        token, device_id, channel_id, stream_id=stream_id,
        app_id=app_id, app_secret=app_secret, base_url=base_url,
    )
    if r.get("success") and r.get("hls"):
        return {"success": True, "hls": r["hls"]}
    if r.get("code") == CODE_LIVE_ALREADY_EXISTS:
        r2 = live_list(token, "1-100", app_id=app_id, app_secret=app_secret, base_url=base_url)
        if not r2.get("success"):
            return {"success": False, "error": r2.get("error", "liveList failed")}
        sid = 0 if stream_id not in (0, 1) else stream_id
        dev = str(device_id).strip()
        ch = str(channel_id).strip()
        for live in r2.get("lives", []):
            if live.get("deviceId") == dev and str(live.get("channelId")) == ch:
                for s in live.get("streams") or []:
                    if s.get("streamId") == sid:
                        return {"success": True, "hls": s.get("hls")}
                if live.get("streams"):
                    return {"success": True, "hls": live["streams"][0].get("hls")}
        return {"success": False, "error": "Live exists but not found in liveList for this device/channel/stream"}
    return {"success": False, "error": r.get("error", "bindDeviceLive failed")}


def create_device_record_hls(
    token: str,
    device_id: str,
    channel_id: str,
    begin_time: str,
    end_time: str,
    record_type: str,
    stream_id: int = 0,
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Create record playback HLS URL. recordType: localRecord | cloudRecord. Time format yyyy-MM-dd HH:mm:ss.
    :return: { "success": bool, "url": str?, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {
        "token": token,
        "deviceId": str(device_id).strip(),
        "channelId": str(channel_id).strip(),
        "beginTime": begin_time.strip(),
        "endTime": end_time.strip(),
        "recordType": record_type.strip(),
        "streamId": 0 if stream_id not in (0, 1) else stream_id,
    }
    try:
        out = _request("createDeviceRecordHls", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "url": data.get("url")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def query_local_records(
    token: str,
    device_id: str,
    channel_id: str,
    begin_time: str,
    end_time: str,
    count: int = 100,
    record_type: str = "All",
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Query local record clips in time range. count max 100 (some devices limit to 32).
    :return: { "success": bool, "records": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    count = max(1, min(100, count))
    try:
        out = _request(
            "queryLocalRecords",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "beginTime": begin_time.strip(),
                "endTime": end_time.strip(),
                "type": (record_type or "All").strip(),
                "count": count,
            },
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "records": data.get("records", [])}
    except Exception as e:
        return {"success": False, "error": str(e)}


def query_cloud_records(
    token: str,
    device_id: str,
    channel_id: str,
    begin_time: str,
    end_time: str,
    query_range: str = "1-100",
    app_id: str = None,
    app_secret: str = None,
    base_url: str = None,
) -> dict:
    """
    Query cloud record clips in time range. queryRange format "1-N", N max 100.
    :return: { "success": bool, "records": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "queryCloudRecords",
            {
                "token": token,
                "deviceId": str(device_id).strip(),
                "channelId": str(channel_id).strip(),
                "beginTime": begin_time.strip(),
                "endTime": end_time.strip(),
                "queryRange": str(query_range).strip(),
            },
            app_id,
            app_secret,
            base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "records": data.get("records", [])}
    except Exception as e:
        return {"success": False, "error": str(e)}
