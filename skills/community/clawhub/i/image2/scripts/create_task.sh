#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${IMAGE2_BASE_URL:-https://kexiangai.com}"
CREATE_ENDPOINT="/api/v1/user_task/asyncCreateWithCost"
QUERY_ENDPOINT_PREFIX="/api/v1/user_task/get/passAuth"
MODEL_NAME="GPT-Image-2"
MODEL_TYPE=""
PROMPT=""
SIZE=""
USE_LOCAL_KEY=0
URLS=()
POLL_INTERVAL=8
MAX_ATTEMPTS=90

ALLOWED_SIZES=("auto" "1:1" "3:2" "2:3" "16:9" "9:16" "4:3" "3:4" "21:9" "9:21" "1:3" "3:1" "2:1" "1:2")

usage() {
  cat <<'EOF'
Usage:
  create_task.sh --mode <text2img|img2img> --prompt "..." --size "3:4" [--url "https://..."]...

Options:
  --mode            Generation mode: text2img or img2img (required)
  --prompt          Prompt text (required)
  --size            Ratio size (required)
  --url             Reference image URL, can be repeated (required for img2img, max 8)
  --poll-interval   Poll interval seconds for query API (default: 8)
  --max-attempts    Max query attempts (default: 90)
  --model-name      Default GPT-Image-2
  --base-url        API base URL, default https://kexiangai.com
  --use-local-key   Read key from ~/.config/image2/.env when X_API_KEY is empty
  -h, --help        Show help

Examples:
  X_API_KEY=xxx ./create_task.sh --mode text2img --prompt "生成产品海报" --size "3:4"
  X_API_KEY=xxx ./create_task.sh --mode img2img --prompt "参考图重绘" --size "3:4" --url "https://example.com/a.png"
EOF
}

is_positive_int() {
  [[ "$1" =~ ^[1-9][0-9]*$ ]]
}

is_allowed_size() {
  local val="$1"
  for s in "${ALLOWED_SIZES[@]}"; do
    if [[ "$s" == "$val" ]]; then
      return 0
    fi
  done
  return 1
}

read_local_key() {
  local env_file="$HOME/.config/image2/.env"
  if [[ -f "$env_file" ]]; then
    grep '^X_API_KEY=' "$env_file" | tail -n 1 | cut -d '=' -f2- | tr -d '"' || true
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODEL_TYPE="${2:-}"
      shift 2
      ;;
    --prompt)
      PROMPT="${2:-}"
      shift 2
      ;;
    --size)
      SIZE="${2:-}"
      shift 2
      ;;
    --url)
      URLS+=("${2:-}")
      shift 2
      ;;
    --poll-interval)
      POLL_INTERVAL="${2:-}"
      shift 2
      ;;
    --max-attempts)
      MAX_ATTEMPTS="${2:-}"
      shift 2
      ;;
    --model-name)
      MODEL_NAME="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --use-local-key)
      USE_LOCAL_KEY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$MODEL_TYPE" || -z "$PROMPT" || -z "$SIZE" ]]; then
  echo "Error: --mode, --prompt and --size are required" >&2
  usage
  exit 1
fi

if [[ "$MODEL_TYPE" != "text2img" && "$MODEL_TYPE" != "img2img" ]]; then
  echo "Error: --mode must be text2img or img2img" >&2
  exit 1
fi

if ! is_allowed_size "$SIZE"; then
  echo "Error: invalid --size: $SIZE" >&2
  echo "Allowed: ${ALLOWED_SIZES[*]}" >&2
  exit 1
fi

