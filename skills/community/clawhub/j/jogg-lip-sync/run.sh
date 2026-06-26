#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ENV_FILE="$SCRIPT_DIR/.env"

load_default_env() {
  [ -f "$ENV_FILE" ] || return 0
  while IFS= read -r raw_line || [ -n "$raw_line" ]; do
    line=$(printf '%s' "$raw_line" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
    [ -n "$line" ] || continue
    case "$line" in
      \#*) continue ;;
      export\ *) line=${line#export } ;;
    esac
    case "$line" in
      *=*) ;;
      *) continue ;;
    esac
    key=${line%%=*}
    value=${line#*=}
    key=$(printf '%s' "$key" | sed 's/[[:space:]]*$//')
    value=$(printf '%s' "$value" | sed 's/^[[:space:]]*//')
    case "$key" in
      ''|[0-9]*|*[!A-Za-z0-9_]*)
        continue
        ;;
    esac
    eval "existing_value=\${$key-}"
    if [ -n "${existing_value:-}" ]; then
      continue
    fi
    case "$value" in
      \"*\")
        value=${value#\"}
        value=${value%\"}
        ;;
      \'*\')
        value=${value#\'}
        value=${value%\'}
        ;;
    esac
    export "$key=$value"
  done < "$ENV_FILE"
}

load_default_env

if ! command -v jq >/dev/null 2>&1; then
  printf '%s\n' '{"error":"jq is required"}' >&2
  exit 1
fi

: "${JOGG_BASE_URL:=https://api.jogg.ai}"
: "${JOGG_API_PLATFORM:=openclaw}"
: "${JOGG_LIP_SYNC_DEFAULT_PLAYBACK_TYPE:=normal}"
: "${JOGG_LIP_SYNC_DEFAULT_POLL_INTERVAL_SECONDS:=10}"
: "${JOGG_LIP_SYNC_DEFAULT_MAX_WAIT_SECONDS:=1800}"
export JOGG_BASE_URL JOGG_API_PLATFORM JOGG_LIP_SYNC_DEFAULT_PLAYBACK_TYPE JOGG_LIP_SYNC_DEFAULT_POLL_INTERVAL_SECONDS JOGG_LIP_SYNC_DEFAULT_MAX_WAIT_SECONDS

PLAYBACK_TYPE="${JOGG_LIP_SYNC_DEFAULT_PLAYBACK_TYPE:-normal}"
TASK_ID=""
VIDEO_INPUT=""
AUDIO_INPUT=""
FORCE_RECREATE="false"
POLL_MODE="default"
POLL_INTERVAL_SECONDS="${JOGG_LIP_SYNC_DEFAULT_POLL_INTERVAL_SECONDS:-5}"
MAX_WAIT_SECONDS="${JOGG_LIP_SYNC_DEFAULT_MAX_WAIT_SECONDS:-1800}"
LAST_JSON=""
RESPONSE_STATUS=""
RESPONSE_BODY=""

print_help() {
  cat <<'EOF'
usage: run.sh [--video VIDEO] [--audio AUDIO]
             [--playback-type normal|normal_reverse|normal_reverse_by_audio]
             [--task-id TASK_ID] [--force-recreate] [--poll] [--no-poll]
             [--poll-interval-seconds SECONDS]
             [--max-wait-seconds SECONDS]

Run or query Jogg lip sync tasks.

Environment:
  .env in this directory is auto-loaded as defaults.
EOF
}

json_error() {
  error_message=$1
  error_code=${2:-}
  if [ -n "$error_code" ]; then
    jq -cn --arg error "$error_message" --argjson code "$error_code" '{error:$error, code:$code}' >&2
  else
    jq -cn --arg error "$error_message" '{error:$error}' >&2
  fi
}

json_config_error() {
  missing_key=$1
  jq -cn \
    --arg error "missing required configuration: $missing_key" \
    --arg missing_key "$missing_key" \
    --arg env_file ".env" \
    --arg action "update .env or set the environment variable before running again" \
    '{
      error: $error,
      missing_key: $missing_key,
      env_file: $env_file,
      action: $action
    }' >&2
}

log_progress() {
  message=$1
  printf '[jogg-lip-sync] %s\n' "$message" >&2
}

run_with_heartbeat() {
  label=$1
  shift
  "$@" &
  cmd_pid=$!
  start_at=$(date +%s)

  while kill -0 "$cmd_pid" 2>/dev/null; do
    now=$(date +%s)
    elapsed=$((now - start_at))
    log_progress "$label ... ${elapsed}s elapsed"
    sleep 3
  done

  wait "$cmd_pid"
  cmd_exit_code=$?
  return "$cmd_exit_code"
}

require_env() {
  var_name=$1
  eval "var_value=\${$var_name:-}"
  var_value=$(printf '%s' "$var_value" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
  if [ -z "$var_value" ]; then
    json_config_error "$var_name"
    exit 1
  fi
}

api_request() {
  method=$1
  url=$2
  payload=${3:-}
  body_file=$(mktemp)

  if [ -n "$payload" ]; then
    if [ -n "${JOGG_API_PLATFORM:-}" ]; then
      RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "$url" \
        -H "X-Api-Key: ${JOGG_API_KEY}" \
        -H "x-api-platform: ${JOGG_API_PLATFORM}" \
        -H "Content-Type: application/json" \
        -d "$payload") || {
          rm -f "$body_file"
          json_error "request failed"
          exit 1
        }
    else
      RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "$url" \
        -H "X-Api-Key: ${JOGG_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload") || {
          rm -f "$body_file"
          json_error "request failed"
          exit 1
        }
    fi
  else
    if [ -n "${JOGG_API_PLATFORM:-}" ]; then
      RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "$url" \
        -H "X-Api-Key: ${JOGG_API_KEY}" \
        -H "x-api-platform: ${JOGG_API_PLATFORM}") || {
          rm -f "$body_file"
          json_error "request failed"
          exit 1
        }
    else
      RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "$url" \
        -H "X-Api-Key: ${JOGG_API_KEY}") || {
          rm -f "$body_file"
          json_error "request failed"
          exit 1
        }
    fi
  fi

  RESPONSE_BODY=$(cat "$body_file")
  rm -f "$body_file"
}

