#!/usr/bin/env bash
set -euo pipefail

# Example glue script for local testing.
# Submit a Manus task, wait for completion, and print the result JSON.
# Actual chat/file sending should stay in OpenClaw tool logic.

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROMPT_SCRIPT="$SCRIPT_DIR/manus_prompt.sh"
WAIT_SCRIPT="$SCRIPT_DIR/manus_wait_and_collect.py"

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 'Manus, generate an image of a rainy forest'" >&2
  exit 1
fi

RAW_RESPONSE="$($PROMPT_SCRIPT "$*")"
echo "$RAW_RESPONSE" >&2

TASK_ID="$(printf '%s' "$RAW_RESPONSE" | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const j=JSON.parse(s);console.log(j.taskId||j.task_id||j.id||'')})")"
if [[ -z "$TASK_ID" ]]; then
  echo "Could not parse task id from submit response" >&2
  exit 1
fi

python3 "$WAIT_SCRIPT" "$TASK_ID" 900
