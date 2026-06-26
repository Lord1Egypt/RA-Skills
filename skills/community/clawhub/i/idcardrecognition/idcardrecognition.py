#!/usr/bin/env python3
"""
ID card recognition skill for OpenClaw.
基于极速数据 身份证识别 API：
https://www.jisuapi.com/api/idcardrecognition/
"""

import base64
import json
import os
import sys
from typing import Any, Dict

import requests


IDCARD_RECOG_URL = "https://api.jisuapi.com/idcardrecognition/recognize"


def _normalize_local_path(user_path: str, field: str) -> Dict[str, Any]:
    """
    规范化并限制本地文件路径，只允许在当前工作目录及其子目录内读写。
    禁止绝对路径和目录穿越（包含 ..），避免被恶意提示利用读取任意系统文件。
    """
    if not user_path:
        return {
            "error": "invalid_param",
            "message": f"field '{field}' is empty",
        }

    if os.path.isabs(user_path):
        return {
            "error": "invalid_path",
            "message": f"Absolute path is not allowed for '{field}'",
        }

    norm = os.path.normpath(user_path)
    if norm.startswith("..") or norm == "..":
        return {
            "error": "invalid_path",
            "message": f"Path traversal is not allowed for '{field}'",
        }

    base = os.getcwd()
    full = os.path.join(base, norm)
    return {"error": None, "path": full, "relative": norm}


def _build_pic_base64(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    从请求中获取 base64 图片内容：
    - 若提供 pic 字段（base64 字符串），直接使用；
    - 若提供 path/image/file，则从本地文件读取并转为 base64。
    """
    pic = req.get("pic")
    if pic:
        return {"pic": str(pic), "error": None}

    path_raw = req.get("path") or req.get("image") or req.get("file")
    if not path_raw:
        return {
            "pic": None,
            "error": "Either 'pic' (base64) or 'path/image/file' is required",
        }

    safe = _normalize_local_path(str(path_raw).strip(), "path")
    if safe["error"]:
        return {"pic": None, "error": safe["message"]}

    path = safe["path"]
    if not os.path.isfile(path):
        return {"pic": None, "error": f"File not found: {safe['relative']}"}

    try:
        with open(path, "rb") as f:
            raw = f.read()
    except Exception as e:
        return {"pic": None, "error": f"Failed to read file: {e}"}

    try:
        encoded = base64.b64encode(raw).decode("utf-8")
    except Exception as e:
        return {"pic": None, "error": f"Failed to base64-encode file: {e}"}

    return {"pic": encoded, "error": None}


def _call_idcard_api(appkey: str, pic_base64: str, typeid: int) -> Dict[str, Any]:
    """
    调用身份证识别接口。
    typeid: 证件类型，参考 /idcardrecognition/type 接口。
    """
    params = {"appkey": appkey}
    data = {"pic": pic_base64, "typeid": typeid}

    try:
        resp = requests.post(IDCARD_RECOG_URL, params=params, data=data, timeout=20)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data_json = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data_json.get("status") != 0:
        return {
            "error": "api_error",
            "code": data_json.get("status"),
            "message": data_json.get("msg"),
        }

    # 文档中 result 为对象，直接返回
    return data_json.get("result", {})


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  idcardrecognition.py '{\"path\":\"id.jpg\",\"typeid\":2}'   # 从本地身份证图像识别\n"
            "  idcardrecognition.py '{\"pic\":\"<base64>\",\"typeid\":2}'  # 直接传 base64\n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[1]
    try:
        req: Dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(req, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)

    # typeid 必填，由 /idcardrecognition/type 查询
    if "typeid" not in req:
        print(
            json.dumps(
                {
                    "error": "invalid_param",
                    "message": "field 'typeid' is required (see /idcardrecognition/type)",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    try:
        typeid = int(req.get("typeid"))
    except Exception:
        print(
            json.dumps(
                {
                    "error": "invalid_param",
                    "message": "field 'typeid' must be an integer",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    pic_info = _build_pic_base64(req)
    if pic_info["error"]:
        print(
            json.dumps(
                {"error": "invalid_param", "message": pic_info["error"]},
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    result = _call_idcard_api(appkey, pic_info["pic"], typeid)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

