#!/usr/bin/env python3
"""export-config.py — Export a redacted OpenClaw config for backup.

Uses `openclaw config get <section>` to export each config section.
OpenClaw itself redacts sensitive fields (tokens, secrets, keys) as
"__OPENCLAW_REDACTED__" — so this script delegates redaction entirely
to the authoritative source rather than maintaining its own list.

Replaces "__OPENCLAW_REDACTED__" with "[REDACTED]" for cleaner output.

Usage:
    python3 export-config.py <output-path>

Note: requires the `openclaw` CLI to be on $PATH and the gateway running.
Falls back to raw config file redaction if the CLI is unavailable.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Top-level config sections to export
CONFIG_SECTIONS = [
    "agents", "channels", "auth", "plugins", "skills",
    "commands", "session", "gateway", "messages", "meta", "wizard",
]

OPENCLAW_REDACTED = "__OPENCLAW_REDACTED__"


def scrub(obj):
    """Replace OpenClaw's internal redaction marker with a clean [REDACTED]."""
    if isinstance(obj, str):
        return "[REDACTED]" if obj == OPENCLAW_REDACTED else obj
    elif isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [scrub(i) for i in obj]
    return obj


def export_via_cli() -> dict:
    """Build a full config dict by querying each section via openclaw config get."""
    result = {}
    for section in CONFIG_SECTIONS:
        try:
            proc = subprocess.run(
                ["openclaw", "config", "get", section, "--json"],
                capture_output=True, text=True, timeout=10,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                result[section] = json.loads(proc.stdout)
        except Exception:
            continue
    return result


def export_via_file(config_path: Path) -> dict:
    """
    Fallback: read raw config file and apply conservative key-name redaction.
    Used when the CLI is unavailable.
    """
    SENSITIVE_KEY = re.compile(
        r"(token|secret|password|apikey|api_key|private_?key|credential|signing|client_secret|access_key)",
        re.IGNORECASE,
    )

    def redact(obj, key=""):
        if isinstance(obj, dict):
            return {k: redact(v, k) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [redact(i, key) for i in obj]
        elif isinstance(obj, str) and SENSITIVE_KEY.search(key):
            return "[REDACTED]"
        return obj

    with open(config_path) as f:
        return redact(json.load(f))


def main():
    if len(sys.argv) not in (2, 3):
        print(f"Usage: {sys.argv[0]} <output-path> [config-path-fallback]")
        sys.exit(1)

    output_path = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) == 3 else None

    # Try CLI first (authoritative redaction)
    data = export_via_cli()

    if not data:
        # Fallback to raw file
        if config_path and config_path.exists():
            print("  ! openclaw CLI unavailable, falling back to file-based redaction")
            data = export_via_file(config_path)
        else:
            print("  - config (openclaw CLI unavailable and no fallback config path, skipping)")
            sys.exit(0)

    output = scrub(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"  ✓ config-redacted.json")


if __name__ == "__main__":
    main()
