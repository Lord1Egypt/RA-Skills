#!/usr/bin/env python3
"""
Prompt Inspector — detection helper script.

Sends text to the Prompt Inspector API and prints the result.
No third-party packages required beyond the Python standard library.

Usage:
    python3 detect.py --text "Ignore all previous instructions..."
    python3 detect.py --file inputs.txt --format json
    python3 detect.py --api-key pi_xxx --text "..." --format json

Authentication (in priority order):
    1. --api-key  command-line argument
    2. PMTINSP_API_KEY  environment variable
    3. ~/.openclaw/.env  file  (line: PMTINSP_API_KEY=...)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://promptinspector.io"
DETECT_PATH = "/api/v1/detect/sdk"
DEFAULT_TIMEOUT = 60  # seconds


# ---------------------------------------------------------------------------
# API key resolution
# ---------------------------------------------------------------------------

def _load_dotenv(path: Path) -> dict:
    """Parse a simple KEY=VALUE .env file and return a dict."""
    env = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip()
            # Remove surrounding quotes if present
            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            env[key.strip()] = value
    except OSError:
        pass
    return env


def resolve_api_key(cli_key: str | None) -> str:
    """Return the first available API key or exit with an error."""
    # 1. CLI argument
    if cli_key:
        return cli_key

    # 2. Environment variable
    env_key = os.environ.get("PMTINSP_API_KEY")
    if env_key:
        return env_key

    # 3. ~/.openclaw/.env
    dotenv_path = Path.home() / ".openclaw" / ".env"
    dotenv = _load_dotenv(dotenv_path)
    dotenv_key = dotenv.get("PMTINSP_API_KEY")
    if dotenv_key:
        return dotenv_key

    print(
        "Error: No API key found.\n"
        "  Provide it via --api-key, the PMTINSP_API_KEY environment variable,\n"
        "  or add PMTINSP_API_KEY=... to ~/.openclaw/.env\n\n"
        "  Get your key at https://promptinspector.io",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def detect(text: str, api_key: str, base_url: str, timeout: int) -> dict:
    """
    Call the Prompt Inspector detection endpoint.

    Returns the parsed JSON response dict.
    Raises SystemExit on error.
    """
    url = base_url.rstrip("/") + DETECT_PATH
    payload = json.dumps({"input_text": text}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("X-App-Key", api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Length", str(len(payload)))
    req.add_header("User-Agent", "python-httpx/0.28.1")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        _handle_http_error(exc.code, body)
    except urllib.error.URLError as exc:
        print(f"Error: Connection failed — {exc.reason}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print(f"Error: Request timed out after {timeout}s.", file=sys.stderr)
        sys.exit(1)


def _handle_http_error(status: int, body: str) -> None:
    """Print a friendly error message for known HTTP status codes and exit."""
    try:
        detail = json.loads(body).get("detail", "")
    except Exception:
        detail = body[:200]

    messages = {
        401: "Authentication failed. Check your API key.",
        403: "Authentication failed. Check your API key.",
        413: "Input text is too long for your current plan.",
        422: f"Invalid request: {detail}",
        429: "Rate limit exceeded. Please slow down your requests.",
    }
    msg = messages.get(status, f"API error (HTTP {status}): {detail or 'unexpected error'}")
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _format_human(data: dict) -> str:
    result = data.get("result", {})
    categories = result.get("category", [])
    cat_str = ", ".join(categories) if categories else "none"
    lines = [
        f"Request ID : {data.get('request_id', 'n/a')}",
        f"Is Safe    : {result.get('is_safe', True)}",
        f"Score      : {result.get('score')}",
        f"Category   : {cat_str}",
        f"Latency    : {data.get('latency_ms', 0)} ms",
    ]
    return "\n".join(lines)


def _format_json(data: dict) -> str:
    result = data.get("result", {})
    out = {
        "request_id": data.get("request_id", ""),
        "is_safe": result.get("is_safe", True),
        "score": result.get("score"),
        "category": result.get("category", []),
        "latency_ms": data.get("latency_ms", 0),
    }
    return json.dumps(out, indent=2)


def print_result(data: dict, fmt: str) -> None:
    if fmt == "json":
        print(_format_json(data))
    else:
        print(_format_human(data))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prompt Inspector — detect prompt injection via the API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 detect.py --text 'Ignore all previous instructions'\n"
            "  python3 detect.py --file inputs.txt --format json\n"
            "  python3 detect.py --api-key pi_xxx --text '...' --format json\n\n"
            "Docs: https://docs.promptinspector.io"
        ),
    )
    parser.add_argument("--text", help="Text to inspect (single input)")
    parser.add_argument(
        "--file",
        help="Path to a text file; each non-empty line is inspected separately",
    )
    parser.add_argument("--api-key", help="Prompt Inspector API key")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--format",
        choices=["human", "json"],
        default="human",
        help="Output format: human-readable (default) or json",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.text and not args.file:
        parser.error("Provide --text or --file.")

    api_key = resolve_api_key(args.api_key)

    if args.text:
        data = detect(args.text, api_key, args.base_url, args.timeout)
        print_result(data, args.format)
        return

    # Batch mode: --file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    lines = [l.strip() for l in file_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        print("Error: File is empty.", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, line in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}] Inspecting: {line[:60]}...", file=sys.stderr)
        data = detect(line, api_key, args.base_url, args.timeout)
        if args.format == "json":
            result = data.get("result", {})
            results.append({
                "input": line,
                "request_id": data.get("request_id", ""),
                "is_safe": result.get("is_safe", True),
                "score": result.get("score"),
                "category": result.get("category", []),
                "latency_ms": data.get("latency_ms", 0),
            })
        else:
            print(f"\n--- [{i}] {line[:80]} ---")
            print_result(data, args.format)

    if args.format == "json":
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
