#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v npm >/dev/null 2>&1; then
  if [[ -f "${SCRIPT_DIR}/package-lock.json" ]]; then
    npm --prefix "${SCRIPT_DIR}" ci
  else
    npm --prefix "${SCRIPT_DIR}" install
  fi
else
  echo "npm is required but not found."
  exit 1
fi

npx --prefix "${SCRIPT_DIR}" playwright install chromium
