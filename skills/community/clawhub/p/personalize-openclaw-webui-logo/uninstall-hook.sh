#!/usr/bin/env bash
# uninstall-hook.sh — remove the logo-guard managed hook.
# Leaves logo files in dist alone.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
MANAGED_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}/hooks"
HOOK_DST="$MANAGED_DIR/logo-guard"

if [ -e "$HOOK_DST" ] || [ -L "$HOOK_DST" ]; then
  rm -rf "$HOOK_DST"
  echo "removed: $HOOK_DST"
else
  echo "nothing to remove at $HOOK_DST"
fi

echo "uninstall complete. The current dist favicon is unchanged."
echo "Restart gateway for the change to take effect."
echo "To re-enable later, run: bash $SKILL_DIR/install-hook.sh"
