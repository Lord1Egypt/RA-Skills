#!/usr/bin/env python3
"""
Imou Open API client for AI multimodal analysis.

Provides: accessToken; humanDetect, smokingDetect, phoneUsingDetect, workwearDetect,
absenceDetect, shelfStatusDetect, trashOverflowDetect, heatmapDetect, faceAnalysis;
createAiDetectRepository, listAiDetectRepositoryByPage, deleteAiDetectRepository;
addAiDetectTarget, listAiDetectTarget, deleteAiDetectTarget.
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


def _get_base_url():
    return os.environ.get("IMOU_BASE_URL", "").strip() or DEFAULT_BASE_URL


def _build_sign(time_sec: int, nonce: str, app_secret: str) -> str:
    """Build sign: MD5 of 'time:{time},nonce:{nonce},appSecret:{app_secret}' (UTF-8), 32-char lowercase hex."""
    raw = f"time:{time_sec},nonce:{nonce},appSecret:{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _request(method: str, params: dict, app_id: str, app_secret: str, base_url: str = None) -> dict:
    """
    Send one Open API request.
    :param method: API method name (e.g. 'accessToken', 'humanDetect').
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
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()


def _image_params(token: str, image_type: str, content: str, detect_region: list = None) -> dict:
    """Build common params for image-based detection: token, type, content, optional detectRegion."""
    p = {"token": token, "type": image_type, "content": content}
    if detect_region:
        p["detectRegion"] = detect_region
    return p


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
        return {"success": False, "error": res.get("msg", "Unknown error"), "code": code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _call_detect(method: str, token: str, image_type: str, content: str, detect_region: list = None,
                 extra_params: dict = None, app_id: str = None, app_secret: str = None,
                 base_url: str = None) -> dict:
    """
    Call an image-based detection API.
    :return: { "success": bool, "data": dict, "error": str?, "code": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = _image_params(token, image_type, content, detect_region)
    if extra_params:
        params.update(extra_params)
    try:
        out = _request(method, params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        return {"success": True, "data": res.get("data", {})}
    except Exception as e:
        return {"success": False, "error": str(e)}


def human_detect(token: str, image_type: str, content: str, detect_region: list = None,
                 app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Human detection. image_type: '0' URL, '1' Base64. Returns detectResult, targets."""
    return _call_detect("humanDetect", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def smoking_detect(token: str, image_type: str, content: str, detect_region: list = None,
                   app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Smoking detection. image_type: '0' URL, '1' Base64. Returns detectResult, targets."""
    return _call_detect("smokingDetect", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def phone_using_detect(token: str, image_type: str, content: str, detect_region: list = None,
                       app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Phone-using detection. image_type: '0' URL, '1' Base64. Returns detectResult, targets."""
    return _call_detect("phoneUsingDetect", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def workwear_detect(token: str, image_type: str, content: str, threshold: float,
                    repository_id: str = None, detect_region: list = None,
                    app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Workwear detection. threshold in (0,1]. Optional repository_id (workwear library)."""
    extra = {"threshold": threshold}
    if repository_id:
        extra["repositoryId"] = repository_id
    return _call_detect("workwearDetect", token, image_type, content, detect_region,
                        extra, app_id, app_secret, base_url)


def absence_detect(token: str, image_type: str, content: str, repository_id: str, threshold: float,
                   detect_region: list = None, app_id: str = None, app_secret: str = None,
                   base_url: str = None) -> dict:
    """Absence detection. repository_id (workwear library) and threshold (0,1] required."""
    extra = {"repositoryId": repository_id, "threshold": threshold}
    return _call_detect("absenceDetect", token, image_type, content, detect_region,
                        extra, app_id, app_secret, base_url)


def shelf_status_detect(token: str, image_type: str, content: str, detect_region: list = None,
                        app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Shelf status detection. Returns structure per API doc."""
    return _call_detect("shelfStatusDetect", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def trash_overflow_detect(token: str, image_type: str, content: str, detect_region: list = None,
                          app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Trash overflow detection. Returns detectResult, targets."""
    return _call_detect("trashOverflowDetect", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def heatmap_detect(token: str, image_type: str, content: str, threshold: float,
                   exclude_repository_ids: list = None, detect_region: list = None,
                   app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Heatmap statistics. threshold in (0,1]. Optional exclude_repository_ids to filter workwear persons."""
    extra = {"threshold": threshold}
    if exclude_repository_ids:
        extra["excludeRepositoryIds"] = exclude_repository_ids
    return _call_detect("heatmapDetect", token, image_type, content, detect_region,
                        extra, app_id, app_secret, base_url)


def face_analysis(token: str, image_type: str, content: str, detect_region: list = None,
                  app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Face analysis. Returns structure per API doc."""
    return _call_detect("faceAnalysis", token, image_type, content, detect_region,
                        None, app_id, app_secret, base_url)


def create_ai_detect_repository(token: str, repository_name: str, repository_type: str,
                                app_id: str = None, app_secret: str = None,
                                base_url: str = None) -> dict:
    """
    Create detect repository. repository_type: 'face' | 'human'.
    :return: { "success": bool, "repository_id": str?, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "createAiDetectRepository",
            {"token": token, "repositoryName": repository_name, "repositoryType": repository_type},
            app_id, app_secret, base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "repository_id": data.get("repositoryId", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_ai_detect_repository_by_page(token: str, page: int = 1, page_size: int = 20,
                                      repository_name: str = None,
                                      app_id: str = None, app_secret: str = None,
                                      base_url: str = None) -> dict:
    """
    List detect repositories by page. page_size max 20.
    :return: { "success": bool, "total": int, "repository_list": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    params = {"token": token, "page": max(1, page), "pageSize": min(20, max(1, page_size))}
    if repository_name:
        params["repositoryName"] = repository_name
    try:
        out = _request("listAiDetectRepositoryByPage", params, app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {
            "success": True,
            "total": data.get("total", 0),
            "repository_list": data.get("repositoryList", []),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_ai_detect_repository(token: str, repository_id: str,
                                app_id: str = None, app_secret: str = None,
                                base_url: str = None) -> dict:
    """Delete detect repository. :return: { "success": bool, "error": str? }"""
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request("deleteAiDetectRepository", {"token": token, "repositoryId": repository_id},
                       app_id, app_secret, base_url)
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_ai_detect_target(token: str, repository_id: str, target_type: str, content: str,
                         app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """
    Add target to repository. target_type: '0' URL, '1' Base64.
    :return: { "success": bool, "target_key": str?, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "addAiDetectTarget",
            {"token": token, "repositoryId": repository_id, "type": int(target_type), "content": content},
            app_id, app_secret, base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        return {"success": True, "target_key": data.get("targetKey", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_ai_detect_target(token: str, repository_id: str, page: int = 1, page_size: int = 20,
                          app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """
    List targets in repository.
    :return: { "success": bool, "total": int, "target_list": list, "error": str? }
    """
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "listAiDetectTarget",
            {"token": token, "repositoryId": repository_id, "page": max(1, page), "pageSize": min(20, max(1, page_size))},
            app_id, app_secret, base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        data = res.get("data", {})
        target_list = data.get("targetList", data.get("target_list", []))
        return {
            "success": True,
            "total": data.get("total", len(target_list)),
            "target_list": target_list,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_ai_detect_target(token: str, repository_id: str, target_id: str,
                            app_id: str = None, app_secret: str = None, base_url: str = None) -> dict:
    """Delete target from repository. target_id is targetKey from add/list. :return: { "success": bool, "error": str? }"""
    app_id = app_id or os.environ.get("IMOU_APP_ID", "")
    app_secret = app_secret or os.environ.get("IMOU_APP_SECRET", "")
    try:
        out = _request(
            "deleteAiDetectTarget",
            {"token": token, "repositoryId": repository_id, "targetId": target_id},
            app_id, app_secret, base_url,
        )
        res = out.get("result", {})
        if res.get("code") != "0":
            return {"success": False, "error": res.get("msg", "Unknown error"), "code": res.get("code")}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
