#!/usr/bin/env bash
# oz-api.sh — Warp Oz Agent API wrapper
# Usage: oz-api.sh <command> [args...]
#
# Commands:
#   run <prompt> [--env ENV_ID] [--name NAME] [--base-prompt TEXT] [--model MODEL] [--title TITLE] [--team]
#   status <run_id>
#   list [--state STATE] [--limit N] [--name NAME] [--source SOURCE]
#   poll <run_id> [--interval 10] [--timeout 600]
#   cancel <run_id>
#   artifacts <artifact_uid>
#   agents                          — list agents (top-level)
#   session-link <session_uuid>     — get session redirect URL
#   schedule-create <prompt> --cron EXPR [--env ENV_ID] [--name NAME] [--base-prompt TEXT]
#   schedule-list
#   schedule-get <schedule_id>
#   schedule-update <schedule_id> [--prompt TEXT] [--cron EXPR] [--env ENV_ID]
#   schedule-delete <schedule_id>
#   schedule-pause <schedule_id>
#   schedule-resume <schedule_id>

set -euo pipefail

API_BASE="https://app.warp.dev/api/v1"

# Override 1Password reference: OP_WARP_REFERENCE="op://your-vault/item/field"
OP_WARP_REFERENCE="${OP_WARP_REFERENCE:-op://your-vault/warp-api-key/credential}"

get_api_key() {
  if [[ -n "${WARP_API_KEY:-}" ]]; then
    echo "$WARP_API_KEY"
  else
    op read "$OP_WARP_REFERENCE" 2>/dev/null || {
      echo "ERROR: No WARP_API_KEY and op read '$OP_WARP_REFERENCE' failed" >&2
      exit 1
    }
  fi
}

api_call() {
  local method="$1" endpoint="$2"
  shift 2
  local key
  key=$(get_api_key)
  curl -sf --max-time 30 -X "$method" "${API_BASE}${endpoint}" \
    -H @<(echo "Authorization: Bearer $key") \
    -H "Content-Type: application/json" \
    "$@"
}

# Fallback: same as api_call but doesn't use -f (shows error bodies)
api_call_verbose() {
  local method="$1" endpoint="$2"
  shift 2
  local key
  key=$(get_api_key)
  local http_code body
  body=$(curl -s --max-time 30 -X "$method" "${API_BASE}${endpoint}" \
    -H @<(echo "Authorization: Bearer $key") \
    -H "Content-Type: application/json" \
    -w "\n%{http_code}" \
    "$@")
  http_code=$(echo "$body" | tail -1)
  body=$(echo "$body" | sed '$d')
  echo "$body"
  if [[ "$http_code" -ge 400 ]]; then
    echo "HTTP $http_code error" >&2
    return 1
  fi
}

cmd_run() {
  local prompt="" env_id="" name="" base_prompt="" model="" title="" team="false"
  local skill="" conversation_id="" interactive="false"
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    prompt="$1"; shift
  fi
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env) env_id="$2"; shift 2 ;;
      --name) name="$2"; shift 2 ;;
      --base-prompt) base_prompt="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --title) title="$2"; shift 2 ;;
      --team) team="true"; shift ;;
      --skill) skill="$2"; shift 2 ;;
      --conversation-id) conversation_id="$2"; shift 2 ;;
      --interactive) interactive="true"; shift ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  [[ -z "$prompt" && -z "$skill" ]] && { echo "ERROR: prompt or --skill required" >&2; exit 1; }
  local json
  json=$(jq -n \
    --arg prompt "$prompt" \
    --arg title "$title" \
    --argjson team "$team" \
    --arg name "$name" \
    --arg model "$model" \
    --arg base_prompt "$base_prompt" \
    --arg env_id "$env_id" \
    --arg skill "$skill" \
    --arg conversation_id "$conversation_id" \
    --argjson interactive "$interactive" \
    '{}
    + (if $prompt != "" then {prompt: $prompt} else {} end)
    + {team: $team}
    + (if $title != "" then {title: $title} else {} end)
    + (if $skill != "" then {skill: $skill} else {} end)
    + (if $conversation_id != "" then {conversation_id: $conversation_id} else {} end)
    + (if $interactive then {interactive: $interactive} else {} end)
    + {config: (
        {}
        + (if $name != "" then {name: $name} else {} end)
        + (if $model != "" then {model_id: $model} else {} end)
        + (if $base_prompt != "" then {base_prompt: $base_prompt} else {} end)
        + (if $env_id != "" then {environment_id: $env_id} else {} end)
      )}
    ')
  api_call POST "/agent/run" -d "$json"
}

