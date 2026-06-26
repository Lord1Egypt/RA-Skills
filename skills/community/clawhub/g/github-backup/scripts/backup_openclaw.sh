#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
REPO_SLUG="nz365guy/openclaw-backup"
DEFAULT_BRANCH="main"
ENV_FILE="${WORKSPACE_DIR}/.env.local"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "[github-backup] Missing ${ENV_FILE}. Create it with GITHUB_TOKEN before running." >&2
  exit 1
fi

set +u
source "${ENV_FILE}"
set -u

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "[github-backup] GITHUB_TOKEN is undefined even after sourcing ${ENV_FILE}." >&2
  exit 1
fi

COMMIT_MSG=${1:-"Auto backup: $(date -Iseconds)"}

cd "${WORKSPACE_DIR}"
if git diff --quiet --ignore-submodules HEAD --; then
  echo "[github-backup] No changes to back up."
  exit 0
fi

# Ensure the remote exists
if ! git remote | grep -q "^origin$"; then
  git remote add origin "https://github.com/${REPO_SLUG}.git"
fi

# Stage, commit, push via token-authenticated URL

git add -A
git commit -m "${COMMIT_MSG}"
GIT_PUSH_URL="https://nz365guy:${GITHUB_TOKEN}@github.com/${REPO_SLUG}.git"
git push "${GIT_PUSH_URL}" "${DEFAULT_BRANCH}"

echo "[github-backup] Backup pushed to ${REPO_SLUG}@${DEFAULT_BRANCH}."
