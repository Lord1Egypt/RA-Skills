#!/bin/bash
set -e

# test_e2e_yellow_path.sh - Manager E2E Test for Yellow Path (Review-Correction loop)
# Created for ISSUE-025

PROJECT_ROOT="$(pwd)"

# 1. 创建隔离沙盒
sandbox_id="$(uuidgen)"
sandbox_dir="tests/e2e_sandbox_yellow_${sandbox_id}"

mkdir -p "$sandbox_dir"
cd "$sandbox_dir"

# Initialize git
git init
git config user.name "E2E Test"
git config user.email "e2e@example.com"
git commit --allow-empty -m "init"

MOCK_GLOBAL="/tmp/mock_global_yellow"
RUN_DIR="$MOCK_GLOBAL/.sdlc_runs/dummy_prd"
export SDLC_GLOBAL_RUN_BASE="$MOCK_GLOBAL/.sdlc_runs"
mkdir -p "$RUN_DIR"

# 2. 挂载依赖（软链接）
ln -s ../../scripts scripts
ln -s ../../playbooks playbooks
ln -s ../../docs docs
ln -s ../../TEMPLATES TEMPLATES

mkdir -p docs/PRDs
cat << 'EOF' > docs/PRDs/dummy_prd.md
# PRD: Hello World
Implement a hello world script.
EOF

# Pre-create a stub PR so Manager skips Planner
mkdir -p "$RUN_DIR"
cat << EOF > "$RUN_DIR/PR_001_Stub.md"
# PR: 001
Implement a hello world script that prints "Hello, SDLC!"
EOF

# 3. 编排测试场景
# Stub Coder
cat << 'EOF' > scripts/spawn_coder.py
#!/usr/bin/env python3
import sys
import os
import json
print(f"Mock Coder running in {os.getcwd()}")
# Simulate Coder creating a file
with open("hello.py", "w") as f:
    f.write("print('Hello, SDLC!')")
# Commit the changes
os.system("git add hello.py && git commit -m 'feat: init hello.py'")
# Simulate successful exit
sys.exit(0)
EOF
chmod +x scripts/spawn_coder.py

# Stub Reviewer (to force Yellow Path)
cat << EOF > scripts/spawn_reviewer.py
#!/usr/bin/env python3
import sys
import os
state_file = ".test_state_reviewer"
# 1st run: ACTION_REQUIRED
# 2nd run: APPROVED
if not os.path.exists(state_file):
    with open(state_file, "w") as f: f.write("1")
    with open("$RUN_DIR/review_report.json", "w") as f:
        f.write('{"status": "ACTION_REQUIRED", "comments": "Missing test coverage."}')
    sys.exit(0)
else:
    with open("$RUN_DIR/review_report.json", "w") as f:
        f.write('{"status": "APPROVED", "comments": "Good job."}')
    sys.exit(0)
EOF
chmod +x scripts/spawn_reviewer.py

# 4. 准备 Manager Prompt
MANAGER_PROMPT="You are the leio-sdlc Manager executing a System Test. A PRD exists at \`docs/PRDs/dummy_prd.md\` and its PR contract is already in \`$RUN_DIR/PR_001_Stub.md\`. I have provided an initial \`hello.py\`. Begin immediately at the Review phase. You MUST execute the reviewer script. If you encounter an [ACTION_REQUIRED], you MUST follow the SKILL.md rules and call Command Template 2b: run \`spawn_coder.py --workdir . --feedback-file $RUN_DIR/review_report.json --run-dir $RUN_DIR --global-dir $MOCK_GLOBAL\` to fix the code, then run \`spawn_reviewer.py --workdir . --run-dir $RUN_DIR --global-dir $MOCK_GLOBAL\` again. The max revisions is MAX_REVISIONS=3. Continue until you get an APPROVED status in JSON and then perform Merge."

# 5. 执行测试
export SDLC_TEST_MODE=true
# Use a here-doc to avoid shell interpretation issues
openclaw agent -m "$MANAGER_PROMPT"

# 6. 断言
# Assert that merge_code was called, which is the final step
if ! grep -q "'tool': 'merge_code'" "tests/tool_calls.log"; then
  echo "❌ Test Failed: Final merge_code tool call not found."
  exit 1
fi

echo "✅ Test Passed: Yellow Path (Review-Correction loop) completed successfully."

# 7. 清理
cd "$PROJECT_ROOT"
rm -rf "$sandbox_dir"
