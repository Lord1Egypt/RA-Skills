#!/usr/bin/env python3
"""Generate images through the imini image generation API."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request


DEFAULT_BASE_URL = "https://openapi.imini.ai/imini/router"
DEFAULT_TIMEOUT = 300.0
DEFAULT_POLL_INTERVAL = 2.0
MAX_PROMPT_LENGTH = 6000
DEFAULT_RESOLUTION = "1K"
MODEL_CAPABILITIES = {
    "google/nano-banana": {
        "max_image_urls": 3,
        "aspect_ratios": {
            "1:1",
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "9:16",
            "16:9",
            "21:9",
        },
        "resolutions": {"1K"},
    },
    "google/nano-banana-pro": {
        "max_image_urls": 14,
        "aspect_ratios": {
            "1:1",
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "9:16",
            "16:9",
            "21:9",
        },
        "resolutions": {"1K", "2K", "4K"},
    },
    "google/nano-banana-2": {
        "max_image_urls": 14,
        "aspect_ratios": {
            "1:1",
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "9:16",
            "16:9",
            "21:9",
            "1:4",
            "1:8",
            "4:1",
            "8:1",
        },
        "resolutions": {"512", "1K", "2K", "4K"},
    },
}
ALLOWED_REFERENCE_TYPES = {"asset", "style"}
TERMINAL_STATUSES = {"succeeded", "failed"}
WAITING_STATUSES = {"queued", "pending", "processing"}


class APIError(RuntimeError):
    """Raised when the remote API returns an actionable error."""


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise APIError(f"Environment variable {name} must be a number, got: {raw!r}") from exc
    if value <= 0:
        raise APIError(f"Environment variable {name} must be > 0, got: {raw!r}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images through the imini image generation API."
    )
    parser.add_argument(
        "--model",
        default="google/nano-banana",
        choices=sorted(MODEL_CAPABILITIES),
        help="Model ID to use for generation.",
    )
    parser.add_argument("--prompt", required=True, help="Prompt text for image generation.")
    parser.add_argument(
        "--image-url",
        action="append",
        default=[],
        help="Public reference image URL. Repeat within the chosen model limit.",
    )
    parser.add_argument(
        "--reference-type",
        default="asset",
        choices=sorted(ALLOWED_REFERENCE_TYPES),
        help="Reference type to apply to every --image-url value.",
    )
    parser.add_argument(
        "--aspect-ratio",
        help="Output aspect ratio.",
    )
    parser.add_argument(
        "--resolution",
        default=DEFAULT_RESOLUTION,
        help="Output resolution. Allowed values depend on the chosen model.",
    )
    parser.add_argument(
        "--out-dir",
        default="output/imagegen",
        help="Directory used to save downloaded result images.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        help="Overall task timeout in seconds. Defaults to IMINI_IMAGE_TIMEOUT or 300.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        help="Polling interval in seconds. Defaults to IMINI_IMAGE_POLL_INTERVAL or 2.",
    )
    return parser.parse_args()


def load_config(args: argparse.Namespace) -> dict[str, Any]:
    api_key = os.getenv("IMINI_IMAGE_API_KEY")
    if not api_key:
        raise APIError(
            "Missing IMINI_IMAGE_API_KEY. Set it in your shell environment before running this script."
        )

    timeout = args.timeout if args.timeout is not None else env_float(
        "IMINI_IMAGE_TIMEOUT", DEFAULT_TIMEOUT
    )
    poll_interval = (
        args.poll_interval
        if args.poll_interval is not None
        else env_float("IMINI_IMAGE_POLL_INTERVAL", DEFAULT_POLL_INTERVAL)
    )
    base_url = os.getenv("IMINI_IMAGE_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

    return {
        "api_key": api_key,
        "base_url": base_url,
        "timeout": timeout,
        "poll_interval": poll_interval,
    }


def validate_args(args: argparse.Namespace) -> None:
    capabilities = MODEL_CAPABILITIES[args.model]
    if len(args.prompt) > MAX_PROMPT_LENGTH:
        raise APIError(f"Prompt exceeds {MAX_PROMPT_LENGTH} characters.")
    if len(args.image_url) > capabilities["max_image_urls"]:
        raise APIError(
            f"Model {args.model!r} supports at most {capabilities['max_image_urls']} --image-url values."
        )
    if args.aspect_ratio and args.aspect_ratio not in capabilities["aspect_ratios"]:
        raise APIError(
            f"Unsupported aspect ratio {args.aspect_ratio!r} for model {args.model!r}."
        )
    if args.resolution not in capabilities["resolutions"]:
        allowed = ", ".join(sorted(capabilities["resolutions"]))
        raise APIError(
            f"Unsupported resolution {args.resolution!r} for model {args.model!r}. Allowed: {allowed}."
        )
    if args.timeout is not None and args.timeout <= 0:
        raise APIError("--timeout must be > 0.")
    if args.poll_interval is not None and args.poll_interval <= 0:
        raise APIError("--poll-interval must be > 0.")


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "imini-imagegen/1.0 (+https://openapi.imini.ai)",
    }


def sanitize_api_key(api_key: str) -> str:
    if len(api_key) <= 5:
        return "*" * len(api_key)
    return f"{api_key[:3]}***{api_key[-2:]}"


def extract_error_message(payload: Any) -> str:
    if isinstance(payload, dict):
        if "code" in payload or "message" in payload or "status" in payload:
            code = payload.get("code")
            message = payload.get("message") or payload.get("error")
            status = payload.get("status")
            request_id = payload.get("request_id")
            parts = [part for part in [code, message] if part]
            suffix = ", ".join(
                str(part) for part in [f"status={status}" if status else None, request_id] if part
            )
            if parts and suffix:
                return f"{': '.join(parts)} ({suffix})"
            if parts:
                return ": ".join(parts)
        err = payload.get("error")
        if isinstance(err, dict):
            code = err.get("code")
            message = err.get("message") or err.get("error")
            status = err.get("status")
            request_id = err.get("request_id")
            parts = [part for part in [code, message] if part]
            suffix = ", ".join(
                str(part) for part in [f"status={status}" if status else None, request_id] if part
            )
            if parts and suffix:
                return f"{': '.join(parts)} ({suffix})"
            if parts:
                return ": ".join(parts)
        if payload.get("message"):
            return str(payload["message"])
    return json.dumps(payload, ensure_ascii=False)


def http_json(
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=60) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            body = resp.read().decode(charset)
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"message": body or exc.reason}
        raise APIError(f"HTTP {exc.code}: {extract_error_message(payload)}") from exc
    except error.URLError as exc:
        raise APIError(f"Network error while calling {url}: {exc.reason}") from exc


def create_task_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "resolution": args.resolution,
    }
    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.image_url:
        payload["images"] = [
            {"url": image_url, "reference_type": args.reference_type}
            for image_url in args.image_url
        ]
    return payload


def create_task(config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    url = f"{config['base_url']}/v1/images/generate"
    headers = build_headers(config["api_key"])
    payload = create_task_payload(args)
    return http_json("POST", url, headers, payload)


def poll_task(config: dict[str, Any], task_id: str) -> dict[str, Any]:
    url = f"{config['base_url']}/v1/images/tasks/{task_id}"
    headers = build_headers(config["api_key"])
    deadline = time.monotonic() + float(config["timeout"])
    last_status = None

    while True:
        if time.monotonic() > deadline:
            raise APIError(
                f"Timed out after {config['timeout']} seconds while waiting for task {task_id}."
            )
        payload = http_json("GET", url, headers)
        status = payload.get("status")
        if status != last_status:
            print(f"[poll] task_id={task_id} status={status}", file=sys.stderr)
            last_status = status
        if status in TERMINAL_STATUSES:
            return payload
        if status not in WAITING_STATUSES:
            raise APIError(f"Unexpected task status {status!r} for task {task_id}.")
        time.sleep(float(config["poll_interval"]))


def choose_extension(image_url: str, content_type: str | None) -> str:
    suffix = Path(image_url).suffix.lower()
    if suffix:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed:
            return guessed
    return ".png"


def download_image(image_url: str, output_path: Path) -> None:
    req = request.Request(image_url, headers={"Accept": "*/*"})
    try:
        with request.urlopen(req, timeout=120) as resp:
            content_type = resp.headers.get("Content-Type")
            data = resp.read()
    except error.HTTPError as exc:
        raise APIError(f"Failed to download {image_url}: HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise APIError(f"Failed to download {image_url}: {exc.reason}") from exc

    ext = choose_extension(image_url, content_type)
    final_path = output_path.with_suffix(ext)
    final_path.write_bytes(data)
    print(f"[saved] {final_path.resolve()}")
    return final_path


def save_images(task_payload: dict[str, Any], out_dir: Path) -> list[Path]:
    images = task_payload.get("images")
    if not images:
        raise APIError("Task succeeded but returned no images.")

    out_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: list[Path] = []

    for index, image in enumerate(images, start=1):
        if not isinstance(image, dict) or not image.get("url"):
            raise APIError(f"Task returned an invalid image entry at index {index - 1}.")
        target = out_dir / f"{task_payload['task_id']}-{index}"
        saved_paths.append(download_image(str(image["url"]), target))
    return saved_paths


def print_summary(submit_payload: dict[str, Any], final_payload: dict[str, Any], saved_paths: list[Path]) -> None:
    print(f"task_id: {submit_payload.get('task_id')}")
    print(f"request_id: {submit_payload.get('request_id') or final_payload.get('request_id')}")
    print(f"status: {final_payload.get('status')}")
    if final_payload.get("completed_at"):
        print(f"completed_at: {final_payload.get('completed_at')}")
    for index, path in enumerate(saved_paths, start=1):
        print(f"image_{index}: {path.resolve()}")


def main() -> int:
    args = parse_args()
    validate_args(args)
    config = load_config(args)

    print(
        f"[config] base_url={config['base_url']} key={sanitize_api_key(config['api_key'])}",
        file=sys.stderr,
    )

    submit_payload = create_task(config, args)
    task_id = submit_payload.get("task_id")
    if not task_id:
        raise APIError(f"Task creation response did not include task_id: {submit_payload}")

    print(
        f"[submit] task_id={task_id} request_id={submit_payload.get('request_id')}",
        file=sys.stderr,
    )

    final_payload = poll_task(config, str(task_id))
    if final_payload.get("status") == "failed":
        raise APIError(
            f"Task {task_id} failed: {extract_error_message(final_payload.get('error'))}"
        )

    output_dir = Path(args.out_dir)
    saved_paths = save_images(final_payload, output_dir)
    print_summary(submit_payload, final_payload, saved_paths)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except APIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
