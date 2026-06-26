#!/bin/bash
set -u

echo "Starting Job Queue Engine Tests..."

# Setup sandbox
SANDBOX="tests/e2e_job_queue_$$"
mkdir -p "$SANDBOX"

# Teardown logic
cleanup() {
  echo "Cleaning up sandbox: $SANDBOX"
  rm -rf "$SANDBOX"
}
trap cleanup EXIT

# Helper for asserting failure (negative tests)
assert_fail() {
  local cmd="$1"
  local expected_msg="$2"
  
  echo "Running (Expecting Failure): $cmd"
  output=$($cmd 2>&1)
  exit_code=$?
  
  if [ $exit_code -ne 1 ]; then
    echo "❌ FAILED: Expected command to fail with exit code 1, but got $exit_code."
    echo "Command: $cmd"
    exit 1
  fi
  
  if [[ "$output" != *"$expected_msg"* ]]; then
    echo "❌ FAILED: Expected error message not found."
    echo "Expected substring: $expected_msg"
    echo "Actual output: $output"
    exit 1
  fi
  echo "✅ PASS: $cmd"
}

# Helper for asserting success (positive tests)
assert_success() {
  local cmd="$1"
  local expected_msg="$2"
  
  echo "Running (Expecting Success): $cmd"
  output=$($cmd 2>&1)
  exit_code=$?
  
  if [ $exit_code -ne 0 ]; then
    echo "❌ FAILED: Expected command to succeed but it failed (exit code $exit_code)."
    echo "Command: $cmd"
    echo "Output: $output"
    exit 1
  fi
  
  if [[ "$output" != *"$expected_msg"* ]]; then
    echo "❌ FAILED: Expected success message not found."
    echo "Expected substring: $expected_msg"
    echo "Actual output: $output"
    exit 1
  fi
  echo "✅ PASS: $cmd"
}

GET_NEXT_PR="python3 scripts/get_next_pr.py --workdir $(pwd)"
UPDATE_PR_STATUS="python3 scripts/update_pr_status.py"

echo "--------------------------------------"
echo "Test 1: Negative - get_next_pr on missing dir"
assert_fail "$GET_NEXT_PR --job-dir missing_dir_$$" "does not exist"
assert_fail "$GET_NEXT_PR --job-dir missing_dir_$$" "does not exist"
echo "--------------------------------------"
echo "Test 2: Negative - update_status on missing file"
assert_fail "$UPDATE_PR_STATUS --pr-file missing_file_$$.md --status open" "[Pre-flight Failed] Cannot update status. PR file 'missing_file_$$.md' not found."

echo "--------------------------------------"
echo "Test 3: Negative - update_status on file without status field"
NO_STATUS_FILE="$SANDBOX/no_status.md"
echo "This file has no status field." > "$NO_STATUS_FILE"
assert_fail "$UPDATE_PR_STATUS --pr-file $NO_STATUS_FILE --status closed" "[Pre-flight Failed] File '$NO_STATUS_FILE' does not contain a 'status: ...' field."

echo "--------------------------------------"
echo "Test 4: Positive Flow"
JOB_DIR="$SANDBOX/feature_x"
mkdir -p "$JOB_DIR"
echo "status: closed" > "$JOB_DIR/01_DB.md"
echo "status: open" > "$JOB_DIR/02_API.md"
echo "status: open" > "$JOB_DIR/03_UI.md"

# Run get_next_pr.py -> expect 02_API.md
assert_success "$GET_NEXT_PR --job-dir $JOB_DIR" "02_API.md"

# Update 02_API.md to closed
assert_success "$UPDATE_PR_STATUS --pr-file $JOB_DIR/02_API.md --status closed" "[STATUS_UPDATED] $JOB_DIR/02_API.md is now closed."

# Run get_next_pr.py -> expect 03_UI.md
assert_success "$GET_NEXT_PR --job-dir $JOB_DIR" "03_UI.md"

# Update 03_UI.md to closed
assert_success "$UPDATE_PR_STATUS --pr-file $JOB_DIR/03_UI.md --status closed" "[STATUS_UPDATED] $JOB_DIR/03_UI.md is now closed."

# Run get_next_pr.py -> expect queue empty
assert_success "$GET_NEXT_PR --job-dir $JOB_DIR" "[QUEUE_EMPTY]"

echo "--------------------------------------"
echo "✅ ALL TESTS PASSED!"
