#!/usr/bin/env python3
"""
Submit and poll a Modellix async task using CLI-first with REST fallback.

Examples:
  python scripts/invoke_and_poll.py \
    --model-slug bytedance/seedream-5.0-lite \
    --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

BASE_URL = "https://api.modellix.ai/api/v1"
RETRYABLE_STATUS = {429, 500, 503}
MAX_RETRIES = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke Modellix and poll result.")
    parser.add_argument(
        "--model-slug",
        required=True,
        help="Model slug in provider/model format, e.g. bytedance/seedream-5.0-lite",
    )
    parser.add_argument("--body", help="Inline JSON request body")
    parser.add_argument("--body-file", help="Path to JSON request body file")
    parser.add_argument("--api-key", help="API key override; defaults to MODELLIX_API_KEY")
    parser.add_argument("--mode", choices=["auto", "cli", "rest"], default="auto")
    parser.add_argument("--initial-wait", type=float, default=1.0)
    parser.add_argument("--max-wait", type=float, default=10.0)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    return parser.parse_args()


def load_body(args: argparse.Namespace) -> Dict[str, Any]:
    if bool(args.body) == bool(args.body_file):
        raise ValueError("Provide exactly one of --body or --body-file.")
    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(args.body)


def get_api_key(args: argparse.Namespace) -> str:
    key = args.api_key or os.getenv("MODELLIX_API_KEY")
    if not key:
        raise RuntimeError("Missing API key. Set MODELLIX_API_KEY or pass --api-key.")
    return key


def parse_model_slug(model_slug: str) -> Tuple[str, str]:
    if "/" not in model_slug:
        raise ValueError("Invalid --model-slug. Expected format: <provider>/<model_id>.")
    provider, model_id = model_slug.split("/", 1)
    provider = provider.strip()
    model_id = model_id.strip()
    if not provider or not model_id:
        raise ValueError("Invalid --model-slug. Provider and model_id must be non-empty.")
    return provider, model_id


def run_cli(args: argparse.Namespace) -> Dict[str, Any]:
    cmd = [
        "modellix-cli",
        "model",
        "invoke",
        "--model-slug",
        args.model_slug,
    ]
    if args.body_file:
        cmd.extend(["--body-file", args.body_file])
    else:
        cmd.extend(["--body", args.body])

    if args.api_key:
        cmd.extend(["--api-key", args.api_key])

    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"CLI invoke failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout)


def http_request(url: str, method: str, api_key: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data: Optional[bytes] = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url=url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
            return json.loads(text) if text else {}
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8")
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            parsed = {"code": exc.code, "message": payload}
        parsed.setdefault("code", exc.code)
        return parsed


def run_rest_submit(args: argparse.Namespace, body: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    provider, model_id = parse_model_slug(args.model_slug)
    url = f"{BASE_URL}/{provider}/{model_id}/async"
    attempts = 0
    wait = args.initial_wait
    while True:
        result = http_request(url=url, method="POST", api_key=api_key, body=body)
        code = int(result.get("code", 500))
        if code == 0:
            return result
        if code not in RETRYABLE_STATUS or attempts >= MAX_RETRIES:
            raise RuntimeError(f"REST invoke failed: {json.dumps(result, ensure_ascii=False)}")
        attempts += 1
        time.sleep(wait)
        wait = min(wait * 2, args.max_wait)


def run_rest_poll(task_id: str, api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/tasks/{task_id}"
    return http_request(url=url, method="GET", api_key=api_key)


def pick_mode(args: argparse.Namespace, api_key: str) -> str:
    if args.mode in {"cli", "rest"}:
        return args.mode
    has_cli = shutil.which("modellix-cli") is not None
    return "cli" if has_cli and api_key else "rest"


def extract_task_id(payload: Dict[str, Any]) -> str:
    data = payload.get("data", {})
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError(f"Missing task_id in response: {json.dumps(payload, ensure_ascii=False)}")
    return str(task_id)


def normalize_output(mode_used: str, submit_payload: Dict[str, Any], poll_payload: Dict[str, Any]) -> Dict[str, Any]:
    data = poll_payload.get("data", {})
    result = data.get("result", {})
    resources = result.get("resources", [])
    return {
        "mode_used": mode_used,
        "task_id": data.get("task_id") or submit_payload.get("data", {}).get("task_id"),
        "status": data.get("status"),
        "model_id": data.get("model_id") or submit_payload.get("data", {}).get("model_id"),
        "resources": resources,
        "raw": {
            "submit": submit_payload,
            "poll": poll_payload,
        },
    }


def main() -> int:
    args = parse_args()
    body = load_body(args)
    api_key = get_api_key(args)
    mode = pick_mode(args, api_key)

    submit_payload: Dict[str, Any]
    if mode == "cli":
        submit_payload = run_cli(args)
    else:
        submit_payload = run_rest_submit(args, body, api_key)

    task_id = extract_task_id(submit_payload)

    started = time.time()
    wait = args.initial_wait
    poll_payload: Dict[str, Any] = {}
    while True:
        if time.time() - started > args.timeout_seconds:
            raise TimeoutError("Polling timed out before task reached success/failed.")
        time.sleep(wait)
        if mode == "cli":
            poll_cmd = ["modellix-cli", "task", "get", task_id]
            if args.api_key:
                poll_cmd.extend(["--api-key", args.api_key])
            proc = subprocess.run(poll_cmd, check=False, capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(f"CLI poll failed: {proc.stderr.strip() or proc.stdout.strip()}")
            poll_payload = json.loads(proc.stdout)
        else:
            poll_payload = run_rest_poll(task_id, api_key)

        status = str(poll_payload.get("data", {}).get("status", "")).lower()
        if status in {"success", "failed"}:
            break
        wait = min(wait * 2, args.max_wait)

    print(json.dumps(normalize_output(mode, submit_payload, poll_payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - simple script error surface
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
