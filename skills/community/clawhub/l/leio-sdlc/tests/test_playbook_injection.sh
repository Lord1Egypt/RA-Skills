#!/bin/bash
set -e

echo "Testing spawn_reviewer.py and spawn_planner.py prompt injections..."

# Use a non-problematic directory name
TEST_DIR="/tmp/sdlc_test_injection_$$"
mkdir -p "$TEST_DIR"
trap 'rm -rf "$TEST_DIR"' EXIT

cd "$TEST_DIR"
git init -b master
git config user.email "test@openclaw.ai"
git config user.name "TDD Tester"
echo "init" > README.md
git add README.md
git commit -m "initial commit"
git checkout -b feature/test

echo "status: in_progress" > PR.md
echo "Test PRD" > PRD.md

export SDLC_TEST_MODE=true

# Test Reviewer
echo "Running spawn_reviewer.py..."
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py \
    --pr-file PR.md \
    --diff-target HEAD \
    --workdir "$TEST_DIR"

if grep -q "REVIEWER PLAYBOOK" tests/tool_calls.log; then
    echo "PASS: Reviewer playbook injected."
else
    echo "FAIL: Reviewer playbook missing."
    exit 1
fi

if grep -q "forbidden from manually editing the markdown file's status field" tests/tool_calls.log; then
    echo "PASS: Status edit forbidden string present for Reviewer."
else
    echo "FAIL: Status edit forbidden string missing for Reviewer."
    exit 1
fi

# Test Planner
echo "Running spawn_planner.py..."
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_planner.py \
    --prd-file PRD.md \
    --workdir "$TEST_DIR"

if grep -q "PLANNER PLAYBOOK" tests/task_string.log; then
    echo "PASS: Planner playbook injected."
else
    echo "FAIL: Planner playbook missing."
    exit 1
fi

if grep -q "forbidden from manually editing the markdown file's status field" tests/task_string.log; then
    echo "PASS: Status edit forbidden string present for Planner."
else
    echo "FAIL: Status edit forbidden string missing for Planner."
    exit 1
fi

echo "All tests passed."
exit 0
