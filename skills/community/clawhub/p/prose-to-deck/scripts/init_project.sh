#!/usr/bin/env bash
# Legacy compatibility wrapper for environments that still call the old shell entrypoint.
# Prefer scripts/init_project.py as the primary implementation.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python >/dev/null 2>&1; then
  exec python "${SCRIPT_DIR}/init_project.py" "$@"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 "${SCRIPT_DIR}/init_project.py" "$@"
else
  echo "Error: python or python3 is required to run init_project.py" >&2
  exit 1
fi
