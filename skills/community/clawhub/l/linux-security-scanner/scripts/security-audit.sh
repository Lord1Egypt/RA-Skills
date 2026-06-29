#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Linux Security Scanner — security-audit.sh
# Audits: SSH config, open ports, firewall rules, failed logins,
#         sudoers, world-writable files, SUID binaries
# ============================================================

SCRIPT_NAME="$(basename "$0")"
REPORT=""

# ─── Help ───────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Options:
  --all              Run all checks (default if no option given)
  --ssh              Check SSH configuration
  --ports            Scan open/listening ports
  --firewall         Check firewall rules (iptables/nftables/ufw)
  --failed-logins    Show failed login attempts
  --sudoers          Audit sudoers files
  --world-writable   Find world-writable files (limited scope)
  --suid             Find SUID binaries
  --help             Show this help

If no specific check is given, runs --all.
EOF
    exit 0
}

# ─── Helper: formatted output ──────────────────────────────
pass()  { echo -e "  [\e[32mPASS\e[0m] $1"; }
warn()  { echo -e "  [\e[33mWARN\e[0m] $1"; }
fail()  { echo -e "  [\e[31mFAIL\e[0m] $1"; }
info()  { echo -e "  [\e[34mINFO\e[0m] $1"; }

section() {
    echo ""
    echo "══════════════════════════════════════════════════════════"
    echo "  $1"
    echo "══════════════════════════════════════════════════════════"
}

