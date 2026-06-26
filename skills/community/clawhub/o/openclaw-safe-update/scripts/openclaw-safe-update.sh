#!/usr/bin/env bash
# openclaw-safe-update: isolated verify-first updater
set -euo pipefail

TARGET_VERSION=""
APPLY=0
VERIFY_ONLY=1
PORT_SPECIFIED=0
SIDECAR_PORT=""
SIDECAR_BASE_PORT="${SIDECAR_BASE_PORT:-18000}"
SIDECAR_MAX_PORT="${SIDECAR_MAX_PORT:-19999}"
SIDECAR_BIND="loopback"
MAX_WAIT="${SIDECAR_MAX_WAIT:-120}"
SIDECAR_PROFILE="${SIDECAR_PROFILE:-sidecar-verify}"
VERSIONS_DIR="${OPENCLAW_VERSIONS_DIR:-$HOME/.openclaw/versions}"
LOG_DIR="${LOG_DIR:-$HOME/.openclaw/logs}"
KEEP_VERSIONS="${KEEP_VERSIONS:-3}"
mkdir -p "$VERSIONS_DIR" "$LOG_DIR"
SIDECAR_LOG="$LOG_DIR/openclaw-sidecar-verify.log"
SIDECAR_PID_FILE="$LOG_DIR/openclaw-sidecar-verify.pid"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; VERIFY_ONLY=0; shift ;;
    --verify-only) VERIFY_ONLY=1; APPLY=0; shift ;;
    --target) TARGET_VERSION="${2:-}"; shift 2 ;;
    --port) SIDECAR_PORT="${2:-}"; PORT_SPECIFIED=1; shift 2 ;;
    --help|-h)
      cat <<'EOF'
Usage:
  openclaw-safe-update.sh                  # default verify-only (auto-select free port >= 18000)
  openclaw-safe-update.sh --apply          # verify then apply global upgrade
  openclaw-safe-update.sh --target <ver>   # pin target version
  openclaw-safe-update.sh --port <port>    # optional manual port override
EOF
      exit 0
      ;;
    *) echo "Unknown argument: $1"; exit 2 ;;
  esac
done

OPENCLAW_BIN="$(command -v openclaw || true)"
NPM_BIN="$(command -v npm || true)"
NODE_BIN="$(command -v node || true)"
[[ -n "$OPENCLAW_BIN" && -n "$NPM_BIN" && -n "$NODE_BIN" ]] || { echo "❌ Missing required binaries: openclaw, npm, node"; exit 1; }

port_in_use() {
  local port="$1"
  (echo > "/dev/tcp/127.0.0.1/${port}") >/dev/null 2>&1
}

select_port() {
  local p
  if [[ "$PORT_SPECIFIED" -eq 1 ]]; then
    if port_in_use "$SIDECAR_PORT"; then
      echo "❌ Requested port ${SIDECAR_PORT} is already in use."
      exit 1
    fi
    return
  fi

  for ((p=SIDECAR_BASE_PORT; p<=SIDECAR_MAX_PORT; p++)); do
    if ! port_in_use "$p"; then
      SIDECAR_PORT="$p"
      return
    fi
  done

  echo "❌ No free sidecar port found in range ${SIDECAR_BASE_PORT}-${SIDECAR_MAX_PORT}."
  exit 1
}

show_log() {
  [[ -f "$SIDECAR_LOG" ]] || return 0
  echo "---- Sidecar log (last 200 lines) ----"
  tail -n 200 "$SIDECAR_LOG" || true
  echo "Log path: $SIDECAR_LOG"
}

cleanup() {
  if [[ -f "$SIDECAR_PID_FILE" ]]; then
    pid=$(cat "$SIDECAR_PID_FILE" || true)
    [[ -n "${pid:-}" ]] && kill "$pid" 2>/dev/null || true
    rm -f "$SIDECAR_PID_FILE"
  fi
}
trap cleanup EXIT

fail() {
  echo "❌ $1"
  show_log
  exit 1
}

