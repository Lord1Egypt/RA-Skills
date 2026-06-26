#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUDIT_LOG="$BASE_DIR/reports/audit-events.jsonl"
FAILURE_LOG="$BASE_DIR/reports/failure-dataset.json"

mkdir -p "$(dirname "$AUDIT_LOG")"

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

# Write a single audit event to the JSONL log
# Usage: audit_write <json_string>
audit_write(){
  if [[ ! -f "$AUDIT_LOG" ]]; then
    touch "$AUDIT_LOG"
    chmod 600 "$AUDIT_LOG"
  fi
  echo "$1" >> "$AUDIT_LOG"
}

# Build and write a structured audit event
# Args: --intent --input --risk --decision --evidence --outcome [--reason] [--skill] [--command]
cmd_log(){
  require_jq
  local intent="" input="" risk="" decision="" evidence="" outcome="" reason="" skill="" command=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --intent)   [[ $# -ge 2 ]] || { echo "error: missing --intent" >&2; exit 1; };   intent="$2";   shift 2 ;;
      --input)    [[ $# -ge 2 ]] || { echo "error: missing --input" >&2; exit 1; };    input="$2";    shift 2 ;;
      --risk)     [[ $# -ge 2 ]] || { echo "error: missing --risk" >&2; exit 1; };     risk="$2";     shift 2 ;;
      --decision) [[ $# -ge 2 ]] || { echo "error: missing --decision" >&2; exit 1; }; decision="$2"; shift 2 ;;
      --evidence) [[ $# -ge 2 ]] || { echo "error: missing --evidence" >&2; exit 1; }; evidence="$2"; shift 2 ;;
      --outcome)  [[ $# -ge 2 ]] || { echo "error: missing --outcome" >&2; exit 1; };  outcome="$2";  shift 2 ;;
      --reason)   [[ $# -ge 2 ]] || { echo "error: missing --reason" >&2; exit 1; };   reason="$2";   shift 2 ;;
      --skill)    [[ $# -ge 2 ]] || { echo "error: missing --skill" >&2; exit 1; };    skill="$2";    shift 2 ;;
      --command)  [[ $# -ge 2 ]] || { echo "error: missing --command" >&2; exit 1; };  command="$2";  shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$intent" ]]   || { echo "error: --intent required" >&2; exit 1; }
  [[ -n "$risk" ]]     || { echo "error: --risk required" >&2; exit 1; }
  [[ -n "$decision" ]] || { echo "error: --decision required" >&2; exit 1; }
  [[ -n "$outcome" ]]  || { echo "error: --outcome required" >&2; exit 1; }

  case "$risk" in
    low|medium|high|critical) ;;
    *) echo "error: --risk must be low|medium|high|critical" >&2; exit 1 ;;
  esac
  case "$decision" in
    allow|block|prompt|dry-run) ;;
    *) echo "error: --decision must be allow|block|prompt|dry-run" >&2; exit 1 ;;
  esac
  case "$outcome" in
    success|failure|blocked|pending|approved|rejected) ;;
    *) echo "error: --outcome must be success|failure|blocked|pending|approved|rejected" >&2; exit 1 ;;
  esac

  local ts
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # Redact potential secrets from input before logging
  # Covers: key=value pairs, Bearer tokens, AWS keys, GitHub tokens (ghp_/gho_/ghs_),
  # base64-encoded blobs, hex strings, and generic long opaque strings
  local safe_input
  safe_input=$(echo "$input" | sed -E \
    -e 's/(token|key|password|secret|credential|api[_-]?key|private[_-]?key|auth|bearer)[=: ]*[^ "]+/\1=***REDACTED***/gi' \
    -e 's/Bearer [A-Za-z0-9._~+\/-]+/Bearer ***REDACTED***/g' \
    -e 's/AKIA[0-9A-Z]{16}/***AWS_KEY_REDACTED***/g' \
    -e 's/gh[pso]_[A-Za-z0-9_]{36,}/***GH_TOKEN_REDACTED***/g' \
    -e 's/sk-[A-Za-z0-9]{20,}/***API_KEY_REDACTED***/g' \
    -e 's/eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/***JWT_REDACTED***/g' \
    -e 's/[0-9a-fA-F]{32,}/***HEX_REDACTED***/g' \
    -e 's/[A-Za-z0-9+\/]{40,}={0,2}/***BASE64_REDACTED***/g' \
    -e 's/[A-Za-z0-9_-]{20,}/***LONG_STRING_REDACTED***/g')

  local event
  event=$(jq -nc \
    --arg ts "$ts" \
    --arg intent "$intent" \
    --arg input "$safe_input" \
    --arg risk "$risk" \
    --arg decision "$decision" \
    --arg evidence "$evidence" \
    --arg outcome "$outcome" \
    --arg reason "$reason" \
    --arg skill "$skill" \
    --arg command "$command" \
    '{
      timestamp: $ts,
      intent: $intent,
      input: (if $input == "" then null else $input end),
      risk: $risk,
      decision: $decision,
      evidence: (if $evidence == "" then null else $evidence end),
      outcome: $outcome,
      reason: (if $reason == "" then null else $reason end),
      skill: (if $skill == "" then null else $skill end),
      command: (if $command == "" then null else $command end)
    }')

  audit_write "$event"
  echo "$event"
}

# Collect a failure/false-positive sample for the evolution pipeline
cmd_collect_failure(){
  require_jq
  local event_json="$1"

  if [[ ! -f "$FAILURE_LOG" ]]; then
    echo '{"failures":[]}' > "$FAILURE_LOG"
    chmod 600 "$FAILURE_LOG"
  fi

  jq --argjson evt "$event_json" '.failures += [$evt]' "$FAILURE_LOG" > "$FAILURE_LOG.tmp" \
    && mv "$FAILURE_LOG.tmp" "$FAILURE_LOG"
  echo "failure sample collected"
}

# Query audit stats
cmd_stats(){
  require_jq
  if [[ ! -f "$AUDIT_LOG" ]]; then
    echo "NO_EVENTS"
    return
  fi

  local total blocked high_risk
  total=$(wc -l < "$AUDIT_LOG" | tr -d ' ')
  blocked=$(jq -s '[.[] | select(.decision == "block")] | length' "$AUDIT_LOG")
  high_risk=$(jq -s '[.[] | select(.risk == "high" or .risk == "critical")] | length' "$AUDIT_LOG")

  echo "total_events: $total"
  echo "blocked: $blocked"
  echo "high_risk: $high_risk"
  echo "block_rate: $(echo "scale=2; $blocked * 100 / ($total + 1)" | bc)%"
}

main(){
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    log)             cmd_log "$@" ;;
    collect-failure) cmd_collect_failure "$@" ;;
    stats)           cmd_stats ;;
    *) echo "usage: audit.sh {log|collect-failure|stats}" >&2; exit 1 ;;
  esac
}

main "$@"
