#!/usr/bin/env python3
"""
Lightpanda Web Scraper — Fast headless browser for OSINT and recon.
Replaces Playwright/Chromium with 0.5s page loads (vs 45s).

Usage:
  python3 lp-scrape.py URL                           # Markdown dump
  python3 lp-scrape.py URL --links                    # Extract all links
  python3 lp-scrape.py URL --html                     # Raw HTML
  python3 lp-scrape.py URL --frames                   # Include iframes
  python3 lp-scrape.py URL --js "document.title"      # Evaluate JS
  python3 lp-scrape.py URL --output /tmp/page.md      # Save to file
  python3 lp-scrape.py URL --wait networkidle         # Wait for network idle
  python3 lp-scrape.py URL --strip js,css             # Strip resource types
  python3 lp-scrape.py URL --proxy socks5://host:port # Use proxy
  python3 lp-scrape.py --serve --port 9222            # CDP server mode
  python3 lp-scrape.py --mcp                          # Start MCP server
"""

import subprocess
import sys
import os
import json
import argparse

LIGHTPANDA = os.path.expanduser("~/.local/bin/lightpanda")


def run_fetch(url, dump="markdown", frames=False, wait="networkidle",
              strip=None, proxy=None, js=None, output=None, timeout=30):
    """Run Lightpanda fetch command."""
    cmd = [LIGHTPANDA, "fetch", "--dump", dump, "--wait-until", wait]

    if frames:
        cmd.append("--with-frames")
    if strip:
        cmd.extend(["--strip-mode", strip])
    if proxy:
        cmd.extend(["--http-proxy", proxy])

    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    if result.returncode != 0:
        return None, result.stderr.strip()

    return result.stdout.strip(), None


def extract_links(url, proxy=None, timeout=30):
    """Extract all links from a page."""
    cmd = [LIGHTPANDA, "fetch", "--dump", "html", "--wait-until", "networkidle"]
    if proxy:
        cmd.extend(["--http-proxy", proxy])
    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        return [], result.stderr.strip()

    import re
    links = re.findall(r'href=["\']([^"\']+)["\']', result.stdout)
    return list(set(links)), None


def run_js(url, script, timeout=30):
    """Evaluate JavaScript on a page via CDP server mode."""
    import time
    import json

    # Start CDP server
    server = subprocess.Popen(
        [LIGHTPANDA, "serve", "--host", "127.0.0.1", "--port", "9223"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(1)

    try:
        import websocket
        import urllib.request

        # Get websocket URL
        resp = urllib.request.urlopen("http://127.0.0.1:9223/json/version")
        data = json.loads(resp.read())
        ws_url = data.get("webSocketDebuggerUrl")

        if not ws_url:
            return None, "No websocket URL"

        ws = websocket.create_connection(ws_url)

        # Navigate
        ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        ws.recv()
        time.sleep(2)

        # Evaluate JS
        ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": script}}))
        result = json.loads(ws.recv())
        ws.close()

        value = result.get("result", {}).get("result", {}).get("value")
        return value, None

    except ImportError:
        return None, "pip install websocket-client"
    finally:
        server.terminate()


def main():
    parser = argparse.ArgumentParser(description="Lightpanda fast web scraper")
    parser.add_argument("url", nargs="?", help="URL to scrape")
    parser.add_argument("--links", action="store_true", help="Extract links")
    parser.add_argument("--html", action="store_true", help="Raw HTML output")
    parser.add_argument("--frames", action="store_true", help="Include iframes")
    parser.add_argument("--wait", default="networkidle", help="Wait event")
    parser.add_argument("--strip", help="Strip modes: js,css,ui,full")
    parser.add_argument("--proxy", help="HTTP proxy")
    parser.add_argument("--js", help="JavaScript to evaluate")
    parser.add_argument("--output", "-o", help="Save to file")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout seconds")
    parser.add_argument("--serve", action="store_true", help="Start CDP server")
    parser.add_argument("--port", type=int, default=9222, help="CDP server port")
    parser.add_argument("--mcp", action="store_true", help="Start MCP server (stdio)")
    args = parser.parse_args()

    if args.mcp:
        os.execv(LIGHTPANDA, [LIGHTPANDA, "mcp"])

    if args.serve:
        os.execv(LIGHTPANDA, [LIGHTPANDA, "serve", "--host", "127.0.0.1", "--port", str(args.port)])

    if not args.url:
        parser.error("URL required (unless --serve or --mcp)")

    url = args.url

    if args.links:
        links, err = extract_links(url, args.proxy, args.timeout)
        if err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
        for link in sorted(links):
            print(link)
        return

    if args.js:
        value, err = run_js(url, args.js, args.timeout)
        if err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value)
        return

    dump_type = "html" if args.html else "markdown"
    content, err = run_fetch(url, dump_type, args.frames, args.wait, args.strip, args.proxy, timeout=args.timeout)

    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            f.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
