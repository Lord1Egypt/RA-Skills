#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$DIR/../../.." && pwd)"
STACK_ROOT="${MEMORY_STACK_ROOT:-$WORKSPACE_ROOT/infra/memory-stack}"
ENV_FILE="${MEMORY_STACK_ENV:-$STACK_ROOT/.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[facts_sql] Missing env file: $ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

PGHOST="${POSTGRES_HOST:-localhost}"
PGPORT="${POSTGRES_PORT:-5432}"
PGUSER="${POSTGRES_USER:?POSTGRES_USER missing}"
PGDB="${POSTGRES_DB:?POSTGRES_DB missing}"
PGPASSWORD="${POSTGRES_PASSWORD:?POSTGRES_PASSWORD missing}"

export PGPASSWORD

PSQL=(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDB" -v ON_ERROR_STOP=1)

if [[ $# -gt 0 ]]; then
  SQL="$*"
  printf '%s\n' "$SQL" | "${PSQL[@]}"
else
  "${PSQL[@]}"
fi
