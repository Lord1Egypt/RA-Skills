#!/bin/bash
set -e

echo "Running E2E Mock Test for UAT Verifier Engine..."

# Setup temporary directories
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

cd "$TEST_DIR"

export SDLC_TEST_MODE="true"
export SDLC_RUN_DIR="$TEST_DIR"
export MOCK_VERIFIER_RESULT='{"status": "PASS", "executive_summary": "All requirements implemented", "verification_details": []}'

WORK_DIR="$TEST_DIR/workdir"
mkdir -p "$WORK_DIR"

PRD_FILE="$TEST_DIR/test_prd.md"
echo "# Mock PRD" > "$PRD_FILE"

OUT_FILE="$TEST_DIR/test_uat_report.json"

SCRIPT_PATH="/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_verifier.py"

python3 "$SCRIPT_PATH" --prd-files "$PRD_FILE" --workdir "$WORK_DIR" --out-file "$OUT_FILE" --enable-exec-from-workspace

if [ ! -f "$OUT_FILE" ]; then
    echo "Error: Output file $OUT_FILE was not created."
    exit 1
fi

STATUS=$(cat "$OUT_FILE" | grep '"status": "PASS"')
if [ -z "$STATUS" ]; then
    echo "Error: Output file does not contain expected mock status."
    exit 1
fi

echo "Test passed!"
exit 0
