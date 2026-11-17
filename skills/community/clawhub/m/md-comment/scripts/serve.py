#!/usr/bin/env python3
"""commentmd - open a browser for the user to comment on a Markdown file."""

import hashlib
from pathlib import Path


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


import socket


def find_free_port(start: int, end: int) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError(f"No free port in [{start}, {end}]")


import json


def build_page_data(md_path: Path) -> dict:
    md_path = md_path.resolve()
    content = md_path.read_text(encoding="utf-8")
    return {
        "md_file": str(md_path),
        "md_name": md_path.name,
        "md_content": content,
        "md_sha256": compute_sha256(md_path),
    }


def resolve_output_path(md_path: Path, out_arg):
    if out_arg is not None:
        return out_arg
    return md_path.with_suffix(".comments.json")


_SENTINEL = "/* __DATA_INJECTION__ */"


def inject_template(html_template: str, data: dict, mode: str) -> str:
    # json.dumps escapes </ so a literal </script> can't leak into the JS
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    mode_js = json.dumps(mode)
    block = f'window.__DATA__ = {payload};\nwindow.__MODE__ = {mode_js};'
    if _SENTINEL in html_template:
        return html_template.replace(_SENTINEL, block)
    injection = f'<script>\n{block}\n</script>\n</head>'
    return html_template.replace("</head>", injection, 1)


import argparse
import sys
import threading
import time
import webbrowser
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler


DEFAULT_PORT_START = 3118
DEFAULT_PORT_END = 3128


def write_output_json(payload: dict, out_path: Path, md_file: str, md_sha256_initial: str, md_sha256_current: str) -> dict:
    comments = payload.get("comments") or []
    result = {
        "schema_version": 1,
        "md_file": md_file,
        "md_sha256": md_sha256_initial,
        "md_changed_during_review": md_sha256_current != md_sha256_initial,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "comment_count": len(comments),
        "comments": comments,
    }
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


class _Handler(BaseHTTPRequestHandler):
    # attributes injected via server.context
    def _ctx(self):
        return self.server.context  # type: ignore[attr-defined]

    def log_message(self, format, *args):  # silence default access log
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = self._ctx()["html"].encode("utf-8")
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/finish":
            self.send_error(404)
            return
        ctx = self._ctx()
        # Reject cross-origin CSRF and DNS-rebinding attempts. Simple POSTs
        # from other pages can hit 127.0.0.1 but Origin is always set by the
        # browser to their own origin, never to ours. Also blocks
        # application/x-www-form-urlencoded and text/plain, which are simple
        # requests that skip preflight.
        origin = self.headers.get("origin")
        expected = f"http://127.0.0.1:{ctx['port']}"
        if origin != expected:
            self.send_error(403, "bad origin")
            return
        ctype = (self.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self.send_error(415, "content-type must be application/json")
            return
        length = int(self.headers.get("content-length", "0"))
        if length > 1_048_576:
            self.send_error(413, "payload too large")
            return
        try:
            payload = json.loads(self.rfile.read(length))
        except json.JSONDecodeError as e:
            self.send_error(400, f"bad json: {e}")
            return
        try:
            current_sha = compute_sha256(ctx["md_path"])
        except OSError:
            current_sha = ""  # file gone; treat as changed
        result = write_output_json(payload, ctx["out_path"], ctx["md_file"], ctx["md_sha256"], current_sha)
        body = json.dumps({"ok": True, "path": str(ctx["out_path"]), "comment_count": result["comment_count"]}).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        threading.Thread(target=self._shutdown_soon, daemon=True).start()

    def _shutdown_soon(self):
        time.sleep(0.2)
        self.server.shutdown()


def _load_viewer_html() -> str:
    here = Path(__file__).resolve().parent
    return (here.parent / "assets" / "viewer.html").read_text(encoding="utf-8")


def write_static_html(md_path: Path, out_html: Path) -> None:
    data = build_page_data(md_path)
    template = _load_viewer_html()
    out_html.write_text(inject_template(template, data, mode="static"), encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="commentmd - comment on a markdown file in the browser.")
    parser.add_argument("md_path", type=Path, help="Path to the markdown file to review.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT_START)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--static", dest="static_out", type=Path, default=None,
                        help="Write a standalone HTML to this path and exit (no server).")
    args = parser.parse_args(argv)

    md_path = args.md_path.resolve()
    if not md_path.is_file():
        print(f"error: not a file: {md_path}", file=sys.stderr)
        return 1

    if args.static_out is not None:
        write_static_html(md_path, args.static_out.resolve())
        print(f"wrote {args.static_out.resolve()}")
        return 0

    data = build_page_data(md_path)
    out_path = resolve_output_path(md_path, args.out).resolve()
    html_template = _load_viewer_html()
    html = inject_template(html_template, data, mode="server")

    try:
        port = find_free_port(args.port, DEFAULT_PORT_END)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    server = HTTPServer(("127.0.0.1", port), _Handler)
    server.context = {  # type: ignore[attr-defined]
        "html": html,
        "out_path": out_path,
        "md_file": data["md_file"],
        "md_sha256": data["md_sha256"],
        "md_path": md_path,
        "port": port,
    }

    url = f"http://127.0.0.1:{port}/"
    print(f"commentmd serving {md_path.name} at {url}")
    print(f"  output: {out_path}")
    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("interrupted; no JSON written.", file=sys.stderr)
        return 130
    finally:
        server.server_close()

    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
