#!/usr/bin/env bash
# init-mcporter.sh — vault seeder for HTTP+OAuth MCP servers.
#
# Reseeds ~/.mcporter/credentials.json when (a) the env-supplied refresh_token
# differs from the skill-owned provision marker, or (b) the vault entry is
# missing entirely. No-op when both match. The provisioner (whichever upstream
# system supplies the env tokens — typically via OpenClaw config.patch)
# triggers reseeds by rotating the env values; mcporter rotates OAuth tokens
# autonomously in-vault via the MCP SDK between reseeds.
#
# Usage: init-mcporter.sh <server-name> <config-path>
#
# Required env (prefix = uppercased server-name, hyphens → underscores, + "_MCP_"):
#   ${prefix}REFRESH_TOKEN  required
#   ${prefix}CLIENT_ID      required (DCR-issued)
#   ${prefix}ACCESS_TOKEN   required (the provisioner has both tokens at OAuth
#                                     completion; seeding the access token
#                                     skips mcporter's first-request 401→refresh)
#
# Vault key from steipete/mcporter src/oauth-vault.ts:
#   "${name}|${sha256({name, url, command:null}).slice(0,16)}"
#
# Variable naming: lowercase `mcp_*` for script-local state to avoid shadowing
# common shell variables (PATH, HOME, USER, etc.). Function-style locals would
# be ideal but the script body isn't in a function.

set -eu

mcp_server="${1:?server name required}"
mcp_config="${2:?config path required}"
mcp_skill_dir="$(dirname "${mcp_config}")"

mcp_url=$(jq -er --arg s "${mcp_server}" \
  '.mcpServers[$s].baseUrl // .mcpServers[$s].url' "${mcp_config}" 2>/dev/null) \
  || { echo "init-mcporter.sh: ${mcp_config} has no baseUrl/url for server '${mcp_server}' (or file missing)" >&2; exit 1; }

mcp_prefix="$(printf '%s' "${mcp_server}" | tr '[:lower:]-' '[:upper:]_')_MCP_"
mcp_refresh_var="${mcp_prefix}REFRESH_TOKEN"
mcp_access_var="${mcp_prefix}ACCESS_TOKEN"
mcp_client_id_var="${mcp_prefix}CLIENT_ID"

mcp_refresh="${!mcp_refresh_var:?${mcp_refresh_var} required}"
mcp_client_id="${!mcp_client_id_var:?${mcp_client_id_var} required}"
mcp_access="${!mcp_access_var:?${mcp_access_var} required}"

mcp_vault="${HOME}/.mcporter/credentials.json"
mcp_descriptor=$(jq -cn --arg n "${mcp_server}" --arg u "${mcp_url}" \
  '{name:$n, url:$u, command:null}')
mcp_hash=$(printf '%s' "${mcp_descriptor}" | shasum -a 256 | cut -c1-16)
mcp_key="${mcp_server}|${mcp_hash}"
# Wrapper-owned sidecar: stores a SHA-256 hash of the last env-supplied refresh
# token (NOT the token itself). We only need equality comparison to detect
# rotation, so a hash is sufficient — and a leaked .provisioned file then has
# no usable credential material. Compare against this hash, NOT against the
# live tokens.refresh_token in the vault — providers may rotate refresh tokens
# and the MCP SDK writes the rotated value back via saveTokens(), so the live
# token can drift away from what the provisioner supplied. Lives in the skill's
# own directory so it's co-located with the skill that owns it (cleaned up on
# uninstall) and outside mcporter's namespace.
mcp_provisioned_file="${mcp_skill_dir}/.provisioned"
mcp_refresh_hash=$(printf '%s' "${mcp_refresh}" | shasum -a 256 | cut -c1-64)

mkdir -p "$(dirname "${mcp_vault}")"

# Serialize concurrent writers: vault is shared across all skills, and two
# skills (or two parallel calls of the same skill) initializing in parallel
# would race the read-modify-write and tmp-file rename. flock on a sidecar
# lock file gates the entire critical section.
exec 200>>"${mcp_vault}.lock"
flock 200

[ -f "${mcp_vault}" ] || echo '{"version":1,"entries":{}}' > "${mcp_vault}"

mcp_provisioned_hash=$(cat "${mcp_provisioned_file}" 2>/dev/null || true)
# Skip reseed only if BOTH the marker hash matches AND the vault entry actually
# exists. Marker can survive while the vault gets reset (different files,
# different parent directories — a partial restore or break-glass vault wipe
# can leave one without the other). Without the vault check, we'd skip seeding
# and leave mcporter with no OAuth state, falling through to its interactive
# auth flow which fails headless.
if [ "${mcp_provisioned_hash}" = "${mcp_refresh_hash}" ] \
   && jq -e --arg k "${mcp_key}" '.entries[$k]' "${mcp_vault}" >/dev/null 2>&1; then
  exit 0
fi

# Atomic writes: tmp file beside the target so rename is guaranteed to stay on
# the same filesystem (atomic regardless of runtime mount layout). Interrupted
# runs may leave `${target}.tmp.<random>` next to the target until next cleanup
# pass / skill uninstall — visible and harmless.
#
# Token values pass to jq via env vars (read with `env.<name>`) instead of
# `--arg`, so they don't appear in /proc/<pid>/cmdline. Non-secret values
# (server name, URL, vault key, timestamp) still use `--arg` for clarity.
mcp_vault_tmp=$(mktemp "${mcp_vault}.tmp.XXXXXX")
mcp_access="${mcp_access}" mcp_refresh="${mcp_refresh}" mcp_client_id="${mcp_client_id}" \
jq --arg k "${mcp_key}" --arg n "${mcp_server}" --arg u "${mcp_url}" \
   --arg ts "$(date -u +%FT%TZ)" \
   '.entries[$k] = {
      serverName: $n,
      serverUrl:  $u,
      tokens:     {access_token: env.mcp_access, refresh_token: env.mcp_refresh, token_type: "Bearer"},
      clientInfo: {client_id: env.mcp_client_id},
      updatedAt:  $ts
    }' \
   "${mcp_vault}" > "${mcp_vault_tmp}"
mv "${mcp_vault_tmp}" "${mcp_vault}"

mcp_provisioned_tmp=$(mktemp "${mcp_provisioned_file}.tmp.XXXXXX")
printf '%s' "${mcp_refresh_hash}" > "${mcp_provisioned_tmp}"
mv "${mcp_provisioned_tmp}" "${mcp_provisioned_file}"