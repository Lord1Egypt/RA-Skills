#!/usr/bin/env bash
set -euo pipefail

# Sync from RUNTIME (source of truth) -> ARTIFACT (ClawHub publish workdir)

RUNTIME_DIR="${RUNTIME_DIR:-/Users/lijunsheng/.openclaw/workspace-jun-invest-option-master-agent}"
ARTIFACT_AGENT_DIR="${ARTIFACT_AGENT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/agent}"

if [[ ! -d "${RUNTIME_DIR}" ]]; then
  echo "FAIL: runtime workspace not found: ${RUNTIME_DIR}" >&2
  exit 1
fi

mkdir -p "${ARTIFACT_AGENT_DIR}"

echo "Sync runtime -> artifact"
echo "  runtime:  ${RUNTIME_DIR}"
echo "  artifact: ${ARTIFACT_AGENT_DIR}"

# One-time safety cleanup: ensure runtime-only files never live in artifact
rm -rf "${ARTIFACT_AGENT_DIR}/memory" >/dev/null 2>&1 || true
rm -f "${ARTIFACT_AGENT_DIR}/.publish-state.json" >/dev/null 2>&1 || true
rm -f "${ARTIFACT_AGENT_DIR}/.publish-now" >/dev/null 2>&1 || true

rsync -a --delete \
  --exclude '.openclaw/' \
  --exclude '.git/' \
  --exclude 'memory/' \
  --exclude '.publish-state.json' \
  --exclude '.publish-now' \
  --exclude '**/.venv/' \
  --exclude '**/__pycache__/' \
  --exclude '**/*.pyc' \
  --exclude '**/*.pyo' \
  --exclude '**/.DS_Store' \
  --exclude 'logs/' \
  --exclude 'tmp/' \
  "${RUNTIME_DIR}/" \
  "${ARTIFACT_AGENT_DIR}/"

# Record which runtime commit this artifact was synced from
if command -v git >/dev/null 2>&1 && [[ -d "${RUNTIME_DIR}/.git" ]]; then
  (cd "${RUNTIME_DIR}" && git rev-parse HEAD) > "${ARTIFACT_AGENT_DIR}/.runtime-head" || true
fi

echo "OK: synced."
