#!/usr/bin/env python3
"""
http_client.py - Developer-friendly HTTP client for agents and scripts.

Usage:
    python3 http_client.py <METHOD> <URL> [options]
"""

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from ssl import create_default_context, CERT_NONE

# ANSI colors
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def colorize(text, color, use_color=True):
    if not use_color:
        return text
    return f"{color}{text}{RESET}"


def status_color(code, use_color=True):
    if not use_color:
        return str(code)
    if code < 300:
        return colorize(str(code), GREEN)
    elif code < 400:
        return colorize(str(code), YELLOW)
    else:
        return colorize(str(code), RED)


def pretty_json(text, use_color=True):
    """Pretty-print JSON with optional color."""
    try:
        obj = json.loads(text)
        pretty = json.dumps(obj, indent=2, ensure_ascii=False)
        if not use_color:
            return pretty
        # Basic colorization
        lines = []
        for line in pretty.splitlines():
            stripped = line.lstrip()
            if stripped.startswith('"') and ":" in stripped:
                key, rest = stripped.split(":", 1)
                indent = line[:len(line) - len(stripped)]
                lines.append(f"{indent}{colorize(key, CYAN)}:{rest}")
            elif stripped.startswith('"'):
                indent = line[:len(line) - len(stripped)]
                lines.append(f"{indent}{colorize(stripped, GREEN)}")
            elif stripped in ("{", "}", "[", "]", "{}", "[]") or stripped.endswith((",", "},")):
                lines.append(colorize(line, DIM))
            else:
                lines.append(line)
        return "\n".join(lines)
    except (json.JSONDecodeError, ValueError):
        return text


def build_request(method, url, headers=None, body=None, no_verify=False):
    """Build a urllib Request object."""
    req = urllib.request.Request(url, method=method.upper())
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    if body:
        if isinstance(body, str):
            body = body.encode("utf-8")
        req.data = body
    return req


def do_request(req, timeout=30, follow_redirects=False, no_verify=False):
    """Execute the HTTP request and return (response_code, headers, body, elapsed_ms)."""
    ctx = None
    if no_verify:
        ctx = create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = CERT_NONE

    opener = urllib.request.build_opener()
    if not follow_redirects:
        opener = urllib.request.build_opener(
            urllib.request.HTTPErrorProcessor()
        )

    start = time.monotonic()
    try:
        resp = opener.open(req, timeout=timeout, context=ctx) if ctx else opener.open(req, timeout=timeout)
        elapsed = int((time.monotonic() - start) * 1000)
        status = resp.status
        headers = dict(resp.headers)
        body = resp.read().decode("utf-8", errors="replace")
        return status, headers, body, elapsed
    except urllib.error.HTTPError as e:
        elapsed = int((time.monotonic() - start) * 1000)
        headers = dict(e.headers) if e.headers else {}
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, headers, body, elapsed
    except urllib.error.URLError as e:
        elapsed = int((time.monotonic() - start) * 1000)
        raise ConnectionError(f"Request failed: {e.reason}") from e
    except TimeoutError:
        raise TimeoutError(f"Request timed out after {timeout}s")


