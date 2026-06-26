#!/usr/bin/env python3
"""List n8n executions for an env, with cursor pagination, status filter, and tally mode.

Default mode: emit a JSON array of execution rows on stdout.
`--tally` mode: walk every page and emit a status histogram (plus `hung_count` and
`crash_count` aggregates) — used by the inspect-execution Step 1.5 baseline.
`--limit` is ignored in `--tally` mode (single source of truth).

Status enum (from n8n's documented `/executions` schema):
    error | success | running | canceled | waiting | crashed | queued

Pagination follows the documented cursor-based scheme: `nextCursor` from the previous
response is passed as `cursor` on the next request; absence of `nextCursor` means
last page.

`workflowId` is `required: false` per n8n's official OpenAPI spec
(packages/cli/src/public-api/v1/handlers/executions/spec/paths/executions.yml).
When `--workflow-key` is omitted, the helper makes a single env-scoped call without
workflowId; when provided, it scopes the call to that one workflow's id.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client, N8nClient


_STATUS_CHOICES = ("error", "success", "running", "canceled", "waiting", "crashed", "queued")
_PAGE_SIZE = 250  # max documented per-page; we cap our own --limit downstream
_RUNNING_HUNG_THRESHOLD_SECONDS = 60 * 60  # "running with startedAt > 1h ago" is the hung signal


def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def _resolve_workflow_id(yaml_data: dict, workflow_key: str) -> str:
    return str(get_config_value(yaml_data, f"workflows.{workflow_key}.id"))


def _fetch_executions(
    client: N8nClient,
    *,
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    started_after: Optional[datetime] = None,
    started_before: Optional[datetime] = None,
    limit: Optional[int] = None,
) -> list[dict]:
    """Walk pages of /executions, applying client-side time-window filtering.

    `workflow_id=None` issues an env-scoped call (no workflowId param). `limit` caps
    the post-filter row count returned (None = no cap). Pagination is cursor-based:
    pass `cursor` from `nextCursor` of the prior page until absent.
    """
    out: list[dict] = []
    cursor: Optional[str] = None
    while True:
        params: dict = {"limit": _PAGE_SIZE}
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status
        if cursor:
            params["cursor"] = cursor

        resp = client.get("executions", params=params)
        rows = resp.get("data") or []
        for row in rows:
            started = _parse_iso(row.get("startedAt"))
            if started_after and started and started < started_after:
                continue
            if started_before and started and started > started_before:
                continue
            out.append(row)
            if limit is not None and len(out) >= limit:
                return out

        cursor = resp.get("nextCursor")
        if not cursor:
            break
    return out


def _is_hung_running(row: dict, now: datetime) -> bool:
    """A row counts as "hung" running if its startedAt is older than the threshold."""
    started = _parse_iso(row.get("startedAt"))
    if not started:
        return False
    age = (now - started).total_seconds()
    return age > _RUNNING_HUNG_THRESHOLD_SECONDS


def _tally_executions(rows: list[dict]) -> dict:
    """Status histogram + derived `hung_count` and `crash_count`."""
    hist: dict = {s: 0 for s in _STATUS_CHOICES}
    now = datetime.now(timezone.utc)
    hung_running = 0
    for row in rows:
        st = row.get("status")
        if st in hist:
            hist[st] += 1
        if st == "running" and _is_hung_running(row, now):
            hung_running += 1
    hung_count = hist["waiting"] + hist["queued"] + hung_running
    crash_count = hist["crashed"]
    total = sum(hist.values())
    return {
        "total": total,
        "by_status": hist,
        "hung_count": hung_count,
        "crash_count": crash_count,
        "running_hung_count": hung_running,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", default=None, dest="workflow_key",
                        help="Yaml key; if omitted, the call is env-scoped (no workflowId filter).")
    parser.add_argument("--status", choices=_STATUS_CHOICES, default=None,
                        help="Filter by execution status server-side.")
    parser.add_argument("--started-after", default=None, dest="started_after",
                        help="ISO 8601 UTC; filter to executions whose startedAt >= this (client-side).")
    parser.add_argument("--started-before", default=None, dest="started_before",
                        help="ISO 8601 UTC; filter to executions whose startedAt <= this (client-side).")
    parser.add_argument("--limit", type=int, default=100,
                        help="Cap on rows returned (post-filter). Default 100. Ignored in --tally.")
    parser.add_argument("--tally", action="store_true",
                        help="Walk every page; emit a status histogram only.")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    yaml_data = load_yaml(args.env, ws)
    load_env(args.env, ws)
    client = ensure_client(args.env, ws)

    started_after = _parse_iso(args.started_after) if args.started_after else None
    started_before = _parse_iso(args.started_before) if args.started_before else None

    workflow_id = _resolve_workflow_id(yaml_data, args.workflow_key) if args.workflow_key else None

    # `--limit` is a post-filter cap; in tally mode we ignore it (walk everything).
    per_call_cap = None if args.tally else args.limit

    rows = _fetch_executions(
        client,
        workflow_id=workflow_id,
        status=args.status,
        started_after=started_after,
        started_before=started_before,
        limit=per_call_cap,
    )

    if args.tally:
        result = _tally_executions(rows)
        print(json.dumps(result, indent=2))
        return

    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
