#!/usr/bin/env python3
"""
MistTrack batch async risk scoring script

Batch-queries AML risk scores for multiple addresses using async mode.
Suitable for large-scale detection scenarios.

Usage:
    export MISTTRACK_API_KEY=YOUR_KEY

    # Pass address list via command line (comma-separated)
    python batch_risk_check.py --addresses 0x1...,0x2...,0x3... --coin ETH

    # Read address list from file (one address per line)
    python batch_risk_check.py --input addresses.txt --coin ETH

    # Output results to CSV file
    python batch_risk_check.py --input addresses.txt --coin ETH --output results.csv

    # API key can also be passed via command line (lower priority than env var)
    python batch_risk_check.py --addresses 0x1...,0x2... --coin ETH --api-key YOUR_KEY
"""

import argparse
import csv
import json
import os
import sys
import threading
from typing import List, Optional

import requests


BASE_URL = "https://openapi.misttrack.io"


def create_task(coin: str, api_key: str, address: str = None, txid: str = None) -> dict:
    """Create an async risk score task"""
    payload = {"coin": coin, "api_key": api_key}
    if address:
        payload["address"] = address
    elif txid:
        payload["txid"] = txid
    else:
        raise ValueError("at least one of address or txid is required")

    response = requests.post(
        f"{BASE_URL}/v2/risk_score_create_task",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def query_task(coin: str, api_key: str, address: str = None, txid: str = None) -> dict:
    """Query async risk score task result (this endpoint has no rate limit)"""
    params = {"coin": coin, "api_key": api_key}
    if address:
        params["address"] = address
    elif txid:
        params["txid"] = txid

    response = requests.get(
        f"{BASE_URL}/v2/risk_score_query_task",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_address_async(
    coin: str,
    api_key: str,
    address: str,
    max_wait: int = 60,
    poll_interval: float = 0.5,
) -> Optional[dict]:
    """
    Async risk score check for a single address

    Args:
        coin: Token type
        api_key: API key
        address: Address to query
        max_wait: Maximum wait time in seconds
        poll_interval: Polling interval in seconds

    Returns:
        Risk score data dict, or None if timed out / failed
    """
    # Create task
    create_result = create_task(coin=coin, api_key=api_key, address=address)
    if not create_result.get("success"):
        print(f"  ❌ Task creation failed [{address}]: {create_result.get('msg')}")
        return None

    has_result = create_result.get("data", {}).get("has_result", False)

    # If no cached result, wait before polling
    if not has_result:
        threading.Event().wait(poll_interval)

    # Poll for result
    elapsed = 0
    while elapsed < max_wait:
        query_result = query_task(coin=coin, api_key=api_key, address=address)

        if query_result.get("msg") == "TaskUnderRunning":
            threading.Event().wait(poll_interval)
            elapsed += poll_interval
            continue

        if query_result.get("success") and query_result.get("data"):
            return query_result.get("data")

        print(f"  ❌ Query failed [{address}]: {query_result.get('msg')}")
        return None

    print(f"  ⏰ Timeout [{address}]: no result after {max_wait} seconds")
    return None


def batch_check(
    addresses: List[str],
    coin: str,
    api_key: str,
    output_file: Optional[str] = None,
    verbose: bool = True,
) -> List[dict]:
    """
    Batch risk score check for addresses

    Args:
        addresses: List of addresses
        coin: Token type
        api_key: API key
        output_file: Output CSV file path (optional)
        verbose: Whether to print detailed output

    Returns:
        List of results, each containing address and risk data
    """
    results = []
    total = len(addresses)

    print(f"\nStarting batch risk score check: {total} addresses, token: {coin}")
    print(f"{'='*60}")

    for idx, address in enumerate(addresses, 1):
        address = address.strip()
        if not address:
            continue

        if verbose:
            print(f"[{idx}/{total}] Checking: {address[:20]}...")

        try:
            data = check_address_async(coin=coin, api_key=api_key, address=address)

            if data:
                score = data.get("score", 0)
                risk_level = data.get("risk_level", "Unknown")
                detail_list = ", ".join(data.get("detail_list", []))

                result = {
                    "address": address,
                    "score": score,
                    "risk_level": risk_level,
                    "detail_list": detail_list,
                    "hacking_event": data.get("hacking_event", ""),
                    "risk_report_url": data.get("risk_report_url", ""),
                }
                results.append(result)

                if verbose:
                    level_emoji = {"Low": "✅", "Moderate": "⚡", "High": "⚠️", "Severe": "⛔"}.get(risk_level, "❓")
                    print(f"       {level_emoji} Score: {score}, Level: {risk_level}")
                    if detail_list:
                        print(f"       Risk: {detail_list}")
            else:
                results.append({
                    "address": address,
                    "score": None,
                    "risk_level": "Error",
                    "detail_list": "Query failed",
                    "hacking_event": "",
                    "risk_report_url": "",
                })

        except Exception as e:
            print(f"  ❌ Exception [{address}]: {e}")
            results.append({
                "address": address,
                "score": None,
                "risk_level": "Error",
                "detail_list": str(e),
                "hacking_event": "",
                "risk_report_url": "",
            })

        # Avoid triggering rate limits
        if idx < total:
            threading.Event().wait(0.3)

    # Summary
    print(f"\n{'='*60}")
    print(f"  Done! {len(results)} addresses checked")
    for level in ["Severe", "High", "Moderate", "Low"]:
        count = sum(1 for r in results if r.get("risk_level") == level)
        if count > 0:
            print(f"  {level}: {count}")
    print(f"{'='*60}\n")

    # Write CSV
    if output_file:
        fieldnames = ["address", "score", "risk_level", "detail_list", "hacking_event", "risk_report_url"]
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Result saved to: {output_file}")

    return results


def main():
    parser = argparse.ArgumentParser(description="MistTrack batch async risk score tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--addresses", help="Address list (comma-separated)")
    group.add_argument("--input", "-i", help="File path containing addresses (one per line)")
    parser.add_argument("--coin", required=True, help="Token type (e.g. ETH, BTC, TRX)")
    parser.add_argument("--api-key", dest="api_key", help="MistTrack API Key (env var MISTTRACK_API_KEY takes priority)")
    parser.add_argument("--output", "-o", help="Output results to CSV file")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output in JSON format")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode, reduce output")

    args = parser.parse_args()

    # Env var takes priority over --api-key
    api_key = os.environ.get("MISTTRACK_API_KEY") or args.api_key
    if not api_key:
        print("Error: set MISTTRACK_API_KEY env var or use --api-key", file=sys.stderr)
        sys.exit(1)

    # Get address list
    if args.addresses:
        addresses = [a.strip() for a in args.addresses.split(",") if a.strip()]
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                addresses = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except FileNotFoundError:
            print(f"Error: file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

    if not addresses:
        print("Error: no valid addresses found", file=sys.stderr)
        sys.exit(1)

    results = batch_check(
        addresses=addresses,
        coin=args.coin,
        api_key=api_key,
        output_file=args.output,
        verbose=not args.quiet,
    )

    if args.json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
