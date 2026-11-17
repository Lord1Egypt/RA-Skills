#!/usr/bin/env python3
"""linkfox-os upload 共享模块：agent-server 调用 + AWS SigV4 单请求 PUT 签名。

被 upload_file.py 复用；不直接调用。纯 stdlib（urllib + hmac + hashlib + uuid），
不引入 boto3 / requests。
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import hmac
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
from typing import Any
from urllib.request import Request, urlopen


def _get_api_key() -> str:
    """API key：LINKFOXAGENT_API_KEY。"""
    return os.environ.get("LINKFOXAGENT_API_KEY") or ""


def _get_agent_base() -> str:
    base = os.environ.get("LINKFOXAGENT_BASE_URL") or "https://agent-api.linkfox.com"
    return base.rstrip("/")


def _stderr_tag() -> str:
    return "[linkfox-os/upload]"


# ─── agent-server 调用 ───────────────────────────────────────────────


def agent_post(path: str, body: dict | None = None) -> dict:
    """POST 到 agent-server，Authorization: <api_key>；重试 3 次 (1s/2s 退避)。
    与 onboarding/setup_common.gateway_post 语义一致，但不放到同一份文件避免耦合。
    """
    base = _get_agent_base()
    url = f"{base}{path if path.startswith('/') else '/' + path}"
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("缺少 LINKFOXAGENT_API_KEY 环境变量")

    payload = json.dumps(body or {}).encode()
    last_exc: Exception = RuntimeError("未知错误")
    for attempt in range(3):
        if attempt:
            time.sleep(1 << (attempt - 1))
        req = Request(
            url,
            method="POST",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": api_key},
        )
        try:
            with urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
            return json.loads(raw)
        except urllib.error.HTTPError as e:
            status = e.code
            raw = e.read().decode()[:300]
            if status in (401, 403):
                raise RuntimeError(f"鉴权失败（{status}）: {raw}")
            last_exc = RuntimeError(f"HTTP {status}: {raw}")
            if status not in (408, 429, 500, 502, 503, 504):
                raise last_exc
        except Exception as e:
            last_exc = RuntimeError(f"agent-server 请求失败: {e}")
            print(
                f"{_stderr_tag()} agent_post attempt {attempt+1}/3 失败: {e}",
                file=sys.stderr,
            )
    raise last_exc


# ─── AWS SigV4 单请求 PUT ────────────────────────────────────────────
#
# 见 AWS 官方文档: https://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
# 请求头必备：
#   Authorization: AWS4-HMAC-SHA256 Credential=<AK>/<date>/<region>/s3/aws4_request,
#                                   SignedHeaders=..., Signature=...
#   x-amz-date: yyyymmddTHHMMSSZ
#   x-amz-security-token: <sessionToken>
#   x-amz-content-sha256: <sha256 of body>
#   Content-Type: <mime>


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _hmac(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode(), hashlib.sha256).digest()


def _derive_signing_key(secret: str, date_stamp: str, region: str, service: str) -> bytes:
    k = _hmac(("AWS4" + secret).encode(), date_stamp)
    k = _hmac(k, region)
    k = _hmac(k, service)
    return _hmac(k, "aws4_request")


def _encode_path_segment(seg: str) -> str:
    # RFC 3986 unreserved 字符 + "/" 由调用者切分保留。AWS SigV4 要求路径按 URI encoding 后
    # 参与签名；不 encode "/" 分隔符本身。
    return urllib.parse.quote(seg, safe="")


def _canonical_uri(key: str) -> str:
    # key 形如 "temp/2026/07/<uuid>.jpg"，按 "/" 分段 encode，保留分隔符
    parts = key.split("/")
    return "/" + "/".join(_encode_path_segment(p) for p in parts if p != "")


def build_signed_put_request(
    *,
    region: str,
    bucket: str,
    key: str,
    body: bytes,
    content_type: str,
    access_key_id: str,
    secret_access_key: str,
    session_token: str,
    now: _dt.datetime | None = None,
) -> tuple[str, dict[str, str]]:
    """构造带 SigV4 签名的 PUT 请求 (url, headers)。
    调用方拿到后直接 urllib PUT 即可（body 已参与签名，不能再改）。
    query 字符串固定用 ``x-id=PutObject``（与 AWS SDK v3 默认行为一致）。
    """
    if now is None:
        now = _dt.datetime.utcnow()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    host = f"{bucket}.s3.{region}.amazonaws.com.cn"
    canonical_uri = _canonical_uri(key)
    canonical_query = "x-id=PutObject"
    payload_hash = _sha256_hex(body)

    # 参与签名的 header 全部小写、按字典序（除 host/x-amz-* 外还带上 content-type）
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{host}\n"
        f"x-amz-content-sha256:{payload_hash}\n"
        f"x-amz-date:{amz_date}\n"
        f"x-amz-security-token:{session_token}\n"
    )
    signed_headers = (
        "content-type;host;x-amz-content-sha256;x-amz-date;x-amz-security-token"
    )
    canonical_request = "\n".join(
        [
            "PUT",
            canonical_uri,
            canonical_query,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )

    service = "s3"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            _sha256_hex(canonical_request.encode()),
        ]
    )
    signing_key = _derive_signing_key(secret_access_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key, string_to_sign.encode(), hashlib.sha256
    ).hexdigest()

    authorization = (
        f"AWS4-HMAC-SHA256 Credential={access_key_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    url = f"https://{host}{canonical_uri}?{canonical_query}"
    headers = {
        "Authorization": authorization,
        "Content-Type": content_type,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
        "x-amz-security-token": session_token,
        "Content-Length": str(len(body)),
    }
    return url, headers


def put_to_s3(url: str, headers: dict[str, str], body: bytes) -> None:
    """执行签好名的 PUT。失败抛 RuntimeError 带上响应体前 300 字。"""
    req = Request(url, method="PUT", data=body, headers=headers)
    try:
        with urlopen(req, timeout=60) as resp:
            if resp.status // 100 != 2:
                raise RuntimeError(f"S3 PUT 非 2xx: {resp.status}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")[:300]
        raise RuntimeError(f"S3 PUT 失败 status={e.code}: {raw}")


# ─── 业务辅助 ────────────────────────────────────────────────────────


def guess_mime_type(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


def make_object_key(filename: str, uuid_val: str, now: _dt.datetime | None = None) -> str:
    """按 temp/YYYY/MM/<uuid>.<ext> 生成 S3 对象 key。"""
    if now is None:
        now = _dt.datetime.utcnow()
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    return f"temp/{now.year:04d}/{now.month:02d}/{uuid_val}.{ext}"
