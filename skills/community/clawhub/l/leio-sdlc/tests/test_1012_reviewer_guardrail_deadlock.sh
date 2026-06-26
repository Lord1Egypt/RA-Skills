#!/bin/bash
set -e

WORK_DIR="/tmp/test_1012_workspace_$$"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

git init
git config user.name "Test User"
git config user.email "test@example.com"

echo "status: in_progress" > PR_001.md
echo "scripts/spawn_reviewer.py" > .sdlc_guardrail
mkdir scripts
echo "original code" > scripts/spawn_reviewer.py
git add PR_001.md .sdlc_guardrail scripts/spawn_reviewer.py
git commit -m "Initial commit"

echo "modified code in master" > scripts/spawn_reviewer.py
git commit -am "Modify protected file on master"

git checkout -b feature/pr-001

echo "new benign code" > benign_file.py
git add benign_file.py
git commit -m "feat: benign feature"

export SDLC_TEST_MODE="true"
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py --pr-file PR_001.md --diff-target master --workdir "$WORK_DIR" --global-dir "$WORK_DIR" > output.log

if grep -q "\[EMPTY DIFF\]" current_review.diff; then
    echo "FAILED: Test 1 - current_review.diff is empty."
    exit 1
fi
if ! grep -q "new benign code" current_review.diff; then
    echo "FAILED: Test 1 - Committed changes not visible."
    exit 1
fi
echo "PASSED: Test 1 - Committed Changes Visibility Test"

if grep -iq "guardrail violation" output.log; then
    echo "FAILED: Test 2 - Guardrail incorrectly flagged historical changes."
    exit 1
fi
echo "PASSED: Test 2 - Historical Immunity Test"

echo "tampered code" > scripts/spawn_reviewer.py
git commit -am "Malicious tamper"

python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py --pr-file PR_001.md --diff-target master --workdir "$WORK_DIR" --global-dir "$WORK_DIR" > output.log || true

if ! grep -iq "guardrail violation" output.log; then
    echo "FAILED: Test 3 - Did not detect active tamper."
    exit 1
fi
echo "PASSED: Test 3 - Active Tamper Test"

rm -rf "$WORK_DIR"
echo "All tests passed!"
