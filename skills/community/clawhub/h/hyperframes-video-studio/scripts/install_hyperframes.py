#!/usr/bin/env python3
"""Check or locally install the Hyperframes CLI for Video Studio."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / ".cache"
NPM_PREFIX = CACHE_DIR / "npm"
LOCAL_BIN = NPM_PREFIX / "node_modules" / ".bin"


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _local_hyperframes() -> Path:
    return LOCAL_BIN / ("hyperframes.cmd" if sys.platform == "win32" else "hyperframes")


def find_hyperframes() -> str | None:
    local = _local_hyperframes()
    if local.exists():
        return str(local.resolve())
    return shutil.which("hyperframes")


def check() -> dict:
    npm = shutil.which("npm")
    node = shutil.which("node")
    hyperframes = find_hyperframes()
    return {
        "status": "ok" if hyperframes else "missing",
        "node": node,
        "npm": npm,
        "hyperframes": hyperframes,
        "local_prefix": str(NPM_PREFIX.resolve()),
        "local_bin": str(_local_hyperframes().resolve()),
        "install_command": f'npm install --prefix "{NPM_PREFIX.resolve()}" hyperframes',
        "safe": {
            "uses_sudo": False,
            "global_install": False,
            "modifies_path": False,
        },
        "message": "Hyperframes CLI is available." if hyperframes else "Hyperframes CLI is missing. Ask the user before local installation.",
    }


def install() -> dict:
    current = check()
    if current["status"] == "ok":
        current["installed"] = False
        return current
    if not current["npm"] or not current["node"]:
        return {
            "status": "dependency_missing",
            "message": "Node.js and npm are required before Hyperframes can be installed locally.",
            "node": current["node"],
            "npm": current["npm"],
        }

    NPM_PREFIX.mkdir(parents=True, exist_ok=True)
    command = ["npm", "install", "--prefix", str(NPM_PREFIX), "hyperframes"]
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        return {
            "status": "install_failed",
            "message": "Local Hyperframes install failed.",
            "command": command,
            "stdout": exc.stdout[-2000:],
            "stderr": exc.stderr[-2000:],
        }

    result = check()
    result["installed"] = True
    result["stdout"] = completed.stdout[-2000:]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or install Hyperframes locally inside .cache/npm.")
    parser.add_argument("--install", action="store_true", help="Install Hyperframes locally. Only run after user confirmation.")
    args = parser.parse_args()
    result = install() if args.install else check()
    _print(result)
    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
