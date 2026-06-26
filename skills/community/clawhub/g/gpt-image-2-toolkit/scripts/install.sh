#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")/../assets/plugin" && pwd)"
DEST_ROOT="${OPENCLAW_CONFIG_DIR:-$HOME/.openclaw}/extensions"
DEST_DIR="$DEST_ROOT/hnbc"

mkdir -p "$DEST_ROOT"
rm -rf "$DEST_DIR"
cp -a "$SRC_DIR" "$DEST_DIR"

printf 'Installed HNBC plugin to: %s\n' "$DEST_DIR"
printf 'Next step: restart the running OpenClaw gateway if it is already running.\n'
