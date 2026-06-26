#!/bin/bash
# ==========================================
# STANDARD AGENTIC PREFLIGHT SCRIPT TEMPLATE
# ==========================================
# Rule: Token-Optimized CI (Silent on Success, Verbose on Failure)

PROJECT_DIR=$(dirname "$0")
TMP_TEST_LOG=$(mktemp)

RUN_E2E=0
if [[ "$1" == "--e2e-test" ]]; then
    RUN_E2E=1
fi

echo "[$(date '+%H:%M:%S')] Starting Smart Preflight Checks..."

# ISSUE-1088: Prune legacy test sandboxes
rm -rf tests/planner_sandbox_* tests/manager_sandbox_* 2>/dev/null || true

cd "$PROJECT_DIR" || exit 1
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

cleanup() {
    rm -f "$TMP_TEST_LOG"
}
trap cleanup EXIT

TOTAL_PASSED=0

run_test() {
    local cmd="$1"
    local desc="$2"
    
    if ! eval "$cmd" > "$TMP_TEST_LOG" 2>&1; then
        echo "❌ PREFLIGHT FAILED: $desc"
        echo "=== ERROR DETAILS (Extracting relevant logs to save tokens) ==="
        if grep -iE -A 10 -B 2 "error:|exception|failed|unresolved|expecting|traceback|❌" "$TMP_TEST_LOG" | head -n 50; then
            :
        else
            tail -n 50 "$TMP_TEST_LOG"
        fi
        echo "==============================================================="
        exit 1
    fi
    ((TOTAL_PASSED++))
}

run_e2e_test() {
    local cmd="$1"
    local desc="$2"
    
    if ! eval "$cmd" > /dev/null 2>&1; then
        echo "[E2E WARNING] $desc failed. Continuing."
    else
        ((TOTAL_PASSED++))
    fi
}

shopt -s nullglob

# 1. Bash Tests Discovery
for f in scripts/test_*.sh; do
    run_test "bash $f" "Bash Test: $f"
done

# 2. Python Tests Discovery
if [ -d "tests" ]; then
    test_files=(tests/test_*.py)
    if [ ${#test_files[@]} -gt 0 ]; then
        run_test "python3 -m unittest discover -s tests -p \"test_*.py\"" "Python Unittest tests/"
    fi
fi

for f in scripts/test_*.py; do
    run_test "python3 $f" "Python Test: $f"
done

# 3. Node.js Tests Discovery
if [ -f "package.json" ] && grep -q '"test"' package.json; then
    run_test "npm test" "NPM Test"
else
    for f in scripts/test_*.js; do
        run_test "node $f" "Node.js Test: $f"
    done
fi

# 4. E2E Tests
if [ $RUN_E2E -eq 1 ]; then
    for f in scripts/e2e/e2e_test_*.sh; do
        run_e2e_test "bash $f" "$(basename "$f")"
    done
fi

# Offline Syntax Checks
if [ -f "scripts/agent_driver.py" ]; then
    run_test "python3 -m py_compile scripts/agent_driver.py" "Syntax Check: agent_driver.py"
fi

echo "✅ $TOTAL_PASSED tests/test-suites passed."
exit 0
