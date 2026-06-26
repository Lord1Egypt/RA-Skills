#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

status=0

if command -v bash >/dev/null 2>&1; then
  echo "[ok] bash: $(command -v bash)"
else
  echo "[missing] bash" >&2
  status=1
fi

if command -v curl >/dev/null 2>&1; then
  echo "[ok] curl: $(command -v curl)"
elif command -v wget >/dev/null 2>&1; then
  echo "[ok] wget: $(command -v wget)"
else
  echo "[missing] curl or wget" >&2
  status=1
fi

echo "[info] cache_dir: $OPENCLAW_DOCS_CACHE_DIR"
echo "[info] ttl: $OPENCLAW_DOCS_TTL"
echo "[info] base_url: $OPENCLAW_DOCS_BASE_URL"

if [[ $status -ne 0 ]]; then
  echo "Environment check failed." >&2
  exit 1
fi

echo "Environment check complete."
