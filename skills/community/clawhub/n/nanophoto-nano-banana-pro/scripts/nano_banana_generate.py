#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

GENERATE_URL = "https://nanophoto.ai/api/nano-banana-pro/generate"
STATUS_URL = "https://nanophoto.ai/api/nano-banana-pro/check-status"
VALID_MODES = {"generate", "edit"}
VALID_ASPECT_RATIOS = {"16:9", "9:16", "4:3", "3:4"}
VALID_QUALITIES = {"1K", "2K", "4K"}
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def post_json(url: str, api_key: str, payload: dict, timeout: int, user_agent: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
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
            text = response.read().decode("utf-8", "replace")
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", "replace")
        fail(f"HTTP {exc.code}: {error_body}")
    except urllib.error.URLError as exc:
        fail(f"Request failed: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON response: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit a Nano Banana Pro generation/edit task and poll until completion.")
    parser.add_argument("--prompt", help="Generation/edit prompt")
    parser.add_argument("--mode", default="generate", choices=sorted(VALID_MODES), help="Mode")
    parser.add_argument("--aspect-ratio", default="16:9", choices=sorted(VALID_ASPECT_RATIOS), help="Aspect ratio")
    parser.add_argument("--image-quality", default="1K", choices=sorted(VALID_QUALITIES), help="Output quality")
    parser.add_argument("--input-image-url", action="append", default=[], help="Public image URL for edit mode; may be passed multiple times")
    parser.add_argument("--api-key", help="NanoPhoto API key; defaults to NANOPHOTO_API_KEY env var")
    parser.add_argument("--generation-id", help="Skip submission and poll an existing generationId")
    parser.add_argument("--json-only", action="store_true", help="Print only raw JSON responses without wrapper stage objects")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds (default: 5)")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds (default: 60)")
    parser.add_argument("--max-wait", type=int, default=600, help="Maximum total wait time in seconds (default: 600)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("NANOPHOTO_API_KEY")
    if not api_key:
        fail("Missing API key. Set NANOPHOTO_API_KEY or pass --api-key.")

    if args.generation_id:
        generation_id = args.generation_id
    else:
        if not args.prompt:
            fail("--prompt is required unless --generation-id is provided.")
        payload = {
            "prompt": args.prompt,
            "mode": args.mode,
            "aspectRatio": args.aspect_ratio,
            "imageQuality": args.image_quality,
        }

        if args.mode == "edit":
            if not args.input_image_url:
                fail("edit mode requires at least one --input-image-url (public URL).")
            if len(args.input_image_url) > 8:
                fail("edit mode accepts at most 8 --input-image-url values.")
            payload["inputImageUrls"] = args.input_image_url

        submit = post_json(GENERATE_URL, api_key, payload, args.timeout, args.user_agent)
        if args.json_only:
            print(json.dumps(submit, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"stage": "submitted", "response": submit}, ensure_ascii=False, indent=2))

        generation_id = submit.get("generationId")
        status = submit.get("status")

        if status == "completed":
            return
        if not generation_id:
            fail("No generationId returned from generate endpoint.")

    started = time.time()
    while True:
        if time.time() - started > args.max_wait:
            fail(f"Timed out waiting for completion after {args.max_wait} seconds.")
        time.sleep(args.poll_interval)
        status_resp = post_json(STATUS_URL, api_key, {"generationId": generation_id}, args.timeout, args.user_agent)
        if args.json_only:
            print(json.dumps(status_resp, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"stage": "status", "response": status_resp}, ensure_ascii=False, indent=2))
        current = status_resp.get("status")
        if current == "completed":
            return
        if current == "failed" or status_resp.get("success") is False:
            fail("Generation failed; see status response above.")


if __name__ == "__main__":
    main()
