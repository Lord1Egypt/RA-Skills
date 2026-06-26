#!/usr/bin/env bash
set -e

# Emulate setup_sandbox
setup_sandbox() {
    TEST_DIR="/tmp/$1"
    mkdir -p "$TEST_DIR"
    cp -r /root/.openclaw/workspace/projects/leio-sdlc/* "$TEST_DIR/"
    cd "$TEST_DIR"
    export PYTHONPATH="$TEST_DIR"
    export WORKSPACE_DIR="$TEST_DIR"
    mkdir -p docs/PRDs "$GLOBAL_MOCK_DIR/.sdlc_runs/PRD"
}

cleanup_sandbox() {
    rm -rf "/tmp/$1"
}

echo "================================================="
echo "Testing: Planner Micro-Slicing Logic"
echo "================================================="

setup_sandbox "test_planner_slice"
export SDLC_TEST_MODE=true
export GLOBAL_MOCK_DIR="/tmp/mock_sdlc_global_$$"
mkdir -p "$GLOBAL_MOCK_DIR/.sdlc_runs/test_planner_slice/PRD"

# Create a mock PRD
echo "# Mock PRD" > PRD.md

# Test Scenario 1: Regression (Happy Path)
echo "Running Test Scenario 1 (Regression)..."
python3 scripts/spawn_planner.py --prd-file PRD.md --workdir . --global-dir "$GLOBAL_MOCK_DIR"
ls -lR "$GLOBAL_MOCK_DIR/.sdlc_runs"
if [[ ! -f "$GLOBAL_MOCK_DIR/.sdlc_runs/test_planner_slice/PRD/PR_A.md" || ! -f "$GLOBAL_MOCK_DIR/.sdlc_runs/test_planner_slice/PRD/PR_B.md" ]]; then
    echo "❌ Scenario 1 Failed: Expected mock PRs not created."
    exit 1
fi
echo "✅ Scenario 1 Passed."

# Test Scenario 2: File Missing
echo "Running Test Scenario 2 (File Missing)..."
if python3 scripts/spawn_planner.py --prd-file PRD.md --workdir . --global-dir "$GLOBAL_MOCK_DIR" --slice-failed-pr fake.md > error_log.txt 2>&1; then
ls -lR "$GLOBAL_MOCK_DIR/.sdlc_runs"
    echo "❌ Scenario 2 Failed: Expected script to exit with error."
    exit 1
fi
if ! grep -q "\[Pre-flight Failed\]" error_log.txt; then
    echo "❌ Scenario 2 Failed: Missing '[Pre-flight Failed]' error message."
    exit 1
fi
echo "✅ Scenario 2 Passed."

# Test Scenario 3: Successful Slice
echo "Running Test Scenario 3 (Successful Slice)..."
echo "# Failed PR content" > PR_001_Failed_PR.md
python3 scripts/spawn_planner.py --prd-file PRD.md --workdir . --global-dir "$GLOBAL_MOCK_DIR" --slice-failed-pr PR_001_Failed_PR.md
ls -lR "$GLOBAL_MOCK_DIR/.sdlc_runs"
if [[ ! -f "$GLOBAL_MOCK_DIR/.sdlc_runs/test_planner_slice/PRD/PR_Slice_1.md" || ! -f "$GLOBAL_MOCK_DIR/.sdlc_runs/test_planner_slice/PRD/PR_Slice_2.md" ]]; then
    echo "❌ Scenario 3 Failed: Expected mock slice PRs not created."
    exit 1
fi
if ! grep -q -- "--insert-after 001" tests/task_string.log; then
    echo "❌ Scenario 3 Failed: Missing '--insert-after 001' in task string."
    exit 1
fi
echo "✅ Scenario 3 Passed."

# Test Scenario 4: Successful Slice with sub-id
echo "Running Test Scenario 4 (Successful Slice with sub-id)..."
echo "# Failed PR content" > PR_002_1_Failed_PR.md
python3 scripts/spawn_planner.py --prd-file PRD.md --workdir . --global-dir "$GLOBAL_MOCK_DIR" --slice-failed-pr PR_002_1_Failed_PR.md
ls -lR "$GLOBAL_MOCK_DIR/.sdlc_runs"
if ! grep -q -- "--insert-after 002_1" tests/task_string.log; then
    echo "❌ Scenario 4 Failed: Missing '--insert-after 002_1' in task string."
    cat tests/task_string.log
    exit 1
fi
echo "✅ Scenario 4 Passed."

cleanup_sandbox "test_planner_slice"
rm -rf "$GLOBAL_MOCK_DIR"
echo "✅ test_planner_slice_failed_pr.sh passed."
exit 0
