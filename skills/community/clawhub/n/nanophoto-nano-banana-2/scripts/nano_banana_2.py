#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional

GENERATE_URL = "https://nanophoto.ai/api/nano-banana-2/generate"
STATUS_URL = "https://nanophoto.ai/api/nano-banana-2/check-status"
DEFAULT_OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SKILL_NAME = "nano-banana-2"
ENV_KEY_NAME = "NANOPHOTO_API_KEY"
VALID_MODES = {"generate", "edit"}
VALID_ASPECT_RATIOS = {"16:9", "9:16", "4:3", "3:4"}
VALID_IMAGE_QUALITIES = {"1K", "2K", "4K"}
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
DEFAULT_POLL_INTERVAL = 4
DEFAULT_MAX_WAIT = 180


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def load_api_key_from_openclaw_config(config_path: str = DEFAULT_OPENCLAW_CONFIG_PATH) -> Optional[str]:
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError):
        return None

    return (
        config.get("skills", {})
        .get("entries", {})
        .get(SKILL_NAME, {})
        .get("env", {})
        .get(ENV_KEY_NAME)
    )


def resolve_api_key(explicit_api_key: Optional[str]) -> Optional[str]:
    return explicit_api_key or os.environ.get(ENV_KEY_NAME) or load_api_key_from_openclaw_config()


def post_json(url: str, api_key: str, payload: dict, timeout: int, user_agent: str) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://nanophoto.ai",
            "Referer": "https://nanophoto.ai/",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        fail(f"HTTP {exc.code}: {body}")
    except urllib.error.URLError as exc:
        fail(f"Request failed: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON response: {exc}")


def emit(stage: str, response: dict, json_only: bool) -> None:
    if json_only:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"stage": stage, "response": response}, ensure_ascii=False, indent=2), flush=True)


def build_generate_payload(args: argparse.Namespace) -> dict:
    if not args.prompt or not args.prompt.strip():
        fail("--prompt is required.")

    payload = {
        "prompt": args.prompt.strip(),
        "mode": args.mode,
        "aspectRatio": args.aspect_ratio,
        "imageQuality": args.image_quality,
        "googleSearch": args.google_search,
    }

    if args.mode == "edit":
        if not args.input_image_url:
            fail("edit mode requires at least one --input-image-url.")
        if len(args.input_image_url) > 14:
            fail("edit mode supports at most 14 --input-image-url values.")
        payload["inputImageUrls"] = args.input_image_url

    return payload


def submit_generation(args: argparse.Namespace, api_key: str) -> dict:
    payload = build_generate_payload(args)
    return post_json(GENERATE_URL, api_key, payload, args.timeout, args.user_agent)


def check_status(generation_id: str, api_key: str, timeout: int, user_agent: str) -> dict:
    return post_json(STATUS_URL, api_key, {"generationId": generation_id}, timeout, user_agent)


def validate_polling(poll_interval: int, max_wait: int) -> None:
    if poll_interval <= 0:
        fail("--poll-interval must be > 0")
    if max_wait <= 0:
        fail("--max-wait must be > 0")


def run_poll_loop(generation_id: str, api_key: str, args: argparse.Namespace, json_only: bool = False) -> dict:
    validate_polling(args.poll_interval, args.max_wait)
    started = time.time()
    while True:
        elapsed = time.time() - started
        if elapsed > args.max_wait:
            fail(f"Timed out waiting for completion after {args.max_wait} seconds.")

        time.sleep(min(args.poll_interval, max(args.max_wait - elapsed, 0)))
        status_resp = check_status(generation_id, api_key, args.timeout, args.user_agent)
        emit("progress", status_resp, json_only)

        status = status_resp.get("status")
        if status == "completed":
            return status_resp
        if status == "failed" or status_resp.get("success") is False:
            fail("Generation failed; see status response above.")


def do_submit(args: argparse.Namespace, api_key: str) -> None:
    submit = submit_generation(args, api_key)
    emit("submitted", submit, args.json_only)

    generation_id = submit.get("generationId")
    status = submit.get("status")
    if status == "completed":
        return
    if not generation_id:
        fail("No generationId returned from generate endpoint.")

    if args.follow:
        run_poll_loop(generation_id, api_key, args, args.json_only)


def do_status(args: argparse.Namespace, api_key: str) -> None:
    status_resp = check_status(args.generation_id, api_key, args.timeout, args.user_agent)
    emit("status", status_resp, args.json_only)


def add_common_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="NanoPhoto API key")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds (default: 60)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")


def add_generation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--mode", default="generate", choices=sorted(VALID_MODES), help="Generation mode")
    parser.add_argument("--aspect-ratio", default="16:9", choices=sorted(VALID_ASPECT_RATIOS), help="Aspect ratio")
    parser.add_argument("--image-quality", default="1K", choices=sorted(VALID_IMAGE_QUALITIES), help="Image quality")
    parser.add_argument("--google-search", action="store_true", help="Enable Google Search prompt enhancement")
    parser.add_argument("--input-image-url", action="append", default=[], help="Public image URL for edit mode; may be passed up to 14 times")


def add_polling_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Polling interval in seconds (default: 4)")
    parser.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT, help="Maximum total wait time in seconds (default: 180)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit and check Nano Banana 2 image generation tasks.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    submit_parser = subparsers.add_parser("submit", help="Submit an image generation task")
    add_generation_args(submit_parser)
    add_common_auth_args(submit_parser)
    add_polling_args(submit_parser)
    submit_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")
    submit_parser.add_argument("--follow", action="store_true", help="Keep polling in the same process after submission")

    status_parser = subparsers.add_parser("status", help="Check status of an existing generation")
    status_parser.add_argument("--generation-id", required=True, help="Existing Nano Banana 2 generationId")
    add_common_auth_args(status_parser)
    status_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = resolve_api_key(getattr(args, "api_key", None))
    if not api_key:
        fail("Missing API key. Pass --api-key, set NANOPHOTO_API_KEY, or configure ~/.openclaw/openclaw.json skills.entries.nano-banana-2.env.NANOPHOTO_API_KEY.")

    if args.command == "submit":
        do_submit(args, api_key)
        return
    if args.command == "status":
        do_status(args, api_key)
        return

    fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
