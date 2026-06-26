#!/usr/bin/env python3
"""
save_archetype.py — Register or update a resume archetype in config.json.

Usage:
    python3 save_archetype.py \
        --name NAME \
        --keywords "kw1,kw2,kw3" \
        --resume-path PATH \
        [--resume-url URL] \
        [--config-file PATH]

Loads config.json, upserts the archetype (update if name exists, append if new),
writes the updated config back, and prints a status JSON object.

Exits 0 on success, exits 1 on failure.
"""

import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_CONFIG_PATH = "~/.job-search/config.json"


def load_config(config_path: Path) -> dict:
    """Load config JSON. Returns empty config scaffold if file missing."""
    if not config_path.exists():
        return {"archetypes": []}
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config_path: Path, config: dict) -> None:
    """Write config JSON, creating parent dirs as needed."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Register or update a resume archetype in config.json."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Archetype name (slug, e.g. 'mle' or 'data-scientist')",
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help="Comma-separated keywords for this archetype",
    )
    parser.add_argument(
        "--resume-path",
        required=True,
        help="Local path to the tailored resume markdown file",
    )
    parser.add_argument(
        "--resume-url",
        default="",
        help="Optional public URL for the resume (e.g. Google Docs link)",
    )
    parser.add_argument(
        "--config-file",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to config.json (default: {DEFAULT_CONFIG_PATH})",
    )
    args = parser.parse_args()

    config_path = Path(os.path.expanduser(args.config_file))

    # Parse keywords — strip whitespace, drop empties
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]

    # Build archetype record
    archetype = {
        "name": args.name.strip(),
        "keywords": keywords,
        "resume_path": args.resume_path.strip(),
        "resume_url": args.resume_url.strip(),
    }

    # Load config (creates new if missing)
    try:
        config = load_config(config_path)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "config_parse_error", "message": str(e)}))
        sys.exit(1)
    except OSError as e:
        print(json.dumps({"error": "config_read_error", "message": str(e)}))
        sys.exit(1)

    # Ensure archetypes list exists
    if "archetypes" not in config or not isinstance(config["archetypes"], list):
        config["archetypes"] = []

    # Upsert: find existing archetype by name
    existing_index = next(
        (i for i, a in enumerate(config["archetypes"]) if a.get("name") == archetype["name"]),
        None,
    )

    action = "updated" if existing_index is not None else "added"
    if existing_index is not None:
        config["archetypes"][existing_index] = archetype
    else:
        config["archetypes"].append(archetype)

    # Save updated config
    try:
        save_config(config_path, config)
    except OSError as e:
        print(json.dumps({"error": "config_write_error", "message": str(e)}))
        sys.exit(1)

    print(json.dumps({"status": "saved", "action": action, "name": archetype["name"]}))
    sys.exit(0)


if __name__ == "__main__":
    main()
