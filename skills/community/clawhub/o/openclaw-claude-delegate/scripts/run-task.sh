#!/bin/bash
# Claude Code Subagent Runner
#
# Modes:
#   run     — one-shot task (default)
#   resume  — continue a previous session
#   status  — check if a session exists and show its last result
#   clean   — remove old result files
#
# Usage:
#   run-task.sh run    <workdir> <budget> <model> <task-description>
#   run-task.sh resume <session-id> <budget> <task-description> [workdir]
#   run-task.sh status <session-id>
#
# Models: opus (default), sonnet, haiku
# Output: JSON to stdout with structured result
#
# Environment:
#   CC_TASK_ID       — optional task ID for tracking
#   CC_TIMEOUT       — optional timeout in seconds (0 = no timeout)
#   CC_STREAM_FILE   — optional raw stream log path
#   CC_STDERR_FILE   — optional stderr log path
#   CLAUDE_RUNNER_USER  — optional non-root user to run Claude as
#   CLAUDE_RUNNER_HOME  — optional home dir for the runner user
#   CLAUDE_BIN          — optional Claude binary path
#   CLAUDE_PERMISSION_MODE — optional Claude permission mode override
#   CLAUDE_BACKEND      — optional backend: acpx | cli
#   CLAUDE_ACPX_BIN     — optional direct acpx binary path

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENSURE_NONROOT_SCRIPT="$SCRIPT_DIR/ensure-nonroot-delegation.sh"
DELEGATE_BOOTSTRAP_SCRIPT="$SCRIPT_DIR/delegate-bootstrap.sh"

RESULTS_DIR="/tmp/claude-subagent-results"
LOGS_DIR="/tmp/claude-subagent-logs"
mkdir -p "$RESULTS_DIR" "$LOGS_DIR"

MODE="${1:-run}"

DELEGATE_RUNNER_USER=""
DELEGATE_RUNNER_HOME=""
DELEGATE_CLAUDE_BIN=""
DELEGATE_ACPX_BIN=""
DELEGATE_BACKEND=""

