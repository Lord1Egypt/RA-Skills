#!/bin/bash
# test_runtime_boundary_allowed.sh
# Executes orchestrator.py --force-replan true WITH --enable-exec-from-workspace.
# Must bypass path check and not print the security violation error.

SCRIPT_DIR=$(dirname "$0")
ORCHESTRATOR_PATH="$SCRIPT_DIR/../scripts/orchestrator.py"

OUTPUT=$(python3 "$ORCHESTRATOR_PATH" --workdir /tmp --prd-file /tmp/test.md --enable-exec-from-workspace 2>&1)
EXIT_CODE=$?

EXPECTED_MSG="\[FATAL\] Security Violation: 除非是为了测试目的，Skill 的执行必须从 ~/.openclaw/skills/ 目录下启动。如果明确是为了测试未发布的源码，必须在命令中显式附加参数: --enable-exec-from-workspace"

if echo "$OUTPUT" | grep -q "$EXPECTED_MSG"; then
    echo "FAIL: Expected bypass, but security error was raised."
    echo "Actual output:"
    echo "$OUTPUT"
    exit 1
else
    echo "PASS: Allowed correctly."
    exit 0
fi
