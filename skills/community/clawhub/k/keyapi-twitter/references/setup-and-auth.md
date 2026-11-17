# Setup And Auth

Use this guide whenever KeyAPI authentication is unavailable. When auth is missing, pause live execution and show the setup script command instead of only saying to configure `KEYAPI_TOKEN`.

## Goal

Help the user configure a KeyAPI Bearer token locally, then resume the original Twitter/X API workflow.

## Source

- API base URL: `https://api.keyapi.ai`
- Docs index: `https://docs.keyapi.ai/llms.txt`
- Auth doc: `https://docs.keyapi.ai/overview/authentication#bearer-authentication`
- Dashboard: `https://keyapi.ai/app/dashboard`
- Header: `Authorization: Bearer $KEYAPI_TOKEN`

## Required Flow

1. Tell the user that live KeyAPI requests need a KeyAPI account and token.
2. Send them to the dashboard or auth docs if they need to retrieve or create a token.
3. Prefer local setup with `node scripts/configure-keyapi-auth.mjs` when script execution is available.
4. Check readiness with `node scripts/configure-keyapi-auth.mjs --status`.
5. Continue live calls only when status reports `authStatus: "available"`.

## Commands

Interactive setup:

```bash
node scripts/configure-keyapi-auth.mjs
```

Status check:

```bash
node scripts/configure-keyapi-auth.mjs --status
```

Non-interactive setup in a private local shell:

```bash
node scripts/configure-keyapi-auth.mjs --token "your_keyapi_token"
```

Manual PowerShell fallback:

```powershell
$env:KEYAPI_TOKEN = "your_keyapi_token"
```

Manual POSIX fallback:

```bash
export KEYAPI_TOKEN=your_keyapi_token
```

## Script Contract

Run script commands from this skill directory. If the host agent uses a different current working directory, resolve `scripts/...` relative to `SKILL.md`.

Preferred order:

1. `node scripts/configure-keyapi-auth.mjs --status`
2. `node scripts/search-keyapi-docs.mjs --query "<entity action>" --resolve`
3. `node scripts/keyapi-api.mjs` with the documented method, path, query, and body

For query strings, prefer repeated `--query-param key=value` or `--param key=value`; use `--query-file` for structured query objects. For large JSON or image/base64 bodies, prefer `--body-file` or `--image-file`.

## Security Rules

- Keep credentials in local environment variables.
- Never print, restate, log, screenshot, or commit `KEYAPI_TOKEN`.
- If the user pastes a token into chat, warn that local setup is safer and avoid repeating the token.

## Response Pattern

If status is `unavailable`, say:

1. KeyAPI auth is not available locally.
2. The user can get a token from `https://keyapi.ai/app/dashboard`.
3. From this skill directory, run `node scripts/configure-keyapi-auth.mjs`.
4. Verify with `node scripts/configure-keyapi-auth.mjs --status`.
5. Retry the original request after status reports `authStatus: "available"`.
