#!/usr/bin/env python3
"""Wait for local ACE-Step tasks while tolerating API quirks.

The helper reconciles `/query_result` status responses with cache-file checks.
It does not kill jobs; it reports timeout with the best known state.

With `--expected-seconds`, a cache file only counts once its measured duration
(via `ffprobe`, when installed) is within `--tolerance` of the request. This
rejects in-progress intermediates that the server can surface early on long
jobs. `--scan-only` skips polling and reports the newest matching take already
in the cache, for recovering a generation whose client hung or died.

The helper only talks to a loopback ACE-Step server (no proxies, no redirects)
and never deletes files.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


AUDIO_SUFFIXES = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def is_loopback_url(api_url: str) -> bool:
    parsed = urllib.parse.urlparse(api_url)
    return parsed.scheme in {"http", "https"} and (parsed.hostname or "") in LOOPBACK_HOSTS


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Refuse every HTTP redirect so a reply can never send us off the loopback host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401, ANN001
        raise urllib.error.HTTPError(newurl, code, f"redirect refused (loopback-only client): {newurl}", headers, fp)


def loopback_opener() -> urllib.request.OpenerDirector:
    """Opener that ignores proxy settings and refuses redirects."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), _RejectRedirects())


def probe_duration_seconds(path: Path) -> float | None:
    """Measured duration via ffprobe, or None when ffprobe is missing or fails."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None or not path.is_file():
        return None
    try:
        completed = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            shell=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    try:
        return float(completed.stdout.strip())
    except ValueError:
        return None


def check_duration(path: Path, expected: float | None, tolerance: float) -> dict[str, object]:
    """Classify one take: accepted, rejected (wrong length) or unverified."""
    if expected is None:
        return {"file": str(path), "verdict": "accepted", "reason": "no expected duration given"}
    measured = probe_duration_seconds(path)
    if measured is None:
        return {"file": str(path), "verdict": "unverified", "reason": "ffprobe unavailable or failed"}
    verdict = "accepted" if abs(measured - expected) <= tolerance else "rejected"
    return {"file": str(path), "verdict": verdict, "measured_seconds": round(measured, 3), "expected_seconds": expected}


def scan_cache(cache_dir: Path, expected: float | None, tolerance: float, limit: int = 10) -> dict[str, object]:
    """Report the newest take in the cache that matches the expected duration."""
    checks = [check_duration(path, expected, tolerance) for path in newest_audio_files(cache_dir, limit=limit)]
    accepted = [check for check in checks if check["verdict"] == "accepted"]
    if accepted:
        return {"state": "found", "selected": accepted[0], "checked": checks}
    return {"state": "not_found", "checked": checks}


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
    if not is_loopback_url(request.full_url):
        raise ValueError(f"refusing non-loopback request URL: {request.full_url}")
    with loopback_opener().open(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_task(
    task_id: str,
    api_url: str,
    cache_dir: Path,
    poll_seconds: float,
    timeout_seconds: float,
    request_timeout: float,
    expected_seconds: float | None = None,
    tolerance: float = 2.0,
) -> dict[str, object]:
    start = time.monotonic()
    before = {str(path) for path in newest_audio_files(cache_dir, limit=50)}
    last_state: dict[str, object] = {"state": "pending", "reason": "not polled yet"}
    rejected: dict[str, dict[str, object]] = {}
    while True:
        elapsed = time.monotonic() - start
        new_files = [path for path in newest_audio_files(cache_dir, limit=10) if str(path) not in before]
        checks = [check_duration(path, expected_seconds, tolerance) for path in new_files]
        for check in checks:
            if check["verdict"] == "rejected":
                rejected[str(check["file"])] = check
        usable = [check for check in checks if check["verdict"] != "rejected"]
        if usable:
            state = "succeeded" if all(check["verdict"] == "accepted" for check in usable) else "succeeded_unverified"
            return {
                "state": state,
                "elapsed_seconds": round(elapsed, 1),
                "files": [str(check["file"]) for check in usable],
                "checks": usable,
                "rejected": list(rejected.values()),
            }
        if elapsed >= timeout_seconds:
            return {
                "state": "timeout",
                "elapsed_seconds": round(elapsed, 1),
                "last_query_state": last_state,
                "rejected": list(rejected.values()),
            }
        try:
            payload = _query_result(api_url, task_id, request_timeout)
            last_state = classify_query_result(payload)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_state = {"state": "poll_error", "error": str(exc)}
        if last_state.get("state") == "failed":
            return {"state": "failed", "elapsed_seconds": round(elapsed, 1), "last_query_state": last_state}
        if last_state.get("state") == "succeeded" and expected_seconds is None:
            return {"state": "succeeded", "elapsed_seconds": round(elapsed, 1), "last_query_state": last_state}
        time.sleep(poll_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wait for a local ACE-Step task")
    parser.add_argument("task_id", nargs="?", help="ACE-Step task id (not needed with --scan-only)")
    parser.add_argument("--api-url", default="http://127.0.0.1:8001", help="loopback ACE-Step server URL")
    parser.add_argument("--cache-dir", type=Path, default=Path.home() / "ACE-Step-1.5/.cache/acestep/tmp/api_audio")
    parser.add_argument("--poll-seconds", type=float, default=10.0)
    parser.add_argument("--timeout-seconds", type=float, default=3600.0)
    parser.add_argument("--request-timeout", type=float, default=60.0)
    parser.add_argument("--expected-seconds", type=float, help="requested audio_duration; rejects takes of another length")
    parser.add_argument("--tolerance", type=float, default=2.0, help="allowed duration difference in seconds (default 2)")
    parser.add_argument("--scan-only", action="store_true", help="do not poll; report the newest matching take in the cache")
    args = parser.parse_args(argv)
    cache_dir = args.cache_dir.expanduser()

    if args.tolerance < 0:
        parser.error("--tolerance must be >= 0")
    if args.scan_only:
        result = scan_cache(cache_dir, args.expected_seconds, args.tolerance)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["state"] == "found" else 1
    if not args.task_id:
        parser.error("task_id is required unless --scan-only is given")
    if not is_loopback_url(args.api_url):
        parser.error("--api-url must point at a local ACE-Step server (127.0.0.1, localhost or ::1)")

    result = wait_for_task(
        args.task_id,
        args.api_url,
        cache_dir,
        args.poll_seconds,
        args.timeout_seconds,
        args.request_timeout,
        expected_seconds=args.expected_seconds,
        tolerance=args.tolerance,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["state"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
