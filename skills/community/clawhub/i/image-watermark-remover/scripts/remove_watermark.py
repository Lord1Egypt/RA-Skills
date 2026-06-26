#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

SUBMIT_PATH = "/api/image/remove-watermark"
STATUS_PATH = "/api/jobs/query"
DEFAULT_BASE_URL = "https://nowatermark.info"
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
            "Origin": DEFAULT_BASE_URL,
            "Referer": f"{DEFAULT_BASE_URL}/",
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
    parser = argparse.ArgumentParser(description="Submit an image watermark-removal task and poll until completion.")
    parser.add_argument("--file-url", help="Public image URL")
    parser.add_argument("--api-key", help="Nowatermark API key; defaults to NOWATERMARK_API_KEY env var")
    parser.add_argument("--request-id", help="Skip submission and poll an existing request_id")
    parser.add_argument("--json-only", action="store_true", help="Print only raw JSON responses without wrapper stage objects")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds (default: 5)")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds (default: 60)")
    parser.add_argument("--max-wait", type=int, default=600, help="Maximum total wait time in seconds (default: 600)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("NOWATERMARK_API_KEY")
    if not api_key:
        fail("Missing API key. Set NOWATERMARK_API_KEY or pass --api-key.")

    submit_url = args.base_url.rstrip("/") + SUBMIT_PATH
    status_url = args.base_url.rstrip("/") + STATUS_PATH

    if args.request_id:
        request_id = args.request_id
    else:
        if not args.file_url:
            fail("--file-url is required unless --request-id is provided.")
        submit = post_json(
            submit_url,
            api_key,
            {"file_url": args.file_url},
            args.timeout,
            args.user_agent,
        )
        if args.json_only:
            print(json.dumps(submit, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"stage": "submitted", "response": submit}, ensure_ascii=False, indent=2))

        request_id = submit.get("request_id")
        status = submit.get("status")

        if status == "completed":
            return
        if not request_id:
            fail("No request_id returned from submit endpoint.")

    started = time.time()
    while True:
        if time.time() - started > args.max_wait:
            fail(f"Timed out waiting for completion after {args.max_wait} seconds.")
        time.sleep(args.poll_interval)
        status_resp = post_json(
            status_url,
            api_key,
            {"request_id": request_id},
            args.timeout,
            args.user_agent,
        )
        if args.json_only:
            print(json.dumps(status_resp, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"stage": "status", "response": status_resp}, ensure_ascii=False, indent=2))
        current = status_resp.get("status")
        if current == "completed":
            return
        if current == "failed" or status_resp.get("success") is False:
            fail("Task failed; see status response above.")


if __name__ == "__main__":
    main()
