#!/bin/bash
# test_hook_logic.sh: Standalone test for the pre-commit hook logic.

# Create a temporary environment to test the hook script
TEST_HOOK="./scripts/pre-commit-payload.sh"

if [ ! -f "$TEST_HOOK" ]; then
    echo "ERROR: Test hook not found."
    exit 1
fi

chmod +x "$TEST_HOOK"

echo "Running Standalone Pre-commit Hook Tests..."

# Test 1: Variable Missing (Should FAIL)
echo "--------------------------------------"
echo "Test 1: Variable Missing (Expecting Failure)"
export SDLC_ORCHESTRATOR_RUNNING=0
OUTPUT=$($TEST_HOOK 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ] && [[ "$OUTPUT" == *"ERROR: SDLC Violation! Direct commits are forbidden. You must use orchestrator.py."* ]]; then
    echo "✅ PASS: Rejection successful with correct message."
else
    echo "❌ FAIL: Hook allowed commit or returned wrong message."
    echo "Output: $OUTPUT"
    echo "Exit Code: $EXIT_CODE"
    exit 1
fi

# Test 2: Variable Present (Should PASS)
echo "--------------------------------------"
echo "Test 2: Variable Present (Expecting Success)"
export SDLC_ORCHESTRATOR_RUNNING=1
$TEST_HOOK
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ PASS: Hook allowed commit."
else
    echo "❌ FAIL: Hook rejected authorized commit."
    exit 1
fi

# Test 3: Installation Script
echo "--------------------------------------"
echo "Test 3: Installation Script"
MOCK_GIT_DIR="/tmp/mock_git_$(date +%s)"
mkdir -p "$MOCK_GIT_DIR"

bash ./scripts/install_hook.sh "$MOCK_GIT_DIR"

if [ -x "$MOCK_GIT_DIR/hooks/pre-commit" ]; then
    echo "✅ PASS: Hook successfully installed and made executable."
else
    echo "❌ FAIL: Hook not found in $MOCK_GIT_DIR/hooks/pre-commit or not executable."
    rm -rf "$MOCK_GIT_DIR"
    exit 1
fi

rm -rf "$MOCK_GIT_DIR"

echo "--------------------------------------"
echo "✅ ALL HOOK TESTS PASSED!"
