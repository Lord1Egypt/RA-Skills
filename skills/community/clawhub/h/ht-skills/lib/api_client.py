# -*- coding: utf-8 -*-
"""
Skill API 客户端：带 Token 的 HTTP 请求封装
author: 灏天文库
"""

import os
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union, BinaryIO

try:
    import requests
except ImportError:
    requests = None


def get_client_root() -> Path:
    """client 目录根路径"""
    return Path(__file__).resolve().parent.parent


def load_config() -> Dict[str, Any]:
    """加载 client config.json，支持环境变量覆盖"""
    root = get_client_root()
    config_path = root / "config.json"
    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    # 环境变量优先
    server_url = os.environ.get("HT_SKILL_SERVER_URL") or config.get("server_base_url")
    token = os.environ.get("HT_SKILL_TOKEN") or config.get("token")
    return {"server_base_url": server_url, "token": token}


def request(
    method: str,
    path: str,
    params: Optional[Dict] = None,
    json_body: Optional[Dict] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    发送请求到 Skill 服务端，自动附带 Token
    method: GET, POST, PATCH 等
    path: 如 /api/collections（不含 base_url）
    params: query 参数（GET）
    json_body: JSON 请求体（POST/PATCH）
    返回解析后的 JSON，失败时输出错误并 sys.exit(1)
    """
    if not requests:
        print(json.dumps({"success": False, "error": "请安装 requests: pip install requests"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    cfg = load_config()
    base_url = (cfg.get("server_base_url") or "").rstrip("/")
    token = cfg.get("token")
    if not base_url:
        print(json.dumps({"success": False, "error": "未配置 server_base_url，请在 config.json 或环境变量 HT_SKILL_SERVER_URL 中设置"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    if not token:
        print(json.dumps({"success": False, "error": "未配置 token，请在 config.json 或环境变量 HT_SKILL_TOKEN 中设置"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    url = f"{base_url}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            headers=headers,
            timeout=timeout,
        )
        data = resp.json() if resp.content else {}
        if resp.status_code >= 400:
            err = data.get("error") or data.get("detail") or resp.text or f"HTTP {resp.status_code}"
            print(json.dumps({"success": False, "error": err, "status_code": resp.status_code}, ensure_ascii=False, indent=2))
            sys.exit(1)
        return data
    except requests.exceptions.RequestException as e:
        print(json.dumps({"success": False, "error": str(e), "message": "请求服务端失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"响应解析失败: {e}"}, ensure_ascii=False, indent=2))
        sys.exit(1)


# multipart 单文件项：文件名 + 二进制或类文件对象，可选 MIME
MultipartFile = Union[
    Tuple[str, bytes],
    Tuple[str, bytes, str],
    Tuple[str, BinaryIO],
    Tuple[str, BinaryIO, str],
]


def post_multipart(
    path: str,
    files: Dict[str, MultipartFile],
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 120,
) -> Dict[str, Any]:
    """
    POST multipart/form-data（用于图片上传等），自动附带 Token。
    勿手动设置 Content-Type，由 requests 生成 boundary。
    files 示例: {"file": ("a.png", image_bytes, "image/png")}
    """
    if not requests:
        print(json.dumps({"success": False, "error": "请安装 requests: pip install requests"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    cfg = load_config()
    base_url = (cfg.get("server_base_url") or "").rstrip("/")
    token = cfg.get("token")
    if not base_url:
        print(json.dumps({"success": False, "error": "未配置 server_base_url，请在 config.json 或环境变量 HT_SKILL_SERVER_URL 中设置"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    if not token:
        print(json.dumps({"success": False, "error": "未配置 token，请在 config.json 或环境变量 HT_SKILL_TOKEN 中设置"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    url = f"{base_url}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    form_data = {k: v for k, v in (data or {}).items() if v is not None}
    try:
        resp = requests.post(url, files=files, data=form_data or None, headers=headers, timeout=timeout)
        resp_data = resp.json() if resp.content else {}
        if resp.status_code >= 400:
            err = resp_data.get("error") or resp_data.get("detail") or resp.text or f"HTTP {resp.status_code}"
            print(json.dumps({"success": False, "error": err, "status_code": resp.status_code}, ensure_ascii=False, indent=2))
            sys.exit(1)
        return resp_data
    except requests.exceptions.RequestException as e:
        print(json.dumps({"success": False, "error": str(e), "message": "请求服务端失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "error": f"响应解析失败: {e}"}, ensure_ascii=False, indent=2))
        sys.exit(1)


def output_result(data: dict) -> None:
    """输出 JSON 结果到 stdout"""
    print(json.dumps(data, ensure_ascii=False, indent=2))
