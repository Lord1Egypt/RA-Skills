#!/usr/bin/env python3
"""Submit a Numinous forecast paying via x402 (USDC on Base or Solana).

Usage:
  python forecast_x402.py "Will ETH exceed $10k before end of 2026?"
  python forecast_x402.py --title "..." --description "..." --cutoff 2026-12-31T23:59:59Z

Requires:
  NUMINOUS_X402_EVM_PRIVATE_KEY  (hex, with or without 0x prefix)   — for Base USDC
  OR extend this script for Solana using register_exact_svm_client.

Dependencies:
  pip install 'x402[client]' eth-account httpx

Cost: $0.10 USDC per request (on-chain settlement).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time

try:
    import httpx
    from eth_account import Account
    from x402 import x402Client
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client
except ImportError as exc:
    sys.exit(
        f"Missing dependency: {exc.name}\n"
        "Install with: pip install 'x402[client]' eth-account httpx"
    )

BASE_URL = os.environ.get("NUMINOUS_BASE_URL", "https://api.numinouslabs.io")
JOBS_PATH = "/api/v1/forecasters/prediction-jobs"
POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 300


def _normalize_evm_key(raw: str) -> str:
    key = raw.strip()
    if len(key) == 64:
        try:
            int(key, 16)
            return "0x" + key
        except ValueError:
            return key
    return key


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
        payload.update(
            title=args.title,
            description=args.description,
            cutoff=args.cutoff,
        )
        if args.topics:
            payload["topics"] = [t.strip() for t in args.topics.split(",") if t.strip()]
        return payload
    if not args.query:
        sys.exit("Provide either a query string or --title/--description/--cutoff.")
    payload["query"] = args.query
    return payload


async def submit_with_x402(payload: dict, account) -> str:
    client = x402Client()
    register_exact_evm_client(client, EthAccountSigner(account))

    async with x402HttpxClient(client, timeout=120) as http:
        resp = await http.post(f"{BASE_URL}{JOBS_PATH}", json=payload)
        await resp.aread()
        if resp.status_code == 202:
            return resp.json()["prediction_id"]
        if resp.status_code == 402:
            sys.exit(
                "402 Payment Required even after x402 flow.\n"
                "Check wallet has enough USDC (need ≥$0.10 on Base). "
                "Server body: " + resp.text[:300]
            )
        sys.exit(f"Unexpected {resp.status_code}: {resp.text[:300]}")


async def poll(prediction_id: str) -> dict:
    url = f"{BASE_URL}{JOBS_PATH}/{prediction_id}"
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    last_status = None
    async with httpx.AsyncClient(timeout=30) as http:
        while time.monotonic() < deadline:
            resp = await http.get(url)
            if resp.status_code == 404:
                sys.exit(f"Prediction {prediction_id} not found.")
            resp.raise_for_status()
            body = resp.json()
            status = body.get("status")
            if status != last_status:
                print(f"  status: {status}", flush=True)
                last_status = status
            if status == "COMPLETED":
                return body
            if status == "FAILED":
                sys.exit(f"Job failed: {body.get('error')}")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    sys.exit(f"Timed out after {POLL_TIMEOUT_SECONDS}s. Prediction ID: {prediction_id}")


def render(job: dict) -> None:
    result = job["result"]
    metadata = result.get("metadata") or {}
    print()
    print(f"Prediction: {result['prediction']:.1%}  (raw: {result['prediction']})")
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


async def main_async() -> None:
    parser = argparse.ArgumentParser(
        description="Submit a Numinous forecast paying via x402 (USDC)."
    )
    parser.add_argument(
        "query", nargs="?", help="Natural-language question (query mode)"
    )
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--cutoff")
    parser.add_argument("--topics")
    parser.add_argument("--agent-version-id")
    args = parser.parse_args()

    raw_key = os.environ.get("NUMINOUS_X402_EVM_PRIVATE_KEY")
    if not raw_key:
        sys.exit(
            "NUMINOUS_X402_EVM_PRIVATE_KEY is not set.\n"
            "Provide the hex private key of a wallet holding USDC on Base (chain 8453).\n"
            "Alternatively, use scripts/forecast.py with a NUMINOUS_API_KEY."
        )
    account = Account.from_key(_normalize_evm_key(raw_key))
    print(f"Paying from wallet: {account.address}")

    payload = _build_payload(args)
    print(f"Submitting forecast to {BASE_URL}{JOBS_PATH}...")
    prediction_id = await submit_with_x402(payload, account)
    print(f"prediction_id: {prediction_id}")
    job = await poll(prediction_id)
    render(job)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
