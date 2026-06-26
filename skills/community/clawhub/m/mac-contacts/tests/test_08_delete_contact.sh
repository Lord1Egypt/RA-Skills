#!/bin/bash
# Test: Delete Contact

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

NAME="Test User123"

echo "--- Running Test: Delete Contact ---"
echo ""

# Test 1: delete command
echo "Test 1: delete '$NAME' --force"
OUT=$(python3 "$CLI" delete "$NAME" --force 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "delete exited with code 0"
else
    fail "delete exited with code $EXIT_CODE"
fi

if echo "$OUT" | grep -q "Success:"; then
    pass "Output contains 'Success:'"
else
    fail "Output does not contain 'Success:'"
fi

# Test 2: show should now fail (contact gone)
echo "Test 2: show '$NAME' (expect non-zero — contact should be deleted)"
SHOW_OUT=$(python3 "$CLI" show "$NAME" 2>&1)
SHOW_EXIT=$?
echo "Command output:"
echo "$SHOW_OUT"
echo ""

if [ $SHOW_EXIT -ne 0 ]; then
    pass "show returned non-zero exit (contact confirmed deleted)"
else
    fail "show returned exit 0 — contact still exists after delete"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
