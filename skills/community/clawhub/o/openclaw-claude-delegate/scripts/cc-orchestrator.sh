#!/bin/bash
# Claude Code Orchestrator
# High-level task management layer on top of run-task.sh
#
# Commands:
#   dispatch  — Submit a task, get a handle back immediately
#   poll      — Check current task status + progress
#   watch     — Tail live progress from the raw stream log
#   result    — Get the final result (json or text)
#   resume    — Send a correction/continuation to a task
#   batch     — Dispatch multiple tasks from a JSONL manifest
#   list      — Show all tracked tasks
#   cancel    — Kill a running task
#   costs     — Show cost summary across all tasks
#   cleanup   — Archive completed tasks, remove old data

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY_DIR="/tmp/claude-subagent-registry"
RESULTS_DIR="/tmp/claude-subagent-results"
LOGS_DIR="/tmp/claude-subagent-logs"
COST_LOG="/tmp/claude-subagent-costs.jsonl"
HOOKS_DIR="/tmp/claude-subagent-hooks"

mkdir -p "$REGISTRY_DIR" "$RESULTS_DIR" "$LOGS_DIR" "$HOOKS_DIR"

json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

gen_task_id() {
  local label="${1:-task}"
  local clean_label
  clean_label=$(echo "$label" | tr ' /' '-' | tr -cd 'a-zA-Z0-9-' | head -c 30)
  echo "${clean_label}-$(date +%s)-$$"
}

