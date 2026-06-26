#!/bin/bash
set -e

echo "Running E2E Mock Test for Orchestrator UAT Integration..."

TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT
cd "$TEST_DIR"

export SDLC_TEST_MODE="true"
export SDLC_RUN_DIR="$TEST_DIR"
export SDLC_BYPASS_BRANCH_CHECK="1"
export OPENCLAW_SESSION_KEY="mock:channel"

WORK_DIR="$TEST_DIR/workdir"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"
git init >/dev/null 2>&1
git commit --allow-empty -m "Initial" >/dev/null 2>&1
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/doctor.py . --fix >/dev/null 2>&1


PRD_FILE="$WORK_DIR/test_prd.md"
cat << 'EOF' > "$PRD_FILE"
# Mock PRD
## 1. Context & Problem
## 2. Requirements & User Stories
## 3. Architecture & Technical Strategy
## 4. Acceptance Criteria
## 5. Overall Test Strategy
## 6. Framework Modifications
## 7. Hardcoded Content
EOF

git add -A >/dev/null 2>&1
git commit -m "add PRD" >/dev/null 2>&1 || true

python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/doctor.py . --fix >/dev/null 2>&1
git add -A >/dev/null 2>&1
git commit -m "fix doctor" >/dev/null 2>&1 || true

rm -f "$WORK_DIR/.sdlc_lock_manifest.json"
git add -A >/dev/null 2>&1 || true
git commit -m "clean dir" >/dev/null 2>&1 || true
echo "#!/bin/bash" > "$WORK_DIR/preflight.sh"
echo "exit 0" >> "$WORK_DIR/preflight.sh"
chmod +x "$WORK_DIR/preflight.sh"
git add -A >/dev/null 2>&1 || true
git commit -m "fix preflight for test" >/dev/null 2>&1 || true

git reset --hard HEAD >/dev/null 2>&1
git clean -fd >/dev/null 2>&1

echo ".sdlc_repo.lock" >> "$WORK_DIR/.gitignore"
echo ".tmp/" >> "$WORK_DIR/.gitignore"
git add .gitignore >/dev/null 2>&1 || true
git commit -m "ignore locks" >/dev/null 2>&1 || true

ORCHESTRATOR="/root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py"

rm -rf "$TEST_DIR/.sdlc_runs"
mkdir -p "$TEST_DIR/.sdlc_runs/workdir/test_prd"

echo "Test Case 1: Handle Missing/Invalid JSON gracefully"
export MOCK_VERIFIER_RESULT='invalid json'
# get_next_pr will return [QUEUE_EMPTY] so orchestrator directly enters state 6
mkdir -p "$TEST_DIR/.sdlc_runs/workdir/test_prd"
echo "" > "$TEST_DIR/.sdlc_runs/workdir/test_prd/.queue_empty_force"

export OPENCLAW_SESSION_KEY="mock:channel"
export MOCK_VERIFIER_RESULT='invalid json'
# Force job_dir to have nothing so it enters state 6 directly by hacking get_next_pr.py mock or directly making it empty
echo "mock_empty_queue" > "$TEST_DIR/mock_queue.txt"
# We can bypass the planner if we create an empty job directory and pass --force-replan false
mkdir -p "$WORK_DIR/.sdlc_runs/workdir/test_prd"
echo "" > "$WORK_DIR/.sdlc_runs/workdir/test_prd/.queue_empty_force"

OUT=$(python3 "$ORCHESTRATOR" --max-prs-to-process 0 --workdir "$WORK_DIR" --prd-file "$PRD_FILE" --force-replan false --enable-exec-from-workspace 2>&1 || true)



if [[ "$OUT" != *"[ACTION REQUIRED FOR MANAGER] UAT Failed. uat_report.json is missing or invalid JSON."* ]]; then
    echo "Fail Test Case 1: Did not print safe error message for invalid json"
    echo "$OUT"
    exit 1
fi
echo "Passed Test Case 1"

echo "Test Case 2: SUCCESS_HANDOFF when PASS"
export MOCK_VERIFIER_RESULT='{"status": "PASS", "executive_summary": "Mock passed", "verification_details": []}'
OUT=$(python3 "$ORCHESTRATOR" --debug --max-prs-to-process 0 --workdir "$WORK_DIR" --prd-file "$PRD_FILE" --force-replan false --enable-exec-from-workspace 2>&1 || true)
if [[ "$OUT" != *"[SUCCESS_HANDOFF] UAT Passed. You are authorized to close the ticket using issues.py."* ]]; then
    echo "Fail Test Case 2: Did not print SUCCESS_HANDOFF"
    echo "$OUT"
    exit 1
fi
echo "Passed Test Case 2"

echo "Test Case 3: ACTION REQUIRED when NEEDS_FIX"
export MOCK_VERIFIER_RESULT='{"status": "NEEDS_FIX", "executive_summary": "Mock failed", "verification_details": []}'
OUT=$(python3 "$ORCHESTRATOR" --max-prs-to-process 0 --workdir "$WORK_DIR" --prd-file "$PRD_FILE" --force-replan false --enable-exec-from-workspace 2>&1 || true)
if [[ "$OUT" != *"[ACTION REQUIRED FOR MANAGER] UAT Failed. Read uat_report.json, summarize the MISSING items to the Boss, and ask whether to append a hotfix or redo."* ]]; then
    echo "Fail Test Case 3: Did not print ACTION REQUIRED FOR MANAGER"
    echo "$OUT"
    exit 1
fi
echo "Passed Test Case 3"

echo "All tests passed!"
exit 0
