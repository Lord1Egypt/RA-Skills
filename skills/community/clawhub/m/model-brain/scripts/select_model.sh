#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="route"
TEXT=""
TASK_TYPE="auto"
HIGH_STAKES=0
ALLOW_ZERO_LLM="true"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --text)
      TEXT="${2:-}"
      shift 2
      ;;
    --task-type)
      TASK_TYPE="${2:-auto}"
      shift 2
      ;;
    --high-stakes)
      HIGH_STAKES=1
      shift
      ;;
    --allow-zero-llm)
      ALLOW_ZERO_LLM="${2:-true}"
      shift 2
      ;;
    --mode)
      MODE="${2:-route}"
      shift 2
      ;;
    -h|--help)
      cat <<'HELP'
Usage: select_model.sh --text "message" [options]

Options:
  --task-type <auto|chat|code|wallet|vision|long-context|deterministic>
  --high-stakes
  --allow-zero-llm <true|false>
  --mode <route|fallback|json|env|summary>
HELP
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [ -z "$TEXT" ]; then
  echo "Missing required --text" >&2
  exit 1
fi

CMD=(python3 "$BASE_DIR/scripts/route_message.py" --text "$TEXT" --task-type "$TASK_TYPE" --allow-zero-llm "$ALLOW_ZERO_LLM" --json)
if [ "$HIGH_STAKES" -eq 1 ]; then
  CMD+=(--high-stakes)
fi

JSON_OUT="$("${CMD[@]}")"
export JSON_OUT

case "$MODE" in
  route)
    python3 - <<'PY'
import json, os
print(json.loads(os.environ['JSON_OUT'])['route'])
PY
    ;;
  fallback)
    python3 - <<'PY'
import json, os
print(json.loads(os.environ['JSON_OUT']).get('fallback') or '')
PY
    ;;
  json)
    printf '%s\n' "$JSON_OUT"
    ;;
  env)
    python3 - <<'PY'
import json, os
payload = json.loads(os.environ['JSON_OUT'])
print(f"MODEL_BRAIN_ROUTE={payload['route']}")
print(f"MODEL_BRAIN_FALLBACK={payload.get('fallback') or ''}")
print(f"MODEL_BRAIN_RISK={payload['risk']}")
print(f"MODEL_BRAIN_TASK_TYPE={payload['task_type']}")
PY
    ;;
  summary)
    python3 - <<'PY'
import json, os
payload = json.loads(os.environ['JSON_OUT'])
print(f"route={payload['route']}")
print(f"fallback={payload.get('fallback') or 'none'}")
print(f"risk={payload['risk']}")
print(f"task_type={payload['task_type']}")
print(f"reason={payload['reason']}")
PY
    ;;
  *)
    echo "Unsupported mode: $MODE" >&2
    exit 1
    ;;
esac
