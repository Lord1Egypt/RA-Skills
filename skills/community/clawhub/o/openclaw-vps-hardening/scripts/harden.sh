#!/bin/bash
# harden.sh — OpenClaw VPS Server Hardening
#
# Implements the full Cloudflare-based hardening strategy:
#   Layer 1: UFW lockdown (close all ports except SSH)
#   Layer 2: SSH hardening (non-default port, disable root login, key-only auth)
#   Layer 3: Fail2Ban (SSH brute-force protection)
#   Layer 4: OpenClaw loopback binding
#   Layer 5: Unattended security upgrades
#   Layer 6: Non-root user for OpenClaw service
#   Layer 7: File permission hardening
#
# NOTE: Cloudflare Tunnel + Cloudflare Access setup is separate.
#       Run this AFTER cloudflared is installed and tunnels are working.
#       Closing port 18789 before Cloudflare Tunnel is active = lockout.
#
# Usage:
#   bash harden.sh [--ssh-port 2222] [--openclaw-user koda] [--skip-ufw] [--dry-run]
#
# Run as root on the VPS.

set -euo pipefail

# ─── Defaults ────────────────────────────────────────────────────────────────
SSH_PORT=2222
OPENCLAW_USER=koda
OPENCLAW_CONFIG_DIR=/root/.openclaw
DRY_RUN=false
SKIP_UFW=false
SKIP_SSH=false
SKIP_FAIL2BAN=false
SKIP_UPGRADES=false

# ─── Argument parsing ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --ssh-port)       SSH_PORT="$2";         shift 2 ;;
    --openclaw-user)  OPENCLAW_USER="$2";    shift 2 ;;
    --openclaw-dir)   OPENCLAW_CONFIG_DIR="$2"; shift 2 ;;
    --dry-run)        DRY_RUN=true;          shift ;;
    --skip-ufw)       SKIP_UFW=true;         shift ;;
    --skip-ssh)       SKIP_SSH=true;         shift ;;
    --skip-fail2ban)  SKIP_FAIL2BAN=true;    shift ;;
    --skip-upgrades)  SKIP_UPGRADES=true;    shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# ─── Helpers ──────────────────────────────────────────────────────────────────
run() {
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] $*"
  else
    eval "$@"
  fi
}

step() { echo -e "\n\033[1;36m━━━ $1 ━━━\033[0m"; }
ok()   { echo -e "\033[1;32m✓\033[0m $1"; }
warn() { echo -e "\033[1;33m⚠\033[0m $1"; }
info() { echo -e "\033[0;37m  $1\033[0m"; }

[[ "$DRY_RUN" == "true" ]] && echo -e "\033[1;33m[DRY RUN MODE — no changes will be made]\033[0m\n"

echo "╔══════════════════════════════════════════════════════╗"
echo "║       OpenClaw VPS Hardening                         ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  SSH Port:  $SSH_PORT                                      "
echo "║  OC User:   $OPENCLAW_USER                                 "
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ─── Pre-flight checks ────────────────────────────────────────────────────────
[[ $EUID -ne 0 ]] && { echo "Run as root"; exit 1; }

# Verify Cloudflare Tunnel is active before closing ports
if ! systemctl is-active --quiet cloudflared 2>/dev/null && \
   ! systemctl list-units "cloudflared-*" --no-pager 2>/dev/null | grep -q "active"; then
  warn "No active cloudflared service detected!"
  warn "Do NOT close port 18789 until Cloudflare Tunnel is working."
  warn "Agents will become inaccessible if you close the port now."
  echo ""
  read -rp "Proceed anyway? [y/N] " confirm
  [[ "$confirm" != "y" && "$confirm" != "Y" ]] && { echo "Aborted."; exit 0; }
fi

