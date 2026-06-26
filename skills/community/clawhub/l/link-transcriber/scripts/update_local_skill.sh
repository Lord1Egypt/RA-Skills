#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-latest}"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="${CODEX_HOME_DIR}/skills"
CANONICAL_SLUG="link-transcriber"
LEGACY_SLUG="link-transcriber-skill-public"

mkdir -p "${SKILLS_DIR}"

install_cmd=(
  npx clawhub@latest
  --workdir "${CODEX_HOME_DIR}"
  --dir skills
  install "${CANONICAL_SLUG}"
  --force
)

if [[ "${VERSION}" != "latest" ]]; then
  install_cmd+=(--version "${VERSION}")
fi

echo "Installing ${CANONICAL_SLUG} into ${SKILLS_DIR}..."
"${install_cmd[@]}"

if [[ -e "${SKILLS_DIR}/${LEGACY_SLUG}" ]]; then
  echo "Removing legacy local directory ${SKILLS_DIR}/${LEGACY_SLUG}"
  rm -rf "${SKILLS_DIR:?}/${LEGACY_SLUG}"
fi

echo "Local skill is ready at ${SKILLS_DIR}/${CANONICAL_SLUG}"
