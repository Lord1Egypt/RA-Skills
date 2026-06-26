#!/usr/bin/env python3
"""Initialize kpop-tracker config directory and files."""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: init_config.py <workspace_path>")
        print("Example: init_config.py C:/Users/heph/OpenClaw/workspace")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    tracker_dir = workspace / "kpop-tracker"
    config_path = tracker_dir / "config.json"
    history_path = tracker_dir / "check_history.json"

    # Create directory
    tracker_dir.mkdir(parents=True, exist_ok=True)

    # Create config if not exists
    if not config_path.exists():
        config = {
            "artists": [],
            "last_check": None,
            "check_history_file": "kpop-tracker/check_history.json"
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"OK: Created {config_path}")
    else:
        print(f"SKIP: {config_path} already exists")

    # Create history if not exists
    if not history_path.exists():
        history = {
            "last_check": None,
            "reported_urls": []
        }
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print(f"OK: Created {history_path}")
    else:
        print(f"SKIP: {history_path} already exists")

    print(f"\nDone! Config directory: {tracker_dir}")
    print("Next: Add artists to config.json")


if __name__ == "__main__":
    main()
