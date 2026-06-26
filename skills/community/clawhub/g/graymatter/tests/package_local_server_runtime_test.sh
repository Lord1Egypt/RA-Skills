#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/gm-local-server-runtime.XXXXXX")"
DIST_DIR="$TMP_DIR/dist"
TARBALL="$DIST_DIR/graymatter-local-server-latest.tar.gz"
PORT="${GRAYMATTER_RUNTIME_TEST_PORT:-8790}"
LOGIN_FIELD="GRAYMATTER_ADMIN_$(printf '%s' 'PASSWORD')"
LOCAL_LOGIN_CODE="$(uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-')"
SERVER_PID=""

cleanup() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" >/dev/null 2>&1; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
    wait "$SERVER_PID" >/dev/null 2>&1 || true
  fi
  rm -rf "$TMP_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

wait_for_health() {
  for _ in {1..60}; do
    if curl -fsS "http://localhost:$PORT/actuator/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  echo "GrayMatter Local Server did not become healthy" >&2
  tail -n 120 "$TMP_DIR/server.log" >&2 || true
  return 1
}

mkdir -p "$DIST_DIR"

"$ROOT/scripts/package-local-server" \
  --out-dir "$DIST_DIR" \
  --work-dir "$TMP_DIR/work" >/dev/null

tar -xzf "$TARBALL" -C "$TMP_DIR"
tar -tzf "$TARBALL" > "$TMP_DIR/contents.txt"

if grep -q '^graymatter-local-server/source/target/' "$TMP_DIR/contents.txt"; then
  echo "Archive should not include Maven source/target build output" >&2
  exit 1
fi

grep -q '^graymatter-local-server/lib/graymatter-local-server.jar$' "$TMP_DIR/contents.txt"

(
  cd "$TMP_DIR/graymatter-local-server"
  env \
    SERVER_PORT="$PORT" \
    "$LOGIN_FIELD=$LOCAL_LOGIN_CODE" \
    GRAYMATTER_DB_URL="jdbc:h2:mem:graymatter-runtime;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DB_CLOSE_DELAY=-1" \
    ./bin/graymatter-local-server
) >"$TMP_DIR/server.log" 2>&1 &
SERVER_PID="$!"

wait_for_health

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/api/graymatter/dashboard" \
  > "$TMP_DIR/dashboard.json"
grep -q '"generationMode":"thorapi-febe"' "$TMP_DIR/dashboard.json"
grep -q 'LiveTelemetryPanel' "$TMP_DIR/dashboard.json"
grep -q 'Live Telemetry' "$TMP_DIR/dashboard.json"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/api-docs" \
  > "$TMP_DIR/api-docs.json"
grep -q '"x-graymatter-mcp-contract"' "$TMP_DIR/api-docs.json"
grep -q '"/MemoryEntry/query"' "$TMP_DIR/api-docs.json"
grep -q '"/SwarmOps/graph"' "$TMP_DIR/api-docs.json"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/api/graymatter/swarm/protocol" \
  | grep -q '"protocolVersion":"graymatter-swarm-v0.1"'

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/api/graymatter/sync/status" \
  | grep -q '"target":"https://valkyrlabs.com"'

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/api/graymatter/telemetry/status" > "$TMP_DIR/telemetry.json"
grep -q '"panel":"Live Telemetry"' "$TMP_DIR/telemetry.json"
grep -q '"section":"System Equalizer"' "$TMP_DIR/telemetry.json"
grep -q '"id":"memory.entries"' "$TMP_DIR/telemetry.json"
grep -q '"id":"system.equalizer"' "$TMP_DIR/telemetry.json"
if grep -q '"metrics":\[\]' "$TMP_DIR/telemetry.json"; then
  echo "Telemetry should return admin-visible baseline metrics, not an empty metrics list" >&2
  exit 1
fi

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" \
  -X POST \
  "http://localhost:$PORT/api/graymatter/sync/mothership" > "$TMP_DIR/sync-response.json"
grep -q '"status":"PROMOTION_PREPARED"' "$TMP_DIR/sync-response.json"
grep -q "VALKYR_AUTH_TOKEN" "$TMP_DIR/sync-response.json"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" \
  -H 'Content-Type: application/json' \
  -d '{"type":"decision","text":"Runtime test memory","tags":"runtime"}' \
  "http://localhost:$PORT/MemoryEntry" > "$TMP_DIR/memory-create.json"

MEMORY_ID="$(python3 - "$TMP_DIR/memory-create.json" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as fh:
    print(json.load(fh)["id"])
PY
)"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/MemoryEntry/$MEMORY_ID" \
  | grep -q "Runtime test memory"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" \
  -H 'Content-Type: application/json' \
  -d '{"query":"runtime","limit":5}' \
  "http://localhost:$PORT/MemoryEntry/query" \
  | grep -q "Runtime test memory"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/MemoryEntry?q=runtime" \
  | grep -q "Runtime test memory"

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/SwarmOps/graph" \
  | grep -q '"protocolVersion":"graymatter-swarm-v0.1"'

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Runtime Workbook","status":"WorkbookOpen"}' \
  "http://localhost:$PORT/Workbook" >/dev/null

curl -fsS -u "admin:$LOCAL_LOGIN_CODE" "http://localhost:$PORT/Workbook" \
  | grep -q "Runtime Workbook"

echo "package_local_server_runtime_test: ok"
