---
name: miro-management
description: Manage Miro through the Miro REST API using OAuth 2.0, saved token files, or direct access tokens. Use when the user wants to connect a personal or local Miro integration, complete OAuth authorization, refresh tokens, list boards, inspect board items or members, create or delete common board content such as sticky notes, text, shapes, cards, and connectors, manage webhooks, export board data, preview write payloads safely, or send raw REST API calls in a reusable local workflow.
---

# Miro Management

Use this skill to work with Miro through the REST API.

## Quick start

1. Get the user's Miro app client ID, client secret, and redirect URI if using OAuth.
2. Prefer a local redirect URI such as `http://127.0.0.1:4000/auth/miro/callback`.
3. Use `scripts/miro_api.py` for OAuth, token refresh, board/item operations, exports, and raw API calls.
4. Start with:
   - `auth-url`
   - `serve-oauth-callback`
   - `list-boards`
   - `list-board-items`
5. Never bundle client secrets, refresh tokens, or live access tokens into the skill package.

## Auth modes

### OAuth mode

Use shell environment variables when possible:

```powershell
$env:MIRO_CLIENT_ID = '...'
$env:MIRO_CLIENT_SECRET = '...'
$env:MIRO_REDIRECT_URI = 'http://127.0.0.1:4000/auth/miro/callback'
```

Start the callback helper:

```powershell
python scripts/miro_api.py serve-oauth-callback --port 4000 --token-file .miro/tokens.json
```

Then generate the authorization URL:

```powershell
python scripts/miro_api.py auth-url
```

Open that URL, approve the app, and let the callback helper store the token payload.

### Direct token mode

If the user already has a working Miro access token, skip OAuth and use either:

```powershell
$env:MIRO_ACCESS_TOKEN = '...'
python scripts/miro_api.py list-boards
```

or a saved token file:

```powershell
python scripts/miro_api.py list-boards --token-file .miro/tokens.json
```

## Core workflow

### 1. Confirm access

Use a cheap check first:

```powershell
python scripts/miro_api.py list-boards --token-file .miro/tokens.json
```

### 2. Inspect a board

```powershell
python scripts/miro_api.py get-board --board-id <id> --token-file .miro/tokens.json
python scripts/miro_api.py list-board-items --board-id <id> --token-file .miro/tokens.json
```

### 3. Create or export content

```powershell
python scripts/miro_api.py create-sticky-note --board-id <id> "Hello from OpenClaw" --token-file .miro/tokens.json
python scripts/miro_api.py create-text --board-id <id> "Roadmap" --token-file .miro/tokens.json
python scripts/miro_api.py create-shape --board-id <id> "API Layer" --token-file .miro/tokens.json
python scripts/miro_api.py create-card --board-id <id> "Task" --token-file .miro/tokens.json
python scripts/miro_api.py export-board-items --board-id <id> --format markdown --output-file board-report.md --token-file .miro/tokens.json
```

### 4. Refresh when needed

```powershell
python scripts/miro_api.py refresh-token --token-file .miro/tokens.json
```

## Common commands

- `auth-url` — print the OAuth authorization URL
- `serve-oauth-callback` — run a local callback server and exchange the returned code for tokens
- `exchange-code` — manually exchange a copied authorization code for tokens
- `refresh-token` — refresh access using the stored refresh token
- `whoami` — test token with a lightweight boards call
- `list-boards` — list accessible boards
- `get-board` — get board details
- `create-board` — create a board
- `list-board-items` — list board items
- `export-board-items` — export board items to markdown, csv, or json
- `create-sticky-note` — create a sticky note
- `create-text` — create a text item
- `create-shape` — create a shape item
- `create-card` / `update-card` — create or update a card item
- `create-sticky-note` / `update-sticky-note` — create or update sticky notes
- `create-text` / `update-text` — create or update text items
- `create-shape` / `update-shape` — create or update shapes
- `create-connector` — connect two board items
- `list-board-members` — list board members
- `get-webhooks` / `create-webhook` / `delete-webhook` — manage webhooks
- `create-brainstorm-cluster` — drop a row of idea sticky notes
- `create-kanban-row` — create a lightweight kanban-style row
- `create-architecture-chain` — create connected architecture boxes
- `delete-item` — delete an item by type path + item id
- `preview-write` — preview a write request without sending it
- `raw` — send an arbitrary Miro API request with optional JSON body

## Mutation rules

For write calls:

1. Confirm the target board and item IDs.
2. Summarize the exact body and endpoint before sending when the change is not obviously desired.
3. Keep secrets and tokens outside the skill folder.
4. Prefer exporting API results to files instead of dumping giant payloads in chat.
5. Treat live board writes as real external actions, not harmless local tests.

## References

Read `references/miro-oauth-notes.md` for the Miro OAuth flow, token endpoint, redirect URI rules, and safe local storage guidance.
Read `references/miro-request-examples.md` for starter create/export commands and raw request examples.