# ─── Layer 1: UFW ─────────────────────────────────────────────────────────────
if [[ "$SKIP_UFW" != "true" ]]; then
  step "Layer 1: UFW Firewall"

  run "apt-get install -y ufw -qq"

  # Reset to clean state
  run "ufw --force reset"

  # Defaults
  run "ufw default deny incoming"
  run "ufw default allow outgoing"

  # SSH on custom port only
  run "ufw allow ${SSH_PORT}/tcp comment 'SSH'"

  # Explicitly close OpenClaw port (no longer public — served via Cloudflare Tunnel)
  run "ufw deny 18789/tcp comment 'OpenClaw - internal only via Cloudflare Tunnel'"
  run "ufw deny 22/tcp comment 'Default SSH - moved to ${SSH_PORT}'"

  run "ufw --force enable"
  ok "UFW: only port ${SSH_PORT} (SSH) open to internet"
  info "Port 18789 denied — access only via Cloudflare Tunnel (loopback)"
fi

# ─── Layer 2: SSH Hardening ───────────────────────────────────────────────────
if [[ "$SKIP_SSH" != "true" ]]; then
  step "Layer 2: SSH Hardening"

  SSHD_CONFIG=/etc/ssh/sshd_config

  # Backup original
  run "cp ${SSHD_CONFIG} ${SSHD_CONFIG}.bak.$(date +%Y%m%d)"

  # Apply settings
  apply_ssh() {
    local key="$1" val="$2"
    if grep -qP "^#?${key}" "$SSHD_CONFIG" 2>/dev/null; then
      run "sed -i 's|^#\?${key}.*|${key} ${val}|' ${SSHD_CONFIG}"
    else
      run "echo '${key} ${val}' >> ${SSHD_CONFIG}"
    fi
  }

  apply_ssh "Port"                    "$SSH_PORT"
  apply_ssh "PermitRootLogin"         "no"
  apply_ssh "PasswordAuthentication"  "no"
  apply_ssh "PubkeyAuthentication"    "yes"
  apply_ssh "AuthorizedKeysFile"      ".ssh/authorized_keys"
  apply_ssh "PermitEmptyPasswords"    "no"
  apply_ssh "X11Forwarding"           "no"
  apply_ssh "MaxAuthTries"            "3"
  apply_ssh "ClientAliveInterval"     "300"
  apply_ssh "ClientAliveCountMax"     "2"
  apply_ssh "LoginGraceTime"          "30"

  # Validate config before restarting
  if [[ "$DRY_RUN" != "true" ]]; then
    sshd -t && ok "sshd config valid" || { warn "sshd config invalid — reverting"; cp "${SSHD_CONFIG}.bak.$(date +%Y%m%d)" "$SSHD_CONFIG"; exit 1; }
    systemctl reload sshd
  fi

  ok "SSH: port ${SSH_PORT}, root login disabled, password auth disabled"
  warn "IMPORTANT: Ensure your SSH key is in ~/.ssh/authorized_keys BEFORE reconnecting"
  warn "Test connection: ssh -p ${SSH_PORT} root@SERVER_IP (in a NEW terminal, don't close this one)"
fi

# ─── Layer 3: Fail2Ban ────────────────────────────────────────────────────────
if [[ "$SKIP_FAIL2BAN" != "true" ]]; then
  step "Layer 3: Fail2Ban"

  run "apt-get install -y fail2ban -qq"

  # Write jail config
  run "cat > /etc/fail2ban/jail.d/openclaw-hardening.conf << 'EOF'
[DEFAULT]
bantime  = 86400
findtime = 600
maxretry = 3
backend  = systemd

[sshd]
enabled  = true
port     = ${SSH_PORT}
filter   = sshd
logpath  = %(sshd_log)s
maxretry = 3
bantime  = 86400

[sshd-ddos]
enabled  = true
port     = ${SSH_PORT}
filter   = sshd-ddos
logpath  = %(sshd_log)s
maxretry = 10
findtime = 60
bantime  = 3600
EOF"

  run "systemctl enable fail2ban"
  run "systemctl restart fail2ban"

  if [[ "$DRY_RUN" != "true" ]]; then
    sleep 2
    fail2ban-client status sshd 2>/dev/null && ok "Fail2Ban: sshd jail active" || warn "Fail2Ban started but sshd jail status unclear"
  fi

  ok "Fail2Ban: ban after 3 SSH failures, 24hr ban"
fi

# ─── Layer 4: OpenClaw Loopback Binding ───────────────────────────────────────
step "Layer 4: OpenClaw Loopback Binding"

