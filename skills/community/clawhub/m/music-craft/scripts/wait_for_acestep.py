#!/usr/bin/env python3
"""Wait for local ACE-Step tasks while tolerating API quirks.

The helper reconciles `/query_result` status responses with cache-file checks.
It does not kill jobs; it reports timeout with the best known state.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


AUDIO_SUFFIXES = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}


def classify_query_result(payload: dict) -> dict[str, object]:
    data = payload.get("data")
    if not data:
        return {"state": "pending", "reason": "empty query_result data"}
    first = data[0]
    if not isinstance(first, dict):
        return {"state": "unknown", "reason": "unexpected query_result item"}
    status = first.get("status")
    if status in {2, "succeeded", "done", "success"}:
        return {"state": "succeeded", "item": first}
    if status in {1, "processing", "running"}:
        return {"state": "processing", "item": first}
    if status in {0, "queued", "pending"}:
        return {"state": "pending", "item": first}
    if status in {-1, 3, "failed", "error"}:
        return {"state": "failed", "item": first}
    return {"state": "unknown", "item": first}


def newest_audio_files(cache_dir: Path, limit: int = 5) -> list[Path]:
    if not cache_dir.exists():
        return []
    files = [
        path
        for path in cache_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in AUDIO_SUFFIXES and path.stat().st_size > 0
    ]
    return sorted(files, key=lambda path: path.stat().st_mtime_ns, reverse=True)[:limit]


def _query_result(api_url: str, task_id: str, timeout: float) -> dict:
    body = json.dumps({"task_ids": [task_id]}).encode("utf-8")
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}/query_result",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - local operator URL
        return json.loads(response.read().decode("utf-8"))


def wait_for_task(
    task_id: str,
    api_url: str,
    cache_dir: Path,
    poll_seconds: float,
    timeout_seconds: float,
    request_timeout: float,
) -> dict[str, object]:
    start = time.monotonic()
    before = {str(path) for path in newest_audio_files(cache_dir, limit=50)}
    last_state: dict[str, object] = {"state": "pending", "reason": "not polled yet"}
    while True:
        elapsed = time.monotonic() - start
        new_files = [path for path in newest_audio_files(cache_dir, limit=10) if str(path) not in before]
        if new_files:
            return {"state": "succeeded", "elapsed_seconds": round(elapsed, 1), "files": [str(path) for path in new_files]}
        if elapsed >= timeout_seconds:
            return {"state": "timeout", "elapsed_seconds": round(elapsed, 1), "last_query_state": last_state}
        try:
            payload = _query_result(api_url, task_id, request_timeout)
            last_state = classify_query_result(payload)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_state = {"state": "poll_error", "error": str(exc)}
        if last_state.get("state") == "failed":
            return {"state": "failed", "elapsed_seconds": round(elapsed, 1), "last_query_state": last_state}
        if last_state.get("state") == "succeeded":
            return {"state": "succeeded", "elapsed_seconds": round(elapsed, 1), "last_query_state": last_state}
        time.sleep(poll_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wait for a local ACE-Step task")
    parser.add_argument("task_id")
    parser.add_argument("--api-url", default="http://127.0.0.1:8001")
    parser.add_argument("--cache-dir", type=Path, default=Path.home() / "ACE-Step-1.5/.cache/acestep/tmp/api_audio")
    parser.add_argument("--poll-seconds", type=float, default=10.0)
    parser.add_argument("--timeout-seconds", type=float, default=3600.0)
    parser.add_argument("--request-timeout", type=float, default=60.0)
    args = parser.parse_args(argv)

    result = wait_for_task(
        args.task_id,
        args.api_url,
        args.cache_dir.expanduser(),
        args.poll_seconds,
        args.timeout_seconds,
        args.request_timeout,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["state"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