write_registry() {
  local task_id="$1"
  local status="$2"
  local session_id="${3:-}"
  local label="${4:-}"
  local workdir="${5:-}"
  local model="${6:-}"
  local budget="${7:-}"
  local pid="${8:-}"
  local cost="${9:-0}"
  local result_preview="${10:-}"
  local timeout_secs="${11:-0}"
  local notify_cmd="${12:-}"
  local batch_id="${13:-}"
  local expected_file="${14:-}"
  local expect_min_bytes="${15:-0}"
  local next_action="${16:-}"
  local continuation_mode="${17:-}"

  local label_json preview_json notify_json expected_file_json next_action_json continuation_mode_json
  label_json=$(printf '%s' "$label" | json_escape)
  preview_json=$(printf '%s' "$result_preview" | json_escape)
  notify_json=$(printf '%s' "$notify_cmd" | json_escape)
  expected_file_json=$(printf '%s' "$expected_file" | json_escape)
  next_action_json=$(printf '%s' "$next_action" | json_escape)
  continuation_mode_json=$(printf '%s' "$continuation_mode" | json_escape)

  python3 - "$REGISTRY_DIR/$task_id.json" "$task_id" "$status" "$session_id" "$workdir" "$model" "$budget" "$pid" "$cost" "$timeout_secs" "$batch_id" "$label_json" "$preview_json" "$notify_json" "$expected_file_json" "$expect_min_bytes" "$next_action_json" "$continuation_mode_json" <<'PY'
import json, os, sys, time
reg_file, task_id, status, session_id, workdir, model, budget, pid, cost, timeout_secs, batch_id, label_json, preview_json, notify_json, expected_file_json, expect_min_bytes, next_action_json, continuation_mode_json = sys.argv[1:19]
entry = {
    'task_id': task_id,
    'status': status,
    'session_id': session_id,
    'label': json.loads(label_json),
    'workdir': workdir,
    'model': model,
    'budget': budget,
    'pid': pid,
    'cost_usd': float(cost) if cost else 0,
    'result_preview': json.loads(preview_json)[:200],
    'timeout_secs': int(timeout_secs) if timeout_secs else 0,
    'notify_cmd': json.loads(notify_json),
    'batch_id': batch_id,
    'expected_file': json.loads(expected_file_json),
    'expect_min_bytes': int(expect_min_bytes) if expect_min_bytes else 0,
    'next_action': json.loads(next_action_json),
    'continuation_mode': json.loads(continuation_mode_json),
    'verified': False,
    'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'started_at': time.strftime('%Y-%m-%dT%H:%M:%S%z') if status == 'running' else ''
}
if os.path.exists(reg_file):
    try:
        with open(reg_file, encoding='utf-8') as f:
            existing = json.load(f)
        existing.update({k: v for k, v in entry.items() if v not in ('', None)})
        entry = existing
    except Exception:
        pass
entry['status'] = status
entry['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
with open(reg_file, 'w', encoding='utf-8') as f:
    json.dump(entry, f, indent=2)
PY
}


verify_expected_artifact() {
  local reg_file="$1"
  python3 - "$reg_file" <<'PY'
import json, os, sys
reg_file=sys.argv[1]
with open(reg_file, encoding='utf-8') as f:
    reg=json.load(f)
expected=reg.get('expected_file','')
min_bytes=int(reg.get('expect_min_bytes',0) or 0)
exists=False
size=0
verified=True
if expected:
    exists=os.path.exists(expected)
    size=os.path.getsize(expected) if exists else 0
    verified=exists and size >= min_bytes
reg['expected_file_exists']=exists
reg['expected_file_bytes']=size
reg['verified']=verified
if reg.get('status')=='done' and not verified:
    reg['status']='incomplete'
with open(reg_file, 'w', encoding='utf-8') as f:
    json.dump(reg, f, indent=2)
print(json.dumps(reg))
PY
}

refresh_from_output_if_ready() {
  local task_id="$1"
  local reg_file="$REGISTRY_DIR/${task_id}.json"
  local out_file="$LOGS_DIR/${task_id}.out"
  local stream_file="$LOGS_DIR/${task_id}.stream"

  python3 - "$reg_file" "$out_file" "$stream_file" "$COST_LOG" <<'PY'
import json, os, sys, time
reg_file, out_file, stream_file, cost_log = sys.argv[1:5]
try:
    with open(reg_file, encoding='utf-8') as f:
        reg = json.load(f)
except Exception:
    print('{}')
    raise SystemExit(0)

updated = False

if reg.get('status') == 'running':
    if os.path.exists(out_file):
        try:
            with open(out_file, encoding='utf-8') as f:
                d = json.load(f)
            status_map = {'ok': 'done', 'error': 'failed', 'timeout': 'timeout'}
            reg['status'] = status_map.get(d.get('status'), reg.get('status'))
            reg['session_id'] = d.get('session_id', reg.get('session_id', ''))
            reg['cost_usd'] = d.get('cost_usd', reg.get('cost_usd', 0))
            reg['result_preview'] = str(d.get('result', reg.get('result_preview', '')))[:200]
            reg['turns'] = d.get('turns', reg.get('turns', 0))
            reg['duration_ms'] = d.get('duration_ms', reg.get('duration_ms', 0))
            reg['result_subtype'] = d.get('result_subtype', reg.get('result_subtype', ''))
            reg['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
            updated = True
        except Exception:
            pass
    elif os.path.exists(stream_file):
        session_id = reg.get('session_id', '')
        assistant_count = 0
        last_assistant = ''
        event_count = 0
        with open(stream_file, encoding='utf-8', errors='replace') as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    event = json.loads(raw)
                except Exception:
                    continue
                event_count += 1
                if event.get('type') == 'system' and event.get('subtype') == 'init' and not session_id:
                    session_id = event.get('session_id', '')
                elif event.get('type') == 'assistant':
                    assistant_count += 1
                    msg = event.get('message', {})
                    texts = [b.get('text','') for b in (msg.get('content') or []) if b.get('type') == 'text']
                    if texts:
                        last_assistant = '\n\n'.join(texts)[-400:]
                elif event.get('type') == 'result':
                    status_map = {'error': 'failed'}
                    reg['status'] = 'failed' if event.get('is_error') else 'done'
                    reg['cost_usd'] = event.get('total_cost_usd', reg.get('cost_usd', 0))
                    reg['turns'] = event.get('num_turns', reg.get('turns', 0))
                    reg['duration_ms'] = event.get('duration_ms', reg.get('duration_ms', 0))
                    reg['result_subtype'] = event.get('subtype', reg.get('result_subtype', ''))
                    if last_assistant:
                        reg['result_preview'] = last_assistant[:200]
                    updated = True
        reg['session_id'] = session_id
        reg['stream_events'] = event_count
        reg['assistant_messages'] = assistant_count
        if last_assistant and not reg.get('result_preview'):
            reg['result_preview'] = last_assistant[:200]
        reg['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        updated = True

if updated:
    with open(reg_file, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2)
print(json.dumps(reg))
PY
}

run_notify_hook() {
  local task_id="$1"
  local reg_file="$REGISTRY_DIR/${task_id}.json"
  [ -f "$reg_file" ] || return 0

  local notify_cmd status result_preview cost expected_file expected_exists expected_bytes verified next_action continuation_mode session_id
  notify_cmd=$(python3 -c "import json; print(json.load(open('$reg_file')).get('notify_cmd',''))" 2>/dev/null || true)
  [ -n "$notify_cmd" ] || return 0

  status=$(python3 -c "import json; print(json.load(open('$reg_file')).get('status',''))" 2>/dev/null || true)
  result_preview=$(python3 -c "import json; print(json.load(open('$reg_file')).get('result_preview',''))" 2>/dev/null || true)
  cost=$(python3 -c "import json; print(json.load(open('$reg_file')).get('cost_usd',0))" 2>/dev/null || true)
  expected_file=$(python3 -c "import json; print(json.load(open('$reg_file')).get('expected_file',''))" 2>/dev/null || true)
  expected_exists=$(python3 -c "import json; print(json.load(open('$reg_file')).get('expected_file_exists',False))" 2>/dev/null || true)
  expected_bytes=$(python3 -c "import json; print(json.load(open('$reg_file')).get('expected_file_bytes',0))" 2>/dev/null || true)
  verified=$(python3 -c "import json; print(json.load(open('$reg_file')).get('verified',False))" 2>/dev/null || true)
  next_action=$(python3 -c "import json; print(json.load(open('$reg_file')).get('next_action',''))" 2>/dev/null || true)
  continuation_mode=$(python3 -c "import json; print(json.load(open('$reg_file')).get('continuation_mode',''))" 2>/dev/null || true)
  session_id=$(python3 -c "import json; print(json.load(open('$reg_file')).get('session_id',''))" 2>/dev/null || true)

  CC_NOTIFY_TASK_ID="$task_id" \
  CC_NOTIFY_STATUS="$status" \
  CC_NOTIFY_COST_USD="$cost" \
  CC_NOTIFY_RESULT_PREVIEW="$result_preview" \
  CC_NOTIFY_EXPECTED_FILE="$expected_file" \
  CC_NOTIFY_EXPECTED_FILE_EXISTS="$expected_exists" \
  CC_NOTIFY_EXPECTED_FILE_BYTES="$expected_bytes" \
  CC_NOTIFY_VERIFIED="$verified" \
  CC_NOTIFY_NEXT_ACTION="$next_action" \
  CC_NOTIFY_CONTINUATION_MODE="$continuation_mode" \
  CC_NOTIFY_SESSION_ID="$session_id" \
  bash -lc "$notify_cmd" > "$HOOKS_DIR/${task_id}.notify.out" 2> "$HOOKS_DIR/${task_id}.notify.err" || true
}

finish_task_from_output() {
  local task_id="$1"
  local exit_code="$2"
  local reg_file="$REGISTRY_DIR/${task_id}.json"
  local out_file="$LOGS_DIR/${task_id}.out"

  if [ -f "$out_file" ]; then
    python3 - "$reg_file" "$out_file" "$COST_LOG" "$exit_code" <<'PY'
import json, os, sys, time
reg_file, out_file, cost_log, exit_code = sys.argv[1:5]
exit_code = int(exit_code)
with open(out_file, encoding='utf-8') as f:
    d = json.load(f)
try:
    with open(reg_file, encoding='utf-8') as f:
        entry = json.load(f)
except Exception:
    entry = {}
status_map = {'ok': 'done', 'error': 'failed', 'timeout': 'timeout'}
status = status_map.get(d.get('status', ''), 'failed' if exit_code else 'done')
entry.update({
    'status': status,
    'session_id': d.get('session_id', entry.get('session_id', '')),
    'cost_usd': d.get('cost_usd', 0),
    'result_preview': str(d.get('result', ''))[:200],
    'turns': d.get('turns', 0),
    'duration_ms': d.get('duration_ms', 0),
    'result_subtype': d.get('result_subtype', ''),
    'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'exit_code': d.get('exit_code', exit_code),
})
with open(reg_file, 'w', encoding='utf-8') as f:
    json.dump(entry, f, indent=2)
with open(cost_log, 'a', encoding='utf-8') as f:
    f.write(json.dumps({
        'task_id': entry.get('task_id', ''),
        'label': entry.get('label', ''),
        'model': entry.get('model', ''),
        'cost_usd': entry.get('cost_usd', 0),
        'status': status,
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z')
    }) + '\n')
PY
  fi
  verify_expected_artifact "$reg_file" >/dev/null 2>&1 || true
  run_notify_hook "$task_id"
}

cmd_dispatch() {
  local workdir="${1:-.}"
  local budget="${2:-1.00}"
  local model="${3:-sonnet}"
  local label="${4:-task}"
  local task="${5:-}"
  shift 5 || true

  local timeout_secs="0"
  local notify_cmd=""
  local expected_file=""
  local expect_min_bytes="0"
  local next_action=""
  local continuation_mode=""
  local batch_id=""

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --timeout) timeout_secs="${2:-0}"; shift 2 ;;
      --notify-cmd) notify_cmd="${2:-}"; shift 2 ;;
      --batch-id) batch_id="${2:-}"; shift 2 ;;
      --expect-file) expected_file="${2:-}"; shift 2 ;;
      --expect-min-bytes) expect_min_bytes="${2:-0}"; shift 2 ;;
      --next-action) next_action="${2:-}"; shift 2 ;;
      --continuation-mode) continuation_mode="${2:-}"; shift 2 ;;
      *) echo "{\"error\": \"Unknown option: $1\"}" >&2; exit 1 ;;
    esac
  done

  if [ -z "$task" ]; then
    echo '{"error": "No task provided"}' >&2
    echo "Usage: cc-orchestrator.sh dispatch <workdir> <budget> <model> <label> \"<task>\" [--timeout N] [--notify-cmd CMD] [--expect-file PATH] [--expect-min-bytes N] [--next-action TEXT] [--continuation-mode continue|switch|blocked]" >&2
    exit 1
  fi

  local task_id
  task_id=$(gen_task_id "$label")
  write_registry "$task_id" "running" "" "$label" "$workdir" "$model" "$budget" "" "0" "" "$timeout_secs" "$notify_cmd" "$batch_id" "$expected_file" "$expect_min_bytes" "$next_action" "$continuation_mode"

  (
    CC_TASK_ID="$task_id" \
    CC_TIMEOUT="$timeout_secs" \
    CC_STREAM_FILE="$LOGS_DIR/${task_id}.stream" \
    CC_STDERR_FILE="$LOGS_DIR/${task_id}.stderr" \
    bash "$SCRIPT_DIR/run-task.sh" run "$workdir" "$budget" "$model" "$task" > "$LOGS_DIR/${task_id}.out"
    EXIT_CODE=$?
    finish_task_from_output "$task_id" "$EXIT_CODE"
  ) &

  local bg_pid=$!
  write_registry "$task_id" "running" "" "$label" "$workdir" "$model" "$budget" "$bg_pid" "0" "" "$timeout_secs" "$notify_cmd" "$batch_id" "$expected_file" "$expect_min_bytes" "$next_action" "$continuation_mode"

  echo "{\"task_id\": \"$task_id\", \"pid\": $bg_pid, \"status\": \"dispatched\", \"label\": \"$label\", \"model\": \"$model\", \"budget\": \"$budget\", \"timeout_secs\": $timeout_secs, \"expected_file\": \"$expected_file\", \"next_action\": \"$next_action\", \"continuation_mode\": \"$continuation_mode\"}"
}

