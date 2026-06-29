#!/usr/bin/env bash
# install-hook.sh — register the logo-guard gateway:startup hook in managed
# hooks dir (~/.openclaw/hooks/) so OpenClaw will load it on next restart.
#
# 1. Sanity-check: the runtime state stamp must exist
#      ${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/applied-state
#    (otherwise the hook has nothing to defend).
# 2. Copy <skill>/hooks/logo-guard → ~/.openclaw/hooks/logo-guard.
#    (We copy, not symlink — OpenClaw's hook discovery does not follow symlinks
#     for managed hooks.)
# 3. Write .skill-dir pointer so the handler can find this skill back.
# 4. Managed hooks default to enabled; no separate enable call needed.
#
# The hook only takes effect AFTER the next gateway restart — this script
# intentionally does NOT restart for you.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOK_SRC="$SKILL_DIR/hooks/logo-guard"
STATE_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo"
STAMP="$STATE_DIR/applied-state"
MANAGED_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}/hooks"
HOOK_DST="$MANAGED_DIR/logo-guard"

if [ ! -d "$HOOK_SRC" ]; then
  echo "ERROR: hook source dir not found: $HOOK_SRC" >&2
  exit 1
fi

if [ ! -f "$STAMP" ]; then
  echo "ERROR: no applied-state stamp at $STAMP" >&2
  echo "  Run 'bash $SKILL_DIR/apply-logo.sh <set>' first so the hook knows what to defend." >&2
  exit 1
fi

mkdir -p "$MANAGED_DIR"

# Remove any prior install (symlink or directory)
if [ -L "$HOOK_DST" ] || [ -e "$HOOK_DST" ]; then
  rm -rf "$HOOK_DST"
fi

# Copy (managed hook discovery does not follow symlinks)
cp -R "$HOOK_SRC" "$HOOK_DST"

# Pointer so handler.js can find this skill back
printf '%s\n' "$SKILL_DIR" > "$HOOK_DST/.skill-dir"

CURRENT_SET="$(grep '^set=' "$STAMP" | cut -d= -f2)"
echo "installed: $HOOK_DST"
echo "  defends: $CURRENT_SET"
echo "  skill:   $SKILL_DIR"
echo "  state:   $STATE_DIR"

# Verify via CLI if available
OC=""
if command -v openclaw >/dev/null 2>&1; then
  OC="openclaw"
else
  for p in "$HOME/.npm-global/bin/openclaw" "/usr/local/bin/openclaw" "/opt/homebrew/bin/openclaw"; do
    [ -x "$p" ] && { OC="$p"; break; }
  done
fi

if [ -n "$OC" ]; then
  echo
  echo "Verifying with: $OC hooks list --json"
  if "$OC" hooks list --json 2>/dev/null | grep -q '"name": "logo-guard"'; then
    echo "OK: openclaw discovered logo-guard (will activate on next gateway restart)"
  else
    echo "WARN: openclaw did not list logo-guard. Try 'openclaw hooks list --verbose' to debug." >&2
  fi
fi

echo
echo "NEXT STEP: restart gateway to activate the hook."
echo "VERIFY:    openclaw hooks list | grep logo-guard"
echo "LOG:       tail -f $STATE_DIR/logo-guard.log"
