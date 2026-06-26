#!/usr/bin/env python3
"""
Extract main content text from HTML — by URL, file path, or stdin.

Designed to feed cleaner text into downstream tools (e.g. readability_check.py).
Uses trafilatura for content extraction.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from urllib.parse import urlparse


REQUIRED_PACKAGES = {
    "trafilatura": "trafilatura",
}


def warn(msg: str) -> None:
    print(msg, file=sys.stderr)


def ensure_dependencies() -> None:
    """Install any required packages that are missing."""
    missing = [
        pip_name
        for module, pip_name in REQUIRED_PACKAGES.items()
        if importlib.util.find_spec(module) is None
    ]
    if not missing:
        return
    warn(f"Installing missing packages: {', '.join(missing)}...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing, "--break-system-packages"]
        )
    except subprocess.CalledProcessError:
        # --break-system-packages may not be supported (e.g. macOS, older pip). Retry without it.
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", *missing]
            )
        except subprocess.CalledProcessError:
            warn(f"Failed to install: {', '.join(missing)}")
            sys.exit(1)


def looks_like_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def fetch_html(url: str) -> str:
    import trafilatura
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        warn(f"Error: failed to fetch {url}")
        sys.exit(1)
    return downloaded


def extract(html: str, url: str | None, output_format: str) -> str:
    import trafilatura
    text = trafilatura.extract(
        html,
        url=url,
        output_format=output_format,
        include_comments=False,
        include_tables=True,
        favor_precision=False,
        with_metadata=(output_format == "json"),
    )
    if not text:
        warn("Error: no extractable content found")
        sys.exit(1)
    return text


def read_input(source: str) -> tuple[str, str | None]:
    """Return (html, source_url). source_url is set only when input was a URL."""
    if source == "-":
        return sys.stdin.read(), None
    if looks_like_url(source):
        warn(f"Fetching {source}...")
        return fetch_html(source), source
    try:
        with open(source, encoding="utf-8") as f:
            return f.read(), None
    except OSError as e:
        warn(f"Error: cannot read file {source}: {e}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract main content from an HTML page (URL, file, or stdin)."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="URL, file path, or '-' for stdin HTML (default: stdin)",
    )
    parser.add_argument(
        "--format",
        choices=("txt", "markdown", "json"),
        default="txt",
        help="Output format (default: txt)",
    )
    args = parser.parse_args()

    html, source_url = read_input(args.input)
    if not html.strip():
        warn("Error: input is empty")
        sys.exit(1)

    print(extract(html, url=source_url, output_format=args.format))


if __name__ == "__main__":
    ensure_dependencies()
    main()
