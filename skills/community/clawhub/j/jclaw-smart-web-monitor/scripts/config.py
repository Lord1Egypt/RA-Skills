#!/usr/bin/env python3
"""
Helper utilities for web-monitor skill v2.
"""

import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
MONITORS_DIR = SKILL_DIR / "monitors"


def list_enabled_monitors() -> list[dict]:
    results = []
    for f in MONITORS_DIR.glob("*.json"):
        with open(f) as fh:
            config = json.load(fh)
        if config.get("enabled", True) and config.get("state", "active") == "active":
            results.append(config)
    return results


def validate_config(config: dict) -> list[str]:
    errors = []
    for key in ["name", "urls", "match"]:
        if key not in config:
            errors.append(f"Missing required field: {key}")

    if "match" in config:
        m = config["match"]
        if "type" not in m:
            errors.append("match.type is required")
        elif m["type"] not in ("keyword", "regex", "css", "jsonpath", "llm"):
            errors.append(f"Invalid match type: {m['type']}")
        if "value" not in m:
            errors.append("match.value is required")

    if "urls" in config:
        if not isinstance(config["urls"], list) or len(config["urls"]) == 0:
            errors.append("urls must be a non-empty list")
        for i, u in enumerate(config["urls"]):
            if "url" not in u:
                errors.append(f"urls[{i}] missing 'url' field")

    if "state" in config:
        if config["state"] not in ("active", "paused", "disabled"):
            errors.append(f"Invalid state: {config['state']}")

    return errors