gather_section() {
    local title="$1"
    shift
    REPORT+="$title"$'\n'
    REPORT+="$(printf '%*s' "${#title}" | tr ' ' '═')"$'\n'
    local out
    out="$("$@" 2>&1)" || true
    REPORT+="$out"$'\n\n'
}

# ─── Checks ─────────────────────────────────────────────────

check_ssh() {
    section "SSH Configuration"

    local sshd_config=""
    for f in /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf; do
        [ -f "$f" ] && sshd_config+="$(cat "$f")"$'\n'
    done

    local permit_root="$(echo "$sshd_config" | grep -iE '^\s*PermitRootLogin\s' | awk '{print $2}')"
    if [[ "$permit_root" == "yes" || "$permit_root" == "prohibit-password" || "$permit_root" == "without-password" ]]; then
        warn "PermitRootLogin is set to '$permit_root' (consider 'no')"
    elif [[ "$permit_root" == "no" ]]; then
        pass "PermitRootLogin is 'no'"
    else
        info "PermitRootLogin not explicitly set (default may allow root)"
    fi

    local password_auth="$(echo "$sshd_config" | grep -iE '^\s*PasswordAuthentication\s' | awk '{print $2}')"
    if [[ "$password_auth" == "yes" || -z "$password_auth" ]]; then
        warn "PasswordAuthentication is enabled or not set (consider key-only auth)"
    elif [[ "$password_auth" == "no" ]]; then
        pass "PasswordAuthentication is disabled"
    fi

    local port="$(echo "$sshd_config" | grep -iE '^\s*Port\s' | awk '{print $2}')"
    if [[ -n "$port" ]]; then
        info "SSH is listening on port $port"
    else
        info "SSH is on default port 22"
    fi

    local protocol="$(echo "$sshd_config" | grep -iE '^\s*Protocol\s' | awk '{print $2}')"
    if [[ -n "$protocol" && "$protocol" != "2" ]]; then
        fail "Protocol is '$protocol' (should be 2)"
    fi

    gather_section "SSH Configuration Summary" bash -c "echo 'PermitRootLogin: ${permit_root:-not set}'; echo 'PasswordAuthentication: ${password_auth:-not set}'; echo 'Port: ${port:-22}'"
}

check_ports() {
    section "Open / Listening Ports"

    if command -v ss &>/dev/null; then
        echo "Listening ports (ss -tlnp):"
        ss -tlnp 2>/dev/null || ss -tln 2>/dev/null
    elif command -v netstat &>/dev/null; then
        echo "Listening ports (netstat):"
        netstat -tlnp 2>/dev/null || netstat -tln 2>/dev/null
    else
        warn "Neither ss nor netstat found — install iproute2 or net-tools"
    fi

    gather_section "Open Ports" bash -c "(command -v ss && ss -tlnp) || (command -v netstat && netstat -tln) || echo 'unavailable'"
}

check_firewall() {
    section "Firewall Rules"

    if command -v ufw &>/dev/null; then
        echo "--- ufw status ---"
        ufw status verbose 2>/dev/null || echo "(ufw installed but not accessible)"
    fi

    if command -v iptables &>/dev/null; then
        echo "--- iptables filter rules ---"
        iptables -L -n --line-numbers 2>/dev/null || echo "(iptables not allowed)"
    fi

    if command -v nft &>/dev/null; then
        echo "--- nftables rules ---"
        nft list ruleset 2>/dev/null || echo "(nftables not allowed)"
    fi

    if ! command -v ufw &>/dev/null && ! command -v iptables &>/dev/null && ! command -v nft &>/dev/null; then
        warn "No firewall tool (ufw/iptables/nftables) detected"
    fi

    gather_section "Firewall" bash -c "echo 'ufw:'; command -v ufw && ufw status 2>/dev/null || echo 'n/a'; echo 'iptables:'; command -v iptables && iptables -L -n --line-numbers 2>/dev/null || echo 'n/a'; echo 'nftables:'; command -v nft && nft list ruleset 2>/dev/null || echo 'n/a'"
}

check_failed_logins() {
    section "Failed Login Attempts"

    if [ -f /var/log/btmp ]; then
        echo "Last 10 failed login attempts (lastb):"
        lastb -10 2>/dev/null || lastb 2>/dev/null | head -10 || echo "(cannot read /var/log/btmp)"
    else
        info "/var/log/btmp not found (no failed login tracking)"
    fi

    # Also check journald for SSH failures
    if command -v journalctl &>/dev/null; then
        echo ""
        echo "SSH authentication failures (last 24h):"
        journalctl -u sshd --since "24 hours ago" -g "Failed password" --no-pager 2>/dev/null | tail -10 || echo "(no journald or no entries)"
    fi

    gather_section "Failed Logins" bash -c "echo '=== lastb ==='; lastb 2>/dev/null | head -5 || echo 'n/a'; echo '=== journalctl sshd failures ==='; journalctl -u sshd -g 'Failed password' --since '24 hours ago' --no-pager 2>/dev/null | tail -5 || echo 'n/a'"
}

check_sudoers() {
    section "Sudoers Audit"

    local sudo_files=$(find /etc/sudoers /etc/sudoers.d -type f 2>/dev/null | sort)

    if [[ -z "$sudo_files" ]]; then
        info "No sudoers files found"
        return
    fi

    # Check sudoers file permissions
    local sudoers_perm=""
    if [ -f /etc/sudoers ]; then
        sudoers_perm=$(stat -c "%a" /etc/sudoers 2>/dev/null)
        if [[ "$sudoers_perm" != "440" ]]; then
            fail "/etc/sudoers permissions are $sudoers_perm (should be 440)"
        else
            pass "/etc/sudoers permissions are 440"
        fi
    fi

    echo ""
    echo "--- sudoers files ---"
    for f in $sudo_files; do
        echo "  $f"
    done

    echo ""
    echo "--- NOPASSWD entries ---"
    for f in $sudo_files; do
        if grep -H 'NOPASSWD' "$f" 2>/dev/null; then :; fi
    done

    echo ""
    echo "--- Users/groups with full sudo access ---"
    for f in $sudo_files; do
        grep -H 'ALL=(ALL:ALL)\s*ALL' "$f" 2>/dev/null || true
        grep -H 'ALL=(ALL)\s*ALL' "$f" 2>/dev/null || true
    done

    gather_section "Sudoers Audit" bash -c "echo 'Files:'; find /etc/sudoers /etc/sudoers.d -type f 2>/dev/null; echo '---'; echo 'NOPASSWD:'; grep -r 'NOPASSWD' /etc/sudoers /etc/sudoers.d 2>/dev/null || echo 'none'; echo 'Full sudo:'; grep -r 'ALL=(ALL:ALL) ALL' /etc/sudoers /etc/sudoers.d 2>/dev/null || echo 'none'"
}

check_world_writable() {
    section "World-Writable Files"

    local dirs=("/etc" "/tmp" "/var" "/home" "/opt")
    local found=0

    echo "Scanning (limited to: ${dirs[*]} — may take a moment)..."
    echo ""

    for d in "${dirs[@]}"; do
        if [ -d "$d" ]; then
            local results=$(find "$d" -maxdepth 3 -type f -perm -0002 ! -type l 2>/dev/null | head -30)
            if [[ -n "$results" ]]; then
                echo "--- $d ---"
                echo "$results"
                echo ""
                found=1
            fi
        fi
    done

    if [[ $found -eq 0 ]]; then
        pass "No world-writable files found in scanned directories"
    else
        warn "World-writable files found — review the list above"
    fi

    gather_section "World-Writable Files" bash -c "for d in /etc /tmp /var /home /opt; do [ -d \"\$d\" ] && find \"\$d\" -maxdepth 3 -type f -perm -0002 2>/dev/null; done | head -50"
}

check_suid() {
    section "SUID Binaries"

    echo "Finding SUID bit set on binaries..."
    local suid_list=$(find / -perm -4000 -type f 2>/dev/null | sort)

    if [[ -z "$suid_list" ]]; then
        info "No SUID binaries found"
        return
    fi

    echo "$suid_list"
    echo ""

    local known_risky=("pkexec" "passwd" "sudo" "su" "mount" "umount" "chsh" "chfn" "newgrp" "gpasswd")
    local risky_found=()

    for bin in $suid_list; do
        local name=$(basename "$bin")
        for risky in "${known_risky[@]}"; do
            if [[ "$name" == "$risky" ]]; then
                risky_found+=("$bin")
                break
            fi
        done
    done

    if [[ ${#risky_found[@]} -gt 0 ]]; then
        warn "Found common SUID binaries that may have CVEs:"
        for r in "${risky_found[@]}"; do
            echo "  $r"
        done
    fi

    # Check for unexpected SUID files outside standard paths
    local unusual=()
    for bin in $suid_list; do
        case "$bin" in
            /usr/bin/*|/bin/*|/usr/sbin/*|/sbin/*) ;;
            *) unusual+=("$bin") ;;
        esac
    done

    if [[ ${#unusual[@]} -gt 0 ]]; then
        warn "Unusual SUID binaries outside standard paths:"
        for u in "${unusual[@]}"; do
            echo "  $u"
        done
    fi

    gather_section "SUID Binaries" echo "$suid_list"
}

# ─── Full Audit ─────────────────────────────────────────────
run_all() {
    echo ""
    echo "  █████╗ ██╗   ██╗██████╗ ██╗████████╗"
    echo "  ██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝"
    echo "  ███████║██║   ██║██████╔╝██║   ██║   "
    echo "  ██╔══██║██║   ██║██╔══██╗██║   ██║   "
    echo "  ██║  ██║╚██████╔╝██║  ██║██║   ██║   "
    echo "  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   "
    echo "  Linux Security Scanner — Full Audit"
    echo ""

    REPORT="# Linux Security Audit Report"
    REPORT+=$'\n'
    REPORT+="Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"$'\n'
    REPORT+="Host: $(hostname)"$'\n'
    REPORT+=$'\n'

    check_ssh
    check_ports
    check_firewall
    check_failed_logins
    check_sudoers
    check_world_writable
    check_suid

    local score=0
    local max=7
    # Rough scoring
    [[ "$(echo "$sshd_config" | grep -iE '^\s*PermitRootLogin\s' | awk '{print $2}')" == "no" ]] && ((score+=1))
    [[ "$(echo "$sshd_config" | grep -iE '^\s*PasswordAuthentication\s' | awk '{print $2}')" == "no" ]] && ((score+=1))
    command -v ufw &>/dev/null && ((score+=1))
    command -v iptables &>/dev/null && command -v nft &>/dev/null && ((score+=1))

    echo ""
    echo "══════════════════════════════════════════════════════════"
    echo "  Audit Complete"
    echo "══════════════════════════════════════════════════════════"
    echo ""
    echo "Raw audit data stored in \$REPORT variable of this session"
    echo "Copy relevant sections or run individual checks as needed."
}

# ─── Main ───────────────────────────────────────────────────

# No args → run all
if [[ $# -eq 0 ]]; then
    run_all
    exit 0
fi

case "$1" in
    --all)          run_all ;;
    --ssh)          check_ssh ;;
    --ports)        check_ports ;;
    --firewall)     check_firewall ;;
    --failed-logins) check_failed_logins ;;
    --sudoers)      check_sudoers ;;
    --world-writable) check_world_writable ;;
    --suid)         check_suid ;;
    --help)         usage ;;
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac
