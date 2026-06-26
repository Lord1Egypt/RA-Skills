#!/usr/bin/env python3
"""httpstat — Pretty HTTP response statistics. Like curl -v but readable.

Usage:
    httpstat URL [--method GET|POST|...] [--header K:V] [--data BODY] [--json] [--follow] [--timeout SECS]

Examples:
    httpstat https://example.com
    httpstat https://api.github.com/zen --header "Accept: text/plain"
    httpstat https://httpbin.org/post --method POST --data '{"key":"value"}'
"""

import argparse
import http.client
import json as json_mod
import socket
import ssl
import sys
import time
import urllib.parse
from dataclasses import dataclass, field


@dataclass
class Timing:
    dns_ms: float = 0
    tcp_ms: float = 0
    tls_ms: float = 0
    ttfb_ms: float = 0  # time to first byte
    transfer_ms: float = 0
    total_ms: float = 0


@dataclass
class Result:
    url: str = ""
    method: str = "GET"
    status: int = 0
    reason: str = ""
    headers: dict = field(default_factory=dict)
    body_size: int = 0
    timing: Timing = field(default_factory=Timing)
    ip: str = ""
    tls_version: str = ""
    tls_cipher: str = ""
    redirects: list = field(default_factory=list)
    error: str = ""


def resolve_dns(host: str, port: int) -> tuple[str, float]:
    """Resolve hostname and return (ip, time_ms)."""
    start = time.monotonic()
    try:
        infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        ip = infos[0][4][0]
    except socket.gaierror as e:
        raise ConnectionError(f"DNS resolution failed: {e}")
    elapsed = (time.monotonic() - start) * 1000
    return ip, elapsed


