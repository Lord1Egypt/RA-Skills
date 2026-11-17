# Mermail CLI command contract

Read this reference when installing the CLI, choosing authentication, constructing commands, checking supported operations, or formatting output.

## Setup and discovery

1. Require Node.js 22 or newer.
2. Install the official public package with `npm install -g mermail-cli`, or run once with `npx --yes mermail-cli`. Do not use a GitHub-source install in user-facing setup instructions.
3. Configure `MERMAIL_API_KEY` in the environment for Sold API commands. Never request or echo the full key. Prefer the environment over `--api-key` because shell history and process listings may expose arguments.
4. Run `mermail doctor`. Run `mermail auth check` only when the user accepts that it consumes one read credit.
5. Inspect `mermail --help` and `mermail <resource> --help` after upgrades. The live CLI help is authoritative for flags.

For staging-only tests, set `MERMAIL_BASE_URL=https://console-staging.mermail.app`. Never silently redirect production work to staging or the reverse.

## Authentication boundaries

- Sold API mail and workspace commands use `MERMAIL_API_KEY`; the CLI does not store API keys.
- Agent Wallet uses browser-based MCP OAuth through `mermail auth login` and stores its session locally with restricted permissions.
- The core OAuth scopes are `mcp:tools`, `openid`, and `offline_access`. Legacy `wallet:read` and `wallet:transact` labels are compatibility-only and are not required for Agent Wallet visibility.
- The CLI's current `wallet` commands call owner-only legacy Agent Wallet tools, so they require the authenticated workspace owner and a connected PayBox account. API keys never unlock Agent Wallet. Current workspace members can use live model-visible `paybox_*` through the owner's active connection only via a full-profile MCP client; the CLI does not expose direct transfer/swap/x402 commands.
- `mermail auth login` requires an interactive terminal. Do not attempt a new wallet login in headless CI.

## Command shape

Use `mermail <resource> <action> [flags]`:

```bash
mermail workspaces list --format json
mermail mailboxes list --format json
mermail emails list --mailbox-id MAILBOX_PUBLIC_ID
mermail emails context \
  --mailbox-id MAILBOX_PUBLIC_ID \
  --email-id EMAIL_ID \
  --limit 20
mermail emails send \
  --mailbox-id MAILBOX_PUBLIC_ID \
  --to recipient@example.com \
  --from you@mermail.app \
  --subject "Hello" \
  --text "Plain text body"
mermail mcp check
mermail mcp check --profile agent-inbox
```

`--mailbox-id` accepts the mailbox `public_id`, hosted alias ID, or current email. Prefer `public_id` returned by `mermail mailboxes list`.

Send, reply, and forward use `--text` and/or `--html` plus `--from`; there is no generic free-form message `--body` flag for those commands. Draft and scheduled-send commands use the string field `body`.

Use typed flags for ordinary fields. For complete or nested bodies, use `--data`, `--data-file PATH`, or `--data-file -` with stdin. Prefer a file or stdin over large inline JSON.

## Supported and retired operations

- The current operation manifest exposes 70 supported Sold API commands.
- `mermail emails context` maps to `get_email_context` and accepts `--mailbox-id`, `--email-id`, `--limit`, `--cursor`, and `--include-held`.
- Workspace deletion is disabled. Do not call or invent `mermail workspaces delete`.
- Default task-triager selection is outside the supported workflow. Do not call or invent `mermail triagers set-default` even if a full MCP catalog exposes a compatibility tool.
- `mermail wallet sign-url` is retired. Signing links are invocation-scoped values returned by Mermail, not locally constructed mailbox URLs.
- The CLI has no substitute for live `paybox_request_swap` or `paybox_pay_x402`.

## Agent Inbox profile

`mermail mcp check --profile agent-inbox` requires exactly these 12 tools:

1. `get_api_credit_usage`
2. `list_workspaces`
3. `get_workspace`
4. `list_email_domains`
5. `list_workspace_mailboxes`
6. `list_mailboxes`
7. `create_mailbox`
8. `get_mailbox`
9. `list_emails`
10. `search_emails`
11. `get_email`
12. `get_email_context`

Keep the full MCP endpoint for sending and the broader catalog. Do not silently replace an existing full connection with the focused profile.

## Output and errors

- Default to `--format json` for automation. `yaml`, `table`, and `raw` are available; `explore` is only for a human-operated terminal.
- Filter JSON deterministically with JMESPath, for example `mermail mailboxes list --transform '[].email'`.
- A JMESPath result of `null` is a valid empty selection, not an API failure.
- Exit `2`: invalid command or payload.
- Exit `3`: missing, invalid, expired, or revoked authentication.
- Exit `4`: a destructive command needs confirmation.
- Exit `5`: `emails wait` timed out without a matching message.
- HTTP `402`: credits exhausted; do not retry.
- HTTP `400` `email_send_recipient_limit_exceeded`: a Free external send has more than 10 total To+Cc+Bcc recipients; do not split or silently alter it.
- HTTP `429`: respect `retryAfterMs`. For `email_send_rate_limit_exceeded`, do not auto-retry a send/reply/forward/schedule command; Free limits are 10 recipient units/minute, 50/hour, and 200/day.
- HTTP `503` `email_send_rate_limit_unavailable`: external sending fails closed; do not switch surfaces or claim success.
