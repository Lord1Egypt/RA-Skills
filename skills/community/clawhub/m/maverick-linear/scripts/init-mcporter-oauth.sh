#!/usr/bin/env bash
# init-mcporter-oauth.sh — OAuth vault seeder for HTTP+OAuth MCP servers.
#
# Pipes the env-supplied tokens to `mcporter vault set <server> --stdin`,
# which atomically writes the OAuth vault entry. Idempotent at the mcporter
# layer — calling with the same payload produces the same vault state.
#
# Usage: init-mcporter-oauth.sh <server-name> <config-path>
#
# Required env (prefix = uppercased server-name, hyphens → underscores, + "_MCP_"):
#   ${prefix}REFRESH_TOKEN  required
#   ${prefix}CLIENT_ID      required (DCR-issued)
#   ${prefix}ACCESS_TOKEN   required (seeding it skips mcporter's
#                                     first-request 401 → refresh round-trip)
#
# Orchestrator contract: the caller (e.g. maverick_poc) MUST only invoke this
# (via skills.setup) when the env it supplies is the freshest credential state
# Maverick has — otherwise this WILL clobber any refresh_token that mcporter's
# SDK rotated in-vault since the last setup call, breaking the integration
# until the user re-authorizes. See maverick_openclaw/docs/skill-install.md
# § "Re-run policy" for the orchestrator-side rules.
#
# Depends on mcporter ≥ v0.11.0 for `vault set --stdin` and for the file lock
# held around vault writes (so the script does not flock).

set -eu

mcp_server="${1:?server name required}"
mcp_config="${2:?config path required}"

mcp_prefix="$(printf '%s' "${mcp_server}" | tr '[:lower:]-' '[:upper:]_')_MCP_"
mcp_refresh_var="${mcp_prefix}REFRESH_TOKEN"
mcp_access_var="${mcp_prefix}ACCESS_TOKEN"
mcp_client_id_var="${mcp_prefix}CLIENT_ID"

mcp_refresh="${!mcp_refresh_var:?${mcp_refresh_var} required}"
mcp_client_id="${!mcp_client_id_var:?${mcp_client_id_var} required}"
mcp_access="${!mcp_access_var:?${mcp_access_var} required}"

# Token values pass via env to keep them out of /proc/<pid>/cmdline.
# `mcporter vault set` resolves the vault key from MCPORTER_CONFIG's
# definition for ${mcp_server}, so the script doesn't reproduce the
# vaultKeyForDefinition hash itself.
export MCPORTER_CONFIG="${mcp_config}"
mcp_access="${mcp_access}" mcp_refresh="${mcp_refresh}" mcp_client_id="${mcp_client_id}" \
  jq -cn '{
    tokens:     {access_token: env.mcp_access, refresh_token: env.mcp_refresh, token_type: "Bearer"},
    clientInfo: {client_id: env.mcp_client_id}
  }' \
  | mcporter vault set "${mcp_server}" --stdin
