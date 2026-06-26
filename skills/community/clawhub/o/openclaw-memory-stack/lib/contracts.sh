#!/usr/bin/env bash
# OpenClaw Memory Stack — Contract helpers
# Sourced by all wrappers for building adapter contract JSON responses.

SCRIPT_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_LIB_DIR/platform.sh"

# Build a successful contract response
# Usage: contract_success <query> <backend> <results_json_array> <result_count> <duration_ms> <normalized_relevance>
contract_success() {
  local query="$1" backend="$2" results="$3" count="$4" duration="$5" relevance="$6"
  local status="success"
  [ "$count" -eq 0 ] && status="empty"

  local escaped_query
  escaped_query=$(json_escape "$query")

  cat <<ENDJSON
{
  "query_echo": "$escaped_query",
  "results": $results,
  "result_count": $count,
  "status": "$status",
  "error_message": null,
  "error_code": null,
  "backend_duration_ms": $duration,
  "normalized_relevance": $relevance,
  "backend": "$backend"
}
ENDJSON
}

# Build an error contract response
# Usage: contract_error <query> <backend> <error_code> <error_message>
contract_error() {
  local query="$1" backend="$2" code="$3" message="$4"
  local escaped_query escaped_msg
  escaped_query=$(json_escape "$query")
  escaped_msg=$(json_escape "$message")

  cat <<ENDJSON
{
  "query_echo": "$escaped_query",
  "results": [],
  "result_count": 0,
  "status": "error",
  "error_message": "$escaped_msg",
  "error_code": "$code",
  "backend_duration_ms": 0,
  "normalized_relevance": 0.0,
  "backend": "$backend"
}
ENDJSON
}

# Build an unavailable contract response
# Usage: contract_unavailable <query> <backend> [message]
contract_unavailable() {
  local query="$1" backend="$2" message="${3:-Backend $backend is not available}"
  contract_error "$query" "$backend" "BACKEND_UNAVAILABLE" "$message"
}

# Build an empty result contract response
# Usage: contract_empty <query> <backend> <duration_ms>
contract_empty() {
  local query="$1" backend="$2" duration="$3"
  contract_success "$query" "$backend" "[]" 0 "$duration" "0.0"
}

# Build a single result entry (for assembling results arrays)
# Usage: result_entry <content> <relevance> <source> [timestamp]
result_entry() {
  local content="$1" relevance="$2" source="$3" timestamp="${4:-$(now_iso)}"
  local escaped_content
  escaped_content=$(json_escape "$content")

  cat <<ENDJSON
{"content": "$escaped_content", "relevance": $relevance, "source": "$source", "timestamp": "$timestamp"}
ENDJSON
}

# Validate contract JSON has required 9 fields
# Usage: validate_contract <json_string>
# Returns 0 if valid, 1 if invalid (prints missing fields to stderr)
validate_contract() {
  local json="$1"
  local required_fields=("query_echo" "results" "result_count" "status" "error_message" "error_code" "backend_duration_ms" "normalized_relevance" "backend")
  local missing=()

  if has_command jq; then
    for field in "${required_fields[@]}"; do
      if ! echo "$json" | jq -e "has(\"$field\")" &>/dev/null; then
        missing+=("$field")
      fi
    done
  elif has_command python3; then
    local missing_str
    missing_str=$(python3 -c "
import json,sys
d=json.loads('''$json''')
required=$( printf '%s' "${required_fields[*]}" | python3 -c "import sys; print(sys.stdin.read().split())" )
missing=[f for f in $( printf "'%s'," "${required_fields[@]}" | sed 's/,$//' | sed 's/^/[/;s/$/]/' ) if f not in d]
print(' '.join(missing))
" 2>/dev/null)
    if [ -n "$missing_str" ]; then
      read -ra missing <<< "$missing_str"
    fi
  fi

  if [ ${#missing[@]} -gt 0 ]; then
    echo "Missing fields: ${missing[*]}" >&2
    return 1
  fi
  return 0
}

# Build a health check response (four-state model)
# Usage: contract_health <backend> <status> [reason]
# Status: ready | degraded | installed | unavailable
contract_health() {
  local backend="$1" status="$2" reason="${3:-}"
  local escaped_reason
  escaped_reason=$(json_escape "$reason")
  cat <<ENDJSON
{"backend": "$backend", "status": "$status", "reason": "$escaped_reason"}
ENDJSON
}
