#!/bin/bash
set -e
export SDLC_TEST_MODE=true
echo "Running CUJ 5 Mock Test via OpenClaw..."
mkdir -p /root/.openclaw/workspace/tests
rm -f /root/.openclaw/workspace/tests/tool_calls.log

openclaw agent --session-id test_cuj_5 --message "请调用 exec 执行: SDLC_TEST_MODE=true python3 /root/.openclaw/skills/leio-sdlc/scripts/update_issue.py --issue-id ISSUE-999 --status closed"

if grep -q "'tool': 'update_issue'" /root/.openclaw/workspace/tests/tool_calls.log; then
    echo "SUCCESS: update_issue mock test passed."
    exit 0
else
    echo "ERROR: log not found."
    exit 1
fi
