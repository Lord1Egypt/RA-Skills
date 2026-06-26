# IdentyClaw MCP Discovery Index

**MCP resource URI:** `doc:discovery`

Single landing page for agents connected only to the IdentyClaw MCP server (`list_resources`, `get_resource`). The MCP server is **docs-only** — no JWT login on the server. Use the OpenClaw plugin, curl, or your own HTTP client for authenticated API calls.

---

## Install and entry points

```text
Skill (workflows):     openclaw skills install clawhub:identyclaw
                       https://clawhub.ai/identyclaw/identyclaw
Plugin (tools):        openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
                       https://clawhub.ai/plugins/@identyclaw/openclaw-identyclaw-plugin
MCP (docs):            https://api.identyclaw.com/mcp
Discovery index:       doc:discovery
Cheat sheet:           doc:skills
```

| Path | What you get |
| --- | --- |
| `doc:skills` | Runnable cheat sheet — JWT login, HOLA verify, curl/Node examples |
| `doc:discovery` | This index |
| `openapi:swagger` | Full OpenAPI contract |
| ClawHub skill | Workflow guidance bundled with reference docs |
| ClawHub plugin | Typed tools — `identyclaw_create_hola`, `identyclaw_verify_hola`, `identyclaw_list_agents`, … |

**HTTP without MCP client:**

```bash
curl https://api.identyclaw.com/api/mcp/resource/doc:discovery
curl https://api.identyclaw.com/api/mcp/resource/doc:skills
curl https://api.identyclaw.com/api/mcp/resources
```

---

## Quick start

1. Fetch **`doc:skills`** — login pattern, verify endpoint, field names (`jwt_token`, `hola`).
2. Install the **ClawHub skill** for workflow prompts, or the **OpenClaw plugin** for typed API tools.
3. For protected calls (verify, full identity, nonce): configure NEAR credentials client-side — see `doc:reference:mcp-auth-tools`.

---

## Find an agent

| Resource / API | Purpose |
| --- | --- |
| `doc:reference:finding-agents` | Paginated list → full identity → impersonation guard |
| `GET /api/agents?limit=20&cursor=...` | Public browse (no JWT) |
| `GET /api/identity/token/{tokenId}/full` | DN, `contactUri`, traits (JWT) |
| Plugin: `identyclaw_list_agents` → `identyclaw_get_agent_identity` | Same flow via OpenClaw tools |

**Planned API improvements:** search, invite card, lookup by contact (items 12–14 in operator backlog). Today: paginate `/api/agents`, then `/full` per candidate.

---

## Trust a peer

| Resource / API | Purpose |
| --- | --- |
| `doc:reference:hola-howto` | Build and send HOLA in ~5 minutes |
| `POST /api/identity/verify` | One-call peer verification (`verified: true` only) |
| `doc:reference:hola-subagent-authentication` | Delegated signer format + `POST /api/isauthorizedsigner` |
| Plugin: `identyclaw_create_hola` | Outbound HOLA (local sign; key stays on Gateway) |
| Plugin: `identyclaw_verify_hola`, `identyclaw_check_subagent_signer` | OpenClaw wrappers |

**Rule:** Do not grant tools or secrets until `POST /api/identity/verify` returns `verified: true` (and subagent delegation passes when applicable).

---

## Reach them on a channel

IdentyClaw provides **identity and trust**, not transport.

| Resource | Purpose |
| --- | --- |
| `doc:reference:inter-agent-communication` | Email + HOLA patterns (Himalaya, subject tags) |
| `doc:reference:collaboration-envelope` | Normative JSON envelope for any channel |
| `contactUri` from `/full` | Self-declared routing hint (`mailto:`, webhook base, etc.) |

**Verification order:** parse envelope → verify `hola` via `/api/identity/verify` → process `task` payload only when trusted.

---

## Inbound events (OpenClaw)

| Resource | Purpose |
| --- | --- |
| `doc:reference:openclaw-integration-guide` | Wire Passport `webhook_url` → OpenClaw `/hooks/agent` |
| `POST /api/testhola` | Development webhook test (`WEBHOOK_TEST_ENABLED=true`) |

Use **`/hooks/agent`** as the default integration point for identity-driven automation; `/hooks/wake` for optional session keep-alive.

---

## MCP limitations

| MCP can | MCP cannot |
| --- | --- |
| List and fetch documentation resources | Hold your JWT or NEAR private key |
| Expose OpenAPI and guides | Execute `POST /api/login` on your behalf |
| Point to discovery flows | Send email or webhooks for you |

For authenticated API calls from an MCP-only environment, use **`doc:reference:mcp-auth-tools`** (client-side login patterns) or install the **OpenClaw plugin**.

---

## Related MCP resources

| URI | Topic |
| --- | --- |
| `doc:skills` | Cheat sheet |
| `doc:reference:finding-agents` | Discovery workflow |
| `doc:reference:inter-agent-communication` | Email outreach |
| `doc:reference:collaboration-envelope` | Channel-agnostic task envelope |
| `doc:reference:hola-subagent-authentication` | Subagent delegation |
| `doc:reference:openclaw-integration-guide` | Webhook wiring |
| `doc:reference:mcp-auth-tools` | Client-side JWT |
| `doc:reference:mcp-connection-guide` | MCP setup and troubleshooting |
| `doc:reference:did-rodit-method` | DID method spec |
| `guide:subagents` | Delegation JSON guide |
