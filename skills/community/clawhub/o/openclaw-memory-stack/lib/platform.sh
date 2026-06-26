#!/usr/bin/env bash
# OpenClaw Memory Stack — Cross-platform helpers
# Sourced by all wrappers and router scripts.

# Millisecond timestamp (portable)
now_ms() {
  if command -v gdate &>/dev/null; then
    gdate +%s%3N
  elif command -v python3 &>/dev/null; then
    python3 -c "import time; print(int(time.time()*1000))"
  else
    # Fallback: seconds * 1000
    echo $(( $(date +%s) * 1000 ))
  fi
}

# ISO 8601 timestamp
now_iso() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# JSON-safe string escaping
json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

# Portable timeout command
# Usage: run_with_timeout <ms> <command> [args...]
run_with_timeout() {
  local timeout_ms="$1"; shift
  local timeout_s=$(( timeout_ms / 1000 ))
  [ "$timeout_s" -lt 1 ] && timeout_s=1

  if command -v gtimeout &>/dev/null; then
    gtimeout "${timeout_s}s" "$@"
  elif command -v timeout &>/dev/null; then
    timeout "${timeout_s}s" "$@"
  else
    # No timeout command — run directly
    "$@"
  fi
}

# Check if a command exists
has_command() {
  command -v "$1" &>/dev/null
}

# Detect OS
detect_os() {
  case "$(uname -s)" in
    Darwin*) echo "macOS" ;;
    Linux*)  echo "Linux" ;;
    MINGW*|MSYS*|CYGWIN*) echo "Windows" ;;
    *)       echo "unknown" ;;
  esac
}

# Portable process group kill
# Usage: kill_process_group <pid>
kill_process_group() {
  local pid="$1"
  if kill -0 "$pid" 2>/dev/null; then
    kill -- -"$pid" 2>/dev/null || kill "$pid" 2>/dev/null || true
  fi
}

# Read JSON field using python3 (jq-free fallback)
# Usage: json_field <file> <field>
json_field() {
  local file="$1" field="$2"
  if has_command jq; then
    jq -r ".$field // empty" "$file" 2>/dev/null
  elif has_command python3; then
    python3 -c "import json,sys; d=json.load(open('$file')); print(d.get('$field',''))" 2>/dev/null
  else
    echo ""
  fi
}

# Read nested JSON field
# Usage: json_nested <file> <path> (dot-separated, e.g., "backends.qmd.status")
json_nested() {
  local file="$1" path="$2"
  if has_command jq; then
    jq -r ".$path // empty" "$file" 2>/dev/null
  elif has_command python3; then
    python3 -c "
import json,sys,functools
d=json.load(open('$file'))
keys='$path'.split('.')
try:
  val=functools.reduce(lambda o,k: o[k], keys, d)
  print(val if val is not None else '')
except (KeyError, TypeError):
  print('')
" 2>/dev/null
  else
    echo ""
  fi
}

# Portable file locking
# Usage: portable_flock <lockfile> <command...>
# macOS lacks flock; fallback to python3 fcntl
portable_flock() {
  local lockfile="$1"; shift
  if command -v flock &>/dev/null; then
    flock -w 5 "$lockfile" "$@"
  elif has_command python3; then
    python3 -c "
import fcntl, subprocess, sys
fd = open('$lockfile', 'w')
try:
    fcntl.flock(fd, fcntl.LOCK_EX)
    result = subprocess.run(sys.argv[1:], check=False)
    sys.exit(result.returncode)
finally:
    fcntl.flock(fd, fcntl.LOCK_UN)
    fd.close()
" "$@"
  else
    # No locking available — run directly
    "$@"
  fi
}

# Atomic JSON update with file locking
# Usage: locked_update_json <file> <dot.path.key> <value>
# Value is passed via stdin-safe mechanism to avoid shell quoting issues
locked_update_json() {
  local file="$1" key="$2" value="$3"
  local lockfile="${file}.lock"
  local tmp="${file}.tmp.$$"

  local update_script
  update_script=$(cat <<'PYEOF'
import json, sys, os

file_path = sys.argv[1]
key_path = sys.argv[2]
raw_value = sys.argv[3]

with open(file_path) as f:
    d = json.load(f)

keys = key_path.split('.')
target = d
for k in keys[:-1]:
    target = target.setdefault(k, {})

# Try parsing as JSON first, fall back to string
try:
    target[keys[-1]] = json.loads(raw_value)
except (json.JSONDecodeError, ValueError):
    target[keys[-1]] = raw_value

tmp_path = sys.argv[4]
with open(tmp_path, 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')

os.rename(tmp_path, file_path)
PYEOF
  )

  if command -v flock &>/dev/null; then
    (
      flock -w 5 200 || { echo "Failed to acquire lock on $file" >&2; return 1; }
      python3 -c "$update_script" "$file" "$key" "$value" "$tmp"
    ) 200>"$lockfile"
  elif has_command python3; then
    python3 -c "
import fcntl, subprocess, sys, os
lockfile = '$lockfile'
fd = open(lockfile, 'w')
try:
    fcntl.flock(fd, fcntl.LOCK_EX)
    import json
    file_path = sys.argv[1]
    key_path = sys.argv[2]
    raw_value = sys.argv[3]
    tmp_path = sys.argv[4]
    with open(file_path) as f:
        d = json.load(f)
    keys = key_path.split('.')
    target = d
    for k in keys[:-1]:
        target = target.setdefault(k, {})
    try:
        target[keys[-1]] = json.loads(raw_value)
    except (json.JSONDecodeError, ValueError):
        target[keys[-1]] = raw_value
    with open(tmp_path, 'w') as f:
        json.dump(d, f, indent=2)
        f.write('\n')
    os.rename(tmp_path, file_path)
finally:
    fcntl.flock(fd, fcntl.LOCK_UN)
    fd.close()
" "$file" "$key" "$value" "$tmp"
  else
    echo "Warning: No locking mechanism available" >&2
    python3 -c "$update_script" "$file" "$key" "$value" "$tmp"
  fi
}
