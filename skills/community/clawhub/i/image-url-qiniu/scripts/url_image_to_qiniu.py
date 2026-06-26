#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests>=2.31.0",
#   "qiniu>=7.13.0",
# ]
# ///
"""
从公网 URL 下载图片并上传到七牛，打印 MEDIA_URL: <七牛公网地址>
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path
from urllib.parse import urlparse

import requests

IMAGE_TYPES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "image/svg+xml": ".svg",
}


def require_qiniu_env() -> tuple[str, str, str, str]:
    keys = ("QINIU_ACCESS_KEY", "QINIU_SECRET_KEY", "QINIU_BUCKET", "QINIU_PUBLIC_BASE_URL")
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        print("Error: 缺少七牛环境变量: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)
    return tuple(os.environ[k] for k in keys)  # type: ignore[return-value]


def ext_from_url(url: str) -> str | None:
    path = urlparse(url).path
    if not path:
        return None
    suf = Path(path).suffix.lower()
    if suf in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}:
        return ".jpg" if suf == ".jpeg" else suf
    return None


def pick_extension(content_type: str | None, url: str) -> str:
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        if ct in IMAGE_TYPES:
            return IMAGE_TYPES[ct]
        if ct.startswith("image/"):
            return ".img"
    ex = ext_from_url(url)
    return ex if ex else ".bin"


def is_allowed_image_type(content_type: str | None) -> bool:
    if not content_type:
        return False
    ct = content_type.split(";")[0].strip().lower()
    if ct.startswith("image/"):
        return True
    # 部分 CDN 对图片返回 octet-stream
    return ct in ("application/octet-stream", "binary/octet-stream")


def sniff_image_ext(data: bytes) -> str | None:
    if len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if len(data) >= 3 and data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if len(data) >= 6 and data[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if len(data) >= 2 and data[:2] == b"BM":
        return ".bmp"
    return None


def download_image(url: str, max_bytes: int, timeout: float, verify_ssl: bool) -> tuple[bytes, str]:
    headers = {
        "User-Agent": "OpenClaw-image-url-qiniu/1.0 (image mirror; +https://github.com/openclaw)",
        "Accept": "image/*,*/*;q=0.8",
    }
    with requests.get(
        url,
        headers=headers,
        timeout=timeout,
        verify=verify_ssl,
        stream=True,
        allow_redirects=True,
    ) as r:
        r.raise_for_status()
        ct = r.headers.get("Content-Type", "")
        if not is_allowed_image_type(ct):
            print(
                f"Error: 响应不是图片类型 (Content-Type: {ct or '空'})",
                file=sys.stderr,
            )
            sys.exit(1)
        chunks: list[bytes] = []
        total = 0
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > max_bytes:
                print(f"Error: 超过体积上限 {max_bytes} 字节", file=sys.stderr)
                sys.exit(1)
            chunks.append(chunk)
        data = b"".join(chunks)
        ext = pick_extension(ct, url)
        ct_main = ct.split(";")[0].strip().lower() if ct else ""
        if ct_main in ("application/octet-stream", "binary/octet-stream") or ext in (".bin", ".img"):
            sniffed = sniff_image_ext(data)
            if not sniffed:
                print(
                    "Error: 无法从内容识别为常见图片格式（PNG/JPEG/GIF/WebP/BMP）",
                    file=sys.stderr,
                )
                sys.exit(1)
            ext = sniffed
        return data, ext


def upload_qiniu(
    data: bytes,
    ext: str,
    access_key: str,
    secret_key: str,
    bucket: str,
    public_base: str,
    key_prefix: str,
) -> str:
    from qiniu import Auth, put_data

    prefix = key_prefix.strip("/")
    suffix = ext if ext.startswith(".") else f".{ext}"
    name = f"{uuid.uuid4().hex}{suffix}"
    key = f"{prefix}/{name}" if prefix else name
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket, key, 3600)
    _ret, info = put_data(token, key, data)
    if info.status_code != 200:
        print(
            f"Error: 七牛上传失败 status={info.status_code} body={info.text_body}",
            file=sys.stderr,
        )
        sys.exit(1)
    base = public_base.rstrip("/")
    return f"{base}/{key}"


def main() -> None:
    parser = argparse.ArgumentParser(description="从 URL 下载图片并上传到七牛")
    parser.add_argument("--url", "-u", required=True, help="图片 HTTP(S) 地址")
    parser.add_argument(
        "--max-mb",
        type=float,
        default=25.0,
        help="最大允许体积（MB），默认 25",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="下载超时（秒），默认 60",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="下载时关闭 SSL 校验（慎用）",
    )
    args = parser.parse_args()

    url = args.url.strip()
    if not url.startswith(("http://", "https://")):
        print("Error: --url 须为 http:// 或 https:// 开头", file=sys.stderr)
        sys.exit(2)

    max_bytes = int(args.max_mb * 1024 * 1024)
    access_key, secret_key, bucket, public_base = require_qiniu_env()
    key_prefix = os.environ.get("QINIU_KEY_PREFIX", "openclaw/url-import")

    print(f"Fetching: {url}")
    data, ext = download_image(
        url,
        max_bytes=max_bytes,
        timeout=args.timeout,
        verify_ssl=not args.no_verify_ssl,
    )
    print(f"Downloaded {len(data)} bytes, uploading to Qiniu…")

    qiniu_url = upload_qiniu(
        data,
        ext,
        access_key,
        secret_key,
        bucket,
        public_base,
        key_prefix,
    )
    print(f"MEDIA_URL: {qiniu_url}")


if __name__ == "__main__":
    main()
