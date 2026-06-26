#!/bin/bash
# safe-upgrade.sh — Atomic OpenClaw upgrade with auto-rollback
#
# ONE command. Backs up everything → upgrades → verifies → auto-rollbacks on ANY failure.
#
# CRITICAL: This script MUST survive the gateway restart it triggers.
# When run inside a systemd service cgroup (e.g., openclaw-gateway.service),
# `systemctl stop` will SIGKILL all processes in the cgroup — including us.
# Solution: re-exec ourselves via `systemd-run --user --scope` to escape
# into our own transient scope unit before touching the gateway.
#
# Usage: bash safe-upgrade.sh [--check] [--rollback] [--force]
#   (no args)    = full atomic upgrade
#   --check      = pre-flight only (no changes)
#   --rollback   = manual rollback from last upgrade
#   --force      = skip "already on latest" check

set -euo pipefail

# ─────────────────────────────────────────────
# CGROUP ESCAPE: Re-exec in own scope if inside gateway cgroup
#
# The escaped process must be FULLY DETACHED — no pipes, no parent shell,
# no tee connecting back to the gateway cgroup. If any part of the pipeline
# stays in the gateway cgroup, systemd kills it on stop, breaking the pipe
# → SIGPIPE → our process dies.
#
# The calling agent should fire this and then poll the log/result file.
# ─────────────────────────────────────────────
LIVE_LOG="/tmp/upgrade-live.log"

if [ "${_UPGRADE_ESCAPED:-}" != "1" ]; then
    OUR_CGROUP=$(cat /proc/self/cgroup 2>/dev/null | grep -o "openclaw-gateway" || true)
    if [ -n "$OUR_CGROUP" ] || [ "${_UPGRADE_FORCE_ESCAPE:-}" = "1" ]; then
        echo "[upgrade] Escaping systemd cgroup via systemd-run --scope..."
        echo "[upgrade] Output: $LIVE_LOG"
        echo "[upgrade] Result: $HOME/.openclaw/upgrade-result.json"
        echo "[upgrade] Monitor: tail -f $LIVE_LOG"
        export _UPGRADE_ESCAPED=1
        systemd-run --user --scope --unit="openclaw-upgrade-$$" \
            bash "$0" "$@" >"$LIVE_LOG" 2>&1 &
        disown
        echo "[upgrade] Launched in own scope. This shell will exit now."
        exit 0
    fi
fi

# ─────────────────────────────────────────────
# CONFIG — auto-detect paths
# ─────────────────────────────────────────────
# Workspace: try openclaw config, then common locations
WORKSPACE="${OPENCLAW_WORKSPACE:-}"
if [ -z "$WORKSPACE" ]; then
    WORKSPACE=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json')).get('workspace',''))" 2>/dev/null || echo "")
fi
if [ -z "$WORKSPACE" ] || [ ! -d "$WORKSPACE" ]; then
    # Fallback: common workspace locations
    for d in "$HOME/openclaw" "$HOME/workspace"; do
        [ -d "$d" ] && WORKSPACE="$d" && break
    done
fi

OC_INSTALL="/usr/lib/node_modules/openclaw"
OC_CONFIG="$HOME/.openclaw/openclaw.json"
CRON_JOBS="$HOME/.openclaw/cron/jobs.json"
ACPX_CONFIG="$HOME/.acpx/config.json"
ACPX_PLUGIN="$OC_INSTALL/extensions/acpx"
BACKUP_BASE="$HOME/.openclaw/upgrade-backups"
BACKUP_CURRENT="$BACKUP_BASE/current"
RESULT_FILE="$HOME/.openclaw/upgrade-result.json"
UPGRADE_LOG="$HOME/.openclaw/upgrade-last.log"

GATEWAY_TIMEOUT=120       # seconds to wait for gateway health after restart
WHATSAPP_TIMEOUT=60       # seconds to wait for WhatsApp reconnect

# Detect gateway port from config (fallback: 3377)
GATEWAY_PORT=$(python3 -c "import json; print(json.load(open('$OC_CONFIG')).get('gateway',{}).get('port', 3377))" 2>/dev/null || echo "3377")

# Track upgrade phase for trap handler
UPGRADE_PHASE="not_started"
UPGRADE_FROM=""
UPGRADE_TO=""

# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
log()  { echo -e "${GREEN}[upgrade]${NC} $1" | tee -a "$UPGRADE_LOG"; }
warn() { echo -e "${YELLOW}[upgrade]${NC} $1" | tee -a "$UPGRADE_LOG"; }
fail() { echo -e "${RED}[upgrade]${NC} $1" | tee -a "$UPGRADE_LOG"; }
ts()   { date -u '+%Y-%m-%d %H:%M:%S UTC'; }

# ─────────────────────────────────────────────
# RESULT FILE (so next agent session can report)
# ─────────────────────────────────────────────
write_result() {
    local status="$1" from_ver="$2" to_ver="$3" msg="$4"
    cat > "$RESULT_FILE" << EOF
{
    "status": "$status",
    "from_version": "$from_ver",
    "to_version": "$to_ver",
    "message": "$msg",
    "timestamp": "$(ts)",
    "hostname": "$(hostname)",
    "log": "$UPGRADE_LOG"
}
EOF
}

# ─────────────────────────────────────────────
# TRAP HANDLER — auto-rollback on unexpected exit
# ─────────────────────────────────────────────
cleanup_on_exit() {
    local exit_code=$?
    if [ "$UPGRADE_PHASE" = "installed_waiting" ] || [ "$UPGRADE_PHASE" = "restarting" ]; then
        fail "Script interrupted during phase: $UPGRADE_PHASE (exit code: $exit_code)"
        fail "Backup exists at $BACKUP_CURRENT — attempting auto-rollback..."
        do_rollback "script interrupted during $UPGRADE_PHASE"
    elif [ "$UPGRADE_PHASE" = "npm_installing" ]; then
        fail "Script interrupted during npm install (exit code: $exit_code)"
        if [ -d "$BACKUP_CURRENT" ]; then
            do_rollback "npm install interrupted"
        fi
    fi
}

# ─────────────────────────────────────────────
# HEALTH CHECKS
# ─────────────────────────────────────────────
wait_for_gateway() {
    local timeout=$1
    local elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if curl -sf -o /dev/null "http://127.0.0.1:${GATEWAY_PORT}/" 2>/dev/null; then
            return 0
        fi
        if openclaw gateway status 2>/dev/null | grep -q "state active"; then
            return 0
        fi
        sleep 3
        elapsed=$((elapsed + 3))
    done
    return 1
}

wait_for_whatsapp() {
    local timeout=$1
    local elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if openclaw gateway status 2>/dev/null | grep -qi "connected"; then
            return 0
        fi
        sleep 5
        elapsed=$((elapsed + 5))
    done
    return 1
}

count_crons() {
    python3 -c "import json; print(len(json.load(open('$CRON_JOBS')).get('jobs',[])))" 2>/dev/null || echo "0"
}

# ─────────────────────────────────────────────
# ROLLBACK
# ─────────────────────────────────────────────
do_rollback() {
    local reason="${1:-manual}"
    UPGRADE_PHASE="rolling_back"
    fail "ROLLING BACK ($reason)..."

    if [ ! -d "$BACKUP_CURRENT" ]; then
        fail "No backup found at $BACKUP_CURRENT — cannot rollback!"
        write_result "rollback_failed" "${UPGRADE_FROM:-unknown}" "${UPGRADE_TO:-unknown}" "No backup found: $reason"
        return 1
    fi

    local from_ver to_ver
    from_ver=$(python3 -c "import json; print(json.load(open('$BACKUP_CURRENT/metadata.json'))['from_version'])" 2>/dev/null || echo "unknown")
    to_ver=$(python3 -c "import json; print(json.load(open('$BACKUP_CURRENT/metadata.json'))['to_version'])" 2>/dev/null || echo "unknown")

    log "Stopping gateway..."
    openclaw gateway stop 2>/dev/null || true
    pkill -f "openclaw.*gateway" 2>/dev/null || true
    sleep 3

    log "Restoring installation ($from_ver)..."
    rm -rf "$OC_INSTALL"
    tar -xzf "$BACKUP_CURRENT/openclaw-install.tar.gz" -C /usr/lib/node_modules/

    log "Restoring config..."
    cp "$BACKUP_CURRENT/openclaw.json" "$OC_CONFIG"

    log "Restoring cron jobs..."
    cp "$BACKUP_CURRENT/jobs.json" "$CRON_JOBS"

    if [ -f "$BACKUP_CURRENT/acpx-config.json" ]; then
        log "Restoring acpx config..."
        mkdir -p "$(dirname "$ACPX_CONFIG")"
        cp "$BACKUP_CURRENT/acpx-config.json" "$ACPX_CONFIG"
    fi
    if [ -f "$BACKUP_CURRENT/acpx-plugin.tar.gz" ]; then
        log "Restoring acpx plugin..."
        rm -rf "$ACPX_PLUGIN"
        tar -xzf "$BACKUP_CURRENT/acpx-plugin.tar.gz" -C "$OC_INSTALL/extensions/" 2>/dev/null || true
    fi

    log "Starting gateway on restored version..."
    if systemctl --user start openclaw-gateway.service 2>/dev/null; then
        log "   Started via systemd"
    else
        openclaw gateway start 2>/dev/null || true
    fi

    if wait_for_gateway $GATEWAY_TIMEOUT; then
        local restored_ver
        restored_ver=$(openclaw --version 2>/dev/null || echo "unknown")
        log "✅ Rollback complete → $restored_ver"
        write_result "rolled_back" "$to_ver" "$restored_ver" "Auto-rollback: $reason"
    else
        fail "❌ Gateway didn't come back after rollback. Manual intervention needed."
        fail "   Try: pkill -f 'openclaw.*gateway'; systemctl --user start openclaw-gateway.service"
        write_result "rollback_failed" "$to_ver" "unknown" "Gateway failed after rollback: $reason"
    fi
}