build_runner_prefix() {
  if [ -n "$DELEGATE_RUNNER_USER" ]; then
    RUNNER_PREFIX=(
      sudo -u "$DELEGATE_RUNNER_USER" -H env
      HOME="$DELEGATE_RUNNER_HOME"
      XDG_CONFIG_HOME="$DELEGATE_RUNNER_HOME/.config"
      XDG_CACHE_HOME="$DELEGATE_RUNNER_HOME/.cache"
      XDG_STATE_HOME="$DELEGATE_RUNNER_HOME/.local/state"
    )
  else
    RUNNER_PREFIX=(env)
  fi

  if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    RUNNER_PREFIX+=(CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN")
  fi
}

augment_prompt_for_context() {
  local task="$1"
  local workdir="${2:-.}"
  local extra=""

  if [ -n "${CC_ADD_DIRS:-}" ]; then
    extra+="Relevant directories you may inspect if useful:\n"
    IFS=':' read -r -a add_dirs <<< "$CC_ADD_DIRS"
    for d in "${add_dirs[@]}"; do
      [ -n "$d" ] && extra+="- $d\n"
    done
    extra+="\n"
  fi

  local delegate_system_prompt=""
  delegate_system_prompt="$(effective_append_system_prompt "$workdir")"
  if [ -n "$delegate_system_prompt" ]; then
    extra+="${delegate_system_prompt}\n\n"
  fi

  if [ -n "$extra" ]; then
    printf '%b%s\n' "$extra" "$task"
  else
    printf '%s\n' "$task"
  fi
}

effective_append_system_prompt() {
  local workdir="$1"
  local builtin_prompt=""
  local user_prompt="${CC_APPEND_SYSTEM_PROMPT:-}"

  if [ "${CLAUDE_DELEGATE_BOOTSTRAP:-1}" != "0" ] && [ -x "$DELEGATE_BOOTSTRAP_SCRIPT" ]; then
    builtin_prompt="$("$DELEGATE_BOOTSTRAP_SCRIPT" system-prompt "$workdir" "${CC_ADD_DIRS:-}" 2>/dev/null || true)"
  fi

  if [ -n "$builtin_prompt" ] && [ -n "$user_prompt" ]; then
    printf '%s\n\n%s\n' "$builtin_prompt" "$user_prompt"
  elif [ -n "$builtin_prompt" ]; then
    printf '%s\n' "$builtin_prompt"
  elif [ -n "$user_prompt" ]; then
    printf '%s\n' "$user_prompt"
  fi
}

resolve_delegate_context() {
  local runner_user="${CLAUDE_RUNNER_USER:-}"
  local runner_home="${CLAUDE_RUNNER_HOME:-}"
  local claude_bin="${CLAUDE_BIN:-}"
  local acpx_bin="${CLAUDE_ACPX_BIN:-}"
  local backend="${CLAUDE_BACKEND:-}"

  if [ -z "$runner_user" ] && [ "$(id -u)" = "0" ] && [ -d /home/ccbot ]; then
    runner_user="ccbot"
    runner_home="/home/ccbot"
  fi

  if [ -n "$runner_user" ]; then
    [ -n "$runner_home" ] || runner_home="/home/$runner_user"
    if [ -x "$ENSURE_NONROOT_SCRIPT" ]; then
      eval "$("$ENSURE_NONROOT_SCRIPT" env "$runner_user" "$runner_home")"
      claude_bin="${claude_bin:-${ENSURED_CLAUDE_BIN:-}}"
      acpx_bin="${acpx_bin:-${ENSURED_ACPX_BIN:-}}"
      runner_home="${runner_home:-${ENSURED_RUNNER_HOME:-}}"
    fi
  fi

  [ -n "$claude_bin" ] || claude_bin="claude"

  if [ -z "$backend" ]; then
    backend="cli"
  fi

  DELEGATE_RUNNER_USER="$runner_user"
  DELEGATE_RUNNER_HOME="$runner_home"
  DELEGATE_CLAUDE_BIN="$claude_bin"
  DELEGATE_ACPX_BIN="$acpx_bin"
  DELEGATE_BACKEND="$backend"
  build_runner_prefix
}

resolve_claude_base_cmd() {
  local permission_mode="${CLAUDE_PERMISSION_MODE:-}"

  resolve_delegate_context
  CLAUDE_BASE_CMD=("${RUNNER_PREFIX[@]}" "$DELEGATE_CLAUDE_BIN")

  if [ -n "$permission_mode" ]; then
    CLAUDE_BASE_CMD+=(--permission-mode "$permission_mode")
  fi
}

normalize_claude_model() {
  local model="${1:-}"
  local normalized

  [ -n "$model" ] || return 0

  normalized="${model,,}"
  normalized="${normalized#claude-cli/}"
  normalized="${normalized#anthropic/}"

  case "$normalized" in
    default|best|opus|sonnet|haiku|opusplan|opus\[1m\]|sonnet\[1m\]|haiku\[1m\])
      printf '%s\n' "$normalized"
      return 0
      ;;
    claude-opus-*)
      if [[ "$normalized" == *1m* ]]; then
        printf 'opus[1m]\n'
      else
        printf 'opus\n'
      fi
      return 0
      ;;
    claude-sonnet-*)
      if [[ "$normalized" == *1m* ]]; then
        printf 'sonnet[1m]\n'
      else
        printf 'sonnet\n'
      fi
      return 0
      ;;
    claude-haiku-*)
      if [[ "$normalized" == *1m* ]]; then
        printf 'haiku[1m]\n'
      else
        printf 'haiku\n'
      fi
      return 0
      ;;
  esac

  printf '%s\n' "$model"
}

