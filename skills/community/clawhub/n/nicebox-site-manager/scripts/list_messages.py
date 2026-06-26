#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error


DEFAULT_BASE_URL = "https://ai.nicebox.cn/api/openclaw"
ENDPOINT_LIST_MESSAGES = "/message/getlist"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def build_url(base_url: str, endpoint: str, params: dict = None) -> str:
    url = base_url.rstrip("/") + endpoint
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    return url


def http_get(url: str, api_key: str, timeout: int = 30):
    req = urllib.request.Request(
        url=url,
        method="GET",
        headers={
            "Authorization": api_key,
            "Accept": "application/json",
            "User-Agent": "nicebox-openclaw-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.getcode(), raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return e.code, raw
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}") from e


def parse_args():
    parser = argparse.ArgumentParser(description="List messages from NiceBox OpenClaw API")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--page-size", type=int, default=20, help="Items per page")
    parser.add_argument("--is-read", choices=["0", "1"], default=None, help="0 unread, 1 read")
    parser.add_argument("--base-url", default=get_env("AIBOX_BASE_URL", DEFAULT_BASE_URL), help="API base URL")
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = get_env("AIBOX_API_KEY")
    if not api_key:
        eprint("Error: AIBOX_API_KEY is not set")
        sys.exit(2)

    params = {
        "page": args.page,
        "page_size": args.page_size,
    }
    if args.is_read is not None:
        params["is_read"] = args.is_read

    url = build_url(args.base_url, ENDPOINT_LIST_MESSAGES, params)

    try:
        status_code, raw = http_get(url, api_key)
    except RuntimeError as e:
        eprint(str(e))
        sys.exit(1)

    try:
        parsed = json.loads(raw)
        print(json.dumps({
            "ok": 200 <= status_code < 300,
            "status_code": status_code,
            "request_url": url,
            "response": parsed,
        }, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({
            "ok": 200 <= status_code < 300,
            "status_code": status_code,
            "request_url": url,
            "response_raw": raw,
        }, ensure_ascii=False, indent=2))

    sys.exit(0 if 200 <= status_code < 300 else 1)


if __name__ == "__main__":
    main()
