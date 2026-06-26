#!/usr/bin/env bash
# init-mcporter-oauth.sh — OAuth vault seeder for HTTP+OAuth MCP servers.
#
# Pipes the env-supplied tokens to `mcporter vault set <server> --stdin`,
# which writes the OAuth vault entry using mcporter's own vault-key logic.
# Calling with the same payload produces the same vault state.
#
# Usage: init-mcporter-oauth.sh <server-name> <config-path>
#
# Required env (prefix = server-name with trailing "-mcp" or "-mcp-<digits>"
# stripped, then uppercased, hyphens -> underscores, + "_MCP_"):
#   ${prefix}REFRESH_TOKEN  required
#   ${prefix}ACCESS_TOKEN   required (seeding it skips mcporter's
#                                     first-request 401 → refresh round-trip)
#   <refresh.clientIdEnv> or ${prefix}CLIENT_ID required
#   <refresh.clientSecretEnv> required when mcporter.json declares one
#
# Provisioning contract: the caller MUST only invoke this when the env it
# supplies is the freshest credential state. Otherwise this can clobber a
# refresh_token that mcporter rotated in-vault since the last setup call.
#
# Depends on mcporter ≥ v0.11.0 for `vault set --stdin` and for the file lock
# held around vault writes (so the script does not flock).

set -eu

mcp_server="${1:?server name required}"
mcp_config="${2:?config path required}"

mcp_server_entry="$(jq -er --arg s "${mcp_server}" '.mcpServers[$s] // empty' "${mcp_config}" 2>/dev/null)" \
  || { echo "init-mcporter-oauth.sh: ${mcp_config} has no mcpServers entry for server '${mcp_server}'" >&2; exit 1; }

mcp_env_stem="${mcp_server}"
if [[ "${mcp_env_stem}" =~ ^(.+)-mcp(-[0-9]+)?$ ]]; then
  mcp_env_stem="${BASH_REMATCH[1]}"
fi
mcp_prefix="$(printf '%s' "${mcp_env_stem}" | tr '[:lower:]-' '[:upper:]_')_MCP_"
mcp_refresh_var="${mcp_prefix}REFRESH_TOKEN"
mcp_access_var="${mcp_prefix}ACCESS_TOKEN"
mcp_client_id_var="$(jq -r '.refresh.clientIdEnv // .oauthClientIdEnv // empty' <<<"${mcp_server_entry}")"
if [ -z "${mcp_client_id_var}" ]; then
  mcp_client_id_var="${mcp_prefix}CLIENT_ID"
fi
mcp_client_secret_var="$(jq -r '.refresh.clientSecretEnv // .oauthClientSecretEnv // .oauth_client_secret_env // empty' <<<"${mcp_server_entry}")"
mcp_token_endpoint_auth_method="$(jq -r '.refresh.clientAuthMethod // .oauthTokenEndpointAuthMethod // .oauth_token_endpoint_auth_method // empty' <<<"${mcp_server_entry}")"
mcp_expires_at_var="${mcp_prefix}EXPIRES_AT"
mcp_expires_in_var="${mcp_prefix}EXPIRES_IN"
mcp_refresh_expires_at_var="${mcp_prefix}REFRESH_TOKEN_EXPIRES_AT"

mcp_refresh="${!mcp_refresh_var:?${mcp_refresh_var} required}"
mcp_client_id="${!mcp_client_id_var:?${mcp_client_id_var} required}"
mcp_access="${!mcp_access_var:?${mcp_access_var} required}"
mcp_client_secret=""
if [ -n "${mcp_client_secret_var}" ]; then
  mcp_client_secret="${!mcp_client_secret_var:?${mcp_client_secret_var} required}"
fi
mcp_expires_at="${!mcp_expires_at_var:-}"
mcp_expires_in="${!mcp_expires_in_var:-}"
mcp_refresh_expires_at="${!mcp_refresh_expires_at_var:-}"

# Token values pass via env to keep them out of /proc/<pid>/cmdline.
# `mcporter vault set` resolves the vault key from MCPORTER_CONFIG's
# definition for ${mcp_server}, so the script doesn't reproduce the
# vaultKeyForDefinition hash itself.
export MCPORTER_CONFIG="${mcp_config}"
mcp_access="${mcp_access}" mcp_refresh="${mcp_refresh}" mcp_client_id="${mcp_client_id}" mcp_client_secret="${mcp_client_secret}" \
mcp_expires_at="${mcp_expires_at}" mcp_expires_in="${mcp_expires_in}" mcp_refresh_expires_at="${mcp_refresh_expires_at}" \
  jq -cn --arg token_endpoint_auth_method "${mcp_token_endpoint_auth_method}" '{
    tokens: (
      {access_token: env.mcp_access, refresh_token: env.mcp_refresh, token_type: "Bearer"}
      + (if env.mcp_expires_at != "" then {expires_at: env.mcp_expires_at} else {} end)
      + (if env.mcp_expires_in != "" then {expires_in: (env.mcp_expires_in | tonumber)} else {} end)
      + (if env.mcp_refresh_expires_at != "" then {refresh_token_expires_at: env.mcp_refresh_expires_at} else {} end)
    ),
    clientInfo: (
      {client_id: env.mcp_client_id}
      + (if env.mcp_client_secret != "" then {client_secret: env.mcp_client_secret} else {} end)
      + (if $token_endpoint_auth_method != "" then {token_endpoint_auth_method: $token_endpoint_auth_method} else {} end)
    )
  }' \
  | mcporter vault set "${mcp_server}" --stdin
