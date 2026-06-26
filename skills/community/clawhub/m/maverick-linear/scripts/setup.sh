#!/usr/bin/env bash
# setup.sh — skill setup hook.
#
# Declared as `metadata.openclaw.setup.script` in SKILL.md. Invoked by the
# OpenClaw skills-setup gateway plugin (`skills.setup` method) after install
# and on credential rotation. The plugin runs `bash setup.sh` with cwd set to
# the skill directory and SKILL_DIR exported; operator-supplied env from the
# RPC call merges over `skills.entries.<slug>.env` from openclaw.json. See
# maverick_openclaw/cloudflare/plugins/skills-setup/index.js for the runner.
#
# Thin delegator to init-mcporter-oauth.sh. Setup-hook env must provide:
# bash, jq, mcporter (≥ v0.11.0), basename. These are NOT declared in
# SKILL.md `requires.bins`, which gates agent-runtime eligibility, not
# setup-time tooling.
#
# Idempotency note: the setup script unconditionally calls `mcporter vault
# set` — there is no in-skill marker fast-path. The caller (maverick_poc)
# MUST only fire skills.setup when the env it supplies is Maverick's
# freshest credential state; see maverick_openclaw/docs/skill-install.md
# § "Re-run policy".

set -eu

: "${SKILL_DIR:?skills-setup plugin should export SKILL_DIR}"

bash "${SKILL_DIR}/scripts/init-mcporter-oauth.sh" \
  "$(basename "${SKILL_DIR}")" \
  "${SKILL_DIR}/mcporter.json"