# ─────────────────────────────────────────────
# PRE-FLIGHT CHECK
# ─────────────────────────────────────────────
do_check() {
    log "=== Pre-flight Check ($(ts)) ==="

    local current latest cron_count disk_free
    current=$(openclaw --version 2>/dev/null || echo "unknown")
    latest=$(npm view openclaw version 2>/dev/null || echo "unknown")
    cron_count=$(count_crons)
    disk_free=$(df -h / | awk 'NR==2{print $4}')

    log "Current:    $current"
    log "Available:  $latest"
    log "Cron jobs:  $cron_count"
    log "Disk free:  $disk_free"

    # Breaking change: gateway.auth.mode required when both token+password set (2026.3.7+)
    log "Checking for breaking changes..."
    local has_token has_password has_mode
    has_token=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('token') else 'no')" 2>/dev/null || echo "unknown")
    has_password=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('password') else 'no')" 2>/dev/null || echo "unknown")
    has_mode=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('mode') else 'no')" 2>/dev/null || echo "unknown")

    if [ "$has_token" = "yes" ] && [ "$has_password" = "yes" ] && [ "$has_mode" != "yes" ]; then
        fail "   ❌ BREAKING: gateway.auth.mode must be set (both token and password configured)"
        fail "   Fix: Add \"mode\": \"token\" (or \"password\") to gateway.auth in openclaw.json"
        return 3
    fi
    log "   ✅ No breaking change conflicts detected"

    local disk_avail_kb
    disk_avail_kb=$(df / | awk 'NR==2{print $4}')
    if [ "$disk_avail_kb" -lt 1048576 ]; then
        fail "   ❌ Insufficient disk space: need 1GB, have ${disk_free}"
        return 4
    fi
    log "   ✅ Disk space OK ($disk_free available)"

    if [ "$current" = "$latest" ]; then
        log "✅ Already on latest. No upgrade needed."
        return 1
    fi

    if [ -d "$BACKUP_CURRENT" ]; then
        warn "⚠️  Previous backup exists — run --rollback or delete $BACKUP_CURRENT first"
        return 2
    fi

    log "✅ Ready to upgrade: $current → $latest"
    return 0
}

# ─────────────────────────────────────────────
# GATEWAY RESTART (process-isolated)
# ─────────────────────────────────────────────
restart_gateway_isolated() {
    log "   Stopping gateway..."
    openclaw gateway stop 2>/dev/null || true
    pkill -f "openclaw.*gateway" 2>/dev/null || true
    sleep 3

    local attempts=0
    while pgrep -f "openclaw.*gateway" >/dev/null 2>&1 && [ $attempts -lt 10 ]; do
        sleep 1
        attempts=$((attempts + 1))
    done

    if pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
        warn "   Gateway still running — force killing"
        pkill -9 -f "openclaw.*gateway" 2>/dev/null || true
        sleep 2
    fi

    log "   Starting gateway..."
    if systemctl --user start openclaw-gateway.service 2>/dev/null; then
        log "   Started via systemd"
    else
        nohup openclaw gateway start </dev/null >>/tmp/openclaw-upgrade-gateway.log 2>&1 &
        disown
        log "   Started via nohup (PID: $!)"
    fi
}

