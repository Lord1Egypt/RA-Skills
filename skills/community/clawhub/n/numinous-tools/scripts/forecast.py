#!/usr/bin/env python3
"""Submit a Numinous forecast and poll to completion.

Usage:
  python forecast.py "Will BTC exceed $150k before end of 2026?"
  python forecast.py --title "..." --description "..." --cutoff 2026-12-31T23:59:59Z --topics crypto,finance
  python forecast.py "..." --agent-version-id <uuid>

Requires: NUMINOUS_API_KEY in env.
Cost: 0.1 credits per call.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("NUMINOUS_BASE_URL", "https://api.numinouslabs.io")
JOBS_PATH = "/api/v1/forecasters/prediction-jobs"
POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 300
USER_AGENT = "numinous-skill/0.3 (+https://numinouslabs.io)"


def _request(
    method: str, url: str, headers: dict, body: dict | None
) -> tuple[int, dict]:
    data = json.dumps(body).encode() if body is not None else None
    merged = {"User-Agent": USER_AGENT, **headers}
    req = urllib.request.Request(url, data=data, method=method, headers=merged)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode() or "{}")
        except Exception:
            payload = {"detail": exc.reason}
        return exc.code, payload


def _build_payload(args: argparse.Namespace) -> dict:
    payload: dict = {}
    if args.agent_version_id:
        payload["agent_version_id"] = args.agent_version_id

    if args.title or args.description or args.cutoff:
        missing = [
            f for f in ("title", "description", "cutoff") if not getattr(args, f)
        ]
        if missing:
            sys.exit(
                f"Structured mode requires title, description, and cutoff. Missing: {', '.join(missing)}"
            )
        payload["title"] = args.title
        payload["description"] = args.description
        payload["cutoff"] = args.cutoff
        if args.topics:
            payload["topics"] = [t.strip() for t in args.topics.split(",") if t.strip()]
        return payload

    if not args.query:
        sys.exit("Provide either a query string or --title/--description/--cutoff.")
    payload["query"] = args.query
    return payload


def submit(payload: dict, api_key: str) -> str:
    status, body = _request(
        "POST",
        f"{BASE_URL}{JOBS_PATH}",
        {"Content-Type": "application/json", "X-API-Key": api_key},
        payload,
    )
    if status == 401:
        sys.exit(
            "401 Unauthorized — NUMINOUS_API_KEY is missing or invalid. Rotate at https://eversight.numinouslabs.io/api-keys"
        )
    if status == 402:
        sys.exit(
            "402 Payment Required — either set a valid NUMINOUS_API_KEY, or use scripts/forecast_x402.py to pay via crypto."
        )
    if status == 500:
        sys.exit(f"500 — server error submitting job: {body}")
    if status != 202:
        sys.exit(f"Unexpected {status}: {body}")
    return body["prediction_id"]


def poll(prediction_id: str) -> dict:
    url = f"{BASE_URL}{JOBS_PATH}/{prediction_id}"
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    last_status = None
    while time.monotonic() < deadline:
        status, body = _request("GET", url, {}, None)
        if status == 404:
            sys.exit(f"Prediction {prediction_id} not found.")
        if status != 200:
            sys.exit(f"Unexpected {status} while polling: {body}")
        job_status = body.get("status")
        if job_status != last_status:
            print(f"  status: {job_status}", flush=True)
            last_status = job_status
        if job_status == "COMPLETED":
            return body
        if job_status == "FAILED":
            sys.exit(f"Job failed: {body.get('error')}")
        time.sleep(POLL_INTERVAL_SECONDS)
    sys.exit(f"Timed out after {POLL_TIMEOUT_SECONDS}s. Prediction ID: {prediction_id}")


def render(job: dict) -> None:
    result = job["result"]
    prediction = result["prediction"]
    metadata = result.get("metadata") or {}
    print()
    print(f"Prediction: {prediction:.1%}  (raw: {prediction})")
    print(f"Forecaster: {result['forecaster_name']}")
    if metadata.get("miner_uid") is not None:
        print(
            f"Miner:      UID {metadata['miner_uid']}  ({metadata.get('agent_name', '?')} v{metadata.get('version_number', '?')})"
        )
    if metadata.get("pool"):
        print(f"Pool:       {metadata['pool']}")
    if result.get("parsed_fields"):
        pf = result["parsed_fields"]
        print("\nParsed from query:")
        print(f"  title:       {pf['title']}")
        print(f"  description: {pf['description']}")
        print(f"  cutoff:      {pf['cutoff']}")
        print(f"  topics:      {', '.join(pf.get('topics', []))}")
    if metadata.get("reasoning"):
        print(f"\nReasoning:\n{metadata['reasoning']}")
    print("\n--- Full response JSON ---")
    print(json.dumps(job, indent=2, default=str))


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit a Numinous forecast.")
    parser.add_argument(
        "query", nargs="?", help="Natural-language question (query mode)"
    )
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--cutoff", help="ISO 8601, e.g. 2026-12-31T23:59:59Z")
    parser.add_argument("--topics", help="Comma-separated, e.g. crypto,finance")
    parser.add_argument(
        "--agent-version-id", help="Pin a specific miner (UUID from leaderboard)"
    )
    args = parser.parse_args()

    api_key = os.environ.get("NUMINOUS_API_KEY")
    if not api_key:
        sys.exit(
            "NUMINOUS_API_KEY is not set.\n"
            "Create one at https://eversight.numinouslabs.io/api-keys, then:\n"
            "  export NUMINOUS_API_KEY=<your_key>"
        )

    payload = _build_payload(args)
    print(f"Submitting forecast to {BASE_URL}{JOBS_PATH}...")
    prediction_id = submit(payload, api_key)
    print(f"prediction_id: {prediction_id}")
    job = poll(prediction_id)
    render(job)


if __name__ == "__main__":
    main()
