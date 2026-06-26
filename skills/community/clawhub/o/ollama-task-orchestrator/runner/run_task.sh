#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# run_task.sh — Ollama Task Runner
#
# Executes tasks via a local Ollama instance with exclusivity locking.
# Locking prevents concurrent Ollama calls that would degrade generation quality.
#
# Configuration (environment variables):
#   WORKER_ROOT     Root directory for the worker (default: $HOME/worker)
#   PROJECTS_DIR    Directory containing projects (default: $WORKER_ROOT/projects)
#   DEFAULT_PROJECT Default project name used for context (default: "")
#   OLLAMA_MODEL    Model to use for code generation (default: qwen2.5-coder:32b)
#   OLLAMA_URL      Ollama API endpoint (default: http://localhost:11434/api/generate)
#   OLLAMA_TIMEOUT  Max seconds to wait for Ollama response (default: 300)
# ─────────────────────────────────────────────────────────────────────────────

WORKER_ROOT="${WORKER_ROOT:-$HOME/worker}"
PROJECTS_DIR="${PROJECTS_DIR:-$WORKER_ROOT/projects}"
DEFAULT_PROJECT="${DEFAULT_PROJECT:-}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5-coder:32b}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434/api/generate}"
OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT:-300}"
ALLOW_NL_EXEC="${ALLOW_NL_EXEC:-false}"
DRY_RUN=false

QUEUE_DIR="$WORKER_ROOT/queue"
LOCK_DIR="$QUEUE_DIR/ollama.lock.d"

while [ "${1:-}" = "--dry-run" ]; do
  DRY_RUN=true
  shift
done

TASK="${1:-}"
shift || true

# ── Locking ───────────────────────────────────────────────────────────────────
# Only acquire lock for tasks that call Ollama
NEEDS_LOCK=false
if [ "$DRY_RUN" = false ]; then
  case "$TASK" in
    help|ping|list-projects|test|exec|"") NEEDS_LOCK=false ;;
    *) NEEDS_LOCK=true ;;
  esac
fi

acquire_lock() {
  mkdir "$LOCK_DIR" 2>/dev/null || {
    echo "ERROR: Ollama is locked by another task ($(cat "$LOCK_DIR/pid" 2>/dev/null || echo 'unknown PID')). Try again shortly or run queue_status.sh clean."
    exit 1
  }
  echo $$ > "$LOCK_DIR/pid"
}

release_lock() {
  rm -rf "$LOCK_DIR"
}

if [ "$NEEDS_LOCK" = true ]; then
  mkdir -p "$QUEUE_DIR"
  acquire_lock
  trap release_lock EXIT
fi

# ── Job status header ─────────────────────────────────────────────────────────
print_status() {
  local active
  local api_base="${OLLAMA_URL%/api/generate}"
  active=$(curl -s --max-time 3 "$api_base/api/ps" 2>/dev/null | python3 -c \
    "import sys,json; m=json.load(sys.stdin).get('models',[]); print(m[0]['name']+' (busy)' if m else 'idle')" 2>/dev/null || echo "unknown")
  local lock_state="clear"
  if [ -d "$LOCK_DIR" ]; then
    lock_state="locked (PID $(cat "$LOCK_DIR/pid" 2>/dev/null || echo '?'))"
  fi
  local mode="live"
  if [ "$DRY_RUN" = true ]; then
    mode="dry-run"
  fi
  echo "┌─ Job: $TASK | Mode: $mode | Model: ${OLLAMA_MODEL} | Ollama: $active | Lock: $lock_state"
  echo "└─ Started: $(date '+%H:%M:%S') | Timeout: ${OLLAMA_TIMEOUT}s"
}

echo "=== RUNNER START ==="
print_status

# ── Ollama generation ─────────────────────────────────────────────────────────
ollama_generate() {
  local instruction="$1"
  local code_only="${2:-false}"
  local prompt="$instruction"

  # Prepend project context if available
  if [ -n "$DEFAULT_PROJECT" ]; then
    local context_file="$PROJECTS_DIR/$DEFAULT_PROJECT/AGENT.md"
    if [ -f "$context_file" ]; then
      local context
      context=$(cat "$context_file")
      prompt="Project context:
$context

Task: $instruction"
    fi
  fi

  if [ "$code_only" = "true" ]; then
    prompt="$prompt

Return ONLY the complete source code. No explanation, no markdown fences, no prose. Start directly with the code."
  fi

  local json_prompt
  json_prompt=$(printf '%s' "$prompt" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

  curl -s --max-time "$OLLAMA_TIMEOUT" "$OLLAMA_URL" -d "{
    \"model\": \"$OLLAMA_MODEL\",
    \"prompt\": $json_prompt,
    \"stream\": false
  }" | python3 -c 'import sys,json; print(json.load(sys.stdin)["response"])'
}

