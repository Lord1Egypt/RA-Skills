#!/bin/bash
# ==========================================
# skill_test_runner.sh
# Implements PRD_010 Section 3.4 (Skill Test Runner Protocol)
# ==========================================

SKILL_PATH="$1"
TEST_PROMPT="${2:-READY?}"

if [ -z "$SKILL_PATH" ]; then
    echo "Usage: $0 <SKILL_PATH> [TEST_PROMPT]"
    exit 1
fi

# Generate a unique validation token to prevent false positives from prompt echoing
V_TOKEN="$(date +%s)_$RANDOM"

echo "=================================================="
echo "[skill_test_runner] 🚀 Spawning sub-agent test runner..."
echo "[skill_test_runner] 📂 Target Skill: $SKILL_PATH"
echo "[skill_test_runner] 💬 Test Prompt: $TEST_PROMPT"
echo "[skill_test_runner] 🔑 Validation Token: $V_TOKEN"
echo "=================================================="

SESSION_ID="test-runner-$(date +%s)-$RANDOM"

META_PROMPT="You are an autonomous QA Test Runner sub-agent.
Your strict protocol:
1. Locate and read the skill documentation at: $SKILL_PATH/SKILL.md to understand its behavior.
2. Execute the user's test prompt: '$TEST_PROMPT' using whatever tools the skill provides.
3. Critically evaluate if the test prompt was successfully executed according to the skill's defined purpose.
4. MANDATORY: If the execution was successful and valid, you MUST output the exact string 'PASSED_' concatenated with the validation token '$V_TOKEN' (e.g., if token is 123, output PASSED_123) on a new line at the very end of your final response. If it fails or errors, output 'FAILED_' concatenated with the token.
Begin execution now."

TMP_LOG=$(mktemp)
openclaw agent --session-id "$SESSION_ID" -m "$META_PROMPT" | tee "$TMP_LOG"

echo ""
echo "=================================================="
echo "[skill_test_runner] 📊 Evaluation Phase"

# Since the prompt explains concatenation, the exact string PASSED_$V_TOKEN will only exist if the agent generated it.
if grep -q "PASSED_$V_TOKEN" "$TMP_LOG"; then
    echo "[skill_test_runner] ✅ SUCCESS: Valid verification token (PASSED_$V_TOKEN) detected."
    rm -f "$TMP_LOG"
    exit 0
else
    echo "[skill_test_runner] ❌ FAILURE: Verification token not found or test failed."
    rm -f "$TMP_LOG"
    exit 1
fi