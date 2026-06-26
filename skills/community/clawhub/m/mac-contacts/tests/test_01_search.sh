#!/bin/bash
# Test: Search Contacts (self-contained, covers all search modes)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/mac-contacts.py"

TESTS_RUN=0; TESTS_PASSED=0; TESTS_FAILED=0
pass() { echo "[PASS] $1"; TESTS_PASSED=$((TESTS_PASSED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
fail() { echo "[FAIL] $1"; TESTS_FAILED=$((TESTS_FAILED+1)); TESTS_RUN=$((TESTS_RUN+1)); }
die()  { echo "[FATAL] $1"; exit 1; }

FIRST="SearchTest"
LAST="Qxz9Fixture"
EMAIL="searchtest.qxz9@example.com"
PHONE="555-111-2222"
CITY="Testville"
COUNTRY="Testlandia"

cleanup() {
    python3 "$CLI" delete "$FIRST $LAST" --force >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "--- Running Test: Search Contacts ---"
echo ""

# Setup: create fixture with all searchable fields
echo "Setup: creating fixture contact..."
SETUP=$(python3 "$CLI" create \
    --first-name "$FIRST" \
    --last-name  "$LAST" \
    --organization "SearchOrg9" \
    --email "$EMAIL" \
    --phone "$PHONE" \
    --city "$CITY" \
    --country "$COUNTRY" 2>&1)
echo "$SETUP"
echo "$SETUP" | grep -q "Success:" || die "Fixture create failed — cannot run search tests."

# --- Comprehensive (auto) search ---

echo ""
echo "Test 1: Comprehensive search by given name"
OUT=$(python3 "$CLI" search "$FIRST" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$FIRST" && pass "Found by given name" || fail "Not found by given name"

echo ""
echo "Test 2: Comprehensive search by family name"
OUT=$(python3 "$CLI" search "$LAST" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found by family name" || fail "Not found by family name"

echo ""
echo "Test 3: Comprehensive search by email (auto-detect)"
OUT=$(python3 "$CLI" search "$EMAIL" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found by email (comprehensive)" || fail "Not found by email (comprehensive)"

echo ""
echo "Test 4: Comprehensive search by phone digits (auto-detect)"
OUT=$(python3 "$CLI" search "5551112222" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found by phone digits (comprehensive)" || fail "Not found by phone digits (comprehensive)"

echo ""
echo "Test 5: Comprehensive search by city (auto-detect)"
OUT=$(python3 "$CLI" search "$CITY" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found by city (comprehensive)" || fail "Not found by city (comprehensive)"

# --- Explicit flag searches ---

echo ""
echo "Test 6: --email flag"
OUT=$(python3 "$CLI" search --email "$EMAIL" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found via --email flag" || fail "Not found via --email flag"

echo ""
echo "Test 7: --phone flag (partial digits)"
OUT=$(python3 "$CLI" search --phone "111-2222" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found via --phone flag" || fail "Not found via --phone flag"

echo ""
echo "Test 8: --city flag"
OUT=$(python3 "$CLI" search --city "$CITY" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found via --city flag" || fail "Not found via --city flag"

echo ""
echo "Test 9: --country flag"
OUT=$(python3 "$CLI" search --country "$COUNTRY" 2>&1); echo "$OUT"
echo "$OUT" | grep -q "$LAST" && pass "Found via --country flag" || fail "Not found via --country flag"

# --- --id flag search ---

echo ""
echo "Test 10: --id flag"
SHOW_OUT=$(python3 "$CLI" show "$FIRST $LAST" 2>&1)
CONTACT_ID=$(echo "$SHOW_OUT" | grep '^id:' | awk '{print $2}')
if [ -z "$CONTACT_ID" ]; then
    fail "Could not extract contact ID for --id test"
else
    OUT=$(python3 "$CLI" search --id "$CONTACT_ID" 2>&1); echo "$OUT"
    echo "$OUT" | grep -q "$LAST" && pass "Found via --id flag" || fail "Not found via --id flag"
fi

# Cleanup and verify deletion
echo ""
echo "Cleanup: deleting fixture contact..."
python3 "$CLI" delete "$FIRST $LAST" --force 2>&1
trap - EXIT

echo ""
echo "Test 11: Deleted contact no longer found"
OUT=$(python3 "$CLI" search "$LAST" 2>&1); echo "$OUT"
if [ $? -ne 0 ] || echo "$OUT" | grep -qi "no contacts\|not found"; then
    pass "Deleted contact not found"
else
    fail "Deleted contact still appears in search"
fi

echo ""
echo "Results: $TESTS_PASSED/$TESTS_RUN passed"
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
