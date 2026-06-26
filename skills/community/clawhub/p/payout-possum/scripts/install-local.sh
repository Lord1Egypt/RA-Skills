#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

install_dir() {
  local target_root="$1"
  local target_dir="${target_root}/payout-possum"

  mkdir -p "${target_root}"
  rm -rf "${target_dir}"
  mkdir -p "${target_dir}/agents" "${target_dir}/references"

  cp "${SKILL_DIR}/SKILL.md" "${target_dir}/SKILL.md"
  cp "${SKILL_DIR}/agents/openai.yaml" "${target_dir}/agents/openai.yaml"
  cp "${SKILL_DIR}/references/"*.md "${target_dir}/references/"

  if [ -f "${SKILL_DIR}/.clawhubignore" ]; then
    cp "${SKILL_DIR}/.clawhubignore" "${target_dir}/.clawhubignore"
  fi
}

install_dir "${HOME}/.codex/skills"
install_dir "${HOME}/.openclaw/skills"

echo "Installed payout-possum to:"
echo "  ${HOME}/.codex/skills/payout-possum"
echo "  ${HOME}/.openclaw/skills/payout-possum"
echo
echo "Restart or refresh the target client to load the updated skill."
