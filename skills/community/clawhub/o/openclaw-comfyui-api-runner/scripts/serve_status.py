"""
Check if the serve_generated server is running. If so, GET /reset-timer (resets 5-min auto-exit).
Run before starting the server to avoid duplicate instances.
Port: COMFYUI_SERVE_PORT (default 8765). Output: JSON with status, running, url (if running), message.
"""

from __future__ import annotations

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

DEFAULT_PORT = 8765
TIMEOUT = 2


def main() -> int:
    port = int(os.environ.get("COMFYUI_SERVE_PORT", str(DEFAULT_PORT)))
    url = f"http://127.0.0.1:{port}/"
    reset_url = f"http://127.0.0.1:{port}/reset-timer"
    try:
        req = Request(reset_url)
        with urlopen(req, timeout=TIMEOUT) as _:
            out = {
                "status": "serve_status",
                "running": True,
                "url": url,
                "message": f"Viewer already running at {url} (5-minute timer reset).",
            }
            print(json.dumps(out), flush=True)
            return 0
    except (URLError, OSError, ValueError):
        out = {
            "status": "serve_status",
            "running": False,
            "message": "Viewer not running. Start it with: python3 scripts/serve_generated.py",
        }
        print(json.dumps(out), flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