api_success_data() {
  api_code=$(printf '%s' "$RESPONSE_BODY" | jq -r '.code // empty')
  if [ "$api_code" = "0" ]; then
    LAST_JSON=$(printf '%s' "$RESPONSE_BODY" | jq -c '.data')
    return 0
  fi
  api_message=$(printf '%s' "$RESPONSE_BODY" | jq -r '.msg // "api request failed"')
  json_error "$api_message" "$api_code"
  exit 1
}

guess_content_type() {
  file_name=$1
  case $(printf '%s' "$file_name" | tr '[:upper:]' '[:lower:]') in
    *.mp4) printf '%s' 'video/mp4' ;;
    *.mov) printf '%s' 'video/quicktime' ;;
    *.m4v) printf '%s' 'video/x-m4v' ;;
    *.webm) printf '%s' 'video/webm' ;;
    *.mp3) printf '%s' 'audio/mpeg' ;;
    *.wav) printf '%s' 'audio/wav' ;;
    *.m4a) printf '%s' 'audio/mp4' ;;
    *.aac) printf '%s' 'audio/aac' ;;
    *.ogg) printf '%s' 'audio/ogg' ;;
    *) printf '%s' 'application/octet-stream' ;;
  esac
}

normalize_media_input() {
  media_input=$1
  if printf '%s' "$media_input" | grep -Eq '^https?://'; then
    log_progress "using remote media url: $media_input"
    printf '%s' "$media_input"
    return 0
  fi

  if [ ! -f "$media_input" ]; then
    json_error "file does not exist: $media_input"
    exit 1
  fi

  file_name=$(basename "$media_input")
  content_type=$(guess_content_type "$file_name")
  file_size=$(wc -c < "$media_input" | tr -d ' ')
  log_progress "uploading local media: $media_input"
  payload=$(jq -cn \
    --arg filename "$file_name" \
    --arg content_type "$content_type" \
    --argjson file_size "$file_size" \
    '{filename:$filename, content_type:$content_type, file_size:$file_size}')

  api_request "POST" "${JOGG_BASE_URL%/}/v2/upload/asset" "$payload"
  api_success_data
  sign_url=$(printf '%s' "$LAST_JSON" | jq -r '.sign_url')
  asset_url=$(printf '%s' "$LAST_JSON" | jq -r '.asset_url')

  upload_status_file=$(mktemp)
  run_with_heartbeat "uploading binary to storage" \
    sh -c '
      curl -sS -o /dev/null -w "%{http_code}" -X PUT "$1" -H "Content-Type: $2" --data-binary "@$3" > "$4"
    ' sh "$sign_url" "$content_type" "$media_input" "$upload_status_file" || {
      rm -f "$upload_status_file"
      json_error "upload failed"
      exit 1
    }
  upload_status=$(cat "$upload_status_file")
  rm -f "$upload_status_file"
  if [ -z "$upload_status" ]; then
    json_error "upload failed"
    exit 1
  fi
  case "$upload_status" in
    2*) ;;
    *)
      json_error "upload failed with status $upload_status"
      exit 1
      ;;
  esac

  printf '%s' "$asset_url"
}

