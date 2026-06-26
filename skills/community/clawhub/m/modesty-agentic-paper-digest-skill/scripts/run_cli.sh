#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$HOME/agentic_paper_digest}"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "PROJECT_DIR not found: $PROJECT_DIR"
  echo "Run scripts/bootstrap.sh first."
  exit 1
fi

cd "$PROJECT_DIR"

if [ ! -d ".venv" ]; then
  echo "Missing .venv in $PROJECT_DIR"
  echo "Run scripts/bootstrap.sh first."
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

ENV_FILE="${ENV_FILE:-.env}"
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

# Map SKILLBOSS_API_KEY to LiteLLM provider settings for SkillBoss API Hub
if [ -n "${SKILLBOSS_API_KEY:-}" ]; then
  export LITELLM_API_BASE="${LITELLM_API_BASE:-https://api.skillboss.co/v1}"
  export LITELLM_API_KEY="${SKILLBOSS_API_KEY}"
fi

python -m paper_finder run --json "$@"
