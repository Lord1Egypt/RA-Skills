#!/usr/bin/env bash
# ProxyGate update checker — runs on Claude Code SessionStart.
# Writes result to ~/.claude/cache/proxygate-update-check.json.
# Exits quickly; never blocks session startup.

set -euo pipefail

CACHE_DIR="$HOME/.claude/cache"
CACHE_FILE="$CACHE_DIR/proxygate-update-check.json"

mkdir -p "$CACHE_DIR"

# Skip if checked within last hour
if [ -f "$CACHE_FILE" ]; then
  if [ "$(uname)" = "Darwin" ]; then
    age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
  else
    age=$(( $(date +%s) - $(stat -c %Y "$CACHE_FILE") ))
  fi
  if [ "$age" -lt 3600 ]; then
    exit 0
  fi
fi

current=$(proxygate --version 2>/dev/null || echo "0.0.0")
latest=$(npm view @proxygate/cli version 2>/dev/null || echo "0.0.0")

if [ "$current" = "$latest" ] || [ "$latest" = "0.0.0" ]; then
  cat > "$CACHE_FILE" <<JSON
{"update_available":false,"current":"$current","latest":"$latest","checked_at":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
JSON
else
  cat > "$CACHE_FILE" <<JSON
{"update_available":true,"current":"$current","latest":"$latest","checked_at":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
JSON
  echo "ProxyGate update available: $current → $latest. Run /pg-update to upgrade."
fi
