#!/usr/bin/env python3
"""
TikTok Video — generic API caller (registered endpoints)
=========================================================

Usage:
  python video_api.py '{"api": "<api_name>", "openId": "..."}'

When no dedicated script exists yet, use video_proxy.py with path/method/ttsAccessToken directly.
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api
from _video_endpoints import list_api_names


def main() -> None:
    if len(sys.argv) < 2:
        names = list_api_names()
        hint = ", ".join(names) if names else "(none yet — use video_proxy.py or wait for endpoint docs)"
        print(f"Usage: video_api.py '<JSON with api field>'\nAvailable: {hint}", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    if not params.get("api"):
        print("Missing required field: api", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(run_video_api(str(params["api"]), params, "video_api.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
