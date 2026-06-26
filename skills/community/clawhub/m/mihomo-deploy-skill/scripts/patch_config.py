#!/usr/bin/env python3
"""
patch_config.py — Safely patch a mihomo/Clash config.yaml with deployment settings.

Usage:
  python3 patch_config.py \
    --config ~/.config/mihomo/config.yaml \
    --mixed-port 7890 \
    --controller-addr 127.0.0.1 \
    --controller-port 9090 \
    [--secret "your-secret"]

Modifies in-place:
  - mixed-port
  - external-controller
  - external-ui (sets to "ui")
  - secret (omit --secret to remove the field)
"""

import argparse
import re
import sys
from pathlib import Path


def set_or_replace(lines: list[str], key: str, value: str) -> list[str]:
    """Replace an existing top-level key's value, or append it if not found."""
    pattern = re.compile(r'^' + re.escape(key) + r'\s*:.*$')
    new_line = f"{key}: {value}"
    replaced = False
    result = []
    for line in lines:
        if pattern.match(line):
            result.append(new_line)
            replaced = True
        else:
            result.append(line)
    if not replaced:
        result.append(new_line)
    return result


def remove_key(lines: list[str], key: str) -> list[str]:
    """Remove a top-level key if present."""
    pattern = re.compile(r'^' + re.escape(key) + r'\s*:.*$')
    return [line for line in lines if not pattern.match(line)]


def main():
    parser = argparse.ArgumentParser(description="Patch mihomo config.yaml")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--mixed-port", type=int, default=7890)
    parser.add_argument("--controller-addr", default="127.0.0.1",
                        help="Bind address for external-controller (127.0.0.1 or 0.0.0.0)")
    parser.add_argument("--controller-port", type=int, default=9090)
    parser.add_argument("--secret", default=None,
                        help="Web UI password. Omit to remove the secret field.")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    if not config_path.exists():
        print(f"Error: config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    lines = config_path.read_text(encoding="utf-8").splitlines()

    # Apply patches
    lines = set_or_replace(lines, "mixed-port", str(args.mixed_port))
    controller_value = f"'{args.controller_addr}:{args.controller_port}'"
    lines = set_or_replace(lines, "external-controller", controller_value)
    lines = set_or_replace(lines, "external-ui", "ui")

    if args.secret:
        lines = set_or_replace(lines, "secret", f"'{args.secret}'")
    else:
        lines = remove_key(lines, "secret")

    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Patched: {config_path}")
    print(f"  mixed-port: {args.mixed_port}")
    print(f"  external-controller: {args.controller_addr}:{args.controller_port}")
    print(f"  external-ui: ui")
    if args.secret:
        print(f"  secret: (set)")
    else:
        print(f"  secret: (removed)")


if __name__ == "__main__":
    main()
