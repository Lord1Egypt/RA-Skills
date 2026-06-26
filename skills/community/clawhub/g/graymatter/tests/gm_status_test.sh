#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT_DIR/scripts/gm-status"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/memory" "$TMP_DIR/tmp"
cat > "$TMP_DIR/memory/graymatter-fallback.json" <<'JSON'
[]
JSON
cat > "$TMP_DIR/tmp/openapi.json" <<'JSON'
{
  "paths": {
    "/SwarmOps/graph": {},
    "/StrategicRecord": {},
    "/KPIRecord": {}
  }
}
JSON

cp "$SCRIPT" "$TMP_DIR/gm-status"
chmod +x "$TMP_DIR/gm-status"
out="$(ROOT_DIR="$TMP_DIR" VALKYR_API_BASE="http://127.0.0.1:9/v1" VALKYR_AUTH_TOKEN=test "$TMP_DIR/gm-status")"

echo "$out" | grep -q '^graymatter_auth=env$'
echo "$out" | grep -q '^memory_layer=degraded$'
echo "$out" | grep -q '^graph_layer=ready$'
echo "$out" | grep -q '^strategic_layer=ready$'
echo "$out" | grep -q '^kpi_layer=ready$'

readonly_jwt='eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXX0.'
out_readonly="$(ROOT_DIR="$TMP_DIR" VALKYR_API_BASE="http://127.0.0.1:9/v1" VALKYR_AUTH_TOKEN="$readonly_jwt" "$TMP_DIR/gm-status")"
echo "$out_readonly" | grep -q '^graymatter_auth=env:read_only$'
echo "$out_readonly" | grep -q '^memory_layer=degraded$'

echo "gm_status_test: ok"
