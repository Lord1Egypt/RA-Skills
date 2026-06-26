#!/bin/bash
set -e

# Setup a test git repo
WORK_DIR="/tmp/test_1058_guardrail_$$"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"
git init
echo "test" > test.txt
git add test.txt
git config user.email "test@example.com"
git config user.name "Test User"
git commit -m "initial commit"

touch dummy_prd.md

# Copy leio-sdlc to a temp "production" directory
PROD_SKILL_DIR="/tmp/mock_skill_leio_sdlc_$$"
cp -r /root/.openclaw/workspace/projects/leio-sdlc "$PROD_SKILL_DIR"

# Script path
ORCHESTRATOR="$PROD_SKILL_DIR/scripts/orchestrator.py"

export SDLC_TEST_MODE=true

echo "--- Scenario 1: With --enable-exec-from-workspace (Warning only) ---"
# We run it with --test-sleep so it exits quickly
OUTPUT1=$(python3 "$ORCHESTRATOR" --workdir "$WORK_DIR" --prd-file dummy_prd.md --force-replan false --channel test --test-sleep --enable-exec-from-workspace 2>&1 || true)

if echo "$OUTPUT1" | grep -q "\[WARNING\] Running Orchestrator in TEST MODE with mocked LLMs. Production safety checks are bypassed."; then
    echo "Scenario 1 passed: Warning detected."
else
    echo "Scenario 1 failed: Output:"
    echo "$OUTPUT1"
    exit 1
fi

if echo "$OUTPUT1" | grep -q "Production runtime detected but SDLC_TEST_MODE is enabled"; then
    echo "Scenario 1 failed: Fatal prompt detected when it shouldn't be."
    exit 1
fi

echo "--- Scenario 2: Without --enable-exec-from-workspace (Fatal) ---"
set +e
OUTPUT2=$(python3 "$ORCHESTRATOR" --workdir "$WORK_DIR" --prd-file dummy_prd.md --force-replan false --channel test --test-sleep 2>&1)
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -eq 1 ]; then
    echo "Scenario 2 correctly exited with code 1."
else
    echo "Scenario 2 failed to exit with code 1. Exit code: $EXIT_CODE"
    exit 1
fi

if echo "$OUTPUT2" | grep -q "Production runtime detected but SDLC_TEST_MODE is enabled"; then
    echo "Scenario 2 passed: Fatal prompt detected."
else
    echo "Scenario 2 failed: Fatal prompt missing. Output:"
    echo "$OUTPUT2"
    exit 1
fi

# Clean up
rm -rf "$WORK_DIR"
rm -rf "$PROD_SKILL_DIR"

echo "All tests passed successfully."
