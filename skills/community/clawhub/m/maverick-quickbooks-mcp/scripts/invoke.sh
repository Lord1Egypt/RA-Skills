#!/usr/bin/env bash
# invoke.sh — universal mcporter wrapper.
#
# Convention: the mcporter server key lives in {SKILL_DIR}/mcporter.json.
# The wrapper reads the manifest key; init-mcporter.sh reads URL + other server
# config from the same manifest.
#
# Always invoke mcporter through this wrapper, never directly.
set -eu

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="${SKILL_DIR}/mcporter.json"
SERVER="$(jq -er '(.mcpServers // {}) | keys_unsorted[0]' "${CONFIG}" 2>/dev/null)" \
  || { echo "invoke.sh: ${CONFIG} has no mcpServers entry (or file missing)" >&2; exit 1; }

bash "${SKILL_DIR}/scripts/init-mcporter.sh" "${SERVER}" "${CONFIG}"
exec env MCPORTER_CONFIG="${CONFIG}" mcporter "$@"
