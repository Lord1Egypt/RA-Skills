#!/bin/bash
export SDLC_TEST_MODE=true
set -e

# scripts/e2e_test_hierarchical_resilience.sh - End-to-end verification of Four-Path Resilience

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
    
    export MOCK_GLOBAL_DIR=$(mktemp -d)
    mkdir -p "$MOCK_GLOBAL_DIR/config"
    cat << 'INNER_EOF' > "$MOCK_GLOBAL_DIR/config/sdlc_config.json"
{
  "YELLOW_RETRY_LIMIT": 3,
  "RED_RETRY_LIMIT": 2
}
INNER_EOF
}

function test_e2e_hierarchical_resilience() {
    echo "--- Running E2E Test: Hierarchical Resilience (Four-Path) ---"
    setup_sandbox
    
    echo "dummy prd" > docs/PRDs/TestProject.md
    
    PROJECT_NAME=$(basename "$sandbox_dir")
    RUN_DIR="$MOCK_GLOBAL_DIR/.sdlc_runs/$PROJECT_NAME/TestProject"
    mkdir -p "$RUN_DIR"
    cat << 'INNER_EOF' > "$RUN_DIR/PR_001_Test.md"
status: open
slice_depth: 0
INNER_EOF

    # Stub coder
    cat << 'INNER_EOF' > scripts/spawn_coder.py
import sys, os
with open("/tmp/coder_runs.log", "a") as f:
    f.write("coder_run\n")
# Create a dummy file to simulate work
with open("feature.txt", "w") as f:
    f.write("code")
os.system("git add feature.txt")
os.system("git commit -m 'feat'")
sys.exit(0)
INNER_EOF
    chmod +x scripts/spawn_coder.py

    # Stub reviewer to always reject
    cat << 'INNER_EOF' > scripts/spawn_reviewer.py
import sys, os
import json
out_file = None
for i, arg in enumerate(sys.argv):
    if arg == "--out-file" and i+1 < len(sys.argv):
        out_file = sys.argv[i+1]
        
if out_file:
    with open(out_file, "w") as f:
        f.write(json.dumps({"status": "ACTION_REQUIRED", "comments": "mock reject"}))
sys.exit(0)
INNER_EOF
    chmod +x scripts/spawn_reviewer.py
    
    # Stub arbitrator to confirm reject
    cat << 'INNER_EOF' > scripts/spawn_arbitrator.py
import sys
print("[CONFIRM_REJECT]")
sys.exit(0)
INNER_EOF
    chmod +x scripts/spawn_arbitrator.py
    
    # Stub planner to fail the test quickly when Black Path is reached
    cat << 'INNER_EOF' > scripts/spawn_planner.py
import sys
print("Spawn Planner triggered (Black Path)!")
sys.exit(0)
INNER_EOF
    chmod +x scripts/spawn_planner.py

    git add .
    git commit -m "setup test" > /dev/null 2>&1

    export SDLC_BYPASS_BRANCH_CHECK=1
    
    rm -f /tmp/coder_runs.log
    
    echo "Starting orchestrator..."
    python3 scripts/orchestrator.py --global-dir "$MOCK_GLOBAL_DIR" --force-replan false --enable-exec-from-workspace --channel "valid:id" --workdir "$(pwd)" --prd-file docs/PRDs/TestProject.md --max-prs-to-process 1 --coder-session-strategy always > ../orchestrator.log 2>&1 || true
    mv ../orchestrator.log orchestrator.log

    # Verify transitions
    CODER_RUNS=$(wc -l < /tmp/coder_runs.log 2>/dev/null || echo 0)
    
    # Yellow limit is 3, Red limit is 2.
    # Total coder runs before Black path:
    # 1st Red cycle: 1 initial + 3 yellow retries = 4
    # Wait, yellow retry: "if yellow_counter < yellow_retry_limit"
    # Actually, the logic in orchestrator:
    # yellow_counter starts at 0. review rejects -> yellow_counter += 1 (now 1).
    # 1 < 3? yes -> spawn coder.
    # review rejects -> yellow_counter += 1 (now 2). 2 < 3? yes -> spawn coder.
    # review rejects -> yellow_counter += 1 (now 3). 3 < 3? no -> spawn arbitrator.
    # Arbitrator confirms reject -> state_5_trigger = True.
    # So 3 coder runs per Red cycle? Wait:
    # Initial spawn coder (State 3).
    # Review rejects (1) -> spawn coder (retry 1).
    # Review rejects (2) -> spawn coder (retry 2).
    # Review rejects (3) -> spawn arbitrator.
    # So 3 coder runs total per Red cycle.
    # Red limit is 2. 
    # Red cycle 1: 3 coder runs. red_counter becomes 1. git reset.
    # Red cycle 2: 3 coder runs. red_counter becomes 2. git reset.
    # Red cycle 3: 3 coder runs. red_counter becomes 3... wait.
    # if red_counter < red_retry_limit (2): continue.
    # Initial run (red_counter=0) -> state_5 -> red_counter=1 -> continue
    # Next run (red_counter=1) -> state_5 -> red_counter=2 -> continue
    # Next run (red_counter=2) -> state_5 -> else block (Black path)
    # Total coder runs = 3 * 3 = 9.

    if ! grep -q "Red Path Triggered" orchestrator.log; then
        echo "❌ FAILED: Red Path was never triggered."
        cat orchestrator.log
        exit 1
    fi
    
    CODER_RUNS=$(wc -l < /tmp/coder_runs.log 2>/dev/null || echo 0)
    if [ "$CODER_RUNS" -ne 9 ]; then
        echo "❌ FAILED: Expected 9 coder runs (Yellow and Red transitions), got $CODER_RUNS"
        cat orchestrator.log
        exit 1
    fi
    
    if ! grep -q "Spawn Planner triggered (Black Path)!" orchestrator.log && ! grep -q "superseded" "$RUN_DIR/PR_001_Test.md" && ! grep -q "blocked_fatal" "$RUN_DIR/PR_001_Test.md"; then
        echo "❌ FAILED: Black Path (Planner slice) was never triggered."
        cat orchestrator.log
        exit 1
    fi

    echo "✅ PASS: Hierarchical Resilience (Four-Path) successfully tested."
}

