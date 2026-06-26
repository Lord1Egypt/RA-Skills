#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import sys
import time
import uuid
from typing import Any

import requests

from .config import get_token

DEFAULT_TIMEOUT = 300
DEFAULT_POLL_INTERVAL = 5
ENDPOINT = os.getenv("HIDREAM_ENDPOINT") or os.getenv("OPENCLAW_ENDPOINT", "https://vivago.ai")


def parse_images(value: str | None) -> list[str]:
    images = []
    if not value:
        return images
    for image in value.split(","):
        image = image.strip()
        if not image:
            continue
        if os.path.exists(image):
            # Security Note: Reading local file for base64 encoding
            try:
                with open(image, "rb") as f:
                    image_bytes = f.read()
                    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                    images.append(image_base64)
            except Exception as e:
                 raise ValueError(f"Failed to read image file '{image}': {e}")
        else:
            # Assume it's a URL or base64 string
            images.append(image)
    return images


def parse_common_args(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--authorization", help="Bearer token value only.")
    parser.add_argument("--request-id", default=f"{uuid.uuid4()}", help="Optional request id.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    return parser


def _headers(authorization: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {authorization}",
        "Content-Type": "application/json",
    }


def submit_task_and_poll_result(
    payload: dict[str, Any], path: str, authorization, poll_timeout: int
) -> dict[str, Any]:
    authorization = authorization or get_token()
    if not authorization:
        raise ValueError(
            "Missing authorization. Run 'scripts/configure.py' or set HIDREAM_AUTHORIZATION."
        )
    endpoint = f"{ENDPOINT}{path}"
    headers = _headers(authorization)
    # print(payload)
    submit_resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    if submit_resp.status_code != 200:
        raise RuntimeError(f"http error: {submit_resp.status_code} {submit_resp.text}")
    resp_json = submit_resp.json()

    if resp_json.get("code") != 0:
        raise RuntimeError(
            f"submit failed: {json.dumps(resp_json, ensure_ascii=False)}"
        )

    task_id = resp_json.get("result", {}).get("task_id")
    if not task_id:
        return resp_json

    result_url = endpoint + "/results"
    start = time.time()
    while True:
        query_resp = requests.get(
            result_url,
            params={"task_id": task_id},
            headers=headers,
            timeout=30,
        )
        # print("poll task result ...", file=sys.stderr)
        if query_resp.status_code != 200 and query_resp.json()["code"] != 0:
            raise RuntimeError(
                f"http error: {query_resp.status_code} {query_resp.text}"
            )
        result_json = query_resp.json()
        sub_task_result = result_json.get("result").get("sub_task_results")
        is_completed = True

        for sub_task in sub_task_result:
            if sub_task["task_status"] not in [1, 3, 4]:
                is_completed = False
                break
        if is_completed is False:
            if time.time() - start >= poll_timeout:
                raise TimeoutError(
                    f"task timeout after {poll_timeout}s, task_id={task_id}"
                )
            time.sleep(DEFAULT_POLL_INTERVAL)
        else:
            return result_json


def main(payload: dict[str, Any], path, args: argparse.Namespace) -> int:
    try:
        result = submit_task_and_poll_result(payload, path, args)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
