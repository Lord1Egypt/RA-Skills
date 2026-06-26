#!/usr/bin/env bash
# Copy this repo skill + mcp-bridge into ~/.openclaw/skills/offlyn-clipper (refresh after git pull).
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${OPENCLAW_SKILL_DIR:-$HOME/.openclaw/skills/offlyn-clipper}"

echo "== Refresh offlyn-clipper skill =="
echo "From: $SKILL_ROOT"
echo "To:   $DEST"

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SKILL_ROOT" "$DEST"

echo "→ npm install in mcp-bridge…"
(cd "$DEST/mcp-bridge" && npm install --omit=dev)

if command -v openclaw >/dev/null 2>&1; then
  echo ""
  echo "→ Eligible check:"
  openclaw skills info offlyn-clipper 2>/dev/null | head -20 || openclaw skills list --eligible 2>&1 | rg -i offlyn || true
  echo ""
  echo "If OpenClaw was already running: openclaw gateway restart"
  echo "Then start a new chat (/new) and ask: catch me up with my live Clipper meeting"
fi

echo "✓ Done."
