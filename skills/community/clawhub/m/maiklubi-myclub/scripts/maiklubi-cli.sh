#!/usr/bin/env bash
set -euo pipefail

# Wrapper for the maiklubi CLI (non-interactive use).
# Usage: maiklubi-cli.sh <args>

# Prefer the globally-installed binary (npm install -g maiklubi).
if command -v maiklubi >/dev/null 2>&1; then
  exec maiklubi "$@"
fi

# Dev fallback: a local build relative to THIS script (not the caller's $PWD).
# Covers both the dev repo (skills/maiklubi/scripts/ -> repo root) and a
# packaged skill that bundles dist alongside it.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
for candidate in \
  "$SCRIPT_DIR/../../../dist/index.js" \
  "$SCRIPT_DIR/../dist/index.js"; do
  if [ -f "$candidate" ]; then
    exec node "$candidate" "$@"
  fi
done

echo "maiklubi is not installed. Install it with: npm install -g maiklubi" >&2
exit 127
