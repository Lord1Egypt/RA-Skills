#!/usr/bin/env bash
# OpenClaw Setup Wizard - Diagnostic Script
# Checks 12 areas and outputs JSON report
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
PASS="${GREEN}✅${NC}"; FAIL="${RED}❌${NC}"; WARN="${YELLOW}⚠️${NC}"

score=0; total=0; issues=()

check() {
    local name="$1" result="$2" detail="${3:-}"
    total=$((total + 1))
    if [ "$result" = "pass" ]; then
        score=$((score + 1))
        echo -e "  ${PASS} ${name}"
    elif [ "$result" = "warn" ]; then
        score=$((score + 1))
        echo -e "  ${WARN} ${name}: ${detail}"
        issues+=("WARN: ${name} - ${detail}")
    else
        echo -e "  ${FAIL} ${name}: ${detail}"
        issues+=("FAIL: ${name} - ${detail}")
    fi
}

echo "🔍 OpenClaw Setup Wizard - Diagnostic Report"
echo "============================================="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Host: $(hostname)"
echo "OS: $(uname -s) $(uname -r) ($(uname -m))"
echo ""

# 1. OpenClaw Installation
echo "📦 1. OpenClaw Installation"
if command -v openclaw &>/dev/null; then
    OC_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
    check "OpenClaw installed" "pass"
    echo "     Version: ${OC_VERSION}"
else
    check "OpenClaw installed" "fail" "openclaw command not found"
fi

# 2. Gateway Status
echo ""
echo "🌐 2. Gateway Status"
GW_STATUS=$(openclaw gateway status 2>&1 || true)
if echo "$GW_STATUS" | grep -qi "running\|online\|active"; then
    check "Gateway running" "pass"
else
    check "Gateway running" "fail" "Gateway not running"
fi

# 3. Node.js
echo ""
echo "📗 3. Node.js"
if command -v node &>/dev/null; then
    NODE_V=$(node --version 2>/dev/null)
    check "Node.js installed" "pass"
    echo "     Version: ${NODE_V}"
    NODE_MAJOR=$(echo "$NODE_V" | sed 's/v//' | cut -d. -f1)
    if [ "$NODE_MAJOR" -ge 20 ]; then
        check "Node.js version >= 20" "pass"
    else
        check "Node.js version >= 20" "warn" "v${NODE_V}, recommend v20+"
    fi
else
    check "Node.js installed" "fail" "node command not found"
fi

# 4. Provider Configuration
echo ""
echo "🤖 4. LLM Provider"
MODELS_DIR="$HOME/.openclaw/agents/main/agent"
if [ -f "$MODELS_DIR/models.json" ]; then
    check "models.json exists" "pass"
    # Check if any model is configured
    if grep -q '"model"' "$MODELS_DIR/models.json" 2>/dev/null; then
        DEFAULT_MODEL=$(grep -o '"model"[[:space:]]*:[[:space:]]*"[^"]*"' "$MODELS_DIR/models.json" | head -1 | cut -d'"' -f4)
        check "Default model configured" "pass"
        echo "     Model: ${DEFAULT_MODEL}"
    else
        check "Default model configured" "fail" "No model set"
    fi
else
    check "models.json exists" "fail" "No provider configuration found"
fi

# Check fallbacks
FALLBACKS=$(openclaw models fallbacks list 2>&1 || true)
if echo "$FALLBACKS" | grep -qi "no fallback\|empty\|none"; then
    check "Fallback models" "warn" "No fallback configured"
else
    check "Fallback models" "pass"
fi

# 5. Channels
echo ""
echo "💬 5. Chat Channels"
CHANNELS=$(openclaw status 2>&1 | grep -i "channel\|telegram\|discord\|slack\|whatsapp\|signal" || true)
if [ -n "$CHANNELS" ]; then
    check "Chat channels" "pass"
    echo "$CHANNELS" | head -5 | sed 's/^/     /'
else
    check "Chat channels" "warn" "No channels detected in status output"
fi

# 6. Skills
echo ""
echo "🧩 6. Installed Skills"
SKILL_COUNT=0
if [ -d "$HOME/.openclaw/workspace/skills" ]; then
    SKILL_COUNT=$(find "$HOME/.openclaw/workspace/skills" -maxdepth 1 -type d | wc -l | tr -d ' ')
    SKILL_COUNT=$((SKILL_COUNT - 1))  # subtract parent dir
fi
BUILTIN_COUNT=0
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills" ]; then
    BUILTIN_COUNT=$(find "/opt/homebrew/lib/node_modules/openclaw/skills" -maxdepth 1 -type d | wc -l | tr -d ' ')
    BUILTIN_COUNT=$((BUILTIN_COUNT - 1))
fi
TOTAL_SKILLS=$((SKILL_COUNT + BUILTIN_COUNT))
if [ "$TOTAL_SKILLS" -gt 5 ]; then
    check "Skills installed" "pass"
elif [ "$TOTAL_SKILLS" -gt 0 ]; then
    check "Skills installed" "warn" "Only ${TOTAL_SKILLS} skills, recommend 5+"
else
    check "Skills installed" "fail" "No skills found"
