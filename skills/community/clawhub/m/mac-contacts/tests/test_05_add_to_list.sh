#!/bin/bash
# Test: Add Contact to List

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

NAME="Test User123"
LIST="Test List Abc789"

echo "--- Running Test: Add Contact to List ---"
echo ""

# Test 1: add_to_list command
echo "Test 1: add_to_list '$NAME' '$LIST'"
OUT=$(python3 "$CLI" add_to_list "$NAME" "$LIST" 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "add_to_list exited with code 0"
else
    fail "add_to_list exited with code $EXIT_CODE"
fi

if echo "$OUT" | grep -q "Success:"; then
    pass "Output contains 'Success:'"
else
    fail "Output does not contain 'Success:'"
fi

# Test 2: search --list confirms membership
echo "Test 2: search --list '$LIST'"
SEARCH_OUT=$(python3 "$CLI" search --list "$LIST" 2>&1)
SEARCH_EXIT=$?
echo "Command output:"
echo "$SEARCH_OUT"
echo ""

if [ $SEARCH_EXIT -eq 0 ]; then
    pass "search --list exited with code 0"
else
    fail "search --list exited with code $SEARCH_EXIT"
fi

if echo "$SEARCH_OUT" | grep -q "User123"; then
    pass "Contact 'User123' found in list search"
else
    fail "Contact 'User123' NOT found in list search"
fi

# Test 3: list_groups confirms group exists
echo "Test 3: list_groups contains '$LIST'"
GROUPS_OUT=$(python3 "$CLI" list_groups 2>&1)
echo "Command output:"
echo "$GROUPS_OUT"
echo ""

if echo "$GROUPS_OUT" | grep -q "Test List Abc789"; then
    pass "list_groups output contains '$LIST'"
else
    fail "list_groups output does not contain '$LIST'"
fi

# Test 4: show confirms list membership
echo "Test 4: show '$NAME' — verify Lists section appears"
SHOW_OUT=$(python3 "$CLI" show "$NAME" 2>&1)
echo "Command output:"
echo "$SHOW_OUT"
echo ""

if echo "$SHOW_OUT" | grep -q "^lists:"; then
    pass "show output contains 'lists:' section"
else
    fail "show output missing 'lists:' section"
fi

if echo "$SHOW_OUT" | grep -q "Test List Abc789"; then
    pass "show output names the list '$LIST'"
else
    fail "show output does not name '$LIST'"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
