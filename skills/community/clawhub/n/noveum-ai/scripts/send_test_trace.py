#!/usr/bin/env python3
"""Send one known-good trace to the Noveum ingest API.

Purpose: isolate connectivity/auth problems from SDK-integration problems.
If this succeeds but the app's traces don't arrive, the issue is in the app's
integration (usually a missing flush), not key/endpoint/network.

Usage:
    NOVEUM_API_KEY=nv_... NOVEUM_PROJECT=my-app python send_test_trace.py

Env:
    NOVEUM_API_KEY   required
    NOVEUM_PROJECT   required (project auto-creates on first trace)
    NOVEUM_ENDPOINT  optional, default https://api.noveum.ai/api (the API *base*)

Stdlib only. Exit codes: 0 accepted, 2 configuration/connectivity error.
"""

import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

DEFAULT_ENDPOINT = "https://api.noveum.ai/api"
# Ingest is enqueue-based; a modest timeout is enough for the ack.
REQUEST_TIMEOUT_S = 30


def build_trace(project: str) -> dict:
    trace_id = uuid.uuid4().hex
    end = datetime.now(timezone.utc)
    start = end - timedelta(seconds=1)
    iso = lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"  # noqa: E731
    return {
        "trace_id": trace_id,
        "name": "noveum-skill-test-trace",
        "project": project,
        "environment": os.environ.get("NOVEUM_ENVIRONMENT", "production"),
        "start_time": iso(start),
        "end_time": iso(end),
        "duration_ms": 1000,
        "status": "ok",
        "span_count": 1,
        "sdk": {"name": "noveum-skill-check", "version": "0.1.0"},
        "metadata": {"tags": {"source": "noveum-skill"}},
        "spans": [
            {
                "span_id": uuid.uuid4().hex[:16],
                "trace_id": trace_id,
                "name": "llm.call",
                "start_time": iso(start),
                "end_time": iso(end),
                "duration_ms": 1000,
                "status": "ok",
                "attributes": {
                    "llm.model": "test-model",
                    "llm.provider": "test",
                    "llm.input_tokens": 10,
                    "llm.output_tokens": 5,
                    "llm.total_tokens": 15,
                    "llm.system_prompt": "You are a test assistant.",
                    "llm.input": '[{"role":"user","content":"ping"}]',
                    "llm.response": "pong",
                },
            }
        ],
    }


def main() -> int:
    api_key = os.environ.get("NOVEUM_API_KEY", "").strip()
    project = os.environ.get("NOVEUM_PROJECT", "").strip()
    if not api_key or not project:
        print("CONFIG ERROR: set NOVEUM_API_KEY and NOVEUM_PROJECT env vars.")
        return 2
    endpoint = os.environ.get("NOVEUM_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")
    if endpoint.endswith("/v1/traces"):
        print(
            "CONFIG ERROR: NOVEUM_ENDPOINT must be the API base "
            f"(e.g. {DEFAULT_ENDPOINT}), not the full /v1/traces path."
        )
        return 2

    url = f"{endpoint}/v1/traces"
    body = json.dumps({"traces": [build_trace(project)]}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as res:
            payload = res.read().decode(errors="replace")
            print(f"OK: HTTP {res.status} from {url}")
            print(payload[:2000])
            print(
                "\nNote: ingest is asynchronous — the trace appears in queries a few "
                "seconds after this ack. Run check_integration.py next."
            )
            return 0
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:1000]
        if e.code == 401:
            print(f"AUTH ERROR: HTTP 401 from {url} — the API key is wrong or expired.")
        elif e.code == 429:
            print(f"QUOTA/RATE ERROR: HTTP 429 from {url} — quota or rate limit. Detail:")
        else:
            print(f"HTTP ERROR {e.code} from {url}:")
        print(detail)
        return 2
    except urllib.error.URLError as e:
        print(f"NETWORK ERROR reaching {url}: {e.reason}")
        print("Check NOVEUM_ENDPOINT and network egress.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
