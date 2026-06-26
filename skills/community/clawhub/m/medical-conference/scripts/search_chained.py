#!/usr/bin/env python3
"""
Chained Conference + Presentation Search Script

Runs conference search first, then automatically injects the top-matching
conference_name into a follow-up presentation search. Use this when you
want to discover the exact conference name before searching its presentations.

Usage:
  python scripts/search_chained.py \
      --conference-params '{"series_name": "ASCO", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}' \
      --presentation-params '{"targets": ["PD-1"]}'

  python scripts/search_chained.py \
      --conference-params '{"series_name": "ASH"}' \
      --presentation-params '{"drugs": ["bispecific antibody"], "institutions": ["Roche"]}' \
      --raw --output results.json

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
# API helper (shared)
# ---------------------------------------------------------------------------

API_URL = "https://www.noah.bio"


def _post(endpoint, payload):
    api_token = os.environ.get("NOAH_API_TOKEN", "").strip()
    url = f"{API_URL}{endpoint}"
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
# Conference search
# ---------------------------------------------------------------------------

CONFERENCE_ENDPOINT = "/api/skills/conference_search/"
CONFERENCE_DEFAULTS = {
    "conference_name": "",
    "conference_start_date": "",
    "conference_end_date": "",
    "conference_location": "",
    "series_name": "",
    "series_organization": "",
    "series_area": [],
    "from_n": 0,
    "size": 50,
}


def search_conferences(params):
    payload = CONFERENCE_DEFAULTS.copy()
    for key, value in params.items():
        if key in payload:
            payload[key] = value
        else:
            print(f"[WARN] Unknown conference field ignored: {key}", file=sys.stderr)
    return _post(CONFERENCE_ENDPOINT, payload)


def format_conferences(data):
    lines = []
    results = data.get("results", [])
    total = data.get("total_count", "unknown")
    lines.append(f"=== Conferences: {total} total, showing {len(results)} ===\n")

    if not results:
        lines.append("No conferences found. Try:")
        lines.append("  - Shorter partial name (e.g. 'ASCO' not full title)")
        lines.append("  - Remove date filters")
        lines.append("  - Broaden series_area")
        return "\n".join(lines)

    for i, conference in enumerate(results, 1):
        lines.append(f"---- [{i}] -----")
        lines.append(_format_json(conference).strip())
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Presentation search
# ---------------------------------------------------------------------------

PRESENTATION_ENDPOINT = "/api/skills/conference_presentation_search/"
PRESENTATION_DEFAULTS = {
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


def search_presentations(params):
    payload = PRESENTATION_DEFAULTS.copy()
    for key, value in params.items():
        if key in payload:
            payload[key] = value
        else:
            print(f"[WARN] Unknown presentation field ignored: {key}", file=sys.stderr)
    return _post(PRESENTATION_ENDPOINT, payload)


def format_presentations(data):
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
        lines.append(_format_json(presentation).strip())
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared formatting helper
# ---------------------------------------------------------------------------

def _format_json(data, indent=0):
    result = ""
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result += f"{prefix}{key}:\n"
                result += _format_json(value, indent + 1)
            else:
                result += f"{prefix}{key}: {value}\n"
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                result += f"{prefix}[{i}]:\n"
                result += _format_json(item, indent + 1)
            else:
                result += f"{prefix}[{i}]: {item}\n"
    else:
        result += f"{prefix}{data}\n"
    return result


# ---------------------------------------------------------------------------
# Chained workflow
# ---------------------------------------------------------------------------

def run_chained(conference_params, presentation_params, raw):
    # Step 1: Conference search
    conf_result = search_conferences(conference_params)
    conf_output = json.dumps(conf_result, indent=2) if raw else format_conferences(conf_result)

    # Auto-inject top conference_name into presentation params
    conf_results = conf_result.get("results", [])
    if conf_results and not presentation_params.get("conference_name"):
        top_name = conf_results[0].get("conference_name", "")
        if top_name:
            presentation_params["conference_name"] = top_name
            print(f"[INFO] Auto-injected conference_name: {top_name}", file=sys.stderr)

    # Step 2: Presentation search
    pres_result = search_presentations(presentation_params)
    pres_output = json.dumps(pres_result, indent=2) if raw else format_presentations(pres_result)

    separator = "\n" + "=" * 60 + "\n\n"
    return f"{conf_output}{separator}{pres_output}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_params(params_str, params_file, label):
    if params_str:
        try:
            return json.loads(params_str)
        except json.JSONDecodeError as e:
            print(f"[ERROR] {label} is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    if params_file:
        try:
            with open(params_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {params_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[ERROR] File is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    print(f"[ERROR] {label}: provide --conference-params / --presentation-params or their --*-file variants", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Chained conference → presentation search (Step 1 then Step 2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
How it works:
  1. Queries conferences with --conference-params
  2. Takes the top-matching conference_name
  3. Automatically injects it into --presentation-params
  4. Queries presentations and returns both result sets

Conference params (--conference-params):
  conference_name        str         Partial conference name
  conference_start_date  str         Start date (YYYY-MM-DD)
  conference_end_date    str         End date (YYYY-MM-DD)
  conference_location    str         City, country, or venue
  series_name            str         Series name (e.g. "ASCO")
  series_organization    str         Organizing body
  series_area            List[str]   Therapeutic area(s)
  from_n / size          int         Pagination

Presentation params (--presentation-params):
  authors          List[str]   Author name(s)
  institutions     List[str]   Institution(s)
  drugs            List[str]   Drug name(s)
  diseases         List[str]   Disease(s)
  targets          List[str]   Biological target(s)
  series_name      str         Override series name
  from_n / size    int         Pagination

Examples:
  # ASCO 2024 PD-1 data
  python scripts/search_chained.py \\
      --conference-params '{"series_name": "ASCO", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}' \\
      --presentation-params '{"targets": ["PD-1"]}'

  # Roche bispecific antibodies at ASH conferences
  python scripts/search_chained.py \\
      --conference-params '{"series_name": "ASH"}' \\
      --presentation-params '{"drugs": ["bispecific antibody"], "institutions": ["Roche"]}'

  # Save raw JSON output
  python scripts/search_chained.py \\
      --conference-params '{"series_name": "ESMO"}' \\
      --presentation-params '{"diseases": ["breast cancer"]}' \\
      --raw --output results.json
        """,
    )
    parser.add_argument("--conference-params", type=str, default=None, help="Conference query as a JSON string")
    parser.add_argument("--conference-params-file", type=str, default=None, help="Path to conference query JSON file")
    parser.add_argument("--presentation-params", type=str, default=None, help="Presentation query as a JSON string")
    parser.add_argument("--presentation-params-file", type=str, default=None, help="Path to presentation query JSON file")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON response")
    parser.add_argument("--output", type=str, default=None, help="Save results to file")

    args = parser.parse_args()

    conf_params = _load_params(args.conference_params, args.conference_params_file, "--conference-params")
    pres_params = _load_params(args.presentation_params, args.presentation_params_file, "--presentation-params")

    try:
        output_text = run_chained(conf_params, pres_params, args.raw)
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
