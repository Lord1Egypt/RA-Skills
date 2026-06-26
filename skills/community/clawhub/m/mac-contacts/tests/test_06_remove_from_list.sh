#!/bin/bash
# Test: Remove Contact from List

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

NAME="Test User123"
LIST="Test List Abc789"

echo "--- Running Test: Remove Contact from List ---"
echo ""

# Test 1: remove_from_list command
echo "Test 1: remove_from_list '$NAME' '$LIST'"
OUT=$(python3 "$CLI" remove_from_list "$NAME" "$LIST" 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "remove_from_list exited with code 0"
else
    fail "remove_from_list exited with code $EXIT_CODE"
fi

if echo "$OUT" | grep -q "Success:"; then
    pass "Output contains 'Success:'"
else
    fail "Output does not contain 'Success:'"
fi

# Test 2: search --list should now return no results (or exit non-zero)
echo "Test 2: search --list '$LIST' (expect empty/no results)"
SEARCH_OUT=$(python3 "$CLI" search --list "$LIST" 2>&1)
SEARCH_EXIT=$?
echo "Command output:"
echo "$SEARCH_OUT"
echo ""

if [ $SEARCH_EXIT -eq 0 ] && echo "$SEARCH_OUT" | grep -q "User123"; then
    fail "Contact 'User123' still appears in list — removal failed"
else
    pass "Contact 'User123' no longer in list (as expected)"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
