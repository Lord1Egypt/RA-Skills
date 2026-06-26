#!/usr/bin/env python3
"""
load_config.py — Read and print the job-search config as JSON.

Usage:
    python3 load_config.py [--config-file PATH]

Exits 0 on success (prints config JSON).
Exits 1 if config file is missing or unreadable (prints error JSON).
"""

import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_CONFIG_PATH = "~/.job-search/config.json"


def main():
    parser = argparse.ArgumentParser(
        description="Load and print job-search config as JSON."
    )
    parser.add_argument(
        "--config-file",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to config.json (default: {DEFAULT_CONFIG_PATH})",
    )
    args = parser.parse_args()

    config_path = Path(os.path.expanduser(args.config_file))

    if not config_path.exists():
        error = {
            "error": "config_not_found",
            "path": str(config_path),
            "message": (
                f"Config file not found at {config_path}. "
                "Run first-time setup to create it."
            ),
        }
        print(json.dumps(error))
        sys.exit(1)

    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        error = {
            "error": "config_parse_error",
            "path": str(config_path),
            "message": f"Failed to parse config JSON: {e}",
        }
        print(json.dumps(error))
        sys.exit(1)
    except OSError as e:
        error = {
            "error": "config_read_error",
            "path": str(config_path),
            "message": f"Failed to read config file: {e}",
        }
        print(json.dumps(error))
        sys.exit(1)

    print(json.dumps(config, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
