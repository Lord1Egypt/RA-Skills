#!/bin/bash
set -e

# e2e test for ISSUE-1092 Global Dir Fallback

TEST_DIR=$(mktemp -d)
echo "Setting up test workspace in $TEST_DIR"

cd "$TEST_DIR"
git init > /dev/null
echo "Affected_Projects: [mock2]" > PRD.md
git add PRD.md
git commit -m "init" > /dev/null

export SDLC_TEST_MODE="true"

# The scripts path
SDLC_ROOT="/root/.openclaw/workspace/projects/leio-sdlc"

echo "Testing spawn_planner.py without --global-dir..."
python3 "$SDLC_ROOT/scripts/spawn_planner.py" --workdir "$TEST_DIR" --prd-file PRD.md

echo "Checking if .sdlc_runs is created in workdir..."
if [ -d "$TEST_DIR/.sdlc_runs" ]; then
    echo "PASS: spawn_planner.py created .sdlc_runs in workdir"
else
    echo "FAIL: spawn_planner.py did not create .sdlc_runs in workdir"
    exit 1
fi

echo "Testing orchestrator.py without --global-dir..."
python3 "$SDLC_ROOT/scripts/orchestrator.py" --workdir "$TEST_DIR" --prd-file PRD.md --force-replan false --test-sleep --enable-exec-from-workspace --channel test_channel

echo "PASS: orchestrator.py did not raise RuntimeError"

rm -rf "$TEST_DIR"
echo "All tests passed."
# --- TDD Blueprint Test Cases for Dual Yellow Path ---

echo "Setting up orchestrator FSM test environment..."
# Copy the scripts to a temporary bin dir so we can mock the spawned agents
TMP_SCRIPTS=$(mktemp -d)
cp -r "$SDLC_ROOT/scripts/"* "$TMP_SCRIPTS/"
cp -r "$SDLC_ROOT/config/" "$TMP_SCRIPTS/../config/"
export RUNTIME_DIR="$TMP_SCRIPTS"

# 1. Mock spawn_coder to just exit 0, but leave a dirty git workspace
cat << 'MOCK' > "$TMP_SCRIPTS/spawn_coder.py"
import sys, os
print("MOCK CODER RUNNING")
# Read args to see if we have a system alert
if "--system-alert" in sys.argv:
    if os.path.exists("mock_dirty.txt"):
        with open("mock_dirty.txt", "a") as f:
            f.write("alert received\n")
    sys.exit(0)
    
if "mock_dirty" in os.environ:
    with open("mock_dirty.txt", "w") as f: f.write("dirty")
elif "mock_preflight_fail" in os.environ:
    with open("preflight.sh", "w") as f: f.write("#!/bin/bash\nexit 1\n")
    os.chmod("preflight.sh", 0o755)
    os.system("git add preflight.sh && git commit -m 'add preflight'")
elif "mock_exhaust" in os.environ:
    with open("preflight.sh", "w") as f: f.write("#!/bin/bash\nexit 1\n")
    os.chmod("preflight.sh", 0o755)
    os.system("git add preflight.sh && git commit -m 'add preflight'")
sys.exit(0)
MOCK
chmod +x "$TMP_SCRIPTS/spawn_coder.py"

cat << 'MOCK' > "$TMP_SCRIPTS/get_next_pr.py"
import sys
print(".sdlc_runs/mock2/PRD/PR_001.md")
MOCK

cat << 'MOCK' > "$TMP_SCRIPTS/spawn_reviewer.py"
import sys
import json
with open(sys.argv[sys.argv.index("--out-file")+1], "w") as f:
    f.write(json.dumps({"status": "APPROVED"}))
MOCK

cat << 'MOCK' > "$TMP_SCRIPTS/spawn_planner.py"
import sys
sys.exit(0) # mock slicing
MOCK

# Setup a fake PR
setup_fake_pr() {
    rm -rf "$TEST_DIR/mock2"
    mkdir -p "$TEST_DIR/mock2"
    cd "$TEST_DIR/mock2"
    git init > /dev/null
    git branch -m master 2>/dev/null || true
    git commit --allow-empty -m "init" > /dev/null
    mkdir -p .sdlc_runs/mock2/PRD
    echo ".sdlc_repo.lock" > .gitignore
    echo "status: in_progress" > .sdlc_runs/mock2/PRD/PR_001.md
    git add .
    git commit -m "add pr" > /dev/null
}

echo "Test Case 1: Mock git status dirty"
setup_fake_pr
export mock_dirty="1"
python3 "$TMP_SCRIPTS/orchestrator.py" --workdir "$TEST_DIR/mock2" --prd-file PRD.md --force-replan false --channel test_channel --enable-exec-from-workspace --debug > /tmp/orch.log 2>&1 || true
if grep -q "Dirty status detected" /tmp/orch.log; then
    echo "PASS: Test Case 1 (Git status dirty increments yellow counter / system alert)"
else
    echo "FAIL: Test Case 1"
    exit 1
fi
unset mock_dirty

echo "Test Case 2: Mock clean git status but failing preflight.sh"
setup_fake_pr
export mock_preflight_fail="1"
python3 "$TMP_SCRIPTS/orchestrator.py" --workdir "$TEST_DIR/mock2" --prd-file PRD.md --force-replan false --channel test_channel --enable-exec-from-workspace --debug > /tmp/orch.log 2>&1 || true
if grep -q "Preflight failed with code 1" /tmp/orch.log; then
    echo "PASS: Test Case 2 (Failing preflight increments yellow counter / system alert)"
else
    echo "FAIL: Test Case 2"
    exit 1
fi
unset mock_preflight_fail

echo "Test Case 3: Trigger orch_yellow_counter >= yellow_retry_limit (Moves to State 5)"
setup_fake_pr
export mock_exhaust="1"
python3 "$TMP_SCRIPTS/orchestrator.py" --workdir "$TEST_DIR/mock2" --prd-file PRD.md --force-replan false --channel test_channel --enable-exec-from-workspace --debug > /tmp/orch.log 2>&1 || true
if grep -q "State 5 Escalation" /tmp/orch.log || grep -q "Archiving forensic artifacts" /tmp/orch.log || grep -q "Archiving crashed dir" /tmp/orch.log; then
    echo "PASS: Test Case 3 (Exhausting yellow limit triggers State 5 / Red Path)"
else
    echo "FAIL: Test Case 3"
    cat /tmp/orch.log
    exit 1
fi
unset mock_exhaust

rm -rf "$TMP_SCRIPTS"

echo "All tests passed."
