#!/usr/bin/env python3
"""Generate images through the ShiyunApi text-to-image endpoint.

Authentication:
  Prefer environment variable SHIYUN_API_KEY.

Example:
  python generate_image.py --prompt "A watercolor cat reading a book" --output-dir ./out
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://shiyunapi.com/v1/images/generations"
TOKEN_URL = "https://shiyunapi.com/console/token"
TOPUP_URL = "https://shiyunapi.com/console/topup"
MODEL_FIELD_CHOICES = {"model", "modal", "auto"}
QUALITY_CHOICES = {"low", "medium", "high", "auto"}
FORMAT_CHOICES = {"png", "jpeg", "webp"}
DOCUMENTED_SIZES = {
    "auto",
    "1024x1024",
    "1536x1024",
    "1024x1536",
    "2048x2048",
    "2048x1152",
    "3840x2160",
    "2160x3840",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images with ShiyunApi.")
    parser.add_argument("--prompt", required=True, help="Image prompt, max 1000 characters.")
    parser.add_argument("--api-key", default=None, help="ShiyunApi key. Prefer SHIYUN_API_KEY instead.")
    parser.add_argument("--model", default="gpt-image-2", help="Model name. Default: gpt-image-2.")
    parser.add_argument("--model-field", default="model", choices=sorted(MODEL_FIELD_CHOICES), help="Request field for model name. Default: model.")
    parser.add_argument("--n", type=int, default=1, help="Number of images, 1-10. Default: 1.")
    parser.add_argument("--size", default="1024x1024", help="Image size or auto. Default: 1024x1024.")
    parser.add_argument("--quality", default="auto", choices=sorted(QUALITY_CHOICES), help="Image quality. Default: auto.")
    parser.add_argument("--format", default="png", choices=sorted(FORMAT_CHOICES), help="Image format. Default: png.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated images and response JSON.")
    parser.add_argument("--timeout", type=int, default=180, help="Request timeout in seconds. Default: 180.")
    parser.add_argument("--raw-response-name", default="response.json", help="File name for raw JSON response.")
    return parser.parse_args()


def fail(message: str, exit_code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def validate_size(size: str) -> None:
    if size == "auto":
        return
    match = re.fullmatch(r"(\d+)x(\d+)", size)
    if not match:
        fail("size must be 'auto' or WIDTHxHEIGHT, for example 1024x1024.")
    width = int(match.group(1))
    height = int(match.group(2))
    long_side = max(width, height)
    short_side = min(width, height)
    total_pixels = width * height
    if long_side > 3840:
        fail("size violates ShiyunApi constraint: maximum side length must be <= 3840px.")
    if width % 16 != 0 or height % 16 != 0:
        fail("size violates ShiyunApi constraint: width and height must be multiples of 16px.")
    if long_side / short_side > 3:
        fail("size violates ShiyunApi constraint: long side / short side must be <= 3:1.")
    if not (655360 <= total_pixels <= 8294400):
        fail("size violates ShiyunApi constraint: total pixels must be between 655360 and 8294400.")


def validate_args(args: argparse.Namespace) -> None:
    if len(args.prompt) > 1000:
        fail("prompt exceeds the documented 1000 character limit.")
    if not (1 <= args.n <= 10):
        fail("n must be between 1 and 10.")
    validate_size(args.size)
    if args.size not in DOCUMENTED_SIZES:
        print(f"WARNING: size '{args.size}' is valid by constraints but not listed in documented examples.", file=sys.stderr)


def build_payload(args: argparse.Namespace, field: str) -> dict[str, Any]:
    return {
        field: args.model,
        "prompt": args.prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "format": args.format,
    }


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


def post_json(payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, dict[str, str], bytes]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
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
        for key in ("images", "result", "results", "output"):
            nested = value.get(key)
            if isinstance(nested, list):
                items.extend(nested)
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
    request = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-ShiyunImageSkill/1.0"})
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


def should_retry_with_alternate_field(status: int, parsed: Any) -> bool:
    if status not in {400, 422}:
        return False
    text = json.dumps(parsed, ensure_ascii=False).lower() if not isinstance(parsed, str) else parsed.lower()
    hints = ("model", "modal", "missing", "required", "invalid", "参数", "字段", "模型")
    return any(hint in text for hint in hints)


def main() -> None:
    args = parse_args()
    validate_args(args)
    api_key = get_api_key(args.api_key)
    if not api_key:
        fail(f"Missing API key. Please create a ShiyunApi key at {TOKEN_URL}, then set SHIYUN_API_KEY or pass --api-key.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fields_to_try = [args.model_field]
    if args.model_field == "auto":
        fields_to_try = ["model", "modal"]

    final_status = 0
    final_headers: dict[str, str] = {}
    final_raw = b""
    final_parsed: Any = None
    used_field = fields_to_try[0]

    for attempt_index, field in enumerate(fields_to_try, start=1):
        payload = build_payload(args, field)
        status, headers, raw = post_json(payload, api_key, args.timeout)
        parsed = parse_response(raw)
        final_status, final_headers, final_raw, final_parsed, used_field = status, headers, raw, parsed, field
        if 200 <= status < 300:
            break
        if attempt_index == 1 and len(fields_to_try) > 1 and should_retry_with_alternate_field(status, parsed):
            print("WARNING: first request failed with likely model-field validation issue; retrying with alternate field.", file=sys.stderr)
            continue
        break

    raw_response_path = output_dir / args.raw_response_name
    raw_response_path.write_text(json.dumps(final_parsed, ensure_ascii=False, indent=2), encoding="utf-8")

    if not (200 <= final_status < 300):
        summary = summarize_error(final_status, final_parsed, api_key)
        fail(f"ShiyunApi request failed with HTTP {final_status}. {summary}. Raw response saved to {raw_response_path}")

    saved = save_outputs(final_parsed, output_dir, args.format, args.timeout)
    metadata = {
        "api_url": API_URL,
        "used_model_field": used_field,
        "status": final_status,
        "content_type": final_headers.get("content-type"),
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
