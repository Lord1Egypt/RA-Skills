#!/bin/bash
set -e
export SDLC_TEST_MODE=true
echo "Running CUJ 4 Mock Test via OpenClaw..."
mkdir -p /root/.openclaw/workspace/tests
rm -f /root/.openclaw/workspace/tests/tool_calls.log

openclaw agent --session-id test_cuj_4 --message "请调用 exec 执行: SDLC_TEST_MODE=true python3 /root/.openclaw/skills/leio-sdlc/scripts/merge_code.py --branch feature/login"

if grep -q "'tool': 'merge_code'" /root/.openclaw/workspace/tests/tool_calls.log; then
    echo "SUCCESS: merge_code mock test passed."
    exit 0
else
    echo "ERROR: log not found."
    exit 1
fi
