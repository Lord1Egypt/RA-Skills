#!/usr/bin/env bash
# Read env-supplied OAuth credentials, write to gogcli's local stores.
# - Client creds (id+secret) → $XDG_CONFIG_HOME/gogcli/credentials-$APP_NAME.json (plaintext, 0600)
# - Refresh token → $XDG_CONFIG_HOME/gogcli/keyring/ (file backend, jose2go-encrypted
#   under GOG_KEYRING_PASSWORD), keyed by (client=$APP_NAME, email=$MAVERICK_GOG_EMAIL)
#
# MVP security boundary: GOG_KEYRING_PASSWORD encrypts the refresh-token keyring
# only. The client-creds file lands plaintext on disk and is protected solely by
# the container filesystem and R2 access boundary, not by GOG_KEYRING_PASSWORD —
# until gogcli upstream issue GOG1 ships. See the plan's "MVP security boundary"
# section for the full trust model.
#
# Backend posture: GOG_KEYRING_BACKEND is pinned to `file` as an image-level
# constant in the deployed container's Dockerfile (cloudflare/Dockerfile in
# maverick_openclaw). Explicit pinning insulates against future base-image
# variants that might introduce dbus and cause gogcli's `auto` resolution to
# attempt SecretService with a 10s cold-call timeout. See the plan's
# `GOG_KEYRING_BACKEND` section.
#
# Setup-runtime prerequisites: bash, jq, gog (≥ v0.17.0). Of these, only `gog`
# is declared in SKILL.md `requires.bins` (the field gates agent-runtime
# eligibility, and `gog` is needed at both setup AND agent runtime). `bash` and
# `jq` are setup-time-only and intentionally NOT in `requires.bins` — they
# belong to the setup runtime contract, not the agent-runtime eligibility gate.
# Matches the mcporter-skill-builder convention (see
# `skills/mcporter-skill-builder/scripts/templates/setup.sh` header).
#
# Re-run policy: caller must only fire skills.setup when MAVERICK_GOG_REFRESH_TOKEN
# is a fresh refresh_token from a just-completed user-side authorization callback
# — specifically, the OAuth callback yielded a new refresh_token value (not just
# "callback succeeded"). Google omits refresh_token from refresh-flow responses
# and may omit it from authorization-code responses for previously-consented
# users; those callbacks must NOT fire skills.setup. Re-firing with a stale
# token clobbers a refresh that gogcli rotated in-keyring, breaking the
# integration until re-authorization. Mirrors mcporter init-mcporter-oauth.sh
# § Re-run policy.

set -eu

: "${APP_NAME:?APP_NAME required from container env}"
: "${MAVERICK_GOG_CLIENT_ID:?MAVERICK_GOG_CLIENT_ID required}"
: "${MAVERICK_GOG_CLIENT_SECRET:?MAVERICK_GOG_CLIENT_SECRET required}"
: "${MAVERICK_GOG_EMAIL:?MAVERICK_GOG_EMAIL required}"
: "${MAVERICK_GOG_REFRESH_TOKEN:?MAVERICK_GOG_REFRESH_TOKEN required}"

# Tokens via env (not argv) to keep them out of /proc/<pid>/cmdline.
# Envelope shape is required by gogcli's parser (ParseGoogleOAuthClientJSON
# accepts {installed:{...}} or {web:{...}} only); only client_id +
# client_secret are extracted — other Google client_secret.json fields are
# accepted but ignored. On disk gogcli stores the flat {client_id,
# client_secret} pair regardless of input envelope. We use {web:{...}} to
# match the typical Google Cloud "Web application" OAuth client type used
# for server-side authorization-code flows; consumers using "Desktop /
# installed application" clients can swap to {installed:{...}} — gogcli's
# behavior is identical post-parse.
MAVERICK_GOG_CLIENT_ID="${MAVERICK_GOG_CLIENT_ID}" \
MAVERICK_GOG_CLIENT_SECRET="${MAVERICK_GOG_CLIENT_SECRET}" \
  jq -cn '{
    web: {
      client_id:     env.MAVERICK_GOG_CLIENT_ID,
      client_secret: env.MAVERICK_GOG_CLIENT_SECRET
    }
  }' \
  | gog auth credentials set - --client="${APP_NAME}" --no-input --force

gog auth import \
  --client="${APP_NAME}" \
  --email="${MAVERICK_GOG_EMAIL}" \
  --refresh-token-env=MAVERICK_GOG_REFRESH_TOKEN \
  --force \
  --no-input
