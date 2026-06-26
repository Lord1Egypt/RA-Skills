#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional

GENERATE_URL = "https://nanophoto.ai/api/veo-3/generate"
STATUS_URL = "https://nanophoto.ai/api/veo-3/check-status"
DEFAULT_OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SKILL_NAME = "veo-3-1"
ENV_KEY_NAME = "NANOPHOTO_API_KEY"
VALID_GENERATION_TYPES = {"TEXT_2_VIDEO", "FIRST_AND_LAST_FRAMES_2_VIDEO", "REFERENCE_2_VIDEO"}
VALID_ASPECT_RATIOS = {"16:9", "9:16"}
VALID_RESOLUTIONS = {"720p", "1080p", "4k"}
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
DEFAULT_POLL_INTERVAL = 8
DEFAULT_MAX_WAIT = 1800


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


def load_shots_from_json(raw_json: str) -> list:
    try:
        shots = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON for --shots-json: {exc}")
    if not isinstance(shots, list):
        fail("--shots-json must decode to a JSON array of shots.")
    return shots


def normalize_shots(shots: list) -> list:
    if not shots:
        fail("At least one shot is required.")
    if len(shots) > 21:
        fail("A maximum of 21 shots is allowed.")

    normalized = []
    for index, shot in enumerate(shots, start=1):
        if not isinstance(shot, dict):
            fail(f"Shot {index} must be an object.")

        shot_id = shot.get("id") or f"shot-{index}"
        prompt = shot.get("prompt")
        generation_type = shot.get("generationType")
        aspect_ratio = shot.get("aspectRatio")
        image_urls = shot.get("imageUrls")

        if not prompt:
            fail(f"Shot {shot_id} is missing prompt.")
        if generation_type not in VALID_GENERATION_TYPES:
            fail(f"Shot {shot_id} has invalid generationType: {generation_type}")
        if aspect_ratio not in VALID_ASPECT_RATIOS:
            fail(f"Shot {shot_id} has invalid aspectRatio: {aspect_ratio}")

        if generation_type == "TEXT_2_VIDEO":
            if image_urls:
                fail(f"Shot {shot_id} uses TEXT_2_VIDEO and must not include imageUrls.")
        elif generation_type == "FIRST_AND_LAST_FRAMES_2_VIDEO":
            if not isinstance(image_urls, list) or not (1 <= len(image_urls) <= 2):
                fail(f"Shot {shot_id} uses FIRST_AND_LAST_FRAMES_2_VIDEO and requires 1-2 imageUrls.")
        elif generation_type == "REFERENCE_2_VIDEO":
            if not isinstance(image_urls, list) or not (1 <= len(image_urls) <= 3):
                fail(f"Shot {shot_id} uses REFERENCE_2_VIDEO and requires 1-3 imageUrls.")

        normalized_shot = {
            "id": shot_id,
            "prompt": prompt,
            "generationType": generation_type,
            "aspectRatio": aspect_ratio,
        }
        if image_urls:
            normalized_shot["imageUrls"] = image_urls
        normalized.append(normalized_shot)

    return normalized


def build_generate_payload(args: argparse.Namespace) -> dict:
    shots = normalize_shots(load_shots_from_json(args.shots_json))
    if args.resolution in {"1080p", "4k"} and len(shots) != 1:
        fail("1080p and 4k are only supported for single-shot generation.")
    return {"shots": shots, "resolution": args.resolution}


def submit_generation(args: argparse.Namespace, api_key: str) -> dict:
    payload = build_generate_payload(args)
    return post_json(GENERATE_URL, api_key, payload, args.timeout, args.user_agent)


def build_status_payload(task_ids_json: str, resolution: str) -> dict:
    try:
        task_ids = json.loads(task_ids_json)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON for --task-ids-json: {exc}")
    if not isinstance(task_ids, list) or not task_ids:
        fail("--task-ids-json must decode to a non-empty JSON array.")
    return {"taskIds": task_ids, "resolution": resolution}


