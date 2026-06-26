#!/usr/bin/env bash
# nix-memory: Session continuity scoring
# Runs all checks and produces a single continuity score (0-100).
# Designed to run at session start or on heartbeat.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -d "$STATE_DIR" ]]; then
    echo "nix-memory not initialized. Running setup..."
    bash "$SCRIPT_DIR/setup.sh"
    echo ""
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SCORE=100
ISSUES=""

echo "=== nix-memory Continuity Check: ${NOW} ==="
echo ""

# 1. Identity verification
echo "--- Step 1: Identity Hash ---"
IDENTITY_RESULT=$(bash "$SCRIPT_DIR/identity-hash.sh" 2>&1) || true
if echo "$IDENTITY_RESULT" | grep -q "IDENTITY_OK"; then
    echo "  PASS"
elif echo "$IDENTITY_RESULT" | grep -q "IDENTITY_DRIFT"; then
    DRIFTED=$(echo "$IDENTITY_RESULT" | grep "file(s) changed" | grep -o "[0-9]*" | head -1 || echo 1)
    SCORE=$((SCORE - DRIFTED * 15))
    ISSUES="${ISSUES}  - Identity drift: ${DRIFTED} file(s) changed\n"
    echo "  DRIFT DETECTED"
else
    echo "  SKIPPED (not initialized)"
fi
echo ""

# 2. Memory integrity
echo "--- Step 2: Memory Integrity ---"
MEMORY_RESULT=$(bash "$SCRIPT_DIR/memory-verify.sh" 2>&1) || true
if echo "$MEMORY_RESULT" | grep -q "MEMORY_OK"; then
    echo "  PASS"
elif echo "$MEMORY_RESULT" | grep -q "MEMORY_CHANGED"; then
    CHANGED=$(echo "$MEMORY_RESULT" | grep "file(s) modified" | grep -o "[0-9]*" | head -1 || echo 1)
    SCORE=$((SCORE - CHANGED * 5))
    ISSUES="${ISSUES}  - Memory files changed: ${CHANGED}\n"
    echo "  CHANGES DETECTED"
else
    echo "  SKIPPED"
fi
echo ""

# 3. Drift analysis
echo "--- Step 3: Drift Detection ---"
DRIFT_RESULT=$(bash "$SCRIPT_DIR/drift-detect.sh" 2>&1) || true
DRIFT_SCORE=$(echo "$DRIFT_RESULT" | grep "DRIFT SCORE:" | grep -o "[0-9]*/100" | cut -d/ -f1 || echo "")
if [[ -n "$DRIFT_SCORE" ]]; then
    echo "  Drift score: ${DRIFT_SCORE}/100"
    # Weight drift score into overall (30% weight)
    DRIFT_PENALTY=$(( (100 - DRIFT_SCORE) * 30 / 100 ))
    SCORE=$((SCORE - DRIFT_PENALTY))
else
    echo "  SKIPPED"
fi
echo ""

# 4. Daily log freshness
echo "--- Step 4: Daily Log Check ---"
TODAY=$(date +%Y-%m-%d)
TODAY_LOG="${WORKSPACE}/memory/${TODAY}.md"
if [[ -f "$TODAY_LOG" ]]; then
    SIZE=$(wc -c < "$TODAY_LOG")
    echo "  Today's log exists (${SIZE} bytes) - PASS"
else
    SCORE=$((SCORE - 10))
    ISSUES="${ISSUES}  - No daily log for today (${TODAY})\n"
    echo "  No log for today - FAIL"
fi
echo ""

# 5. SOUL.md existence
echo "--- Step 5: Soul Check ---"
if [[ -f "${WORKSPACE}/SOUL.md" ]]; then
    SOUL_SIZE=$(wc -c < "${WORKSPACE}/SOUL.md")
    echo "  SOUL.md present (${SOUL_SIZE} bytes) - PASS"
else
    SCORE=$((SCORE - 25))
    ISSUES="${ISSUES}  - SOUL.md MISSING\n"
    echo "  SOUL.md MISSING - CRITICAL"
fi
echo ""

# Clamp score
[[ $SCORE -lt 0 ]] && SCORE=0
[[ $SCORE -gt 100 ]] && SCORE=100

# Grade
if [[ $SCORE -ge 90 ]]; then
    GRADE="EXCELLENT"
elif [[ $SCORE -ge 75 ]]; then
    GRADE="GOOD"
elif [[ $SCORE -ge 50 ]]; then
    GRADE="FAIR"
elif [[ $SCORE -ge 25 ]]; then
    GRADE="POOR"
else
    GRADE="CRITICAL"
fi

echo "=========================================="
echo "  CONTINUITY SCORE: ${SCORE}/100 (${GRADE})"
echo "=========================================="

if [[ -n "$ISSUES" ]]; then
    echo ""
    echo "Issues found:"
    echo -e "$ISSUES"
fi

# Save report
REPORT_FILE="${STATE_DIR}/sessions/continuity-${TODAY}.json"
cat > "$REPORT_FILE" << EOF
{
    "timestamp": "${NOW}",
    "score": ${SCORE},
    "grade": "${GRADE}",
    "drift_score": ${DRIFT_SCORE:-0},
    "soul_present": $([ -f "${WORKSPACE}/SOUL.md" ] && echo true || echo false),
    "daily_log_present": $([ -f "$TODAY_LOG" ] && echo true || echo false),
    "issues": "$(echo -e "${ISSUES}" | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF

echo ""
echo "Report saved: ${REPORT_FILE}"