emit_acpx_stream_json() {
  local stream_file="$1"
  local session_name="$2"
  local model="$3"
  local stdout_file="$4"
  local stderr_file="$5"
  local exit_code="$6"
  local duration_ms="$7"

  python3 - "$stream_file" "$session_name" "$model" "$stdout_file" "$stderr_file" "$exit_code" "$duration_ms" <<'PY'
import json, sys
from pathlib import Path

stream_file, session_name, model, stdout_file, stderr_file, exit_code, duration_ms = sys.argv[1:8]
exit_code = int(exit_code)
duration_ms = int(duration_ms)

stdout_text = Path(stdout_file).read_text(encoding='utf-8', errors='replace').strip() if Path(stdout_file).exists() else ''
stderr_text = Path(stderr_file).read_text(encoding='utf-8', errors='replace').strip() if Path(stderr_file).exists() else ''
result_text = stdout_text or stderr_text or 'no result'

events = [
    {
        'type': 'system',
        'subtype': 'init',
        'session_id': session_name,
        'model': model,
        'backend': 'acpx',
    }
]

if stdout_text:
    events.append({
        'type': 'assistant',
        'session_id': session_name,
        'message': {
            'content': [
                {'type': 'text', 'text': stdout_text}
            ]
        }
    })

events.append({
    'type': 'result',
    'session_id': session_name,
    'is_error': exit_code != 0,
    'result': result_text,
    'total_cost_usd': 0,
    'num_turns': 1 if stdout_text else 0,
    'duration_ms': duration_ms,
    'subtype': 'success' if exit_code == 0 else 'error',
    'stop_reason': 'completed' if exit_code == 0 else 'failed',
})

with open(stream_file, 'w', encoding='utf-8') as fh:
    for event in events:
        fh.write(json.dumps(event) + '\n')
PY
}

run_acpx_stream() {
  local workdir="$1"
  local budget="$2"
  local model="$3"
  local task="$4"
  local stream_file="$5"
  local stderr_file="$6"
  local timeout_secs="$7"
  local session_name="$8"

  resolve_delegate_context
  [ -x "$DELEGATE_ACPX_BIN" ] || { echo "acpx backend requested but no acpx binary available" > "$stderr_file"; return 1; }

  local prompt_file stdout_file started_at ended_at duration_ms
  prompt_file="${stream_file}.prompt"
  stdout_file="${stream_file}.stdout"
  printf '%s' "$(augment_prompt_for_context "$task" "$workdir")" > "$prompt_file"

  local -a session_cmd=("${RUNNER_PREFIX[@]}" "$DELEGATE_ACPX_BIN" --cwd "$workdir" --approve-all --non-interactive-permissions fail --auth-policy skip claude sessions show "$session_name")
  if ! "${session_cmd[@]}" >/dev/null 2>&1; then
    "${RUNNER_PREFIX[@]}" "$DELEGATE_ACPX_BIN" --cwd "$workdir" --approve-all --non-interactive-permissions fail --auth-policy skip claude sessions new --name "$session_name" >/dev/null 2>> "$stderr_file"
  fi

  local -a cmd=("${RUNNER_PREFIX[@]}" "$DELEGATE_ACPX_BIN" --cwd "$workdir" --approve-all --non-interactive-permissions fail --auth-policy skip --format quiet)
  [ -n "$model" ] && cmd+=(--model "$model")
  cmd+=(claude prompt -s "$session_name" -f "$prompt_file")

  started_at=$(date +%s%3N)
  if [ "$timeout_secs" != "0" ] && [ -n "$timeout_secs" ]; then
    timeout --signal=TERM "$timeout_secs" "${cmd[@]}" > "$stdout_file" 2> "$stderr_file"
  else
    "${cmd[@]}" > "$stdout_file" 2> "$stderr_file"
  fi
  local exit_code=$?
  ended_at=$(date +%s%3N)
  duration_ms=$((ended_at - started_at))
  emit_acpx_stream_json "$stream_file" "$session_name" "$model" "$stdout_file" "$stderr_file" "$exit_code" "$duration_ms"
  return "$exit_code"
}

