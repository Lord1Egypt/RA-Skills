#!/usr/bin/env bash
# VibeSafe Starter — Quick Dependency Audit
# Usage: ./audit.sh [project_path]

set -euo pipefail
PROJECT="${1:-.}"
ISSUES=0

echo "🔒 VibeSafe Quick Audit"
echo "========================"
echo "Project: $(cd "$PROJECT" && pwd)"
echo ""

# npm
if [ -f "$PROJECT/package.json" ]; then
    echo "📦 npm audit..."
    cd "$PROJECT"
    npm install --package-lock-only --silent 2>/dev/null || true
    
    if npm audit --json 2>/dev/null > /tmp/vibe-npm-audit.json; then
        critical=$(python3 -c "import json; d=json.load(open('/tmp/vibe-npm-audit.json')); print(sum(1 for v in d.get('vulnerabilities',{}).values() if v.get('severity')=='critical'))" 2>/dev/null || echo "0")
        high=$(python3 -c "import json; d=json.load(open('/tmp/vibe-npm-audit.json')); print(sum(1 for v in d.get('vulnerabilities',{}).values() if v.get('severity')=='high'))" 2>/dev/null || echo "0")
        moderate=$(python3 -c "import json; d=json.load(open('/tmp/vibe-npm-audit.json')); print(sum(1 for v in d.get('vulnerabilities',{}).values() if v.get('severity')=='moderate'))" 2>/dev/null || echo "0")
        
        echo "   🔴 Critical: $critical"
        echo "   🟠 High:     $high"
        echo "   🟡 Moderate: $moderate"
        
        if [ "$critical" -gt 0 ]; then
            echo "   ⚠️  Critical vulnerabilities found! DO NOT DEPLOY."
            ISSUES=$((ISSUES + critical))
        fi
    else
        echo "   ✅ No issues (or audit unavailable)"
    fi
    echo ""
fi

# Python
if ls "$PROJECT"/requirements*.txt 2>/dev/null | head -1 >/dev/null; then
    echo "🐍 pip audit..."
    if command -v pip-audit &>/dev/null; then
        req_file=$(ls "$PROJECT"/requirements*.txt | head -1)
        pip-audit -r "$req_file" 2>&1 | tail -5
        if [ ${PIPESTATUS[0]} -ne 0 ]; then
            ISSUES=$((ISSUES + 1))
        fi
    else
        echo "   ⚠️  pip-audit not installed. Run: pip install pip-audit"
        echo "   Then re-run: ./audit.sh"
    fi
    echo ""
fi

# Secrets
echo "🔍 Secrets scan..."
if command -v gitleaks &>/dev/null; then
    gitleaks detect --source="$PROJECT" --no-git 2>/dev/null | head -5 || echo "   ✅ No secrets found"
else
    # Quick manual scan
    if grep -rq "sk-\|ghp_\|gho_\|xai-\|-----BEGIN.*PRIVATE KEY" "$PROJECT" --exclude-dir=.git --exclude-dir=node_modules 2>/dev/null; then
        echo "   ⚠️  Possible secrets found! Review manually."
        ISSUES=$((ISSUES + 1))
    else
        echo "   ✅ No obvious secrets"
    fi
fi

echo ""
echo "========================"
if [ "$ISSUES" -eq 0 ]; then
    echo "✅ CLEAN — safe to proceed"
    exit 0
else
    echo "⚠️  $ISSUES issue(s) found — review before deploying"
    exit 1
fi
