#!/usr/bin/env bash

set -euo pipefail

export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8:replace}"
export PYTHONUTF8="${PYTHONUTF8:-1}"
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
STATUS_DIR="${SYSTEM_ROOT}/status"
TASKS_DIR="${SYSTEM_ROOT}/tasks"
LOGS_DIR="${SYSTEM_ROOT}/logs"
TEMPLATES_DIR="${SYSTEM_ROOT}/templates"

print_divider() {
  printf '%s\n' "============================================================"
}

print_title() {
  print_divider
  printf '%s\n' "$1"
  print_divider
}

info() {
  printf '[信息] %s\n' "$*"
}

warn() {
  printf '[警告] %s\n' "$*" >&2
}

error() {
  printf '[错误] %s\n' "$*" >&2
}

die() {
  error "$*"
  exit 1
}

ensure_runtime_dirs() {
  mkdir -p "${STATUS_DIR}" "${TASKS_DIR}" "${LOGS_DIR}" "${TEMPLATES_DIR}"
}

require_command() {
  local command_name="$1"
  local help_text="${2:-}"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    if [[ -n "${help_text}" ]]; then
      die "缺少命令 ${command_name}。${help_text}"
    fi
    die "缺少命令 ${command_name}。"
  fi
}

detect_agent_command() {
  if command -v agent >/dev/null 2>&1; then
    printf '%s\n' "agent"
    return 0
  fi
  if command -v cursor-agent >/dev/null 2>&1; then
    printf '%s\n' "cursor-agent"
    return 0
  fi
  return 1
}

slugify() {
  python3 - "$1" <<'PY'
import re
import sys

value = sys.argv[1].strip().lower()
value = re.sub(r"[^a-z0-9]+", "-", value)
value = re.sub(r"-{2,}", "-", value).strip("-")
print(value or "task")
PY
}

now_iso() {
  python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
PY
}

timestamp_compact() {
  date +"%Y%m%d-%H%M%S"
}

status_file_path() {
  printf '%s\n' "${STATUS_DIR}/$1.json"
}

task_file_path() {
  printf '%s\n' "${TASKS_DIR}/$1.md"
}

runner_file_path() {
  printf '%s\n' "${TASKS_DIR}/$1.runner.sh"
}

log_file_path() {
  printf '%s\n' "${LOGS_DIR}/$1.log"
}

session_exists() {
  tmux has-session -t "$1" 2>/dev/null
}

pane_pid() {
  tmux display-message -p -t "$1" "#{pane_pid}" 2>/dev/null || true
}

pane_current_command() {
  tmux display-message -p -t "$1" "#{pane_current_command}" 2>/dev/null || true
}

pane_current_path() {
  tmux display-message -p -t "$1" "#{pane_current_path}" 2>/dev/null || true
}

capture_recent_output() {
  local session_name="$1"
  local lines="${2:-30}"
  tmux capture-pane -t "${session_name}" -p -S "-${lines}" 2>/dev/null || true
}

pretty_print_json() {
  python3 - "$1" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
print(json.dumps(data, ensure_ascii=False, indent=2))
PY
}

resolve_session_name() {
  local query="${1:-}"
  [[ -n "${query}" ]] || return 1

  python3 - "${STATUS_DIR}" "${query}" <<'PY'
import json
import os
import sys
from datetime import datetime

status_dir = sys.argv[1]
query = sys.argv[2].strip()

if not query or not os.path.isdir(status_dir):
    sys.exit(1)

def parse_time(value: str) -> datetime:
    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return datetime.min

records = []
for name in os.listdir(status_dir):
    if not name.endswith(".json"):
        continue
    path = os.path.join(status_dir, name)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        continue
    session_name = str(data.get("sessionName") or os.path.splitext(name)[0]).strip()
    task_name = str(data.get("taskName") or "").strip()
    created_at = str(data.get("createdAt") or "").strip()
    records.append({
        "session": session_name,
        "task": task_name,
        "createdAt": created_at,
    })

exact = [r for r in records if query == r["session"]]
if exact:
    exact.sort(key=lambda item: parse_time(item["createdAt"]), reverse=True)
    print(exact[0]["session"])
    sys.exit(0)

partial = [
    r for r in records
    if query in r["session"] or (r["task"] and query in r["task"])
]
if partial:
    partial.sort(key=lambda item: parse_time(item["createdAt"]), reverse=True)
    print(partial[0]["session"])
    sys.exit(0)

sys.exit(1)
PY
}

update_status_file() {
  local file_path="$1"
  shift

  python3 - "${file_path}" "$@" <<'PY'
import json
import os
import sys

path = sys.argv[1]
pairs = sys.argv[2:]

data = {}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        data = {}

def parse_value(raw: str):
    if raw.startswith("json:"):
        return json.loads(raw[5:])
    if raw == "null":
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    return raw

for pair in pairs:
    key, value = pair.split("=", 1)
    current = data
    pieces = key.split(".")
    for part in pieces[:-1]:
        node = current.get(part)
        if not isinstance(node, dict):
          node = {}
          current[part] = node
        current = node
    current[pieces[-1]] = parse_value(value)

with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
PY
}

list_known_sessions() {
  python3 - "${STATUS_DIR}" <<'PY'
import json
import os
import sys

status_dir = sys.argv[1]
if not os.path.isdir(status_dir):
    sys.exit(0)

items = []
for name in os.listdir(status_dir):
    if not name.endswith(".json"):
        continue
    path = os.path.join(status_dir, name)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        continue
    items.append((
        str(data.get("createdAt") or ""),
        str(data.get("sessionName") or os.path.splitext(name)[0]),
        str(data.get("status") or "unknown"),
        str(data.get("taskName") or ""),
    ))

for _, session_name, status, task_name in sorted(items, reverse=True):
    print(f"{session_name}\t{status}\t{task_name}")
PY
}
