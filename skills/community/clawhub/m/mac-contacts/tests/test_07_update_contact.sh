#!/bin/bash
# Test: Update Contact Data

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

NAME="Test User123"

echo "--- Running Test: Update Contact ---"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

# Test 1: Update contact — org, phone, birthday (replace), url (append)
echo ""
echo "Test 1: Update '$NAME'"
UPDATE_OUTPUT=$(python3 "$CLI" update "$NAME" \
    --organization "Updated Company" \
    --phone "999-888-7777" \
    --birthday "2000-01-15" \
    --url "https://updated.example.com" 2>&1)
EXIT_CODE=$?
echo "Update command output:"
echo "$UPDATE_OUTPUT"

if [ $EXIT_CODE -eq 0 ]; then
    pass "Update command exited with code 0"
else
    fail "Update command exited with code $EXIT_CODE"
    die "Update failed — cannot validate show output."
fi

if echo "$UPDATE_OUTPUT" | grep -q "Success:"; then
    pass "Update command output contains 'Success:'"
else
    fail "Update command output does not contain 'Success:'"
fi

# Test 2: Show updated contact and verify all changes
echo ""
echo "Test 2: Show updated contact"
SHOW_OUTPUT=$(python3 "$CLI" show "$NAME" 2>&1)
EXIT_CODE=$?
echo "Show command output:"
echo "$SHOW_OUTPUT"

if [ $EXIT_CODE -eq 0 ]; then
    pass "Show command exited with code 0"
else
    fail "Show command exited with code $EXIT_CODE"
    die "Show failed — cannot validate fields."
fi

# Organization updated
if echo "$SHOW_OUTPUT" | grep -q "Updated Company"; then
    pass "Show output contains updated organization"
else
    fail "Show output does not contain updated organization"
fi

# Phone appended
if echo "$SHOW_OUTPUT" | grep -q "999-888-7777"; then
    pass "Show output contains appended phone"
else
    fail "Show output does not contain appended phone"
fi

# Original email preserved
if echo "$SHOW_OUTPUT" | grep -q "test.user@example.com"; then
    pass "Original email preserved"
else
    fail "Original email missing"
fi

# Birthday replaced (new value present)
if echo "$SHOW_OUTPUT" | grep -q "2000-01-15"; then
    pass "Updated birthday present"
else
    fail "Updated birthday not found"
fi

# Birthday replaced (old value absent)
if echo "$SHOW_OUTPUT" | grep -q "1990-07-04"; then
    fail "Original birthday still present — should have been replaced"
else
    pass "Original birthday correctly replaced"
fi

# URL appended (new value present)
if echo "$SHOW_OUTPUT" | grep -q "updated.example.com"; then
    pass "Appended URL present"
else
    fail "Appended URL not found"
fi

# URL appended (original value preserved)
if echo "$SHOW_OUTPUT" | grep -q "fixture.example.com"; then
    pass "Original URL preserved (correct append behaviour)"
else
    fail "Original URL removed — should have been preserved"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
