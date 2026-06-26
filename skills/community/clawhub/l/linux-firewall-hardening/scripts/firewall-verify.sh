#!/bin/bash
# firewall-verify.sh — Post-hardening verification checklist
# Run this after any firewall hardening operation to confirm success criteria.
# Exit code 0 = all critical checks passed. Exit code 60 = one or more failures
# (matches SKILL.md exit codes contract for verify failure → auto-rollback).

set -euo pipefail

ERRORS=0

echo "=== 1. SSH Reachable ==="
SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk -F: '{print $NF}' | head -1)
SSH_PORT=${SSH_PORT:-22}
if nc -z -w5 localhost "$SSH_PORT" 2>/dev/null; then
    echo "PASS: SSH port $SSH_PORT reachable locally"
else
    echo "FAIL: SSH port $SSH_PORT not reachable"
    ERRORS=$((ERRORS+1))
fi

echo ""
echo "=== 2. Listening Ports ==="
ss -tlnp | grep LISTEN | awk '{print $4}' | while read line; do
    echo "  Listening: $line"
done

echo ""
echo "=== 3. IPv4 Firewall Active ==="
if sudo iptables -L -n 2>/dev/null | grep -qv "Chain\|policy"; then
    echo "PASS: iptables rules present"
elif sudo nft list ruleset 2>/dev/null | grep -q "table"; then
    echo "PASS: nftables rules present"
elif sudo ufw status 2>/dev/null | grep -q "Status: active"; then
    echo "PASS: ufw active"
else
    echo "FAIL: No active IPv4 firewall detected"
    ERRORS=$((ERRORS+1))
fi

echo ""
echo "=== 4. IPv6 Symmetry ==="
if sudo ip6tables -L -n 2>/dev/null | grep -qv "Chain\|policy"; then
    echo "PASS: ip6tables rules present"
elif sudo nft list ruleset 2>/dev/null | grep -q "inet filter"; then
    echo "PASS: nftables inet family covers IPv6"
else
    echo "WARN: No explicit IPv6 firewall detected"
fi

echo ""
echo "=== 5. Persistence ==="
for svc in ufw nftables firewalld; do
    if systemctl is-enabled "$svc" &>/dev/null; then
        echo "PASS: $svc is enabled for persistence"
    fi
done

echo ""
echo "=== 6. Docker Check ==="
if command -v docker &>/dev/null && docker ps &>/dev/null; then
    if sudo iptables -L DOCKER-USER -n 2>/dev/null | grep -q "DROP"; then
        echo "PASS: DOCKER-USER has DROP rule"
    else
        echo "WARN: DOCKER-USER chain missing DROP rule"
    fi
else
    echo "SKIP: Docker not running"
fi

echo ""
echo "=== 7. fail2ban (if installed) ==="
if command -v fail2ban-server &>/dev/null; then
    if sudo fail2ban-client status sshd &>/dev/null; then
        echo "PASS: fail2ban sshd jail active"
    else
        echo "WARN: fail2ban installed but sshd jail not active"
    fi
else
    echo "SKIP: fail2ban not installed"
fi

echo ""
echo "=== 8. Exposure Check ==="
echo "Public-bound (0.0.0.0) listening sockets:"
ss -tlnp | grep -E "0\.0\.0\.0|\[::\]" | awk '{print $4, $7}' | while read line; do
    echo "  $line"
done

echo ""
echo "=== Summary ==="
if [[ $ERRORS -eq 0 ]]; then
    echo "All critical checks passed."

    # --- Cancel rollback timer on successful verification ---
    ROLLBACK_CANCELLED=false
    if command -v at &>/dev/null; then
        # Cancel all pending at jobs (rollback timer uses at)
        # Store job IDs in an array first to avoid subshell scoping issue
        mapfile -t AT_JOBS < <(atq 2>/dev/null | awk '{print $1}')
        for job in "${AT_JOBS[@]}"; do
            [[ -z "$job" ]] && continue
            atrm "$job" 2>/dev/null && ROLLBACK_CANCELLED=true
        done
        echo "INFO: Pending 'at' jobs cancelled ($ROLLBACK_CANCELLED)"
    fi
    if command -v systemctl &>/dev/null; then
        # Cancel systemd transient timer units created by systemd-run (system scope)
        systemctl list-units --type=service --state=running 2>/dev/null | grep 'firewall-rollback' | awk '{print $1}' | while read unit; do
            sudo systemctl stop "$unit" 2>/dev/null && echo "INFO: Stopped $unit"
        done
        # Also check --user scope since systemd-run --user creates user units
        systemctl --user list-units --type=service --state=running 2>/dev/null | grep 'firewall-rollback' | awk '{print $1}' | while read unit; do
            systemctl --user stop "$unit" 2>/dev/null && echo "INFO: Stopped (user) $unit"
        done
    fi
    # Clear the state file if it exists
    if [[ -f .firewall-hardening/state.json ]]; then
        rm -f .firewall-hardening/state.json
        echo "INFO: State file cleared"
    fi

    exit 0
else
    echo "$ERRORS critical check(s) failed. Review output above."
    exit 60  # Match SKILL.md Exit Codes core contract: "60 | Verify failed | Auto-rollback triggered"
fi