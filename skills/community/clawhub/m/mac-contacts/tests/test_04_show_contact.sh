#!/bin/bash
# Test: Show Contact — all fields, no list membership yet

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

NAME="Test User123"

echo "--- Running Test: Show Contact ---"
echo ""

echo "Test 1: show '$NAME'"
OUT=$(python3 "$CLI" show "$NAME" 2>&1)
EXIT_CODE=$?
echo "Command output:"
echo "$OUT"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    pass "show exited with code 0"
else
    fail "show exited with code $EXIT_CODE"
    die "show failed — cannot validate fields."
fi

# Core identity fields
echo "$OUT" | grep -q "Test"                  && pass "Given name present"              || fail "Given name missing"
echo "$OUT" | grep -q "User123"               && pass "Family name present"             || fail "Family name missing"
echo "$OUT" | grep -q "Test Company"          && pass "Organization present"            || fail "Organization missing"

# Contact data
echo "$OUT" | grep -q "test.user@example.com" && pass "Email present"                  || fail "Email missing"
echo "$OUT" | grep -q "555-000-0000"          && pass "Phone present"                  || fail "Phone missing"

# Address (created in test_03 with --city Springfield --country "United States")
echo "$OUT" | grep -q "Springfield"           && pass "City present in address"         || fail "City missing from address"
echo "$OUT" | grep -q "United States"         && pass "Country present in address"      || fail "Country missing from address"

# Birthday and URL (set in test_03)
echo "$OUT" | grep -q "1990-07-04"            && pass "Birthday present"                || fail "Birthday missing"
echo "$OUT" | grep -q "fixture.example.com"   && pass "URL present"                    || fail "URL missing"

# show by --id
CONTACT_ID=$(echo "$OUT" | grep '^id:' | awk '{print $2}')
if [ -n "$CONTACT_ID" ]; then
    ID_OUT=$(python3 "$CLI" show --id "$CONTACT_ID" 2>&1)
    if [ $? -eq 0 ]; then
        pass "show --id exited with code 0"
    else
        fail "show --id exited with non-zero"
    fi
    echo "$ID_OUT" | grep -q "User123" && pass "show --id returns correct contact" || fail "show --id returned wrong contact"
else
    fail "Could not extract contact ID for show --id test"
fi

# No list membership yet (added in test_05)
if echo "$OUT" | grep -q "^lists:"; then
    fail "Lists section should not appear before test_05 runs"
else
    pass "No Lists section (correct — contact not in any list yet)"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
