#!/usr/bin/env python3
"""
Pangolin Google SERP & AI Mode API Client

Zero-dependency Python client for Pangolin's Google SERP and AI Mode APIs.
Supports AI Mode search (Google AI Overviews), standard SERP results,
multi-turn dialogue, and screenshot capture.

Usage:
    pangolin.py --q "quantum computing"
    pangolin.py --q "best databases 2025" --mode serp --screenshot
    pangolin.py --q "kubernetes" --follow-up "how to deploy"
    pangolin.py --auth-only

Environment:
    PANGOLIN_API_KEY  - API Key (skips login)
    PANGOLIN_EMAIL    - Account email (for login)
    PANGOLIN_PASSWORD - Account password (for login)
"""

import argparse
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Fix Windows / macOS console encoding for Unicode output
# ---------------------------------------------------------------------------
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace"
    )
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding="utf-8", errors="replace"
    )

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_BASE = "https://scrapeapi.pangolinfo.com"
AUTH_ENDPOINT = f"{API_BASE}/api/v1/auth"
SCRAPE_V1_ENDPOINT = f"{API_BASE}/api/v1/scrape"
SCRAPE_V2_ENDPOINT = f"{API_BASE}/api/v2/scrape"
API_KEY_CACHE_PATH = Path.home() / ".pangolin_api_key"

EXIT_SUCCESS = 0
EXIT_API_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_NETWORK_ERROR = 3
EXIT_AUTH_ERROR = 4


# ---------------------------------------------------------------------------
# Unified error helper
# ---------------------------------------------------------------------------
def _emit_error(code, message, hint=None, exit_code=None):
    """Print a structured error envelope to stderr and optionally exit.

    NEVER include API keys, passwords, or cookies in error output.
    """
    envelope = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if hint:
        envelope["error"]["hint"] = hint
    print(json.dumps(envelope), file=sys.stderr)
    if exit_code is not None:
        sys.exit(exit_code)


# ---------------------------------------------------------------------------
# API key caching
# ---------------------------------------------------------------------------
def load_cached_api_key():
    """Load API key from cache file if it exists."""
    if API_KEY_CACHE_PATH.exists():
        api_key = API_KEY_CACHE_PATH.read_text().strip()
        if api_key and len(api_key.split(".")) == 3:  # Basic JWT format check
            return api_key
    return None


