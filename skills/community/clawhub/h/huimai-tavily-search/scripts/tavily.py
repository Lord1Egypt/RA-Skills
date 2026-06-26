#!/usr/bin/env python3
"""
Tavily API CLI helper for Hermes skills.

Dependency-free (Python stdlib only) and prints JSON to stdout.
Designed to be called via the Hermes terminal tool from the tavily skill.
"""

from __future__ import annotations

import argparse
import json
from os import environ as _environ
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, NoReturn, Optional


TAVILY_API_BASE_URL = "https://api.tavily.com"


def _die(msg: str, *, code: int = 2) -> NoReturn:
    print(json.dumps({"success": False, "error": msg}, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def _headers() -> Dict[str, str]:
    # Only read the single intended credential from the environment.
    api_key = _environ.get("TAVILY_API_KEY")
    if not api_key:
        _die("TAVILY_API_KEY environment variable not set")
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "hermes-skill-tavily/1.0",
    }


def _try_parse_json(raw: bytes) -> Dict[str, Any]:
    text = raw.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(text)
    except Exception:
        return {"raw": text}

    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}


def _request(method: str, path: str, *, json_body: Optional[dict] = None, http_timeout: float = 60.0) -> Dict[str, Any]:
    # Hardcode the API host to prevent exfil via injected base URL overrides.
    url = f"{TAVILY_API_BASE_URL}{path}"
    headers = _headers()
    data = None
    if json_body is not None:
        headers = dict(headers)
        headers["Content-Type"] = "application/json"
        data = json.dumps(json_body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=http_timeout) as resp:
            final_url = resp.geturl()
            if not final_url.startswith(TAVILY_API_BASE_URL + "/"):
                _die(f"Unexpected redirect: {final_url}", code=1)
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raw = e.read()
        payload = _try_parse_json(raw)
        _die(f"HTTP {e.code}: {payload}", code=1)
    except urllib.error.URLError as e:
        _die(f"Request failed: {e.reason}", code=1)
    except Exception as e:
        _die(f"Request failed: {type(e).__name__}: {e}", code=1)

    return _try_parse_json(raw)


