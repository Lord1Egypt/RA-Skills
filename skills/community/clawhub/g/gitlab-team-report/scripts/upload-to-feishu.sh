#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -f "$SCRIPT_DIR/../config/config.json" ]]; then
  export FEISHU_APP_ID="${FEISHU_APP_ID:-$(jq -r '.feishu.app_id // empty' "$SCRIPT_DIR/../config/config.json")}"
  export FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-$(jq -r '.feishu.app_secret // empty' "$SCRIPT_DIR/../config/config.json")}"
fi

exec node "$SCRIPT_DIR/upload-to-feishu.js" "$@"