def save_cached_api_key(api_key):
    """Save API key to cache file."""
    API_KEY_CACHE_PATH.write_text(api_key)
    try:
        API_KEY_CACHE_PATH.chmod(0o600)
    except OSError:
        pass
    # Windows: restrict file access to current user
    if sys.platform == "win32":
        try:
            import subprocess
            subprocess.run(
                ["icacls", str(API_KEY_CACHE_PATH), "/inheritance:r",
                 "/grant:r", f"{os.environ.get('USERNAME', '')}:F"],
                capture_output=True, check=False,
            )
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def authenticate(email, password):
    """Authenticate with Pangolin API and return an API key."""
    body = json.dumps({"email": email, "password": password}).encode()
    req = urllib.request.Request(
        AUTH_ENDPOINT,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as e:
        # Improvement 1: macOS SSL certificate handling
        if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
            _emit_error(
                "SSL_CERT",
                "SSL certificate verification failed",
                hint=(
                    "macOS users: run '/Applications/Python 3.x/Install Certificates.command' "
                    "or set SSL_CERT_FILE env var. "
                    "See: python3 -c \"import certifi; print(certifi.where())\""
                ),
                exit_code=EXIT_NETWORK_ERROR,
            )
        _emit_error(
            "NETWORK",
            "Network error during authentication",
            hint="Check your internet connection and try again.",
            exit_code=EXIT_NETWORK_ERROR,
        )

    if result.get("code") != 0:
        _emit_error(
            "AUTH_FAILED",
            "Authentication failed",
            hint="Verify PANGOLIN_EMAIL and PANGOLIN_PASSWORD are correct.",
            exit_code=EXIT_AUTH_ERROR,
        )

    api_key = result["data"]
    save_cached_api_key(api_key)
    return api_key


def get_api_key():
    """Resolve API key from env var, cache file, or fresh login."""
    api_key = os.environ.get("PANGOLIN_API_KEY")
    if api_key:
        save_cached_api_key(api_key)  # Cache for future calls without env var
        return api_key

    api_key = load_cached_api_key()
    if api_key:
        return api_key

    email = os.environ.get("PANGOLIN_EMAIL")
    password = os.environ.get("PANGOLIN_PASSWORD")
    if not email or not password:
        _emit_error(
            "MISSING_ENV",
            "No authentication credentials found.",
            hint=(
                "Set PANGOLIN_API_KEY, or both PANGOLIN_EMAIL and PANGOLIN_PASSWORD "
                "environment variables."
            ),
            exit_code=EXIT_AUTH_ERROR,
        )

    return authenticate(email, password)


def refresh_api_key():
    """Force re-authentication using email/password."""
    email = os.environ.get("PANGOLIN_EMAIL")
    password = os.environ.get("PANGOLIN_PASSWORD")
    if not email or not password:
        _emit_error(
            "MISSING_ENV",
            "Cannot refresh API key without credentials.",
            hint="Set PANGOLIN_EMAIL and PANGOLIN_PASSWORD environment variables.",
            exit_code=EXIT_AUTH_ERROR,
        )
    return authenticate(email, password)



# ---------------------------------------------------------------------------
# Request building (Google only)
# ---------------------------------------------------------------------------
def build_google_body(query, mode, screenshot, follow_ups, num, region=None):
    """Build request body for Google SERP / AI Mode APIs."""
    if mode == "ai-mode":
        url = (
            f"https://www.google.com/search?num={num}&udm=50"
            f"&q={urllib.parse.quote_plus(query)}"
        )
        body = {
            "url": url,
            "parserName": "googleAISearch",
        }
    else:
        url = (
            f"https://www.google.com/search?num={num}"
            f"&q={urllib.parse.quote_plus(query)}"
        )
        body = {
            "url": url,
            "parserName": "googleSearch",
            "format": "json",
            "scrapeContext": {
                "resultNum": num,
            },
        }
        if region:
            body["scrapeContext"]["region"] = region

    if screenshot:
        body["screenshot"] = True

    if follow_ups:
        body["param"] = follow_ups

    return body


# ---------------------------------------------------------------------------
# API call with retry
# ---------------------------------------------------------------------------
def call_api(api_key, body, endpoint, max_retries=3, timeout=120):
    """Call the scrape API with retry and exponential backoff."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Pangolin-CLI/1.0",
    }
    payload = json.dumps(body).encode()

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            if e.code == 429:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                _emit_error(
                    "RATE_LIMIT",
                    "Rate limited by API server.",
                    hint="Wait a moment and retry, or reduce request frequency.",
                    exit_code=EXIT_NETWORK_ERROR,
                )
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            _emit_error(
                "API_ERROR",
                f"HTTP {e.code} from API.",
                hint="Check your request parameters and try again.",
                exit_code=EXIT_NETWORK_ERROR,
            )
        except urllib.error.URLError as e:
            # Improvement 1: macOS SSL certificate handling
            if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
                _emit_error(
                    "SSL_CERT",
                    "SSL certificate verification failed",
                    hint=(
                        "macOS users: run '/Applications/Python 3.x/Install Certificates.command' "
                        "or set SSL_CERT_FILE env var. "
                        "See: python3 -c \"import certifi; print(certifi.where())\""
                    ),
                    exit_code=EXIT_NETWORK_ERROR,
                )
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            _emit_error(
                "NETWORK",
                "Network error communicating with API.",
                hint="Check your internet connection and try again.",
                exit_code=EXIT_NETWORK_ERROR,
            )

    return None


# ---------------------------------------------------------------------------
# Response handling
# ---------------------------------------------------------------------------
def handle_response(result, api_key, body, endpoint, timeout=120):
    """Handle API response, retrying auth on 1004 error."""
    if result.get("code") == 1004:
        new_api_key = refresh_api_key()
        return call_api(new_api_key, body, endpoint, timeout=timeout)
    return result


def extract_google_output(result):
    """Extract structured output from Google SERP / AI Mode API response."""
    code = result.get("code")
    if code != 0:
        return {
            "success": False,
            "error": {
                "code": "API_ERROR",
                "message": result.get("message", "Unknown API error"),
                "hint": f"Pangolin API returned error code {code}. See references/error-codes.md.",
            },
        }

    data = result.get("data", {})
    output = {
        "success": True,
        "task_id": data.get("taskId"),
        "results_num": data.get("results_num", 0),
        "ai_overview_count": data.get("ai_overview", 0),
    }

    json_data = data.get("json", {})

    # v1 (SERP) returns json as array: [{code, data: {items: [...]}}]
    # v2 (AI Mode) returns json as object: {items: [...]}
    if isinstance(json_data, list) and len(json_data) > 0:
        inner = json_data[0]
        items = inner.get("data", {}).get("items", [])
    elif isinstance(json_data, dict):
        items = json_data.get("items", [])
    else:
        items = []

    ai_overviews = []
    organic_results = []

    for item in items:
        item_type = item.get("type")
        if item_type == "ai_overview":
            overview = {"content": [], "references": []}
            for sub in item.get("items", []):
                if sub.get("type") == "ai_overview_elem":
                    overview["content"].extend(sub.get("content", []))
            for ref in item.get("references", []):
                overview["references"].append({
                    "title": ref.get("title"),
                    "url": ref.get("url"),
                    "domain": ref.get("domain"),
                })
            ai_overviews.append(overview)
        elif item_type == "organic":
            for sub in item.get("items", []):
                organic_results.append({
                    "title": sub.get("title"),
                    "url": sub.get("url"),
                    "text": sub.get("text"),
                })

    if ai_overviews:
        output["ai_overview"] = ai_overviews
        output["ai_overview_count"] = len(ai_overviews)
    if organic_results:
        output["organic_results"] = organic_results
        output["results_num"] = len(organic_results)

    screenshot_url = data.get("screenshot")
    if screenshot_url:
        output["screenshot"] = screenshot_url

    return output


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Pangolin Google SERP & AI Mode API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # AI Mode search (default)\n"
            '  python3 scripts/pangolin.py --q "what is quantum computing"\n'
            "\n"
            "  # Standard SERP with screenshot\n"
            '  python3 scripts/pangolin.py --q "best databases 2025" --mode serp --screenshot\n'
            "\n"
            "  # Multi-turn follow-up\n"
            '  python3 scripts/pangolin.py --q "kubernetes" --follow-up "how to deploy" '
            '--follow-up "monitoring tools"\n'
            "\n"
            "  # Auth check\n"
            "  python3 scripts/pangolin.py --auth-only\n"
            "\n"
            "Environment variables:\n"
            "  PANGOLIN_API_KEY    API Key (skips login)\n"
            "  PANGOLIN_EMAIL      Account email\n"
            "  PANGOLIN_PASSWORD   Account password\n"
        ),
    )
    parser.add_argument("--q", dest="query", help="Search query")
    parser.add_argument(
        "--mode",
        choices=["ai-mode", "serp"],
        default="ai-mode",
        help="API mode: ai-mode (default) | serp",
    )
    parser.add_argument(
        "--screenshot", action="store_true", help="Capture page screenshot"
    )
    parser.add_argument(
        "--follow-up",
        action="append",
        dest="follow_ups",
        help=(
            "Follow-up question for multi-turn (ai-mode only). "
            "Can be repeated. >5 may slow response."
        ),
    )
    parser.add_argument(
        "--num",
        type=int,
        default=10,
        help="Number of results (default: 10)",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="Geographic region for SERP results (e.g., us, uk). SERP mode only.",
    )
    parser.add_argument(
        "--auth-only",
        action="store_true",
        help="Only authenticate and print API key info",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw API response instead of extracted data",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="API request timeout in seconds (default: 120)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.query and not args.auth_only:
        parser.error("--q is required unless using --auth-only")

    if args.follow_ups and args.mode != "ai-mode":
        parser.error("--follow-up is only supported in ai-mode")

    if args.follow_ups and len(args.follow_ups) > 5:
        print(json.dumps({"warning": f"Using {len(args.follow_ups)} follow-ups (>5). Response may be slower."}), file=sys.stderr)

    # Authenticate
    api_key = get_api_key()

    if args.auth_only:
        print(json.dumps({
            "success": True,
            "message": "Authentication successful",
            "api_key_preview": (
                f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            ),
        }, indent=2))
        sys.exit(EXIT_SUCCESS)

    # Build request
    body = build_google_body(
        args.query, args.mode, args.screenshot, args.follow_ups, args.num,
        region=args.region,
    )
    if args.mode == "ai-mode":
        endpoint = SCRAPE_V2_ENDPOINT
    else:
        endpoint = SCRAPE_V1_ENDPOINT

    # Call API
    result = call_api(api_key, body, endpoint, timeout=args.timeout)

    if result is None:
        _emit_error(
            "NETWORK",
            "API call failed after retries.",
            hint="Check your internet connection and try again.",
            exit_code=EXIT_NETWORK_ERROR,
        )

    result = handle_response(result, api_key, body, endpoint, timeout=args.timeout)

    if result is None:
        _emit_error(
            "NETWORK",
            "API call failed after API key refresh.",
            hint="Check your internet connection and try again.",
            exit_code=EXIT_NETWORK_ERROR,
        )

    # Output
    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        output = extract_google_output(result)
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if result.get("code") != 0:
        sys.exit(EXIT_API_ERROR)

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
