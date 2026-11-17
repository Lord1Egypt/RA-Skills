#!/usr/bin/env bash
# Read env-supplied OAuth credentials, write to gogcli's local stores.
# - Client creds (id+secret) → $XDG_CONFIG_HOME/gogcli/credentials-$MAVERICK_GOG_CLIENT.json (plaintext, 0600)
# - Refresh token → $XDG_CONFIG_HOME/gogcli/keyring/ (file backend, jose2go-encrypted
#   under GOG_KEYRING_PASSWORD), keyed by (client=$MAVERICK_GOG_CLIENT, email=$MAVERICK_GOG_EMAIL)
#
# MAVERICK_GOG_CLIENT is the client name of the persisted state, not of the
# gateway generation: the orchestrator keeps it across every gateway the state
# outlives, so credentials seeded here stay addressable after a restore. It
# arrives with the setup call itself, never from the container's boot env, so a
# container started before the name existed still seeds under it.
#
# Security boundary: GOG_KEYRING_PASSWORD encrypts the refresh-token keyring
# only. The client-creds file lands plaintext on disk, protected by the
# container filesystem and the R2 access boundary alone, until gogcli encrypts
# it upstream.
#
# GOG_KEYRING_BACKEND is pinned to `file` as an image-level constant in
# infra/openclaw/image/Dockerfile, so a future base image that introduces dbus
# cannot make gogcli's `auto` resolution attempt SecretService and pay its 10s
# cold-call timeout.
#
# Setup-runtime prerequisites: bash, jq, gog (≥ v0.17.0). Only `gog` is declared
# in SKILL.md `requires.bins` — the field gates agent-runtime eligibility, and
# `gog` is the only one needed there; `bash` and `jq` are setup-time-only.
# Matches the mcporter-skill-builder convention.
#
# Re-run policy: fire skills.setup only when MAVERICK_GOG_REFRESH_TOKEN is a NEW
# refresh_token value from a just-completed user-side authorization callback —
# not merely "callback succeeded". Google omits refresh_token from refresh-flow
# responses and may omit it from authorization-code responses for
# previously-consented users, and re-firing with a stale token clobbers a
# refresh that gogcli rotated in-keyring, breaking the integration until
# re-authorization. Mirrors mcporter init-mcporter-oauth.sh § Re-run policy.

set -eu

: "${MAVERICK_GOG_CLIENT:?MAVERICK_GOG_CLIENT required (the orchestrator passes it with every setup)}"
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
  | gog auth credentials set - --client="${MAVERICK_GOG_CLIENT}" --no-input --force

# Its own stdin, as the jq call above has: it reads none, and an inherited one
# could hold a real gog waiting on a caller's open pipe.
gog auth import \
  --client="${MAVERICK_GOG_CLIENT}" \
  --email="${MAVERICK_GOG_EMAIL}" \
  --refresh-token-env=MAVERICK_GOG_REFRESH_TOKEN \
  --force \
  --no-input < /dev/null
