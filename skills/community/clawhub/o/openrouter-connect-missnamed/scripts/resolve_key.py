#!/usr/bin/env python3
"""
resolve_key.py — Print the resolved OPENROUTER_API_KEY or exit with an error.
Used by the openrouter-connect skill to verify the key exists before proceeding.
"""
import os
import sys
from pathlib import Path


def load_dotenv_simple(path: Path) -> dict:
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        result[key.strip()] = val.strip().strip("\"'")
    return result


def main():
    env = {}

    # 1. Global ~/.env
    env.update(load_dotenv_simple(Path.home() / ".env"))

    # 2. Project .env (overrides global)
    env.update(load_dotenv_simple(Path(".env")))

    # 3. Shell environment (highest priority)
    env.update(os.environ)

    key = env.get("OPENROUTER_API_KEY", "").strip()

    if not key:
        print(
            "ERROR: OPENROUTER_API_KEY not found.\n"
            "Add it to ./.env or ~/.env:\n\n"
            "  OPENROUTER_API_KEY=sk-or-...\n\n"
            "Get a free key at https://openrouter.ai/keys",
            file=sys.stderr,
        )
        sys.exit(1)

    # Print masked version so the skill can confirm it's there
    masked = key[:8] + "..." + key[-4:]
    print(f"OK: OPENROUTER_API_KEY found ({masked})")


if __name__ == "__main__":
    main()
