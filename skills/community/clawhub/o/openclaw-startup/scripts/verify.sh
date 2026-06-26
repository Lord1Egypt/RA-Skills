#!/bin/bash
# openclaw-startup: Post-setup verification
# Usage: bash verify.sh [workspace_path]

set -euo pipefail

WORKSPACE="${1:-${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}}"
ERRORS=0
WARNINGS=0

echo "🔍 OpenClaw Startup — Post-Setup Verification"
echo "   Workspace: $WORKSPACE"
echo ""

check_file() {
    local file="$1"
    local label="$2"
    local required="${3:-true}"
    
    if [ -f "$file" ]; then
        local size=$(wc -c < "$file" | tr -d ' ')
        if [ "$size" -gt 0 ]; then
            echo "  ✅ $label ($size bytes)"
        else
            echo "  ⚠️  $label (empty!)"
            WARNINGS=$((WARNINGS + 1))
        fi
    elif [ "$required" = "true" ]; then
        echo "  ❌ $label (MISSING)"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ⏭️  $label (optional, not present)"
    fi
}

echo "## Core Files"
check_file "$WORKSPACE/SOUL.md" "SOUL.md"
check_file "$WORKSPACE/USER.md" "USER.md"
check_file "$WORKSPACE/IDENTITY.md" "IDENTITY.md"
check_file "$WORKSPACE/AGENTS.md" "AGENTS.md"
check_file "$WORKSPACE/MEMORY.md" "MEMORY.md"
check_file "$WORKSPACE/ACTIVE.md" "ACTIVE.md"
check_file "$WORKSPACE/HEARTBEAT.md" "HEARTBEAT.md" "false"

echo ""
echo "## Memory Structure"
check_file "$WORKSPACE/memory/FUTURE_INTENTS.md" "FUTURE_INTENTS.md"
[ -d "$WORKSPACE/memory/bank" ] && echo "  ✅ memory/bank/" || { echo "  ❌ memory/bank/ (MISSING)"; ERRORS=$((ERRORS + 1)); }
[ -d "$WORKSPACE/memory/procedures" ] && echo "  ✅ memory/procedures/" || { echo "  ⚠️  memory/procedures/ (missing)"; WARNINGS=$((WARNINGS + 1)); }

echo ""
echo "## Learning Files"
check_file "$WORKSPACE/.learnings/errors.md" ".learnings/errors.md" "false"
check_file "$WORKSPACE/.learnings/learnings.md" ".learnings/learnings.md" "false"
check_file "$WORKSPACE/.learnings/wishes.md" ".learnings/wishes.md" "false"

echo ""
echo "## Git Status"
if [ -d "$WORKSPACE/.git" ]; then
    cd "$WORKSPACE"
    DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    if [ "$DIRTY" -eq 0 ]; then
        echo "  ✅ Git repo clean"
    else
        echo "  ⚠️  Git repo has $DIRTY uncommitted changes"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ⚠️  No git repo initialized"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "## Cron Jobs"
if command -v openclaw &>/dev/null; then
    CRON_COUNT=$(openclaw cron list 2>/dev/null | grep -c "enabled" || echo "0")
    echo "  📋 Active crons: $CRON_COUNT"
    if [ "$CRON_COUNT" -eq 0 ]; then
        echo "  ⚠️  No crons configured — consider adding a heartbeat"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ⏭️  openclaw CLI not available for cron check"
fi

echo ""
echo "## Security Quick Check"
# Check for exposed secrets in workspace (broad pattern set)
SECRET_PATTERN="sk-\|ghp_\|xoxb-\|xoxp-\|Bearer \|AKIA[A-Z0-9]\|hooks\.slack\.com\|AIza[A-Za-z0-9_-]\|-----BEGIN.*PRIVATE KEY\|password[[:space:]]*=[[:space:]]*['\"]"
SECRET_HITS="$(grep -rl "$SECRET_PATTERN" "$WORKSPACE"/*.md "$WORKSPACE"/memory/*.md 2>/dev/null || true)"
SECRET_HITS="$(echo "$SECRET_HITS" | grep -c . || true)"
if [ "$SECRET_HITS" -gt 0 ]; then
    echo "  ⚠️  Possible exposed secrets in $SECRET_HITS file(s)"
    echo "     Tip: consider running gitleaks or trufflehog for deeper scanning"
    WARNINGS=$((WARNINGS + 1))
else
    echo "  ✅ No obvious secrets in workspace files"
fi

# Check SOUL.md for safety rules
if [ -f "$WORKSPACE/SOUL.md" ]; then
    if grep -qi "injection\|override.*instruction\|exfiltrat\|hard stop\|never.*share\|no external" "$WORKSPACE/SOUL.md" 2>/dev/null; then
        echo "  ✅ SOUL.md contains safety/injection defense rules"
    else
        echo "  ⚠️  SOUL.md missing injection defense rules"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

echo ""
echo "## OpenClaw Doctor"
if command -v openclaw &>/dev/null; then
    echo "  Running openclaw doctor..."
    if openclaw doctor --non-interactive 2>&1 | grep -qi "warning\|error\|fail"; then
        echo "  ⚠️  openclaw doctor reported issues — review output above"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ✅ openclaw doctor passed"
    fi
else
    echo "  ⏭️  openclaw CLI not available — skipping doctor check"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $ERRORS errors, $WARNINGS warnings"

if [ "$ERRORS" -gt 0 ]; then
    echo "❌ Setup incomplete — fix errors above"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo "⚠️  Setup complete with warnings"
    exit 0
else
    echo "✅ Setup verified — all clear!"
    exit 0
fi
