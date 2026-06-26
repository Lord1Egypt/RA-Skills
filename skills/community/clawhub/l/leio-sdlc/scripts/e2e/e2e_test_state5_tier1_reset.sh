#!/bin/bash
export SDLC_TEST_MODE=true
set -e

# scripts/test_state5_tier1_reset.sh - Test for PR-002

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

function setup_sandbox() {
    sandbox_dir=$(mktemp -d)
    cd "$sandbox_dir"
    mkdir -p "bin"
    cat << 'INNER_EOF' > "bin/openclaw"
#!/bin/bash
exit 0
INNER_EOF
    chmod +x "bin/openclaw"
    export PATH="$(pwd)/bin:$PATH"
    git init > /dev/null 2>&1
    git config user.name "E2E Test"
    git config user.email "e2e@example.com"
    git commit --allow-empty -m "init" > /dev/null 2>&1
    echo "*.log" > .gitignore
    git add .gitignore
    git commit -m "add gitignore" > /dev/null 2>&1

    mkdir -p docs/PRDs
    mkdir -p scripts config
    
    # Copy essential scripts
    cp "${PROJECT_ROOT}/scripts/orchestrator.py" scripts/
cp "${PROJECT_ROOT}/scripts/setup_logging.py" scripts/ || true
    cp "${PROJECT_ROOT}/scripts/agent_driver.py" scripts/
    cp "${PROJECT_ROOT}/config/prompts.json" config/
    cp "${PROJECT_ROOT}/scripts/get_next_pr.py" scripts/
    cp "${PROJECT_ROOT}/scripts/git_utils.py" scripts/
    cp "${PROJECT_ROOT}/scripts/notification_formatter.py" scripts/
    cp "${PROJECT_ROOT}/scripts/handoff_prompter.py" scripts/

    echo "*.lock" >> .gitignore
    echo "__pycache__/" >> .gitignore
}

function run_test() {
    echo "--- Running State 5 Tier 1 Reset Test ---"
    setup_sandbox
    
    # Create a dummy PRD
    echo "dummy prd" > docs/PRDs/TestProject.md
    
    export MOCK_GLOBAL_DIR=$(mktemp -d)
    # Create a PR in the global run dir
    PROJECT_NAME=$(basename "$sandbox_dir")
    RUN_DIR="$MOCK_GLOBAL_DIR/.sdlc_runs/$PROJECT_NAME/TestProject"
    mkdir -p "$RUN_DIR"
    cat << 'INNER_EOF' > "$RUN_DIR/PR_001_Test.md"
status: open
slice_depth: 0
INNER_EOF

    # Stub spawn_coder.py to intentionally fail to trigger State 5
    cat << 'INNER_EOF' > scripts/spawn_coder.py
import sys, subprocess, os
# Simulate a coder that leaves the workspace dirty but fails
if not os.path.exists("run_once.txt"):
    with open("run_once.txt", "w") as f: f.write("1")
    with open("dirty_file.txt", "w") as f:
    f.write("I am dirty")
sys.exit(1)
INNER_EOF
    chmod +x scripts/spawn_coder.py

    # Stub spawn_planner.py (needed if Tier 2 is hit, but we target Tier 1)
    cat << 'INNER_EOF' > scripts/spawn_planner.py
import sys
sys.exit(0)
INNER_EOF
    chmod +x scripts/spawn_planner.py

    git add .
    git commit -m "setup test" > /dev/null 2>&1

    # Use a lock-safe execution environment
    export SDLC_BYPASS_BRANCH_CHECK=1
    
    # Run orchestrator.
    # We expect it to:
    # 1. Start PR_001
    # 2. Spawn coder (which fails and leaves workspace dirty)
    # 3. Trigger State 5
    # 4. Perform Tier 1 Reset (git reset --hard, git clean -fd)
    # 5. Succeed checkout master
    
    # Use a mock global dir
    echo "Starting orchestrator..."
    # We use a temporary log file so we don't pollute the git status of the sandbox if it checks it
    git status
    python3 scripts/orchestrator.py --global-dir "$MOCK_GLOBAL_DIR" --force-replan false --enable-exec-from-workspace --channel "valid:id" --workdir "$(pwd)" --prd-file docs/PRDs/TestProject.md --max-prs-to-process 1 --coder-session-strategy always > ../orchestrator.log 2>&1 || true
    mv ../orchestrator.log orchestrator.log

    # Assertions
    if grep -q "GitCheckoutError" orchestrator.log; then
        echo "❌ FAILED: GitCheckoutError detected in logs."
        cat orchestrator.log
        exit 1
    fi

    echo "--- Orchestrator Log Snippet ---"
    grep "Tier 1 (Reset): Deleting branch and retrying." orchestrator.log || echo "Tier 1 log not found"
    echo "-------------------------------"

    if ! grep -q "Tier 1 (Reset): Deleting branch and retrying." orchestrator.log; then
        echo "❌ FAILED: Did not reach Tier 1 Reset."
        cat orchestrator.log
        exit 1
    fi

    # Verify we are back on master (or at least the branch is gone and master is clean)
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "master" ]; then
        # The orchestrator might have continued to another loop or exited, 
        # but if Tier 1 worked, master should be accessible.
        git checkout master > /dev/null 2>&1 || { echo "❌ FAILED: Cannot checkout master after reset."; exit 1; }
    fi

    if [ -f "dirty_file.txt" ]; then
        echo "❌ FAILED: dirty_file.txt still exists. Clean failed."
        cat orchestrator.log
        exit 1
    fi

    # Project basename is evaluated to the sandbox_dir name
    PROJECT_NAME=$(basename "$sandbox_dir")
    RUN_DIR="$MOCK_GLOBAL_DIR/.sdlc_runs/$PROJECT_NAME"

    if [ ! -d "$RUN_DIR" ]; then
        echo "❌ FAILED: Global run directory $RUN_DIR does not exist."
        exit 1
    fi

    # Explicitly check that git info exclude does NOT contain .sdlc_runs/
    if grep -q "\.sdlc_runs/" .git/info/exclude 2>/dev/null; then
        echo "❌ FAILED: .git/info/exclude contains .sdlc_runs/, it should not."
        exit 1
    fi

    echo "✅ PASS: State 5 Tier 1 Reset successfully cleaned workspace and preserved Control Plane state."
}

run_test
