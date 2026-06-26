#!/usr/bin/env bash
# OpenClaw Setup Wizard - Security Hardening Script
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
fixed=0; skipped=0

echo "🔒 OpenClaw Security Hardening"
echo "=============================="
echo ""

# 1. Config file permissions
echo "1. Config file permissions"
for f in "$HOME/.openclaw/openclaw.json" \
         "$HOME/.openclaw/agents/main/agent/models.json" \
         "$HOME/.openclaw/agents/main/agent/auth-profiles.json"; do
    if [ -f "$f" ]; then
        PERMS=$(stat -f "%Lp" "$f" 2>/dev/null || stat -c "%a" "$f" 2>/dev/null)
        if [ "$PERMS" != "600" ]; then
            chmod 600 "$f"
            echo -e "  ${GREEN}✅ Fixed${NC}: $f (was $PERMS → 600)"
            fixed=$((fixed + 1))
        else
            echo -e "  ${GREEN}✅ OK${NC}: $f (600)"
        fi
    fi
done

# 2. Gateway token check
echo ""
echo "2. Gateway token strength"
CONFIG="$HOME/.openclaw/openclaw.json"
if [ -f "$CONFIG" ]; then
    if grep -qE '"(mysecret123|password|changeme|secret|12345)"' "$CONFIG" 2>/dev/null; then
        echo -e "  ${RED}❌ WEAK TOKEN DETECTED${NC}"
        echo "     Run: openclaw configure --section gateway"
        echo "     Use a strong random token (32+ chars)"
        skipped=$((skipped + 1))
    else
        echo -e "  ${GREEN}✅ OK${NC}: Token appears strong"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC}: Config file not found"
fi

# 3. Workspace permissions
echo ""
echo "3. Workspace directory permissions"
WS="$HOME/.openclaw/workspace"
if [ -d "$WS" ]; then
    WS_PERMS=$(stat -f "%Lp" "$WS" 2>/dev/null || stat -c "%a" "$WS" 2>/dev/null)
    if [ "$WS_PERMS" != "700" ] && [ "$WS_PERMS" != "755" ]; then
        chmod 700 "$WS"
        echo -e "  ${GREEN}✅ Fixed${NC}: workspace (was $WS_PERMS → 700)"
        fixed=$((fixed + 1))
    else
        echo -e "  ${GREEN}✅ OK${NC}: workspace ($WS_PERMS)"
    fi
fi

# 4. Check for exposed secrets in logs
echo ""
echo "4. Secret exposure in logs"
LOG_DIR="$HOME/.openclaw/agents/main/sessions"
EXPOSED=0
if [ -d "$LOG_DIR" ]; then
    # Check recent logs only (last 24h)
    RECENT=$(find "$LOG_DIR" -name "*.json" -mtime -1 2>/dev/null | head -20)
    for log in $RECENT; do
        if grep -qiE '(api[_-]?key|secret|token|password)["\s]*[:=]["\s]*[A-Za-z0-9_-]{20,}' "$log" 2>/dev/null; then
            EXPOSED=$((EXPOSED + 1))
        fi
    done
    if [ "$EXPOSED" -gt 0 ]; then
        echo -e "  ${YELLOW}⚠️${NC}: Found $EXPOSED log files with potential secret exposure"
        echo "     Consider rotating affected keys"
    else
        echo -e "  ${GREEN}✅ OK${NC}: No secrets found in recent logs"
    fi
else
    echo -e "  ${GREEN}✅ OK${NC}: No session logs to check"
fi

# 5. Backup verification
echo ""
echo "5. Backup configuration"
BACKUP_DIR="$HOME/backups/openclaw"
if [ -d "$BACKUP_DIR" ]; then
    BACKUP_COUNT=$(ls "$BACKUP_DIR" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BACKUP_COUNT" -gt 0 ]; then
        echo -e "  ${GREEN}✅ OK${NC}: $BACKUP_COUNT backups found"
    else
        echo -e "  ${YELLOW}⚠️${NC}: Backup directory empty"
    fi
else
    mkdir -p "$BACKUP_DIR"
    echo -e "  ${GREEN}✅ Created${NC}: $BACKUP_DIR"
    fixed=$((fixed + 1))
fi

# 6. Auto-start resilience
echo ""
echo "6. Auto-start configuration"
PLIST="$HOME/Library/LaunchAgents/com.openclaw.gateway.plist"
if [ -f "$PLIST" ]; then
    ISSUES=""
    grep -q "RunAtLoad.*true" "$PLIST" || ISSUES="${ISSUES}RunAtLoad "
    grep -q "KeepAlive.*true" "$PLIST" || ISSUES="${ISSUES}KeepAlive "
    if [ -z "$ISSUES" ]; then
        echo -e "  ${GREEN}✅ OK${NC}: RunAtLoad + KeepAlive enabled"
    else
        echo -e "  ${YELLOW}⚠️${NC}: Missing: $ISSUES"
        echo "     Edit $PLIST to add these settings"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC}: No LaunchAgent found"
    echo "     Run: openclaw gateway install"
fi

# 7. macOS specific
echo ""
echo "7. macOS power settings"
if command -v pmset &>/dev/null; then
    SLEEP=$(pmset -g | grep "^[[:space:]]*sleep" | head -1 | awk '{print $2}')
    if [ "$SLEEP" = "0" ]; then
        echo -e "  ${GREEN}✅ OK${NC}: Sleep disabled"
    else
        echo -e "  ${YELLOW}⚠️${NC}: Sleep = $SLEEP (recommend: sudo pmset -a sleep 0 disksleep 0)"
        skipped=$((skipped + 1))
    fi
fi

# Summary
echo ""
echo "=============================="
echo "🔧 Fixed: $fixed | ⏭️ Manual: $skipped"
if [ "$skipped" -eq 0 ] && [ "$fixed" -eq 0 ]; then
    echo -e "🏆 ${GREEN}All secure!${NC}"
else
    echo "Run this script again after fixing manual items."
fi
