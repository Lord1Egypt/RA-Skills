#!/bin/bash
# Standard callback helper for Claude Code orchestrator notify hooks.
# Sends a concise completion packet back into an OpenClaw session.
#
# Usage:
#   notify-openclaw.sh <agent-id> <session-id> [lane-label]
#
# Consumes env vars exported by cc-orchestrator.sh:
#   CC_NOTIFY_TASK_ID
#   CC_NOTIFY_STATUS
#   CC_NOTIFY_COST_USD
#   CC_NOTIFY_RESULT_PREVIEW
#   CC_NOTIFY_EXPECTED_FILE
#   CC_NOTIFY_EXPECTED_FILE_EXISTS
#   CC_NOTIFY_EXPECTED_FILE_BYTES
#   CC_NOTIFY_VERIFIED
#   CC_NOTIFY_NEXT_ACTION
#   CC_NOTIFY_CONTINUATION_MODE
#   CC_NOTIFY_SESSION_ID

set -euo pipefail

AGENT_ID="${1:-main}"
SESSION_ID="${2:-}"
LANE_LABEL="${3:-claude-code-lane}"

if [ -z "$SESSION_ID" ]; then
  echo "Usage: $0 <agent-id> <session-id> [lane-label]" >&2
  exit 1
fi

STATUS="${CC_NOTIFY_STATUS:-unknown}"
TASK_ID="${CC_NOTIFY_TASK_ID:-unknown}"
COST="${CC_NOTIFY_COST_USD:-0}"
PREVIEW="${CC_NOTIFY_RESULT_PREVIEW:-}"
EXPECTED_FILE="${CC_NOTIFY_EXPECTED_FILE:-}"
EXPECTED_EXISTS="${CC_NOTIFY_EXPECTED_FILE_EXISTS:-False}"
EXPECTED_BYTES="${CC_NOTIFY_EXPECTED_FILE_BYTES:-0}"
VERIFIED="${CC_NOTIFY_VERIFIED:-False}"
NEXT_ACTION="${CC_NOTIFY_NEXT_ACTION:-}"
CONT_MODE="${CC_NOTIFY_CONTINUATION_MODE:-}"
RUN_SESSION_ID="${CC_NOTIFY_SESSION_ID:-}"

MSG=$(cat <<EOF
CLAUDE_CODE_CALLBACK [$LANE_LABEL]
- task_id: $TASK_ID
- status: $STATUS
- verified: $VERIFIED
- expected_file: $EXPECTED_FILE
- file_exists: $EXPECTED_EXISTS
- file_bytes: $EXPECTED_BYTES
- next_action: $NEXT_ACTION
- continuation_mode: $CONT_MODE
- run_session_id: $RUN_SESSION_ID
- cost_usd: $COST
- result_preview: ${PREVIEW:0:180}

Required parent action now: choose exactly one -> continue | switch | blocked
EOF
)

openclaw agent --agent "$AGENT_ID" --session-id "$SESSION_ID" --message "$MSG" >/dev/null
