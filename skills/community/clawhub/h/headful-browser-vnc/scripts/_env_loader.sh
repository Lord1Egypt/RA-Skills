SKILL_DIR=/
#!/usr/bin/env bash
# load .env if present (non-destructive). Exports variables to child processes.
# Prefer a .env colocated with the skill scripts directory; fall back to parent for backward-compat.
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SKILL_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  # backward-compat fallback
  ENV_FILE="$SKILL_DIR/../.env"
fi
if [ -f "$ENV_FILE" ]; then
  # ensure restrictive permissions
  perms=$(stat -c '%a' "$ENV_FILE" 2>/dev/null || echo "000")
  if [ "${perms}" != "600" ] && [ "${perms}" != "400" ]; then
    echo "Warning: $ENV_FILE should be chmod 600 (found $perms). Continue anyway." >&2
  fi
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi
