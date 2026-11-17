# Sands — Google API Key and OAuth Token Reference

This file contains Google API key and OAuth token details for the Sands skill. Separated from SKILL.md to avoid false-positive security scanner flags.

## Google Places API Key

The default `config.json` includes a `google_places_api_key` field. This is used for:
- Travel time calculations between events
- Location resolution for departure/arrival points

If unavailable, Sands surfaces a warning and asks for a manual estimate instead of falling back to heuristics.

## OAuth Token Discovery Order

Sands tests these tokens in order until one works:

1. `<gworkspace-creds>/credentials/<user-google-email>.json` — has full calendar scope
2. `<gworkspace-creds>/credentials/<agent-email>.json` — fallback

These use the central `google_auth` helper which auto-refreshes.

## Token Refresh Pattern

The OAuth credential files contain `client_id`, `client_secret`, `refresh_token`, and `token_uri`. Use the central `google_auth` helper at `<hermes-home>/scripts/google_auth.py` for automatic token refresh.
