#!/bin/bash
# test_runtime_boundary_blocked.sh
# Executes orchestrator.py --force-replan true WITHOUT --enable-exec-from-workspace.
# Must verify exit code is 1 and error message is correct.

SCRIPT_DIR=$(dirname "$0")
ORCHESTRATOR_PATH="$SCRIPT_DIR/../scripts/orchestrator.py"

OUTPUT=$(python3 "$ORCHESTRATOR_PATH" --workdir /tmp --prd-file /tmp/test.md 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 1 ]; then
    echo "FAIL: Expected exit code 1, got $EXIT_CODE"
    exit 1
fi

if echo "$OUTPUT" | grep -qF "[FATAL] Security Violation: Unless for testing purposes, skills must be executed from the ~/.openclaw/skills/ runtime directory."; then
    echo "PASS: Blocked correctly."
    exit 0
else
    echo "FAIL: Error message not found in output."
    echo "Actual output:"
    echo "$OUTPUT"
    exit 1
fi