prune_old_candidates() {
  local keep="${KEEP_VERSIONS:-3}"
  [[ "$keep" =~ ^[0-9]+$ ]] || keep=3
  if [[ "$keep" -lt 1 ]]; then
    keep=1
  fi

  # Keep newest N version directories, remove older ones.
  local to_delete
  to_delete=$(ls -1dt "$VERSIONS_DIR"/*/ 2>/dev/null | tail -n +$((keep + 1)) || true)
  if [[ -n "$to_delete" ]]; then
    echo "Pruning old candidate versions (keep=$keep)..."
    while IFS= read -r dir; do
      [[ -n "$dir" ]] || continue
      rm -rf "$dir"
    done <<< "$to_delete"
  fi
}

echo "[1/7] Checking versions..."
CURRENT_VERSION="$($OPENCLAW_BIN --version | tr -d '[:space:]')"
if [[ -n "$TARGET_VERSION" ]]; then
  LATEST_VERSION="$TARGET_VERSION"
else
  LATEST_VERSION="$($NPM_BIN view openclaw version | tr -d '[:space:]')"
fi

echo "Current version: $CURRENT_VERSION"
echo "Target version : $LATEST_VERSION"
[[ "$CURRENT_VERSION" == "$LATEST_VERSION" ]] && { echo "Already at target version. Nothing to do."; exit 0; }

echo "[2/7] Selecting sidecar port..."
select_port
echo "Selected port : $SIDECAR_PORT"

echo "[3/7] Installing candidate version into isolated directory..."
CANDIDATE_DIR="$VERSIONS_DIR/$LATEST_VERSION"
$NPM_BIN install --prefix "$CANDIDATE_DIR" "openclaw@$LATEST_VERSION" --no-save --no-audit --no-fund --loglevel=error >/dev/null
CANDIDATE_ENTRY="$CANDIDATE_DIR/node_modules/openclaw/dist/index.js"
[[ -f "$CANDIDATE_ENTRY" ]] || fail "Candidate entry not found: $CANDIDATE_ENTRY"

echo "[4/7] Starting sidecar (profile=$SIDECAR_PROFILE, port=$SIDECAR_PORT)..."
rm -f "$SIDECAR_LOG"
"$NODE_BIN" "$CANDIDATE_ENTRY" --profile "$SIDECAR_PROFILE" gateway --port "$SIDECAR_PORT" --bind "$SIDECAR_BIND" >"$SIDECAR_LOG" 2>&1 &
SIDECAR_PID=$!
echo "$SIDECAR_PID" > "$SIDECAR_PID_FILE"

echo "[5/7] Waiting for sidecar readiness..."
WAIT=0
READY=0
until [[ $WAIT -ge $MAX_WAIT ]]; do
  if curl -sf "http://127.0.0.1:${SIDECAR_PORT}/" >/dev/null 2>&1; then
    READY=1; break
  fi
  if grep -q "canvas host mounted" "$SIDECAR_LOG" 2>/dev/null && kill -0 "$SIDECAR_PID" 2>/dev/null; then
    READY=1; break
  fi
  sleep 1
  WAIT=$((WAIT + 1))
done
[[ "$READY" -eq 1 ]] || fail "Sidecar startup timed out (${MAX_WAIT}s)"
kill -0 "$SIDECAR_PID" 2>/dev/null || fail "Sidecar process exited unexpectedly"

echo "✅ Sidecar verification passed"

echo "[6/7] Stopping sidecar..."
cleanup

if [[ "$APPLY" -ne 1 || "$VERIFY_ONLY" -eq 1 ]]; then
  echo "[7/7] verify-only mode: global install unchanged."
  prune_old_candidates
  echo "Log file: $SIDECAR_LOG"
  exit 0
fi

echo "[7/7] Applying global upgrade + restarting gateway..."
$NPM_BIN install -g "openclaw@$LATEST_VERSION" --no-audit --no-fund --loglevel=error >/dev/null
$OPENCLAW_BIN gateway restart >/dev/null 2>&1 || true
prune_old_candidates

echo "✅ Upgrade completed: $CURRENT_VERSION -> $LATEST_VERSION"
echo "Log file: $SIDECAR_LOG"
