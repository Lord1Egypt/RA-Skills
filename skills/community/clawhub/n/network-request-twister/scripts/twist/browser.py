"""Cross-platform browser launcher.

Detects Chrome / Chromium / Edge on Windows, macOS, and Linux,
launches with --remote-debugging-port and a temporary profile.
"""

from __future__ import annotations

import os
import platform
import socket
import subprocess
import sys
import tempfile

BROWSER_CMD: dict[str, dict[str, list[str]]] = {
    "chrome": {
        "Windows": [
            "${ProgramFiles}\\Google\\Chrome\\Application\\chrome.exe",
            "${LocalAppData}\\Google\\Chrome\\Application\\chrome.exe",
        ],
        "Darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ],
        "Linux": [
            "google-chrome",
            "google-chrome-stable",
        ],
    },
    "chromium": {
        "Windows": [
            "${LocalAppData}\\Chromium\\Application\\chrome.exe",
        ],
        "Darwin": [
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ],
        "Linux": [
            "chromium",
            "chromium-browser",
        ],
    },
    "edge": {
        "Windows": [
            "${ProgramFiles(x86)}\\Microsoft\\Edge\\Application\\msedge.exe",
            "${ProgramFiles}\\Microsoft\\Edge\\Application\\msedge.exe",
        ],
        "Darwin": [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ],
        "Linux": [
            "microsoft-edge",
            "microsoft-edge-stable",
        ],
    },
}

VALID_BROWSERS = frozenset(BROWSER_CMD)


class BrowserError(Exception):
    """Raised when browser detection or launch fails."""


class Browser:
    """Manages a single browser process for CDP interception."""

    def __init__(self, launch: bool = False, port: int = 9222) -> None:
        self._launch = launch
        self._port = port
        self._process: subprocess.Popen[bytes] | None = None
        self._tmp_dir: str | None = None

    @property
    def launched(self) -> bool:
        return self._launch

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(
        self,
        browser_type: str = "chrome",
        extra_args: list[str] | None = None,
        url: str = "",
    ) -> None:
        """Launch the browser if self._launch is True; no-op otherwise."""
        if not self._launch:
            return

        if browser_type not in VALID_BROWSERS:
            raise BrowserError(
                f"unknown browser {browser_type!r}; "
                f"expected one of {sorted(VALID_BROWSERS)}"
            )

        self._check_port()

        exe = _find_executable(browser_type)
        if exe is None:
            raise BrowserError(
                f"browser {browser_type!r} not found; "
                f"install Chrome, Chromium, or Edge"
            )

        self._tmp_dir = tempfile.mkdtemp(prefix="twist-browser-")

        args = [
            exe,
            f"--remote-debugging-port={self._port}",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
            f"--user-data-dir={self._tmp_dir}",
        ]
        if extra_args:
            args.extend(extra_args)
        if url:
            args.append(url)

        self._process = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        """Terminate the browser process, if launched."""
        if self._process is not None and self._process.poll() is None:
            self._process.kill()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
        self._process = None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _check_port(self) -> None:
        """Raise BrowserError if port is already in use."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", self._port))
        except OSError:
            raise BrowserError(
                f"port {self._port} is already in use"
            ) from None
        finally:
            sock.close()


# ------------------------------------------------------------------
# Executable discovery
# ------------------------------------------------------------------


def _find_executable(browser_type: str) -> str | None:
    system = platform.system()
    candidates = BROWSER_CMD.get(browser_type, {}).get(system, [])

    for raw in candidates:
        path = os.path.expandvars(raw)
        if system == "Windows":
            if os.path.isfile(path):
                return path
        else:
            # Use which-like lookup on Unix
            import shutil
            resolved = shutil.which(path)
            if resolved:
                return resolved
    return None
