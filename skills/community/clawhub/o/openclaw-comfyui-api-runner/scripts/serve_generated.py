"""
Serve the skill's generated/ folder over HTTP with a browse/delete UI.
Run from skill root. Auto-exits after 5 minutes (COMFYUI_SERVE_TIMEOUT_SEC); GET /reset-timer resets the timer.
Port: COMFYUI_SERVE_PORT (default 8765).
When run normally, spawns the server in a subprocess and prints JSON success then exits so the agent gets immediate feedback.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path
from subprocess import DEVNULL, Popen
from urllib.parse import parse_qs, urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PORT = 8765
DEFAULT_TIMEOUT_SEC = 300
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov", ".avi", ".mkv"}
MIME_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
    ".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime",
    ".avi": "video/x-msvideo", ".mkv": "video/x-matroska",
}


def _safe_path(generated_dir: Path, filename: str) -> Path | None:
    """Resolve filename under generated_dir; return None if invalid (path traversal)."""
    if not filename or "/" in filename or "\\" in filename or ".." in filename:
        return None
    resolved = (generated_dir / filename).resolve()
    try:
        resolved.relative_to(generated_dir.resolve())
    except ValueError:
        return None
    return resolved if resolved.is_file() else None


class GeneratedHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass  # Suppress default request logging

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query)
        generated_dir: Path = self.server.generated_dir  # type: ignore[attr-defined]

        # Reset timer (also used by serve_status.py)
        if path == "/reset-timer":
            self._reset_timer()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        # Delete file then redirect to /
        if path == "/delete":
            file_param = query.get("file", [None])[0]
            safe = _safe_path(generated_dir, file_param) if file_param else None
            if safe:
                try:
                    safe.unlink()
                except OSError:
                    pass
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        # Serve a file under /files/<filename>
        if path.startswith("/files/"):
            filename = path[7:].lstrip("/").split("/")[0]
            safe = _safe_path(generated_dir, filename)
            if safe:
                self.send_response(200)
                mime = MIME_TYPES.get(safe.suffix.lower(), "application/octet-stream")
                self.send_header("Content-Type", mime)
                self.send_header("Content-Disposition", f'inline; filename="{filename}"')
                self.end_headers()
                self.wfile.write(safe.read_bytes())
                return
            self.send_response(404)
            self.end_headers()
            return

        # Index: carousel of media (sorted by date, newest first)
        if path == "/":
            try:
                files_with_mtime = [
                    (f.name, f.stat().st_mtime)
                    for f in generated_dir.iterdir()
                    if f.is_file() and f.suffix.lower() in MEDIA_EXTENSIONS
                ]
                files = [n for n, _ in sorted(files_with_mtime, key=lambda x: -x[1])]
            except OSError:
                files = []
            html = self._carousel_html(files)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def _carousel_html(self, files: list[str]) -> str:
        if not files:
            return (
                "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Generated</title></head>"
                "<body style='font-family:sans-serif;padding:2rem;'><h1>Generated</h1><p>No media yet.</p></body></html>"
            )
        ext = Path(files[0]).suffix.lower()
        is_video = ext in {".mp4", ".webm", ".mov", ".avi", ".mkv"}
        files_js = ",".join(repr(f) for f in files)
        initial_media = (
            f'<video src="/files/{files[0]}" controls style="max-width:100%;max-height:70vh;"></video>'
            if is_video
            else f'<img src="/files/{files[0]}" alt="" style="max-width:100%;max-height:70vh;display:block;">'
        )
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Generated</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 0; padding: 1rem; background: #1a1a1a; color: #eee; }}
  .toolbar {{ display: flex; align-items: center; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }}
  .toolbar a, .toolbar button {{ padding: 0.5rem 1rem; text-decoration: none; color: #eee; background: #333; border: 1px solid #555; border-radius: 4px; cursor: pointer; font-size: 1rem; }}
  .toolbar a:hover, .toolbar button:hover {{ background: #444; }}
  .counter {{ margin-left: auto; }}
  .viewer > * {{ border-radius: 6px; }}
</style></head>
<body>
  <h1>Generated</h1>
  <div class="viewer" id="mediaWrap">{initial_media}</div>
  <div class="toolbar">
    <button id="prev">← Prev</button>
    <button id="next">Next →</button>
    <a id="download" href="/files/{files[0]}" download="{files[0]}">Download</a>
    <button id="del">Delete</button>
    <span class="counter" id="counter">1 / {len(files)}</span>
  </div>
  <script>
    const files = [{files_js}];
    let i = 0;
    const wrap = document.getElementById("mediaWrap");
    const download = document.getElementById("download");
    const counter = document.getElementById("counter");
    const isVideo = (f) => /\\.(mp4|webm|mov|avi|mkv)$/i.test(f);
    function show() {{
      const f = files[i];
      if (isVideo(f))
        wrap.innerHTML = '<video src="/files/' + f.replace(/"/g, '&quot;') + '" controls style="max-width:100%;max-height:70vh;"></video>';
      else
        wrap.innerHTML = '<img src="/files/' + f.replace(/"/g, '&quot;') + '" alt="" style="max-width:100%;max-height:70vh;display:block;">';
      download.href = "/files/" + encodeURIComponent(f);
      download.download = f;
      counter.textContent = (i + 1) + " / " + files.length;
    }}
    document.getElementById("prev").onclick = () => {{ if (files.length) {{ i = (i - 1 + files.length) % files.length; show(); }} }};
    document.getElementById("next").onclick = () => {{ if (files.length) {{ i = (i + 1) % files.length; show(); }} }};
    document.getElementById("del").onclick = () => {{
      if (!files.length || !confirm("Delete " + files[i] + "?")) return;
      window.location.href = "/delete?file=" + encodeURIComponent(files[i]);
    }};
  </script>
</body></html>"""

    def _reset_timer(self) -> None:
        server = self.server
        lock: threading.Lock = server.shutdown_lock  # type: ignore[attr-defined]
        timeout_sec: int = server.shutdown_timeout_sec  # type: ignore[attr-defined]
        with lock:
            old = getattr(server, "shutdown_timer", None)
            if old is not None:
                old.cancel()
            t = threading.Timer(timeout_sec, server.shutdown)
            t.daemon = True
            server.shutdown_timer = t  # type: ignore[attr-defined]
            t.start()


