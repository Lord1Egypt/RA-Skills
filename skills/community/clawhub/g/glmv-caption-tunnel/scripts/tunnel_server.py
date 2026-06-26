"""
Local file tunnel via Cloudflare Quick Tunnel.

Exposes local files through a temporary HTTP server + cloudflared tunnel,
producing public HTTPS URLs usable by remote APIs (e.g., ZhiPu GLM-V).

Usage:
    from tunnel_server import LocalTunnel

    with LocalTunnel(['/path/to/video.mp4', '/path/to/doc.pdf']) as tunnel:
        video_url = tunnel.get_url('/path/to/video.mp4')
        doc_url = tunnel.get_url('/path/to/doc.pdf')
        # video_url and doc_url are now public HTTPS URLs
"""

import os
import sys
import time
import socket
import tempfile
import threading
import subprocess
import shutil
import re
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional, List, Dict
from urllib.parse import quote


def find_free_port() -> int:
    """Find an available port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def find_cloudflared() -> Optional[str]:
    """Find the cloudflared binary on the system."""
    # Check PATH first
    cf = shutil.which("cloudflared")
    if cf:
        return cf

    # Check common install locations
    if sys.platform == "win32":
        common = [
            r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
            r"C:\Program Files\cloudflared\cloudflared.exe",
            os.path.expanduser(
                r"~\AppData\Local\Microsoft\WinGet\Links\cloudflared.exe"
            ),
            os.path.expanduser(r"~\AppData\Local\cloudflared\cloudflared.exe"),
        ]
    else:
        common = [
            "/usr/local/bin/cloudflared",
            "/usr/bin/cloudflared",
            os.path.expanduser("~/.local/bin/cloudflared"),
            os.path.expanduser("~/cloudflared"),
        ]

    for p in common:
        if os.path.isfile(p):
            return p
    return None


class _QuietHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves a specific directory with no logging."""

    def log_message(self, format, *args):
        pass


def _make_handler(serve_dir: str):
    """Create a handler class bound to serve_dir."""

    class Handler(_QuietHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=serve_dir, **kwargs)

    return Handler


class LocalTunnel:
    """
    Context manager: exposes local files via HTTP server + cloudflare quick tunnel.

    On enter:
      1. Creates a temp directory
      2. Symlinks (or copies) files into it  -- only the given files are exposed
      3. Starts a Python HTTP server on a random port
      4. Starts ``cloudflared tunnel --url http://localhost:<port>``
      5. Waits for the public URL to appear in cloudflared output

    On exit:
      1. Terminates cloudflared
      2. Shuts down HTTP server
      3. Removes temp directory
    """

    def __init__(self, file_paths: List[str]):
        self._resolved: List[str] = [str(Path(f).resolve()) for f in file_paths]
        self._temp_dir: Optional[str] = None
        self._http_server: Optional[HTTPServer] = None
        self._http_thread: Optional[threading.Thread] = None
        self._http_port: Optional[int] = None
        self._cf_process: Optional[subprocess.Popen] = None
        self._cf_binary: Optional[str] = None
        self._tunnel_base: Optional[str] = None
        self._name_map: Dict[str, str] = {}

    def __enter__(self):
        self._setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()
        return False

    @property
    def tunnel_url(self) -> str:
        if not self._tunnel_base:
            raise RuntimeError("Tunnel not established")
        return self._tunnel_base

    def get_url(self, file_path: str) -> str:
        resolved = str(Path(file_path).resolve())
        name = self._name_map.get(resolved)
        if name is None:
            raise ValueError(f"File not tracked by tunnel: {file_path}")
        return f"{self._tunnel_base}/{quote(name)}"

    def _setup(self):
        self._cf_binary = find_cloudflared()
        if not self._cf_binary:
            raise FileNotFoundError(
                "cloudflared not found. "
                "The calling agent should have checked for this before invoking the script."
            )

        # Prepare temp dir with (sym)linked files
        self._temp_dir = tempfile.mkdtemp(prefix="glmv-serve-")
        for resolved in self._resolved:
            src = Path(resolved)
            if not src.exists():
                raise FileNotFoundError(f"File not found: {resolved}")

            dest_name = src.name
            dest = os.path.join(self._temp_dir, dest_name)

            if os.path.exists(dest):
                stem, suffix = src.stem, src.suffix
                i = 1
                while os.path.exists(
                    os.path.join(self._temp_dir, f"{stem}_{i}{suffix}")
                ):
                    i += 1
                dest_name = f"{stem}_{i}{suffix}"
                dest = os.path.join(self._temp_dir, dest_name)

            try:
                os.symlink(str(src), dest)
            except (OSError, NotImplementedError):
                shutil.copy2(str(src), dest)

            self._name_map[resolved] = dest_name

        # Start HTTP server
        self._http_port = find_free_port()
        handler = _make_handler(self._temp_dir)
        self._http_server = HTTPServer(("0.0.0.0", self._http_port), handler)
        self._http_thread = threading.Thread(
            target=self._http_server.serve_forever, daemon=True
        )
        self._http_thread.start()

        # Start cloudflared quick tunnel
        cmd = [
            self._cf_binary,
            "tunnel",
            "--url",
            f"http://localhost:{self._http_port}",
        ]
        popen_kwargs: dict = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "text": True,
            "bufsize": 1,
        }
        if sys.platform == "win32":
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        self._cf_process = subprocess.Popen(cmd, **popen_kwargs)
        self._tunnel_base = self._wait_for_url(timeout=30)

    def _wait_for_url(self, timeout: int = 30) -> str:
        url_pat = re.compile(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com")
        deadline = time.time() + timeout
        process = self._cf_process
        if process is None or process.stdout is None:
            raise RuntimeError("cloudflared process did not start correctly")

        while time.time() < deadline:
            line = process.stdout.readline()
            if not line:
                rc = process.poll()
                if rc is not None:
                    raise RuntimeError(f"cloudflared exited unexpectedly (code {rc})")
                time.sleep(0.1)
                continue
            m = url_pat.search(line)
            if m:
                return m.group(0)
        raise TimeoutError(f"cloudflared tunnel URL not found within {timeout}s")

    def _cleanup(self):
        if self._cf_process and self._cf_process.poll() is None:
            try:
                self._cf_process.terminate()
                self._cf_process.wait(timeout=5)
            except Exception as e:
                print(f"[tunnel] Warning: terminate failed, killing process: {e}", file=sys.stderr)
                try:
                    self._cf_process.kill()
                except Exception as kill_error:
                    print(f"[tunnel] Warning: kill failed: {kill_error}", file=sys.stderr)

        if self._http_server:
            try:
                self._http_server.shutdown()
            except Exception as e:
                print(f"[tunnel] Warning: HTTP server shutdown failed: {e}", file=sys.stderr)

        if self._temp_dir and os.path.isdir(self._temp_dir):
            try:
                shutil.rmtree(self._temp_dir)
            except Exception as e:
                print(f"[tunnel] Warning: temp dir cleanup failed: {e}", file=sys.stderr)
