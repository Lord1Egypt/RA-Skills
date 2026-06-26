#!/usr/bin/env bash
set -euo pipefail
# Continuous Claude loop: 1 TODO per Claude session.
#
# Usage:
#   bash scripts/claude_loop.sh               # auto-pick next unchecked Txxx from docs/TODO.md
#   bash scripts/claude_loop.sh T104          # force a specific TODO id
#   MAX_ITERS=48 bash scripts/claude_loop.sh  # run up to N tasks
#   RETRY_DELAY=15 bash scripts/claude_loop.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

TERM="${TERM:-xterm}"
export TERM

MAX_ITERS="${MAX_ITERS:-999999}"
RETRY_DELAY="${RETRY_DELAY:-10}"
PROMPT_TEMPLATE="${PROMPT_TEMPLATE:-prompts/claude_loop_prompt.txt}"

mkdir -p .claude/out .claude/logs

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1"
    exit 1
  }
}

preflight_check() {
  [[ -f docs/TODO.md ]] || { echo "Missing docs/TODO.md"; exit 1; }
  [[ -f docs/STATE.md ]] || { echo "Missing docs/STATE.md"; exit 1; }
  [[ -f docs/FEEDBACK.md ]] || { echo "Missing docs/FEEDBACK.md"; exit 1; }
  [[ -f CLAUDE.md ]] || { echo "Missing CLAUDE.md"; exit 1; }
  [[ -f "${PROMPT_TEMPLATE}" ]] || { echo "Missing ${PROMPT_TEMPLATE}"; exit 1; }
}

require_cmd claude
has_jq=1
if ! command -v jq >/dev/null 2>&1; then
  has_jq=0
fi

pick_next_todo() {
  grep -E '^- \[ \] T[0-9]+' -n docs/TODO.md \
    | head -n 1 \
    | sed -E 's/^.*\[ \] (T[0-9]+).*$/\1/'
}

build_prompt() {
  local todo_id="$1"
  python3 - "$todo_id" "$PROMPT_TEMPLATE" <<'PY'
from pathlib import Path
import sys

todo_id = sys.argv[1]
template_path = Path(sys.argv[2])
text = template_path.read_text(encoding='utf-8')
text = text.replace('{{ACTIVE_TODO}}', todo_id)
print(text)
PY
}

normalize_output() {
  local raw_file="$1"
  local out_file="$2"
  local todo_id="$3"

  python3 - "$raw_file" "$out_file" "$todo_id" <<'PY'
import json
import re
import sys
from pathlib import Path

raw_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
todo_id = sys.argv[3]

text = raw_path.read_text(encoding='utf-8', errors='ignore').strip()

def write_obj(obj):
    out_path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    sys.exit(0)

def try_extract_json_object(s: str):
    s = s.strip()

    # 1) 整体就是 JSON object
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # 2) 从文本中提取最后一个 JSON object
    decoder = json.JSONDecoder()
    for i in range(len(s)):
        if s[i] != '{':
            continue
        try:
            obj, end = decoder.raw_decode(s[i:])
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    return None

# 情况 A：raw_file 本身是 JSON
try:
    outer = json.loads(text)
    if isinstance(outer, dict):
        # A1: 已经是目标业务 JSON
        if "run_status" in outer and "completed" in outer:
            write_obj(outer)

        # A2: Claude CLI envelope，真正结果在 .result
        result_field = outer.get("result")
        if isinstance(result_field, str):
            inner = try_extract_json_object(result_field)
            if isinstance(inner, dict):
                write_obj(inner)
except Exception:
    pass

# 情况 B：原始文本里直接提取 JSON
inner = try_extract_json_object(text)
if isinstance(inner, dict) and "run_status" in inner:
    write_obj(inner)

fallback = {
    "run_status": "failed",
    "active_todo": todo_id,
    "completed": False,
    "summary": "Claude output was not valid task JSON",
    "files_changed": [],
    "state_updated": False,
    "todo_updated": False,
    "next_todo": "",
    "blockers": ["invalid_json_output"],
}
write_obj(fallback)
PY
}

run_claude_once() {
  local todo_id="$1"
  local ts out_json log_file prompt_file raw_out

  ts="$(date +%Y%m%d_%H%M%S)"
  out_json=".claude/out/${ts}_${todo_id}.json"
  log_file=".claude/logs/${ts}_${todo_id}.log"
  prompt_file=".claude/out/${ts}_${todo_id}.prompt.txt"
  raw_out=".claude/out/${ts}_${todo_id}.raw.txt"

  build_prompt "${todo_id}" > "${prompt_file}"

  echo
  echo "=== [${ts}] ACTIVE_TODO=${todo_id} ==="
  echo "log: ${log_file}"
  echo "out: ${out_json}"
  echo "prompt: ${prompt_file}"
  echo

  set +e
  claude -p "$(cat "${prompt_file}")" \
    --output-format json \
    > "${raw_out}" 2> "${log_file}"
  local rc=$?
  set -e

  if [[ $rc -ne 0 ]]; then
    echo "Claude exited with non-zero code: ${rc}"
    echo "See: ${log_file}"
    return $rc
  fi

  normalize_output "${raw_out}" "${out_json}" "${todo_id}"

  if [[ ! -s "${out_json}" ]]; then
    echo "Failed to normalize Claude output into JSON."
    echo "See raw output: ${raw_out}"
    return 1
  fi

  if [[ $has_jq -eq 1 ]]; then
    jq -r '"run_status=" + (.run_status // "-")
      + " completed=" + ((.completed // false)|tostring)
      + " next_todo=" + (.next_todo // "-")
      + " summary=" + (.summary // "")' "${out_json}" || true
  else
    echo "Tip: install jq for nicer summaries. Raw JSON at: ${out_json}"
  fi
}

main() {
  local forced_todo="${1:-}"
  preflight_check

  for ((i=1; i<=MAX_ITERS; i++)); do
    local todo_id latest_json completed status

    if [[ -n "${forced_todo}" ]]; then
      todo_id="${forced_todo}"
      forced_todo=""
    else
      todo_id="$(pick_next_todo || true)"
    fi

    if [[ -z "${todo_id}" ]]; then
      echo "No unchecked TODO found in docs/TODO.md. Stop."
      exit 0
    fi

    if ! run_claude_once "${todo_id}"; then
      echo "Retrying same TODO in ${RETRY_DELAY}s..."
      sleep "${RETRY_DELAY}"
      forced_todo="${todo_id}"
      continue
    fi

    if [[ $has_jq -eq 1 ]]; then
      latest_json="$(ls -t .claude/out/*_"${todo_id}".json 2>/dev/null | head -n 1 || true)"
      if [[ -n "${latest_json}" ]]; then
        completed="$(jq -r '.completed // false' "${latest_json}" 2>/dev/null || echo false)"
        status="$(jq -r '.run_status // ""' "${latest_json}" 2>/dev/null || echo "")"
        if [[ "${completed}" != "true" || "${status}" == "blocked" || "${status}" == "failed" ]]; then
          echo "Task ${todo_id} not fully completed; retrying same TODO in next round."
          forced_todo="${todo_id}"
        fi
      fi
    fi
  done
}

main "$@"
