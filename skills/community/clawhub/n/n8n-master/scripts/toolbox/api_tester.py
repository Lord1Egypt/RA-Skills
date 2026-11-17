#!/usr/bin/env python3
"""Small standard-library HTTP tester for n8n workflow prototyping."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any

from _common import (
    ToolboxError,
    die,
    json_dumps,
    load_json_arg,
    load_text_arg,
    merge_query,
    parse_json_maybe,
    redact,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lightweight Postman-style HTTP tester with redacted output.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--method", default="GET", help="HTTP method")
    parser.add_argument("--url", required=True, help="Request URL")
    parser.add_argument(
        "--headers",
        help='Headers JSON object, or @file. Example: \'{"Authorization":"Bearer ..."}\'',
    )
    parser.add_argument(
        "--query",
        help='Query JSON object, or @file. Lists become repeated parameters.',
    )
    body_group = parser.add_mutually_exclusive_group()
    body_group.add_argument("--body-json", help="JSON request body, or @file")
    body_group.add_argument("--body-raw", help="Raw request body string, or @file")
    body_group.add_argument("--body-file", help="Read raw request body from a file")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout seconds")
    parser.add_argument(
        "--max-body-chars",
        type=int,
        default=12000,
        help="Maximum response body characters to print",
    )
    parser.add_argument(
        "--output",
        choices=("summary", "json"),
        default="summary",
        help="Output format",
    )
    parser.add_argument(
        "--print-n8n-config",
        action="store_true",
        help="Print a redacted n8n HTTP Request node parameter draft",
    )
    parser.add_argument(
        "--n8n-config-out",
        help="Write the redacted n8n HTTP Request config draft to this file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the redacted request without sending it",
    )
    return parser


def normalize_headers(raw: Any) -> dict[str, str]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ToolboxError("--headers must decode to a JSON object")
    return {str(key): str(value) for key, value in raw.items()}


def prepare_body(args: argparse.Namespace, headers: dict[str, str]) -> tuple[bytes | None, Any, str | None]:
    if args.body_json is not None:
        parsed = load_json_arg(args.body_json, "--body-json")
        headers.setdefault("Content-Type", "application/json")
        return json.dumps(parsed, ensure_ascii=False).encode("utf-8"), parsed, "json"
    if args.body_raw is not None:
        raw = load_text_arg(args.body_raw, "--body-raw")
        return raw.encode("utf-8"), raw, "raw"
    if args.body_file is not None:
        with open(args.body_file, "rb") as handle:
            raw_bytes = handle.read()
        try:
            raw_preview: Any = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raw_preview = f"<{len(raw_bytes)} binary bytes>"
        return raw_bytes, raw_preview, "raw"
    return None, None, None


def make_n8n_config(
    method: str,
    url: str,
    headers: dict[str, str],
    query: dict[str, Any],
    body_preview: Any,
    body_mode: str | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "method": method.upper(),
        "url": url,
        "options": {},
    }
    if headers:
        params["sendHeaders"] = True
        params["headerParameters"] = {
            "parameters": [
                {"name": key, "value": redact(value, key)}
                for key, value in headers.items()
            ]
        }
    if query:
        params["sendQuery"] = True
        params["queryParameters"] = {
            "parameters": [
                {"name": str(key), "value": redact(value, str(key))}
                for key, value in query.items()
            ]
        }
    if body_mode:
        params["sendBody"] = True
        if body_mode == "json":
            params["contentType"] = "json"
            params["jsonBody"] = redact(body_preview)
        else:
            params["contentType"] = "raw"
            params["rawBody"] = redact(body_preview)
    return {
        "node_type": "n8n-nodes-base.httpRequest",
        "parameters": params,
        "note": "Sensitive values are redacted. Replace them with n8n credentials or expressions before use.",
    }


def run(args: argparse.Namespace) -> int:
    method = args.method.upper()
    headers = normalize_headers(load_json_arg(args.headers, "--headers", default={}))
    query = load_json_arg(args.query, "--query", default={})
    if not isinstance(query, dict):
        raise ToolboxError("--query must decode to a JSON object")
    url = merge_query(args.url, query)
    body_bytes, body_preview, body_mode = prepare_body(args, headers)

    redacted_request = {
        "method": method,
        "url": redact(url),
        "headers": redact(headers),
        "query": redact(query),
        "body": redact(body_preview),
        "timeout": args.timeout,
    }

    n8n_config = make_n8n_config(method, args.url, headers, query, body_preview, body_mode)
    if args.print_n8n_config or args.n8n_config_out:
        write_text(args.n8n_config_out, json_dumps(n8n_config))

    if args.dry_run:
        print(json_dumps({"dry_run": True, "request": redacted_request}))
        return 0

    req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            status = response.status
            reason = response.reason
            response_headers = dict(response.headers.items())
            raw_body = response.read()
    except urllib.error.HTTPError as exc:
        status = exc.code
        reason = exc.reason
        response_headers = dict(exc.headers.items())
        raw_body = exc.read()
    except urllib.error.URLError as exc:
        raise ToolboxError(f"request failed: {exc.reason}") from exc
    elapsed_ms = round((time.monotonic() - started) * 1000)

    text_body = raw_body.decode("utf-8", errors="replace")
    truncated = len(text_body) > args.max_body_chars
    if truncated:
        text_body = text_body[: args.max_body_chars] + "\n<truncated>"
    parsed_body = parse_json_maybe(text_body)
    redacted_body = redact(parsed_body)

    result = {
        "request": redacted_request,
        "response": {
            "status": status,
            "reason": reason,
            "elapsed_ms": elapsed_ms,
            "headers": redact(response_headers),
            "body": redacted_body,
            "truncated": truncated,
        },
    }
    if args.output == "json":
        print(json_dumps(result))
    else:
        print(f"{method} {redact(url)}")
        print(f"status: {status} {reason} ({elapsed_ms} ms)")
        print("response_headers:")
        print(json_dumps(redact(response_headers)))
        print("response_body:")
        if isinstance(redacted_body, (dict, list)):
            print(json_dumps(redacted_body))
        else:
            print(redacted_body)
    return 0 if 200 <= status < 400 else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except ToolboxError as exc:
        die(str(exc))
    except KeyboardInterrupt:
        die("interrupted", 130)
    return 1


if __name__ == "__main__":
    sys.exit(main())
