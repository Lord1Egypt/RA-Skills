#!/usr/bin/env python3
"""
Pangolin SERP & Scrape API Client

Zero-dependency Python client for Pangolin's Google SERP and Amazon APIs.
Supports AI Mode search, AI Overview SERP, Amazon product scraping,
multi-turn dialogue, and screenshot capture.

Usage:
    pangolin.py --q "query" [--mode ai-mode|serp|amazon] [--screenshot]
    pangolin.py --q "query" --mode ai-mode --follow-up "follow up question"
    pangolin.py --url "https://amazon.com/dp/..." --mode amazon
    pangolin.py --auth-only

Environment:
    PANGOLIN_TOKEN    - Bearer token (skips login)
    PANGOLIN_EMAIL    - Account email (for login)
    PANGOLIN_PASSWORD - Account password (for login)
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://scrapeapi.pangolinfo.com"
AUTH_ENDPOINT = f"{API_BASE}/api/v1/auth"
SCRAPE_V1_ENDPOINT = f"{API_BASE}/api/v1/scrape"
SCRAPE_V2_ENDPOINT = f"{API_BASE}/api/v2/scrape"
TOKEN_CACHE_PATH = Path.home() / ".pangolin_token"

EXIT_SUCCESS = 0
EXIT_API_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_NETWORK_ERROR = 3
EXIT_AUTH_ERROR = 4

AMAZON_PARSERS = [
    "amzProductDetail",
    "amzKeyword",
    "amzProductOfCategory",
    "amzProductOfSeller",
    "amzBestSellers",
    "amzNewReleases",
    "amzFollowSeller",
]


def load_cached_token():
    """Load token from cache file if it exists."""
    if TOKEN_CACHE_PATH.exists():
        token = TOKEN_CACHE_PATH.read_text().strip()
        if token:
            return token
    return None


def save_cached_token(token):
    """Save token to cache file."""
    TOKEN_CACHE_PATH.write_text(token)
    TOKEN_CACHE_PATH.chmod(0o600)


def authenticate(email, password):
    """Authenticate with Pangolin API and return a bearer token."""
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
        print(json.dumps({"error": f"Network error during auth: {e}"}), file=sys.stderr)
        sys.exit(EXIT_NETWORK_ERROR)

    if result.get("code") != 0:
        print(json.dumps({
            "error": "Authentication failed",
            "code": result.get("code"),
            "message": result.get("message"),
        }), file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)

    token = result["data"]
    save_cached_token(token)
    return token


def get_token():
    """Resolve token from env var, cache file, or fresh login."""
    token = os.environ.get("PANGOLIN_TOKEN")
    if token:
        return token

    token = load_cached_token()
    if token:
        return token

    email = os.environ.get("PANGOLIN_EMAIL")
    password = os.environ.get("PANGOLIN_PASSWORD")
    if not email or not password:
        print(json.dumps({
            "error": "No authentication credentials. Set PANGOLIN_TOKEN, or both PANGOLIN_EMAIL and PANGOLIN_PASSWORD.",
        }), file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)

    return authenticate(email, password)


def refresh_token():
    """Force re-authentication using email/password."""
    email = os.environ.get("PANGOLIN_EMAIL")
    password = os.environ.get("PANGOLIN_PASSWORD")
    if not email or not password:
        print(json.dumps({
            "error": "Cannot refresh token: PANGOLIN_EMAIL and PANGOLIN_PASSWORD required.",
        }), file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)
    return authenticate(email, password)


def build_google_body(query, mode, screenshot, follow_ups, num):
    """Build request body for Google SERP APIs."""
    if mode == "ai-mode":
        url = f"https://www.google.com/search?num={num}&udm=50&q={urllib.parse.quote_plus(query)}"
        body = {
            "url": url,
            "parserName": "googleAISearch",
        }
    else:
        url = f"https://www.google.com/search?num={num}&q={urllib.parse.quote_plus(query)}"
        body = {
            "url": url,
            "parserName": "googleSearch",
        }

    if screenshot:
        body["screenshot"] = True

    if follow_ups:
        body["param"] = follow_ups

    return body


def build_amazon_body(url, query, parser, zipcode, fmt):
    """Build request body for Amazon Scrape API."""
    if not url and query:
        url = f"https://www.amazon.com/s?k={urllib.parse.quote_plus(query)}"
        if parser == "amzProductDetail":
            parser = "amzKeyword"

    if not url:
        print(json.dumps({
            "error": "Amazon mode requires --url or --q",
        }), file=sys.stderr)
        sys.exit(EXIT_USAGE_ERROR)

    body = {
        "url": url,
        "format": fmt,
        "parserName": parser,
        "bizContext": {
            "zipcode": zipcode,
        },
    }
    return body


def call_api(token, body, endpoint, max_retries=3):
    """Call the scrape API with retry and exponential backoff."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
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
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(json.dumps({
                "error": f"HTTP {e.code}: {error_body}",
            }), file=sys.stderr)
            sys.exit(EXIT_NETWORK_ERROR)
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(json.dumps({
                "error": f"Network error: {e}",
            }), file=sys.stderr)
            sys.exit(EXIT_NETWORK_ERROR)

    return None


