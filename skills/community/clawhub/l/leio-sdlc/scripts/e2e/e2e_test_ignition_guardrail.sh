#!/bin/bash
set -e

# test_ignition_guardrail.sh - Verify that the orchestrator enforces the Initial Handshake

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

git init > /dev/null 2>&1
git config user.name "E2E Test"
git config user.email "e2e@example.com"
echo "init" > init.txt
echo ".sdlc_repo.lock" > .gitignore
echo "*.log" >> .gitignore
git add init.txt .gitignore
git commit -m "init" > /dev/null 2>&1

mkdir -p docs/PRDs docs/PRs/dummy
cat << 'EOF' > docs/PRDs/dummy.md
# dummy
EOF
cat << 'EOF' > docs/PRs/dummy/PR_001.md
status: open
slice_depth: 0
EOF
git add docs
git commit -m "add PRD" > /dev/null 2>&1

echo "Running Ignition Failure Test..."
# Mock the orchestrator failure
output=$(SDLC_TEST_MODE=true python3 "${PROJECT_ROOT}/scripts/orchestrator.py" --enable-exec-from-workspace --workdir "$(pwd)" --prd-file docs/PRDs/dummy.md --channel "invalid:id" --max-prs-to-process 1 --coder-session-strategy always 2>&1 || true)

if ! echo "$output" | grep -q "Invalid notification channel format"; then
    echo "Fail: Orchestrator did not fail correctly on invalid channel."
    echo "Output: $output"
    exit 1
fi

echo "Running Ignition Success Test..."

# We need a background process that we can kill after handshake because
# if we run the orchestrator it will actually execute the PR logic.
SDLC_TEST_MODE=true python3 "${PROJECT_ROOT}/scripts/orchestrator.py" --enable-exec-from-workspace --workdir "$(pwd)" --prd-file docs/PRDs/dummy.md --channel "valid:id" --max-prs-to-process 1 --coder-session-strategy always > ../success_test.log 2>&1 &
ORCH_PID=$!

# Wait for handshake
MAX_WAIT=10
COUNT=0
FOUND=0
while [ $COUNT -lt $MAX_WAIT ]; do
    if grep -q "Initial Handshake successful" ../success_test.log; then
        FOUND=1
        break
    fi
    sleep 1
    COUNT=$((COUNT+1))
done

kill $ORCH_PID || true

if [ $FOUND -eq 0 ]; then
    echo "Fail: Orchestrator did not send handshake message"
    cat ../success_test.log
    rm -f ../success_test.log
    exit 1
fi

echo "✅ All Ignition Guardrail tests passed."
rm -rf "$TEST_DIR" ../success_test.log
exit 0