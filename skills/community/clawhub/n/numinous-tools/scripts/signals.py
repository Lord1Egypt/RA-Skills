#!/usr/bin/env python3
"""Get LLM-scored signals for a Polymarket market or a free-text question.

Usage:
  python signals.py --market https://polymarket.com/event/some-slug
  python signals.py --market some-slug-or-condition-id
  python signals.py --question "Will Iran conduct a nuclear test before end of 2026?"

Optional knobs: --threshold (default 0.25), --max-per-source (default 25), --window-hours (default 72).

Requires: NUMINOUS_API_KEY in env. Signals does not accept x402.
Cost: 0.025 credits per call.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get("NUMINOUS_SIGNALS_URL", "https://signals.numinouslabs.io")
SIGNALS_PATH = "/api/v1/signals"
USER_AGENT = "numinous-skill/0.3 (+https://numinouslabs.io)"


def _request(url: str, headers: dict, body: dict) -> tuple[int, dict]:
    merged = {"User-Agent": USER_AGENT, **headers}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST", headers=merged
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode() or "{}")
        except Exception:
            payload = {"detail": exc.reason}
        return exc.code, payload


def _exit_with_error(status: int, body: dict) -> None:
    detail = body.get("detail", {})
    if isinstance(detail, dict):
        code = detail.get("error_code", "")
        message = detail.get("message", "")
        if code == "MARKET_NOT_FOUND":
            sys.exit(
                f"Market not found: {message}\nTry a current Polymarket URL, or use --question instead."
            )
        if code == "VALIDATION_ERROR":
            sys.exit(f"Validation error: {message}")
        if code == "UPSTREAM_UNAVAILABLE":
            sys.exit(
                f"Polymarket Gamma API unavailable: {message}\nRetry, or use --question."
            )
        sys.exit(f"{status} {code}: {message}")
    sys.exit(f"{status}: {body}")


def render(response: dict) -> None:
    signals = response.get("signals", [])
    meta = response.get("processing_metadata", {})
    print(f"\nContext: {response.get('question_context', '')}")
    if meta.get("market_yes_price") is not None:
        print(f"Market YES price: {meta['market_yes_price']}")
    print(
        f"Signals: {len(signals)} returned  |  scored {meta.get('llm_scored_count', '?')}/{meta.get('total_ingested_events', '?')} events  |  {meta.get('duration_seconds', 0):.1f}s"
    )
    if response.get("failed_sources"):
        print(f"Failed sources: {', '.join(response['failed_sources'])}")
    print()
    for i, signal in enumerate(signals, 1):
        direction_icon = {"supports_yes": "↑", "supports_no": "↓", "neutral": "·"}.get(
            signal["direction"], "?"
        )
        print(
            f"{i:2}. [{signal['source']}] {direction_icon} "
            f"rel={signal['relevance_score']:.2f} imp={signal['impact_score']:.2f} ({signal.get('impact_bucket', '?')})"
        )
        print(f"    {signal['headline']}")
        print(f"    → {signal['rationale']}")
        if signal.get("source_url"):
            print(f"    {signal['source_url']}")
        print()
    print("--- Full response JSON ---")
    print(json.dumps(response, indent=2, default=str))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get signals for a market or question."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--market", help="Polymarket URL, slug, or condition_id")
    group.add_argument("--question", help="Free-text question")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.25,
        help="Relevance threshold 0-1 (default 0.25)",
    )
    parser.add_argument(
        "--max-per-source",
        type=int,
        default=25,
        help="Cap per source 1-100 (default 25)",
    )
    parser.add_argument(
        "--window-hours",
        type=int,
        default=72,
        help="Lookback window 1-720 (default 72)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("NUMINOUS_API_KEY")
    if not api_key:
        sys.exit(
            "NUMINOUS_API_KEY is not set. Signals requires an API key (no x402).\n"
            "Create one at https://eversight.numinouslabs.io/api-keys, then:\n"
            "  export NUMINOUS_API_KEY=<your_key>"
        )

    payload = {
        "market": args.market,
        "question": args.question,
        "relevance_threshold": args.threshold,
        "max_events_per_source": args.max_per_source,
        "time_window_hours": args.window_hours,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    print(f"Requesting signals from {BASE_URL}{SIGNALS_PATH}...")
    status, body = _request(
        f"{BASE_URL}{SIGNALS_PATH}",
        {"Content-Type": "application/json", "X-API-Key": api_key},
        payload,
    )
    if status == 401:
        sys.exit("401 Unauthorized — NUMINOUS_API_KEY is missing or invalid.")
    if status != 200:
        _exit_with_error(status, body)
    render(body)


if __name__ == "__main__":
    main()
