#!/usr/bin/env python3
"""
fetch_page.py - Web scraping helper for OpenRouter pages.

Effective strategy:
  Layer 1: requests (preferred, stable, fast)
  Layer 2: urllib fallback

This helper intentionally avoids pretending to call OpenClaw tools from a plain
Python script. Tool-driven fetches belong in agent runs, not local subprocess
shims.
"""

import sys
from typing import Optional, Tuple
from urllib.error import URLError
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"


def fetch_with_requests(url: str, timeout: int = 15) -> Tuple[bool, str]:
    """Layer 1: Direct HTTP request with requests library."""
    try:
        import requests

        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=timeout)

        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"

        return True, resp.text
    except ImportError as e:
        return False, f"requests not installed: {e}"
    except Exception as e:
        return False, f"requests failed: {e}"


def fetch_with_urllib(url: str, timeout: int = 20) -> Tuple[bool, str]:
    """Layer 2: Standard-library urllib fallback."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            if status != 200:
                return False, f"HTTP {status}"
            return True, resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        return False, f"urllib failed: {e}"
    except Exception as e:
        return False, f"urllib error: {e}"


def fetch_page(url: str, verbose: bool = False) -> Optional[str]:
    """Fetch page content with a small, honest fallback chain."""
    if verbose:
        print(f"Fetching: {url}")

    success, content = fetch_with_requests(url)
    if success:
        if verbose:
            print("  ✓ Layer 1 (requests) succeeded")
        return content
    if verbose:
        print(f"  ✗ Layer 1 (requests) failed: {content}")

    success, content = fetch_with_urllib(url)
    if success:
        if verbose:
            print("  ✓ Layer 2 (urllib) succeeded")
        return content
    if verbose:
        print(f"  ✗ Layer 2 (urllib) failed: {content}")

    print(f"ERROR: All fetch methods failed for {url}", file=sys.stderr)
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_page.py <url> [--verbose]")
        sys.exit(1)

    url = sys.argv[1]
    verbose = "--verbose" in sys.argv

    content = fetch_page(url, verbose)
    if content:
        print(content[:1000])
    else:
        sys.exit(1)