query_latest_task() {
  video_url=$1
  audio_url=$2
  playback_type=$3
  body_file=$(mktemp)
  if [ -n "${JOGG_API_PLATFORM:-}" ]; then
    RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -G "${JOGG_BASE_URL%/}/v2/lip_sync_video" \
      -H "X-Api-Key: ${JOGG_API_KEY}" \
      -H "x-api-platform: ${JOGG_API_PLATFORM}" \
      --data-urlencode "video_url=$video_url" \
      --data-urlencode "audio_url=$audio_url" \
      --data-urlencode "playback_type=$playback_type") || {
        rm -f "$body_file"
        json_error "request failed"
        exit 1
      }
  else
    RESPONSE_STATUS=$(curl -sS -o "$body_file" -w "%{http_code}" -G "${JOGG_BASE_URL%/}/v2/lip_sync_video" \
      -H "X-Api-Key: ${JOGG_API_KEY}" \
      --data-urlencode "video_url=$video_url" \
      --data-urlencode "audio_url=$audio_url" \
      --data-urlencode "playback_type=$playback_type") || {
        rm -f "$body_file"
        json_error "request failed"
        exit 1
      }
  fi
  RESPONSE_BODY=$(cat "$body_file")
  rm -f "$body_file"

  api_code=$(printf '%s' "$RESPONSE_BODY" | jq -r '.code // empty')
  if [ "$api_code" = "0" ]; then
    LAST_JSON=$(printf '%s' "$RESPONSE_BODY" | jq -c '.data')
    return 0
  fi
  if [ "$api_code" = "10104" ] || [ "$api_code" = "17003" ]; then
    LAST_JSON=""
    return 1
  fi

  api_message=$(printf '%s' "$RESPONSE_BODY" | jq -r '.msg // "api request failed"')
  json_error "$api_message" "$api_code"
  exit 1
}

create_task() {
  video_url=$1
  audio_url=$2
  playback_type=$3
  payload=$(jq -cn \
    --arg video_url "$video_url" \
    --arg audio_url "$audio_url" \
    --arg playback_type "$playback_type" \
    '{video_url:$video_url, audio_url:$audio_url, playback_type:$playback_type}')
  api_request "POST" "${JOGG_BASE_URL%/}/v2/create_lip_sync_video" "$payload"
  api_success_data
}

get_task() {
  task_id=$1
  api_request "GET" "${JOGG_BASE_URL%/}/v2/lip_sync_video/$task_id"
  api_success_data
}

wait_for_task() {
  task_id=$1
  current_json=""
  started_at=$(date +%s)
  log_progress "polling task: $task_id"
  while :; do
    get_task "$task_id"
    current_json=$LAST_JSON
    status=$(printf '%s' "$current_json" | jq -r '.status')
    log_progress "task status: $status (task_id=$task_id)"
    if [ "$status" = "success" ] || [ "$status" = "failed" ]; then
      LAST_JSON=$current_json
      return 0
    fi
    now=$(date +%s)
    if [ $((now - started_at)) -ge "$MAX_WAIT_SECONDS" ]; then
      LAST_JSON=$current_json
      return 0
    fi
    sleep "$POLL_INTERVAL_SECONDS"
  done
}

emit_result() {
  task_json=$1
  action=$2
  reused=$3
  video_url=${4:-}
  audio_url=${5:-}
  playback_type=${6:-}

  printf '%s' "$task_json" | jq -c \
    --arg action "$action" \
    --argjson reused "$reused" \
    --arg video_url "$video_url" \
    --arg audio_url "$audio_url" \
    --arg playback_type "$playback_type" \
    '{
      action: $action,
      reused: $reused,
      task_id: .task_id,
      status: .status,
      completed: ((.status == "success") or (.status == "failed"))
    }
    + (if $video_url != "" then {video_url: $video_url} else {} end)
    + (if $audio_url != "" then {audio_url: $audio_url} else {} end)
    + (if $playback_type != "" then {playback_type: $playback_type} else {} end)
    + (if (.data.result_url? // "") != "" then {result_url: .data.result_url} else {} end)
    + (if (.data.cover_url? // "") != "" then {cover_url: .data.cover_url} else {} end)
    + (if .data.duration_seconds? != null then {duration_seconds: .data.duration_seconds} else {} end)
    + (if (.error.message? // "") != "" then {error_message: .error.message} else {} end)
    + (if .created_at? != null then {created_at: .created_at} else {} end)
    + (if .completed_at? != null then {completed_at: .completed_at} else {} end)'
}

while [ $# -gt 0 ]; do
  case "$1" in
    --video)
      VIDEO_INPUT=$2
      shift 2
      ;;
    --audio)
      AUDIO_INPUT=$2
      shift 2
      ;;
    --playback-type)
      PLAYBACK_TYPE=$2
      shift 2
      ;;
    --task-id)
      TASK_ID=$2
      shift 2
      ;;
    --force-recreate)
      FORCE_RECREATE="true"
      shift
      ;;
    --poll)
      POLL_MODE="true"
      shift
      ;;
    --no-poll)
      POLL_MODE="false"
      shift
      ;;
    --poll-interval-seconds)
      POLL_INTERVAL_SECONDS=$2
      shift 2
      ;;
    --max-wait-seconds)
      MAX_WAIT_SECONDS=$2
      shift 2
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      json_error "unknown argument: $1"
      exit 1
      ;;
  esac
