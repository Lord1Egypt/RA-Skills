#!/bin/bash
# update.sh — Pull latest Look from GitHub source
# Usage: bash update.sh
# Options:
#   --help    Show this help message
#   --check   Check if a newer version exists (exit 0=yes, exit 1=no)

set -euo pipefail

case "${1:-}" in
  --help)
    echo "update.sh — Pull latest Look from GitHub"
    echo "Usage: bash update.sh [--check] [--help]"
    echo ""
    echo "  --check   Only check for updates (do not apply)"
    echo "  --help    Show this message"
    exit 0
    ;;
esac

cd "$(dirname "$0")/.."

if ! command -v git & then
  echo "ERROR: git is not installed" >&2
  exit 1
fi

if [ ! -d .git ]; then
  echo "ERROR: Not a git repository. Look must be installed from a git repo." >&2
  exit 1
fi

# Fetch remote without applying
git fetch origin main 2>/dev/null

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "Look is already up to date (${LOCAL:0:8})"
  exit 0
fi

if [ "${1:-}" = "--check" ]; then
  echo "Update available: ${LOCAL:0:8} → ${REMOTE:0:8}"
  exit 0
fi

# Apply update
git reset --hard origin/main 2>/dev/null || { echo "ERROR: Failed to reset to remote" >&2; exit 1; }

echo "Updated Look from ${LOCAL:0:8} to ${REMOTE:0:8}"