if [[ "$MODEL_TYPE" == "img2img" ]]; then
  if [[ ${#URLS[@]} -lt 1 ]]; then
    echo "Error: --url is required when --mode=img2img" >&2
    exit 1
  fi
fi

if [[ ${#URLS[@]} -gt 8 ]]; then
  echo "Error: maximum 8 --url values are allowed" >&2
  exit 1
fi

if ! is_positive_int "$POLL_INTERVAL"; then
  echo "Error: --poll-interval must be a positive integer" >&2
  exit 1
fi

if ! is_positive_int "$MAX_ATTEMPTS"; then
  echo "Error: --max-attempts must be a positive integer" >&2
  exit 1
fi

X_API_KEY="${X_API_KEY:-}"
if [[ -z "$X_API_KEY" && $USE_LOCAL_KEY -eq 1 ]]; then
  X_API_KEY="$(read_local_key)"
fi
if [[ -z "$X_API_KEY" ]]; then
  echo "Error: missing X_API_KEY (set env var or use --use-local-key after set_key.sh)" >&2
  exit 1
fi

MASKED="${X_API_KEY:0:4}****${X_API_KEY: -4}"
URL_COUNT=${#URLS[@]}

echo "Request summary:"
echo "- create endpoint: ${BASE_URL}${CREATE_ENDPOINT}"
echo "- query endpoint: ${BASE_URL}${QUERY_ENDPOINT_PREFIX}/{id}"
echo "- modelName: $MODEL_NAME"
echo "- modelType: $MODEL_TYPE"
echo "- size: $SIZE"
echo "- urls: $URL_COUNT"
echo "- key: $MASKED"
echo "- poll interval: ${POLL_INTERVAL}s"
echo "- max attempts: $MAX_ATTEMPTS"

URLS_JSON="$(python3 - <<'PY' "${URLS[@]}"
import json, sys
print(json.dumps(sys.argv[1:], ensure_ascii=False))
PY
)"

PAYLOAD="$(python3 - <<'PY' "$MODEL_NAME" "$MODEL_TYPE" "$PROMPT" "$SIZE" "$URLS_JSON"
import json, sys
model_name, model_type, prompt, size, urls_json = sys.argv[1:]
urls = json.loads(urls_json)
body = {
    "cost_type": 1,
    "business_url": "gpt-image2/img",
    "user_input": {
        "modelName": model_name,
        "modelType": model_type,
        "prompt": prompt,
        "size": size,
    },
}
if model_type == "img2img":
    body["user_input"]["urls"] = urls
print(json.dumps(body, ensure_ascii=False))
PY
)"

CREATE_RESPONSE="$(curl --location "${BASE_URL}${CREATE_ENDPOINT}" \
  --header 'Content-Type: application/json' \
  --header "x-api-key: ${X_API_KEY}" \
  --data "$PAYLOAD")"

echo "$CREATE_RESPONSE"

TASK_ID="$(python3 - <<'PY' "$CREATE_RESPONSE"
import json, sys
raw = sys.argv[1]
try:
    data = json.loads(raw)
except Exception:
    print("")
    raise SystemExit(0)
task_id = data.get("id")
print(str(task_id) if task_id is not None else "")
PY
)"

if [[ -z "$TASK_ID" ]]; then
  echo "Warning: task id not found in create response; cannot continue polling." >&2
  exit 1
fi

echo "Task created successfully."
echo "Task ID: $TASK_ID"
echo "Start querying until terminal status..."

attempt=1
while [[ $attempt -le $MAX_ATTEMPTS ]]; do
  QUERY_URL="${BASE_URL}${QUERY_ENDPOINT_PREFIX}/${TASK_ID}"
  QUERY_RESPONSE="$(curl --location "$QUERY_URL" \
    --header 'Content-Type: application/json' \
    --header "x-api-key: ${X_API_KEY}")"

  STATUS="$(python3 - <<'PY' "$QUERY_RESPONSE"
import json, sys
raw = sys.argv[1]
try:
    data = json.loads(raw)
except Exception:
    print("unknown")
    raise SystemExit(0)
status = data.get("task_status")
if status is None:
    status = "unknown"
print(str(status).lower())
PY
)"

  echo "[Attempt ${attempt}/${MAX_ATTEMPTS}] task_status=${STATUS}"

  if [[ "$STATUS" == "success" || "$STATUS" == "succeeded" || "$STATUS" == "done" || "$STATUS" == "completed" ]]; then
    echo "Task finished successfully. Final query response:"
    echo "$QUERY_RESPONSE"
    exit 0
  fi

  if [[ "$STATUS" == "failed" || "$STATUS" == "error" || "$STATUS" == "canceled" || "$STATUS" == "cancelled" ]]; then
    echo "Task finished with failure status. Final query response:"
    echo "$QUERY_RESPONSE"
    exit 2
  fi

  if [[ $attempt -lt $MAX_ATTEMPTS ]]; then
    sleep "$POLL_INTERVAL"
  fi
  attempt=$((attempt + 1))
done

echo "Polling timed out after ${MAX_ATTEMPTS} attempts."
echo "Task may still be running. Query manually with task id: $TASK_ID"
echo "curl --location '${BASE_URL}${QUERY_ENDPOINT_PREFIX}/${TASK_ID}' --header 'Content-Type: application/json' --header 'x-api-key: <YOUR_X_API_KEY>'"
exit 3