parse_stream() {
  local stream_file="$1"
  local output_file="$2"
  local task_id="$3"
  local status_hint="$4"
  local session_hint="${5:-}"
  local exit_code="${6:-0}"

  python3 - "$stream_file" "$output_file" "$task_id" "$status_hint" "$session_hint" "$exit_code" <<'PY'
import json, sys, os
from pathlib import Path

stream_file, output_file, task_id, status_hint, session_hint, exit_code = sys.argv[1:7]
exit_code = int(exit_code)

session_id = session_hint or ""
assistant_texts = []
result_event = None
models = []
stream_events = 0
last_event_type = ""
errors = []

if os.path.exists(stream_file):
    with open(stream_file, 'r', encoding='utf-8', errors='replace') as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                event = json.loads(raw)
            except Exception:
                continue
            stream_events += 1
            last_event_type = event.get('type', '')
            if event.get('type') == 'system' and event.get('subtype') == 'init':
                session_id = event.get('session_id') or session_id
            elif event.get('type') == 'assistant':
                session_id = event.get('session_id') or session_id
                msg = event.get('message', {})
                for block in msg.get('content', []) or []:
                    if block.get('type') == 'text' and block.get('text'):
                        assistant_texts.append(block.get('text'))
            elif event.get('type') == 'result':
                result_event = event
                session_id = event.get('session_id') or session_id
                models = list((event.get('modelUsage') or {}).keys())
                errors = event.get('errors') or []

result_text = "\n\n".join(t.strip() for t in assistant_texts if t and t.strip()).strip()
if result_event and result_event.get('result'):
    result_text = result_event.get('result')

status = status_hint
if exit_code == 124:
    status = 'timeout'
elif result_event is not None:
    status = 'ok' if not result_event.get('is_error', False) else 'error'
elif status_hint not in ('ok', 'error', 'timeout'):
    status = 'error' if exit_code else 'ok'

out = {
    'status': status,
    'task_id': task_id,
    'session_id': session_id,
    'result': result_text or (errors[0] if errors else 'no result'),
    'cost_usd': (result_event or {}).get('total_cost_usd', 0),
    'turns': (result_event or {}).get('num_turns', 0),
    'duration_ms': (result_event or {}).get('duration_ms', 0),
    'model': models,
    'stop_reason': (result_event or {}).get('stop_reason', ''),
    'result_subtype': (result_event or {}).get('subtype', ''),
    'stream_events': stream_events,
    'last_event_type': last_event_type,
    'output_file': output_file,
    'stream_file': stream_file,
    'exit_code': exit_code,
}

Path(output_file).write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
PY
}

run_claude_stream() {
  local workdir="$1"
  local budget="$2"
  local model="$3"
  local task="$4"
  local stream_file="$5"
  local stderr_file="$6"
  local timeout_secs="$7"
  local delegate_system_prompt=""

  resolve_claude_base_cmd
  model="$(normalize_claude_model "$model")"
  local -a cmd=("${CLAUDE_BASE_CMD[@]}" --print --output-format stream-json --verbose --max-budget-usd "$budget" --model "$model")
  if [ -n "${CC_ADD_DIRS:-}" ]; then
    IFS=':' read -r -a add_dirs <<< "$CC_ADD_DIRS"
    for d in "${add_dirs[@]}"; do
      [ -n "$d" ] && cmd+=(--add-dir "$d")
    done
  fi
  delegate_system_prompt="$(effective_append_system_prompt "$workdir")"
  if [ -n "$delegate_system_prompt" ]; then
    cmd+=(--append-system-prompt "$delegate_system_prompt")
  fi
  cmd+=(-p "$task")

  cd "$workdir"
  if [ "$timeout_secs" != "0" ] && [ -n "$timeout_secs" ]; then
    timeout --signal=TERM "$timeout_secs" "${cmd[@]}" > "$stream_file" 2> "$stderr_file"
  else
    "${cmd[@]}" > "$stream_file" 2> "$stderr_file"
  fi
}

resume_claude_stream() {
  local session_id="$1"
  local budget="$2"
  local task="$3"
  local stream_file="$4"
  local stderr_file="$5"
  local timeout_secs="$6"
  local workdir="$7"
  local delegate_system_prompt=""

  resolve_claude_base_cmd
  local -a cmd=("${CLAUDE_BASE_CMD[@]}" --print --output-format stream-json --verbose --max-budget-usd "$budget")
  if [ -n "${CC_ADD_DIRS:-}" ]; then
    IFS=':' read -r -a add_dirs <<< "$CC_ADD_DIRS"
    for d in "${add_dirs[@]}"; do
      [ -n "$d" ] && cmd+=(--add-dir "$d")
    done
  fi
  delegate_system_prompt="$(effective_append_system_prompt "$workdir")"
  if [ -n "$delegate_system_prompt" ]; then
    cmd+=(--append-system-prompt "$delegate_system_prompt")
  fi
  cmd+=(--resume "$session_id" -p "$task")

  if [ "$timeout_secs" != "0" ] && [ -n "$timeout_secs" ]; then
    timeout --signal=TERM "$timeout_secs" "${cmd[@]}" > "$stream_file" 2> "$stderr_file"
  else
    "${cmd[@]}" > "$stream_file" 2> "$stderr_file"
  fi
}

run_backend_stream() {
  local workdir="$1"
  local budget="$2"
  local model="$3"
  local task="$4"
  local stream_file="$5"
  local stderr_file="$6"
  local timeout_secs="$7"
  local session_name="$8"

  resolve_delegate_context
  if [ "$DELEGATE_BACKEND" = "acpx" ]; then
    run_acpx_stream "$workdir" "$budget" "$model" "$task" "$stream_file" "$stderr_file" "$timeout_secs" "$session_name"
  else
    run_claude_stream "$workdir" "$budget" "$model" "$task" "$stream_file" "$stderr_file" "$timeout_secs"
  fi
}

resume_backend_stream() {
  local session_id="$1"
  local budget="$2"
  local task="$3"
  local stream_file="$4"
  local stderr_file="$5"
  local timeout_secs="$6"
  local workdir="$7"
  local model="$8"

  resolve_delegate_context
  if [ "$DELEGATE_BACKEND" = "acpx" ]; then
    run_acpx_stream "$workdir" "$budget" "$model" "$task" "$stream_file" "$stderr_file" "$timeout_secs" "$session_id"
  else
    resume_claude_stream "$session_id" "$budget" "$task" "$stream_file" "$stderr_file" "$timeout_secs" "$workdir"
  fi
}

case "$MODE" in
  run)
    WORKDIR="${2:-.}"
    BUDGET="${3:-1.00}"
    MODEL="${4:-opus}"
    TASK="${5:-}"

    if [ -z "$TASK" ]; then
      echo '{"error": "No task provided", "usage": "run-task.sh run <workdir> <budget> <model> <task>"}' >&2
      exit 1
    fi

    TASK_ID="${CC_TASK_ID:-$(date +%s)-$$}"
    OUTPUT_FILE="$RESULTS_DIR/${TASK_ID}.json"
    STREAM_FILE="${CC_STREAM_FILE:-$LOGS_DIR/${TASK_ID}.stream}"
    STDERR_FILE="${CC_STDERR_FILE:-$LOGS_DIR/${TASK_ID}.stderr}"
    TIMEOUT_SECS="${CC_TIMEOUT:-0}"

    STATUS_HINT="ok"
    EXIT_CODE=0
    SESSION_NAME="${CC_SESSION_NAME:-$TASK_ID}"

    set +e
    run_backend_stream "$WORKDIR" "$BUDGET" "$MODEL" "$TASK" "$STREAM_FILE" "$STDERR_FILE" "$TIMEOUT_SECS" "$SESSION_NAME"
    EXIT_CODE=$?
    set -e
    if [ "$EXIT_CODE" -eq 124 ]; then
      STATUS_HINT="timeout"
    elif [ "$EXIT_CODE" -ne 0 ]; then
      STATUS_HINT="error"
    fi

    parse_stream "$STREAM_FILE" "$OUTPUT_FILE" "$TASK_ID" "$STATUS_HINT" "$SESSION_NAME" "$EXIT_CODE"
    ;;

  resume)
    SESSION_ID="${2:-}"
    BUDGET="${3:-1.00}"
    TASK="${4:-}"
    WORKDIR="${5:-.}"
    MODEL="${CC_MODEL:-opus}"

    if [ -z "$SESSION_ID" ] || [ -z "$TASK" ]; then
      echo '{"error": "Need session_id and task", "usage": "run-task.sh resume <session-id> <budget> <task> [workdir]"}' >&2
      exit 1
    fi

    TASK_ID="${CC_TASK_ID:-resume-$(date +%s)-$$}"
    OUTPUT_FILE="$RESULTS_DIR/${TASK_ID}.json"
    STREAM_FILE="${CC_STREAM_FILE:-$LOGS_DIR/${TASK_ID}.stream}"
    STDERR_FILE="${CC_STDERR_FILE:-$LOGS_DIR/${TASK_ID}.stderr}"
    TIMEOUT_SECS="${CC_TIMEOUT:-0}"

    STATUS_HINT="ok"
    EXIT_CODE=0
    cd "$WORKDIR"
    set +e
    resume_backend_stream "$SESSION_ID" "$BUDGET" "$TASK" "$STREAM_FILE" "$STDERR_FILE" "$TIMEOUT_SECS" "$WORKDIR" "$MODEL"
    EXIT_CODE=$?
    set -e
    if [ "$EXIT_CODE" -eq 124 ]; then
      STATUS_HINT="timeout"
    elif [ "$EXIT_CODE" -ne 0 ]; then
      STATUS_HINT="error"
    fi

    parse_stream "$STREAM_FILE" "$OUTPUT_FILE" "$TASK_ID" "$STATUS_HINT" "$SESSION_ID" "$EXIT_CODE"
    ;;

  status)
    SESSION_ID="${2:-}"

    if [ -z "$SESSION_ID" ]; then
      echo "Recent Claude Code results:"
      ls -lt "$RESULTS_DIR"/*.json 2>/dev/null | head -10
      exit 0
    fi

    python3 - "$RESULTS_DIR" "$SESSION_ID" <<'PY'
import json, glob, os, sys
results_dir, session_id = sys.argv[1:3]
results = []
for f in glob.glob(os.path.join(results_dir, '*.json')):
    try:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        sid = d.get('session_id', '')
        if sid == session_id or d.get('resumed_from', '') == session_id:
            results.append({
                'file': f,
                'task_id': d.get('task_id', ''),
                'session_id': sid,
                'status': d.get('status', '?'),
                'cost_usd': d.get('cost_usd', 0),
                'result_preview': str(d.get('result', ''))[:200],
                'mtime': os.path.getmtime(f)
            })
    except Exception:
        pass
results.sort(key=lambda x: x.get('mtime', 0))
if results:
    print(json.dumps(results, indent=2))
else:
    print(json.dumps({'error': f'No results found for session {session_id}'}))
PY
    ;;

  clean)
    find "$RESULTS_DIR" -name "*.json" -mmin +1440 -delete 2>/dev/null || true
    find "$LOGS_DIR" -name "*.stream" -mmin +1440 -delete 2>/dev/null || true
    find "$LOGS_DIR" -name "*.stderr" -mmin +1440 -delete 2>/dev/null || true
    echo "Cleaned old results and stream logs"
    ;;

  *)
    echo "Usage: $0 {run|resume|status|clean} [args...]" >&2
    exit 1
    ;;
esac
