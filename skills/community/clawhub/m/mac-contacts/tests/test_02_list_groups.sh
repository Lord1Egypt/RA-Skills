#!/bin/bash
# Test: List Groups

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

echo "--- Running Test: List Groups ---"
echo ""

# Test 1: Command exits successfully
echo "Test 1: Run list_groups"
OUT=$(python3 "$CLI" list_groups 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "list_groups exited with code 0"
else
    fail "list_groups exited with code $EXIT_CODE"
fi

# Test 2: Output format is recognizable
if echo "$OUT" | grep -qE "^- .+"; then
    pass "Output is a YAML list of groups"
elif echo "$OUT" | grep -q "No lists found."; then
    pass "Output contains 'No lists found.' (zero groups is valid)"
else
    fail "Output format unrecognized — expected a YAML list of group names or 'No lists found.'"
    echo "Raw output was:"
    echo "$OUT"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