# ── Strip markdown fences — return pure code ──────────────────────────────────
strip_to_code() {
  python3 - "$1" << 'PYEOF'
import sys, re

text = open(sys.argv[1]).read()

blocks = re.findall(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)
if blocks:
    print(blocks[0].rstrip())
else:
    lines = text.splitlines()
    code_lines = [l for l in lines if not re.match(r'^(###|##|#|\*\*|--)', l)]
    print('\n'.join(code_lines).strip())
PYEOF
}

require_default_project() {
  if [ -z "$DEFAULT_PROJECT" ]; then
    echo "ERROR: DEFAULT_PROJECT is not set."
    exit 1
  fi
}

run_codegen() {
  local instruction="$1"
  if [ -z "$instruction" ]; then
    echo "ERROR: no instruction provided"
    echo "Usage: run_task.sh codegen \"write a function to...\""
    exit 1
  fi
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would generate code"
    echo "Instruction: $instruction"
    return 0
  fi
  ollama_generate "$instruction" false
}

run_write() {
  local rel_file="$1"
  local instruction="$2"

  if [ -z "$rel_file" ] || [ -z "$instruction" ]; then
    echo "ERROR: missing file path or instruction"
    echo "Usage: run_task.sh write <relative/path/file.ext> <instruction>"
    exit 1
  fi

  require_default_project

  case "$rel_file" in
    /*|../*|*/../*|..)
      echo "ERROR: file path must stay inside the project directory."
      exit 1
      ;;
  esac

  local target_file="$PROJECTS_DIR/$DEFAULT_PROJECT/$rel_file"
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would write generated code"
    echo "Target: $target_file"
    echo "Instruction: $instruction"
    return 0
  fi
  local tmp_file
  tmp_file=$(mktemp /tmp/ollama_output_XXXXXX)

  mkdir -p "$(dirname "$target_file")"
  ollama_generate "$instruction" true > "$tmp_file"
  strip_to_code "$tmp_file" > "$target_file"
  rm -f "$tmp_file"

  echo "WROTE: $target_file"
}

run_test() {
  local suite="${1:-all}"
  require_default_project

  local project_dir="$PROJECTS_DIR/$DEFAULT_PROJECT"
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would run tests"
    echo "Project: $project_dir"
    echo "Suite: $suite"
    return 0
  fi
  cd "$project_dir"

  case "$suite" in
    all)
      if [ -f "backend/venv/bin/python" ]; then
        ./backend/venv/bin/python -m pytest backend/tests/ --verbose
      else
        echo "ERROR: Python venv not found at backend/venv"
        exit 1
      fi
      ;;
    *)
      if [ -f "backend/venv/bin/python" ]; then
        ./backend/venv/bin/python -m pytest "backend/tests/test_${suite}.py" --verbose
      else
        echo "ERROR: Python venv not found at backend/venv"
        exit 1
      fi
      ;;
  esac
}

run_exec() {
  local cmd="$1"
  if [ -z "$cmd" ]; then
    echo "ERROR: no command provided"
    exit 1
  fi
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would run shell command"
    echo "Command: $cmd"
    return 0
  fi
  eval "$cmd"
}

run_list_projects() {
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would list projects from $PROJECTS_DIR"
    return 0
  fi
  ls "$PROJECTS_DIR"
}

interpret_nl_request() {
  local request="$1"
  local project_context=""
  if [ -n "$DEFAULT_PROJECT" ]; then
    project_context="default project: $DEFAULT_PROJECT"
  else
    project_context="default project: unset"
  fi

  python3 - "$request" "$project_context" "$ALLOW_NL_EXEC" << 'PYEOF'
import json
import re
import sys

request = sys.argv[1].strip()
project_context = sys.argv[2]
allow_nl_exec = sys.argv[3].lower() == "true"
lower = request.lower()
path_pattern = r"[A-Za-z0-9_./-]+\.[A-Za-z0-9_+-]+"

def clean_text(value):
    return value.strip().strip("\"'`").strip(" .,:;!?")

def normalize_path(value):
    return clean_text(value)

def emit(action, instruction="", path="", suite="", command="", source="rule"):
    print(json.dumps({
        "action": action,
        "instruction": instruction,
        "path": path,
        "suite": suite,
        "command": command,
        "source": source,
    }))
    raise SystemExit

if not request:
    emit("error", instruction="empty request")

if re.search(r"\b(list|show)\b.*\bprojects\b", lower) or "what projects" in lower:
    emit("list-projects")

if re.search(r"\b(run|execute)?\s*tests?\b", lower) or lower.startswith("test "):
    suite = "all"
    suite_patterns = [
        r"\btests?\s+(?:for|on|in)\s+([a-zA-Z0-9_-]+)\b",
        r"\btest\s+([a-zA-Z0-9_-]+)\b",
        r"\b([a-zA-Z0-9_-]+)\s+tests?\b",
    ]
    for pattern in suite_patterns:
        match = re.search(pattern, lower)
        if match and match.group(1) not in {"all", "suite"}:
            suite = match.group(1)
            break
    emit("test", suite=suite)

write_patterns = [
    rf"\b(?:write|create|add|update|put|implement)\b(?P<instruction>.+?)\b(?:to|in|into)\s+(?P<path>{path_pattern})\b",
    rf"\b(?:write|create|add|update|put|implement)\b\s+(?P<path>{path_pattern})\s+(?:with|to|for)\s+(?P<instruction>.+)$",
    rf"\b(?:write|create|add|update|put|implement)\b\s+(?P<path>{path_pattern})\b(?P<instruction>.+)$",
    rf"\b(?:in|into)\s+(?P<path>{path_pattern})\b[,:\s]+(?P<instruction>.+)$",
]
for pattern in write_patterns:
    write_match = re.search(pattern, request, re.IGNORECASE)
    if write_match:
        path = normalize_path(write_match.group("path"))
        instruction = clean_text(write_match.group("instruction"))
        if instruction and path:
            emit("write", instruction=instruction, path=path)

quoted_path_match = re.search(
    rf"(?P<path>{path_pattern})",
    request,
    re.IGNORECASE,
)
if quoted_path_match and re.search(r"\b(?:file|path|module|script|component|class)\b", lower):
    path = normalize_path(quoted_path_match.group("path"))
    instruction = clean_text(re.sub(path_pattern, "", request, count=1, flags=re.IGNORECASE))
    if instruction and path:
        emit("write", instruction=instruction, path=path, source="path-hint")

codegen_match = re.search(
    r"\b(?:generate|show|draft|design|outline|write|create|make|build)\b\s+(?P<instruction>.+)$",
    request,
    re.IGNORECASE,
)
if codegen_match:
    emit("codegen", instruction=clean_text(codegen_match.group("instruction")))

if allow_nl_exec and re.search(r"\b(?:run|execute)\s+(?:command|shell)\b", lower):
    command = re.sub(r"^\s*(?:run|execute)\s+(?:command|shell)\s*", "", request, flags=re.IGNORECASE).strip()
    emit("exec", command=command)

print(json.dumps({
    "action": "route-with-llm",
    "instruction": request,
    "path": "",
    "suite": "",
    "command": "",
    "source": "fallback",
    "context": project_context,
}))
PYEOF
}

llm_route_request() {
  local request="$1"
  local router_prompt
  router_prompt=$(cat <<EOF
You are a strict task router for a local Ollama runner.

Allowed actions:
- codegen: generate code or a technical answer
- write: generate code and write it to a relative project file
- test: run the test suite, optionally with a suite name
- list-projects: list available projects
$( [ "$ALLOW_NL_EXEC" = "true" ] && echo "- exec: run a shell command" )

Rules:
- Return exactly one JSON object.
- Do not wrap JSON in markdown fences.
- If the user asks to modify a file and names a file path, use action "write".
- For "write", include "path" and "instruction".
- For "codegen", include "instruction".
- For "test", include "suite" and use "all" if unspecified.
- For "list-projects", no extra fields are needed.
- Use "exec" only if the request clearly asks to run a shell command and exec is allowed.
- If the request is ambiguous, prefer "codegen" over "exec".
- Relative file paths only. Never use absolute paths or "..".

Return JSON with these keys:
{"action":"","instruction":"","path":"","suite":"","command":""}

User request:
$request
EOF
)

  ollama_generate "$router_prompt" false
}

validate_route_json() {
  local raw_json="$1"
  python3 - "$raw_json" "$ALLOW_NL_EXEC" << 'PYEOF'
import json
import re
import sys

raw = sys.argv[1]
allow_nl_exec = sys.argv[2].lower() == "true"

try:
    data = json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"ERROR: could not parse route JSON: {exc}")
    raise SystemExit(1)

action = data.get("action", "")
if action not in {"codegen", "write", "test", "list-projects", "exec"}:
    print(f"ERROR: unsupported routed action: {action}")
    raise SystemExit(1)

if action == "exec" and not allow_nl_exec:
    print("ERROR: NL exec routing is disabled. Set ALLOW_NL_EXEC=true to enable it.")
    raise SystemExit(1)

path = data.get("path", "")
if path:
    if path.startswith("/") or ".." in path.split("/"):
        print("ERROR: routed file path must stay inside the project directory.")
        raise SystemExit(1)
    if not re.match(r"^[A-Za-z0-9_./+-]+$", path):
        print("ERROR: routed file path contains unsupported characters.")
        raise SystemExit(1)

suite = data.get("suite", "") or "all"
instruction = data.get("instruction", "")
command = data.get("command", "")

print(json.dumps({
    "action": action,
    "instruction": instruction,
    "path": path,
    "suite": suite,
    "command": command,
}))
PYEOF
}

run_nl() {
  local request="$1"
  if [ -z "$request" ]; then
    echo "ERROR: no natural-language request provided"
    echo "Usage: run_task.sh [--dry-run] nl \"write a retry decorator in src/utils.py\""
    exit 1
  fi

  local route_json
  route_json=$(interpret_nl_request "$request")
  local action
  action=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"])')

  if [ "$action" = "route-with-llm" ]; then
    route_json=$(llm_route_request "$request")
  fi

  route_json=$(validate_route_json "$route_json")

  local routed_action instruction path suite command
  routed_action=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"])')
  instruction=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["instruction"])')
  path=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["path"])')
  suite=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["suite"])')
  command=$(printf '%s' "$route_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["command"])')

  echo "Interpreted request as: $routed_action"
  case "$routed_action" in
    codegen)
      [ -n "$instruction" ] && echo "Instruction: $instruction"
      run_codegen "$instruction"
      ;;
    write)
      echo "Path: $path"
      [ -n "$instruction" ] && echo "Instruction: $instruction"
      run_write "$path" "$instruction"
      ;;
    test)
      echo "Suite: ${suite:-all}"
      run_test "${suite:-all}"
      ;;
    list-projects)
      run_list_projects
      ;;
    exec)
      echo "Command: $command"
      run_exec "$command"
      ;;
  esac
}

# ── Commands ──────────────────────────────────────────────────────────────────
case "$TASK" in
  help)
    cat << 'HELP'
Ollama Task Runner — powered by a local Ollama model.

Commands:

  ping
    Check runner is alive.

  codegen <instruction>
    Generate code from an instruction using the configured Ollama model.
    Usage: run_task.sh [--dry-run] codegen "write a Python function to parse JSON"

  nl <request>
    Interpret a natural-language request, route it safely, then execute it.
    Usage: run_task.sh [--dry-run] nl "write a retry decorator in src/utils.py"

  write <relative/path/file.ext> <instruction>
    Generate code and write it to a file inside the project directory.
    Prose and markdown fences are stripped — file gets pure code.
    Usage: run_task.sh [--dry-run] write src/utils.py "write a retry decorator"

  test [suite]
    Run tests for the configured project.
    Usage: run_task.sh [--dry-run] test
    Usage: run_task.sh [--dry-run] test <suite_name>

  exec <shell command>
    Run any shell command on this machine.
    Usage: run_task.sh [--dry-run] exec "ls ~/worker/projects"

  list-projects
    List available projects in PROJECTS_DIR.

Environment variables:
  WORKER_ROOT, PROJECTS_DIR, DEFAULT_PROJECT, OLLAMA_MODEL, OLLAMA_URL, ALLOW_NL_EXEC

HELP
    ;;

  ping)
    echo "RUNNER_OK"
    ;;

  list-projects)
    run_list_projects
    ;;

  test)
    SUITE="${1:-all}"
    run_test "$SUITE"
    ;;

  codegen)
    INSTRUCTION="${*}"
    run_codegen "$INSTRUCTION"
    ;;

  write)
    REL_FILE="${1:-}"
    shift || true
    INSTRUCTION="${*}"
    run_write "$REL_FILE" "$INSTRUCTION"
    ;;

  exec)
    CMD="${*}"
    run_exec "$CMD"
    ;;

  nl)
    REQUEST="${*}"
    run_nl "$REQUEST"
    ;;

  "")
    echo "ERROR: no task specified. Run: run_task.sh help"
    exit 1
    ;;

  *)
    run_nl "$TASK${*:+ $*}"
    ;;
esac

echo "=== RUNNER END ==="
