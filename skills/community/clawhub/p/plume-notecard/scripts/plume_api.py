#!/usr/bin/env python3
"""
Plume API 客户端
封装 Open API 的 HTTP 调用：创建任务、查询任务、上传图片
"""

import json
import os
import ssl
import sys
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

SSL_CONTEXT = ssl.create_default_context()


def get_config():
    """获取 API Key 和 Base URL（多源）"""
    api_key = config.get_api_key()

    if not api_key:
        print("Error: PLUME_API_KEY must be set in environment.")
        sys.exit(1)

    api_base = config.get_api_base()
    return api_key, api_base


def _request(method: str, url: str, data: dict = None, headers: dict = None,
             timeout: int = 30) -> dict:
    """通用 HTTP 请求"""
    if headers is None:
        headers = {}

    headers.setdefault("User-Agent", "Plume-Notecard/1.0")

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(error_body)
        except json.JSONDecodeError:
            return {
                "success": False,
                "code": f"HTTP_{e.code}",
                "message": error_body or str(e),
            }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "code": "NETWORK_ERROR",
            "message": str(e.reason),
        }


def _detect_mime_type(file_data: bytes, file_path: str) -> str:
    """通过 magic bytes 检测真实 MIME 类型，后缀作为 fallback"""
    import mimetypes

    if file_data[:3] == b'\xff\xd8\xff':
        return "image/jpeg"
    if file_data[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if file_data[:4] == b'RIFF' and file_data[8:12] == b'WEBP':
        return "image/webp"
    if file_data[:6] in (b'GIF87a', b'GIF89a'):
        return "image/gif"

    return mimetypes.guess_type(file_path)[0] or "application/octet-stream"


def _upload_multipart(url: str, file_path: str, headers: dict,
                      timeout: int = 60) -> dict:
    """multipart/form-data 文件上传"""
    from uuid import uuid4

    boundary = f"----PlumeUpload{uuid4().hex}"
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()

    content_type = _detect_mime_type(file_data, file_path)

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n"
        f"\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    headers.setdefault("User-Agent", "Plume-Notecard/1.0")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(error_body)
        except json.JSONDecodeError:
            return {"success": False, "code": f"HTTP_{e.code}", "message": error_body}
    except urllib.error.URLError as e:
        return {"success": False, "code": "NETWORK_ERROR", "message": str(e.reason)}


def create_task(category: str, content: dict, project_id: str = None,
                widget_mapping: dict = None, title: str = None) -> dict:
    """创建 AI 任务"""
    api_key, api_base = get_config()
    url = f"{api_base}/api/open/tasks"

    payload = {
        "category": category,
        "content": content,
        "type": 2,
    }
    if title:
        payload["title"] = title
    if project_id:
        payload["project_id"] = project_id
    if widget_mapping:
        payload["widget_mapping"] = widget_mapping

    return _request("POST", url, data=payload, headers={
        "Authorization": f"Bearer {api_key}",
    })


def get_task(task_id: str) -> dict:
    """查询单个任务状态"""
    api_key, api_base = get_config()
    url = f"{api_base}/api/open/tasks/{task_id}"

    return _request("GET", url, headers={
        "Authorization": f"Bearer {api_key}",
    })


def upload_image(file_path: str) -> dict:
    """上传图片到 R2"""
    api_key, api_base = get_config()
    url = f"{api_base}/api/open/upload"

    if not os.path.isfile(file_path):
        return {"success": False, "code": "FILE_NOT_FOUND", "message": f"文件不存在: {file_path}"}

    return _upload_multipart(url, file_path, headers={
        "Authorization": f"Bearer {api_key}",
    })


def describe_image(image_url: str, focus: str = "general") -> dict:
    """调用 VL 模型描述图片内容"""
    api_key, api_base = get_config()
    url = f"{api_base}/api/open/describe"

    return _request("POST", url, data={
        "image_url": image_url,
        "focus": focus,
    }, headers={
        "Authorization": f"Bearer {api_key}",
    })


def batch_get_tasks(task_ids: list) -> dict:
    """批量查询任务"""
    api_key, api_base = get_config()
    ids_str = ",".join(str(tid) for tid in task_ids)
    url = f"{api_base}/api/open/tasks/batch?ids={ids_str}"

    return _request("GET", url, headers={
        "Authorization": f"Bearer {api_key}",
    })


def validate_api_key() -> dict:
    """验证 API Key 是否有效"""
    api_key, api_base = get_config()
    url = f"{api_base}/api/open/validate"

    return _request("GET", url, headers={
        "Authorization": f"Bearer {api_key}",
    })
