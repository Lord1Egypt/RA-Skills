#!/bin/bash
# Final integration test script for nano-gpt-plugin
# Based on working manual tests with proper timing

set -euo pipefail

# Configuration
DATE=$(date +%Y-%m-%d)
PLUGIN_DIR="/workspace/nano-gpt-plugin"
REMOTE_HOST="ssh_gateway"
REMOTE_PLUGIN_DIR="/tmp/nano-gpt-plugin-$DATE"

echo "Starting final integration test for nano-gpt-plugin"
echo "Date: $DATE"
echo "Plugin directory: $PLUGIN_DIR"
echo "Remote host: $REMOTE_HOST"


set -x

# 1) Sync plugin to remote
echo "Step 1: Syncing plugin to remote host..."
tar --exclude='.git' --exclude='node_modules' --exclude='pnpm-lock.yaml' -czf - . | \
  ssh -o ConnectTimeout=30 "$REMOTE_HOST" "rm -rf $REMOTE_PLUGIN_DIR 2>/dev/null; mkdir -p $REMOTE_PLUGIN_DIR && tar -xzf - -C $REMOTE_PLUGIN_DIR"

# 2) Remove existing plugin and install
echo "Step 2: Installing plugin..."
ssh -o ConnectTimeout=120 "$REMOTE_HOST" "set -x ; rm -rf /home/node/.openclaw/extensions/nano-gpt 2>/dev/null; rm ~/.openclaw/agents/main/sessions/* ;cd '$REMOTE_PLUGIN_DIR'; openclaw plugins install '$REMOTE_PLUGIN_DIR' "

# 3) Start gateway
echo "Step 3: Starting gateway..."
ssh -o ConnectTimeout=30 "$REMOTE_HOST" "nohup openclaw gateway run > /tmp/gateway.log 2>&1 & sleep 5; openclaw gateway health"

# 4) Onboard with NanoGPT
echo "Step 4: Onboarding with NanoGPT..."
ssh -o ConnectTimeout=30 "$REMOTE_HOST" "openclaw onboard --non-interactive --accept-risk --nano-gpt-api-key \"$NANOGPT_API_KEY\" --flow quickstart --skip-health"

# 5) Set default model
echo "Step 5: Setting default model..."
ssh -o ConnectTimeout=30 "$REMOTE_HOST" "openclaw models set nano-gpt/minimax/minimax-m2.7"

ssh -o ConnectTimeout=30 "$REMOTE_HOST" "openclaw models list"

# 6) Run test agent with proper session ID
echo "Step 6: Running test agent..."
ssh -o ConnectTimeout=30 "$REMOTE_HOST" "
  SESSION_ID=\"test-nano-final-\$(date +%s)\"
  echo \"Using session ID: \$SESSION_ID\"
  openclaw agent --session-id \"\$SESSION_ID\" --message 'My name is Test. You are Helper. Say hello.' --timeout 120
  
  # Give it a moment to finish
  sleep 2
  
  # Save the session ID for collection
  echo \"\$SESSION_ID\" > /tmp/last_session_id.txt
"

# 7) Wait a bit more for file to be written
echo "Step 7: Waiting for session file to be written..."
sleep 3

# 8) Collect gateway logs (contains prepareExtraParams debug output)
echo "Step 8: Collecting gateway logs..."
mkdir -p "$PLUGIN_DIR/test_results/$DATE"
scp "$REMOTE_HOST:/tmp/gateway.log" "$PLUGIN_DIR/test_results/$DATE/gateway.log" 2>/dev/null || true

# 9) Collect results
echo "Step 9: Collecting results..."
LAST_SESSION_ID=$(ssh -o ConnectTimeout=30 "$REMOTE_HOST" "cat /tmp/last_session_id.txt 2>/dev/null || echo 'test-nano-final-$(date +%s)'")
echo "Looking for session: $LAST_SESSION_ID"

scp "$REMOTE_HOST:/home/node/.openclaw/agents/main/session/${LAST_SESSION_ID}.jsonl" "$PLUGIN_DIR/test_results/$DATE/" 2>/dev/null || true

# Also collect any test-nano files from recent runs as fallback
scp "$REMOTE_HOST:/home/node/.openclaw/agents/main/sessions/test-nano-*.jsonl" "$PLUGIN_DIR/test_results/$DATE/" 2>/dev/null || true

echo "Results collected to: $PLUGIN_DIR/test_results/$DATE/"
ls -la "$PLUGIN_DIR/test_results/$DATE/" || echo "No files in results directory"

# 10) Verify prepareExtraParams debug logs were captured
echo "Step 10: Checking for prepareExtraParams debug logs..."
if grep -q "prepareExtraParams" "$PLUGIN_DIR/test_results/$DATE/gateway.log" 2>/dev/null; then
  echo "SUCCESS: prepareExtraParams debug logs found in gateway.log"
  grep "prepareExtraParams" "$PLUGIN_DIR/test_results/$DATE/gateway.log"
else
  echo "WARNING: No prepareExtraParams debug logs found"
fi

echo "Integration test completed successfully!"
