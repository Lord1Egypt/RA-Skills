#!/usr/bin/env bash
# Install Handover Hangover lifecycle integration for OpenClaw.
# Safe/idempotent: copies a managed hook pack and enables it when the hooks CLI exists.
set -euo pipefail

log() { printf '[handover-hangover install] %s\n' "$*"; }
warn() { printf '[handover-hangover install] WARNING: %s\n' "$*" >&2; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOK_SRC="$SKILL_DIR/hooks/handover-hangover"
HOOK_DST="${OPENCLAW_HOME:-$HOME/.openclaw}/hooks/handover-hangover"
WORKSPACE="${WORKSPACE:-${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}}"

if [ ! -f "$SCRIPT_DIR/handoff.sh" ]; then
  warn "missing $SCRIPT_DIR/handoff.sh"
  exit 1
fi
chmod +x "$SCRIPT_DIR/handoff.sh" || true

if [ ! -f "$HOOK_SRC/HOOK.md" ] || [ ! -f "$HOOK_SRC/handler.js" ]; then
  warn "missing hook pack files in $HOOK_SRC"
  exit 1
fi

mkdir -p "$HOOK_DST"
cp "$HOOK_SRC/HOOK.md" "$HOOK_DST/HOOK.md"
cp "$HOOK_SRC/handler.js" "$HOOK_DST/handler.js"
cp "$SCRIPT_DIR/handoff.sh" "$HOOK_DST/handoff.sh"
chmod +x "$HOOK_DST/handoff.sh" || true

log "installed managed hook pack at $HOOK_DST"

if command -v openclaw >/dev/null 2>&1 && openclaw hooks --help >/dev/null 2>&1; then
  if openclaw hooks enable handover-hangover >/dev/null 2>&1; then
    log "enabled OpenClaw hook: handover-hangover"
    log "restart the Gateway for hook loading if it is already running"
  else
    warn "OpenClaw hooks CLI exists, but enabling failed. Run: openclaw hooks list --verbose"
  fi
else
  warn "OpenClaw hooks CLI not available; use fallback snippets below"
fi

cat <<EOF

Fallback integration for older OpenClaw versions:

Add this line to AGENTS.md boot and/or HEARTBEAT.md if hook discovery is unavailable:

  WORKSPACE="$WORKSPACE" bash "$SCRIPT_DIR/handoff.sh"

The watchdog is idempotent. Running it at startup, heartbeat, or before turns is safe.
EOF
