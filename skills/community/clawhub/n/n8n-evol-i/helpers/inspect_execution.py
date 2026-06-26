#!/usr/bin/env python3
"""Fetch a single n8n execution by id and emit its JSON to stdout.

`--include-data` defaults FALSE (matches the lighter-weight metadata default of
GET /executions/{id}). With it on, the helper truncates the `data` payload at
`--max-size-kb` and prints a TRUNCATED warning to stderr; pass `--no-truncate`
to get the full payload (warns on stderr if > 100KB so the agent can route to
targeted node inspection instead of consuming the full blob).

Status-enum semantics, retryOf chain, and the truncation-escalation rule are
documented in skills/patterns/investigation-discipline.md (Step 3 / Step 3b).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_env
from helpers.n8n_client import ensure_client


_DEFAULT_MAX_SIZE_KB = 50
_NO_TRUNCATE_WARN_THRESHOLD_KB = 100


def _truncate_data_field(execution: dict, max_size_kb: int) -> tuple[dict, bool]:
    """If execution['data'] serializes to more than max_size_kb, replace with a marker.

    Returns (possibly-truncated dict, was_truncated_bool).
    """
    if "data" not in execution or execution["data"] is None:
        return execution, False
    serialized = json.dumps(execution["data"])
    size_bytes = len(serialized.encode("utf-8"))
    if size_bytes <= max_size_kb * 1024:
        return execution, False

    truncated = dict(execution)
    truncated["data"] = {
        "__truncated__": True,
        "original_size_bytes": size_bytes,
        "max_size_kb": max_size_kb,
        "preview": serialized[: max_size_kb * 1024],
    }
    return truncated, True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--execution-id", required=True, dest="execution_id")
    parser.add_argument("--include-data", action="store_true", dest="include_data",
                        help="Include the per-node data field. Default off.")
    parser.add_argument("--max-size-kb", type=int, default=_DEFAULT_MAX_SIZE_KB, dest="max_size_kb",
                        help=f"Truncate `data` if it exceeds this many KB. Default {_DEFAULT_MAX_SIZE_KB}.")
    parser.add_argument("--no-truncate", action="store_true", dest="no_truncate",
                        help="Return the full payload regardless of size; warns to stderr if >100KB.")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    client = ensure_client(args.env, ws)

    params: dict = {}
    if args.include_data:
        params["includeData"] = "true"

    execution = client.get(f"executions/{args.execution_id}", params=params)

    if args.include_data and not args.no_truncate:
        execution, was_truncated = _truncate_data_field(execution, args.max_size_kb)
        if was_truncated:
            print(
                f"TRUNCATED — execution {args.execution_id} `data` exceeded "
                f"{args.max_size_kb}KB; pass --no-truncate for full payload",
                file=sys.stderr,
            )

    if args.include_data and args.no_truncate and execution.get("data") is not None:
        size_bytes = len(json.dumps(execution["data"]).encode("utf-8"))
        if size_bytes > _NO_TRUNCATE_WARN_THRESHOLD_KB * 1024:
            print(
                f"WARN — full payload is {size_bytes // 1024}KB; consider node-targeted inspection",
                file=sys.stderr,
            )

    print(json.dumps(execution, indent=2))


if __name__ == "__main__":
    main()
