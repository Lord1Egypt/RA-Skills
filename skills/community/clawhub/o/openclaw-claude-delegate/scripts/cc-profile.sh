#!/bin/bash
# Claude Code profile wrapper
# Usage:
#   cc-profile.sh <profile> dispatch <budget> <model> <label> "<task>" [extra cc-orchestrator options]
#   cc-profile.sh <profile> resume <task-id> <budget> "<follow-up>" [extra cc-orchestrator options]
#   cc-profile.sh <profile> env
# Profiles are defined in ../profiles.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROFILES_JSON="${CLAUDE_DELEGATE_PROFILES:-${SCRIPT_DIR%/scripts}/profiles.json}"
CC_ORCH="$SCRIPT_DIR/cc-orchestrator.sh"

PROFILE="${1:-}"
CMD="${2:-}"
shift 2 || true

if [ -z "$PROFILE" ] || [ -z "$CMD" ]; then
  echo "Usage: $0 <profile> <dispatch|resume|env> ..." >&2
  exit 1
fi

read_profile() {
  python3 - "$PROFILES_JSON" "$PROFILE" <<'PY'
import json, os, sys, shlex
p, profile = sys.argv[1:3]
with open(p, encoding='utf-8') as f:
    j = json.load(f)
if profile not in j:
    raise SystemExit(f'Unknown profile: {profile}')
prof = j[profile]

def norm(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))

workdir = norm(prof['workdir'])
add_dirs = [norm(d) for d in prof.get('add_dirs', [])]
print('WORKDIR=' + shlex.quote(workdir))
print('CC_ADD_DIRS=' + shlex.quote(':'.join(add_dirs)))
print('PROFILE_NOTES=' + shlex.quote(prof.get('notes', '')))
PY
}

eval "$(read_profile)"

case "$CMD" in
  env)
    echo "PROFILE=$PROFILE"
    echo "WORKDIR=$WORKDIR"
    echo "CC_ADD_DIRS=$CC_ADD_DIRS"
    echo "PROFILE_NOTES=$PROFILE_NOTES"
    ;;
  dispatch)
    BUDGET="${1:-1.00}"
    MODEL="${2:-sonnet}"
    LABEL="${3:-task}"
    TASK="${4:-}"
    shift 4 || true
    [ -n "$TASK" ] || { echo "Need task" >&2; exit 1; }
    CC_ADD_DIRS="$CC_ADD_DIRS" bash "$CC_ORCH" dispatch "$WORKDIR" "$BUDGET" "$MODEL" "$LABEL" "$TASK" "$@"
    ;;
  resume)
    TASK_ID="${1:-}"
    BUDGET="${2:-0.50}"
    FOLLOW_UP="${3:-}"
    shift 3 || true
    [ -n "$TASK_ID" ] && [ -n "$FOLLOW_UP" ] || { echo "Need task-id and follow-up" >&2; exit 1; }
    CC_ADD_DIRS="$CC_ADD_DIRS" bash "$CC_ORCH" resume "$TASK_ID" "$BUDGET" "$FOLLOW_UP" "$@"
    ;;
  *)
    echo "Unknown command: $CMD" >&2
    exit 1
    ;;
esac
