#!/usr/bin/env bash
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

usage() {
  cat <<'EOF'
Usage:
  myreels-generate.sh <model_name> <json_body>
  myreels-generate.sh --model <model_name> --file <request.json>
  myreels-generate.sh --model <model_name> --file -
  myreels-generate.sh -h | --help

Description:
  Submit a generation task to POST /generation/:modelName.

Arguments:
  <model_name>         Real modelName from /api/v1/models/api
  <json_body>          JSON request body as a single shell argument

Options:
  --model <name>       Same as the positional model_name
  --file <path>        Read the JSON request body from a file
                       Use - to read from stdin

Returns:
  Normalized JSON with taskID and the next polling hint.

Common errors:
  400  Invalid body or missing required parameters
  401  Missing or invalid AccessToken
  402  Insufficient points
  403  Subscription or permission required
  404  modelName not found
  500  Server-side processing error
EOF
}

source "$(dirname "$0")/_common.sh"

model_name=""
body_arg=""
body_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      [[ $# -ge 2 ]] || { echo "Error: --model requires a value" >&2; exit 2; }
      model_name="$2"
      shift 2
      ;;
    --file)
      [[ $# -ge 2 ]] || { echo "Error: --file requires a value" >&2; exit 2; }
      body_file="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -z "$model_name" ]]; then
        model_name="$1"
      elif [[ -z "$body_arg" ]]; then
        body_arg="$1"
      else
        echo "Error: unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      shift
      ;;
  esac
done

[[ -n "$model_name" ]] || { usage >&2; exit 2; }

input_sources=0
[[ -n "$body_arg" ]] && input_sources=$((input_sources + 1))
[[ -n "$body_file" ]] && input_sources=$((input_sources + 1))

if [[ "$input_sources" -ne 1 ]]; then
  echo "Error: provide exactly one request body source: positional JSON or --file" >&2
  usage >&2
  exit 2
fi

if [[ -n "$body_file" ]]; then
  if [[ "$body_file" == "-" ]]; then
    body_arg=$(cat)
  else
    [[ -f "$body_file" ]] || { echo "Error: file not found: $body_file" >&2; exit 1; }
    body_arg=$(cat "$body_file")
  fi
fi

if ! jq -e 'type == "object"' >/dev/null 2>&1 <<<"$body_arg"; then
  echo "Error: request body must be a valid JSON object" >&2
  exit 2
fi

payload=$(myreels_post_auth "/generation/${model_name}" "$body_arg")
myreels_require_api_ok "$payload" "Task submission failed" || exit 1

task_id=$(echo "$payload" | jq -r '.data.taskID // empty')
if [[ -z "$task_id" ]]; then
  echo "Error: task submission response missing data.taskID" >&2
  echo "$payload" | jq '.' >&2
  exit 1
fi

echo "$payload" | jq \
  --arg model "$model_name" \
  --arg taskID "$task_id" \
  '{
    modelName: $model,
    taskID: $taskID,
    status: "submitted",
    nextAction: "WAIT",
    nextActionHint: ("Poll with myreels-task-get.sh " + $taskID)
  }
  + (if (.message // "") != "" then {message: .message} else {} end)'
