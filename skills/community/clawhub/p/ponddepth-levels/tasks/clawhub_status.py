#!/usr/bin/env python3
"""Write ClawHub login status into Control UI assets for B2 UX.

Outputs:
- clawhub-status.json into OpenClaw Control UI assets dir

Env:
- OPENCLAW_UI_ASSETS_DIR (optional)
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
from pathlib import Path


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def assets_dir() -> Path:
    env = os.environ.get("OPENCLAW_UI_ASSETS_DIR")
    if env:
        return Path(env).expanduser()
    return Path("/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets")


def main() -> None:
    out = {"schemaVersion": 1, "updatedAt": now_iso(), "loggedIn": False, "user": None, "error": None}
    try:
        cp = subprocess.run(["clawhub", "whoami"], text=True, capture_output=True, timeout=20)
        if cp.returncode == 0:
            out["loggedIn"] = True
            out["user"] = (cp.stdout or "").strip().splitlines()[-1].strip()
        else:
            out["error"] = ((cp.stderr or cp.stdout) or "").strip()[:500]
    except Exception as e:
        out["error"] = repr(e)[:500]

    d = assets_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / "clawhub-status.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {p}")


if __name__ == "__main__":
    main()
