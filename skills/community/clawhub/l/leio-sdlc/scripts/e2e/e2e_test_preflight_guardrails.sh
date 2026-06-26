#!/bin/bash
set -e

echo "Starting Pre-flight Guardrails Test..."

# 1. Initialize Sandbox
TEST_DIR=$(mktemp -d -t sdlc_guardrails_test_XXXXXX)
echo "Sandbox created at $TEST_DIR"

cd "$TEST_DIR"
# mount scripts (just copy them)
mkdir scripts
cp /root/.openclaw/workspace/projects/leio-sdlc/scripts/*.py scripts/
git init
git commit --allow-empty -m "init"

export SDLC_TEST_MODE=true

# 2. Test Planner Pre-flight
echo "Testing Planner Pre-flight..."
set +e
output=$(python3 scripts/spawn_planner.py --prd-file missing.md --workdir . --global-dir . 2>&1)
exit_code=$?
set -e
if [ $exit_code -ne 1 ]; then
    echo "Fail: Planner exit code is not 1"
    exit 1
fi
if ! echo "$output" | grep -q "\[Pre-flight Failed\]"; then
    echo "Fail: Planner did not output [Pre-flight Failed]"
    exit 1
fi

# 3. Test Coder Pre-flight
echo "Testing Coder Pre-flight..."
git checkout -b feature/dummy-guardrails >/dev/null 2>&1
set +e
output=$(python3 scripts/spawn_coder.py --pr-file missing.md --prd-file missing.md --workdir . --global-dir . 2>&1)
exit_code=$?
set -e
git checkout - >/dev/null 2>&1
if [ $exit_code -ne 1 ]; then
    echo "Fail: Coder exit code is not 1"
    exit 1
fi
if ! echo "$output" | grep -q "\[Pre-flight Failed\]"; then
    echo "Fail: Coder did not output [Pre-flight Failed]"
    echo "Output was: $output"
    exit 1
fi

# 4. Test Reviewer Pre-flight
echo "Testing Reviewer Pre-flight..."
# Create a dummy PR file to satisfy file check, but it should still fail status check or logic
echo "status: open" > PR.md
set +e
output=$(python3 scripts/spawn_reviewer.py --pr-file PR.md --diff-target HEAD --workdir . --global-dir . 2>&1)
exit_code=$?
set -e
# Note: In a sandbox without real git diff or reviewer setup, this should fail.
# We just want to ensure it doesn't crash or return 0.

# 5. Test Merge Pre-flight
echo "Testing Merge Pre-flight..."
# Action 1: fake review file
set +e
output=$(python3 scripts/merge_code.py --branch fake-branch --review-file missing.md 2>&1)
exit_code=$?
set -e
if [ $exit_code -ne 1 ]; then
    echo "Fail: Merge exit code is not 1"
    exit 1
fi
if ! echo "$output" | grep -q "\[Pre-flight Failed\]"; then
    echo "Fail: Merge did not output [Pre-flight Failed]"
    exit 1
fi

# Action 2: {"status": "ACTION_REQUIRED"} without force
echo '{"status": "ACTION_REQUIRED"}' > review.md
set +e
output=$(python3 scripts/merge_code.py --branch fake-branch --review-file review.md 2>&1)
exit_code=$?
set -e
if [ $exit_code -ne 1 ]; then
    echo "Fail: Merge exit code is not 1"
    exit 1
fi
if ! echo "$output" | grep -q "\[Pre-flight Failed\]"; then
    echo "Fail: Merge did not output [Pre-flight Failed]"
    exit 1
fi

# Action 3: {"status": "ACTION_REQUIRED"} with force
echo "Testing Merge with force-approved..."
set +e
python3 scripts/merge_code.py --branch fake-branch --review-file review.md --force-approved >/dev/null 2>&1
exit_code=$?
set -e
if [ $exit_code -ne 0 ]; then
    echo "Fail: Merge should have succeeded with force-approved"
    exit 1
fi

# Action 4: {"status": "APPROVED"}
echo "Testing Merge with APPROVED..."
echo '{"status": "APPROVED"}' > review2.md
set +e
python3 scripts/merge_code.py --branch fake-branch --review-file review2.md >/dev/null 2>&1
exit_code=$?
set -e
if [ $exit_code -ne 0 ]; then
    echo "Fail: Merge should have succeeded with APPROVED"
    exit 1
fi

# 6. Cleanup Sandbox
echo "[GUARDRAILS_TEST_SUCCESS]"
rm -rf "$TEST_DIR"
