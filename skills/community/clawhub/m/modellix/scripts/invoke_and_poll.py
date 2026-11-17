#!/usr/bin/env python3
"""
Submit a Modellix async task using CLI-first with REST fallback.

CLI path uses `modellix-cli model run --wait` (no hand-rolled poll loop).
REST path keeps submit + exponential-backoff poll.

Examples:
  python scripts/invoke_and_poll.py \\
    --model-slug google/nano-banana-2-lite \\
    --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

from cli_runtime import CliRuntime, resolve_cli_runtime

BASE_URL = "https://api.modellix.ai/api/v1"
RETRYABLE_READ_STATUS = {408, 429, 500, 502, 503, 504}
MAX_READ_RETRIES = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke Modellix and wait for result.")
    parser.add_argument(
        "--model-slug",
        required=True,
        help="Model slug in provider/model format, e.g. google/nano-banana-2-lite",
    )
    parser.add_argument("--body", help="Inline JSON request body")
    parser.add_argument("--body-file", help="Path to JSON request body file")
    parser.add_argument("--api-key", help="API key override; defaults to MODELLIX_API_KEY")
    parser.add_argument("--mode", choices=["auto", "cli", "rest"], default="auto")
    parser.add_argument(
        "--timeout",
        default="5m",
        help="CLI wait timeout (e.g. 5m, 300s). Also used to derive REST timeout seconds.",
    )
    parser.add_argument("--initial-wait", type=float, default=1.0)
    parser.add_argument("--max-wait", type=float, default=10.0)
    parser.add_argument(
        "--output-dir",
        help="If set and CLI mode succeeds, run task download into this directory",
    )
    return parser.parse_args()


def load_body(args: argparse.Namespace) -> Dict[str, Any]:
    if bool(args.body) == bool(args.body_file):
        raise ValueError("Provide exactly one of --body or --body-file.")
    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(args.body)


def get_api_key(args: argparse.Namespace) -> Optional[str]:
    """Return API key if present. CLI may still auth via saved profile when unset."""
    key = args.api_key or os.getenv("MODELLIX_API_KEY")
    return key.strip() if key and key.strip() else None


def parse_model_slug(model_slug: str) -> Tuple[str, str]:
    if "/" not in model_slug:
        raise ValueError("Invalid --model-slug. Expected format: <provider>/<model_id>.")
    provider, model_id = model_slug.split("/", 1)
    provider = provider.strip()
    model_id = model_id.strip()
    if not provider or not model_id:
        raise ValueError("Invalid --model-slug. Provider and model_id must be non-empty.")
    return provider, model_id


def timeout_to_seconds(timeout: str) -> int:
    value = timeout.strip().lower()
    if value.endswith("ms"):
        return max(1, int(float(value[:-2]) / 1000) or 1)
    if value.endswith("s") and not value.endswith("ms"):
        return max(1, int(float(value[:-1])))
    if value.endswith("m"):
        return max(1, int(float(value[:-1]) * 60))
    if value.endswith("h"):
        return max(1, int(float(value[:-1]) * 3600))
    return max(1, int(float(value)))


def child_env(api_key: Optional[str]) -> Dict[str, str]:
    """Pass an explicit key through the child environment, never process arguments."""
    env = os.environ.copy()
    if api_key:
        env["MODELLIX_API_KEY"] = api_key
    return env


def run_cli(args: argparse.Namespace, cli_path: str = "modellix-cli") -> Dict[str, Any]:
    cmd = [
        cli_path,
        "model",
        "run",
        "--model-slug",
        args.model_slug,
        "--wait",
        "--timeout",
        args.timeout,
        "--json",
    ]
    if args.body_file:
        cmd.extend(["--body-file", args.body_file])
    else:
        cmd.extend(["--body", args.body])

    # Paid POST must not be auto-retried by this wrapper.
    try:
        proc = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            env=child_env(get_api_key(args)),
            timeout=timeout_to_seconds(args.timeout) + 30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "CLI model run exceeded its local deadline. The paid submission outcome may be "
            "unknown; check `modellix-cli task history` before submitting again."
        ) from exc
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(
            f"CLI model run failed (exit {proc.returncode}): {detail}. "
            "If the paid submission outcome is unknown, check: modellix-cli task history"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"CLI returned non-JSON stdout: {proc.stdout[:500]}") from exc


def run_cli_download(
    task_id: str,
    output_dir: str,
    api_key: Optional[str],
    cli_path: str = "modellix-cli",
) -> Dict[str, Any]:
    cmd = [
        cli_path,
        "task",
        "download",
        task_id,
        "--output-dir",
        output_dir,
        "--json",
    ]
    proc = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        env=child_env(api_key),
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"CLI task download failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return json.loads(proc.stdout)


def http_request(
    url: str, method: str, api_key: str, body: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
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
    try:
        result = http_request(url=url, method="POST", api_key=api_key, body=body)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(
            "REST paid submit hit a transport error and was not retried. Its outcome may be "
            "unknown; inspect task history or the console before another submit."
        ) from exc
    code = int(result.get("code", 500))
    if code == 0:
        return result
    raise RuntimeError(
        "REST submit did not succeed and was not retried because this is a paid POST. "
        f"Inspect task history or the console before another submit: {json.dumps(result, ensure_ascii=False)}"
    )


def run_rest_poll(task_id: str, api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/tasks/{task_id}"
    return http_request(url=url, method="GET", api_key=api_key)


def pick_mode(args: argparse.Namespace, runtime: CliRuntime | None) -> str:
    if args.mode in {"cli", "rest"}:
        return args.mode
    # CLI can authenticate via saved profile even without env key.
    return "cli" if runtime and runtime.available else "rest"


def extract_task_id(payload: Dict[str, Any]) -> Optional[str]:
    data = payload.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    if payload.get("task_id"):
        return str(payload["task_id"])
    # Some CLI JSON envelopes nest differently; best-effort scan.
    for key in ("taskId", "id"):
        if payload.get(key):
            return str(payload[key])
    return None


def normalize_output(
    mode_used: str,
    result_payload: Dict[str, Any],
    download_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data = result_payload.get("data", result_payload)
    if not isinstance(data, dict):
        data = {}
    result = data.get("result", {}) if isinstance(data.get("result"), dict) else {}
    resources = result.get("resources", [])
    out: Dict[str, Any] = {
        "mode_used": mode_used,
        "task_id": data.get("task_id") or result_payload.get("task_id"),
        "status": data.get("status") or result_payload.get("status"),
        "model_id": data.get("model_id") or result_payload.get("model_id"),
        "resources": resources,
        "raw": result_payload,
    }
    if download_payload is not None:
        out["download"] = download_payload
    return out


def main() -> int:
    args = parse_args()
    body = load_body(args)
    api_key = get_api_key(args)
    # Resolve/update the CLI before any paid submission, then pin this workflow
    # to the resolved executable path.
    runtime = resolve_cli_runtime() if args.mode != "rest" else None
    mode = pick_mode(args, runtime)

    if mode == "cli" and (runtime is None or not runtime.available):
        warning = f" {runtime.update_warning}" if runtime and runtime.update_warning else ""
        raise RuntimeError(f"modellix-cli is unavailable after preflight.{warning}")

    if mode == "rest" and not api_key:
        raise RuntimeError("Missing API key. Set MODELLIX_API_KEY or pass --api-key.")

    download_payload: Optional[Dict[str, Any]] = None

    if mode == "cli":
        cli_path = runtime.path if runtime and runtime.path else "modellix-cli"
        result_payload = run_cli(args, cli_path)
        task_id = extract_task_id(result_payload)
        if args.output_dir and task_id:
            download_payload = run_cli_download(task_id, args.output_dir, api_key, cli_path)
        normalized = normalize_output(mode, result_payload, download_payload)
        if runtime:
            normalized["cli_runtime"] = runtime.to_dict()
        print(
            json.dumps(
                normalized,
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    # REST fallback: submit once; only subsequent task-status reads may retry.
    submit_payload = run_rest_submit(args, body, api_key or "")
    task_id = extract_task_id(submit_payload)
    if not task_id:
        raise RuntimeError(
            f"Missing task_id in response: {json.dumps(submit_payload, ensure_ascii=False)}"
        )

    timeout_seconds = timeout_to_seconds(args.timeout)
    started = time.time()
    wait = args.initial_wait
    read_failures = 0
    poll_payload: Dict[str, Any] = {}
    while True:
        if time.time() - started > timeout_seconds:
            raise TimeoutError(
                f"Polling timed out for {task_id}. Remote task may still be running."
            )
        time.sleep(wait)
        try:
            poll_payload = run_rest_poll(task_id, api_key or "")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if read_failures < MAX_READ_RETRIES:
                read_failures += 1
                wait = min(wait * 2, args.max_wait)
                continue
            raise RuntimeError(
                f"REST task read failed after {MAX_READ_RETRIES} retries: {exc}"
            ) from exc
        code = int(poll_payload.get("code", 500))
        if code != 0:
            if code in RETRYABLE_READ_STATUS and read_failures < MAX_READ_RETRIES:
                read_failures += 1
                wait = min(wait * 2, args.max_wait)
                continue
            raise RuntimeError(
                f"REST task read failed: {json.dumps(poll_payload, ensure_ascii=False)}"
            )
        read_failures = 0
        status = str(poll_payload.get("data", {}).get("status", "")).lower()
        if status in {"success", "failed"}:
            break
        wait = min(wait * 2, args.max_wait)

    print(
        json.dumps(
            normalize_output(
                mode,
                {
                    "data": {
                        **(poll_payload.get("data") or {}),
                        "task_id": task_id,
                        "model_id": (submit_payload.get("data") or {}).get("model_id"),
                    },
                    "submit": submit_payload,
                    "poll": poll_payload,
                },
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - simple script error surface
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
