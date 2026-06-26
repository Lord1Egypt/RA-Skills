#!/usr/bin/env python3
"""CLI wrapper for the Nano Banana REST API."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://www.nananobanana.com/api/v1"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36 NanoBananaSkill/0.1"
)


class ApiError(Exception):
    """Raised when the API returns an error or unexpected payload."""

    def __init__(self, status: int, payload: Any):
        super().__init__(f"HTTP {status}")
        self.status = status
        self.payload = payload


def get_api_key(explicit_key: str | None) -> str | None:
    return explicit_key or os.getenv("NANO_BANANA_API_KEY") or os.getenv("NB_API_KEY")


def build_headers(
    api_key: str | None,
    *,
    require_auth: bool = False,
    include_json: bool = False,
) -> dict[str, str]:
    headers: dict[str, str] = {"User-Agent": DEFAULT_USER_AGENT}
    if include_json:
        headers["Content-Type"] = "application/json"

    resolved_key = get_api_key(api_key)
    if resolved_key:
        headers["Authorization"] = f"Bearer {resolved_key}"
    elif require_auth:
        raise SystemExit(
            "Missing API key. Set NANO_BANANA_API_KEY or NB_API_KEY, or pass --api-key."
        )

    return headers


def parse_body(raw_body: bytes) -> Any:
    if not raw_body:
        return None

    text = raw_body.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def request_json(
    method: str,
    path: str,
    *,
    api_key: str | None,
    body: dict[str, Any] | None = None,
    timeout: int = 120,
    require_auth: bool = False,
) -> tuple[int, Any]:
    base_url = os.getenv("NANO_BANANA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}{path}"
    headers = build_headers(api_key, require_auth=require_auth, include_json=body is not None)
    payload = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, parse_body(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, parse_body(exc.read())
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc}") from exc


def emit(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def ensure_success(status: int, payload: Any) -> Any:
    if 200 <= status < 300:
        return payload
    raise ApiError(status, payload)


def infer_extension(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    return suffix if suffix else ".png"


def download_images(image_urls: list[str], download_dir: str, prefix: str) -> list[str]:
    target_dir = Path(download_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[str] = []

    for index, image_url in enumerate(image_urls, start=1):
        filename = f"{prefix}-{index}{infer_extension(image_url)}"
        destination = target_dir / filename
        request = urllib.request.Request(image_url, headers={"User-Agent": DEFAULT_USER_AGENT})
        with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as fh:
            shutil.copyfileobj(response, fh)
        downloaded.append(str(destination))

    return downloaded


def command_models(args: argparse.Namespace) -> int:
    status, payload = request_json("GET", "/models", api_key=None, timeout=args.timeout)
    emit(ensure_success(status, payload))
    return 0


def command_credits(args: argparse.Namespace) -> int:
    status, payload = request_json(
        "GET",
        "/credits",
        api_key=args.api_key,
        timeout=args.timeout,
        require_auth=True,
    )
    emit(ensure_success(status, payload))
    return 0


def poll_generation(
    generation_id: str,
    *,
    api_key: str | None,
    timeout: int,
    wait: bool,
    poll_interval: int,
    max_polls: int,
) -> Any:
    for attempt in range(1, max_polls + 1):
        status, payload = request_json(
            "GET",
            f"/generate?id={urllib.parse.quote(generation_id)}",
            api_key=api_key,
            timeout=timeout,
            require_auth=True,
        )
        ensure_success(status, payload)
        data = payload.get("data", {}) if isinstance(payload, dict) else {}
        processing_status = data.get("processingStatus")

        if not wait or processing_status in {"completed", "failed"}:
            return payload

        print(
            f"[poll {attempt}/{max_polls}] status={processing_status or 'unknown'}",
            file=sys.stderr,
        )
        time.sleep(poll_interval)

    raise SystemExit(f"Polling timed out after {max_polls} attempts.")


def command_poll(args: argparse.Namespace) -> int:
    payload = poll_generation(
        args.id,
        api_key=args.api_key,
        timeout=args.timeout,
        wait=args.wait,
        poll_interval=args.poll_interval,
        max_polls=args.max_polls,
    )
    emit(payload)
    return 0


def handle_downloads(payload: Any, download_dir: str | None) -> Any:
    if not download_dir or not isinstance(payload, dict):
        return payload

    image_urls: list[str] = []
    generation_id = "nano-banana"

    if payload.get("imageUrls"):
        image_urls = payload["imageUrls"]
        generation_id = payload.get("generationId") or generation_id
    elif payload.get("data", {}).get("outputImageUrls"):
        image_urls = payload["data"]["outputImageUrls"]
        generation_id = payload["data"].get("id") or generation_id

    if image_urls:
        payload = dict(payload)
        payload["_downloadedFiles"] = download_images(image_urls, download_dir, generation_id)

    return payload


def handle_stream(args: argparse.Namespace, body: dict[str, Any]) -> int:
    base_url = os.getenv("NANO_BANANA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    headers = build_headers(args.api_key, require_auth=True, include_json=True)
    request = urllib.request.Request(
        f"{base_url}/generate",
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            final_event: dict[str, Any] | None = None
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data: "):
                    continue

                try:
                    event = json.loads(line[6:])
                except json.JSONDecodeError:
                    print(line)
                    continue

                emit(event)
                if event.get("type") == "complete":
                    final_event = event
                if event.get("type") == "error":
                    return 1

            if final_event and args.download_dir:
                payload = handle_downloads(
                    {
                        "generationId": final_event.get("data", {}).get("generationId"),
                        "imageUrls": final_event.get("data", {}).get("imageUrls", []),
                    },
                    args.download_dir,
                )
                emit(payload)
            return 0
    except urllib.error.HTTPError as exc:
        emit({"status": exc.code, "error": parse_body(exc.read())})
        return 1
    except urllib.error.URLError as exc:
        raise SystemExit(f"Stream request failed: {exc}") from exc


def build_generation_body(args: argparse.Namespace) -> dict[str, Any]:
    body: dict[str, Any] = {"prompt": args.prompt}
    if args.model:
        body["selectedModel"] = args.model
    if args.aspect_ratio:
        body["aspectRatio"] = args.aspect_ratio
    if args.reference_image_url:
        body["referenceImageUrls"] = args.reference_image_url
    if args.mode != "sync":
        body["mode"] = args.mode
    return body


def command_generate(args: argparse.Namespace) -> int:
    body = build_generation_body(args)

    if args.mode == "stream":
        return handle_stream(args, body)

    status, payload = request_json(
        "POST",
        "/generate",
        api_key=args.api_key,
        body=body,
        timeout=args.timeout,
        require_auth=True,
    )
    payload = ensure_success(status, payload)

    if args.mode == "async" and args.wait:
        generation_id = payload.get("generationId")
        if not generation_id:
            raise SystemExit("Async submission succeeded but no generationId was returned.")
        payload = poll_generation(
            generation_id,
            api_key=args.api_key,
            timeout=args.timeout,
            wait=True,
            poll_interval=args.poll_interval,
            max_polls=args.max_polls,
        )

    payload = handle_downloads(payload, args.download_dir)
    emit(payload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Nano Banana REST API CLI")
    parser.add_argument("--api-key", help="API key. Defaults to NANO_BANANA_API_KEY or NB_API_KEY.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-request timeout in seconds. Default: 120.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    models_parser = subparsers.add_parser("models", help="List available models.")
    models_parser.set_defaults(func=command_models)

    credits_parser = subparsers.add_parser("credits", help="Get remaining credits.")
    credits_parser.set_defaults(func=command_credits)

    poll_parser = subparsers.add_parser("poll", help="Poll an async generation.")
    poll_parser.add_argument("--id", required=True, help="Generation ID returned by async mode.")
    poll_parser.add_argument("--wait", action="store_true", help="Poll until completion or failure.")
    poll_parser.add_argument(
        "--poll-interval",
        type=int,
        default=3,
        help="Seconds between polling attempts. Default: 3.",
    )
    poll_parser.add_argument(
        "--max-polls",
        type=int,
        default=60,
        help="Maximum polling attempts when --wait is set. Default: 60.",
    )
    poll_parser.set_defaults(func=command_poll)

    generate_parser = subparsers.add_parser("generate", help="Create an image generation.")
    generate_parser.add_argument("--prompt", required=True, help="Prompt text.")
    generate_parser.add_argument(
        "--mode",
        choices=["sync", "stream", "async"],
        default="sync",
        help="Request mode. Default: sync.",
    )
    generate_parser.add_argument("--model", help="Model id from the /models endpoint.")
    generate_parser.add_argument("--aspect-ratio", help="Aspect ratio string such as 1:1 or 16:9.")
    generate_parser.add_argument(
        "--reference-image-url",
        action="append",
        help="Reference image URL. Repeat the flag for multiple images.",
    )
    generate_parser.add_argument(
        "--wait",
        action="store_true",
        help="In async mode, poll until the job reaches a terminal state.",
    )
    generate_parser.add_argument(
        "--poll-interval",
        type=int,
        default=3,
        help="Seconds between polling attempts in async wait mode. Default: 3.",
    )
    generate_parser.add_argument(
        "--max-polls",
        type=int,
        default=60,
        help="Maximum polling attempts in async wait mode. Default: 60.",
    )
    generate_parser.add_argument(
        "--download-dir",
        help="Directory where returned image URLs should be downloaded.",
    )
    generate_parser.set_defaults(func=command_generate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.func(args)
    except ApiError as exc:
        emit({"status": exc.status, "error": exc.payload})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