# ─────────────────────────────────────────────
# ATOMIC UPGRADE
# ─────────────────────────────────────────────
do_upgrade() {
    local force="${1:-}"

    echo "=== Upgrade started: $(ts) ===" > "$UPGRADE_LOG"

    log "════════════════════════════════════════════"
    log "  ATOMIC UPGRADE — $(ts)"
    log "════════════════════════════════════════════"

    trap cleanup_on_exit EXIT

    # ── Pre-flight ──
    local current latest
    current=$(openclaw --version 2>/dev/null || echo "unknown")
    latest=$(npm view openclaw version 2>/dev/null || echo "unknown")
    UPGRADE_FROM="$current"
    UPGRADE_TO="$latest"

    if [ "$current" = "$latest" ] && [ "$force" != "force" ]; then
        log "Already on latest ($current). Nothing to do."
        write_result "no_change" "$current" "$current" "Already on latest"
        UPGRADE_PHASE="complete"
        exit 0
    fi

    if [ -d "$BACKUP_CURRENT" ]; then
        fail "Previous backup exists. Run --rollback or delete $BACKUP_CURRENT first."
        UPGRADE_PHASE="complete"
        exit 1
    fi

    # Breaking change checks
    log "Running pre-flight checks..."
    local has_token has_password has_mode
    has_token=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('token') else 'no')" 2>/dev/null || echo "unknown")
    has_password=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('password') else 'no')" 2>/dev/null || echo "unknown")
    has_mode=$(python3 -c "import json; c=json.load(open('$OC_CONFIG')); print('yes' if c.get('gateway',{}).get('auth',{}).get('mode') else 'no')" 2>/dev/null || echo "unknown")

    if [ "$has_token" = "yes" ] && [ "$has_password" = "yes" ] && [ "$has_mode" != "yes" ]; then
        fail "BLOCKED: gateway.auth.mode must be set before upgrading to $latest"
        write_result "blocked" "$current" "$latest" "Breaking change: gateway.auth.mode required"
        UPGRADE_PHASE="complete"
        exit 1
    fi

    local pre_cron_count
    pre_cron_count=$(count_crons)
    log "Upgrading: $current → $latest ($pre_cron_count cron jobs)"

    # ── Step 1: Full backup ──
    UPGRADE_PHASE="backing_up"
    log "① Backing up everything..."
    mkdir -p "$BACKUP_CURRENT"

    cp "$CRON_JOBS" "$BACKUP_CURRENT/jobs.json"
    tar -czf "$BACKUP_CURRENT/openclaw-install.tar.gz" -C /usr/lib/node_modules openclaw 2>/dev/null || true
    cp "$OC_CONFIG" "$BACKUP_CURRENT/openclaw.json"

    if [ -f "$ACPX_CONFIG" ]; then
        cp "$ACPX_CONFIG" "$BACKUP_CURRENT/acpx-config.json"
    fi
    if [ -d "$ACPX_PLUGIN" ]; then
        tar -czf "$BACKUP_CURRENT/acpx-plugin.tar.gz" -C "$OC_INSTALL/extensions/" acpx 2>/dev/null || true
    fi

    cat > "$BACKUP_CURRENT/metadata.json" << METAEOF
{
    "from_version": "$current",
    "to_version": "$latest",
    "timestamp": "$(ts)",
    "cron_count": $pre_cron_count,
    "hostname": "$(hostname)"
}
METAEOF

    local backup_size
    backup_size=$(du -sh "$BACKUP_CURRENT" | cut -f1)
    log "   Backup complete ($backup_size)"
    UPGRADE_PHASE="backed_up"

    # ── Step 2: Install ──
    UPGRADE_PHASE="npm_installing"
    log "② Installing openclaw@$latest..."
    if ! npm i -g openclaw@latest --no-fund --no-audit --loglevel=error 2>&1 | tee -a "$UPGRADE_LOG"; then
        fail "npm install failed"
        do_rollback "npm install failed"
        UPGRADE_PHASE="complete"
        exit 1
    fi

    local installed_ver
    installed_ver=$(openclaw --version 2>/dev/null || echo "unknown")
    log "   Installed: $installed_ver"
    UPGRADE_PHASE="installed_waiting"

    # ── Step 3: Restore acpx ──
    log "③ Restoring acpx customizations..."
    if [ -f "$BACKUP_CURRENT/acpx-config.json" ]; then
        mkdir -p "$(dirname "$ACPX_CONFIG")"
        cp "$BACKUP_CURRENT/acpx-config.json" "$ACPX_CONFIG"
        log "   acpx config restored"
    fi

    # ── Step 4: Restart gateway ──
    UPGRADE_PHASE="restarting"
    log "④ Restarting gateway (process-isolated)..."
    restart_gateway_isolated
    sleep 5

    # ── Step 5: Wait for gateway health ──
    log "⑤ Waiting for gateway (${GATEWAY_TIMEOUT}s timeout)..."
    if ! wait_for_gateway $GATEWAY_TIMEOUT; then
        fail "Gateway didn't respond within ${GATEWAY_TIMEOUT}s"
        do_rollback "gateway health timeout after ${GATEWAY_TIMEOUT}s"
        UPGRADE_PHASE="complete"
        exit 1
    fi
    log "   Gateway healthy ✓"

    # ── Step 6: Wait for WhatsApp ──
    log "⑥ Waiting for WhatsApp (${WHATSAPP_TIMEOUT}s timeout)..."
    if wait_for_whatsapp $WHATSAPP_TIMEOUT; then
        log "   WhatsApp connected ✓"
    else
        warn "   WhatsApp not connected yet (non-fatal)"
    fi

    # ── Step 7: Verify ──
    UPGRADE_PHASE="verifying"
    log "⑦ Verifying..."
    local post_ver post_crons all_pass=true

    post_ver=$(openclaw --version 2>/dev/null || echo "unknown")
    if [ "$post_ver" = "$latest" ]; then
        log "   ✅ Version: $post_ver"
    else
        fail "   ❌ Version: expected $latest, got $post_ver"
        all_pass=false
    fi

    post_crons=$(count_crons)
    if [ "$post_crons" -ge "$pre_cron_count" ]; then
        log "   ✅ Crons: $post_crons (was $pre_cron_count)"
    else
        fail "   ❌ Crons: $post_crons (was $pre_cron_count) — LOST JOBS"
        all_pass=false
    fi

    # Optional: workspace service health check
    if [ -n "$WORKSPACE" ] && [ -f "$WORKSPACE/scripts/service-quick-check.py" ]; then
        if python3 "$WORKSPACE/scripts/service-quick-check.py" >/dev/null 2>&1; then
            log "   ✅ Services: healthy"
        else
            warn "   ⚠️  Services: issues (non-fatal)"
        fi
    fi

    if [ "$all_pass" = false ]; then
        do_rollback "post-upgrade verification failed"
        UPGRADE_PHASE="complete"
        exit 1
    fi

    UPGRADE_PHASE="verified"

    # ── Step 8: Record result (BEFORE cleanup) ──
    log "⑧ Recording result..."
    write_result "success" "$current" "$post_ver" "Upgrade successful"

    # ── Step 9: Optional golden snapshot ──
    if [ -n "$WORKSPACE" ] && [ -f "$WORKSPACE/scripts/golden-snapshot.sh" ]; then
        log "⑨ Taking golden snapshot..."
        local label="gold-$(date +%Y-%m-%d)"
        bash "$WORKSPACE/scripts/golden-snapshot.sh" "$label" 2>/dev/null || true
        log "   Snapshot: $label"
    else
        log "⑨ Golden snapshot skipped (no snapshot script found)"
    fi

    # ── Step 10: Cleanup ──
    log "⑩ Cleaning up backup..."
    rm -rf "$BACKUP_CURRENT"

    # Optional: git commit in workspace
    if [ -n "$WORKSPACE" ] && [ -d "$WORKSPACE/.git" ]; then
        cd "$WORKSPACE"
        git add -A 2>/dev/null || true
        git commit -m "upgrade: OpenClaw $current → $post_ver" 2>/dev/null || true
        git push 2>/dev/null || true
    fi

    UPGRADE_PHASE="complete"

    echo "" | tee -a "$UPGRADE_LOG"
    log "════════════════════════════════════════════"
    log "  ✅ UPGRADE COMPLETE: $current → $post_ver"
    log "  Crons: $post_crons"
    log "════════════════════════════════════════════"
}

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
case "${1:-}" in
    --check)
        do_check
        ;;
    --rollback)
        do_rollback "manual"
        ;;
    --force)
        do_upgrade "force"
        ;;
    "")
        do_upgrade
        ;;
    *)
        echo "Usage: safe-upgrade.sh [--check | --rollback | --force]"
        echo ""
        echo "  (no args)    Full atomic upgrade with auto-rollback"
        echo "  --check      Pre-flight only (no changes)"
        echo "  --rollback   Manual rollback from last upgrade"
        echo "  --force      Upgrade even if already on latest"
        exit 1
        ;;
esac
