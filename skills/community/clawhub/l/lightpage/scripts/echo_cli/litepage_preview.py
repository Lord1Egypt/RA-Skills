"""Serve the exact upload bytes at a /p/ prefix, with hosting browser policies."""

import argparse
import json
import mimetypes
import threading
import zipfile
from html import escape
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlsplit

from echo_cli.compat import ThreadingHTTPServer
from echo_cli.litepage_bundle import bundle

PREFIX = "/p/preview0/"
# Mirror the content gateway, without importing the separately installed backend.
CSP = "default-src 'self' https: data: blob:; script-src 'self' https: 'unsafe-inline' 'unsafe-eval'; style-src 'self' https: 'unsafe-inline'; connect-src 'self' https:; worker-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
PERMISSIONS = "camera=(self), microphone=(self), geolocation=()"


def server(source):
    data, inspection = bundle(source)
    with zipfile.ZipFile(BytesIO(data)) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}

    if "index.html" not in files:
        inspection["preview_note"] = (
            "Local document preview shows escaped source; Markdown is rendered by the deployed content gateway."
        )

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not log query strings or user-provided URLs.

        def do_GET(self):
            self.respond()

        def do_HEAD(self):
            self.respond(head=True)

        def respond(self, head=False):
            path = unquote(urlsplit(self.path).path)
            host = self.headers.get("Host", "")
            expected_host = f"127.0.0.1:{self.server.server_port}"
            name = path[len(PREFIX) :] if path.startswith(PREFIX) else None
            if name is not None and (not name or name.endswith("/")):
                name = next(
                    (
                        name + entry
                        for entry in ("index.html", "index.md", "index.txt")
                        if name + entry in files
                    ),
                    name + "index.html",
                )
            valid = host == expected_host and name in files
            body = files[name] if valid else b"Not found (no root asset or SPA fallback)"
            document = valid and name in {"index.md", "index.txt"}
            if document:
                text = body.decode("utf-8")
                body = (
                    '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><pre style="white-space:pre-wrap;max-width:860px;margin:24px auto;font:16px/1.7 monospace">'
                    + escape(text)
                    + "</pre>"
                ).encode("utf-8")
            self.send_response(200 if valid else 404)
            media = (
                "text/html; charset=utf-8"
                if document
                else (mimetypes.guess_type(name or "")[0] if valid else "text/plain")
            )
            self.send_header("Content-Type", media or "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("Permissions-Policy", PERMISSIONS)
            self.end_headers()
            if not head:
                self.wfile.write(body)

    return ThreadingHTTPServer(("127.0.0.1", 0), Handler), inspection


def screenshot(httpd, output):
    """Capture only local upload assets in a fresh browser with outbound requests blocked."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(
            "Screenshot needs optional Playwright and Chromium on Python 3.9+: python3 -m pip install playwright>=1.48; python3 -m playwright install chromium"
        ) from None
    output = Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise RuntimeError("Screenshot output already exists; choose a new file")
    origin = f"http://127.0.0.1:{httpd.server_port}"
    blocked = set()
    worker = threading.Thread(target=httpd.serve_forever, daemon=True)
    worker.start()
    try:
        with sync_playwright() as engine:
            browser = engine.chromium.launch()
            try:
                context = browser.new_context(
                    viewport={"width": 1200, "height": 750},
                    device_scale_factor=1,
                    service_workers="block",
                    accept_downloads=False,
                )

                def route(request):
                    url = urlsplit(request.request.url)
                    if (
                        f"{url.scheme}://{url.netloc}" == origin
                        and url.path.startswith(PREFIX)
                        and request.request.method in {"GET", "HEAD"}
                    ):
                        request.continue_()
                    else:
                        blocked.add("external_or_write_request")
                        request.abort()

                context.route("**/*", route)
                context.route_web_socket("**/*", lambda socket: socket.close())
                page = context.new_page()
                page.goto(origin + PREFIX, wait_until="load", timeout=15000)
                page.wait_for_timeout(800)
                data = page.screenshot(type="png", animations="disabled", timeout=10000)
                with output.open("xb") as stream:
                    stream.write(data)
            finally:
                browser.close()
    finally:
        httpd.shutdown()
        worker.join(timeout=5)
    return {
        "screenshot_path": str(output),
        "width": 1200,
        "height": 750,
        "external_requests_blocked": bool(blocked),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--screenshot", type=Path, help="Save a local first-screen PNG and exit")
    parser.add_argument(
        "--seconds", type=int, default=600, help="Stop automatically (1-3600 seconds)"
    )
    args = parser.parse_args()
    if not 1 <= args.seconds <= 3600:
        parser.error("--seconds must be between 1 and 3600")
    httpd, inspection = server(args.source)
    if args.screenshot:
        try:
            print(json.dumps(screenshot(httpd, args.screenshot)), flush=True)
        finally:
            httpd.server_close()
        return
    print(
        json.dumps(
            {
                "preview_url": f"http://127.0.0.1:{httpd.server_port}{PREFIX}",
                "seconds": args.seconds,
                **inspection,
            }
        ),
        flush=True,
    )
    timer = threading.Timer(args.seconds, httpd.shutdown)
    timer.daemon = True
    timer.start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        timer.cancel()
        httpd.server_close()


if __name__ == "__main__":
    main()
