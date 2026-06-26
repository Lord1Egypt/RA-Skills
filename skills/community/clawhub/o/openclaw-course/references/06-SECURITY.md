# Module 6: Security & DevOps

## Securing Your AI Employee

Your OpenClaw agent has access to your files, systems, and potentially sensitive data. Security isn't optional—it's essential. This module provides copy-paste ready scripts for securing your OpenClaw deployment.

---

## Table of Contents

1. [Complete SSH Hardening](#complete-ssh-hardening)
2. [UFW Firewall Configuration](#ufw-firewall-configuration)
3. [fail2ban Setup](#fail2ban-setup)
4. [API Key Management](#api-key-management)
5. [Security Audit Checklist](#security-audit-checklist)
6. [Safe Skill Installation](#safe-skill-installation)
7. [Incident Response](#incident-response)

---

## Complete SSH Hardening

### Ready-to-Use SSH Hardening Script

```bash
#!/bin/bash
# ssh-hardening.sh - Run as root or with sudo
# Copy-paste ready SSH hardening for OpenClaw VPS

set -e

echo "=== SSH Security Hardening ==="

# Backup original config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)

# Create new hardened config
cat > /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
# === OpenClaw SSH Hardening ===

# Authentication
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
MaxAuthTries 3
MaxSessions 2
LoginGraceTime 30

# Connection settings
ClientAliveInterval 300
ClientAliveCountMax 2
TCPKeepAlive no

# Security
X11Forwarding no
AllowTcpForwarding no
PermitTunnel no
GatewayPorts no
AllowAgentForwarding no

# Cryptography
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256

# Logging
LogLevel VERBOSE
EOF

# Set proper permissions
chmod 600 /etc/ssh/sshd_config.d/hardening.conf

# Test configuration before applying
echo "Testing SSH configuration..."
if sshd -t; then
    echo "✅ SSH configuration valid"
else
    echo "❌ SSH configuration invalid! Reverting..."
    mv /etc/ssh/sshd_config.bak.$(date +%Y%m%d) /etc/ssh/sshd_config
    exit 1
fi

# Generate ED25519 host key if not exists (stronger than RSA)
if [ ! -f /etc/ssh/ssh_host_ed25519_key ]; then
    ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" -C "$(hostname)"
fi

# Disable weak host key algorithms
sed -i 's/^HostKey \/etc\/ssh\/ssh_host_dsa_key/#HostKey \/etc\/ssh\/ssh_host_dsa_key/' /etc/ssh/sshd_config
sed -i 's/^HostKey \/etc\/ssh\/ssh_host_ecdsa_key/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/' /etc/ssh/sshd_config

# Restart SSH service
echo "Restarting SSH service..."
if systemctl is-active --quiet sshd; then
    systemctl restart sshd
elif systemctl is-active --quiet ssh; then
    systemctl restart ssh
fi

echo "=== SSH Hardening Complete ==="
echo ""
echo "⚠️  IMPORTANT: Before logging out:"
echo "1. Open a NEW terminal/SSH session to verify access"
echo "2. Keep this session open until you confirm the new session works"
echo "3. If new session fails, run: mv /etc/ssh/sshd_config.bak.* /etc/ssh/sshd_config"
echo ""
echo "Current settings:"
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config.d/hardening.conf
```

### SSH Key Generation and Setup

```bash
# Generate strong SSH key (ED25519 recommended)
ssh-keygen -t ed25519 -C "openclaw-$(date +%Y%m%d)" -f ~/.ssh/id_ed25519_openclaw

# Or generate RSA with 4096 bits (for legacy compatibility)
ssh-keygen -t rsa -b 4096 -C "openclaw-$(date +%Y%m%d)" -f ~/.ssh/id_rsa_openclaw

# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519_openclaw.pub openclaw@your-server-ip

# Configure SSH client (~/.ssh/config)
cat >> ~/.ssh/config << 'EOF'

Host openclaw-vps
    HostName your-server-ip
    User openclaw
    Port 22
    IdentityFile ~/.ssh/id_ed25519_openclaw
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    StrictHostKeyChecking accept-new
EOF

chmod 600 ~/.ssh/config

# Now connect with: ssh openclaw-vps
```

### SSH Access Restriction (Allow Specific Users Only)

```bash
# Create SSH allowlist
cat >> /etc/ssh/sshd_config.d/allowlist.conf << 'EOF'
# Only allow specific users
AllowUsers openclaw

# Or allow specific groups
AllowGroups openclaw sudo

# Deny specific users
DenyUsers root admin test guest
EOF

# Restart SSH
systemctl restart sshd
```

---

## UFW Firewall Configuration

### Complete UFW Setup Script

```bash
#!/bin/bash
# ufw-setup.sh - Comprehensive UFW configuration
# Run as root or with sudo

set -e

echo "=== UFW Firewall Setup ==="

# Install UFW if not present
if ! command -v ufw > /dev/null; then
    apt-get update
    apt-get install -y ufw
fi

# Reset to defaults
ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (CRITICAL - keep this!)
ufw allow 22/tcp comment 'SSH'

# Allow HTTP/HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Allow OpenClaw Gateway (restrict to specific IPs if possible)
# ufw allow from YOUR_HOME_IP to any port 18789 comment 'OpenClaw Gateway'
# OR allow from anywhere (less secure):
ufw allow 18789/tcp comment 'OpenClaw Gateway'

# Rate limit SSH (prevent brute force)
ufw limit 22/tcp comment 'SSH rate limit'

# Optional: Allow specific services
# ufw allow 8080/tcp comment 'Custom web app'
# ufw allow 10000:20000/tcp comment 'Port range'

# Enable firewall
echo "Enabling firewall..."
ufw --force enable

# Show status
echo ""
echo "=== UFW Status ==="
ufw status verbose

echo ""
echo "=== Firewall Rules ==="
ufw status numbered

echo ""
echo "=== Setup Complete ==="
echo "To add more rules: ufw allow [port]/[protocol]"
echo "To delete a rule: ufw delete [number]"
echo "To disable: ufw disable"
```

### Advanced UFW Rules

```bash
# Allow from specific IP only
ufw allow from 192.168.1.100 to any port 22 comment 'Home office'

# Allow from subnet
ufw allow from 192.168.1.0/24 to any port 18789 comment 'Office network'

# Allow from Tailscale network
ufw allow from 100.64.0.0/10 comment 'Tailscale'

# Block specific IP
ufw deny from 10.0.0.100 comment 'Blocked attacker'

# Application profiles
ufw app list
ufw allow 'Nginx Full'
ufw allow 'OpenSSH'

# IPv6 support (edit /etc/default/ufw)
sed -i 's/IPV6=no/IPV6=yes/' /etc/default/ufw
```

---

## fail2ban Setup

### Complete fail2ban Installation and Configuration

```bash
#!/bin/bash
# fail2ban-setup.sh - Complete fail2ban setup for OpenClaw
# Run as root or with sudo

set -e

echo "=== fail2ban Setup ==="

# Install fail2ban
apt-get update
apt-get install -y fail2ban

# Create custom jail configuration
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# Ban settings
bantime = 1h
findtime = 10m
maxretry = 3
backend = auto

# Notification (optional - requires mail setup)
# destemail = admin@example.com
# sender = fail2ban@example.com
# mta = sendmail
# action = %(action_mwl)s

# SSH protection
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 1h

# OpenClaw-specific: Protect gateway auth
[openclaw-gateway]
enabled = true
port = 18789
filter = openclaw-gateway
logpath = /home/openclaw/.openclaw/logs/auth.log
maxretry = 5
bantime = 2h
findtime = 15m

# Nginx protection
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

# Nginx limit req (DDoS protection)
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log

# Additional protections
[recidive]
enabled = true
filter = recidive
logpath = /var/log/fail2ban.log
action = %(action_mwl)s
bantime = 1w
findtime = 1d
EOF

# Create OpenClaw filter
cat > /etc/fail2ban/filter.d/openclaw-gateway.conf << 'EOF'
[Definition]
failregex = ^.*Failed authentication attempt from <HOST>.*$
            ^.*Invalid credentials from <HOST>.*$
            ^.*Rate limit exceeded for <HOST>.*$
ignoreregex = ^.*Successful authentication from <HOST>.*$
EOF

# Set proper permissions
chmod 644 /etc/fail2ban/jail.local
chmod 644 /etc/fail2ban/filter.d/openclaw-gateway.conf

# Create log directory if needed
mkdir -p /home/openclaw/.openclaw/logs
chown -R openclaw:openclaw /home/openclaw/.openclaw

# Restart fail2ban
systemctl enable fail2ban
systemctl restart fail2ban

# Wait for service to start
sleep 2

echo ""
echo "=== fail2ban Status ==="
fail2ban-client status

echo ""
echo "=== SSH Jail Status ==="
fail2ban-client status sshd

echo ""
echo "=== Setup Complete ==="
echo "Monitor: fail2ban-client status"
echo "View banned IPs: fail2ban-client status sshd"
echo "Unban IP: fail2ban-client set sshd unbanip IP_ADDRESS"
```

### fail2ban Management Commands

```bash
# Check status
sudo fail2ban-client status

# Check specific jail
sudo fail2ban-client status sshd

# List banned IPs
sudo fail2ban-client status sshd | grep "Banned IP list"

# Unban an IP
sudo fail2ban-client set sshd unbanip 192.168.1.100

# View fail2ban logs
sudo tail -f /var/log/fail2ban.log

# Test a filter against log
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

---

## API Key Management

### Secure Environment Variable Setup

```bash
#!/bin/bash
# setup-api-keys.sh - Secure API key management
# Run as openclaw user

set -e

echo "=== API Key Setup ==="

mkdir -p ~/.openclaw

# Create secure .env file
cat > ~/.openclaw/.env << 'EOF'
# OpenClaw API Keys
# Generated: $(date)

# Anthropic (Claude)
ANTHROPIC_API_KEY=

# OpenAI (GPT)
OPENAI_API_KEY=

# OpenRouter (multi-provider)
OPENROUTER_API_KEY=

# Google (Gemini)
GOOGLE_API_KEY=

# GitHub (for gh-issues skill)
GH_TOKEN=

# Gateway security
GATEWAY_PASSWORD=$(openssl rand -base64 32)

# Other services
BRAVE_API_KEY=
FIRECRAWL_API_KEY=
EOF

# Set restrictive permissions
chmod 600 ~/.openclaw/.env

# Create systemd service override for environment
echo ""
echo "Add to /etc/systemd/system/openclaw.service:"
echo "EnvironmentFile=/home/openclaw/.openclaw/.env"
echo ""
echo "Then run: sudo systemctl daemon-reload && sudo systemctl restart openclaw"

echo ""
echo "=== Instructions ==="
echo "1. Edit ~/.openclaw/.env and add your API keys"
echo "2. Never commit this file to git"
echo "3. Add .env to .gitignore"
echo "4. Use 'source ~/.openclaw/.env' to load in shell"
```

### API Key Rotation Script

```bash
#!/bin/bash
# rotate-api-keys.sh - Rotate API keys securely

set -e

ENV_FILE="$HOME/.openclaw/.env"
BACKUP_DIR="$HOME/.openclaw/backups"

# Create backup
echo "Creating backup..."
mkdir -p "$BACKUP_DIR"
cp "$ENV_FILE" "$BACKUP_DIR/.env.bak.$(date +%Y%m%d_%H%M%S)"

# Function to update key
update_key() {
    local key_name=$1
    local new_value=$2
    
    if grep -q "^${key_name}=" "$ENV_FILE"; then
        sed -i "s/^${key_name}=.*/${key_name}=${new_value}/" "$ENV_FILE"
        echo "✅ Updated $key_name"
    else
        echo "$key_name=$new_value" >> "$ENV_FILE"
        echo "✅ Added $key_name"
    fi
}

echo "=== API Key Rotation ==="
echo "Enter new API keys (press Enter to skip):"

read -s -p "New ANTHROPIC_API_KEY: " anthropic_key
echo
if [ -n "$anthropic_key" ]; then
    update_key "ANTHROPIC_API_KEY" "$anthropic_key"
fi

read -s -p "New OPENAI_API_KEY: " openai_key
echo
if [ -n "$openai_key" ]; then
    update_key "OPENAI_API_KEY" "$openai_key"
fi

read -s -p "New OPENROUTER_API_KEY: " openrouter_key
echo
if [ -n "$openrouter_key" ]; then
    update_key "OPENROUTER_API_KEY" "$openrouter_key"
fi

read -s -p "New GATEWAY_PASSWORD: " gateway_pass
echo
if [ -n "$gateway_pass" ]; then
    update_key "GATEWAY_PASSWORD" "$gateway_pass"
fi

# Secure permissions
chmod 600 "$ENV_FILE"

echo ""
echo "=== Rotation Complete ==="
echo "Restart OpenClaw to apply changes:"
echo "sudo systemctl restart openclaw"
```

### OpenClaw Configuration with Environment Variables

```json5
// ~/.openclaw/openclaw.json
{
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": { "source": "env", "id": "ANTHROPIC_API_KEY" }
      },
      "openai": {
        "apiKey": { "source": "env", "id": "OPENAI_API_KEY" }
      },
      "openrouter": {
        "apiKey": { "source": "env", "id": "OPENROUTER_API_KEY" }
      }
    }
  },
  "gateway": {
    "auth": {
      "mode": "password",
      "password": { "source": "env", "id": "GATEWAY_PASSWORD" }
    }
  },
  "skills": {
    "entries": {
      "gh-issues": {
        "apiKey": { "source": "env", "id": "GH_TOKEN" }
      }
    }
  }
}
```

---

## Security Audit Checklist

### Copy-Paste Security Audit Script

```bash
#!/bin/bash
# security-audit.sh - Comprehensive security audit
# Run as root or with sudo for full checks

set -e

REPORT_FILE="/tmp/security-audit-$(date +%Y%m%d_%H%M%S).txt"

echo "========================================" | tee -a "$REPORT_FILE"
echo "OpenClaw Security Audit Report" | tee -a "$REPORT_FILE"
echo "Generated: $(date)" | tee -a "$REPORT_FILE"
echo "Hostname: $(hostname)" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1" | tee -a "$REPORT_FILE"
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1" | tee -a "$REPORT_FILE"
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1" | tee -a "$REPORT_FILE"
}

echo "=== 1. SSH Configuration ===" | tee -a "$REPORT_FILE"

# Check root login
if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null; then
    check_pass "Root login disabled"
else
    check_fail "Root login not disabled"
fi

# Check password auth
if grep -q "^PasswordAuthentication no" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null; then
    check_pass "Password authentication disabled"
else
    check_fail "Password authentication enabled"
fi

# Check pubkey auth
if grep -q "^PubkeyAuthentication yes" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null; then
    check_pass "Public key authentication enabled"
else
    check_warn "Public key authentication not confirmed"
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 2. Firewall Status ===" | tee -a "$REPORT_FILE"

if command -v ufw > /dev/null; then
    if ufw status | grep -q "Status: active"; then
        check_pass "UFW is active"
        echo "Active rules:" | tee -a "$REPORT_FILE"
        ufw status numbered | tee -a "$REPORT_FILE"
    else
        check_fail "UFW is not active"
    fi
else
    check_warn "UFW not installed"
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 3. fail2ban Status ===" | tee -a "$REPORT_FILE"

if command -v fail2ban-client > /dev/null; then
    if systemctl is-active --quiet fail2ban; then
        check_pass "fail2ban is running"
        echo "Jail status:" | tee -a "$REPORT_FILE"
        fail2ban-client status | tee -a "$REPORT_FILE"
    else
        check_fail "fail2ban is not running"
    fi
else
    check_warn "fail2ban not installed"
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 4. File Permissions ===" | tee -a "$REPORT_FILE"

# Check OpenClaw config permissions
if [ -f /home/openclaw/.openclaw/.env ]; then
    PERMS=$(stat -c "%a" /home/openclaw/.openclaw/.env)
    if [ "$PERMS" = "600" ]; then
        check_pass "API key file has correct permissions (600)"
    else
        check_fail "API key file permissions are $PERMS (should be 600)"
    fi
else
    check_warn "API key file not found"
fi

# Check SSH directory permissions
if [ -d /home/openclaw/.ssh ]; then
    PERMS=$(stat -c "%a" /home/openclaw/.ssh)
    if [ "$PERMS" = "700" ]; then
        check_pass ".ssh directory has correct permissions (700)"
    else
        check_fail ".ssh directory permissions are $PERMS (should be 700)"
    fi
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 5. Open Ports ===" | tee -a "$REPORT_FILE"

echo "Listening ports:" | tee -a "$REPORT_FILE"
ss -tlnp | grep LISTEN | tee -a "$REPORT_FILE"

echo "" | tee -a "$REPORT_FILE"
echo "=== 6. Recent Login Activity ===" | tee -a "$REPORT_FILE"

echo "Successful logins:" | tee -a "$REPORT_FILE"
last -10 | tee -a "$REPORT_FILE"

echo "" | tee -a "$REPORT_FILE"
echo "Failed SSH attempts (last 24h):" | tee -a "$REPORT_FILE"
grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l | tee -a "$REPORT_FILE"

echo "" | tee -a "$REPORT_FILE"
echo "=== 7. System Updates ===" | tee -a "$REPORT_FILE"

if command -v apt > /dev/null; then
    UPDATES=$(apt list --upgradable 2>/dev/null | wc -l)
    if [ "$UPDATES" -gt 1 ]; then
        check_warn "$UPDATES packages can be upgraded"
        apt list --upgradable 2>/dev/null | head -10 | tee -a "$REPORT_FILE"
    else
        check_pass "System is up to date"
    fi
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 8. OpenClaw Security ===" | tee -a "$REPORT_FILE"

# Check if OpenClaw is running
if systemctl is-active --quiet openclaw; then
    check_pass "OpenClaw service is running"
else
    check_warn "OpenClaw service is not running"
fi

# Check gateway binding
if ss -tlnp | grep -q ":18789"; then
    echo "OpenClaw Gateway is listening on port 18789" | tee -a "$REPORT_FILE"
    check_warn "Ensure port 18789 is properly firewalled"
fi

echo "" | tee -a "$REPORT_FILE"
echo "=== 9. Disk Encryption ===" | tee -a "$REPORT_FILE"

if command -v cryptsetup > /dev/null; then
    if cryptsetup status &> /dev/null; then
        check_pass "Disk encryption detected"
    else
        check_warn "No disk encryption detected"
    fi
else
    check_warn "Cannot check disk encryption status"
fi

echo "" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"
echo "Audit Complete" | tee -a "$REPORT_FILE"
echo "Report saved to: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"
```

### Quick Security Check (Daily)

```bash
#!/bin/bash
# daily-security-check.sh - Quick daily security check

echo "=== $(date) ==="
echo "Failed SSH attempts (last 24h): $(grep 'Failed password' /var/log/auth.log 2>/dev/null | wc -l)"
echo "Banned IPs (fail2ban): $(sudo fail2ban-client status sshd 2>/dev/null | grep 'Banned IP list' | wc -l)"
echo "Disk usage: $(df -h / | awk 'NR==2 {print $5}')"
echo "Memory usage: $(free | awk 'NR==2{printf "%.0f%%", $3*100/$2}')"
echo "Load average: $(uptime | awk -F'load average:' '{print $2}')"
```

---

## Safe Skill Installation

### Skill Security Checklist

```bash
#!/bin/bash
# check-skill.sh - Security check for skill installation

SKILL_NAME=$1

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <skill-name>"
    exit 1
fi

SKILL_DIR="$HOME/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/$SKILL_NAME"

echo "=== Security Check: $SKILL_NAME ==="

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Skill not found"
    exit 1
fi

echo "Checking SKILL.md..."

# Check for dangerous patterns
DANGEROUS_PATTERNS=(
    "eval("
    "exec.*rm -rf"
    "sudo"
    "curl.*|.*bash"
    "wget.*|.*sh"
    "/etc/shadow"
    "/etc/passwd"
    "~/.ssh"
    "fetch.*http"
)

FOUND_DANGEROUS=0
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if grep -r "$pattern" "$SKILL_DIR" 2>/dev/null; then
        echo "⚠️  Found potentially dangerous pattern: $pattern"
        FOUND_DANGEROUS=1
    fi
done

if [ $FOUND_DANGEROUS -eq 0 ]; then
    echo "✅ No dangerous patterns found"
fi

# Check file permissions
echo ""
echo "Checking file permissions..."
find "$SKILL_DIR" -type f -perm /002 -exec ls -l {} \;

echo ""
echo "=== Check Complete ==="
echo "Review the output above before installing this skill"
```

---

## Incident Response

### Breach Response Playbook

```bash
#!/bin/bash
# incident-response.sh - Emergency response script

set -e

REPORT_FILE="/tmp/incident-report-$(date +%Y%m%d_%H%M%S).txt"

echo "🚨 SECURITY INCIDENT RESPONSE 🚨"
echo "Started: $(date)" | tee "$REPORT_FILE"
echo ""

echo "Step 1: Document active connections..."
ss -tp | tee -a "$REPORT_FILE"

echo ""
echo "Step 2: Check recent logins..."
last -20 | tee -a "$REPORT_FILE"

echo ""
echo "Step 3: Check running processes..."
ps auxf | tee -a "$REPORT_FILE"

echo ""
echo "Step 4: Check for suspicious users..."
grep -v "nologin\|false" /etc/passwd | tee -a "$REPORT_FILE"

echo ""
echo "Step 5: Check cron jobs..."
echo "=== User crons ===" | tee -a "$REPORT_FILE"
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -u $user -l 2>/dev/null | grep -v "^#" | grep -v "^$" && echo "User: $user" | tee -a "$REPORT_FILE"
done

echo "=== System crons ===" | tee -a "$REPORT_FILE"
ls -la /etc/cron.d/ /etc/cron.hourly/ /etc/cron.daily/ | tee -a "$REPORT_FILE"

echo ""
echo "Step 6: Recent file changes..."
find / -mtime -1 -type f 2>/dev/null | head -50 | tee -a "$REPORT_FILE"

echo ""
echo "========================================"
echo "REPORT SAVED TO: $REPORT_FILE"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Review the report above"
echo "2. Change ALL passwords and API keys"
echo "3. Check for unauthorized SSH keys: cat ~/.ssh/authorized_keys"
echo "4. Consider isolating the system from network"
echo "5. Notify relevant parties"
```

### Emergency Lockdown

```bash
#!/bin/bash
# emergency-lockdown.sh - Isolate system immediately

echo "🔒 EMERGENCY LOCKDOWN INITIATED"
echo "Time: $(date)"

# Block all incoming except your IP
YOUR_IP=$(echo $SSH_CONNECTION | awk '{print $1}')

echo "Allowing only: $YOUR_IP"

# Reset UFW
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow only your IP
ufw allow from $YOUR_IP to any port 22

# Enable firewall
ufw --force enable

# Stop OpenClaw
systemctl stop openclaw

echo "✅ Lockdown complete"
echo "System isolated. Only $YOUR_IP can access SSH."
echo "OpenClaw service stopped."
```

---

**Security Maintenance Schedule:**

| Task | Frequency | Command |
|------|-----------|---------|
| Security audit | Weekly | `sudo ./security-audit.sh` |
| Update check | Daily | `apt list --upgradable` |
| fail2ban review | Weekly | `fail2ban-client status` |
| Key rotation | Quarterly | `./rotate-api-keys.sh` |
| Log review | Daily | `tail /var/log/auth.log` |
| Backup test | Monthly | Restore from backup |

---

**Estimated Setup Time**: 1-2 hours
**Maintenance**: 15 minutes/week
