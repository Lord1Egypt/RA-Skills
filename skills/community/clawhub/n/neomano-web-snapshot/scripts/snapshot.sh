#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

URL="${1:-}"
shift || true

if [[ -z "$URL" ]]; then
  echo "Usage: snapshot.sh <url> [--out path] [--full-page] [--wait-ms N] [--timeout-ms N]" >&2
  exit 2
fi

node "$BASE_DIR/scripts/snapshot.mjs" "$URL" "$@"