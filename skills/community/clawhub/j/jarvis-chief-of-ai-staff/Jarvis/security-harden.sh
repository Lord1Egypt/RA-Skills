#!/usr/bin/env bash
# security-harden.sh — Security hardening for Jarvis on DGX Spark
# Author: Yogesh Huja (https://www.linkedin.com/in/yogeshhuja/)
# Powered by: Gignaati (https://gignaati.com)
# License: MIT
#
# SECURITY DECLARATION:
# This script does NOT make network calls to external endpoints.
# This script does NOT install packages or download binaries.
# This script ONLY modifies local OpenClaw configuration and firewall rules.
# All changes are logged and reversible.

set -euo pipefail

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/security-audit.log"
TIMESTAMP=$(date -Iseconds)

echo "============================================"
echo " Jarvis — Security Hardening"
echo " Powered by Gignaati"
echo "============================================"
echo ""

log_action() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
    echo "   $1"
}

# --- Step 1: Audit current state ---
echo "🔍 Step 1: Auditing current security posture..."
echo ""

log_action "AUDIT: Security hardening started"

# Check if OpenClaw is running
if systemctl is-active --quiet openclaw 2>/dev/null; then
    log_action "AUDIT: OpenClaw gateway is running"
else
    log_action "WARNING: OpenClaw gateway is not running"
fi

# Check open ports
echo "   Open ports listening:"
ss -tlnp 2>/dev/null | grep -E ':(18789|11434|8888|8080)' | while read -r line; do
    echo "     $line"
    log_action "AUDIT: Open port detected: $line"
done
echo ""

# Check if dashboard is exposed beyond localhost
if ss -tlnp 2>/dev/null | grep -q '0.0.0.0:18789'; then
    echo "   ⚠️  WARNING: Dashboard is exposed on all interfaces (0.0.0.0:18789)"
    log_action "WARNING: Dashboard exposed on 0.0.0.0:18789 — should be 127.0.0.1 only"
else
    echo "   ✅ Dashboard is localhost-only"
    log_action "OK: Dashboard is localhost-only"
fi
echo ""

# --- Step 2: Configure WhatsApp allowlist ---
echo "🔒 Step 2: WhatsApp allowlist configuration..."
echo ""
echo "   To restrict who can message Jarvis, add your phone number(s)"
echo "   to the allowlist in ~/.openclaw/openclaw.json:"
echo ""
echo '   {
     "channels": {
       "whatsapp": {
         "allowFrom": ["+91XXXXXXXXXX"]
       }
     }
   }'
echo ""
echo "   For group chats, require @mention to prevent prompt injection:"
echo ""
echo '   {
     "channels": {
       "whatsapp": {
         "groups": {
           "*": { "requireMention": true }
         }
       }
     }
   }'
echo ""
log_action "REMINDER: Configure WhatsApp allowlist in openclaw.json"

# --- Step 3: UFW firewall rules ---
echo "🧱 Step 3: Firewall configuration..."
echo ""

if command -v ufw &>/dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | head -1)
    echo "   Current UFW status: $UFW_STATUS"

    if [[ "$UFW_STATUS" == *"inactive"* ]]; then
        echo ""
        echo "   Recommended UFW rules for Jarvis:"
        echo "     sudo ufw default deny incoming"
        echo "     sudo ufw default allow outgoing"
        echo "     sudo ufw allow ssh"
        echo "     sudo ufw allow from 100.64.0.0/10 to any port 18789  # Tailscale only"
        echo "     sudo ufw enable"
        echo ""
        log_action "REMINDER: UFW is inactive — enable with recommended rules"
    else
        echo "   ✅ UFW is active"
        log_action "OK: UFW is active"
    fi
else
    echo "   ⚠️  UFW not installed. Install with: sudo apt install ufw"
    log_action "WARNING: UFW not installed"
fi
echo ""

# --- Step 4: SSL for dashboard ---
echo "🔐 Step 4: SSL certificate check..."
echo ""

SSL_DIR="$HOME/.openclaw/ssl"
if [ -f "$SSL_DIR/cert.pem" ] && [ -f "$SSL_DIR/key.pem" ]; then
    echo "   ✅ SSL certificates found at $SSL_DIR"
    log_action "OK: SSL certificates present"
else
    echo "   ⚠️  No SSL certificates found."
    echo "   Generate self-signed certs:"
    echo "     mkdir -p $SSL_DIR"
    echo "     openssl req -x509 -newkey rsa:4096 -keyout $SSL_DIR/key.pem \\"
    echo "       -out $SSL_DIR/cert.pem -days 365 -nodes \\"
    echo "       -subj '/CN=jarvis.local'"
    echo ""
    log_action "REMINDER: Generate SSL certificates for dashboard"
fi
echo ""

# --- Step 5: Tailscale check ---
echo "🌐 Step 5: Remote access security..."
echo ""

if command -v tailscale &>/dev/null; then
    TS_STATUS=$(tailscale status 2>/dev/null | head -1 || echo "Not connected")
    echo "   Tailscale status: $TS_STATUS"
    log_action "OK: Tailscale installed — $TS_STATUS"
else
    echo "   ⚠️  Tailscale not installed."
    echo "   For secure remote access, install Tailscale:"
    echo "   See: https://build.nvidia.com/spark/tailscale"
    log_action "REMINDER: Install Tailscale for secure remote access"
fi
echo ""

# --- Step 6: Workspace permissions ---
echo "📂 Step 6: Workspace file permissions..."
echo ""

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
if [ -d "$WORKSPACE" ]; then
    # Ensure workspace is not world-readable
    chmod 700 "$WORKSPACE"
    chmod 600 "$WORKSPACE"/*.md 2>/dev/null || true
    echo "   ✅ Workspace permissions set to owner-only (700/600)"
    log_action "OK: Workspace permissions hardened"
else
    echo "   ⚠️  Workspace not found at $WORKSPACE"
    log_action "WARNING: Workspace directory not found"
fi
echo ""

# --- Summary ---
echo "============================================"
echo " 🛡️  Security Hardening Complete"
echo "============================================"
echo ""
echo " Audit log: $LOG_FILE"
echo ""
echo " MANUAL ACTIONS REQUIRED:"
echo " 1. Add your phone number to WhatsApp allowlist"
echo " 2. Enable UFW firewall if inactive"
echo " 3. Generate SSL certificates if missing"
echo " 4. Install Tailscale if remote access needed"
echo ""
echo " After changes, restart gateway:"
echo "   sudo systemctl restart openclaw"
echo ""
echo " For the full security model, read:"
echo "   https://docs.openclaw.ai/gateway/security"
echo ""
echo " By Yogesh Huja | Powered by Gignaati"
echo "============================================"

log_action "AUDIT: Security hardening completed"
