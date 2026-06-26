#!/usr/bin/env python3
"""
LinkFoxAgent CLI - Cross-border e-commerce AI Agent.

Submit tasks to LinkFoxAgent and retrieve structured results.
Supports 41 tools for product research, competitor analysis, keyword tracking,
review insights, patent detection, and more.

Default mode is background: submit task and return messageId immediately,
so the caller can continue while the task runs (tasks typically take 1-5 min).
Use --poll to check the result later, or --wait to block until done.

Usage:
    linkfox.py "<task>"                       # Submit in background, return messageId (default)
    linkfox.py --wait "<task>"               # Submit and wait for result (blocking)
    linkfox.py --poll <messageId>             # Poll result for a messageId
    linkfox.py --timeout 600 --poll <id>     # Custom timeout when polling (seconds)
    linkfox.py --format json --poll <id>     # Output raw JSON

Environment:
    LINKFOXAGENT_API_KEY - Required API key for LinkFoxAgent
"""

import argparse
import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


LINKFOXAGENT_BASE_URL = "https://agent-api.linkfox.com/"
SUBMIT_ENDPOINT = "chat/saveMessageForApi"
POLL_ENDPOINT = "chat/getMessageForApi"

TERMINAL_STATUSES = {"finished", "error", "cancel"}


def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "Error: LINKFOXAGENT_API_KEY environment variable not set.\n"
            "Get your API key from: https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb\n"
            "Then set it:\n"
            "  export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def api_request(endpoint: str, payload: dict) -> dict:
    """Make a POST request to the LinkFoxAgent API."""
    api_key = get_api_key()
    url = f"{LINKFOXAGENT_BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")

    req = Request(
        url,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFoxAgent-Skill/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def submit_task(text: str) -> dict:
    """Submit a task to LinkFoxAgent. Returns response with messageId."""
    return api_request(SUBMIT_ENDPOINT, {"text": text})


def poll_result(message_id: str, max_wait: int = 300, interval: int = 5) -> dict:
    """Poll for task result until terminal status or timeout."""
    elapsed = 0
    while elapsed < max_wait:
        result = api_request(POLL_ENDPOINT, {"id": message_id})

        if "error" in result:
            return result

        status = result.get("status", "")
        if status in TERMINAL_STATUSES:
            return result

        # Still working, wait and retry
        time.sleep(interval)
        elapsed += interval

        if elapsed % 30 == 0:
            print(f"... still working ({elapsed}s elapsed)", file=sys.stderr)

    return {"error": f"Timeout after {max_wait}s. messageId: {message_id}. Use --poll {message_id} to check later."}


def format_result(result: dict) -> str:
    """Format a poll result as human-readable text."""
    if "error" in result:
        return f"Error: {result['error']}"

    lines = []
    status = result.get("status", "unknown")
    lines.append(f"Status: {status}")

    reflection = result.get("reflection")
    if reflection:
        lines.append(f"\n{reflection}")

    results = result.get("results", [])
    for i, item in enumerate(results, 1):
        content_type = item.get("type", "unknown")
        content = item.get("content", "")

        if content_type == "html":
            lines.append(f"\n--- Result {i} (HTML URL) ---")
            lines.append(content)
        elif content_type == "json":
            lines.append(f"\n--- Result {i} (JSON Data) ---")
            try:
                parsed = json.loads(content) if isinstance(content, str) else content
                lines.append(json.dumps(parsed, indent=2, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError):
                lines.append(str(content))
        else:
            lines.append(f"\n--- Result {i} ({content_type}) ---")
            lines.append(str(content))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="LinkFoxAgent - Cross-border e-commerce AI Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("task", nargs="?", help="Task description to submit")
    parser.add_argument(
        "--wait", action="store_true",
        help="Block until task completes and return the result (default: background, return messageId immediately)",
    )
    parser.add_argument(
        "--poll", dest="poll_id", metavar="MESSAGE_ID",
        help="Poll result for an existing messageId",
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Max wait time in seconds (default: 300)",
    )
    parser.add_argument(
        "--interval", type=int, default=5,
        help="Poll interval in seconds (default: 5)",
    )
    parser.add_argument(
        "--format", "-f", choices=["json", "text"], default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Mode: poll existing messageId
    if args.poll_id:
        result = poll_result(args.poll_id, max_wait=args.timeout, interval=args.interval)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_result(result))
        return

    # Require task for submit modes
    if not args.task:
        parser.error("task is required (or use --poll MESSAGE_ID)")

    response = submit_task(args.task)
    if "error" in response:
        print(f"Error: {response['error']}", file=sys.stderr)
        if response.get("details"):
            print(f"Details: {response['details']}", file=sys.stderr)
        sys.exit(1)

    message_id = response.get("messageId", "")

    # Mode: background (default) — return messageId immediately so the caller can continue
    if not args.wait:
        print(json.dumps({"messageId": message_id}, indent=2))
        return

    # Mode: --wait — block until task completes
    print(f"Task submitted. messageId: {message_id}", file=sys.stderr)
    print("Waiting for result...", file=sys.stderr)

    result = poll_result(message_id, max_wait=args.timeout, interval=args.interval)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result(result))

    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
