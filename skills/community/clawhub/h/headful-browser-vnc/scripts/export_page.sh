#!/usr/bin/env bash
set -euo pipefail
# load env if present
source "$(dirname "$0")/_env_loader.sh"

SESSION=${1:-debug}
URL=${2:-}
if [ -z "$URL" ]; then echo "Usage: $0 <session> <url> [devtools-port]"; exit 2; fi
OUTDIR=${OUT_DIR:-out}
mkdir -p "$OUTDIR"
WS_PORT=${3:-${REMOTE_DEBUG_PORT:-9222}}

# Use playwright via node if available else use wget as fallback
if command -v node >/dev/null 2>&1; then
  SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
  # Call the safer external JS exporter with positional args to avoid shell injection
  if [ -f "$SKILL_DIR/tools/playwright_export.js" ]; then
    node "$SKILL_DIR/tools/playwright_export.js" "$WS_PORT" "$URL" "$OUTDIR" || true
  else
    # fallback to system-installed playwright if available
    node -e "console.error('playwright exporter not found'); process.exit(1)" || true
  fi
else
  echo "Playwright not available; saving via wget as fallback"
  wget -q -O "$OUTDIR/backup.html" --proxy=on --execute="http_proxy=${PROXY_URL:-http://127.0.0.1:3128}" "$URL" || true
fi
