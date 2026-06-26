#!/bin/bash
set -e

# test_agent_driver_gemini.sh
# Standalone E2E test harness for Gemini driver integration
# Usage: ./test_agent_driver_gemini.sh [model_name]
# Defaults to google/gemini-2.0-flash if not provided.

export LLM_DRIVER="gemini"
export TEST_MODEL="${1:-${TEST_MODEL:-google/gemini-2.0-flash}}"

echo "==========================================="
echo "Running Isolated E2E Test for Gemini Driver"
echo "Model: $TEST_MODEL"
echo "==========================================="

PROJECT_DIR=$(dirname $(dirname $(dirname $(realpath $0))))

# Create a temporary python test script to invoke agent_driver
TEST_SCRIPT=$(mktemp)
cat << PYEOF > "$TEST_SCRIPT"
import sys
import os

# Append the project scripts directory so agent_driver can be imported
sys.path.insert(0, os.path.join("$PROJECT_DIR", "scripts"))

try:
    from agent_driver import invoke_agent
except ImportError as e:
    print(f"Failed to import agent_driver: {e}")
    sys.exit(1)

task = "Respond with a simple 'OK' if you receive this message. This is a connectivity test."
print("Testing Gemini driver invocation...")

try:
    # We bypass the actual execution in the test if gemini is not available on this CI
    # But since it's an isolated integration test, it's expected to run.
    session = invoke_agent(task, role="test_harness")
    if session:
        print("Test successful, session created.")
    else:
        print("Test failed, no session created.")
        sys.exit(1)
except Exception as e:
    print(f"Test failed with exception: {e}")
    sys.exit(1)
PYEOF

python3 "$TEST_SCRIPT"
RESULT=$?

rm -f "$TEST_SCRIPT"

if [ $RESULT -eq 0 ]; then
    echo "==========================================="
    echo "✅ Isolated E2E Test Passed"
    echo "==========================================="
    exit 0
else
    echo "==========================================="
    echo "❌ Isolated E2E Test Failed"
    echo "==========================================="
    exit 1
fi
