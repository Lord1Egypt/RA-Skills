#!/bin/bash
set -e
export SDLC_TEST_MODE=true
echo "Running CUJ 3 Mock Test via OpenClaw..."
mkdir -p /root/.openclaw/workspace/tests
touch /root/.openclaw/workspace/docs/PRs/dummy_pr.md
rm -f /root/.openclaw/workspace/tests/tool_calls.log

openclaw agent --session-id test_cuj_3 --message "请调用 exec 执行: SDLC_TEST_MODE=true python3 /root/.openclaw/skills/leio-sdlc/scripts/spawn_reviewer.py --pr-file /root/.openclaw/workspace/docs/PRs/dummy_pr.md --diff-target HEAD~1..HEAD --workdir /root/.openclaw/workspace"

if grep -q "'tool': 'spawn_reviewer'" /root/.openclaw/workspace/tests/tool_calls.log; then
    echo "SUCCESS: spawn_reviewer mock test passed."
    exit 0
else
    echo "ERROR: log not found."
    exit 1
fi
