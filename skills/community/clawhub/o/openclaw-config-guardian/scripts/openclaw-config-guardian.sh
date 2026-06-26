#!/bin/bash
# OpenClaw Config Guardian v3.2
# Protects: /root/.openclaw/openclaw.json
# Triggers on: close_write + moved_to in /root/.openclaw/
# Behavior: snapshot -> validate -> update baseline or rollback
# Features: state-machine lock mode (disk-persistent), SIGUSR1 reload,
#           7-version baseline history, baseline SHA256, audit log,
#           self-integrity (fail-closed), unlock subcommand
# Changelog:
#   v3.0 2026-03-19 - lock-mode fuse, multi-baseline, SIGUSR1, sha256, audit, self-check
#   v3.1 2026-03-19 - fail-closed self-check, remove create event, locked-revert SIGUSR1
#   v3.2 2026-03-19 - true state-machine lock (disk-read every cycle, remove _REVERTING),
#                     unlock subcommand, locked path bypasses validate entirely

set -euo pipefail

SCRIPT_PATH="$(readlink -f "$0")"
CONFIG_DIR="/root/.openclaw"
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
BACKUP_DIR="$CONFIG_DIR/backups/config"
BASELINE="$BACKUP_DIR/baseline.bak"
BASELINE_SHA="$BACKUP_DIR/baseline.bak.sha256"
BASELINE_HISTORY_DIR="$BACKUP_DIR/baseline_history"
ATTEMPTS_DIR="$BACKUP_DIR/attempts"
STATE_FILE="$BACKUP_DIR/.guardian_state.json"
AUDIT_LOG="$BACKUP_DIR/guardian_audit.log"
SELF_CHECKSUM="$BACKUP_DIR/.guardian_checksum"
MAX_RETRIES=3
BASELINE_KEEP=7
SNAPSHOT_KEEP=20
GATEWAY_PID_PATTERN='openclaw-gateway'

# ── Self-integrity check (fail-closed) ───────────────────────────────────────
self_check() {
  if [[ ! -f "$SELF_CHECKSUM" ]]; then
    echo "[GUARDIAN] ⛔ SELF-INTEGRITY FAIL: checksum file missing ($SELF_CHECKSUM), refusing to start" | logger -t openclaw-guardian
    send_alert "⛔ [大黑 #F_SEC] guardian checksum 文件不存在，已拒绝启动。请运行：sha256sum $SCRIPT_PATH > $SELF_CHECKSUM"
    exit 1
  fi
  if ! sha256sum -c "$SELF_CHECKSUM" --quiet 2>/dev/null; then
    echo "[GUARDIAN] ⛔ SELF-INTEGRITY FAIL: script tampered, refusing to start" | logger -t openclaw-guardian
    send_alert "⛔ [大黑 #F_SEC] guardian 自身完整性校验失败！脚本疑似被篡改，已拒绝启动。请立即检查 $SCRIPT_PATH"
    exit 1
  fi
}

# ── Logging ───────────────────────────────────────────────────────────────────
log() {
  echo "[GUARDIAN] $*"
  logger -t openclaw-guardian "$*" || true
}

audit() {
  local action="$1" detail="${2:-}"
  local ts writer_pid writer_cmd
  ts=$(date -Iseconds)
  writer_pid=$(fuser "$CONFIG_FILE" 2>/dev/null | tr -s ' ' | cut -d' ' -f1 || echo "unknown")
  writer_cmd=$(ps -p "${writer_pid:-0}" -o comm= 2>/dev/null || echo "unknown")
  echo "$ts | GUARDIAN_PID=$$ | ACTION=$action | writer=${writer_cmd}(pid=${writer_pid}) | $detail" >> "$AUDIT_LOG"
}

# ── Alert ─────────────────────────────────────────────────────────────────────
send_alert() {
  local msg="$1"
  openclaw message send --channel discord --channel-id 1483995509910667455 "$msg" 2>/dev/null || true
  openclaw message send --channel telegram --target telegram:5189839048 "$msg" 2>/dev/null || true
}

# ── State helpers ─────────────────────────────────────────────────────────────
init_state() {
  mkdir -p "$BACKUP_DIR" "$ATTEMPTS_DIR" "$BASELINE_HISTORY_DIR"
  if [[ ! -f "$STATE_FILE" ]]; then
    cat > "$STATE_FILE" <<JSON
{
  "attempts": 0,
  "last_error": null,
  "last_backup": null,
  "locked": false,
  "failed_at": null
}
JSON
  fi
  touch "$AUDIT_LOG"
  # Rotate audit log if too large (keep last 30000 lines)
  local lines
  lines=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo 0)
  if (( lines > 50000 )); then
    tail -n 30000 "$AUDIT_LOG" > "${AUDIT_LOG}.tmp" && mv "${AUDIT_LOG}.tmp" "$AUDIT_LOG"
    log "📋 audit log rotated"
  fi
}

