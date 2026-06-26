#!/bin/bash
# Full Security Audit Suite with Frequency Management

set -e

TARGET_PATH="${1:-.}"
SCAN_TYPE="${2:-quick}"  # quick, full, history, dependencies, ai
STATE_FILE="$HOME/.openclaw/workspace/skills/pre-publish-security/audit-state.json"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
REPORT_FILE="/tmp/security-audit-$(date +%s).md"

# Initialize state file if missing
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'EOF'
{
  "lastRun": {},
  "scanCount": {},
  "findings": { "total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0 }
}
EOF
fi

CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0

cd "$TARGET_PATH"

echo "# Security Audit Report" > "$REPORT_FILE"
echo "**Target:** $TARGET_PATH" >> "$REPORT_FILE"
echo "**Scan Type:** $SCAN_TYPE" >> "$REPORT_FILE"
echo "**Time:** $TIMESTAMP" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

### QUICK SCAN (Always) ###
if [ "$SCAN_TYPE" = "quick" ] || [ "$SCAN_TYPE" = "full" ]; then
    echo "## 🔒 Quick Security Scan" >> "$REPORT_FILE"
    echo "**Frequency:** Every push" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # Secret patterns (current files only)
    SECRETS=$(grep -r -E "(github_pat_|ghp_|AKIA|sk-[A-Za-z0-9]{32,}|api[_-]?key|Bearer [A-Za-z0-9_-]+)" . \
      --exclude-dir=node_modules \
      --exclude-dir=.git \
      --exclude="*.tar.gz" \
      --exclude="audit-*.sh" \
      2>/dev/null || true)
    
    if [ -n "$SECRETS" ]; then
        echo "❌ **CRITICAL:** Secrets detected in current files" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        echo "$SECRETS" | head -5 >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        ((CRITICAL_COUNT++))
    else
        echo "✅ No secrets in current files" >> "$REPORT_FILE"
    fi
    
    # Documentation check
    PLACEHOLDERS=$(grep -r -E "\[ORG\]|\[TODO\]|\[USERNAME\]|example\.com|your-.*-here" . \
      --include="*.md" \
      --include="*.json" \
      2>/dev/null || true)
    
    if [ -n "$PLACEHOLDERS" ]; then
        echo "❌ **CRITICAL:** Placeholders found" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        echo "$PLACEHOLDERS" | head -3 >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        ((CRITICAL_COUNT++))
    else
        echo "✅ No placeholders" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    
    # Update state
    jq ".lastRun.quickScan = \"$TIMESTAMP\" | .scanCount.quickScan += 1" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

### GIT HISTORY DEEP SCAN (Monthly/On-Demand) ###
if [ "$SCAN_TYPE" = "history" ] || [ "$SCAN_TYPE" = "full" ]; then
    LAST_HISTORY=$(jq -r '.lastRun.historyScan // "never"' "$STATE_FILE")
    
    echo "## 🕵️ Git History Deep Scan" >> "$REPORT_FILE"
    echo "**Frequency:** Monthly or on-demand" >> "$REPORT_FILE"
    echo "**Last Run:** $LAST_HISTORY" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    if [ -d .git ]; then
        echo "Scanning git history (this may take a while)..."
        HISTORY_SECRETS=$(git log --all --full-history -p 2>/dev/null | \
          grep -E "(github_pat_|ghp_|AKIA|sk-[A-Za-z0-9]{32,}|api[_-]?key|Bearer [A-Za-z0-9_-]+)" | \
          head -10 || true)
        
        if [ -n "$HISTORY_SECRETS" ]; then
            echo "❌ **CRITICAL:** Secrets found in git history!" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
            echo "$HISTORY_SECRETS" | head -5 >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
            echo "" >> "$REPORT_FILE"
            echo "⚠️ **Action Required:** These secrets are permanently in git history." >> "$REPORT_FILE"
            echo "Consider: git filter-repo, BFG Repo-Cleaner, or repo reset." >> "$REPORT_FILE"
            ((CRITICAL_COUNT++))
        else
            echo "✅ No secrets in git history" >> "$REPORT_FILE"
        fi
    else
        echo "ℹ️ Not a git repository, skipping history scan" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    
    # Update state
    jq ".lastRun.historyScan = \"$TIMESTAMP\" | .scanCount.historyScan += 1" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

### DEPENDENCY CVE SCAN (Weekly) ###
if [ "$SCAN_TYPE" = "dependencies" ] || [ "$SCAN_TYPE" = "full" ]; then
    LAST_DEP=$(jq -r '.lastRun.dependencyScan // "never"' "$STATE_FILE")
    
    echo "## 📦 Dependency Security Scan" >> "$REPORT_FILE"
    echo "**Frequency:** Weekly" >> "$REPORT_FILE"
    echo "**Last Run:** $LAST_DEP" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # NPM audit
    if [ -f package.json ]; then
        NPM_AUDIT=$(npm audit --json 2>/dev/null || echo '{}')
        VULN_COUNT=$(echo "$NPM_AUDIT" | jq '.metadata.vulnerabilities | to_entries | map(select(.value > 0)) | length' 2>/dev/null || echo 0)
        
        if [ "$VULN_COUNT" -gt 0 ]; then
            CRITICAL_VULN=$(echo "$NPM_AUDIT" | jq -r '.metadata.vulnerabilities.critical // 0')
            HIGH_VULN=$(echo "$NPM_AUDIT" | jq -r '.metadata.vulnerabilities.high // 0')
            
            if [ "$CRITICAL_VULN" -gt 0 ]; then
                echo "❌ **CRITICAL:** $CRITICAL_VULN critical npm vulnerabilities" >> "$REPORT_FILE"
                ((CRITICAL_COUNT++))
            fi
            
            if [ "$HIGH_VULN" -gt 0 ]; then
                echo "⚠️ **HIGH:** $HIGH_VULN high npm vulnerabilities" >> "$REPORT_FILE"
                ((HIGH_COUNT++))
            fi
            
            echo "" >> "$REPORT_FILE"
            echo "Run: \`npm audit fix\` to resolve" >> "$REPORT_FILE"
        else
            echo "✅ No npm vulnerabilities" >> "$REPORT_FILE"
        fi
    else
        echo "ℹ️ No package.json found" >> "$REPORT_FILE"
    fi
    
    # Python safety check (if requirements.txt exists)
    if [ -f requirements.txt ]; then
        if command -v safety >/dev/null 2>&1; then
            SAFETY_CHECK=$(safety check --json 2>/dev/null || echo '[]')
            SAFETY_COUNT=$(echo "$SAFETY_CHECK" | jq 'length' 2>/dev/null || echo 0)
            
            if [ "$SAFETY_COUNT" -gt 0 ]; then
                echo "⚠️ **HIGH:** $SAFETY_COUNT Python package vulnerabilities" >> "$REPORT_FILE"
                ((HIGH_COUNT++))
            else
                echo "✅ No Python vulnerabilities" >> "$REPORT_FILE"
            fi
        else
            echo "ℹ️ Safety not installed (pip install safety)" >> "$REPORT_FILE"
        fi
    fi
    
    echo "" >> "$REPORT_FILE"
    
    # Update state
    jq ".lastRun.dependencyScan = \"$TIMESTAMP\" | .scanCount.dependencyScan += 1" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

### ENVIRONMENT VARIABLE LEAK DETECTION ###
if [ "$SCAN_TYPE" = "full" ]; then
    echo "## 🔐 Environment Variable Leak Detection" >> "$REPORT_FILE"
    echo "**Frequency:** Weekly" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    ENV_LEAKS=$(grep -r "export.*KEY\|export.*TOKEN\|export.*PASSWORD\|export.*SECRET" . \
      --include="*.sh" \
      --include="*.bash" \
      --exclude-dir=node_modules \
      2>/dev/null | grep -v "^Binary" || true)
    
    if [ -n "$ENV_LEAKS" ]; then
        echo "⚠️ **MEDIUM:** Exported environment variables with sensitive names" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        echo "$ENV_LEAKS" | head -5 >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        ((MEDIUM_COUNT++))
    else
        echo "✅ No suspicious environment exports" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
fi

### PRE-COMMIT HOOK CHECK ###
if [ "$SCAN_TYPE" = "full" ]; then
    echo "## 🪝 Pre-Commit Hook Status" >> "$REPORT_FILE"
    echo "**Frequency:** One-time setup" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    if [ -f .git/hooks/pre-commit ]; then
        echo "✅ Pre-commit hook installed" >> "$REPORT_FILE"
    else
        echo "⚠️ **MEDIUM:** No pre-commit hook installed" >> "$REPORT_FILE"
        echo "Install: \`./install-hooks.sh --pre-commit .\`" >> "$REPORT_FILE"
        ((MEDIUM_COUNT++))
    fi
    
    echo "" >> "$REPORT_FILE"
fi

### SUMMARY ###
echo "---" >> "$REPORT_FILE"
echo "## Summary" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Severity | Count |" >> "$REPORT_FILE"
echo "|----------|-------|" >> "$REPORT_FILE"
echo "| CRITICAL | $CRITICAL_COUNT |" >> "$REPORT_FILE"
echo "| HIGH     | $HIGH_COUNT |" >> "$REPORT_FILE"
echo "| MEDIUM   | $MEDIUM_COUNT |" >> "$REPORT_FILE"
echo "| LOW      | $LOW_COUNT |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Update findings in state
jq ".findings.critical += $CRITICAL_COUNT | .findings.high += $HIGH_COUNT | .findings.medium += $MEDIUM_COUNT | .findings.low += $LOW_COUNT" "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# Display report
cat "$REPORT_FILE"

echo ""
echo "📄 Full report: $REPORT_FILE"
echo "📊 State file: $STATE_FILE"

# Exit codes
if [ $CRITICAL_COUNT -gt 0 ]; then
    echo ""
    echo "❌ CRITICAL ISSUES FOUND - PUSH BLOCKED"
    exit 1
elif [ $HIGH_COUNT -gt 0 ]; then
    echo ""
    echo "⚠️  HIGH SEVERITY ISSUES - REVIEW REQUIRED"
    exit 2
fi

echo ""
echo "✅ Security audit passed"
exit 0
