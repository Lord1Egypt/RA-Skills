#!/usr/bin/env python3
"""Wait for block inclusion, then query tx or theorem status on Shentu."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

from submission_config import detect_working_shentud

# Default when no config: Shentu RPC fallback
_FALLBACK_NODE_URL = os.environ.get("SHENTU_NODE_URL", "https://rpc.shentu.org:443")


def _default_node_url() -> str:
    """Use SHENTU_NODE_URL when set; otherwise fall back to the mainnet default."""
    return _FALLBACK_NODE_URL


DEFAULT_NODE_URL = _default_node_url()
DEFAULT_WAIT_SECONDS = 6

STATUS_MEANINGS = {
    "THEOREM_STATUS_PASSED": "The theorem proof has passed verification.",
    "THEOREM_STATUS_PROOF_PERIOD": "The theorem is still active and currently in the proof period.",
    "THEOREM_STATUS_CLOSED": "The theorem is closed and can no longer be proven.",
}


def run_shentud_query(args: list[str], *, shentud_bin: str) -> dict:
    command = [shentud_bin, *args, "-o", "json"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except (FileNotFoundError, OSError) as exc:
        raise RuntimeError(
            "shentud is unavailable "
            f"({exc}). First try plain `shentud` from PATH. If that fails, set "
            "`OPENMATH_SHENTUD_BIN` to a trusted binary path and verify it with "
            "`shentud version` or `$OPENMATH_SHENTUD_BIN version` first."
        ) from exc
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "shentud query failed"
        raise RuntimeError(message)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("shentud returned non-JSON output") from exc


def maybe_wait(wait_seconds: int) -> None:
    if wait_seconds <= 0:
        return
    print(f"Waiting {wait_seconds}s for block inclusion...")
    time.sleep(wait_seconds)


def summarize_tx(payload: dict) -> int:
    print("\n--- Tx Status ---")
    print("TxHash:", payload.get("txhash", "N/A"))
    print("Code:", payload.get("code", "N/A"))
    print("Height:", payload.get("height", "N/A"))
    print("Timestamp:", payload.get("timestamp", "N/A"))

    events = payload.get("events") or []
    for event in events:
        if event.get("type") != "message":
            continue
        attrs = {item.get("key"): item.get("value") for item in event.get("attributes") or []}
        if attrs.get("action"):
            print("Action:", attrs["action"])
            break

    return 0 if str(payload.get("code", "0")) == "0" else 1


def summarize_theorem(payload: dict) -> int:
    theorem = payload.get("theorem") or {}
    theorem_id = theorem.get("id", "N/A")
    status = theorem.get("status", "UNKNOWN")
    title = theorem.get("title", "N/A")

    print("\n--- Theorem Status ---")
    print("Theorem ID:", theorem_id)
    print("Title:", title)
    print("Status:", status)
    print("Meaning:", STATUS_MEANINGS.get(status, "Unknown theorem status."))
    print("End Time:", theorem.get("end_time", "N/A"))

    total_grant = theorem.get("total_grant") or []
    if total_grant:
        amounts = ", ".join(f"{item.get('amount', '?')}{item.get('denom', '')}" for item in total_grant)
        print("Total Grant:", amounts)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Wait for a Shentu block, then query tx or theorem status."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    tx_parser = subparsers.add_parser("tx", help="Wait, then query a transaction hash.")
    tx_parser.add_argument("txhash", help="Transaction hash to query")
    tx_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help=f"Seconds to wait before querying (default: {DEFAULT_WAIT_SECONDS})",
    )
    tx_parser.add_argument(
        "--node",
        default=DEFAULT_NODE_URL,
        help=f"RPC node URL (default: {DEFAULT_NODE_URL})",
    )

    theorem_parser = subparsers.add_parser("theorem", help="Wait, then query a theorem ID.")
    theorem_parser.add_argument("theorem_id", type=int, help="Theorem ID to query")
    theorem_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help=f"Seconds to wait before querying (default: {DEFAULT_WAIT_SECONDS})",
    )
    theorem_parser.add_argument(
        "--node",
        default=DEFAULT_NODE_URL,
        help=f"RPC node URL (default: {DEFAULT_NODE_URL})",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        shentud_bin, _version = detect_working_shentud()
        maybe_wait(args.wait_seconds)
        if args.mode == "tx":
            payload = run_shentud_query(
                ["q", "tx", args.txhash, "--node", args.node],
                shentud_bin=shentud_bin,
            )
            return summarize_tx(payload)
        if args.mode == "theorem":
            payload = run_shentud_query(
                ["q", "bounty", "theorem", str(args.theorem_id), "--node", args.node],
                shentud_bin=shentud_bin,
            )
            return summarize_theorem(payload)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"unsupported mode: {args.mode}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
