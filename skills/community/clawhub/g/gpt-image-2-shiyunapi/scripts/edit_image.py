#!/usr/bin/env python3
"""Edit images through the ShiyunApi image editing endpoint.

Authentication:
  Prefer environment variable SHIYUN_API_KEY.

Example:
  python edit_image.py --image ./input.png --prompt "Replace the background" --output-dir ./out
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://shiyunapi.com/v1/images/edits"
TOKEN_URL = "https://shiyunapi.com/console/token"
TOPUP_URL = "https://shiyunapi.com/console/topup"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
FORMAT_CHOICES = {"png", "jpeg", "webp"}
QUALITY_CHOICES = {"auto", "low", "medium", "high", "standard"}
BACKGROUND_CHOICES = {"auto", "transparent", "opaque"}
MODERATION_CHOICES = {"auto", "low"}
RESPONSE_FORMAT_CHOICES = {"url", "b64_json"}
DOCUMENTED_SIZES = {
    "auto",
    "1024x1024",
    "1536x1024",
    "1024x1536",
    "256x256",
    "512x512",
    "1792x1024",
    "1024x1792",
}
GPT_IMAGE_MAX_BYTES = 25 * 1024 * 1024
MASK_MAX_BYTES = 4 * 1024 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Edit images with ShiyunApi.")
    parser.add_argument("--image", action="append", required=True, help="Input image path. Repeat this option for multiple images.")
    parser.add_argument("--prompt", required=True, help="Edit prompt. Max 32000 characters for gpt-image-2.")
    parser.add_argument("--api-key", default=None, help="ShiyunApi key. Prefer SHIYUN_API_KEY instead.")
    parser.add_argument("--mask", default=None, help="Optional PNG mask path for local editing.")
    parser.add_argument("--model", default="gpt-image-2", help="Model name. Default: gpt-image-2.")
    parser.add_argument("--n", type=int, default=1, help="Number of images, 1-10. Default: 1.")
    parser.add_argument("--size", default="1024x1024", help="Image size or auto. Default: 1024x1024.")
    parser.add_argument("--quality", default="auto", choices=sorted(QUALITY_CHOICES), help="Image quality. Default: auto.")
    parser.add_argument("--background", default="auto", choices=sorted(BACKGROUND_CHOICES), help="Background mode. Default: auto.")
    parser.add_argument("--moderation", default="auto", choices=sorted(MODERATION_CHOICES), help="Moderation mode. Default: auto.")
    parser.add_argument("--response-format", default=None, choices=sorted(RESPONSE_FORMAT_CHOICES), help="Only for dall-e-2: url or b64_json.")
    parser.add_argument("--format", default="png", choices=sorted(FORMAT_CHOICES), help="File extension for saved base64 images. Default: png.")
    parser.add_argument("--output-dir", required=True, help="Directory for edited images and response JSON.")
    parser.add_argument("--timeout", type=int, default=300, help="Request timeout in seconds. Default: 300.")
    parser.add_argument("--raw-response-name", default="response.json", help="File name for raw JSON response.")
    return parser.parse_args()


def fail(message: str, exit_code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def validate_size(size: str) -> None:
    if size == "auto":
        return
    if not re.fullmatch(r"\d+x\d+", size):
        fail("size must be 'auto' or WIDTHxHEIGHT, for example 1024x1024.")
    if size not in DOCUMENTED_SIZES:
        print(f"WARNING: size '{size}' is not listed in the public image editing docs.", file=sys.stderr)


def validate_file(path: Path, allowed_extensions: set[str], max_bytes: int | None, label: str) -> None:
    if not path.exists():
        fail(f"{label} does not exist: {path}")
    if not path.is_file():
        fail(f"{label} is not a file: {path}")
    suffix = path.suffix.lower()
    if suffix not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        fail(f"{label} must use one of these extensions: {allowed}. Got: {suffix or '[none]'}")
    if max_bytes is not None and path.stat().st_size > max_bytes:
        size_mb = path.stat().st_size / (1024 * 1024)
        max_mb = max_bytes / (1024 * 1024)
        fail(f"{label} is too large: {size_mb:.2f}MB. Limit: {max_mb:.0f}MB.")


def validate_args(args: argparse.Namespace) -> tuple[list[Path], Path | None]:
    if not args.prompt.strip():
        fail("prompt cannot be empty.")
    prompt_limit = 1000 if args.model == "dall-e-2" else 32000
    if len(args.prompt) > prompt_limit:
        fail(f"prompt exceeds the documented {prompt_limit} character limit for {args.model}.")
    if not (1 <= args.n <= 10):
        fail("n must be between 1 and 10.")
    validate_size(args.size)
    if args.response_format and args.model.startswith("gpt-image-2"):
        fail("response_format should not be used with gpt-image-2 because it always returns base64 according to the docs.")

    image_paths = [Path(item) for item in args.image]
    if args.model == "dall-e-2" and len(image_paths) > 1:
        fail("dall-e-2 supports only one input image according to the docs.")
    for path in image_paths:
        max_bytes = 4 * 1024 * 1024 if args.model == "dall-e-2" else GPT_IMAGE_MAX_BYTES
        allowed = {".png"} if args.model == "dall-e-2" else IMAGE_EXTENSIONS
        validate_file(path, allowed, max_bytes, "image")

    mask_path = Path(args.mask) if args.mask else None
    if mask_path:
        validate_file(mask_path, {".png"}, MASK_MAX_BYTES, "mask")
    return image_paths, mask_path


def redact(text: str, api_key: str | None) -> str:
    if api_key:
        text = text.replace(api_key, "[REDACTED_API_KEY]")
    return re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED_API_KEY]", text)


def get_api_key(cli_api_key: str | None) -> str | None:
    if cli_api_key:
        return cli_api_key
    env_api_key = os.environ.get("SHIYUN_API_KEY")
    if env_api_key:
        return env_api_key
    if os.name == "nt":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                value, _ = winreg.QueryValueEx(key, "SHIYUN_API_KEY")
                return str(value) if value else None
        except Exception:
            return None
    return None


def guess_mime_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    if guessed:
        return guessed
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "application/octet-stream"


def multipart_field(name: str, value: str, boundary: str) -> bytes:
    return (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"{name}\"\r\n\r\n"
        f"{value}\r\n"
    ).encode("utf-8")


def multipart_file(name: str, path: Path, boundary: str) -> bytes:
    filename = path.name.replace('"', "_")
    content_type = guess_mime_type(path)
    header = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\n"
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    return header + path.read_bytes() + b"\r\n"


def build_multipart_body(args: argparse.Namespace, image_paths: list[Path], mask_path: Path | None) -> tuple[bytes, str]:
    boundary = f"----WorkBuddyShiyunApi{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for path in image_paths:
        chunks.append(multipart_file("image", path, boundary))
    if mask_path:
        chunks.append(multipart_file("mask", mask_path, boundary))

    fields: dict[str, str] = {
        "prompt": args.prompt,
        "model": args.model,
        "n": str(args.n),
        "size": args.size,
        "quality": args.quality,
        "background": args.background,
        "moderation": args.moderation,
    }
    if args.response_format:
        fields["response_format"] = args.response_format

    for name, value in fields.items():
        if value is not None and str(value) != "":
            chunks.append(multipart_field(name, str(value), boundary))
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary


def post_multipart(body: bytes, boundary: str, api_key: str, timeout: int) -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            return response.status, headers, response.read()
    except urllib.error.HTTPError as exc:
        headers = {k.lower(): v for k, v in exc.headers.items()}
        return exc.code, headers, exc.read()
    except TimeoutError:
        fail("Network request timed out before ShiyunApi returned a response. Retry with a larger --timeout or try again later.")
    except urllib.error.URLError as exc:
        fail(f"Network request failed: {exc.reason}")
    raise AssertionError("unreachable")


def parse_response(raw: bytes) -> Any:
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_text": text}


def response_to_text(parsed: Any) -> str:
    if isinstance(parsed, str):
        return parsed
    try:
        return json.dumps(parsed, ensure_ascii=False)
    except TypeError:
        return str(parsed)


def looks_like_balance_error(text: str) -> bool:
    lowered = text.lower()
    indicators = (
        "余额不足",
        "额度不足",
        "欠费",
        "充值",
        "账户余额",
        "insufficient balance",
        "insufficient quota",
        "quota exceeded",
        "billing",
        "payment required",
        "top up",
        "recharge",
    )
    return any(indicator in lowered for indicator in indicators)


def guidance_for_error(status: int, parsed: Any) -> str:
    text = response_to_text(parsed)
    guidance: list[str] = []
    if status in {401, 403}:
        guidance.append(f"请检查诗云API Key 和 Authorization 格式；如未创建 API Key，请进入 {TOKEN_URL} 创建。")
    if status == 413:
        guidance.append("图片文件可能过大；gpt-image-2 单张输入图应小于 25MB，mask 应小于 4MB。")
    if status in {400, 422}:
        guidance.append("请检查 image、mask、prompt、model、n、size、quality、background、moderation 等参数。")
    if looks_like_balance_error(text):
        guidance.append(f"诗云API账户余额可能不足，请进入 {TOPUP_URL} 充值后重试。")
    return " ".join(guidance)


def summarize_error(status: int, parsed: Any, api_key: str | None) -> str:
    if isinstance(parsed, dict):
        candidates = []
        for key in ("error", "message", "msg", "code", "detail"):
            if key in parsed:
                candidates.append(f"{key}: {parsed[key]}")
        base = "; ".join(candidates) if candidates else json.dumps(parsed, ensure_ascii=False)[:1000]
    else:
        base = f"HTTP {status}: undocumented error response"
    guidance = guidance_for_error(status, parsed)
    message = f"{base}. {guidance}" if guidance else base
    return redact(message, api_key)


def iter_image_items(value: Any) -> list[Any]:
    items: list[Any] = []
    if isinstance(value, dict):
        if "data" in value and isinstance(value["data"], list):
            items.extend(value["data"])
        if any(key in value for key in ("url", "b64_json", "base64", "image_base64")):
            items.append(value)
        for key in ("images", "image", "result", "results", "output", "outputs"):
            nested = value.get(key)
            if isinstance(nested, list):
                items.extend(iter_image_items(nested))
            elif isinstance(nested, dict):
                items.extend(iter_image_items(nested))
    elif isinstance(value, list):
        for item in value:
            items.extend(iter_image_items(item))
    return items


def extension_from_url(url: str, fallback: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower().lstrip(".")
    if suffix in FORMAT_CHOICES or suffix == "jpg":
        return "jpeg" if suffix == "jpg" else suffix
    return fallback


def download_url(url: str, destination: Path, timeout: int) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-ShiyunImageEditingSkill/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        destination.write_bytes(response.read())


def save_base64_image(data: str, destination: Path) -> None:
    if data.startswith("data:"):
        _, _, data = data.partition(",")
    destination.write_bytes(base64.b64decode(data))


def save_outputs(parsed: Any, output_dir: Path, image_format: str, timeout: int) -> list[Path]:
    saved: list[Path] = []
    items = iter_image_items(parsed)
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("url"), str):
            ext = extension_from_url(item["url"], image_format)
            target = output_dir / f"image_{index}.{ext}"
            download_url(item["url"], target, timeout)
            saved.append(target)
        else:
            b64_value = None
            for key in ("b64_json", "base64", "image_base64"):
                if isinstance(item.get(key), str):
                    b64_value = item[key]
                    break
            if b64_value:
                target = output_dir / f"image_{index}.{image_format}"
                save_base64_image(b64_value, target)
                saved.append(target)
    return saved


def main() -> None:
    args = parse_args()
    image_paths, mask_path = validate_args(args)
    api_key = get_api_key(args.api_key)
    if not api_key:
        fail(f"Missing API key. Please create a ShiyunApi key at {TOKEN_URL}, then set SHIYUN_API_KEY or pass --api-key.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    body, boundary = build_multipart_body(args, image_paths, mask_path)
    status, headers, raw = post_multipart(body, boundary, api_key, args.timeout)
    parsed = parse_response(raw)

    raw_response_path = output_dir / args.raw_response_name
    raw_response_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")

    if not (200 <= status < 300):
        summary = summarize_error(status, parsed, api_key)
        fail(f"ShiyunApi request failed with HTTP {status}. {summary}. Raw response saved to {raw_response_path}")

    saved = save_outputs(parsed, output_dir, args.format, args.timeout)
    metadata = {
        "api_url": API_URL,
        "status": status,
        "content_type": headers.get("content-type"),
        "model": args.model,
        "image_count": len(image_paths),
        "has_mask": mask_path is not None,
        "raw_response": str(raw_response_path),
        "saved_files": [str(path) for path in saved],
        "created_at": int(time.time()),
    }
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    if saved:
        print("Saved image files:")
        for path in saved:
            print(path)
    else:
        print(f"No direct image URL/base64 fields detected. Raw response saved to: {raw_response_path}")
        print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
