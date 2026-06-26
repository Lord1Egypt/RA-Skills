#!/usr/bin/env python3
"""Update openclaw.json to add claude-cli provider for oauth-coder bridge."""

import json
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"

MODELS = [
    {"id": "claude-opus-4-6", "name": "Claude Opus 4.6 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-opus-4-5", "name": "Claude Opus 4.5 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-opus-4-1", "name": "Claude Opus 4.1 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-opus-4-0", "name": "Claude Opus 4.0 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-sonnet-4-5", "name": "Claude Sonnet 4.5 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-sonnet-4-0", "name": "Claude Sonnet 4.0 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5 (claude-cli)", "contextWindow": 200000},
    {"id": "claude-3-7-sonnet-latest", "name": "Claude 3.7 Sonnet (claude-cli)", "contextWindow": 200000},
    {"id": "claude-3-5-sonnet-latest", "name": "Claude 3.5 Sonnet (claude-cli)", "contextWindow": 200000},
    {"id": "claude-3-5-haiku-latest", "name": "Claude 3.5 Haiku (claude-cli)", "contextWindow": 200000},
]

def main():
    if not CONFIG_PATH.exists():
        print(f"Error: {CONFIG_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    config.setdefault("models", {}).setdefault("providers", {})

    config["models"]["providers"]["claude-cli"] = {
        "baseUrl": "http://127.0.0.1:8787",
        "apiKey": "local-bridge-no-key-needed",
        "api": "anthropic-messages",
        "models": [
            {
                "id": m["id"],
                "name": m["name"],
                "reasoning": True,
                "input": ["text"],
                "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                "contextWindow": m["contextWindow"],
                "maxTokens": 8192,
            }
            for m in MODELS
        ],
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Updated {CONFIG_PATH}")
    print(f"Added claude-cli provider with {len(MODELS)} models")

if __name__ == "__main__":
    main()
