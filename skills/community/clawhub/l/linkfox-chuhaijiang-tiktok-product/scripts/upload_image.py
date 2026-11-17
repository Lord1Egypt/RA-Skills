#!/usr/bin/env python3
"""Upload a local image with the accelerated presign API and print safe metadata."""

import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_PATH = "/chuhaijiang/upload/presigned-url"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def get_api_base() -> str:
    """网关基础地址：env LINKFOX_TOOL_GATEWAY 优先，缺省回退正式地址。"""
    return (os.environ.get("LINKFOX_TOOL_GATEWAY") or "https://tool-gateway.linkfox.com").rstrip("/")


def get_api_key() -> str:
    key = os.environ.get("LINKFOX_AGENT_API_KEY") or os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Set LINKFOX_AGENT_API_KEY or LINKFOXAGENT_API_KEY first.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return key


def request_upload_target(file_name: str):
    payload = json.dumps({"fileName": file_name}).encode("utf-8")
    request = Request(
        get_api_base() + API_PATH,
        data=payload,
        headers={
            "Authorization": get_api_key(),
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/2.0",
            "SESSION_ID": (os.environ.get("SESSION_ID") or "").strip(),
            "MESSAGE_ID": os.environ.get("MESSAGE_ID", ""),
            "MODE_ID": os.environ.get("MODE_ID", ""),
            "APP_NAME": os.environ.get("APP_NAME", ""),
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=150) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        print(f"Failed to request upload target: HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        raise SystemExit(1) from exc
    except (URLError, json.JSONDecodeError) as exc:
        print(f"Failed to request upload target: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if not isinstance(result, dict) or result.get("errcode") not in (None, 200):
        message = result.get("errmsg", "unknown business error") if isinstance(result, dict) else "invalid response"
        print(f"Failed to request upload target: {message}", file=sys.stderr)
        raise SystemExit(1)

    data = result.get("data") if isinstance(result.get("data"), dict) else {}
    # The accelerated API documents `url` as the PUT target. `signed_url` is
    # the temporary read URL and must never be used as an upload fallback.
    upload_url = data.get("url")
    os_key = data.get("os_key") or data.get("osKey")
    os_bucket = data.get("os_bucket") or data.get("osBucket")
    if not upload_url or not os_key:
        print("Upload target response did not contain url and os_key.", file=sys.stderr)
        raise SystemExit(1)
    return (
        str(upload_url),
        str(os_key),
        os_bucket,
        result.get("request_id"),
        result.get("errcode"),
        result.get("errmsg"),
        sorted(data.keys()),
    )


def upload_file(upload_url: str, file_path: Path, content_type: str) -> int:
    request = Request(
        upload_url,
        data=file_path.read_bytes(),
        headers={"Content-Type": content_type},
        method="PUT",
    )
    try:
        with urlopen(request, timeout=150) as response:
            if response.status not in (200, 201, 204):
                raise RuntimeError(f"unexpected upload status {response.status}")
            return response.status
    except (HTTPError, URLError, RuntimeError) as exc:
        print(f"Image upload failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: upload_image.py <local-image.jpg|jpeg|png>", file=sys.stderr)
        raise SystemExit(1)

    file_path = Path(sys.argv[1]).expanduser().resolve()
    if not file_path.is_file():
        print(f"File not found: {file_path}", file=sys.stderr)
        raise SystemExit(1)
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        print("Unsupported image format. Use jpg, jpeg, or png.", file=sys.stderr)
        raise SystemExit(1)

    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    (
        upload_url,
        os_key,
        os_bucket,
        request_id,
        errcode,
        errmsg,
        presign_data_fields,
    ) = request_upload_target(file_path.name)
    upload_status = upload_file(upload_url, file_path, content_type)
    print(
        json.dumps(
            {
                "osKey": os_key,
                "osBucket": os_bucket,
                "fileName": file_path.name,
                "contentType": content_type,
                "fileSize": file_path.stat().st_size,
                "uploadStatus": upload_status,
                "requestId": request_id,
                "errcode": errcode,
                "errmsg": errmsg,
                "presignDataFields": presign_data_fields,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
