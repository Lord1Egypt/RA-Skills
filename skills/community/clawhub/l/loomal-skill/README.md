# loomal-skill

Loomal skill for [OpenClaw](https://openclaw.ai) and other AgentSkills-compatible clients (picoclaw, nanoclaw, …).

Gives your agent its own:

- **Email** at `agent-xxx@mailgent.dev` — send, receive, reply with correct threading
- **Encrypted vault** for logins, API keys, OAuth tokens, certs, cards (AES-256-GCM at rest)
- **2FA** — attach TOTP to any credential, fetch live codes without ever exposing the seed
- **Calendar** — read, create, update events; expose a public iCal URL
- **Payments** — accept USDC on Base via x402 (HTTP 402 + buyer-signed `X-Payment` header)
- **DID identity** — sign and verify with the agent's Ed25519 key

All tools are scope-gated by the API key. The trust boundary is enforced on the API side, so a compromised agent only sees what its key was scoped for.

## Install

### One command (recommended)

```bash
clawhub install loomal-skill
```

This drops the skill into your workspace's `skills/` directory.

### Register the MCP server

The skill teaches the agent *when* to use Loomal. The MCP server provides the actual tools. Register it once per machine — the npm package version is pinned for supply-chain safety:

```bash
openclaw mcp set loomal '{"command":"npx","args":["-y","@loomal/mcp@0.5.0"],"env":{"LOOMAL_API_KEY":"loid-..."}}'
```

Get a `loid-...` key at [console.loomal.ai](https://console.loomal.ai). Scopes attached to the key control which tools appear. Bump `@loomal/mcp@0.5.0` to a newer version intentionally when you want a release; check [npm](https://www.npmjs.com/package/@loomal/mcp) for the latest.

### Manual install

If your client doesn't have the `clawhub` CLI, copy this `loomal-skill/` folder into the client's skills directory and run the `mcp set` command above (the verb may differ per client — `picoclaw mcp add`, etc. — but the JSON payload is the same).

## Verify

Ask your agent:

> Who am I?

It should call `identity_whoami` and return your agent's email (`agent-xxx@mailgent.dev`), DID, and the scopes attached to your key.

## What you can ask

The headline chain — signup → 2FA → paid API call:

```
> Sign me up for serviceX.com using my agent email,
  store the login + 2FA in the vault, and call their
  paid /search API for $0.05.
```

The agent will:

1. `identity_whoami` → get `agent-xxx@mailgent.dev`
2. Fill the signup form with that address + a generated password
3. `mail_list_messages` until the welcome email lands, `mail_get_message` to read the verification link
4. `vault_store` the credential (`type: "LOGIN"`) with a TOTP attached
5. `vault_totp` for the live 6-digit 2FA code at login time
6. On the 402 response, sign + send `X-Payment` and call `payments_redeem`

Other common asks:

```
> Check my inbox for unread emails
> Reply to the latest email from Sarah
> Store my Stripe API key in the vault
> Get my AWS 2FA code
> Schedule a meeting with the team for Tuesday at 2pm
> Make my calendar public
```

## Tool surface

| Namespace | Tools |
|---|---|
| `identity_*` | `whoami`, `sign`, `verify` |
| `mail_*` | `send`, `reply`, `list_messages`, `get_message`, `get_attachment`, `list_threads`, `get_thread`, `update_labels`, `update_thread_labels`, `delete_message`, `delete_thread` |
| `vault_*` | `list`, `get`, `store`, `delete`, `totp`, `totp_use_backup` |
| `calendar_*` | `list`, `get`, `create`, `update`, `delete`, `set_public` |
| `payments_*` | `challenge`, `redeem`, `list`, `sellers_endpoints_*` |

Tools only appear if your identity has the required scopes (`mail:send`, `vault:write`, `payments:accept`, etc.). Add scopes at [console.loomal.ai](https://console.loomal.ai).

## Multiple inboxes

Register one MCP server per identity:

```bash
openclaw mcp set loomal-sales '{"command":"npx","args":["-y","@loomal/mcp@0.5.0"],"env":{"LOOMAL_API_KEY":"loid-sales-key"}}'
openclaw mcp set loomal-support '{"command":"npx","args":["-y","@loomal/mcp@0.5.0"],"env":{"LOOMAL_API_KEY":"loid-support-key"}}'
```

Tools namespace per server (`loomal-sales:mail_send` vs `loomal-support:mail_send`).

## Compatibility

Built against the [ClawHub skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md). Should install cleanly on any AgentSkills-compatible client.

| Client | Status |
|---|---|
| OpenClaw | Tested via `clawhub install` + `openclaw mcp set` |
| picoclaw | AgentSkills spec-compatible (untested — please report) |
| nanoclaw | AgentSkills spec-compatible (untested — please report) |
| Other claw-family forks | If they follow AgentSkills, the same skill should work |

If you're running another claw-family client and the install works (or doesn't), please open an issue.

## Security note

OpenClaw — like any agent that runs locally with broad system access — has had high-severity CVEs. Loomal's defense in depth is **scope-gated API keys**: a compromised agent can only do what its `loid-...` key was scoped for. Keep keys per-task (not org-wide), revoke at the first sign of trouble, and prefer narrower scopes.

## Links

- Loomal: <https://loomal.ai>
- Docs: <https://docs.loomal.ai/integrations/openclaw>
- Console (get an API key): <https://console.loomal.ai>
- MCP package on npm: <https://www.npmjs.com/package/@loomal/mcp>
- ClawHub: <https://clawhub.ai>

## License

MIT-0 (per [ClawHub registry policy](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#license)).
