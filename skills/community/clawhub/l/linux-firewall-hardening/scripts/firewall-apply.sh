#!/bin/bash
# Firewall Apply Script
# Applies firewall rules after PLAN approval. Requires an approved plan token.
# Run after firewall-plan.sh and VALIDATE steps. Do NOT skip VALIDATE.
#
# Usage:
#   bash scripts/firewall-apply.sh --approved-plan=<sha256:...>
#   bash scripts/firewall-apply.sh --approved-plan=<token> --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPROVED_TOKEN=""
DRY_RUN=false
ROLLBACK_TIMER_MINUTES=5

while [[ $# -gt 0 ]]; do
    case "$1" in
        --approved-plan) APPROVED_TOKEN="$2"; shift 2 ;;
        --approved-plan=*) APPROVED_TOKEN="${1#*=}"; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        *) echo "Unknown option: $1"; exit 40 ;;
    esac
done

if [[ -z "$APPROVED_TOKEN" ]]; then
    echo "ERROR: --approved-plan=<token> is required. Run firewall-plan.sh --json to get the plan and its approval_token." >&2
    exit 40  # PREFLIGHT: missing required parameter
fi

PLAN_CACHE="/tmp/firewall-plan.json"
# --- Verify approval token against cached plan ---
# Plan output is cached by firewall-plan.sh --json to PLAN_CACHE
if [[ ! -f "$PLAN_CACHE" ]]; then
    echo "ERROR: No plan cache found. Run firewall-plan.sh --json first." >&2
    exit 40  # PREFLIGHT: plan cache missing — run PLAN first
fi

# Read token from cached plan file (do NOT re-run plan; that would self-verify)
PLAN_JSON=$(cat "$PLAN_CACHE")
PLAN_TOKEN=$(echo "$PLAN_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['approval_token'])" 2>/dev/null || echo "")

if [[ -z "$PLAN_TOKEN" ]]; then
    echo "ERROR: Could not extract approval_token from plan cache. Re-run firewall-plan.sh --json." >&2
    exit 40  # PREFLIGHT: plan cache malformed — re-run PLAN
fi

if [[ "$APPROVED_TOKEN" != "$PLAN_TOKEN" ]]; then
    echo "ERROR: approval_token mismatch." >&2
    echo "  Expected: $PLAN_TOKEN" >&2
    echo "  Got:      $APPROVED_TOKEN" >&2
    echo "  The plan has changed since approval. Re-run VALIDATE with the new plan." >&2
    exit 41  # PREFLIGHT: plan approval mismatch
fi

# --- Gate: ensure VALIDATE ran (check for rollback timer) ---
# Detection is best-effort: at jobs can't be tagged, so we check for any pending at job.
# Systemd transient timers are scoped to --user (matching VALIDATE's systemd-run --user).
ROLLBACK_TIMER_ACTIVE=false
if command -v at &>/dev/null && atq 2>/dev/null | grep -q '[0-9]'; then
    ROLLBACK_TIMER_ACTIVE=true
elif command -v systemctl &>/dev/null; then
    # Check both system and user scope (VALIDATE uses --user)
    systemctl list-units --type=service --state=running 2>/dev/null | grep -q 'firewall-rollback' && ROLLBACK_TIMER_ACTIVE=true
    $ROLLBACK_TIMER_ACTIVE || systemctl --user list-units --type=service --state=running 2>/dev/null | grep -q 'firewall-rollback' && ROLLBACK_TIMER_ACTIVE=true
fi

if ! $ROLLBACK_TIMER_ACTIVE; then
    echo "WARNING: No rollback timer detected. VALIDATE step may have been skipped." >&2
    echo "Without a rollback timer, a misconfigured firewall rule could lock you out." >&2
    echo "Aborting. Run VALIDATE to schedule a rollback timer, then re-run APPLY." >&2
    exit 40  # PREFLIGHT: no rollback safety net — run VALIDATE first
fi

# --- Apply rules ---
BACKEND=$(echo "$PLAN_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['backend'])" 2>/dev/null || echo "none")
TARGET_PORTS=$(echo "$PLAN_JSON" | python3 -c "import sys,json; print(','.join(str(p) for p in json.load(sys.stdin)['target_ports']))" 2>/dev/null || echo "22,80,443")

