# Mermail MCP platform configuration

Read this reference when selecting an authentication mode, tool profile, or exact client configuration. The hosted Streamable HTTP endpoint is `https://console.mermail.app/mcp`.

## Authentication and profile selection

| Need | Endpoint | Authentication | Capability boundary |
| --- | --- | --- | --- |
| Normal external Mermail work | `/mcp` | Prefer OAuth; API key fallback | Full base catalog |
| Least-privilege verification inbox | `/mcp?profile=agent-inbox` | OAuth or API key | Exact 12-tool mailbox-provisioning and safe-email-read set |
| Live PayBox financial tools | `/mcp` | Full-profile OAuth as a current workspace member | Model-visible live `paybox_*` and safe invocation status through the owner's active PayBox connection |
| PayBox connection management / legacy Agent Wallet | `/mcp` | Full-profile OAuth as workspace owner | Connect/reauth handoffs and owner-only legacy compatibility tools |

OAuth uses the same Enoki account as the Mermail console and binds the grant to the workspace selected during browser consent. Core scope is `mcp:tools`; `openid` and `offline_access` may accompany it. Legacy `wallet:read` and `wallet:transact` labels are compatibility-only and do not unlock tools.

API-key mode uses a workspace-scoped Mermail API key mapped from `MERMAIL_API_KEY` to the `x-api-key` header. API-key mode cannot unlock Agent Wallet or `paybox_*` tools.

## Codex

Prefer native MCP OAuth with a current Codex CLI:

```bash
codex mcp add mermail --url https://console.mermail.app/mcp
codex mcp login mermail
codex mcp list
```

Start a new Codex session and inspect `/mcp`. Installable skills do not replace
this OAuth connection. API-key config is a limited fallback for core mail and
workspace automation only; it cannot use PayBox or x402:

```json
{
  "type": "http",
  "url": "https://console.mermail.app/mcp",
  "env_http_headers": {
    "x-api-key": "MERMAIL_API_KEY"
  }
}
```

Set `MERMAIL_API_KEY` in the environment that launches Codex, restart the client, then inspect `/mcp`. Do not place a key in chat or an official Directory App configuration.

## Claude and Claude Code

When Claude exposes custom connectors in the workspace, add the hosted URL in
**Settings → Connectors**, complete OAuth, enable Mermail in the conversation,
then verify `list_mailboxes`. If connector creation is unavailable, ask the
workspace owner to enable it.

For Claude Code, prefer OAuth at user scope:

```bash
claude mcp add --transport http --scope user mermail https://console.mermail.app/mcp
```

Open `/mcp`, choose **Authenticate**, and verify the catalog. For a limited
Claude Code API-key fallback:

```json
{
  "type": "http",
  "url": "https://console.mermail.app/mcp",
  "headers": {
    "x-api-key": "${MERMAIL_API_KEY:-}"
  }
}
```

Keep the `:-` empty default. Without it, an unset variable is sent as the
literal `${MERMAIL_API_KEY}` header, which Mermail rejects before OAuth is tried.

Use `/mcp` or `claude mcp get mermail` to inspect connection state. Start a new
session after skill or connector updates.

Claude commonly exposes host-qualified identifiers such as `Mermail:list_mailboxes` and `Mermail:list_emails`; another host may expose a different namespace or bare names. Never manually add, strip, or invent the qualifier. The protocol `tools/list` names remain bare `list_mailboxes` and `list_emails`.

## Cursor

Prefer OAuth: add `https://console.mermail.app/mcp` or use the Cursor deeplink from [mermail.app/agents](https://mermail.app/agents), then select Authenticate.

If OAuth is unavailable, use:

```json
{
  "type": "http",
  "url": "https://console.mermail.app/mcp",
  "headers": {
    "x-api-key": "${env:MERMAIL_API_KEY}"
  }
}
```

Open MCP settings to inspect the server after restarting Cursor. An already-running desktop process does not receive an environment variable exported later in an unrelated shell.

## ChatGPT

When ChatGPT exposes custom apps in the workspace, enable developer controls,
open **Settings → Apps → Create**, paste the hosted Mermail URL, choose OAuth,
scan tools, finish workspace consent, then enable Mermail in a new chat. If
**Create** is unavailable, ask the workspace owner to enable custom apps. Do
not add `x-api-key` headers to this path.

## OpenClaw

Prefer native OAuth:

```bash
openclaw mcp add mermail --url https://console.mermail.app/mcp --transport streamable-http --auth oauth
openclaw mcp login mermail
openclaw mcp doctor mermail --probe
```

Do not classify proof creation or an unauthenticated catalog response as a
healthy connection; the doctor probe must connect and list capabilities.

## Hermes Agent

Merge this entry under the existing `mcp_servers` key in
`~/.hermes/config.yaml`, then authenticate from a fresh terminal:

```yaml
mcp_servers:
  mermail:
    url: "https://console.mermail.app/mcp"
    auth: oauth
```

```bash
hermes mcp login mermail
```

For a remote/headless Hermes host, keep OAuth: open the printed authorization
URL locally and paste the final redirect URL back into the login prompt. Do not
downgrade a PayBox or x402 workflow to API-key auth.

## Generic headless clients

Use the client's secret store, process supervisor, CI secret injection, or another non-recording credential input to provide `MERMAIL_API_KEY` to the launching process. Do not type a real key in an interactive `export` command that may remain in shell history. For generic MCP configuration, preserve the same Streamable HTTP URL and `x-api-key` mapping; do not place the actual key in examples, logs, command arguments, or tracked files.

## Mailbox identifiers

For mailbox-scoped tools, prefer `public_id` from `list_mailboxes` as `mailboxId`. A hosted alias id or current email may also resolve, but never infer a mailbox from display name or mix identifiers across workspaces.
