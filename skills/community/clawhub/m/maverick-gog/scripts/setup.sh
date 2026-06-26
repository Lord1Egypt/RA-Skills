#!/usr/bin/env bash
# setup.sh — skill setup hook.
#
# Declared as `metadata.openclaw.setup.script` in SKILL.md. Invoked by the
# deployment harness (typically via the OpenClaw `skills.setup` WS RPC) after
# install and on credential rotation. The harness runs `bash setup.sh` with
# cwd set to the skill directory and SKILL_DIR exported.
#
# Thin delegator: enforces SKILL_DIR + the GOG_KEYRING_PASSWORD env-state
# contract, then delegates to init-gog-oauth.sh. Setup-hook env must provide:
# bash, jq, gog (>= v0.17.0). Of these, only `gog` is in SKILL.md
# `requires.bins` (the field gates agent-runtime eligibility; `gog` is needed
# at both setup and agent runtime). `bash` and `jq` are setup-time-only.

set -eu

: "${SKILL_DIR:?setup environment should export SKILL_DIR}"

# gogcli's file keyring distinguishes "unset" from "set to empty string":
# unset + non-TTY = hard error (errNoTTY); set (any value, including "") =
# silent (FixedStringPrompt). Verified at internal/secrets/store.go
# fileKeyringPasswordFuncFrom.
#
# Refuse setup if the env var is truly unset — the deployment must expose it
# (any value, including empty) so it reaches both the setup subprocess AND
# every later agent-runtime `gog ...` call. Normalizing here would only fix
# the setup subprocess; the agent would still hit errNoTTY on first API call.
if [ -z "${GOG_KEYRING_PASSWORD+x}" ]; then
  echo "setup.sh: ERROR — GOG_KEYRING_PASSWORD must be set in the container env (any value, including empty)." >&2
  echo "setup.sh:   Setting it only for this subprocess would leave the agent runtime broken on first \`gog\` call." >&2
  echo "setup.sh:   Empty string is acceptable (no at-rest crypto). A real per-instance passphrase is recommended." >&2
  exit 1
fi

if [ -z "${GOG_KEYRING_PASSWORD}" ]; then
  echo "setup.sh: WARNING — GOG_KEYRING_PASSWORD is empty (no at-rest crypto)." >&2
fi

bash "${SKILL_DIR}/scripts/init-gog-oauth.sh"
