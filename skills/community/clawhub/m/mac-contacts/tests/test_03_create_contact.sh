#!/bin/bash
# Test: Create Contact

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

echo "--- Running Test: Create Contact ---"
echo ""

# Test 1: Create contact with all fields
echo "Test 1: Create 'Test User123'"
OUT=$(python3 "$CLI" create \
    --first-name "Test" \
    --last-name "User123" \
    --organization "Test Company" \
    --email "test.user@example.com" \
    --phone "555-000-0000" \
    --city "Springfield" \
    --state "IL" \
    --country "United States" \
    --birthday "1990-07-04" \
    --url "https://fixture.example.com" 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "create exited with code 0"
else
    fail "create exited with code $EXIT_CODE"
    die "Contact creation failed — downstream tests 04–08 require this contact."
fi

if echo "$OUT" | grep -q "Success:"; then
    pass "Output contains 'Success:'"
else
    fail "Output does not contain 'Success:'"
    die "Contact creation appears to have failed — downstream tests 04–08 require this contact."
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
