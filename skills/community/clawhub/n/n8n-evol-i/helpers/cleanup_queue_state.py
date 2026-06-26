#!/usr/bin/env python3
"""Wipe a queue's Redis state (semaphore counter, permit sidecars, consumer
group, main stream, DLQ stream). Operator script for debugging, draining a
deprecated queue, or post-incident reset.

Dry-run by default — shows current state and the commands that would be issued.
Pass --force to actually mutate.

Usage:

    python3 helpers/cleanup_queue_state.py --env <env> --stream <name> [--group <name>] [--keep-dlq] [--force]

Reads UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN from <workspace>/n8n-config/.env.<env>.
"""
import argparse
import json
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_env


def _upstash_call(base_url: str, token: str, cmd: list) -> dict:
    resp = requests.post(
        base_url.rstrip("/") + "/",
        headers={"Authorization": f"Bearer {token}"},
        json=cmd,
    )
    resp.raise_for_status()
    return resp.json()


def _probe_state(base_url: str, token: str, stream: str, group: str, dlq_stream: str) -> dict:
    """Best-effort snapshot of current state. Tolerates errors per-command."""
    state = {"stream": stream, "group": group, "dlq_stream": dlq_stream}
    def safe(cmd):
        try:
            return _upstash_call(base_url, token, cmd).get("result")
        except Exception as e:
            return f"<error: {e}>"
    state["inflight"] = safe(["GET", f"q:{stream}:inflight"])
    state["permit_keys"] = safe(["KEYS", f"q:{stream}:permits:*"])
    state["xlen_main"] = safe(["XLEN", stream])
    state["xlen_dlq"] = safe(["XLEN", dlq_stream])
    # XINFO GROUPS — may return error if stream/group doesn't exist
    state["xinfo_groups"] = safe(["XINFO", "GROUPS", stream])
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True, help="Env name (e.g. dev, prod, dod)")
    parser.add_argument("--stream", required=True, help="Stream name (e.g. orders, test-stream)")
    parser.add_argument("--group", default=None,
                        help="Consumer group name. Defaults to '<stream>-cg' (the queue_pop default).")
    parser.add_argument("--keep-dlq", action="store_true",
                        help="Do not delete the DLQ stream (<stream>-dlq). Use when you want to preserve "
                             "forensic data for inspection after cleanup.")
    parser.add_argument("--force", action="store_true",
                        help="Actually mutate. Without --force, prints the snapshot + planned commands and exits.")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)

    base_url = os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    if not base_url or not token:
        raise SystemExit(
            f"UPSTASH_REDIS_REST_URL or UPSTASH_REDIS_REST_TOKEN missing from "
            f".env.{args.env}. Set both before running."
        )

    stream = args.stream
    group = args.group or f"{stream}-cg"
    dlq_stream = f"{stream}-dlq"

    print(f"Probing current state for stream='{stream}' (group='{group}')…")
    snapshot = _probe_state(base_url, token, stream, group, dlq_stream)
    print(json.dumps(snapshot, indent=2))

    permit_keys = snapshot.get("permit_keys") or []
    if not isinstance(permit_keys, list):
        permit_keys = []

    planned = [
        ["DEL", f"q:{stream}:inflight"],
        *[["DEL", k] for k in permit_keys],
        ["XGROUP", "DESTROY", stream, group],
        ["DEL", stream],
    ]
    if not args.keep_dlq:
        planned.append(["DEL", dlq_stream])

    print(f"\nPlanned commands ({len(planned)}):")
    for cmd in planned:
        print(f"  {' '.join(cmd)}")

    if not args.force:
        print("\nDRY-RUN. Rerun with --force to execute.")
        return

    print("\nExecuting…")
    results = []
    for cmd in planned:
        try:
            r = _upstash_call(base_url, token, cmd)
            results.append({"cmd": cmd, "result": r.get("result"), "error": r.get("error")})
        except Exception as e:
            results.append({"cmd": cmd, "result": None, "error": str(e)})
    print(json.dumps(results, indent=2))

    n_ok = sum(1 for r in results if not r.get("error"))
    print(f"\nDone. {n_ok}/{len(results)} commands succeeded.")
    if n_ok != len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
