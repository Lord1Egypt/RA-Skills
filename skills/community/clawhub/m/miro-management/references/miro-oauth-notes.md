# Miro OAuth notes

## Core endpoints

- Authorization URL base: `https://miro.com/oauth/authorize`
- Token endpoint: `https://api.miro.com/v1/oauth/token`
- REST API base: `https://api.miro.com/v2`

## Required auth parameters

For authorization URL:

- `response_type=code`
- `client_id`
- `redirect_uri`

For exchanging an authorization code:

- `grant_type=authorization_code`
- `client_id`
- `client_secret`
- `code`
- `redirect_uri`

For refreshing:

- `grant_type=refresh_token`
- `client_id`
- `client_secret`
- `refresh_token`

## Important redirect rule

The `redirect_uri` used during the OAuth request must match the app settings exactly.

Recommended local setup:

- App URL: `http://127.0.0.1:4000`
- Redirect URI: `http://127.0.0.1:4000/auth/miro/callback`

## Token behavior

Miro docs say:

- access token valid for about 60 minutes
- refresh token valid for about 60 days
- refresh returns a new access token and new refresh token

## Safe storage

Do not store real client secrets or live tokens inside the skill folder.

Prefer:

- environment variables for client ID / client secret / redirect URI
- a local token file outside the skill package, such as `.miro/tokens.json`

## Good first API checks

- `GET /boards`
- `GET /boards/{board_id}`
- `GET /boards/{board_id}/items`
