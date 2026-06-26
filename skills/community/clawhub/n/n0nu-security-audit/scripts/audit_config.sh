#!/usr/bin/env bash
# audit_config.sh — Delegate config audit to `openclaw security audit`
#
# Usage:
#   ./audit_config.sh [--deep] [--fix]
#
# Options:
#   --deep   Attempt live Gateway probe (best-effort)
#   --fix    Apply safe fixes (tighten defaults + chmod state/config)
#
# Output: Markdown-formatted security findings from openclaw security audit

set -euo pipefail

DEEP=""
FIX=""

for arg in "$@"; do
  case "$arg" in
    --deep) DEEP="--deep" ;;
    --fix)  FIX="--fix"   ;;
  esac
done

if ! command -v openclaw &>/dev/null; then
  echo "## OpenClaw Config Security Audit"
  echo "**Error**: \`openclaw\` CLI not found in PATH. Cannot run audit."
  exit 1
fi

echo "## OpenClaw Config Security Audit"
echo ""
echo "_Powered by \`openclaw security audit\`_"
echo ""

# Run the native audit; capture output
OUTPUT=$(openclaw security audit $DEEP $FIX 2>&1)
echo "$OUTPUT"
