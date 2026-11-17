#!/usr/bin/env python3
"""Ingest URL markdown through Firecrawl into a local source directory."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import sys
import urllib.parse
from typing import Any

from _common import (
    ToolboxError,
    die,
    json_dumps,
    load_json_arg,
    redact,
    request_json,
    require_env,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch one or more URLs with Firecrawl and save Markdown plus manifest.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("urls", nargs="+", help="URLs to scrape")
    parser.add_argument("--source-dir", required=True, help="Directory to write markdown files and manifest")
    parser.add_argument(
        "--endpoint",
        default="https://api.firecrawl.dev/v2/scrape",
        help="Firecrawl scrape endpoint. Override for self-hosted or older API shapes.",
    )
    parser.add_argument(
        "--formats-json",
        default='["markdown"]',
        help='Firecrawl formats JSON. Example: \'["markdown","html"]\'',
    )
    parser.add_argument(
        "--request-json",
        help="Extra JSON object merged into each Firecrawl request body, or @file",
    )
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout seconds")
    parser.add_argument("--manifest", default="manifest.json", help="Manifest filename inside source-dir")
    parser.add_argument("--dry-run", action="store_true", help="Validate planned requests without network or writes")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing markdown files")
    return parser


def slugify_url(url: str, index: int) -> str:
    parsed = urllib.parse.urlsplit(url)
    base = (parsed.netloc + parsed.path).strip("/") or "page"
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-").lower()
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{index:03d}-{base[:80]}-{digest}.md"


def extract_markdown(response: Any) -> tuple[str, dict[str, Any]]:
    if not isinstance(response, dict):
        raise ToolboxError("Firecrawl response was not a JSON object")
    candidates = [
        response.get("markdown"),
        response.get("content"),
    ]
    data = response.get("data")
    if isinstance(data, dict):
        candidates.extend([data.get("markdown"), data.get("content")])
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            metadata = {}
            if isinstance(data, dict) and isinstance(data.get("metadata"), dict):
                metadata = data["metadata"]
            elif isinstance(response.get("metadata"), dict):
                metadata = response["metadata"]
            return candidate, metadata
    raise ToolboxError(
        "Could not find markdown/content in Firecrawl response. "
        f"Response shape: {json_dumps(redact(response))[:1200]}"
    )


def make_request_body(url: str, formats: Any, extra: dict[str, Any]) -> dict[str, Any]:
    body = {"url": url, "formats": formats}
    body.update(extra)
    body["url"] = url
    return body


def run(args: argparse.Namespace) -> int:
    formats = load_json_arg(args.formats_json, "--formats-json")
    if not isinstance(formats, list):
        raise ToolboxError("--formats-json must decode to a JSON array")
    extra = load_json_arg(args.request_json, "--request-json", default={})
    if not isinstance(extra, dict):
        raise ToolboxError("--request-json must decode to a JSON object")

    planned = []
    for index, url in enumerate(args.urls, 1):
        planned.append(
            {
                "url": url,
                "endpoint": args.endpoint,
                "request_body": redact(make_request_body(url, formats, extra)),
                "output_file": slugify_url(url, index),
            }
        )
    if args.dry_run:
        print(json_dumps({"dry_run": True, "planned": planned}))
        return 0

    api_key = require_env("FIRECRAWL_API_KEY")
    os.makedirs(args.source_dir, exist_ok=True)
    manifest_entries = []
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    for index, url in enumerate(args.urls, 1):
        filename = slugify_url(url, index)
        output_path = os.path.join(args.source_dir, filename)
        if os.path.exists(output_path) and not args.overwrite:
            raise ToolboxError(f"output exists, pass --overwrite to replace: {output_path}")
        body = make_request_body(url, formats, extra)
        response = request_json(
            "POST",
            args.endpoint,
            headers={"Authorization": f"Bearer {api_key}"},
            payload=body,
            timeout=args.timeout,
        )
        markdown, metadata = extract_markdown(response)
        write_text(output_path, markdown.rstrip() + "\n")
        manifest_entries.append(
            {
                "url": url,
                "file": filename,
                "fetched_at": now,
                "endpoint": args.endpoint,
                "formats": formats,
                "metadata": redact(metadata),
                "sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
            }
        )
    manifest = {
        "generated_at": now,
        "tool": "firecrawl_ingest_docs.py",
        "entries": manifest_entries,
        "note": "API keys and authorization headers are intentionally omitted.",
    }
    write_text(os.path.join(args.source_dir, args.manifest), json_dumps(manifest) + "\n")
    print(json_dumps({"written": manifest_entries, "manifest": args.manifest}))
    return 0


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