function test_deploy_hot_preservation() {
    echo "--- Running E2E Test: Deploy Hot Preservation ---"
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    mkdir -p leio-sdlc
    cp "${PROJECT_ROOT}/deploy.sh" leio-sdlc/
    cd leio-sdlc
    
    export HOME_MOCK="$test_dir/home"
    mkdir -p "$HOME_MOCK/.openclaw/skills/leio-sdlc/config"
    echo '{"HOT": "PRESERVED"}' > "$HOME_MOCK/.openclaw/skills/leio-sdlc/config/sdlc_config.json"
    
    # Mock preflight and release
    mkdir -p scripts
    echo "exit 0" > scripts/test_sdlc_cujs.sh
    echo "mkdir -p .dist && echo 'new_code' > .dist/main.py" > scripts/build_release.sh
    chmod +x scripts/*.sh
    
    bash deploy.sh --no-restart > deploy.log 2>&1
    
    if [ ! -f "$HOME_MOCK/.openclaw/skills/leio-sdlc/config/sdlc_config.json" ]; then
        echo "❌ FAILED: sdlc_config.json was not preserved!"
        cat deploy.log
        exit 1
    fi
    
    if ! grep -q "PRESERVED" "$HOME_MOCK/.openclaw/skills/leio-sdlc/config/sdlc_config.json"; then
        echo "❌ FAILED: sdlc_config.json content was altered or not restored!"
        exit 1
    fi
    
    echo "✅ PASS: Deploy Hot Preservation successfully tested."
}

test_deploy_hot_preservation
test_e2e_hierarchical_resilience

