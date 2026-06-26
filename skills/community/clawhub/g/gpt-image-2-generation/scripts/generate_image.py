#!/usr/bin/env python3
"""Generate images via the WellAPI gpt-image-2 endpoint.

Reads the API key from --api-key, then $WELLAPI_API_KEY, then the per-user
config file. Sends an authenticated POST request, decodes each returned
``b64_json`` payload and writes the bytes to disk.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Make sibling helper importable when the script is invoked directly.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_key import load_api_key, missing_key_message  # noqa: E402

API_URL = "https://wellapi.ai/v1/images/generations"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "low"
DEFAULT_FORMAT = "jpeg"
DEFAULT_N = 1
# WellAPI's image generation endpoint is synchronous; a single request commonly
# takes 1–3 minutes (occasionally longer under load). Default to 10 minutes so
# legitimate long-running jobs are not killed by a premature client timeout.
REQUEST_TIMEOUT = 600  # seconds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images with WellAPI gpt-image-2.",
    )
    parser.add_argument("--prompt", required=True, help="Text prompt for the image.")
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="Number of images (default: 1).")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Image size, e.g. 1024x1024.")
    parser.add_argument(
        "--quality",
        default=DEFAULT_QUALITY,
        choices=["low", "medium", "high"],
        help="Render quality (default: low).",
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        choices=["jpeg", "png", "webp"],
        dest="img_format",
        help="Output image format (default: jpeg).",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path. When --n > 1 an index suffix is appended.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key override. Falls back to $WELLAPI_API_KEY then config file.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help=(
            "HTTP request timeout in seconds. Defaults to $WELLAPI_TIMEOUT or "
            f"{REQUEST_TIMEOUT}s. The endpoint is synchronous and a single "
            "image typically takes 1–3 minutes, so keep this generous."
        ),
    )
    return parser.parse_args()


def resolve_api_key(cli_value: str | None) -> str:
    if cli_value:
        return cli_value.strip()
    key = load_api_key()
    if not key:
        print(missing_key_message(), file=sys.stderr)
        sys.exit(2)
    return key


def resolve_timeout(cli_value: float | None) -> float:
    if cli_value is not None:
        return max(1.0, float(cli_value))
    env = os.environ.get("WELLAPI_TIMEOUT")
    if env:
        try:
            return max(1.0, float(env))
        except ValueError:
            print(
                f"Ignoring invalid WELLAPI_TIMEOUT={env!r}; using default "
                f"{REQUEST_TIMEOUT}s.",
                file=sys.stderr,
            )
    return float(REQUEST_TIMEOUT)


# Hint shown alongside any non-2xx response from WellAPI. A non-200 — 4xx
# (e.g. 400/401/403/404/429) or 5xx — frequently means the API key's group
# does not have available capacity for ``gpt-image-2``. Switching the key's
# group to "官转OpenAI分组" or "优质官转OpenAI分组" usually resolves it.
GROUP_HINT = (
    "提示 / Hint: 若返回状态非 200（如 400 / 401 / 403 / 404 / 429 / 5xx），\n"
    "可能是该 API Key 所属分组资源不足或不支持 gpt-image-2。\n"
    "请前往 https://wellapi.ai 的「API 令牌管理」，将此 API Key 的分组改为\n"
    "  · 官转OpenAI分组\n"
    "  · 优质官转OpenAI分组\n"
    "之一，保存后重新调用本技能。\n"
    "If WellAPI returned a non-200 status, the key's group likely lacks "
    "capacity for gpt-image-2. In WellAPI's token management page, switch "
    "this key's group to '官转OpenAI分组' or '优质官转OpenAI分组' and retry."
)


def call_api(api_key: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "gpt-image-2-generation-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise SystemExit(
            f"WellAPI request failed: HTTP {exc.code} {exc.reason}\n"
            f"{detail}\n\n{GROUP_HINT}"
        ) from exc
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        # ``socket.timeout`` surfaces here when the synchronous call exceeds
        # ``timeout``. Make the remediation obvious to the caller.
        if isinstance(reason, TimeoutError) or "timed out" in str(reason).lower():
            raise SystemExit(
                f"WellAPI request timed out after {timeout:.0f}s. "
                "Image generation is synchronous and can take 1–3 minutes; "
                "retry, or pass --timeout / set WELLAPI_TIMEOUT to a larger value."
            ) from exc
        raise SystemExit(f"Network error contacting WellAPI: {reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"WellAPI returned non-JSON response:\n{raw[:500]}") from exc


def output_paths(user_output: str | None, count: int, ext: str) -> list[Path]:
    timestamp = int(time.time())
    if user_output:
        base = Path(user_output)
        if count == 1:
            return [base]
        stem = base.with_suffix("")
        suffix = base.suffix or f".{ext}"
        return [Path(f"{stem}_{i + 1}{suffix}") for i in range(count)]

    return [Path(f"./gpt-image-2_{timestamp}{'_' + str(i + 1) if count > 1 else ''}.{ext}") for i in range(count)]


def main() -> int:
    args = parse_args()
    api_key = resolve_api_key(args.api_key)
    timeout = resolve_timeout(args.timeout)

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "format": args.img_format,
    }

    response = call_api(api_key, payload, timeout)

    images = response.get("data") or []
    if not images:
        raise SystemExit(f"WellAPI response contained no images:\n{json.dumps(response)[:500]}")

    ext = (response.get("output_format") or args.img_format or "png").lower()
    paths = output_paths(args.output, len(images), ext)

    for path, item in zip(paths, images):
        b64 = item.get("b64_json")
        if not b64:
            raise SystemExit("Image entry missing 'b64_json' field.")
        try:
            data = base64.b64decode(b64)
        except (ValueError, TypeError) as exc:
            raise SystemExit(f"Failed to decode base64 image data: {exc}") from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(str(path.resolve()))

    usage = response.get("usage")
    if usage:
        print(f"# usage: {json.dumps(usage)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
