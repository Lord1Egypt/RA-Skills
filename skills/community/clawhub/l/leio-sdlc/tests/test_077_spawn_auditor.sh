#!/usr/bin/env bash
set -e

echo "================================================="
echo "Testing: Auditor Spawn and Playbook Injection"
echo "================================================="

export SDLC_TEST_MODE=true
WORK_DIR=$(mktemp -d)
cp -r /root/.openclaw/workspace/projects/leio-sdlc/* "$WORK_DIR/"
cd "$WORK_DIR"

mkdir -p docs/PRDs
echo "dummy PRD content" > docs/PRDs/dummy.md

# Test 1: Approved
echo "Running Test Scenario 1 (Approved)..."
export MOCK_AUDIT_RESULT="APPROVE"
OUTPUT=$(python3 scripts/spawn_auditor.py --prd-file docs/PRDs/dummy.md --workdir .)

if ! echo "$OUTPUT" | grep -q '"status": "APPROVED"'; then
    echo "❌ Scenario 1 Failed: Expected APPROVED JSON output."
    exit 1
fi

if ! grep -q "Read your strict auditing guidelines from" tests/auditor_task_string.log; then
    echo "❌ Scenario 1 Failed: Task string missing playbook instruction."
    cat tests/auditor_task_string.log
    exit 1
fi
echo "✅ Scenario 1 Passed."

# Test 2: Rejected
echo "Running Test Scenario 2 (Rejected)..."
export MOCK_AUDIT_RESULT="REJECT"
OUTPUT=$(python3 scripts/spawn_auditor.py --prd-file docs/PRDs/dummy.md --workdir .)

if ! echo "$OUTPUT" | grep -q '"status": "REJECTED"'; then
    echo "❌ Scenario 2 Failed: Expected REJECTED JSON output."
    exit 1
fi
echo "✅ Scenario 2 Passed."

rm -rf "$WORK_DIR"
echo "✅ test_077_spawn_auditor.sh passed."
exit 0