cmd_status() {
  local run_id="${1:?run_id required}"
  api_call GET "/agent/runs/${run_id}"
}

cmd_list() {
  local params=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --state) params+="state=$2&"; shift 2 ;;
      --limit) params+="limit=$2&"; shift 2 ;;
      --name) params+="config_name=$2&"; shift 2 ;;
      --source) params+="source=$2&"; shift 2 ;;
      --cursor) params+="cursor=$2&"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  params="${params%&}"
  api_call GET "/agent/runs${params:+?$params}"
}

cmd_poll() {
  local run_id="${1:?run_id required}"; shift
  local interval=10 timeout=600
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --interval) interval="$2"; shift 2 ;;
      --timeout) timeout="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  local elapsed=0
  while (( elapsed < timeout )); do
    local result
    result=$(cmd_status "$run_id")
    local state
    state=$(echo "$result" | jq -r '.state')
    case "$state" in
      SUCCEEDED|FAILED)
        echo "$result"
        return 0
        ;;
      *)
        local msg
        msg=$(echo "$result" | jq -r '.status_message.message // "no status"')
        echo "[$state] $msg (${elapsed}s elapsed)" >&2
        sleep "$interval"
        elapsed=$((elapsed + interval))
        ;;
    esac
  done
  echo "TIMEOUT after ${timeout}s" >&2
  cmd_status "$run_id"
  return 1
}

cmd_cancel() {
  local run_id="${1:?run_id required}"
  api_call_verbose POST "/agent/runs/${run_id}/cancel"
}

cmd_artifacts() {
  local artifact_uid="${1:?artifact_uid required}"
  api_call_verbose GET "/agent/artifacts/${artifact_uid}"
}

cmd_agents() {
  api_call_verbose GET "/agent"
}

cmd_session_link() {
  local session_uuid="${1:?session_uuid required}"
  api_call_verbose GET "/agent/sessions/${session_uuid}/redirect"
}

# --- Schedules ---

cmd_schedule_create() {
  local prompt="" cron="" env_id="" name="" base_prompt="" enabled="true"
  if [[ $# -gt 0 && ! "$1" =~ ^-- ]]; then
    prompt="$1"; shift
  fi
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --cron) cron="$2"; shift 2 ;;
      --env) env_id="$2"; shift 2 ;;
      --name) name="$2"; shift 2 ;;
      --base-prompt) base_prompt="$2"; shift 2 ;;
      --disabled) enabled="false"; shift ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  [[ -z "$prompt" ]] && { echo "ERROR: prompt required" >&2; exit 1; }
  [[ -z "$cron" ]] && { echo "ERROR: --cron required" >&2; exit 1; }
  [[ -z "$name" ]] && { echo "ERROR: --name required" >&2; exit 1; }
  local json
  json=$(jq -n \
    --arg prompt "$prompt" \
    --arg cron_schedule "$cron" \
    --arg name "$name" \
    --argjson enabled "$enabled" \
    --arg base_prompt "$base_prompt" \
    --arg env_id "$env_id" \
    '{
      prompt: $prompt,
      cron_schedule: $cron_schedule,
      name: $name,
      enabled: $enabled
    }
    + {agent_config: (
        {}
        + (if $base_prompt != "" then {base_prompt: $base_prompt} else {} end)
        + (if $env_id != "" then {environment_id: $env_id} else {} end)
      )}
    ')
  api_call_verbose POST "/agent/schedules" -d "$json"
}