def _print(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _parse_csv(value: Optional[str]) -> Optional[List[str]]:
    if not value:
        return None
    items = [x.strip() for x in value.split(",") if x.strip()]
    return items or None


def _parse_bool_or_enum(value: str, *, true_values: set[str], false_values: set[str]) -> Any:
    v = value.strip().lower()
    if v in false_values:
        return False
    if v in true_values:
        return True
    return value


def cmd_search(args: argparse.Namespace) -> None:
    payload: Dict[str, Any] = {
        "query": args.query,
        "max_results": args.max_results,
        "search_depth": args.search_depth,
        "topic": args.topic,
    }

    if args.chunks_per_source is not None:
        payload["chunks_per_source"] = args.chunks_per_source
    if args.time_range:
        payload["time_range"] = args.time_range
    if args.start_date:
        payload["start_date"] = args.start_date
    if args.end_date:
        payload["end_date"] = args.end_date

    include_answer = _parse_bool_or_enum(
        args.include_answer,
        true_values={"true", "1", "yes"},
        false_values={"false", "0", "no"},
    )
    if include_answer is not False:
        payload["include_answer"] = include_answer

    include_raw_content = _parse_bool_or_enum(
        args.include_raw_content,
        true_values={"true", "1", "yes"},
        false_values={"false", "0", "no"},
    )
    if include_raw_content is not False:
        payload["include_raw_content"] = include_raw_content

    if args.include_image_descriptions:
        payload["include_images"] = True
        payload["include_image_descriptions"] = True
    elif args.include_images:
        payload["include_images"] = True

    if args.include_favicon:
        payload["include_favicon"] = True

    if args.country:
        payload["country"] = args.country

    if args.auto_parameters:
        payload["auto_parameters"] = True
    if args.exact_match:
        payload["exact_match"] = True
    if args.include_usage:
        payload["include_usage"] = True

    if (include_domains := _parse_csv(args.include_domains)) is not None:
        payload["include_domains"] = include_domains
    if (exclude_domains := _parse_csv(args.exclude_domains)) is not None:
        payload["exclude_domains"] = exclude_domains

    data = _request("POST", "/search", json_body=payload, http_timeout=args.http_timeout)
    _print(data)


def cmd_extract(args: argparse.Namespace) -> None:
    urls: List[str] = []
    if args.url:
        urls.extend(args.url)
    if args.urls:
        urls.extend([u.strip() for u in args.urls.split(",") if u.strip()])
    if not urls:
        _die("extract requires --url or --urls")

    payload: Dict[str, Any] = {
        "urls": urls if len(urls) > 1 else urls[0],
        "format": args.format,
        "extract_depth": args.extract_depth,
    }
    if args.query:
        payload["query"] = args.query
    if args.chunks_per_source is not None:
        payload["chunks_per_source"] = args.chunks_per_source
    if args.include_images:
        payload["include_images"] = True
    if args.include_favicon:
        payload["include_favicon"] = True
    if args.timeout_seconds is not None:
        payload["timeout"] = float(args.timeout_seconds)
    if args.include_usage:
        payload["include_usage"] = True

    data = _request("POST", "/extract", json_body=payload, http_timeout=args.http_timeout)
    _print(data)


def cmd_research_get(args: argparse.Namespace) -> None:
    data = _request("GET", f"/research/{args.request_id}", http_timeout=args.http_timeout)
    _print(data)


def cmd_research(args: argparse.Namespace) -> None:
    payload: Dict[str, Any] = {
        "input": args.input,
        "model": args.model,
        "citation_format": args.citation_format,
        "stream": False,
    }

    if args.output_schema_json:
        try:
            payload["output_schema"] = json.loads(args.output_schema_json)
        except Exception as e:
            _die(f"Failed to parse --output-schema-json: {e}")

    queued = _request("POST", "/research", json_body=payload, http_timeout=args.http_timeout)
    request_id = queued.get("request_id")

    if args.no_wait or not request_id:
        _print(queued)
        return

    deadline = time.monotonic() + float(args.max_wait_seconds)
    last: Dict[str, Any] = queued
    while time.monotonic() < deadline:
        status = _request("GET", f"/research/{request_id}", http_timeout=args.http_timeout)
        last = status
        if status.get("status") in ("completed", "failed"):
            _print(status)
            return
        time.sleep(float(args.poll_interval_seconds))

    last = dict(last)
    last["timed_out"] = True
    _print(last)


def cmd_usage(args: argparse.Namespace) -> None:
    data = _request("GET", "/usage", http_timeout=args.http_timeout)
    _print(data)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tavily.py", description="Call Tavily APIs (Search/Extract/Research) and print JSON.")
    p.add_argument("--http-timeout", type=float, default=60.0, help="HTTP timeout in seconds (default: 60)")

    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search", help="POST /search")
    sp.add_argument("--query", required=True, help="Search query")
    sp.add_argument("--max-results", type=int, default=5, help="Max results (default: 5)")
    sp.add_argument("--search-depth", choices=["basic", "advanced", "fast", "ultra-fast"], default="basic")
    sp.add_argument("--chunks-per-source", type=int, choices=[1, 2, 3], default=None)
    sp.add_argument("--topic", choices=["general", "news", "finance"], default="general")
    sp.add_argument("--time-range", choices=["day", "week", "month", "year", "d", "w", "m", "y"], default=None)
    sp.add_argument("--start-date", default=None, help="YYYY-MM-DD")
    sp.add_argument("--end-date", default=None, help="YYYY-MM-DD")
    sp.add_argument("--include-answer", default="false", help="false|true|basic|advanced (default: false)")
    sp.add_argument("--include-raw-content", default="false", help="false|true|markdown|text (default: false)")
    sp.add_argument("--include-images", action="store_true", help="Include image results")
    sp.add_argument("--include-image-descriptions", action="store_true", help="Include image descriptions (implies --include-images)")
    sp.add_argument("--include-favicon", action="store_true")
    sp.add_argument("--include-domains", default=None, help="Comma-separated allowlist domains")
    sp.add_argument("--exclude-domains", default=None, help="Comma-separated blocklist domains")
    sp.add_argument("--country", default=None, help="Boost results for a country (general topic only)")
    sp.add_argument("--auto-parameters", action="store_true")
    sp.add_argument("--exact-match", action="store_true")
    sp.add_argument("--include-usage", action="store_true")
    sp.set_defaults(func=cmd_search)

    ep = sub.add_parser("extract", help="POST /extract")
    ep.add_argument("--url", action="append", help="URL to extract (repeatable)")
    ep.add_argument("--urls", default=None, help="Comma-separated URLs to extract")
    ep.add_argument("--query", default=None, help="Intent for reranking extracted chunks")
    ep.add_argument("--chunks-per-source", type=int, choices=[1, 2, 3, 4, 5], default=None)
    ep.add_argument("--extract-depth", choices=["basic", "advanced"], default="basic")
    ep.add_argument("--format", choices=["markdown", "text"], default="markdown")
    ep.add_argument("--include-images", action="store_true")
    ep.add_argument("--include-favicon", action="store_true")
    ep.add_argument("--timeout-seconds", type=float, default=None, help="Tavily extract timeout (1-60)")
    ep.add_argument("--include-usage", action="store_true")
    ep.set_defaults(func=cmd_extract)

    rp = sub.add_parser("research", help="POST /research then poll GET /research/{request_id}")
    rp.add_argument("--input", required=True, help="Research task/prompt")
    rp.add_argument("--model", choices=["mini", "pro", "auto"], default="auto")
    rp.add_argument("--citation-format", choices=["numbered", "mla", "apa", "chicago"], default="numbered")
    rp.add_argument("--output-schema-json", default=None, help="JSON schema string for structured output (no file reads)")
    rp.add_argument("--no-wait", action="store_true", help="Only create task, do not poll")
    rp.add_argument("--max-wait-seconds", type=float, default=180.0, help="Max time to poll (default: 180)")
    rp.add_argument("--poll-interval-seconds", type=float, default=2.0, help="Poll interval (default: 2)")
    rp.set_defaults(func=cmd_research)

    rgp = sub.add_parser("research-get", help="GET /research/{request_id}")
    rgp.add_argument("--request-id", required=True)
    rgp.set_defaults(func=cmd_research_get)

    up = sub.add_parser("usage", help="GET /usage")
    up.set_defaults(func=cmd_usage)

    return p


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
