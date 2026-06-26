#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
state_kv.sh get <key>
state_kv.sh set <key> <value> [ttl_seconds]
state_kv.sh del <key>
EOF
}

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$DIR/../../.." && pwd)"
STACK_ROOT="${MEMORY_STACK_ROOT:-$WORKSPACE_ROOT/infra/memory-stack}"
ENV_FILE="${MEMORY_STACK_ENV:-$STACK_ROOT/.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD:-}"

CLI=(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT")
if [[ -n "$REDIS_PASSWORD" ]]; then
  CLI+=(-a "$REDIS_PASSWORD")
fi

cmd="$1"
shift
case "$cmd" in
  get)
    key="$1"
    "${CLI[@]}" GET "$key"
    ;;
  set)
    if [[ $# -lt 2 ]]; then
      usage >&2; exit 1
    fi
    key="$1"; value="$2"
    if [[ $# -ge 3 ]]; then
      ttl="$3"
      "${CLI[@]}" SET "$key" "$value" EX "$ttl"
    else
      "${CLI[@]}" SET "$key" "$value"
    fi
    ;;
  del)
    key="$1"
    "${CLI[@]}" DEL "$key"
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