cmd_schedule_list() {
  api_call_verbose GET "/agent/schedules"
}

cmd_schedule_get() {
  local schedule_id="${1:?schedule_id required}"
  api_call_verbose GET "/agent/schedules/${schedule_id}"
}

cmd_schedule_update() {
  local schedule_id="${1:?schedule_id required}"; shift
  local prompt="" cron="" env_id="" name="" enabled=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --prompt) prompt="$2"; shift 2 ;;
      --cron) cron="$2"; shift 2 ;;
      --env) env_id="$2"; shift 2 ;;
      --name) name="$2"; shift 2 ;;
      --enabled) enabled="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  [[ -z "$cron" ]] && { echo "ERROR: --cron required for update" >&2; exit 1; }
  [[ -z "$name" ]] && { echo "ERROR: --name required for update" >&2; exit 1; }
  local json
  json=$(jq -n \
    --arg prompt "$prompt" \
    --arg cron_schedule "$cron" \
    --arg name "$name" \
    --arg enabled "$enabled" \
    --arg env_id "$env_id" \
    '{
      cron_schedule: $cron_schedule,
      name: $name
    }
    + (if $enabled != "" then {enabled: ($enabled == "true")} else {} end)
    + (if $prompt != "" then {prompt: $prompt} else {} end)
    + (if $env_id != "" then {agent_config: {environment_id: $env_id}} else {} end)
    ')
  api_call_verbose PUT "/agent/schedules/${schedule_id}" -d "$json"
}

cmd_schedule_delete() {
  local schedule_id="${1:?schedule_id required}"
  api_call_verbose DELETE "/agent/schedules/${schedule_id}"
}

cmd_schedule_pause() {
  local schedule_id="${1:?schedule_id required}"
  api_call_verbose POST "/agent/schedules/${schedule_id}/pause"
}

cmd_schedule_resume() {
  local schedule_id="${1:?schedule_id required}"
  api_call_verbose POST "/agent/schedules/${schedule_id}/resume"
}

# --- Dispatch ---
case "${1:-help}" in
  run)             shift; cmd_run "$@" ;;
  status)          shift; cmd_status "$@" ;;
  list)            shift; cmd_list "$@" ;;
  poll)            shift; cmd_poll "$@" ;;
  cancel)          shift; cmd_cancel "$@" ;;
  artifacts)       shift; cmd_artifacts "$@" ;;
  agents)          shift; cmd_agents ;;
  session-link)    shift; cmd_session_link "$@" ;;
  schedule-create) shift; cmd_schedule_create "$@" ;;
  schedule-list)   shift; cmd_schedule_list ;;
  schedule-get)    shift; cmd_schedule_get "$@" ;;
  schedule-update) shift; cmd_schedule_update "$@" ;;
  schedule-delete) shift; cmd_schedule_delete "$@" ;;
  schedule-pause)  shift; cmd_schedule_pause "$@" ;;
  schedule-resume) shift; cmd_schedule_resume "$@" ;;
  help|*)
    echo "Usage: oz-api.sh <command> [args...]"
    echo ""
    echo "Commands:"
    echo "  run <prompt> [--env ID] [--name N] [--base-prompt T] [--model M] [--title T] [--team] [--skill S] [--conversation-id ID] [--interactive]"
    echo "  status <run_id>"
    echo "  list [--state S] [--limit N] [--name N] [--source S]"
    echo "  poll <run_id> [--interval 10] [--timeout 600]"
    echo "  cancel <run_id>"
    echo "  artifacts <artifact_uid>"
    echo "  agents"
    echo "  session-link <session_uuid>"
    echo "  schedule-create <prompt> --cron EXPR [--env ID] [--name N] [--base-prompt T]"
    echo "  schedule-list"
    echo "  schedule-get <schedule_id>"
    echo "  schedule-update <schedule_id> [--prompt T] [--cron E] [--env ID]"
    echo "  schedule-delete <schedule_id>"
    echo "  schedule-pause <schedule_id>"
    echo "  schedule-resume <schedule_id>"
    ;;
esac
