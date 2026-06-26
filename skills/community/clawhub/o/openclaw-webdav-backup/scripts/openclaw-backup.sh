#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE_DIR="$(cd "${SKILL_DIR}/../.." && pwd)"
export OPENCLAW_WORKSPACE_DIR="${WORKSPACE_DIR}"
exec /usr/bin/bash "${SKILL_DIR}/scripts/openclaw-backup.impl.sh" "$@"
