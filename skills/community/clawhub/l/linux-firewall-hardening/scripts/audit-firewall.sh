#!/bin/bash
# Firewall Environment Audit Script
# Run this to detect the active firewall stack, Docker, cloud provider, SSH port, exposure, and ownership.
# Safe to run anywhere; makes no changes.
#
# Usage:
#   bash scripts/audit-firewall.sh          # Human-readable output
#   bash scripts/audit-firewall.sh --json   # Machine-readable JSON to stdout

set -euo pipefail

OUTPUT_MODE="text"
[[ "${1:-}" == "--json" ]] && OUTPUT_MODE="json"

# Global state
declare CONFIDENCE=100
declare -a WARNINGS=()
declare ACTIVE_FRONTENDS=()
declare CONTAINERIZED=false
declare CLOUD_PROVIDER="none"
declare SSH_PORT=""
declare SSH_SOURCE=""
declare RECOMMENDED_BACKEND=""
declare BACKEND_RAW=""
declare OWNERSHIP="manual"
declare DOCKER_HOST=false
declare K8S_NODE=false
declare CNI_PLUGIN=""
declare HALT_REASONS=()
declare FAIL2BAN_ACTIVE=false
declare RISK_TIER="auto"
declare AT_AVAILABLE=false
declare SYSTEMD_RUN_AVAILABLE=false

# ---- Detection Functions ----

detect_firewall_tools() {
    local tools=()
    which iptables &>/dev/null && tools+=("iptables")
    which nft &>/dev/null && tools+=("nft")
    which ufw &>/dev/null && tools+=("ufw")
    which firewall-cmd &>/dev/null && tools+=("firewall-cmd")
    echo "${tools[@]}"
}

detect_containerization() {
    if [[ -f /.dockerenv ]]; then
        CONTAINERIZED=true
        HALT_REASONS+=("Inside Docker container — do not modify host firewall")
    elif [[ -f /run/.containerenv ]]; then
        CONTAINERIZED=true
        HALT_REASONS+=("Inside Podman container — do not modify host firewall")
    fi
}

detect_cloud_provider() {
    if curl -s --max-time 2 http://169.254.169.254/latest/meta-data/ >/dev/null 2>&1; then
        CLOUD_PROVIDER="aws"
    elif curl -s --max-time 2 -H "Metadata-Flavor: Google" http://metadata.google.internal/ >/dev/null 2>&1; then
        CLOUD_PROVIDER="gcp"
    elif curl -s --max-time 2 -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" >/dev/null 2>&1; then
        CLOUD_PROVIDER="azure"
    fi
}

detect_ssh() {
    SSH_PORT=$(ss -tlnp 2>/dev/null | grep -E "sshd|ssh" | awk -F: '{print $NF}' | head -1 || true)
    SSH_PORT=${SSH_PORT:-22}
    # Detect SSH source address (current connection)
    SSH_SOURCE=$(who -m 2>/dev/null | awk '{print $NF}' | tr -d '()' | head -1 || true)
    SSH_SOURCE=${SSH_SOURCE:-"unknown"}
}

detect_active_frontends() {
    if systemctl is-active ufw &>/dev/null; then
        ACTIVE_FRONTENDS+=("ufw")
    fi
    if systemctl is-active firewalld &>/dev/null; then
        ACTIVE_FRONTENDS+=("firewalld")
    fi
    if [[ ${#ACTIVE_FRONTENDS[@]} -gt 1 ]]; then
        CONFIDENCE=$((CONFIDENCE - 30))
        WARNINGS+=("Both ufw and firewalld are active — conflicting frontends")
        HALT_REASONS+=("Multiple active firewall frontends (${ACTIVE_FRONTENDS[*]}) — resolve conflict first")
    fi
}

detect_backend() {
    local has_nft_rules=false
    local has_ipt_rules=false

    if sudo nft list ruleset 2>/dev/null | grep -q "table"; then
        has_nft_rules=true
    fi
    if sudo iptables -L -n 2>/dev/null | grep -qv "Chain\|policy"; then
        has_ipt_rules=true
    fi

    if $has_nft_rules && $has_ipt_rules; then
        BACKEND_RAW="nftables+iptables"
    elif $has_nft_rules; then
        BACKEND_RAW="nftables"
    elif $has_ipt_rules; then
        BACKEND_RAW="iptables"
    else
        BACKEND_RAW="none"
    fi
}

detect_docker() {
    if command -v docker &>/dev/null && docker ps >/dev/null 2>&1; then
        DOCKER_HOST=true
    fi
}

detect_k8s() {
    if [[ -f /etc/kubernetes/kubelet.conf ]] || [[ -d /etc/cni/net.d ]] || command -v kubectl &>/dev/null; then
        K8S_NODE=true
        HALT_REASONS+=("Kubernetes node detected — use NetworkPolicies, not host firewall changes")
        # Detect specific CNI
        if ls /etc/cni/net.d/*calico* &>/dev/null 2>&1; then
            CNI_PLUGIN="calico"
        elif ls /etc/cni/net.d/*flannel* &>/dev/null 2>&1; then
            CNI_PLUGIN="flannel"
        elif ls /etc/cni/net.d/*cilium* &>/dev/null 2>&1 || ls /etc/cni/net.d/*05-cilium* &>/dev/null 2>&1; then
            CNI_PLUGIN="cilium"
        else
            CNI_PLUGIN="unknown"
        fi
        CONFIDENCE=$((CONFIDENCE - 50))
        WARNINGS+=("Kubernetes node with CNI: $CNI_PLUGIN — host firewall mutation can break pod networking")
    fi
}

detect_ownership() {
    if [[ -d /opt/terraform ]] || find /etc /var /opt -maxdepth 4 -name "*.tf" -o -name ".terraform" 2>/dev/null | head -1 | grep -q .; then
        OWNERSHIP="terraform"
        HALT_REASONS+=("Firewall managed by Terraform — update .tf and terraform apply instead")
    elif [[ -f /etc/cron.d/ansible-pull ]] || (crontab -l 2>/dev/null | grep -qi ansible); then
        OWNERSHIP="ansible"
        HALT_REASONS+=("Firewall managed by Ansible — update playbook and re-run instead")
    elif which puppet &>/dev/null || [[ -f /etc/puppetlabs/puppet/puppet.conf ]]; then
        OWNERSHIP="puppet"
        HALT_REASONS+=("Firewall managed by Puppet — update manifest and trigger agent instead")
    elif which chef-client &>/dev/null || [[ -d /etc/chef ]]; then
        OWNERSHIP="chef"
        HALT_REASONS+=("Firewall managed by Chef — update cookbook and upload instead")
    elif grep -r "ufw\|firewalld\|iptables" /etc/cloud/cloud.cfg.d/ 2>/dev/null | grep -q .; then
        OWNERSHIP="cloud-init"
        HALT_REASONS+=("Firewall managed by cloud-init — update user-data/cloud-config instead")
    fi

    if [[ "$OWNERSHIP" != "manual" ]]; then
        CONFIDENCE=$((CONFIDENCE - 15))
        WARNINGS+=("Firewall managed by $OWNERSHIP — manual mutation not recommended")
    fi
}

detect_fail2ban() {
    if command -v fail2ban-server &>/dev/null; then
        FAIL2BAN_ACTIVE=true
    fi
}

detect_rollback_capability() {
    if command -v at &>/dev/null && systemctl is-active atd &>/dev/null 2>&1; then
        AT_AVAILABLE=true
    fi
    if command -v systemd-run &>/dev/null; then
        SYSTEMD_RUN_AVAILABLE=true
    fi
    if ! $AT_AVAILABLE && ! $SYSTEMD_RUN_AVAILABLE; then
        CONFIDENCE=$((CONFIDENCE - 25))
        WARNINGS+=("No rollback mechanism available — install 'at' or ensure systemd-run is present")
        HALT_REASONS+=("Cannot schedule rollback: neither 'at' nor 'systemd-run' available. Install: sudo apt install at")
    fi
}

assess_risk_tier() {
    # risk_tier determines what the agent is allowed to do without human confirmation
    if $CONTAINERIZED || $K8S_NODE || [[ "$OWNERSHIP" != "manual" ]]; then
        RISK_TIER="halt"
    elif [[ $CONFIDENCE -ge 90 ]]; then
        RISK_TIER="auto"
    elif [[ $CONFIDENCE -ge 70 ]]; then
        RISK_TIER="confirmed"
    elif [[ $CONFIDENCE -ge 50 ]]; then
        RISK_TIER="manual"
    else
        RISK_TIER="halt"
    fi
}

assess_recommendation() {
    if $CONTAINERIZED; then
        RECOMMENDED_BACKEND="STOP"
    elif $K8S_NODE; then
        RECOMMENDED_BACKEND="STOP"
    elif [[ "$OWNERSHIP" != "manual" ]]; then
        RECOMMENDED_BACKEND="STOP"
    elif [[ " ${ACTIVE_FRONTENDS[@]} " =~ " ufw " ]]; then
        RECOMMENDED_BACKEND="ufw"
    elif [[ " ${ACTIVE_FRONTENDS[@]} " =~ " firewalld " ]]; then
        RECOMMENDED_BACKEND="firewalld"
    elif [[ "$BACKEND_RAW" == "nftables" ]]; then
        RECOMMENDED_BACKEND="nftables"
    elif [[ "$BACKEND_RAW" == "nftables+iptables" ]]; then
        RECOMMENDED_BACKEND="nftables"
    elif [[ "$BACKEND_RAW" == "iptables" ]]; then
        RECOMMENDED_BACKEND="iptables"
    else
        RECOMMENDED_BACKEND="install"
        CONFIDENCE=$((CONFIDENCE - 20))
        WARNINGS+=("No firewall tools installed — installation path required")
    fi
}

# ---- Output Functions ----

output_json() {
    local DQ='"'
    local halt_json="["
    local comma=""
    for reason in "${HALT_REASONS[@]}"; do
        halt_json+="${comma}${DQ}${reason}${DQ}"
        comma=","
    done
    halt_json+="]"

    local frontends_json="["
    comma=""
    local DQ='"'
    for f in "${ACTIVE_FRONTENDS[@]}"; do
        frontends_json+="${comma}${DQ}${f}${DQ}"
        comma=","
    done
    frontends_json+="]"

    cat <<EOF
{
  "confidence": $CONFIDENCE,
  "recommended_backend": "$RECOMMENDED_BACKEND",
  "active_frontend": "$([[ ${#ACTIVE_FRONTENDS[@]} -gt 0 ]] && echo "${ACTIVE_FRONTENDS[0]}" || echo "none")",
  "active_frontends": $frontends_json,
  "backend": "$BACKEND_RAW",
  "ssh_port": $SSH_PORT,
  "ssh_source": "$SSH_SOURCE",
  "containerized": $CONTAINERIZED,
  "docker_host": $DOCKER_HOST,
  "k8s_node": $K8S_NODE,
  "cni_plugin": "$CNI_PLUGIN",
  "cloud_provider": "$CLOUD_PROVIDER",
  "iac_owner": "$OWNERSHIP",
  "fail2ban_active": $FAIL2BAN_ACTIVE,
  "risk_tier": "$RISK_TIER",
  "at_available": $AT_AVAILABLE,
  "systemd_run_available": $SYSTEMD_RUN_AVAILABLE,
  "halt_reasons": $halt_json
}
EOF
}

output_text() {
    echo "=== Firewall Tool Inventory ==="
    local tools
    tools=$(detect_firewall_tools)
    echo "$tools"

    echo ""
    echo "=== Containerization Check ==="
    $CONTAINERIZED && echo "INSIDE container" || echo "Not inside container"

    echo ""
    echo "=== Docker Host Check ==="
    $DOCKER_HOST && echo "Docker host detected" || echo "No Docker"

    echo ""
    echo "=== SSH Port(s) ==="
    echo "SSH port: $SSH_PORT (source: $SSH_SOURCE)"

    echo ""
    echo "=== Exposure Analysis ==="
    ss -tulpn 2>/dev/null | grep LISTEN || echo "No listening sockets"

    echo ""
    echo "=== Active Firewall Framework ==="
    if [[ ${#ACTIVE_FRONTENDS[@]} -gt 0 ]]; then
        echo "Frontends: ${ACTIVE_FRONTENDS[*]}"
    else
        echo "No frontend active"
    fi
    echo "Raw backend: $BACKEND_RAW"

    echo ""
    echo "=== Cloud Provider ==="
    echo "$CLOUD_PROVIDER"

    echo ""
    echo "=== Kubernetes Detection ==="
    if $K8S_NODE; then
        echo "WARNING: Kubernetes node detected (CNI: $CNI_PLUGIN)"
    else
        echo "No Kubernetes detected"
    fi

    echo ""
    echo "=== Ownership Boundary Detection ==="
    echo "Owner: $OWNERSHIP"

    echo ""
    echo "=== fail2ban ==="
    $FAIL2BAN_ACTIVE && echo "fail2ban installed" || echo "fail2ban not installed"

    echo ""
    echo "=== Rollback Capability ==="
    echo "at available: $AT_AVAILABLE"
    echo "systemd-run available: $SYSTEMD_RUN_AVAILABLE"

    echo ""
    echo "=== Confidence Assessment ==="
    for w in "${WARNINGS[@]}"; do
        echo "  WARNING: $w"
    done
    echo "Confidence score: $CONFIDENCE%"
    echo "Risk tier: $RISK_TIER"

    if [[ ${#HALT_REASONS[@]} -gt 0 ]]; then
        echo "HALT REASONS:"
        for r in "${HALT_REASONS[@]}"; do
            echo "  - $r"
        done
    fi

    if [[ $CONFIDENCE -lt 70 ]]; then
        echo "RESULT: HALT — confidence below 70%"
    else
        echo "RESULT: PROCEED"
    fi

    echo ""
    echo "=== Summary Recommendation ==="
    echo "Recommended path: $RECOMMENDED_BACKEND"
}

# ---- Main ----

# Wrap detection in error trap to catch internal errors
trap 'exit 11' ERR

detect_containerization
detect_cloud_provider
detect_ssh
detect_docker
detect_k8s
detect_active_frontends
detect_backend
detect_ownership
detect_fail2ban
detect_rollback_capability
assess_recommendation
assess_risk_tier

if [[ "$OUTPUT_MODE" == "json" ]]; then
    output_json
else
    output_text
fi

trap - ERR

# --- Exit code selection (must match SKILL.md § Exit Codes) ---
# 0  = SUCCESS — proceed
# 10 = RESERVED (backend conflict — nftables+iptables dual backend)
# 11 = Backend detection failed (no firewall tools / no backend detected)
# 12 = Multiple backends active (conflicting frontends)
# 20 = IaC managed (terraform/ansible/puppet/chef/cloud-init)
# 21 = Inside container (do not modify host firewall)
# 22 = K8s node detected (use NetworkPolicies instead)
# 30 = Low confidence (<70%) — drop to audit-only mode
# 31 = No rollback capability (install at or ensure systemd-run)

# Order matters: most specific / highest-priority conditions first.
# Each exit code maps to exactly one meaning per SKILL.md contract.
if [[ "$CONTAINERIZED" == "true" ]]; then
    exit 21
elif [[ "$K8S_NODE" == "true" ]]; then
    exit 22
elif [[ "$OWNERSHIP" != "manual" ]]; then
    exit 20
elif [[ ${#ACTIVE_FRONTENDS[@]} -gt 1 ]]; then
    exit 12
elif [[ "$RECOMMENDED_BACKEND" == "install" ]] || [[ "$BACKEND_RAW" == "none" ]]; then
    exit 11
elif ! $AT_AVAILABLE && ! $SYSTEMD_RUN_AVAILABLE; then
    exit 31
elif [[ "$RISK_TIER" == "manual" ]] || [[ "$RISK_TIER" == "halt" ]] || [[ $CONFIDENCE -lt 70 ]]; then
    exit 30
else
    exit 0
fi