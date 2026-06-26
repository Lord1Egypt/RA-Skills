#!/usr/bin/env python3
"""Call Hidream txt2img async API with explicit auth and parameters."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from typing import Any
import requests


DEFAULT_ENDPOINT = "https://www.hidreamai.com"
ALLOWED_RESOLUTIONS = (
    "1024*1024",
    "832*1248",
    "880*1168",
    "768*1360",
    "1248*832",
    "1168*880",
    "1360*768",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send async txt2img request to Hidream API."
    )
    parser.add_argument("--authorization", help="Bearer token value only.")
    parser.add_argument("--prompt", required=True, help="Image prompt text.")
    parser.add_argument(
        "--resolution",
        default="1024*1024",
        choices=ALLOWED_RESOLUTIONS,
        help="Image resolution.",
    )
    parser.add_argument("--img-count", type=int, default=1, help="Image count.")
    parser.add_argument("--version", default="v2L", help="Model version.")
    parser.add_argument("--request-id", default="", help="Optional request id.")
    parser.add_argument("--poll-interval", type=int, default=5, help="Poll seconds.")
    parser.add_argument("--timeout", type=int, default=300, help="Max wait seconds.")

    return parser.parse_args()


def _build_payload(args: argparse.Namespace) -> dict[str, Any]:
    request_id = args.request_id or str(uuid.uuid4())
    return {
        "prompt": args.prompt,
        "img_count": args.img_count,
        "version": args.version,
        "resolution": args.resolution,
        "request_id": request_id,
    }


def _parse_sub_tasks(result_json: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    done = True
    images: list[str] = []
    errors: list[str] = []
    for sub_task in result_json["result"]["sub_task_results"]:
        task_status = sub_task.get("task_status")
        if task_status == 1:
            image = sub_task.get("image")
            if image:
                images.append(image)
        elif task_status in (3, 4):
            errors.append(f"生成失败: {sub_task.get('sub_task_id')}")
        else:
            done = False
    return done, images, errors


def generate_and_wait(args: argparse.Namespace) -> dict[str, Any]:
    authorization = args.authorization or os.getenv("HIDREAM_AUTHORIZATION", "")
    if not authorization:
        raise ValueError(
            "Missing authorization. Pass --authorization or set HIDREAM_AUTHORIZATION."
        )

    payload = _build_payload(args)
    payload = {
        "prompt": payload["prompt"],
        "img_count": payload["img_count"],
        "version": payload["version"],
        "resolution": payload["resolution"],
        "request_id": payload["request_id"],
    }
    headers = {
        "Authorization": f"Bearer {authorization}",
        "Content-Type": "application/json",
    }

    gen_task_url = f"{DEFAULT_ENDPOINT}/api-pub/gw/v3/image/txt2img/async"
    get_task_result_url = gen_task_url + "/results"

    submit_resp = requests.post(gen_task_url, json=payload, headers=headers, timeout=30)
    if submit_resp.status_code != 200:
        raise RuntimeError(f"http error: {submit_resp.status_code} {submit_resp.text}")
    resp_json = submit_resp.json()
    if resp_json.get("code") != 0:
        raise RuntimeError(f"submit failed: {json.dumps(resp_json, ensure_ascii=False)}")
    task_id = resp_json["result"]["task_id"]
    print(f"Send Task Success: {task_id}")
    start = time.time()
    while True:
        print(f"Query Task result ...")
        query_resp = requests.get(
            get_task_result_url,
            params={"task_id": task_id},
            headers=headers,
            timeout=30,
        )
        if query_resp.status_code != 200:
            raise RuntimeError(f"http error: {query_resp.status_code} {query_resp.text}")
        result_resp_json = query_resp.json()
        if result_resp_json.get("code") != 0:
            raise RuntimeError(
                f"query failed: {json.dumps(result_resp_json, ensure_ascii=False)}"
            )
        done, images, errors = _parse_sub_tasks(result_resp_json)
        if done:
            return {
                "task_id": task_id,
                "request_id": payload["request_id"],
                "images": images,
                "errors": errors,
                # "raw_result": result_resp_json,
            }
        if time.time() - start >= args.timeout:
            raise TimeoutError(f"task timeout after {args.timeout}s, task_id={task_id}")
        time.sleep(args.poll_interval)


def main() -> int:
    args = parse_args()
    try:
        result = generate_and_wait(args)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