echo "=== Applying firewall rules ==="
echo "Backend: $BACKEND"
echo "Ports: $TARGET_PORTS"
echo "Approval: $APPROVED_TOKEN"
echo "Dry-run: $DRY_RUN"
echo ""

apply_ufw() {
    echo "[ufw] Setting default deny incoming..."
    if ! $DRY_RUN; then
        sudo ufw default deny incoming
        sudo ufw default allow outgoing
    else
        echo "  [DRY-RUN] sudo ufw default deny incoming"
    fi
    for port in $(echo "$TARGET_PORTS" | tr ',' ' '); do
        if $DRY_RUN; then
            echo "  [DRY-RUN] sudo ufw allow ${port}/tcp"
        else
            sudo ufw allow "${port}/tcp" && echo "  ufw allow ${port}/tcp ✓"
        fi
    done
    if ! $DRY_RUN; then
        sudo ufw --force enable
        echo "ufw enabled"
    fi
}

apply_firewalld() {
    local ZONE
    ZONE=$(sudo firewall-cmd --get-default-zone 2>/dev/null || echo "public")
    echo "[firewalld] Zone: $ZONE"
    for port in $(echo "$TARGET_PORTS" | tr ',' ' '); do
        if $DRY_RUN; then
            echo "  [DRY-RUN] sudo firewall-cmd --zone=$ZONE --add-port=${port}/tcp --permanent"
        else
            sudo firewall-cmd --zone="$ZONE" --add-port="${port}/tcp" --permanent && echo "  ${port}/tcp added to $ZONE ✓"
        fi
    done
    if ! $DRY_RUN; then
        sudo firewall-cmd --reload
        echo "firewalld reloaded"
    fi
}

apply_nftables() {
    echo "[nftables] This backend requires a pre-built /etc/nftables.conf.new"
    echo "  Run firewall-plan.sh first to prepare the config."
    if [[ -f /etc/nftables.conf.new ]]; then
        if $DRY_RUN; then
            echo "  [DRY-RUN] sudo nft -c -f /etc/nftables.conf.new"
        else
            sudo nft -c -f /etc/nftables.conf.new && sudo nft -f /etc/nftables.conf.new
            echo "nftables rules applied"
        fi
    else
        echo "  ERROR: /etc/nftables.conf.new not found"
        exit 40
    fi
}

apply_iptables() {
    echo "[iptables] Adding INPUT rules..."
    for port in $(echo "$TARGET_PORTS" | tr ',' ' '); do
        if sudo iptables -C INPUT -p tcp --dport "$port" -j ACCEPT 2>/dev/null; then
            echo "  [SKIP] tcp/${port} (already exists)"
        else
            if $DRY_RUN; then
                echo "  [DRY-RUN] sudo iptables -A INPUT -p tcp --dport $port -j ACCEPT"
            else
                sudo iptables -A INPUT -p tcp --dport "$port" -j ACCEPT && echo "  tcp/${port} ACCEPT added ✓"
            fi
        fi
    done
}

case "$BACKEND" in
    ufw) apply_ufw ;;
    firewalld) apply_firewalld ;;
    nftables) apply_nftables ;;
    iptables) apply_iptables ;;
    *) echo "ERROR: Unknown backend '$BACKEND'"; exit 40 ;;
esac

echo ""
echo "=== Apply complete ==="
echo "Next step: Run firewall-verify.sh"
if $DRY_RUN; then
    echo "  bash $SCRIPT_DIR/firewall-verify.sh"
    exit 0
fi

# --- Verify immediately ---
echo ""
echo "Running verification..."
bash "$SCRIPT_DIR/firewall-verify.sh"
VERIFY_EXIT=$?

if [[ $VERIFY_EXIT -eq 0 ]]; then
    echo ""
    echo "All checks passed. Rollback timer will be cancelled by firewall-verify.sh on success."
    exit 0
else
    echo ""
    echo "WARNING: Verification failed (exit code $VERIFY_EXIT). Leave the rollback timer running and investigate."
    exit 51  # APPLY: verify failed after apply
fi