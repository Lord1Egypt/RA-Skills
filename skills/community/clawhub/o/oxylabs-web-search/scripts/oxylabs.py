#!/usr/bin/env python3
"""Web search and page reading via the Oxylabs AI Studio REST API.

Dependency-free: calls the API directly with Python's standard library
(urllib) — no SDK, no `pip install`. One subcommand per job:

    search   find pages for a query (URLs + optional content) -> /search
    scrape   read a single URL as Markdown                     -> /scrape

Auth: OpenClaw can inject skills.entries.oxylabs-web-search.apiKey as
OXYLABS_AI_STUDIO_API_KEY. Direct script runs can set that env var or add it to
~/.openclaw/.env. Output is Markdown.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_KEY_ENV = "OXYLABS_AI_STUDIO_API_KEY"
BASE_URL = "https://api-aistudio.oxylabs.io"
POLL_INTERVAL_SECONDS = 5

# Sent on every request so Oxylabs can attribute traffic: User-Agent names the
# integration (like the Hermes plugin's "hermes-agent"); the source header names
# the distribution channel this skill was installed from.
INTEGRATION_UA = "openclaw"
INTEGRATION_SOURCE = "clawhub"


# --------------------------------------------------------------------------- #
# API key + REST client (stdlib only)
# --------------------------------------------------------------------------- #
def _require_api_key() -> str:
    key = os.getenv(API_KEY_ENV, "").strip()
    if not key:
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.is_file():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip().removeprefix("export ").strip()
                name, sep, value = line.partition("=")
                if sep and name.strip() == API_KEY_ENV:
                    key = value.strip().strip("'\"")
                    break
    if not key:
        sys.exit(
            f"error: {API_KEY_ENV} is not set.\n"
            "Get a key at https://aistudio.oxylabs.io/api-key.\n"
            "Inside OpenClaw, add skills.entries.oxylabs-web-search.apiKey to ~/.openclaw/openclaw.json.\n"
            "For direct script runs, export it:\n"
            f"    export {API_KEY_ENV}=...\n"
            f"or add {API_KEY_ENV}=... to ~/.openclaw/.env"
        )
    return key


def _request(method: str, path: str, api_key: str, body=None, params=None):
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("x-api-key", api_key)
    req.add_header("User-Agent", INTEGRATION_UA)
    req.add_header("x-integration-source", INTEGRATION_SOURCE)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        sys.exit(f"error: HTTP {exc.code} from {path}: {exc.read().decode(errors='replace')}")
    except urllib.error.URLError as exc:
        sys.exit(f"error: request to {path} failed: {exc.reason}")


def _poll(path: str, run_id: str, api_key: str, timeout_seconds: int):
    for _ in range(timeout_seconds // POLL_INTERVAL_SECONDS):
        status, body = _request("GET", path, api_key, params={"run_id": run_id})
        if status != 200:  # 202 = still running
            time.sleep(POLL_INTERVAL_SECONDS)
            continue
        state = body.get("status")
        if state == "completed":
            return body.get("data")
        if state == "failed":
            sys.exit(f"error: job failed: {body.get('error_code')}")
        time.sleep(POLL_INTERVAL_SECONDS)
    sys.exit("error: timed out waiting for job to complete")


# --------------------------------------------------------------------------- #
# search
# --------------------------------------------------------------------------- #
def cmd_search(args, api_key: str) -> None:
    # Instant endpoint is faster but only for small, content-free queries.
    if args.limit <= 10 and not args.content:
        _, body = _request("POST", "/search/instant", api_key,
                           body={"query": args.query, "limit": args.limit, "geo_location": args.geo})
        results = body.get("data") or []
    else:
        _, body = _request("POST", "/search/run", api_key, body={
            "query": args.query, "limit": args.limit, "render_javascript": args.render_js,
            "return_content": args.content, "geo_location": args.geo,
        })
        results = _poll("/search/run/data", body["run_id"], api_key, 180) or []

    if not results:
        print("No results.")
        return
    lines = [f"# Results for: {args.query}", ""]
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r.get('title', '(untitled)')}")
        lines.append(r.get("url", ""))
        if r.get("description"):
            lines += ["", r["description"]]
        if args.content and r.get("content"):
            lines += ["", r["content"]]
        lines.append("")
    print("\n".join(lines).strip())


# --------------------------------------------------------------------------- #
# scrape
# --------------------------------------------------------------------------- #
def cmd_scrape(args, api_key: str) -> None:
    render_js = "auto" if args.render_js == "auto" else (args.render_js == "true")
    _, body = _request("POST", "/scrape", api_key, body={
        "url": args.url,
        "output_format": "markdown",
        "render_javascript": render_js,
        "geo_location": args.geo,
    })
    data = _poll("/scrape/run/data", body["run_id"], api_key, 180)
    print(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, default=str))


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oxylabs", description="Oxylabs AI Studio: search the web + read pages.")
    sub = parser.add_subparsers(dest="command", required=True)

    se = sub.add_parser("search", help="Find pages for a query.")
    se.add_argument("query")
    se.add_argument("-n", "--limit", type=int, default=10, help="Max results (<=50, default 10).")
    se.add_argument("--content", action="store_true", help="Include per-result page content.")
    se.add_argument("--render-js", action="store_true", help="Render JavaScript before extracting.")
    se.add_argument("--geo", help="Two-letter ISO country code (e.g. US, DE).")
    se.set_defaults(func=cmd_search)

    sc = sub.add_parser("scrape", help="Get one URL's content as Markdown.")
    sc.add_argument("url")
    sc.add_argument("--render-js", choices=["true", "false", "auto"], default="false")
    sc.add_argument("--geo", help="Two-letter ISO country code (e.g. US, DE).")
    sc.set_defaults(func=cmd_scrape)

    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args, _require_api_key())


if __name__ == "__main__":
    main()
