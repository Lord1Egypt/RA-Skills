#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────
# publish.sh — Publish molql skill to ClawHub
# ──────────────────────────────────────────────
# Prerequisites:
#   1. Install ClawHub CLI: npm install -g @openclaw/clawhub
#   2. Sign in:            clawhub login
#
# Usage:
#   ./scripts/publish.sh                  # publish as authed user
#   ./scripts/publish.sh --owner openclaw # publish to org
#   ./scripts/publish.sh --dry-run        # preview only
# ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

OWNER=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --owner)   OWNER="$2";   shift 2 ;;
    --dry-run) DRY_RUN=true; shift   ;;
    --help)
      echo "Usage: $0 [--owner <handle>] [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--owner <handle>] [--dry-run]"
      exit 1
      ;;
  esac
done

ARGS=(
  --slug molql
  --name "MolQL"
)

if [[ -n "$OWNER" ]]; then
  ARGS+=(--owner "$OWNER")
fi

if [[ "$DRY_RUN" == true ]]; then
  ARGS+=(--dry-run)
  echo "=== DRY RUN ==="
fi

echo "Publishing molql from: $SKILL_DIR"
clawhub skill publish "$SKILL_DIR" "${ARGS[@]}"
