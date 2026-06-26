#!/usr/bin/env python3
"""
Promarkia API client — run squads, list squads, and fetch run results.

Usage:
    python promarkia_run.py --squad 11 --prompt "Post about AI on LinkedIn"
    python promarkia_run.py --list-squads
    python promarkia_run.py --get-run RUN_ID

Environment:
    PROMARKIA_API_KEY   — Required. Your Promarkia API key (pmk_...).
    PROMARKIA_API_BASE  — Optional. Default: https://www.promarkia.com
"""

import argparse
import json
import os
import sys

# Fix Unicode output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API_BASE = os.environ.get("PROMARKIA_API_BASE", "https://www.promarkia.com").rstrip("/")
API_KEY = os.environ.get("PROMARKIA_API_KEY", "")

# Security: only allow API calls to official Promarkia domains
_ALLOWED_HOSTS = {"www.promarkia.com", "promarkia.com"}
from urllib.parse import urlparse as _urlparse
_parsed_host = _urlparse(API_BASE).hostname
if _parsed_host not in _ALLOWED_HOSTS:
    print(f"ERROR: PROMARKIA_API_BASE points to untrusted host '{_parsed_host}'.", file=sys.stderr)
    print(f"Only {_ALLOWED_HOSTS} are allowed. This prevents your API key from being sent to arbitrary servers.", file=sys.stderr)
    sys.exit(1)


def _headers():
    if not API_KEY:
        print("ERROR: PROMARKIA_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get your key at https://www.promarkia.com (sidebar → API Keys).", file=sys.stderr)
        sys.exit(1)
    return {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
    }


def _request(method, path, json_body=None, params=None):
    """Minimal HTTP client using urllib (no external dependencies)."""
    import urllib.request
    import urllib.error
    import urllib.parse

    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = _headers()
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=1260) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            err = {"error": body}
        print(f"ERROR: HTTP {e.code} — {err.get('description') or err.get('error') or body}", file=sys.stderr)
        sys.exit(1)


def list_squads():
    """Fetch and display available squads."""
    squads = _request("GET", "/api/external/squads")
    print(f"\n{'ID':<6} {'Name':<28} {'Integrations'}")
    print("-" * 70)
    for s in squads:
        integrations = ", ".join(s.get("integrations", []))
        print(f"{s['id']:<6} {s['name']:<28} {integrations}")
    print(f"\n{len(squads)} squads available.\n")


def _display_result(result):
    """Display agent output from a completed result."""
    credit_cost = result.get("creditCost", 0)
    total_tokens = result.get("totalTokens", 0)
    print(f"Credits used: {credit_cost} ({total_tokens} tokens)")

    # Display readable messages (agent outputs with content)
    messages = result.get("messages", [])
    if messages:
        print(f"\n--- Agent Output ---")
        for msg in messages:
            source = msg.get("source", "unknown")
            content = msg.get("content", "")
            if content and not content.strip().startswith("{"):
                # Skip raw JSON blobs, show human-readable content
                # Strip termination markers
                for marker in ("TERMINATE", "PLAN_READY_ON_SCREEN", "DOCS_DONE"):
                    content = content.replace(marker, "").strip()
                if content:
                    print(f"\n[{source}]")
                    print(content[:5000])
        print()
    else:
        # Fallback: try to extract from task_result
        task_result = result.get("result")
        if task_result and isinstance(task_result, dict):
            msgs = task_result.get("messages", [])
            for msg in reversed(msgs):
                if isinstance(msg, dict):
                    content = msg.get("content", "")
                    source = msg.get("source", "")
                    if content and isinstance(content, str) and source != "user":
                        for marker in ("TERMINATE", "PLAN_READY_ON_SCREEN", "DOCS_DONE"):
                            content = content.replace(marker, "").strip()
                        if content:
                            print(f"\n--- Result ---")
                            print(f"[{source}]")
                            print(content[:5000])
                            print()
                            break
            else:
                print("\n--- Result (raw) ---")
                print(json.dumps(task_result, indent=2, default=str)[:3000])
                print()
        else:
            print("\nNo result content returned.\n")


def submit_task(squad_id, prompt, timeout=1200, poll_interval=10):
    """Submit a task (async) and poll for the result."""
    import time

    print(f"Submitting task to squad {squad_id}...")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print(f"Timeout: {timeout}s\n")

    result = _request("POST", "/api/external/tasks", json_body={
        "squadId": str(squad_id),
        "prompt": prompt,
        "timeout": timeout,
    })

    status = result.get("status", "unknown")
    run_id = result.get("runId", "N/A")

    if status == "error":
        print(f"Status: {status}")
        print(f"\nError: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    # If server returned completed immediately (backward compat)
    if status == "completed":
        print(f"Status: completed")
        print(f"Run ID: {run_id}")
        _display_result(result)
        return

    # Async mode: poll for result
    print(f"Run ID: {run_id}")
    print(f"Status: processing (async)...")

    elapsed = 0
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval

        try:
            poll_result = _request("GET", f"/api/external/runs/{run_id}")
        except SystemExit:
            # _request calls sys.exit on HTTP errors — retry on transient errors
            print(f"  [{elapsed}s] Poll error, retrying...")
            continue

        poll_status = poll_result.get("status", "processing")

        if poll_status == "completed":
            print(f"\nCompleted after ~{elapsed}s")
            _display_result(poll_result)
            return

        elif poll_status == "error":
            print(f"\nTask failed after ~{elapsed}s")
            print(f"Error: {poll_result.get('error', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)

        else:
            # Still processing
            print(f"  [{elapsed}s] Still processing...")

    print(f"\nTimed out after {timeout}s. Run ID: {run_id}")
    print(f"Check later with: python promarkia_run.py --get-run {run_id}")
    sys.exit(1)


def get_run(run_id):
    """Fetch and display a previous run result."""
    result = _request("GET", f"/api/external/runs/{run_id}")
    status = result.get("status", "unknown")
    print(f"Run ID: {result.get('runId', run_id)}")
    print(f"Status: {status}")
    if status == "completed":
        _display_result(result)
    elif status == "error":
        print(f"Error: {result.get('error', 'Unknown error')}")
    elif status == "processing":
        print("Task is still running. Check again later.")
    else:
        print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        description="Promarkia API client — run AI squads from the command line.",
        epilog="Get your API key at https://www.promarkia.com",
    )
    parser.add_argument("--squad", "-s", type=str, help="Squad ID to run (e.g. 11 for Social Media)")
    parser.add_argument("--prompt", "-p", type=str, help="Task prompt to send to the squad")
    parser.add_argument("--timeout", "-t", type=int, default=1200, help="Max execution time in seconds (default: 1200)")
    parser.add_argument("--list-squads", "-l", action="store_true", help="List available squads")
    parser.add_argument("--get-run", "-g", type=str, metavar="RUN_ID", help="Fetch a previous run result by ID")

    args = parser.parse_args()

    if args.list_squads:
        list_squads()
    elif args.get_run:
        get_run(args.get_run)
    elif args.squad and args.prompt:
        submit_task(args.squad, args.prompt, args.timeout)
    else:
        parser.print_help()
        print("\nExamples:")
        print('  python promarkia_run.py --list-squads')
        print('  python promarkia_run.py --squad 11 --prompt "Post about AI on LinkedIn"')
        print('  python promarkia_run.py --get-run 123456')


if __name__ == "__main__":
    main()
