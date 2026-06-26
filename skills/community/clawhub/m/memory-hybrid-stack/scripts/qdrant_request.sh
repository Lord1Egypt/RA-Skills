#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: qdrant_request.sh <METHOD> <PATH> [json | @file]" >&2
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

QDRANT_HOST="${QDRANT_HOST:-localhost}"
QDRANT_PORT="${QDRANT_HTTP_PORT:-6333}"
BASE_URL="${QDRANT_URL:-http://$QDRANT_HOST:$QDRANT_PORT}"

METHOD="$1"; shift
PATH_SEG="$1"; shift
if [[ "$PATH_SEG" != /* ]]; then
  PATH_SEG="/$PATH_SEG"
fi

EXTRA_ARGS=()
if [[ $# -gt 0 ]]; then
  DATA="$1"
  if [[ "$DATA" == @* ]]; then
    FILE_PATH="${DATA:1}"
    EXTRA_ARGS=(--data-binary "@${FILE_PATH}")
  else
    EXTRA_ARGS=(--data "$DATA")
  fi
fi

curl -fsSL -X "$METHOD" "$BASE_URL$PATH_SEG" \
  -H "Content-Type: application/json" \
  "${EXTRA_ARGS[@]}"
