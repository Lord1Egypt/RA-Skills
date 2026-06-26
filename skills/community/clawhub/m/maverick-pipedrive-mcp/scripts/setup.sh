#!/usr/bin/env bash
# setup.sh — skill setup hook.
#
# Declared as `metadata.openclaw.setup.script` in SKILL.md. Invoked by the
# deployment harness after install and on credential rotation. The harness runs
# `bash setup.sh` with cwd set to the skill directory and SKILL_DIR exported.
#
# Thin delegator to init-mcporter-oauth.sh. Setup-hook env must provide:
# bash, jq, mcporter (≥ v0.11.0), basename. These are NOT declared in
# SKILL.md `requires.bins`, which gates agent-runtime eligibility, not
# setup-time tooling.
#
# Idempotency note: the setup script unconditionally calls `mcporter vault
# set` — there is no in-skill marker fast-path. The caller must only run setup
# when the env it supplies is the freshest credential state.

set -eu

: "${SKILL_DIR:?setup environment should export SKILL_DIR}"

CONFIG="${SKILL_DIR}/mcporter.json"
SERVER="$(jq -er '(.mcpServers // {}) | keys_unsorted[0]' "${CONFIG}" 2>/dev/null)" \
  || { echo "setup.sh: ${CONFIG} has no mcpServers entry (or file missing)" >&2; exit 1; }

bash "${SKILL_DIR}/scripts/init-mcporter-oauth.sh" \
  "${SERVER}" \
  "${CONFIG}"