cmd_poll() {
  local task_id="${1:-}"
  if [ -z "$task_id" ]; then echo '{"error": "No task_id"}' >&2; exit 1; fi

  local reg_file="$REGISTRY_DIR/${task_id}.json"
  if [ ! -f "$reg_file" ]; then
    echo "{\"error\": \"Task not found: $task_id\"}"
    exit 1
  fi

  refresh_from_output_if_ready "$task_id" > /tmp/cc-poll-${task_id}.json

  python3 - "/tmp/cc-poll-${task_id}.json" "$reg_file" <<'PY'
import json, os, sys
with open(sys.argv[1], encoding='utf-8') as f:
    d = json.load(f)
reg_file = sys.argv[2]
pid = d.get('pid', '')
if pid and d.get('status') == 'running':
    try:
        os.kill(int(pid), 0)
        d['alive'] = True
    except Exception:
        d['alive'] = False
        if d.get('status') == 'running':
            d['status'] = 'failed-interrupted'
            d['failure_reason'] = 'worker_pid_dead_before_result'
            d['recommended_action'] = 'rerun-or-resume'
            try:
                with open(reg_file, 'w', encoding='utf-8') as f:
                    json.dump(d, f, indent=2)
            except Exception:
                pass
print(json.dumps(d, indent=2))
PY
  rm -f "/tmp/cc-poll-${task_id}.json"
}

cmd_watch() {
  local task_id="${1:-}"
  if [ -z "$task_id" ]; then echo '{"error": "No task_id"}' >&2; exit 1; fi
  local stream_file="$LOGS_DIR/${task_id}.stream"
  if [ ! -f "$stream_file" ]; then
    echo "No stream file yet for $task_id"
    exit 1
  fi

  tail -n +1 -f "$stream_file" | python3 -c '
import json, sys
for raw in sys.stdin:
    raw = raw.strip()
    if not raw:
        continue
    try:
        event = json.loads(raw)
    except Exception:
        continue
    t = event.get("type")
    if t == "system" and event.get("subtype") == "init":
        print(f"[init] session={event.get('"'"'session_id'"'"','"'"''"'"')} model={event.get('"'"'model'"'"','"'"''"'"')}", flush=True)
    elif t == "assistant":
        msg = event.get("message", {})
        texts = [b.get("text","").strip() for b in (msg.get("content") or []) if b.get("type") == "text" and b.get("text","").strip()]
        if texts:
            print(f"[assistant] {'"'"' '"'"'.join(texts)}", flush=True)
        else:
            print("[assistant] (non-text event)", flush=True)
    elif t == "result":
        print(f"[result] subtype={event.get('"'"'subtype'"'"','"'"''"'"')} cost=${event.get('"'"'total_cost_usd'"'"',0):.4f} turns={event.get('"'"'num_turns'"'"',0)} duration_ms={event.get('"'"'duration_ms'"'"',0)}", flush=True)
    else:
        print(f"[{t}]", flush=True)
'
}

cmd_result() {
  local mode="json"
  if [ "${1:-}" = "--text" ]; then
    mode="text"
    shift
  elif [ "${1:-}" = "--raw" ]; then
    mode="raw"
    shift
  fi

  local task_id="${1:-}"
  if [ -z "$task_id" ]; then echo '{"error": "No task_id"}' >&2; exit 1; fi

  local out_file="$LOGS_DIR/${task_id}.out"
  local stream_file="$LOGS_DIR/${task_id}.stream"

  case "$mode" in
    json)
      [ -f "$out_file" ] && cat "$out_file" || echo "{\"error\": \"No output file for task $task_id\"}"
      ;;
    text)
      if [ -f "$out_file" ]; then
        python3 - "$out_file" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    d = json.load(f)
print(d.get('result', ''))
PY
      else
        echo "No output file for task $task_id"
        exit 1
      fi
      ;;
    raw)
      [ -f "$stream_file" ] && cat "$stream_file" || echo "{\"error\": \"No stream file for task $task_id\"}"
      ;;
  esac
}

cmd_resume() {
  local task_id="${1:-}"
  local budget="${2:-0.50}"
  local follow_up="${3:-}"
  shift 3 || true

  local timeout_secs="0"
  local notify_cmd=""
  local expected_file=""
  local expect_min_bytes="0"
  local next_action=""
  local continuation_mode=""

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --timeout) timeout_secs="${2:-0}"; shift 2 ;;
      --notify-cmd) notify_cmd="${2:-}"; shift 2 ;;
      --expect-file) expected_file="${2:-}"; shift 2 ;;
      --expect-min-bytes) expect_min_bytes="${2:-0}"; shift 2 ;;
      --next-action) next_action="${2:-}"; shift 2 ;;
      --continuation-mode) continuation_mode="${2:-}"; shift 2 ;;
      *) echo "{\"error\": \"Unknown option: $1\"}" >&2; exit 1 ;;
    esac
  done

  if [ -z "$task_id" ] || [ -z "$follow_up" ]; then
    echo '{"error": "Need task_id and follow-up prompt"}' >&2
    exit 1
  fi

  local reg_file="$REGISTRY_DIR/${task_id}.json"
  if [ ! -f "$reg_file" ]; then
    echo "{\"error\": \"Task not found: $task_id\"}"
    exit 1
  fi

  local session_id label workdir model batch_id attempts=0
  while [ "$attempts" -lt 10 ]; do
    refresh_from_output_if_ready "$task_id" >/dev/null 2>&1 || true
    session_id=$(python3 -c "import json; print(json.load(open('$reg_file')).get('session_id', ''))" 2>/dev/null || true)
    label=$(python3 -c "import json; print(json.load(open('$reg_file')).get('label', 'resume'))" 2>/dev/null || true)
    workdir=$(python3 -c "import json; print(json.load(open('$reg_file')).get('workdir', ''))" 2>/dev/null || true)
    model=$(python3 -c "import json; print(json.load(open('$reg_file')).get('model', ''))" 2>/dev/null || true)
    batch_id=$(python3 -c "import json; print(json.load(open('$reg_file')).get('batch_id', ''))" 2>/dev/null || true)
    [ -n "$session_id" ] && break
    attempts=$((attempts + 1))
    sleep 1
  done

  if [ -z "$session_id" ]; then
    echo "{\"error\": \"No session_id found for task $task_id after waiting — cannot resume\"}"
    exit 1
  fi

  local resume_id="${task_id}-r$(date +%s)"
  write_registry "$resume_id" "running" "$session_id" "${label}-resume" "$workdir" "$model" "$budget" "" "0" "" "$timeout_secs" "$notify_cmd" "$batch_id" "$expected_file" "$expect_min_bytes" "$next_action" "$continuation_mode"

  (
    CC_TASK_ID="$resume_id" \
    CC_MODEL="$model" \
    CC_TIMEOUT="$timeout_secs" \
    CC_STREAM_FILE="$LOGS_DIR/${resume_id}.stream" \
    CC_STDERR_FILE="$LOGS_DIR/${resume_id}.stderr" \
    bash "$SCRIPT_DIR/run-task.sh" resume "$session_id" "$budget" "$follow_up" "$workdir" > "$LOGS_DIR/${resume_id}.out"
    EXIT_CODE=$?
    python3 - "$REGISTRY_DIR/${resume_id}.json" "$LOGS_DIR/${resume_id}.out" "$COST_LOG" "$task_id" "$EXIT_CODE" <<'PY'
import json, sys, time
reg_file, out_file, cost_log, parent_task_id, exit_code = sys.argv[1:6]
exit_code = int(exit_code)
with open(out_file, encoding='utf-8') as f:
    d = json.load(f)
with open(reg_file, encoding='utf-8') as f:
    entry = json.load(f)
status_map = {'ok': 'done', 'error': 'failed', 'timeout': 'timeout'}
status = status_map.get(d.get('status', ''), 'failed' if exit_code else 'done')
entry.update({
    'status': status,
    'session_id': d.get('session_id', entry.get('session_id', '')),
    'resumed_from': parent_task_id,
    'cost_usd': d.get('cost_usd', 0),
    'result_preview': str(d.get('result', ''))[:200],
    'turns': d.get('turns', 0),
    'duration_ms': d.get('duration_ms', 0),
    'result_subtype': d.get('result_subtype', ''),
    'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'exit_code': d.get('exit_code', exit_code),
})
with open(reg_file, 'w', encoding='utf-8') as f:
    json.dump(entry, f, indent=2)
with open(cost_log, 'a', encoding='utf-8') as f:
    f.write(json.dumps({
        'task_id': entry.get('task_id', ''),
        'label': entry.get('label', ''),
        'model': entry.get('model', ''),
        'cost_usd': entry.get('cost_usd', 0),
        'status': status,
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z')
    }) + '\n')
PY
    verify_expected_artifact "$REGISTRY_DIR/${resume_id}.json" >/dev/null 2>&1 || true
    run_notify_hook "$resume_id"
  ) &

  local bg_pid=$!
  write_registry "$resume_id" "running" "$session_id" "${label}-resume" "$workdir" "$model" "$budget" "$bg_pid" "0" "" "$timeout_secs" "$notify_cmd" "$batch_id" "$expected_file" "$expect_min_bytes" "$next_action" "$continuation_mode"

  echo "{\"task_id\": \"$resume_id\", \"resumed_from\": \"$task_id\", \"session_id\": \"$session_id\", \"pid\": $bg_pid, \"status\": \"dispatched\", \"timeout_secs\": $timeout_secs, \"expected_file\": \"$expected_file\", \"next_action\": \"$next_action\", \"continuation_mode\": \"$continuation_mode\"}"
}

cmd_batch() {
  local manifest="${1:-}"
  shift || true
  local max_parallel="2"

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --max-parallel) max_parallel="${2:-2}"; shift 2 ;;
      *) echo "{\"error\": \"Unknown option: $1\"}" >&2; exit 1 ;;
    esac
  done

  [ -n "$manifest" ] || { echo '{"error": "Need manifest path"}' >&2; exit 1; }
  [ -f "$manifest" ] || { echo "{\"error\": \"Manifest not found: $manifest\"}" >&2; exit 1; }

  local batch_id="batch-$(date +%s)-$$"
  local tmp_handles="/tmp/${batch_id}.handles"
  : > "$tmp_handles"

  while IFS= read -r encoded; do
    [ -n "$encoded" ] || continue
    eval "$(python3 - "$encoded" <<'PY'
import base64, json, shlex, sys
row = json.loads(base64.b64decode(sys.argv[1]).decode())
for k in ['workdir','budget','model','label','task','timeout']:
    print(f"{k.upper()}={shlex.quote(str(row.get(k,'')))}")
PY
)"

    while true; do
      local running_count
      running_count=$(python3 - "$REGISTRY_DIR" "$batch_id" <<'PY'
import glob, json, os, sys
reg_dir, batch_id = sys.argv[1:3]
count = 0
for path in glob.glob(os.path.join(reg_dir, '*.json')):
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        if d.get('batch_id') == batch_id and d.get('status') == 'running':
            count += 1
    except Exception:
        pass
print(count)
PY
)
      [ "$running_count" -lt "$max_parallel" ] && break
      sleep 2
    done

    if [ -n "$TIMEOUT" ]; then
      bash "$0" dispatch "$WORKDIR" "$BUDGET" "$MODEL" "$LABEL" "$TASK" --timeout "$TIMEOUT" --batch-id "$batch_id" | tee -a "$tmp_handles"
    else
      bash "$0" dispatch "$WORKDIR" "$BUDGET" "$MODEL" "$LABEL" "$TASK" --batch-id "$batch_id" | tee -a "$tmp_handles"
    fi
    sleep 1
  done < <(python3 - "$manifest" <<'PY'
import base64, json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        print(base64.b64encode(line.encode()).decode())
PY
)

  echo "==="
  echo "{\"batch_id\": \"$batch_id\", \"manifest\": \"$manifest\", \"handles_file\": \"$tmp_handles\"}"
}

cmd_list() {
  local filter="${1:---all}"
  python3 - "$REGISTRY_DIR" "$filter" <<'PY'
import json, glob, os, sys
reg_dir, filt = sys.argv[1:3]
tasks = []
for f in glob.glob(os.path.join(reg_dir, '*.json')):
    try:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        tasks.append(d)
    except Exception:
        pass
tasks.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
if filt == '--running':
    tasks = [t for t in tasks if t.get('status') == 'running']
elif filt == '--done':
    tasks = [t for t in tasks if t.get('status') == 'done']
elif filt == '--failed':
    tasks = [t for t in tasks if t.get('status') in ('failed','timeout')]
if not tasks:
    print('No tasks found.')
else:
    for t in tasks[:30]:
        sid = (t.get('session_id') or '')[:12]
        cost = t.get('cost_usd', 0) or 0
        extra = f" batch:{t.get('batch_id')}" if t.get('batch_id') else ''
        print(f"{t.get('status','?'):8} | {t.get('task_id','?'):40} | ${cost:.3f} | {t.get('label','')} | sid:{sid}{extra}")
PY
}

cmd_cancel() {
  local task_id="${1:-}"
  if [ -z "$task_id" ]; then echo '{"error": "No task_id"}' >&2; exit 1; fi
  local reg_file="$REGISTRY_DIR/${task_id}.json"
  [ -f "$reg_file" ] || { echo "{\"error\": \"Task not found: $task_id\"}"; exit 1; }

  local pid
  pid=$(python3 -c "import json; print(json.load(open('$reg_file')).get('pid', ''))")
  if [ -n "$pid" ]; then
    kill -TERM "$pid" 2>/dev/null && echo "Killed PID $pid" || echo "PID $pid not running"
    pkill -P "$pid" 2>/dev/null || true
  fi
  write_registry "$task_id" "cancelled" "" "" "" "" "" "" "0" ""
  echo "{\"task_id\": \"$task_id\", \"status\": \"cancelled\"}"
}

cmd_costs() {
  local filter="${1:---today}"
  if [ ! -f "$COST_LOG" ]; then
    echo "No cost data yet."
    exit 0
  fi
  python3 - "$COST_LOG" "$filter" <<'PY'
import json, sys
from datetime import datetime
cost_log, filt = sys.argv[1:3]
entries = []
with open(cost_log, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
if filt == '--today':
    today = datetime.now().strftime('%Y-%m-%d')
    entries = [e for e in entries if e.get('ts', '').startswith(today)]
total = sum(e.get('cost_usd', 0) for e in entries)
by_model = {}
for e in entries:
    m = e.get('model', 'unknown')
    by_model[m] = by_model.get(m, 0) + e.get('cost_usd', 0)
print(f'Tasks: {len(entries)}')
print(f'Total cost: ${total:.4f}')
print('By model:')
for m, c in sorted(by_model.items(), key=lambda x: -x[1]):
    print(f'  {m}: ${c:.4f}')
print('By task:')
for e in entries[-10:]:
    print(f"  {e.get('task_id','?'):40} | ${e.get('cost_usd',0):.4f} | {e.get('status','?')}")
PY
}

cmd_cleanup() {
  local count=0
  for f in "$REGISTRY_DIR"/*.json; do
    [ -f "$f" ] || continue
    local age=$(( ($(date +%s) - $(stat -c %Y "$f")) / 3600 ))
    if [ "$age" -gt 48 ]; then
      local status
      status=$(python3 -c "import json; print(json.load(open('$f')).get('status', ''))" 2>/dev/null)
      if [ "$status" = "done" ] || [ "$status" = "failed" ] || [ "$status" = "cancelled" ] || [ "$status" = "timeout" ]; then
        rm -f "$f"
        count=$((count + 1))
      fi
    fi
  done
  find "$LOGS_DIR" -name "*.out" -mmin +2880 -delete 2>/dev/null || true
  find "$LOGS_DIR" -name "*.stream" -mmin +2880 -delete 2>/dev/null || true
  find "$LOGS_DIR" -name "*.stderr" -mmin +2880 -delete 2>/dev/null || true
  find "$RESULTS_DIR" -name "*.json" -mmin +2880 -delete 2>/dev/null || true
  find "$HOOKS_DIR" -type f -mmin +2880 -delete 2>/dev/null || true
  echo "Cleaned $count old registry entries and old logs/results"
}

CMD="${1:-}"
shift || true

case "$CMD" in
  dispatch) cmd_dispatch "$@" ;;
  poll)     cmd_poll "$@" ;;
  watch)    cmd_watch "$@" ;;
  result)   cmd_result "$@" ;;
  resume)   cmd_resume "$@" ;;
  batch)    cmd_batch "$@" ;;
  list)     cmd_list "$@" ;;
  cancel)   cmd_cancel "$@" ;;
  costs)    cmd_costs "$@" ;;
  cleanup)  cmd_cleanup "$@" ;;
  *)
    echo "Claude Code Orchestrator"
    echo ""
    echo "Commands:"
    echo "  dispatch <workdir> <budget> <model> <label> \"<task>\" [--timeout N] [--notify-cmd CMD] [--expect-file PATH] [--expect-min-bytes N] [--next-action TEXT] [--continuation-mode continue|switch|blocked]"
    echo "  poll <task-id>"
    echo "  watch <task-id>"
    echo "  result [--text|--raw] <task-id>"
    echo "  resume <task-id> <budget> \"<follow-up>\" [--timeout N] [--notify-cmd CMD] [--expect-file PATH] [--expect-min-bytes N] [--next-action TEXT] [--continuation-mode continue|switch|blocked]"
    echo "  batch <manifest.jsonl> [--max-parallel N]"
    echo "  list [--running|--done|--failed|--all]"
    echo "  cancel <task-id>"
    echo "  costs [--today|--all]"
    echo "  cleanup"
    ;;
esac
