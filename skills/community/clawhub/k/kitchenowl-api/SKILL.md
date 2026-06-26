---
name: kitchenowl-api
description: Interact with KitchenOwl APIs (login, token handling, REST/GraphQL calls, and shopping-list read/update) through a reusable CLI script. Use when the user asks to read or modify shopping-list items on self-hosted or cloud KitchenOwl instances.
---

# KitchenOwl API

Use `scripts/kitchenowl-api.sh` for KitchenOwl operations without relying on the web UI.

## Prerequisites

- `curl`
- `jq`

## Quick configuration

Supported environment variables:

- `KITCHENOWL_URL` (e.g. `https://kitchenowl.example.com`) **[preferred]**
- `KITCHENOWL_TOKEN` (Bearer token; access token or long-lived token)
- `KITCHENOWL_REFRESH_TOKEN` (optional)
- `KITCHENOWL_BASE_URL` (legacy compatibility)

## Main commands

```bash
# 1) Probe useful API endpoints
{baseDir}/scripts/kitchenowl-api.sh probe --base-url https://kitchenowl.example.com

# 2) Login (saves tokens in ~/.config/kitchenowl-api/session.json)
{baseDir}/scripts/kitchenowl-api.sh login \
  --base-url https://kitchenowl.example.com \
  --username USERNAME \
  --password 'PASSWORD' \
  --device openclaw

# 3) Generic authenticated REST call
{baseDir}/scripts/kitchenowl-api.sh request GET /api/user

# 4) REST call with JSON body
{baseDir}/scripts/kitchenowl-api.sh request POST /api/auth/llt \
  --json '{"device":"openclaw-llt"}'

# 5) GraphQL query (if available on the instance)
{baseDir}/scripts/kitchenowl-api.sh graphql \
  --query '{ __typename }'
```

## Recommended flow for shopping-list tasks

1. Run `probe`.
2. Run `login` (if no valid token is available).
3. Use `request` against shopping-list endpoints of the target instance.
4. If endpoint paths are unknown, start from `request GET /api` and/or check instance docs.

## Operational notes

- Some instances use reverse proxies with broken redirects (example: `/api -> http://localhost/api/`).
- In that case, force the correct `--base-url` or fix proxy settings server-side.
- The script does not print plain-text passwords.
- Tokens are stored locally only in `~/.config/kitchenowl-api/session.json`.
