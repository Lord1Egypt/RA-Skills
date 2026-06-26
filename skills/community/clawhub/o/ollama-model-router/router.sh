#!/bin/bash
# Model Router — Route tasks to optimal Ollama model
# Usage: router.sh "your task description"

set -euo pipefail

TASK="${1:-}"
REGISTRY="${MODEL_REGISTRY:-$HOME/.openclaw/model-registry.json}"
PREFER_LOCAL="${PREFER_LOCAL:-false}"
PREFER_SPEED="${PREFER_SPEED:-false}"

if [ -z "$TASK" ]; then
  echo "Usage: router.sh \"your task description\""
  echo ""
  echo "Environment variables:"
  echo "  MODEL_REGISTRY    Path to registry JSON (default: ~/.openclaw/model-registry.json)"
  echo "  PREFER_LOCAL      true/false (default: false)"
  echo "  PREFER_SPEED      true/false (default: false)"
  exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "Error: jq is required. Install with: brew install jq"
  exit 1
fi

# Check if registry exists
if [ ! -f "$REGISTRY" ]; then
  echo "Error: Model registry not found at $REGISTRY"
  echo "Create one with: cp ~/.openclaw/workspace/skills/model-router/registry.example.json ~/.openclaw/model-registry.json"
  exit 1
fi

# Classify task type
classify_task() {
  local task="$1"
  local lower_task=$(echo "$task" | tr '[:upper:]' '[:lower:]')
  
  if echo "$lower_task" | grep -qiE "code|function|bug|refactor|syntax|error|debug|implement|program|script|class|method"; then
    echo "coding"
  elif echo "$lower_task" | grep -qiE "analyse|compare|evaluate|why|how.*does|explain|logic|reason|think|inference"; then
    echo "reasoning"
  elif echo "$lower_task" | grep -qiE "write|story|poem|draft|design|creative|brainstorm|imagine|compose"; then
    echo "creative"
  elif echo "$lower_task" | grep -qiE "data|summary|extract|parse|metrics|report|analyse.*data|visuali[sz]e"; then
    echo "analysis"
  elif echo "$lower_task" | grep -qiE "config|setup|install|deploy|architecture|build|docker|k8s|kubernetes"; then
    echo "technical"
  else
    echo "general"
  fi
}

# Check if Ollama is running and model is available
check_model_available() {
  local model="$1"
  if ! curl -s "http://localhost:11434/api/tags" 2>/dev/null | jq -e --arg m "$model" '.models[] | select(.name == $m)' > /dev/null; then
    return 1
  fi
  return 0
}

# Score models for task type
score_models() {
  local task_type="$1"
  local prefer_local="$2"
  local prefer_speed="$3"
  
  jq -r --arg type "$task_type" \
        --arg local "$prefer_local" \
        --arg speed "$prefer_speed" \
        '
    .models | map(
      . as $m |
      ($m.tags | map(ascii_downcase) | index($type) // -1) as $tag_match |
      ($m.strengths | map(ascii_downcase) | index($type) // -1) as $strength_match |
      (
        (if $tag_match >= 0 then 3 else 0 end) +
        (if $strength_match >= 0 then 2 else 0 end) +
        (if $m.host == "local" and $local == "true" then 1 else 0 end) +
        (if ($m.speed | ascii_downcase) == "very-fast" and $speed == "true" then 2 
         elif ($m.speed | ascii_downcase) == "fast" and $speed == "true" then 1 
         else 0 end)
      ) as $score |
      {
        id: $m.id,
        provider: $m.provider,
        host: $m.host,
        score: $score,
        speed: $m.speed,
        max_tokens: $m.max_tokens
      }
    ) | sort_by(-.score)
  ' "$REGISTRY"
}

# Main
TASK_TYPE=$(classify_task "$TASK")
echo "Task: $TASK"
echo "Type: $TASK_TYPE"
echo ""

# Get scored models
SCORED=$(score_models "$TASK_TYPE" "$PREFER_LOCAL" "$PREFER_SPEED")

# Find first available model
RECOMMENDED=""
REASON=""

while IFS= read -r model; do
  ID=$(echo "$model" | jq -r '.id')
  HOST=$(echo "$model" | jq -r '.host')
  SCORE=$(echo "$model" | jq -r '.score')
  SPEED=$(echo "$model" | jq -r '.speed')
  
  if [ "$SCORE" -lt 0 ]; then continue; fi
  
  # Check availability
  AVAILABLE=false
  if [ "$HOST" == "local" ]; then
    if check_model_available "$ID"; then
      AVAILABLE=true
    fi
  else
    # Cloud models assumed available (could add ping check)
    AVAILABLE=true
  fi
  
  if [ "$AVAILABLE" = true ]; then
    RECOMMENDED="$ID"
    REASON="Best match for $TASK_TYPE (score: $SCORE, speed: $SPEED, host: $HOST)"
    break
  fi
done <>(echo "$SCORED" | jq -c '.[]')

if [ -n "$RECOMMENDED" ]; then
  echo "Recommended: $RECOMMENDED"
  echo "Reason: $REASON"
  echo ""
  echo "Command: ollama run $RECOMMENDED"
  
  # Output JSON for programmatic use
  echo ""
  echo '{"model": "'"$RECOMMENDED"'", "reason": "'"$REASON"'", "task_type": "'"$TASK_TYPE"'"}'
else
  echo "No suitable model found. Available models:"
  curl -s http://localhost:11434/api/tags 2>/dev/null | jq -r '.models[].name' || echo "Ollama not running"
  exit 1
fi