def handle_response(result, token, body, endpoint):
    """Handle API response, retrying auth on 1004 error."""
    if result.get("code") == 1004:
        new_token = refresh_token()
        return call_api(new_token, body, endpoint)
    return result


def extract_google_output(result):
    """Extract structured output from Google SERP API response."""
    code = result.get("code")
    if code != 0:
        return {
            "success": False,
            "error_code": code,
            "message": result.get("message", "Unknown error"),
        }

    data = result.get("data", {})
    output = {
        "success": True,
        "task_id": data.get("taskId"),
        "results_num": data.get("results_num", 0),
        "ai_overview_count": data.get("ai_overview", 0),
    }

    json_data = data.get("json", {})
    items = json_data.get("items", [])

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
    if organic_results:
        output["organic_results"] = organic_results

    screenshot_url = data.get("screenshot")
    if screenshot_url:
        output["screenshot"] = screenshot_url

    return output


def extract_amazon_output(result):
    """Extract structured output from Amazon Scrape API response."""
    code = result.get("code")
    if code != 0:
        return {
            "success": False,
            "error_code": code,
            "message": result.get("message", "Unknown error"),
        }

    data = result.get("data", {})
    output = {
        "success": True,
        "task_id": data.get("taskId"),
        "url": data.get("url"),
    }

    json_data = data.get("json")
    if isinstance(json_data, list):
        output["products"] = json_data
        output["results_count"] = len(json_data)
    elif isinstance(json_data, dict):
        output["product"] = json_data
        output["results_count"] = 1
    else:
        output["data"] = json_data
        output["results_count"] = 0

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Pangolin SERP & Scrape API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Environment variables:\n"
               "  PANGOLIN_TOKEN      Bearer token (skips login)\n"
               "  PANGOLIN_EMAIL      Account email\n"
               "  PANGOLIN_PASSWORD   Account password\n"
               "\n"
               "Amazon parsers:\n"
               "  amzProductDetail       Product detail page\n"
               "  amzKeyword             Keyword search results\n"
               "  amzProductOfCategory   Category listing\n"
               "  amzProductOfSeller     Seller's products\n"
               "  amzBestSellers         Best sellers ranking\n"
               "  amzNewReleases         New releases ranking\n"
               "  amzFollowSeller        Product variants/seller options",
    )
    parser.add_argument("--q", dest="query", help="Search query")
    parser.add_argument("--url", dest="target_url", help="Target URL (required for Amazon product pages)")
    parser.add_argument(
        "--mode",
        choices=["ai-mode", "serp", "amazon"],
        default="ai-mode",
        help="API mode: ai-mode (default) | serp | amazon",
    )
    parser.add_argument("--screenshot", action="store_true", help="Capture page screenshot (Google only)")
    parser.add_argument(
        "--follow-up",
        action="append",
        dest="follow_ups",
        help="Follow-up question for multi-turn (ai-mode only). Can be repeated. >5 may slow response.",
    )
    parser.add_argument("--num", type=int, default=10, help="Number of results (default: 10, Google only)")
    parser.add_argument(
        "--parser",
        choices=AMAZON_PARSERS,
        default="amzProductDetail",
        help="Amazon parser name (default: amzProductDetail)",
    )
    parser.add_argument("--zipcode", default="10041", help="Amazon zipcode for localized pricing (default: 10041)")
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["json", "rawHtml", "markdown"],
        default="json",
        help="Amazon response format (default: json)",
    )
    parser.add_argument("--auth-only", action="store_true", help="Only authenticate and print token info")
    parser.add_argument("--raw", action="store_true", help="Output raw API response instead of extracted data")

    args = parser.parse_args()

    if not args.query and not args.target_url and not args.auth_only:
        parser.error("--q or --url is required unless using --auth-only")

    if args.follow_ups and args.mode != "ai-mode":
        parser.error("--follow-up is only supported in ai-mode")

    if args.follow_ups and len(args.follow_ups) > 5:
        print(json.dumps({
            "warning": f"Using {len(args.follow_ups)} follow-ups (>5). Response may be slower.",
        }), file=sys.stderr)

    token = get_token()

    if args.auth_only:
        print(json.dumps({
            "success": True,
            "message": "Authentication successful",
            "token_preview": f"{token[:8]}...{token[-4:]}" if len(token) > 12 else "***",
        }, indent=2))
        sys.exit(EXIT_SUCCESS)

    if args.mode == "amazon":
        body = build_amazon_body(args.target_url, args.query, args.parser, args.zipcode, args.fmt)
        endpoint = SCRAPE_V1_ENDPOINT
    else:
        query = args.query
        if not query:
            parser.error("--q is required for Google search modes")
        body = build_google_body(query, args.mode, args.screenshot, args.follow_ups, args.num)
        endpoint = SCRAPE_V2_ENDPOINT

    result = call_api(token, body, endpoint)

    if result is None:
        print(json.dumps({"error": "API call failed after retries"}), file=sys.stderr)
        sys.exit(EXIT_NETWORK_ERROR)

    result = handle_response(result, token, body, endpoint)

    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if args.mode == "amazon":
            output = extract_amazon_output(result)
        else:
            output = extract_google_output(result)
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if result.get("code") != 0:
        sys.exit(EXIT_API_ERROR)

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