done

case "$PLAYBACK_TYPE" in
  normal|normal_reverse|normal_reverse_by_audio) ;;
  *)
    json_error "--playback-type is invalid"
    exit 1
    ;;
esac

case "$POLL_INTERVAL_SECONDS" in
  ''|*[!0-9]*)
    json_error "--poll-interval-seconds must be a positive integer"
    exit 1
    ;;
esac

case "$MAX_WAIT_SECONDS" in
  ''|*[!0-9]*)
    json_error "--max-wait-seconds must be a positive integer"
    exit 1
    ;;
esac

if [ "$POLL_INTERVAL_SECONDS" -le 0 ] || [ "$MAX_WAIT_SECONDS" -le 0 ]; then
  json_error "poll intervals must be greater than 0"
  exit 1
fi

if [ -z "$TASK_ID" ] && { [ -z "$VIDEO_INPUT" ] || [ -z "$AUDIO_INPUT" ]; }; then
  json_error "either --task-id or both --video and --audio are required"
  exit 1
fi

require_env "JOGG_API_KEY"

if [ -n "$TASK_ID" ]; then
  log_progress "querying existing task by task_id: $TASK_ID"
  get_task "$TASK_ID"
  if [ "$POLL_MODE" = "true" ]; then
    wait_for_task "$TASK_ID"
  fi
  emit_result "$LAST_JSON" "queried_task" "false"
  exit 0
fi

VIDEO_URL=$(normalize_media_input "$VIDEO_INPUT")
AUDIO_URL=$(normalize_media_input "$AUDIO_INPUT")

log_progress "querying latest matching task"
if query_latest_task "$VIDEO_URL" "$AUDIO_URL" "$PLAYBACK_TYPE"; then
  status=$(printf '%s' "$LAST_JSON" | jq -r '.status')
  should_reuse="false"
  if [ "$status" = "pending" ] || [ "$status" = "processing" ]; then
    should_reuse="true"
  fi
  if [ "$FORCE_RECREATE" = "false" ] && { [ "$status" = "success" ] || [ "$status" = "failed" ]; }; then
    should_reuse="true"
  fi
  if [ "$should_reuse" = "true" ]; then
    log_progress "reusing existing task with status: $status"
    if [ "$POLL_MODE" != "false" ] && [ "$status" != "success" ] && [ "$status" != "failed" ]; then
      task_id=$(printf '%s' "$LAST_JSON" | jq -r '.task_id')
      wait_for_task "$task_id"
    fi
    emit_result "$LAST_JSON" "reused_existing_task" "true" "$VIDEO_URL" "$AUDIO_URL" "$PLAYBACK_TYPE"
    exit 0
  fi
fi

log_progress "creating new lip sync task"
create_task "$VIDEO_URL" "$AUDIO_URL" "$PLAYBACK_TYPE"
created_task_id=$(printf '%s' "$LAST_JSON" | jq -r '.task_id')
created_status=$(printf '%s' "$LAST_JSON" | jq -r '.status')
log_progress "created task: $created_task_id (status=$created_status)"
if [ "$POLL_MODE" != "false" ] && [ "$created_status" != "success" ] && [ "$created_status" != "failed" ]; then
  wait_for_task "$created_task_id"
else
  LAST_JSON=$(jq -cn --arg task_id "$created_task_id" --arg status "$created_status" '{task_id:$task_id, status:$status}')
fi

emit_result "$LAST_JSON" "created_new_task" "false" "$VIDEO_URL" "$AUDIO_URL" "$PLAYBACK_TYPE"