def do_request(url: str, method: str = "GET", headers: dict = None,
               body: str = None, timeout: float = 10, follow: bool = False,
               max_redirects: int = 10) -> Result:
    """Perform HTTP request with detailed timing."""
    result = Result(url=url, method=method)
    headers = headers or {}

    parsed = urllib.parse.urlparse(url)
    is_https = parsed.scheme == "https"
    host = parsed.hostname
    port = parsed.port or (443 if is_https else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    # DNS
    try:
        ip, dns_ms = resolve_dns(host, port)
        result.ip = ip
        result.timing.dns_ms = dns_ms
    except ConnectionError as e:
        result.error = str(e)
        return result

    # TCP connect
    t0 = time.monotonic()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
    except (socket.timeout, OSError) as e:
        result.error = f"TCP connect failed: {e}"
        return result
    result.timing.tcp_ms = (time.monotonic() - t0) * 1000

    # TLS handshake
    if is_https:
        t1 = time.monotonic()
        ctx = ssl.create_default_context()
        sock = ctx.wrap_socket(sock, server_hostname=host)
        result.timing.tls_ms = (time.monotonic() - t1) * 1000
        result.tls_version = sock.version() or ""
        cipher = sock.cipher()
        result.tls_cipher = cipher[0] if cipher else ""

    # Send request
    if "Host" not in headers:
        headers["Host"] = host
    if "User-Agent" not in headers:
        headers["User-Agent"] = "httpstat/1.0"
    if "Connection" not in headers:
        headers["Connection"] = "close"

    req_line = f"{method} {path} HTTP/1.1\r\n"
    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    if body:
        if "Content-Length" not in headers:
            header_lines += f"Content-Length: {len(body.encode())}\r\n"
    req = (req_line + header_lines + "\r\n").encode()
    if body:
        req += body.encode()

    t2 = time.monotonic()
    sock.sendall(req)

    # Read response
    response_data = b""
    first_byte = True
    while True:
        try:
            chunk = sock.recv(8192)
        except socket.timeout:
            break
        if not chunk:
            break
        if first_byte:
            result.timing.ttfb_ms = (time.monotonic() - t2) * 1000
            first_byte = False
        response_data += chunk

    result.timing.transfer_ms = (time.monotonic() - t2) * 1000 - result.timing.ttfb_ms
    result.timing.total_ms = (result.timing.dns_ms + result.timing.tcp_ms +
                               result.timing.tls_ms + result.timing.ttfb_ms +
                               result.timing.transfer_ms)

    sock.close()

    # Parse response
    try:
        header_end = response_data.index(b"\r\n\r\n")
        header_part = response_data[:header_end].decode("utf-8", errors="replace")
        body_part = response_data[header_end + 4:]
    except ValueError:
        header_part = response_data.decode("utf-8", errors="replace")
        body_part = b""

    lines = header_part.split("\r\n")
    if lines:
        status_line = lines[0]
        parts = status_line.split(" ", 2)
        if len(parts) >= 2:
            try:
                result.status = int(parts[1])
            except ValueError:
                pass
            result.reason = parts[2] if len(parts) > 2 else ""

    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            result.headers[k] = v

    result.body_size = len(body_part)

    # Handle redirects
    if follow and result.status in (301, 302, 303, 307, 308) and "Location" in result.headers:
        location = result.headers["Location"]
        if not location.startswith("http"):
            location = urllib.parse.urljoin(url, location)
        result.redirects.append({"status": result.status, "url": url, "location": location})
        if len(result.redirects) < max_redirects:
            redirect_method = "GET" if result.status == 303 else method
            return do_request(location, redirect_method, headers, body, timeout, follow, max_redirects)

    return result


# Colors
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"


def color_status(status: int) -> str:
    if status < 300:
        return f"{GREEN}{status}{RESET}"
    elif status < 400:
        return f"{YELLOW}{status}{RESET}"
    else:
        return f"{RED}{status}{RESET}"


def format_ms(ms: float) -> str:
    if ms < 1:
        return f"{ms:.1f}ms"
    elif ms < 1000:
        return f"{ms:.0f}ms"
    else:
        return f"{ms/1000:.2f}s"


def bar(width: int, char: str = "█") -> str:
    return char * max(1, width)


def format_text(result: Result) -> str:
    if result.error:
        return f"{RED}Error: {result.error}{RESET}"

    t = result.timing
    total = max(t.total_ms, 1)
    max_bar = 40

    lines = [
        f"",
        f"  {BOLD}{result.method} {result.url}{RESET}",
        f"  {color_status(result.status)} {result.reason}",
        f"",
    ]

    # Timing waterfall
    phases = []
    if t.dns_ms > 0:
        phases.append(("DNS Lookup", t.dns_ms, CYAN))
    phases.append(("TCP Connection", t.tcp_ms, GREEN))
    if t.tls_ms > 0:
        phases.append(("TLS Handshake", t.tls_ms, YELLOW))
    phases.append(("Server Processing", t.ttfb_ms, CYAN))
    phases.append(("Content Transfer", t.transfer_ms, GREEN))

    for name, ms, color in phases:
        w = int((ms / total) * max_bar)
        lines.append(f"  {name:>20s}  {color}{bar(w)}{RESET}  {format_ms(ms)}")

    lines.append(f"  {'':>20s}  {'─' * max_bar}")
    lines.append(f"  {'Total':>20s}  {BOLD}{format_ms(t.total_ms)}{RESET}")
    lines.append(f"")

    # Connection info
    if result.ip:
        lines.append(f"  {DIM}IP: {result.ip}{RESET}")
    if result.tls_version:
        lines.append(f"  {DIM}TLS: {result.tls_version} ({result.tls_cipher}){RESET}")
    lines.append(f"  {DIM}Body: {result.body_size:,} bytes{RESET}")

    # Key headers
    interesting = ["Content-Type", "Server", "Cache-Control", "X-Request-Id",
                   "CF-Ray", "X-Powered-By", "Strict-Transport-Security"]
    shown = []
    for h in interesting:
        if h in result.headers:
            shown.append(f"  {DIM}{h}: {result.headers[h]}{RESET}")
    if shown:
        lines.append("")
        lines.extend(shown)

    if result.redirects:
        lines.append(f"\n  {YELLOW}Redirects:{RESET}")
        for r in result.redirects:
            lines.append(f"    {r['status']} {r['url']} → {r['location']}")

    lines.append("")
    return "\n".join(lines)


def format_json(result: Result) -> str:
    return json_mod.dumps({
        "url": result.url,
        "method": result.method,
        "status": result.status,
        "reason": result.reason,
        "ip": result.ip,
        "tls": {"version": result.tls_version, "cipher": result.tls_cipher},
        "timing": {
            "dns_ms": round(result.timing.dns_ms, 1),
            "tcp_ms": round(result.timing.tcp_ms, 1),
            "tls_ms": round(result.timing.tls_ms, 1),
            "ttfb_ms": round(result.timing.ttfb_ms, 1),
            "transfer_ms": round(result.timing.transfer_ms, 1),
            "total_ms": round(result.timing.total_ms, 1),
        },
        "headers": result.headers,
        "body_size": result.body_size,
        "redirects": result.redirects,
        "error": result.error,
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(prog="httpstat",
                                     description="Pretty HTTP response statistics")
    parser.add_argument("url", help="URL to request")
    parser.add_argument("--method", "-X", default="GET", help="HTTP method")
    parser.add_argument("--header", "-H", action="append", default=[], help="Header (K: V)")
    parser.add_argument("--data", "-d", default=None, help="Request body")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--follow", "-L", action="store_true", help="Follow redirects")
    parser.add_argument("--timeout", "-t", type=float, default=10, help="Timeout in seconds")

    args = parser.parse_args()

    headers = {}
    for h in args.header:
        if ": " in h:
            k, v = h.split(": ", 1)
            headers[k] = v
        elif ":" in h:
            k, v = h.split(":", 1)
            headers[k] = v.lstrip()

    result = do_request(args.url, method=args.method, headers=headers,
                       body=args.data, timeout=args.timeout, follow=args.follow)

    if args.json:
        print(format_json(result))
    else:
        print(format_text(result))

    sys.exit(0 if result.status and result.status < 400 else 1)


if __name__ == "__main__":
    main()