fi
echo "     Custom: ${SKILL_COUNT} | Built-in: ${BUILTIN_COUNT} | Total: ${TOTAL_SKILLS}"

# 7. Cron Jobs
echo ""
echo "⏰ 7. Cron Jobs"
CRON_OUTPUT=$(openclaw cron list 2>&1 || true)
CRON_COUNT=$(echo "$CRON_OUTPUT" | grep -c "ok\|idle\|error" || true)
if [ "$CRON_COUNT" -gt 0 ]; then
    check "Cron jobs configured" "pass"
    echo "     Active jobs: ${CRON_COUNT}"
else
    check "Cron jobs configured" "warn" "No cron jobs set up"
fi

# 8. Backup
echo ""
echo "💾 8. Backup"
if [ -d "$HOME/backups/openclaw" ]; then
    LATEST_BACKUP=$(ls -t "$HOME/backups/openclaw/" 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        check "Backup directory" "pass"
        echo "     Latest: ${LATEST_BACKUP}"
    else
        check "Backup directory" "warn" "Directory exists but empty"
    fi
else
    check "Backup directory" "warn" "No backup directory at ~/backups/openclaw/"
fi

# 9. Security
echo ""
echo "🔒 9. Security"
# Check config file permissions
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    PERMS=$(stat -f "%Lp" "$CONFIG_FILE" 2>/dev/null || stat -c "%a" "$CONFIG_FILE" 2>/dev/null || echo "unknown")
    if [ "$PERMS" = "600" ]; then
        check "Config permissions" "pass"
    else
        check "Config permissions" "warn" "Permissions are ${PERMS}, recommend 600"
    fi
fi

# Check gateway token
if [ -f "$CONFIG_FILE" ]; then
    if grep -q '"mysecret123"\|"password"\|"changeme"\|"secret"' "$CONFIG_FILE" 2>/dev/null; then
        check "Gateway token" "fail" "Using default/weak token!"
    else
        check "Gateway token" "pass"
    fi
fi

# 10. System Resources
echo ""
echo "💻 10. System Resources"
# Disk
DISK_USED=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USED" -lt 80 ]; then
    check "Disk usage" "pass"
elif [ "$DISK_USED" -lt 90 ]; then
    check "Disk usage" "warn" "${DISK_USED}% used"
else
    check "Disk usage" "fail" "${DISK_USED}% used - critical!"
fi
echo "     Disk: ${DISK_USED}% used"

# Memory (macOS)
if command -v vm_stat &>/dev/null; then
    FREE_PAGES=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
    INACTIVE_PAGES=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | tr -d '.')
    AVAIL_MB=$(( (FREE_PAGES + INACTIVE_PAGES) * 16384 / 1048576 ))
    if [ "$AVAIL_MB" -gt 2048 ]; then
        check "Available memory" "pass"
    elif [ "$AVAIL_MB" -gt 1024 ]; then
        check "Available memory" "warn" "${AVAIL_MB}MB available"
    else
        check "Available memory" "fail" "Only ${AVAIL_MB}MB available"
    fi
    echo "     Available: ${AVAIL_MB}MB"
fi

# 11. Auto-start
echo ""
echo "🔄 11. Auto-start"
PLIST="$HOME/Library/LaunchAgents/com.openclaw.gateway.plist"
if [ -f "$PLIST" ]; then
    check "LaunchAgent configured" "pass"
    if grep -q "RunAtLoad.*true" "$PLIST" 2>/dev/null; then
        check "RunAtLoad enabled" "pass"
    else
        check "RunAtLoad enabled" "warn" "Not set to start on boot"
    fi
    if grep -q "KeepAlive.*true" "$PLIST" 2>/dev/null; then
        check "KeepAlive enabled" "pass"
    else
        check "KeepAlive enabled" "warn" "Won't auto-restart on crash"
    fi
else
    check "LaunchAgent configured" "warn" "No LaunchAgent found"
fi

# 12. Workspace Files
echo ""
echo "📄 12. Workspace Files"
WS="$HOME/.openclaw/workspace"
for f in SOUL.md AGENTS.md MEMORY.md TOOLS.md USER.md; do
    if [ -f "$WS/$f" ]; then
        check "$f" "pass"
    else
        check "$f" "warn" "Missing - recommended for personalization"
    fi
done

# Summary
echo ""
echo "============================================="
echo "📊 Score: ${score}/${total}"
PCT=$((score * 100 / total))
if [ "$PCT" -ge 90 ]; then
    echo -e "🏆 Rating: ${GREEN}EXCELLENT${NC}"
elif [ "$PCT" -ge 70 ]; then
    echo -e "👍 Rating: ${GREEN}GOOD${NC}"
elif [ "$PCT" -ge 50 ]; then
    echo -e "⚠️  Rating: ${YELLOW}NEEDS WORK${NC}"
else
    echo -e "🚨 Rating: ${RED}CRITICAL${NC}"
fi

if [ ${#issues[@]} -gt 0 ]; then
    echo ""
    echo "📋 Issues to fix:"
    for issue in "${issues[@]}"; do
        echo "  - $issue"
    done
fi

echo ""
echo "Run 'bash scripts/harden.sh' to fix security issues."
