#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="${WORKSPACE:-${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
printf 'Handover Hangover status\n'
printf '  skill dir: %s\n' "$SKILL_DIR"
printf '  workspace: %s\n' "$WORKSPACE"
printf '  watchdog: '
[ -x "$SKILL_DIR/scripts/handoff.sh" ] && echo 'ok' || echo 'missing/not executable'
printf '  managed hook: '
[ -f "${OPENCLAW_HOME:-$HOME/.openclaw}/hooks/handover-hangover/HOOK.md" ] && echo 'installed' || echo 'not installed'
printf '  OpenClaw hook entry: '
if command -v openclaw >/dev/null 2>&1; then
  openclaw config get hooks.internal.entries.handover-hangover 2>/dev/null || echo 'not enabled'
else
  echo 'openclaw cli unavailable'
fi
printf '  memory files:\n'
ls -la "$WORKSPACE/memory" 2>/dev/null | grep -E 'handoff|current-task' || true
