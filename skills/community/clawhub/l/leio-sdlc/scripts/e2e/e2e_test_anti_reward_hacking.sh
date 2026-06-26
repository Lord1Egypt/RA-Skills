#!/usr/bin/env bash
export SDLC_TEST_MODE=true
set -e

echo "Running Anti-Reward Hacking Tests..."

# Scenario 1
mkdir -p dummy_workspace/bin
cat << 'INNER_EOF' > dummy_workspace/bin/openclaw
#!/bin/bash
exit 0
INNER_EOF
chmod +x dummy_workspace/bin/openclaw
export PATH="$(pwd)/dummy_workspace/bin:$PATH"
mkdir -p dummy_workspace
cd dummy_workspace
touch dummy.md
python3 ../scripts/orchestrator.py --force-replan true --enable-exec-from-workspace --channel "valid:id" --workdir "$(pwd)" --prd-file dummy.md --global-dir ../ --max-prs-to-process 1 > test.log 2>&1 || true

if grep -q "No such file or directory.*scripts/" test.log; then
    echo "FAILED: Orchestrator is still using relative scripts/ paths!"
    cat test.log
    exit 1
fi
echo "Test Scenario 1 passed."

# Scenario 2
cd ..
# We need to make a dummy change so spawn_reviewer.py gets a diff
echo "dummy diff content" > dummy_workspace/dummy_diff.txt
git add dummy_workspace/dummy_diff.txt

SDLC_TEST_MODE=true python3 scripts/spawn_reviewer.py --pr-file dummy_workspace/dummy.md --diff-target HEAD --workdir "$(pwd)" --global-dir "$(pwd)" || true

# Cleanup git changes
git reset HEAD dummy_workspace/dummy_diff.txt >/dev/null 2>&1
rm dummy_workspace/dummy_diff.txt

if ! grep -q "CRITICAL REDLINE - ANTI-REWARD HACKING" tests/tool_calls.log; then
    echo "FAILED: Prompt Guardrail missing in payload!"
    exit 1
fi
echo "Test Scenario 2 passed."

rm -rf dummy_workspace tests/tool_calls.log

echo "All Anti-Reward Hacking Tests passed."
