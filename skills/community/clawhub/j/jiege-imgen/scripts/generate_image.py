#!/usr/bin/env python3
"""Generate or edit images through the OpenAI Images API.

Use /images/generations for new images and /images/edits for reference-image
edits. The configured compatible gateway is the default and can be overridden.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import random
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

DEFAULT_BASE_URL = "https://token.minapp.xin/v1"
DEFAULT_MODEL = "gpt-image-2"
RETRYABLE_HTTP_CODES = {408, 409, 425, 429, 500, 502, 503, 504}


@dataclass
class RequestFailure(RuntimeError):
    message: str
    retryable: bool = False

    def __str__(self) -> str:
        return self.message


def load_api_key(auth_file: Path | None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if api_key:
        return api_key
    if auth_file is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not set; export it or pass --auth-file explicitly"
        )
    try:
        payload = json.loads(auth_file.expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Auth file not found: {auth_file}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read auth file: {auth_file}") from exc
    api_key = payload.get("OPENAI_API_KEY") if isinstance(payload, dict) else None
    if not isinstance(api_key, str) or not api_key.strip():
        raise RuntimeError(f"OPENAI_API_KEY is missing from: {auth_file}")
    return api_key.strip()


def request_bytes(request: urllib.request.Request, timeout: int) -> bytes:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        retryable = exc.code in RETRYABLE_HTTP_CODES or 500 <= exc.code <= 599
        raise RequestFailure(
            f"HTTP {exc.code}: {details[:800]}", retryable=retryable
        ) from exc
    except urllib.error.URLError as exc:
        raise RequestFailure(f"Connection error: {exc.reason}", retryable=True) from exc
    except TimeoutError as exc:
        raise RequestFailure(f"Request timed out: {exc}", retryable=True) from exc


def parse_response(raw: bytes) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        preview = raw.decode("utf-8", errors="replace")[:300]
        raise RequestFailure(f"Invalid JSON response: {preview}", retryable=True) from exc


def request_json(
    endpoint: str, api_key: str, body: dict[str, Any], timeout: int
) -> Any:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    return parse_response(request_bytes(request, timeout))


def encode_multipart(
    fields: dict[str, str], files: dict[str, Path]
) -> tuple[bytes, str]:
    """Build a valid multipart request so reference images reach /images/edits."""
    boundary = f"----CodexImage{uuid.uuid4().hex}"
    body = bytearray()
    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        )
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")
    for name, image_path in files.items():
        if not image_path.is_file():
            raise RuntimeError(
                f"Input image does not exist or is not a file: {image_path}"
            )
        content_type = (
            mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
        )
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            (
                f'Content-Disposition: form-data; name="{name}"; '
                f'filename="{image_path.name}"\r\n'
            ).encode()
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
        body.extend(image_path.read_bytes())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    return bytes(body), boundary


def request_multipart(
    endpoint: str,
    api_key: str,
    fields: dict[str, str],
    files: dict[str, Path],
    timeout: int,
) -> Any:
    payload, boundary = encode_multipart(fields, files)
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )
    return parse_response(request_bytes(request, timeout))


def run_with_retries(
    route_name: str,
    operation: Callable[[], bytes],
    retries: int,
    base_delay: float,
) -> bytes:
    last_error: RequestFailure | None = None
    for attempt in range(1, retries + 2):
        try:
            return operation()
        except RequestFailure as exc:
            last_error = exc
            print(
                f"[{route_name}] attempt {attempt}/{retries + 1} failed: {exc}",
                file=sys.stderr,
            )
            if not exc.retryable or attempt > retries:
                break
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            print(f"[{route_name}] retrying in {delay:.1f}s", file=sys.stderr)
            time.sleep(delay)
    if last_error is None:
        raise RequestFailure(f"{route_name} failed without an error response")
    raise last_error


def decode_base64_image(encoded: str, source: str) -> bytes:
    try:
        return base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise RequestFailure(f"{source} returned invalid base64 image data") from exc


def download_image(image_url: str, timeout: int) -> bytes:
    request = urllib.request.Request(image_url, headers={"Accept": "image/*"})
    return request_bytes(request, timeout)


def extract_image_item(item: Any, timeout: int, source: str) -> bytes | None:
    if not isinstance(item, dict):
        return None
    for key in ("b64_json", "result", "image_base64", "base64"):
        encoded = item.get(key)
        if isinstance(encoded, str) and encoded:
            return decode_base64_image(encoded, source)
    image_url = item.get("url") or item.get("image_url")
    if isinstance(image_url, str) and image_url:
        if image_url.startswith("data:image/") and "," in image_url:
            return decode_base64_image(image_url.split(",", 1)[1], source)
        return download_image(image_url, timeout)
    content = item.get("content")
    if isinstance(content, list):
        for child in content:
            image = extract_image_item(child, timeout, source)
            if image is not None:
                return image
    return None


def extract_image_bytes(result: Any, timeout: int, source: str) -> bytes:
    if isinstance(result, dict):
        data = result.get("data")
        if isinstance(data, list):
            for item in data:
                image = extract_image_item(item, timeout, source)
                if image is not None:
                    return image
        image = extract_image_item(result, timeout, source)
        if image is not None:
            return image
    raise RequestFailure(f"{source} response does not contain image data", retryable=True)


def api_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def request_generation(
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    size: str,
    quality: str,
    timeout: int,
) -> bytes:
    result = request_json(
        api_url(base_url, "/images/generations"),
        api_key,
        {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality,
            "output_format": "png",
        },
        timeout,
    )
    return extract_image_bytes(result, timeout, "Images API")


def request_edit(
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    input_image: Path,
    size: str,
    quality: str,
    timeout: int,
) -> bytes:
    result = request_multipart(
        api_url(base_url, "/images/edits"),
        api_key,
        {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "output_format": "png",
        },
        {"image": input_image},
        timeout,
    )
    return extract_image_bytes(result, timeout, "Images edit API")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit an image through the OpenAI Images API."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Image-generation or edit prompt")
    prompt_group.add_argument("--prompt-file", type=Path, help="UTF-8 prompt file")
    parser.add_argument("--output", type=Path, required=True, help="Output PNG path")
    parser.add_argument(
        "--input-image", type=Path, help="Reference image; enables /images/edits"
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL),
        help="API base URL",
    )
    parser.add_argument(
        "--size",
        default="1024x1024",
        choices=("1024x1024", "1024x1536", "1536x1024", "auto"),
    )
    parser.add_argument(
        "--quality", default="high", choices=("low", "medium", "high", "auto")
    )
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument(
        "--auth-file",
        type=Path,
        help="Optional explicit JSON file containing OPENAI_API_KEY",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.retries < 0 or args.retry_delay < 0 or args.timeout <= 0:
            raise RuntimeError(
                "--retries and --retry-delay must be non-negative; --timeout must be positive"
            )
        prompt = args.prompt
        if args.prompt_file is not None:
            prompt = args.prompt_file.read_text(encoding="utf-8").strip()
        if not prompt or not prompt.strip():
            raise RuntimeError("Prompt cannot be empty")
        api_key = load_api_key(args.auth_file)
        if args.input_image is not None:
            operation = lambda: request_edit(
                args.base_url,
                api_key,
                args.model,
                prompt.strip(),
                args.input_image,
                args.size,
                args.quality,
                args.timeout,
            )
            route = "edits"
        else:
            operation = lambda: request_generation(
                args.base_url,
                api_key,
                args.model,
                prompt.strip(),
                args.size,
                args.quality,
                args.timeout,
            )
            route = "generations"
        image_bytes = run_with_retries(
            f"Images {route} API", operation, args.retries, args.retry_delay
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(image_bytes)
        print(
            json.dumps(
                {"output": str(args.output.resolve()), "route": route},
                ensure_ascii=False,
            )
        )
        return 0
    except (OSError, RuntimeError, RequestFailure) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
