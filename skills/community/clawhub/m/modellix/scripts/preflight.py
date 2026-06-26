#!/usr/bin/env python3
"""
Cross-platform preflight check for CLI-first routing.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Modellix CLI and API key readiness.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    notes: list[str] = []
    cli_available = shutil.which("modellix-cli") is not None
    if not cli_available:
        notes.append("modellix-cli not found. Using REST fallback. Recommend user install: npm i -g modellix-cli@latest")

    api_key_available = bool((os.getenv("MODELLIX_API_KEY") or "").strip())
    if not api_key_available:
        notes.append("MODELLIX_API_KEY is not set. Configure it or pass --api-key per command.")

    recommended_mode = "rest"
    if cli_available and api_key_available:
        recommended_mode = "cli"
        notes.append("CLI path is available. Canonical commands: model invoke -> task get.")
    elif api_key_available:
        notes.append("REST fallback is available because API key exists (supported path).")
    else:
        notes.append("Neither CLI-auth nor REST-auth is ready. Configure API key first.")

    result = {
        "cli_available": cli_available,
        "cli_missing": not cli_available,
        "api_key_available": api_key_available,
        "recommended_mode": recommended_mode,
        "notes": notes,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"cli_available      : {result['cli_available']}")
        print(f"api_key_available  : {result['api_key_available']}")
        print(f"recommended_mode   : {result['recommended_mode']}")
        if notes:
            print("notes:")
            for note in notes:
                print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
