# shellcheck shell=bash

# Auto-loads local environment overrides for the Memelord skill.
ENV_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.env"
if [[ -f "$ENV_FILE" ]]; then
  # Export everything defined in .env so child processes inherit the values.
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi
