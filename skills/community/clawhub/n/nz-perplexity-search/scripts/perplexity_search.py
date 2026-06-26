#!/usr/bin/env python3
"""Perplexity Sonar web search for OpenClaw / ClawHub.

Reads PERPLEXITY_API_KEY from the environment.
Uses only Python standard library — no pip installs required.

Usage:
    python3 perplexity_search.py --query "your question here"
    python3 perplexity_search.py --query "..." --model sonar-pro
    python3 perplexity_search.py --query "..." --domains docs.example.com
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
from typing import Any

# ── Constants ──────────────────────────────────────────────────────────────────

API_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar"

ALLOWED_MODELS = {
    "sonar",
    "sonar-pro",
    "sonar-deep-research",
    "sonar-reasoning",
    "sonar-reasoning-pro",
}

SYSTEM_PROMPT = (
    "You are a web research assistant. "
    "Give a precise, concise answer grounded in recent web sources. "
    "Include enough detail to be directly useful, but avoid filler."
)


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Search the web with Perplexity Sonar.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--query", required=True, help="Search query or user question")
    p.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=sorted(ALLOWED_MODELS),
        metavar="MODEL",
        help=(
            f"Perplexity model. One of: {', '.join(sorted(ALLOWED_MODELS))}. "
            f"Default: {DEFAULT_MODEL}"
        ),
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature 0–1. Lower = more factual. Default: 0.2",
    )
    p.add_argument(
        "--domains",
        default="",
        help="Comma-separated domain allowlist, e.g. docs.python.org,github.com",
    )
    p.add_argument(
        "--max-results",
        type=int,
        default=8,
        help="Max search results to display. Default: 8",
    )
    p.add_argument(
        "--json",
        dest="raw_json",
        action="store_true",
        help="Print raw JSON response instead of formatted markdown",
    )
    return p.parse_args()


# ── Auth ───────────────────────────────────────────────────────────────────────

def require_api_key() -> str:
    key = os.environ.get("PERPLEXITY_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: PERPLEXITY_API_KEY environment variable is not set.\n"
            "Add it to ~/.openclaw/.env:\n"
            "  PERPLEXITY_API_KEY=pplx-your-key-here\n"
            "Get a key at: https://www.perplexity.ai/settings/api",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


# ── Request ────────────────────────────────────────────────────────────────────

def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "temperature": args.temperature,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": args.query.strip()},
        ],
    }
    domains = [d.strip() for d in args.domains.split(",") if d.strip()]
    if domains:
        payload["search_domain_filter"] = domains
    return payload


def call_api(api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code} from Perplexity API:\n{body}", file=sys.stderr)
        sys.exit(3)
    except urllib.error.URLError as exc:
        print(f"Network error reaching Perplexity API: {exc}", file=sys.stderr)
        sys.exit(4)


# ── Formatting ─────────────────────────────────────────────────────────────────

def _text(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    return (((choices[0] or {}).get("message") or {}).get("content") or "").strip()


def format_output(response: dict[str, Any], max_results: int, model: str) -> str:
    answer = _text(response)
    citations: list[str] = response.get("citations") or []
    search_results: list[dict] = response.get("search_results") or []
    related: list[str] = response.get("related_questions") or []
    usage: dict = response.get("usage") or {}

    lines: list[str] = []

    # ── Header
    lines += [f"# 🔎 Perplexity Search  ·  model: {model}", ""]

    # ── Answer
    if answer:
        lines += ["## Answer", "", answer, ""]

    # ── Citations
    if citations:
        lines += ["## Citations", ""]
        for i, url in enumerate(citations, 1):
            lines.append(f"{i}. {url}")
        lines.append("")

    # ── Search results
    if search_results:
        lines += ["## Search Results", ""]
        for i, item in enumerate(search_results[:max_results], 1):
            title = item.get("title") or "Untitled"
            url = item.get("url") or item.get("origin_url") or ""
            date = item.get("date") or item.get("last_updated") or ""
            snippet = (item.get("snippet") or "").strip()
            if snippet:
                snippet = textwrap.shorten(snippet, width=260, placeholder="…")

            header = f"**{i}. {title}**"
            if date:
                header += f" _({date})_"
            lines.append(header)
            if url:
                lines.append(f"   <{url}>")
            if snippet:
                lines.append(f"   {snippet}")
            lines.append("")

    # ── Related questions
    if related:
        lines += ["## Related Questions", ""]
        for q in related[:6]:
            lines.append(f"- {q}")
        lines.append("")

    # ── Usage summary
    if usage:
        parts = []
        if (t := usage.get("total_tokens")) is not None:
            parts.append(f"tokens: {t}")
        if (n := usage.get("num_search_queries")) is not None:
            parts.append(f"queries: {n}")
        if (c := (usage.get("cost") or {}).get("total_cost")) is not None:
            parts.append(f"cost: ${c:.4f}")
        if parts:
            lines += [f"_Usage — {' · '.join(parts)}_", ""]

    if not answer and not search_results:
        lines.append("_No results returned from Perplexity._")

    return "\n".join(lines).rstrip() + "\n"


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    api_key = require_api_key()
    payload = build_payload(args)
    response = call_api(api_key, payload)

    if args.raw_json:
        print(json.dumps(response, indent=2, ensure_ascii=False))
        return

    print(format_output(response, max_results=args.max_results, model=args.model))


if __name__ == "__main__":
    main()
