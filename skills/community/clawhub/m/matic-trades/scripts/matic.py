#!/usr/bin/env python3
"""
Matic Trades API helper for OpenClaw skills (stdlib only).

- toolbox  -> POST /toolbox/execute  (mode AI_PICK, prompt only by default)
- data     -> POST /data/execute      (mode SMART_SEARCH)
- chart    -> POST /agent/chart/autonomous

AI_PICK does not require `context`; put everything in `prompt` (see SKILL.md).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict


def _base_url() -> str:
    raw = os.environ.get("MATIC_TRADES_API_BASE", "https://api.matictrades.com/api/v1").strip().rstrip("/")
    return raw


def _api_key() -> str:
    key = os.environ.get("MATIC_API_KEY") or os.environ.get("MATIC_TRADES_API_KEY")
    if not key or not key.strip():
        print(
            "Error: Set MATIC_API_KEY (or MATIC_TRADES_API_KEY) to your Matic Trades API key.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key.strip()


def _post(path: str, body: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{_base_url()}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            if not text.strip():
                return {}
            return json.loads(text)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(err_body)
        except json.JSONDecodeError:
            detail = err_body
        print(
            f"HTTP {e.code} {e.reason}\n"
            f"{json.dumps(detail, indent=2) if isinstance(detail, dict) else detail}",
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_toolbox(args: argparse.Namespace) -> None:
    # AI_PICK: only mode + prompt required; context is optional on API but not needed for tool selection
    body: Dict[str, Any] = {
        "mode": "AI_PICK",
        "prompt": args.prompt,
    }
    out = _post("/toolbox/execute", body)
    print(json.dumps(out, indent=2))


def cmd_data(args: argparse.Namespace) -> None:
    body: Dict[str, Any] = {
        "mode": "SMART_SEARCH",
        "prompt": args.prompt,
    }
    if args.symbol:
        body["symbol"] = args.symbol
    if args.interval:
        body["interval"] = args.interval
    out = _post("/data/execute", body)
    print(json.dumps(out, indent=2))


def cmd_chart(args: argparse.Namespace) -> None:
    options: Dict[str, Any] = {
        "images": args.images,
    }
    if args.max_actions is not None:
        options["max_actions"] = args.max_actions
    if args.model:
        options["model"] = args.model
    body: Dict[str, Any] = {
        "prompt": args.prompt,
        "options": options,
    }
    out = _post("/agent/chart/autonomous", body)
    print(json.dumps(out, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="Matic Trades API CLI for OpenClaw skill")
    sub = p.add_subparsers(dest="command", required=True)

    t = sub.add_parser("toolbox", help="POST /toolbox/execute with mode=AI_PICK (prompt only)")
    t.add_argument("--prompt", required=True, help="Full natural-language task; tool choice is derived from this")
    t.set_defaults(func=cmd_toolbox)

    d = sub.add_parser("data", help="POST /data/execute with mode=SMART_SEARCH")
    d.add_argument("--prompt", required=True, help="Natural language data / indicator request")
    d.add_argument("--symbol", default=None, help="Optional symbol hint (e.g. NVDA, BTC/USD)")
    d.add_argument("--interval", default=None, help="Optional interval (e.g. 1day)")
    d.set_defaults(func=cmd_data)

    c = sub.add_parser("chart", help="POST /agent/chart/autonomous")
    c.add_argument("--prompt", required=True, help="Chart / analysis instruction")
    c.add_argument(
        "--images",
        choices=("url", "b64", "both"),
        default="url",
        help="How to return chart images in response",
    )
    c.add_argument("--max-actions", type=int, default=None, help="Optional cap on agent steps")
    c.add_argument("--model", default=None, help="Optional model override (e.g. gpt-4o)")
    c.set_defaults(func=cmd_chart)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
