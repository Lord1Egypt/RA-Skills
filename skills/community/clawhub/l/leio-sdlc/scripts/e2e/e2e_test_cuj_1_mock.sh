#!/bin/bash
set -e
export SDLC_TEST_MODE=true
echo "Running CUJ 1 Mock Test via OpenClaw..."
mkdir -p /root/.openclaw/workspace/tests
touch /root/.openclaw/workspace/docs/PRDs/dummy.md
rm -f /root/.openclaw/workspace/tests/tool_calls.log

openclaw agent --session-id test_cuj_1 --message "无需检查文件内容，请立刻根据 leio-sdlc 的 Command Template 1 规范，调用 exec 工具执行: SDLC_TEST_MODE=true python3 /root/.openclaw/skills/leio-sdlc/scripts/spawn_planner.py --prd-file /root/.openclaw/workspace/docs/PRDs/dummy.md --workdir /root/.openclaw/workspace"

if grep -q "'tool': 'spawn_planner'" /root/.openclaw/workspace/tests/tool_calls.log; then
    echo "SUCCESS: spawn_planner mock test passed."
    exit 0
else
    echo "ERROR: tests/tool_calls.log does not contain expected output."
    exit 1
fi
