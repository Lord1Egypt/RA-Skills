#!/usr/bin/env python3
"""
Submit a Modellix async task using CLI-first with REST fallback.

CLI path uses `modellix-cli model run --wait` (no hand-rolled poll loop).
REST submits once and uses bounded server-side wait; only transient read failures back off.

Examples:
  python scripts/invoke_and_poll.py \\
    --model-slug <provider/model> \\
    --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

from cli_runtime import CliRuntime, resolve_cli_runtime
from http_deadline import DeadlineHTTPHandler, DeadlineHTTPSHandler, HttpDeadline

BASE_URL = "https://api.modellix.ai/api/v1"
RETRYABLE_READ_STATUS = {408, 429, 500, 502, 503, 504}
MAX_READ_RETRIES = 3


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Authenticated REST calls must never forward a Key to a redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke Modellix and wait for result.")
    parser.add_argument(
        "--model-slug",
        required=True,
        help="Model slug in provider/model format, supplied by the user",
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
    parser.add_argument("--initial-wait", type=float, default=1.0, help="Deprecated compatibility option; server-side wait does not use local polling intervals.")
    parser.add_argument("--max-wait", type=float, default=10.0, help="Deprecated compatibility option; server-side wait does not use local polling intervals.")
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
    url: str, method: str, api_key: str, body: Optional[Dict[str, Any]] = None,
    timeout_seconds: float = 30,
) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data: Optional[bytes] = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url=url, method=method, headers=headers, data=data)
    with HttpDeadline(timeout_seconds) as deadline:
        opener = urllib.request.build_opener(DeadlineHTTPHandler(deadline), DeadlineHTTPSHandler(deadline), NoRedirectHandler())
        try:
            with opener.open(req, timeout=deadline.remaining()) as resp:
                raw = resp.read(16 * 1024 * 1024 + 1)
                deadline.remaining()
                if len(raw) > 16 * 1024 * 1024:
                    raise ValueError("REST response exceeds the 16 MiB limit.")
                text = raw.decode("utf-8")
                return json.loads(text) if text else {}
        except urllib.error.HTTPError as exc:
            # Do not consume unbounded error bodies or echo credentials/request data.
            exc.close()
            return {"code": exc.code}


def run_rest_submit(args: argparse.Namespace, body: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    provider, model_id = parse_model_slug(args.model_slug)
    url = f"{BASE_URL}/{provider}/{model_id}/async"
    unknown = (
        "REST paid submission outcome is unknown; it was not retried. "
        "Inspect task history or the console before another submit."
    )
    try:
        result = http_request(url=url, method="POST", api_key=api_key, body=body)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        raise RuntimeError(unknown) from exc
    if not isinstance(result, dict) or type(result.get("code")) is not int:
        raise RuntimeError(unknown)
    code = result["code"]
    if code == 0:
        data = result.get("data")
        task_id = data.get("task_id") if isinstance(data, dict) else None
        if not isinstance(task_id, str) or re.fullmatch(r"[A-Za-z0-9._~:+@=-]{1,512}", task_id) is None:
            raise RuntimeError(unknown)
        return result
    if code in {400, 401, 402, 403, 404, 405, 413, 415, 422, 429}:
        raise RuntimeError(f"REST submit was rejected (code {code}) and was not retried. Check the model schema and account status before another submit.")
    raise RuntimeError(unknown)


def run_rest_poll(task_id: str, api_key: str, remaining_seconds: float = 50) -> Dict[str, Any]:
    from urllib.parse import quote
    if not task_id or any(ord(char) < 32 for char in task_id):
        raise ValueError("A valid task ID is required.")
    seconds = min(45, max(1, int(remaining_seconds - 1)))
    url = f"{BASE_URL}/tasks/{quote(task_id, safe='')}?wait=true&timeout={seconds}"
    return http_request(url=url, method="GET", api_key=api_key,
                        timeout_seconds=min(remaining_seconds, seconds + 5))


def wait_rest_task(task_id: str, api_key: str, timeout_seconds: float) -> Dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    read_failures = 0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Wait timed out for {task_id}. The remote task may still be running; resume using this ID, never resubmit.")
        try:
            payload = run_rest_poll(task_id, api_key, remaining_seconds=remaining)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if read_failures < MAX_READ_RETRIES and time.monotonic() < deadline:
                read_failures += 1
                time.sleep(min(2 ** (read_failures - 1), max(0, deadline - time.monotonic())))
                continue
            raise RuntimeError(f"REST task read failed for {task_id}; keep the ID and retry waiting.") from exc
        code = int(payload.get("code", 500))
        if code != 0:
            if code in RETRYABLE_READ_STATUS and read_failures < MAX_READ_RETRIES:
                read_failures += 1
                time.sleep(min(2 ** (read_failures - 1), max(0, deadline - time.monotonic())))
                continue
            raise RuntimeError(f"REST task read rejected for {task_id} (code {code}); no new submission was made.")
        read_failures = 0
        data = payload.get("data") or {}
        if data.get("task_id") != task_id:
            raise RuntimeError("REST task response has no matching task_id.")
        status = str(data.get("status", "")).lower()
        if status in {"success", "failed", "canceled", "cancelled", "error", "completed", "succeeded"}:
            return payload
        wait = data.get("wait")
        if not isinstance(wait, dict) or not isinstance(wait.get("timed_out"), bool):
            raise RuntimeError(f"The API does not support server-side wait for {task_id}. Keep the task ID and use an immediate task query; do not resubmit.")


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
    poll_payload = wait_rest_task(task_id, api_key or "", timeout_seconds)

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