def check_status(task_ids_json: str, resolution: str, api_key: str, timeout: int, user_agent: str) -> dict:
    payload = build_status_payload(task_ids_json, resolution)
    return post_json(STATUS_URL, api_key, payload, timeout, user_agent)


def validate_polling(poll_interval: int, max_wait: int) -> None:
    if poll_interval <= 0:
        fail("--poll-interval must be > 0")
    if max_wait <= 0:
        fail("--max-wait must be > 0")


def extract_task_ids_json(submit_response: dict) -> str:
    shots = submit_response.get("shots")
    if not isinstance(shots, list) or not shots:
        fail("No shots returned from generate endpoint.")
    task_ids = []
    for shot in shots:
        shot_id = shot.get("shotId")
        task_id = shot.get("taskId")
        if not shot_id or not task_id:
            fail("Generate response is missing shotId or taskId.")
        task_ids.append({"shotId": shot_id, "taskId": task_id})
    return json.dumps(task_ids, ensure_ascii=False)


def run_poll_loop(task_ids_json: str, resolution: str, api_key: str, args: argparse.Namespace, json_only: bool = False) -> dict:
    validate_polling(args.poll_interval, args.max_wait)
    started = time.time()
    while True:
        elapsed = time.time() - started
        if elapsed > args.max_wait:
            fail(f"Timed out waiting for completion after {args.max_wait} seconds.")

        time.sleep(min(args.poll_interval, max(args.max_wait - elapsed, 0)))
        status_resp = check_status(task_ids_json, resolution, api_key, args.timeout, args.user_agent)
        emit("progress", status_resp, json_only)

        status = status_resp.get("status")
        if status == "completed":
            return status_resp
        if status == "failed":
            fail("Generation failed; see status response above.")


def do_submit(args: argparse.Namespace, api_key: str) -> None:
    submit = submit_generation(args, api_key)
    emit("submitted", submit, args.json_only)

    if submit.get("status") == "failed":
        fail("Generation failed; see submitted response above.")

    if args.follow:
        task_ids_json = extract_task_ids_json(submit)
        run_poll_loop(task_ids_json, args.resolution, api_key, args, args.json_only)


def do_status(args: argparse.Namespace, api_key: str) -> None:
    status_resp = check_status(args.task_ids_json, args.resolution, api_key, args.timeout, args.user_agent)
    emit("status", status_resp, args.json_only)


def add_common_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="NanoPhoto API key")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds (default: 60)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")


def add_polling_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Polling interval in seconds (default: 8)")
    parser.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT, help="Maximum total wait time in seconds (default: 1800)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit and check Veo 3.1 video generation tasks.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    submit_parser = subparsers.add_parser("submit", help="Submit a video generation task")
    submit_parser.add_argument("--shots-json", required=True, help="JSON array of shot objects")
    submit_parser.add_argument("--resolution", default="720p", choices=sorted(VALID_RESOLUTIONS), help="Output resolution")
    add_common_auth_args(submit_parser)
    add_polling_args(submit_parser)
    submit_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")
    submit_parser.add_argument("--follow", action="store_true", help="Keep polling in the same process after submission")

    status_parser = subparsers.add_parser("status", help="Check status of an existing Veo generation")
    status_parser.add_argument("--task-ids-json", required=True, help="JSON array of {shotId, taskId} objects")
    status_parser.add_argument("--resolution", default="720p", choices=sorted(VALID_RESOLUTIONS), help="Output resolution")
    add_common_auth_args(status_parser)
    status_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = resolve_api_key(getattr(args, "api_key", None))
    if not api_key:
        fail("Missing API key. Pass --api-key, set NANOPHOTO_API_KEY, or configure ~/.openclaw/openclaw.json skills.entries.veo-3-1.env.NANOPHOTO_API_KEY.")

    if args.command == "submit":
        do_submit(args, api_key)
        return
    if args.command == "status":
        do_status(args, api_key)
        return

    fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