def run_server(port: int, timeout_sec: int) -> None:
    """Run the HTTP server (blocking). Used by the daemon subprocess."""
    generated = SKILL_ROOT / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    server = HTTPServer(("0.0.0.0", port), GeneratedHandler)
    server.generated_dir = generated  # type: ignore[attr-defined]
    server.shutdown_lock = threading.Lock()  # type: ignore[attr-defined]
    server.shutdown_timeout_sec = timeout_sec  # type: ignore[attr-defined]
    server.shutdown_timer = None  # type: ignore[attr-defined]
    t = threading.Timer(timeout_sec, server.shutdown)
    t.daemon = True
    server.shutdown_timer = t  # type: ignore[attr-defined]
    t.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def main() -> int:
    port = int(os.environ.get("COMFYUI_SERVE_PORT", str(DEFAULT_PORT)))
    timeout_sec = int(os.environ.get("COMFYUI_SERVE_TIMEOUT_SEC", str(DEFAULT_TIMEOUT_SEC)))
    url = f"http://127.0.0.1:{port}/"

    # If we are the daemon subprocess, run the server (blocking) and exit when server stops.
    if os.environ.get("COMFYUI_SERVE_DAEMON") == "1":
        run_server(port, timeout_sec)
        return 0

    # Otherwise: spawn daemon subprocess, wait for it to bind, print JSON success, exit so the agent gets immediate response.
    env = {**os.environ, "COMFYUI_SERVE_DAEMON": "1"}
    child = Popen(
        [sys.executable, __file__],
        cwd=str(SKILL_ROOT),
        env=env,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    time.sleep(0.3)
    if child.poll() is not None:
        out = {
            "status": "serve_started",
            "success": False,
            "error": "Server process exited immediately.",
        }
        print(json.dumps(out), flush=True)
        return 1
    out = {
        "status": "serve_started",
        "success": True,
        "url": url,
        "port": port,
        "message": f"Server started. Available at {url} for the next {timeout_sec // 60} minutes.",
    }
    print(json.dumps(out), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