read_state() { cat "$STATE_FILE"; }

# Read locked field directly from disk — single source of truth
is_locked() {
  local locked
  locked=$(jq -r '.locked' "$STATE_FILE" 2>/dev/null || echo "false")
  [[ "$locked" == "true" ]]
}

write_state() {
  local attempts="$1" last_error="$2" last_backup="$3" locked="$4" failed_at="$5"
  if command -v jq >/dev/null 2>&1; then
    jq -n \
      --argjson attempts "$attempts" \
      --arg last_error "$last_error" \
      --arg last_backup "$last_backup" \
      --argjson locked "$locked" \
      --arg failed_at "$failed_at" \
      '{attempts:$attempts,last_error:$last_error,last_backup:$last_backup,locked:$locked,failed_at:$failed_at}' \
      > "$STATE_FILE"
  else
    cat > "$STATE_FILE" <<JSON
{
  "attempts": $attempts,
  "last_error": "${last_error}",
  "last_backup": "${last_backup}",
  "locked": $locked,
  "failed_at": "${failed_at}"
}
JSON
  fi
}

# ── Baseline helpers ──────────────────────────────────────────────────────────
ensure_baseline() {
  if [[ ! -f "$CONFIG_FILE" ]]; then
    log "❌ config file missing: $CONFIG_FILE"
    exit 1
  fi
  if [[ ! -f "$BASELINE" ]]; then
    cp "$CONFIG_FILE" "$BASELINE"
    sha256sum "$BASELINE" > "$BASELINE_SHA"
    log "✅ baseline created: $BASELINE"
    audit "BASELINE_INIT" "first baseline created"
  fi
}

verify_baseline_integrity() {
  if [[ -f "$BASELINE_SHA" ]]; then
    if ! sha256sum -c "$BASELINE_SHA" --quiet 2>/dev/null; then
      log "⚠️ baseline.bak checksum mismatch — attempting restore from history"
      audit "BASELINE_CORRUPT" "sha256 mismatch, trying history"
      restore_baseline_from_history || {
        log "❌ all history baselines unavailable — MANUAL INTERVENTION REQUIRED"
        send_alert "【大黑 #F_SEC】⚠️ CRITICAL: baseline.bak 校验失败且历史版本均不可用，需要人工干预！"
        return 1
      }
    fi
  fi
  return 0
}

update_baseline() {
  if [[ -f "$BASELINE" ]]; then
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    cp "$BASELINE" "$BASELINE_HISTORY_DIR/baseline_${ts}.bak"
    ( cd "$BASELINE_HISTORY_DIR" && ls -t baseline_*.bak 2>/dev/null | tail -n +$((BASELINE_KEEP + 1)) | xargs -r rm -f ) || true
    log "📦 baseline archived (history kept: $BASELINE_KEEP versions)"
  fi
  cp "$CONFIG_FILE" "$BASELINE"
  sha256sum "$BASELINE" > "$BASELINE_SHA"
}

restore_baseline_from_history() {
  local hist
  hist=$(ls -t "$BASELINE_HISTORY_DIR"/baseline_*.bak 2>/dev/null | head -1)
  if [[ -z "$hist" ]]; then
    return 1
  fi
  cp "$hist" "$BASELINE"
  sha256sum "$BASELINE" > "$BASELINE_SHA"
  log "♻️ baseline restored from history: $hist"
  audit "BASELINE_RESTORED" "from $hist"
  return 0
}

# ── Snapshot helpers ──────────────────────────────────────────────────────────
snapshot() {
  local ts
  ts=$(date +%F-%H%M%S)
  local snap="$ATTEMPTS_DIR/openclaw.json.${ts}.bak"
  cp "$CONFIG_FILE" "$snap"
  echo "$snap"
}

rotate_snapshots() {
  ( cd "$ATTEMPTS_DIR" 2>/dev/null && ls -t *.bak 2>/dev/null | tail -n +$((SNAPSHOT_KEEP + 1)) | xargs -r rm -f ) || true
}

# ── Validate ──────────────────────────────────────────────────────────────────
validate_config() {
  local out
  out=$(openclaw config validate 2>&1) || true
  if echo "$out" | grep -q "Config valid"; then
    return 0
  fi
  log "❌ validate failed: $out"
  return 1
}

# ── Gateway SIGUSR1 reload ────────────────────────────────────────────────────
reload_gateway() {
  local gw_pid
  gw_pid=$(pgrep -f "$GATEWAY_PID_PATTERN" 2>/dev/null | head -1 || true)
  if [[ -n "$gw_pid" ]]; then
    kill -SIGUSR1 "$gw_pid" 2>/dev/null \
      && log "📡 SIGUSR1 sent to gateway (pid=$gw_pid)" \
      || log "⚠️ failed to send SIGUSR1 to gateway (pid=$gw_pid)"
    audit "GATEWAY_RELOAD" "SIGUSR1 -> pid=$gw_pid"
  else
    log "⚠️ gateway process not found, skipping reload signal"
    audit "GATEWAY_RELOAD" "skipped: no gateway process"
  fi
}

