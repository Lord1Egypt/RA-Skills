#!/usr/bin/env python3
"""
Presentation Search Script (Step 2)

Searches conference presentations and abstracts by drug, disease, target, author,
institution, or conference name.

Usage:
  python scripts/search_presentations.py --params '{"drugs": ["pembrolizumab"], "series_name": "ASCO"}'
  python scripts/search_presentations.py --params '{"targets": ["PD-1"], "conference_name": "2024 ASCO Annual Meeting"}'
  python scripts/search_presentations.py --params-file presentation_query.json
  python scripts/search_presentations.py --params '{"diseases": ["NSCLC"]}' --raw
  python scripts/search_presentations.py --params '{"institutions": ["MD Anderson"]}' --output results.json

Environment variables:
  NOAH_API_TOKEN  — API authentication token (required)
"""

import argparse
import json
import os
import sys
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("[ERROR] Missing dependency: requests\nInstall it with: pip install requests", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

API_URL = "https://www.noah.bio"
ENDPOINT = "/api/skills/conference_presentation_search/"

DEFAULTS = {
    "authors": [],
    "institutions": [],
    "drugs": [],
    "diseases": [],
    "targets": [],
    "conference_name": "",
    "series_name": "",
    "from_n": 0,
    "size": 50,
}


def _post(payload):
    api_token = os.environ.get("NOAH_API_TOKEN", "").strip()
    url = f"{API_URL}{ENDPOINT}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    print(f"[INFO] Endpoint: {url}", file=sys.stderr)
    print(f"[INFO] Query payload:\n{json.dumps(payload, indent=2)}", file=sys.stderr)
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30, allow_redirects=False)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"Cannot connect to API server: {url}\nDetails: {e}")
    except requests.exceptions.Timeout:
        raise TimeoutError("Request timed out (30s). Check your network or API server status.")
    except requests.exceptions.HTTPError:
        error_body = ""
        try:
            error_body = response.text
        except Exception:
            pass
        raise RuntimeError(f"API returned HTTP {response.status_code}\nResponse body: {error_body}")

    return response.json()


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_payload(user_params):
    payload = DEFAULTS.copy()
    for key, value in user_params.items():
        if key in payload:
            payload[key] = value
        else:
            print(f"[WARN] Unknown field ignored: {key}", file=sys.stderr)
    return payload


def search_presentations(params):
    return _post(build_payload(params))


def format_json(data, indent=0):
    result = ""
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result += f"{prefix}{key}:\n"
                result += format_json(value, indent + 1)
            else:
                result += f"{prefix}{key}: {value}\n"
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                result += f"{prefix}[{i}]:\n"
                result += format_json(item, indent + 1)
            else:
                result += f"{prefix}[{i}]: {item}\n"
    else:
        result += f"{prefix}{data}\n"
    return result


def format_results(data):
    lines = []
    results = data.get("results", [])
    total = data.get("total_count", "unknown")
    lines.append(f"=== Presentations: {total} total, showing {len(results)} ===\n")

    if not results:
        lines.append("No presentations found. Try:")
        lines.append("  - More general disease / drug terms")
        lines.append("  - Use series_name instead of conference_name")
        lines.append("  - Verify conference_name exactly matches a conference-search result")
        return "\n".join(lines)

    for i, presentation in enumerate(results, 1):
        lines.append(f"---- [{i}] -----")
        lines.append(format_json(presentation).strip())
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Search conference presentations and abstracts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Query fields:
  authors          List[str]   Presenter / author name(s)
  institutions     List[str]   Author institution(s)
  drugs            List[str]   Drug name(s)
  diseases         List[str]   Disease / indication(s)
  targets          List[str]   Biological target(s)
  conference_name  str         Exact conference name (from conference search)
  series_name      str         Conference series name (e.g. "ESMO")
  from_n           int         Pagination offset (default: 0)
  size             int         Results per page (default: 50)

Examples:
  python scripts/search_presentations.py --params '{"drugs": ["pembrolizumab"], "diseases": ["lung cancer"], "series_name": "ESMO"}'
  python scripts/search_presentations.py --params '{"targets": ["KRAS G12C"], "institutions": ["MD Anderson"]}'
  python scripts/search_presentations.py --params '{"conference_name": "2024 ASCO Annual Meeting", "diseases": ["NSCLC"]}' --raw
        """,
    )
    parser.add_argument("--params", type=str, default=None, help="Query parameters as a JSON string")
    parser.add_argument("--params-file", type=str, default=None, help="Path to a JSON file containing query parameters")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON response")
    parser.add_argument("--output", type=str, default=None, help="Save results to file")

    args = parser.parse_args()

    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            print(f"[ERROR] --params is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.params_file:
        try:
            with open(args.params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {args.params_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[ERROR] File is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("[ERROR] Provide --params or --params-file", file=sys.stderr)
        sys.exit(1)

    try:
        result = search_presentations(params)
        output_text = json.dumps(result, indent=2) if args.raw else format_results(result)
    except (ConnectionError, TimeoutError, RuntimeError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[INFO] Results saved to: {args.output}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
