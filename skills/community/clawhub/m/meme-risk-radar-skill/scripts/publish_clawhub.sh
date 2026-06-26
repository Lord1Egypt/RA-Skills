#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found. Install with: npm i -g clawhub"
  exit 1
fi

echo "Publishing skill from: ${SKILL_DIR}"
clawhub publish "${SKILL_DIR}"