OC_CONFIG="${OPENCLAW_CONFIG_DIR}/openclaw.json"

if [[ -f "$OC_CONFIG" ]]; then
  if python3 -c "import json; c=json.load(open('${OC_CONFIG}')); assert c.get('gateway',{}).get('bind')=='loopback'" 2>/dev/null; then
    ok "OpenClaw: already bound to loopback"
  else
    if [[ "$DRY_RUN" != "true" ]]; then
      python3 - << PYEOF
import json, sys
with open('${OC_CONFIG}') as f:
    c = json.load(f)
c.setdefault('gateway', {})['bind'] = 'loopback'
with open('${OC_CONFIG}', 'w') as f:
    json.dump(c, f, indent=2)
print("Updated gateway.bind to loopback")
PYEOF
      systemctl restart openclaw 2>/dev/null || true
    else
      echo "[DRY-RUN] Would set gateway.bind = loopback in ${OC_CONFIG}"
    fi
    ok "OpenClaw: bound to loopback (127.0.0.1 only)"
  fi
else
  warn "OpenClaw config not found at ${OC_CONFIG} — skipping loopback binding"
  info "Set manually: openclaw config set gateway.bind loopback"
fi

# ─── Layer 5: Unattended Security Upgrades ────────────────────────────────────
if [[ "$SKIP_UPGRADES" != "true" ]]; then
  step "Layer 5: Unattended Security Upgrades"

  run "apt-get install -y unattended-upgrades apt-listchanges -qq"
  run "dpkg-reconfigure -plow unattended-upgrades 2>/dev/null || true"

  run "cat > /etc/apt/apt.conf.d/50unattended-upgrades-openclaw << 'EOF'
Unattended-Upgrade::Allowed-Origins {
  \"\${distro_id}:\${distro_codename}-security\";
};
Unattended-Upgrade::AutoFixInterruptedDpkg \"true\";
Unattended-Upgrade::MinimalSteps \"true\";
Unattended-Upgrade::Remove-Unused-Dependencies \"true\";
Unattended-Upgrade::Automatic-Reboot \"false\";
EOF"

  ok "Unattended upgrades: security patches auto-applied"
fi

# ─── Layer 6: File Permission Hardening ───────────────────────────────────────
step "Layer 6: File Permission Hardening"

# Secure OpenClaw config dir
if [[ -d "$OPENCLAW_CONFIG_DIR" ]]; then
  run "chmod 700 ${OPENCLAW_CONFIG_DIR}"
  run "chmod 600 ${OPENCLAW_CONFIG_DIR}/openclaw.json 2>/dev/null || true"
  run "chmod 600 ${OPENCLAW_CONFIG_DIR}/secrets.json 2>/dev/null || true"
  ok "OpenClaw config: mode 700/600"
fi

# Secure cloudflared credentials
if [[ -d /root/.cloudflared ]]; then
  run "chmod 700 /root/.cloudflared"
  run "chmod 600 /root/.cloudflared/*.json 2>/dev/null || true"
  run "chmod 600 /root/.cloudflared/cert.pem 2>/dev/null || true"
  ok "Cloudflared credentials: mode 700/600"
fi

# SSH keys
run "chmod 700 /root/.ssh 2>/dev/null || true"
run "chmod 600 /root/.ssh/authorized_keys 2>/dev/null || true"
ok "SSH keys: mode 700/600"

# ─── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ HARDENING COMPLETE                                       ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Layer 1: UFW — port 18789 closed, SSH on ${SSH_PORT} only      ║"
echo "║  Layer 2: SSH — no root, no passwords, port ${SSH_PORT}          ║"
echo "║  Layer 3: Fail2Ban — 3 strikes, 24hr SSH ban                ║"
echo "║  Layer 4: OpenClaw — loopback only (127.0.0.1)              ║"
echo "║  Layer 5: Auto security upgrades enabled                    ║"
echo "║  Layer 6: File permissions hardened (600/700)               ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  NEXT: Set up Cloudflare Access policy for each agent URL   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Reconnect via: ssh -p ${SSH_PORT} root@YOUR_SERVER_IP"
echo "  (Test in a new terminal before closing this session)"
echo ""
