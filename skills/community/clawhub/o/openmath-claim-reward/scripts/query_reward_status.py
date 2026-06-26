#!/usr/bin/env python3
"""Wait for block inclusion, then query rewards or tx status on Shentu."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from decimal import Decimal

from reward_config import (
    DEFAULT_CONFIG_PATH,
    RewardConfigError,
    load_reward_address,
)


DEFAULT_NODE_URL_FALLBACK = os.environ.get("SHENTU_NODE_URL", "https://rpc.shentu.org:443")
DEFAULT_WAIT_SECONDS = 6
DEFAULT_NODE_URL = DEFAULT_NODE_URL_FALLBACK


def run_shentud_query(args: list[str]) -> dict:
    try:
        result = subprocess.run(
            ["shentud", *args, "-o", "json"],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError) as exc:
        raise RuntimeError(
            "shentud is unavailable. Install or fix a trusted local shentud binary before querying or withdrawing rewards."
        ) from exc
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "shentud query failed"
        raise RuntimeError(message)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("shentud returned non-JSON output") from exc


def is_no_rewards_error(message: str) -> bool:
    lowered = message.lower()
    return "no rewards found for address" in lowered or "key not found" in lowered


def maybe_wait(wait_seconds: int) -> None:
    if wait_seconds <= 0:
        return
    print(f"Waiting {wait_seconds}s for block inclusion...")
    time.sleep(wait_seconds)


def total_amount(entries: list[dict]) -> str:
    if not entries:
        return "0"

    total = sum(Decimal(entry.get("amount", "0")) for entry in entries)
    return format(total, "f")


def summarize_rewards(payload: dict, address: str) -> int:
    imported_rewards = payload.get("imported_rewards") or []
    proof_rewards = payload.get("proof_rewards") or []

    print("\n--- Reward Status ---")
    print("Address:", address)
    print("Imported Rewards:", total_amount(imported_rewards))
    if imported_rewards:
        for entry in imported_rewards:
            print(f"  - {entry.get('amount', '0')}{entry.get('denom', '')}")

    print("Proof Rewards:", total_amount(proof_rewards))
    if proof_rewards:
        for entry in proof_rewards:
            print(f"  - {entry.get('amount', '0')}{entry.get('denom', '')}")

    if imported_rewards and proof_rewards:
        print("Withdraw Behavior: withdraw-rewards will withdraw both imported_rewards and proof_rewards.")
    elif imported_rewards or proof_rewards:
        print("Withdraw Behavior: withdraw-rewards will withdraw the available reward bucket.")
    else:
        print("Withdraw Behavior: no claimable rewards were returned for this address.")

    return 0


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Wait for a Shentu block, then query rewards or tx status. Reward config can come from --config or OPENMATH_ENV_CONFIG."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    rewards_parser = subparsers.add_parser(
        "rewards", help="Wait, then query claimable imported/proof rewards for an address."
    )
    rewards_parser.add_argument(
        "address",
        nargs="?",
        help="Address to query; if omitted, use prover_address from --config, OPENMATH_ENV_CONFIG, or the default openmath-env.json locations",
    )
    rewards_parser.add_argument(
        "--config",
        default=None,
        help=(
            "Shared config path (resolution: --config, then OPENMATH_ENV_CONFIG, "
            f"then ./.openmath-skills/openmath-env.json, then ~/.openmath-skills/openmath-env.json; "
            f"default target: {DEFAULT_CONFIG_PATH})."
        ),
    )
    rewards_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help=f"Seconds to wait before querying (default: {DEFAULT_WAIT_SECONDS})",
    )
    rewards_parser.add_argument(
        "--node",
        default=DEFAULT_NODE_URL,
        help=f"RPC node URL (default: SHENTU_NODE_URL or {DEFAULT_NODE_URL_FALLBACK})",
    )

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
        help=f"RPC node URL (default: SHENTU_NODE_URL or {DEFAULT_NODE_URL_FALLBACK})",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        if args.mode == "rewards":
            try:
                address = args.address
                if not address:
                    address, config_path = load_reward_address(args.config)
                    print(f"Using prover_address from config: {config_path}")
            except RewardConfigError as exc:
                print(exc, file=sys.stderr)
                return 1
            maybe_wait(args.wait_seconds)
            try:
                payload = run_shentud_query(["q", "bounty", "rewards", address, "--node", args.node])
            except RuntimeError as exc:
                if not is_no_rewards_error(str(exc)):
                    raise
                payload = {"imported_rewards": [], "proof_rewards": []}
            return summarize_rewards(payload, address)
        if args.mode == "tx":
            maybe_wait(args.wait_seconds)
            payload = run_shentud_query(["q", "tx", args.txhash, "--node", args.node])
            return summarize_tx(payload)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"unsupported mode: {args.mode}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