# ── Revert to baseline (shared by locked-path and failure-path) ───────────────
do_revert() {
  local reason="$1"
  if verify_baseline_integrity && [[ -f "$BASELINE" ]]; then
    cp "$BASELINE" "$CONFIG_FILE"
    reload_gateway
    log "🔄 reverted to baseline ($reason)"
    audit "REVERT" "reason=$reason"
    return 0
  else
    log "❌ baseline missing or corrupt; cannot revert ($reason)"
    audit "REVERT_FAIL" "reason=$reason; no valid baseline"
    return 1
  fi
}

# ── Success handler ───────────────────────────────────────────────────────────
after_success() {
  local snap="$1"
  update_baseline
  write_state 0 "" "$snap" false ""
  log "✅ config ok; baseline updated"
  audit "VALIDATE_OK" "baseline updated; snap=$snap"
  reload_gateway
}

# ── Failure handler ───────────────────────────────────────────────────────────
after_failure() {
  local snap="$1" err="$2"
  local state attempts
  state=$(read_state)
  attempts=$(echo "$state" | jq -r '.attempts' 2>/dev/null || echo 0)

  attempts=$((attempts + 1))
  do_revert "validate_fail attempt=$attempts/$MAX_RETRIES"
  audit "VALIDATE_FAIL" "attempt=$attempts/$MAX_RETRIES; snap=$snap; err=$err"

  if (( attempts >= MAX_RETRIES )); then
    local failed_at
    failed_at=$(date -Iseconds)
    write_state "$attempts" "$err" "$snap" true "$failed_at"
    log "⛔ reached max failures ($MAX_RETRIES); entering LOCK MODE (monitoring continues)"
    audit "CIRCUIT_BREAK" "locked at $failed_at; err=$err"
    send_alert "【大黑 #F_SEC】⛔ Config Guardian 熔断！\n\n连续 $MAX_RETRIES 次验证失败，已进入锁定模式。\n所有后续写入将自动回滚，监控继续运行。\n\n错误：$err\n时间：$failed_at\n快照：$snap\n\n解锁方式：openclaw-config-guardian unlock"
  else
    write_state "$attempts" "$err" "$snap" false ""
  fi

  return 0
}

# ── Main change handler (true state-machine: read lock from disk every cycle) ──
handle_change() {
  init_state
  ensure_baseline

  # ── LOCKED PATH: read from disk, bypass validate entirely ──
  if is_locked; then
    log "⛔ [LOCKED] write detected; reverting without validate"
    do_revert "locked_mode"
    audit "LOCKED_REVERT" "reverted in lock mode; no validate"
    return 0
  fi

  # ── NORMAL PATH ──
  local snap
  snap=$(snapshot)
  rotate_snapshots

  if validate_config; then
    after_success "$snap"
  else
    after_failure "$snap" "validate_failed"
  fi
}

# ── Unlock subcommand ─────────────────────────────────────────────────────────
cmd_unlock() {
  echo "[GUARDIAN] unlock: validating current config before unlocking..."
  if ! validate_config; then
    echo "[GUARDIAN] ❌ unlock REFUSED: config is still invalid. Fix config first."
    exit 1
  fi
  # Config valid — clear lock
  local state attempts last_backup
  state=$(read_state)
  attempts=$(echo "$state" | jq -r '.attempts' 2>/dev/null || echo 0)
  last_backup=$(echo "$state" | jq -r '.last_backup' 2>/dev/null || echo "")
  write_state 0 "" "$last_backup" false ""
  # Update baseline to current valid config
  update_baseline
  echo "[GUARDIAN] ✅ unlocked. Locked state cleared, baseline updated."
  audit "UNLOCKED" "manual unlock; config validated ok"
  reload_gateway
}

# ── Entry point ───────────────────────────────────────────────────────────────
main() {
  # Handle subcommands
  if [[ "${1:-}" == "unlock" ]]; then
    init_state
    cmd_unlock
    exit 0
  fi

  self_check
  init_state
  ensure_baseline
  log "🛡️ guardian v3.2 started; dir=$CONFIG_DIR file=$CONFIG_FILE"
  log "   features: state-machine lock(disk), baseline-history($BASELINE_KEEP), SIGUSR1, sha256, audit-log, self-check, unlock-cmd"
  audit "GUARDIAN_START" "v3.2 pid=$$"

  inotifywait -m -e close_write,moved_to --format '%e %f' "$CONFIG_DIR" 2>/dev/null | \
  while read -r evt fname; do
    if [[ "$fname" == "openclaw.json" ]]; then
      log "🔄 change detected ($evt $fname)"
      handle_change || true
    fi
  done
}

main "$@"