def main():
    parser = argparse.ArgumentParser(
        description="Developer-friendly HTTP client for agents and scripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 http_client.py GET https://httpbin.org/get
  python3 http_client.py POST https://httpbin.org/post --json '{"key": "value"}'
  python3 http_client.py GET https://api.example.com/me --bearer mytoken123
  python3 http_client.py GET https://api.example.com/ --auth user:pass
  python3 http_client.py POST https://api.example.com/ --form "name=test&val=1"
  python3 http_client.py GET https://httpbin.org/get --output-json
        """
    )
    parser.add_argument("method", metavar="METHOD",
                        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
                        help="HTTP method")
    parser.add_argument("url", metavar="URL", help="Target URL")
    parser.add_argument("--json", dest="json_body",
                        help="JSON request body")
    parser.add_argument("--form",
                        help="Form-encoded body (key=value&key2=val2)")
    parser.add_argument("--bearer",
                        help="Bearer token for Authorization header")
    parser.add_argument("--auth",
                        help="Basic auth as user:password")
    parser.add_argument("--api-key",
                        help="API key header as 'Header-Name:value'")
    parser.add_argument("--header", "-H", action="append", dest="headers",
                        help="Custom header 'Name: Value' (repeatable)")
    parser.add_argument("--follow", "-L", action="store_true",
                        help="Follow redirects")
    parser.add_argument("--timeout", type=float, default=30,
                        help="Timeout in seconds (default: 30)")
    parser.add_argument("--status-only", action="store_true",
                        help="Print only HTTP status code")
    parser.add_argument("--output", "-o",
                        help="Save response body to file")
    parser.add_argument("--output-json", action="store_true",
                        help="Output full response as JSON")
    parser.add_argument("--timing", action="store_true",
                        help="Show request timing")
    parser.add_argument("--no-verify", action="store_true",
                        help="Skip TLS certificate verification")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show request headers sent")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable color output")

    args = parser.parse_args()
    use_color = not args.no_color and sys.stdout.isatty()

    # Build headers
    req_headers = {}

    # Content-type for body
    if args.json_body:
        req_headers["Content-Type"] = "application/json"
    elif args.form:
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"

    # Auth
    if args.bearer:
        req_headers["Authorization"] = f"Bearer {args.bearer}"
    elif args.auth:
        encoded = base64.b64encode(args.auth.encode()).decode()
        req_headers["Authorization"] = f"Basic {encoded}"

    # API key
    if args.api_key:
        if ":" not in args.api_key:
            print("[ERROR] --api-key must be in format 'Header-Name:value'", file=sys.stderr)
            sys.exit(2)
        hname, hval = args.api_key.split(":", 1)
        req_headers[hname.strip()] = hval.strip()

    # Custom headers
    if args.headers:
        for h in args.headers:
            if ":" not in h:
                print(f"[ERROR] Invalid header format: {h!r}. Use 'Name: Value'", file=sys.stderr)
                sys.exit(2)
            name, val = h.split(":", 1)
            req_headers[name.strip()] = val.strip()

    # Default User-Agent
    if "User-Agent" not in req_headers:
        req_headers["User-Agent"] = "jrv-http-client/1.0"

    # Accept
    if "Accept" not in req_headers:
        req_headers["Accept"] = "*/*"

    # Body
    body = None
    if args.json_body:
        # Validate JSON
        try:
            json.loads(args.json_body)
            body = args.json_body
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON body: {e}", file=sys.stderr)
            sys.exit(2)
    elif args.form:
        body = args.form

    if args.verbose:
        print(colorize(f"→ {args.method} {args.url}", BOLD, use_color))
        for k, v in req_headers.items():
            masked = v if "Authorization" not in k else v[:20] + "..."
            print(colorize(f"  {k}: {masked}", DIM, use_color))
        if body:
            print(colorize(f"  [body: {len(body)} bytes]", DIM, use_color))
        print()

    # Build and execute request
    req = build_request(args.method, args.url, req_headers, body, args.no_verify)

    try:
        status, resp_headers, resp_body, elapsed_ms = do_request(
            req, timeout=args.timeout,
            follow_redirects=args.follow,
            no_verify=args.no_verify
        )
    except ConnectionError as e:
        print(colorize(f"[ERROR] {e}", RED, use_color), file=sys.stderr)
        sys.exit(2)
    except TimeoutError as e:
        print(colorize(f"[TIMEOUT] {e}", RED, use_color), file=sys.stderr)
        sys.exit(2)

    # --status-only
    if args.status_only:
        print(status)
        sys.exit(0 if status < 400 else 1)

    # --output-json
    if args.output_json:
        result = {
            "status": status,
            "headers": resp_headers,
            "body": resp_body,
            "elapsed_ms": elapsed_ms,
            "url": args.url,
            "method": args.method,
        }
        # Try to parse body as JSON
        try:
            result["body_parsed"] = json.loads(resp_body)
        except (json.JSONDecodeError, ValueError):
            pass
        print(json.dumps(result, indent=2, default=str))
        sys.exit(0 if status < 400 else 1)

    # Pretty output
    content_type = resp_headers.get("Content-Type", "")

    # Status line
    status_str = status_color(status, use_color)
    timing_str = colorize(f" ({elapsed_ms}ms)", DIM, use_color) if args.timing else ""
    print(colorize(f"HTTP {status_str}", BOLD, use_color) + timing_str)

    # Response headers (condensed)
    for k, v in sorted(resp_headers.items()):
        if k.lower() in ("content-type", "content-length", "server", "date", "x-request-id"):
            print(colorize(f"  {k}: {v}", DIM, use_color))

    print()

    # Body
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(resp_body, encoding="utf-8")
        size = len(resp_body.encode("utf-8"))
        print(colorize(f"[OK] Response saved to {args.output} ({size} bytes)", GREEN, use_color))
    else:
        if "json" in content_type or resp_body.strip().startswith(("{", "[")):
            print(pretty_json(resp_body, use_color))
        else:
            print(resp_body)

    if args.timing and not args.output_json:
        print()
        print(colorize(f"⏱  {elapsed_ms}ms", DIM, use_color))

    sys.exit(0 if status < 400 else 1)


if __name__ == "__main__":
    main()
