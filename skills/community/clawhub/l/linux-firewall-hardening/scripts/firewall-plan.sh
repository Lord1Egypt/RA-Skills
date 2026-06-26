#!/bin/bash
# Firewall Plan / Dry-Run Script
# Shows what rules will be added/removed without applying anything.
# Run after audit-firewall.sh. Requires a security profile or explicit ports.
#
# Usage:
#   bash scripts/firewall-plan.sh --profile public-web-server
#   bash scripts/firewall-plan.sh --ports 22,80,443
#   bash scripts/firewall-plan.sh --policy-file /path/to/policy.yaml
#   bash scripts/firewall-plan.sh --refresh-audit   # force re-run audit

set -euo pipefail

PROFILE=""
PORTS=""
POLICY_FILE=""
OUTPUT_MODE="text"
REFRESH_AUDIT=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile) PROFILE="$2"; shift 2 ;;
        --ports) PORTS="$2"; shift 2 ;;
        --policy-file) POLICY_FILE="$2"; shift 2 ;;
        --json) OUTPUT_MODE="json"; shift ;;
        --refresh-audit) REFRESH_AUDIT=true; shift ;;
        *) echo "Unknown option: $1"; exit 40 ;;
    esac
done

# Detect backend
BACKEND="none"
ACTIVE_FRONTEND=""
if systemctl is-active ufw &>/dev/null; then
    BACKEND="ufw"
    ACTIVE_FRONTEND="ufw"
elif systemctl is-active firewalld &>/dev/null; then
    BACKEND="firewalld"
    ACTIVE_FRONTEND="firewalld"
elif sudo nft list ruleset 2>/dev/null | grep -q "table"; then
    BACKEND="nftables"
elif sudo iptables -L -n 2>/dev/null | grep -qv "Chain\|policy"; then
    BACKEND="iptables"
fi

# Determine target ports from profile or --ports
declare -a TARGET_PORTS=()
if [[ -n "$PROFILE" ]]; then
    case "$PROFILE" in
        public-web-server) TARGET_PORTS=(22 80 443) ;;
        bastion-host) TARGET_PORTS=(22) ;;
        internal-database) TARGET_PORTS=(22 3306) ;;
        *) echo "Unknown profile: $PROFILE"; exit 40 ;;
    esac
elif [[ -n "$PORTS" ]]; then
    IFS=',' read -ra TARGET_PORTS <<< "$PORTS"
else
    TARGET_PORTS=(22 80 443)
fi

# ---- Plan for each backend ----

plan_ufw() {
    echo "=== UFW Plan ==="
    echo "Backend: ufw (active: $(sudo ufw status 2>/dev/null | head -1))"
    echo "Default policy changes:"
    echo "  incoming: allow -> deny"
    echo "  outgoing: (unchanged: allow)"
    echo ""
    echo "Rules to be added:"
    for port in "${TARGET_PORTS[@]}"; do
        if sudo ufw status | awk '{print $1}' | grep -qx "${port}/tcp"; then
            echo "  [SKIP] ${port}/tcp (already exists)"
        else
            echo "  [ADD]  ${port}/tcp"
        fi
    done
    echo ""
    echo "Rules to be removed: (none)"
    echo ""
    echo "Dry-run validation:"
    sudo ufw --dry-run default deny incoming 2>&1 | sed 's/^/  /'
}

plan_firewalld() {
    local ZONE
    ZONE=$(sudo firewall-cmd --get-default-zone 2>/dev/null || echo "public")
    echo "=== firewalld Plan ==="
    echo "Backend: firewalld (zone: $ZONE)"
    echo ""
    echo "Rules to be added:"
    for port in "${TARGET_PORTS[@]}"; do
        if sudo firewall-cmd --zone="$ZONE" --query-port="${port}/tcp" &>/dev/null; then
            echo "  [SKIP] ${port}/tcp (already in zone $ZONE)"
        else
            echo "  [ADD]  ${port}/tcp to zone $ZONE"
        fi
    done
}

plan_nftables() {
    echo "=== nftables Plan ==="
    echo "Backend: nftables"
    echo ""
    if [[ -f /etc/nftables.conf.new ]]; then
        echo "Validating /etc/nftables.conf.new..."
        sudo nft -c -f /etc/nftables.conf.new 2>&1 | sed 's/^/  /'
    else
        echo "  Would create inet filter table with ports: ${TARGET_PORTS[*]}"
    fi
    echo ""
    echo "Atomic apply command: sudo nft -f /etc/nftables.conf.new"
}

plan_iptables() {
    echo "=== iptables Plan ==="
    echo "Backend: iptables (IPv4 + IPv6)"
    echo ""
    echo "Current INPUT rules (v4):"
    sudo iptables -L INPUT -n --line-numbers 2>/dev/null | sed 's/^/  /'
    echo ""
    echo "Rules to be added (v4):"
    for port in "${TARGET_PORTS[@]}"; do
        if sudo iptables -C INPUT -p tcp --dport "$port" -j ACCEPT 2>/dev/null; then
            echo "  [SKIP] tcp/${port} (already exists)"
        else
            echo "  [ADD]  tcp/${port}"
        fi
    done
}

# ---- JSON output (must match SKILL.md § PLAN JSON schema) ----
plan_json() {
    # --- Audit caching ---
    local AUDIT_CACHE="/tmp/firewall-audit.json"
    local AUDIT_CACHE_TTL=300  # 5 minutes
    local USE_CACHED_AUDIT=false

    if $REFRESH_AUDIT; then
        rm -f "$AUDIT_CACHE"
    fi

    if [[ -f "$AUDIT_CACHE" ]]; then
        local CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$AUDIT_CACHE" 2>/dev/null || stat -f %m "$AUDIT_CACHE" 2>/dev/null || echo 99999)))
        if (( CACHE_AGE < AUDIT_CACHE_TTL )); then
            USE_CACHED_AUDIT=true
        fi
    fi

    if ! $USE_CACHED_AUDIT; then
        bash "$SCRIPT_DIR/audit-firewall.sh" --json > "$AUDIT_CACHE" 2>/dev/null || true
    fi

    # --- Build diff objects (structured, not flat strings) ---
    local add_entries=""
    local skip_entries=""
    local add_count=0
    local skip_count=0

    for port in "${TARGET_PORTS[@]}"; do
        if [[ "$BACKEND" == "ufw" ]] && sudo ufw status 2>/dev/null | awk '{print $1}' | grep -qx "${port}/tcp"; then
            (( ++skip_count ))
            skip_entries+="        {\"port\":$port,\"proto\":\"tcp\",\"reason\":\"already_exists\"},
"
        else
            (( ++add_count ))
            add_entries+="        {\"port\":$port,\"proto\":\"tcp\",\"source\":\"any\"},
"
        fi
    done

    # Trim trailing commas/newlines
    add_entries="${add_entries%,$'\n'}"
    skip_entries="${skip_entries%,$'\n'}"

    # --- Risk assessment ---
    local RISK="low"
    local DISRUPTION="none"
    if [[ $skip_count -eq 0 && $add_count -le 2 ]]; then
        RISK="low"
        DISRUPTION="none"
    elif [[ $add_count -ge 5 ]]; then
        RISK="medium"
        DISRUPTION="brief_outage_possible"
    else
        RISK="low"
        DISRUPTION="momentary"
    fi

    # --- Approval token (sha256 of plan fingerprint) ---
    local PLAN_CONTENT="${BACKEND}|${ACTIVE_FRONTEND}|${PROFILE:-none}|${TARGET_PORTS[*]}|${RISK}|${DISRUPTION}"
    local APPROVAL_TOKEN="sha256:$(echo -n "$PLAN_CONTENT" | sha256sum | awk '{print $1}')"

    cat <<EOF
{
  "backend": "$BACKEND",
  "active_frontend": "$ACTIVE_FRONTEND",
  "profile": "${PROFILE:-none}",
  "target_ports": [${TARGET_PORTS[*]// /, }],
  "diff": {
    "add": [
$add_entries
    ],
    "skip": [
$skip_entries
    ],
    "remove": []
  },
  "risk_assessment": "$RISK",
  "estimated_disruption": "$DISRUPTION",
  "approval_token": "$APPROVAL_TOKEN",
  "audit_cached": $USE_CACHED_AUDIT,
  "audit_cache_file": "$AUDIT_CACHE"
}
EOF
}

if [[ "$OUTPUT_MODE" == "json" ]]; then
    PLAN_CACHE="/tmp/firewall-plan.json"
    plan_json | tee "$PLAN_CACHE"
else
    case "$BACKEND" in
        ufw) plan_ufw ;;
        firewalld) plan_firewalld ;;
        nftables) plan_nftables ;;
        iptables) plan_iptables ;;
        *) echo "Cannot determine firewall backend. Run audit-firewall.sh first."; exit 11 ;;
    esac
fi
