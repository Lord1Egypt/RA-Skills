#!/bin/bash
# Test Runner for mac-contacts skill
# Runs all tests in order and prints a final summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOTAL=0; PASSED=0; FAILED=0
FAILED_TESTS=()

run_test() {
    local file="$1"
    local name
    name="$(basename "$file")"
    echo ""
    echo "════════════════════════════════════════"
    echo "  $name"
    echo "════════════════════════════════════════"
    bash "$file"
    local exit_code=$?
    ((TOTAL++))
    if [ $exit_code -eq 0 ]; then
        ((PASSED++))
        echo "  → SUITE PASSED"
    else
        ((FAILED++))
        FAILED_TESTS+=("$name")
        echo "  → SUITE FAILED (exit $exit_code)"
    fi
}

for test_file in "$SCRIPT_DIR"/test_*.sh; do
    run_test "$test_file"
done

echo ""
echo "════════════════════════════════════════"
echo "  FINAL RESULTS: $PASSED/$TOTAL suites passed"
echo "════════════════════════════════════════"

if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo "  Failed suites:"
    for t in "${FAILED_TESTS[@]}"; do
        echo "    - $t"
    done
fi

[ $FAILED -eq 0 ] && exit 0 || exit 1
