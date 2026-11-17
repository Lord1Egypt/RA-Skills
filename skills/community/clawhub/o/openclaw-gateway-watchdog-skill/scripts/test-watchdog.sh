#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(mktemp -d)"
SENTINEL="$TEST_DIR/config-was-executed"

cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

printf '%s\n' \
  "DISCORD_WEBHOOK_URL=\$(touch $SENTINEL)" \
  "GW_WATCHDOG_FAIL_THRESHOLD=99" \
  > "$TEST_DIR/config.env"

OPENCLAW_BIN=/usr/bin/true \
GW_WATCHDOG_BASE_DIR="$TEST_DIR" \
SPARK_API_URL=http://127.0.0.1:1 \
LOCAL_API_URL=http://127.0.0.1:1 \
DASHBOARD_PORT=1 \
bash "$SCRIPT_DIR/gateway-watchdog.sh"

if [[ -e "$SENTINEL" ]]; then
  echo "config.env was executed" >&2
  exit 1
fi

for state_file in state.json spark_state.json api_hub_state.json dashboard_state.json; do
  [[ -f "$TEST_DIR/$state_file" ]] || {
    echo "missing state file: $state_file" >&2
    exit 1
  }
done

echo "Gateway watchdog checks passed."
