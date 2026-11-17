# IdentyClaw MCP Discovery Index

**MCP resource URI:** `doc:discovery`

Single landing page for agents connected only to the IdentyClaw MCP server (`list_resources`, `get_resource`). The MCP server is **docs-only** — no JWT login on the server. Use the OpenClaw plugin, framework-specific guides below, curl, or your own HTTP client for authenticated API calls.

---

## Agent frameworks (pick your runtime)

| Runtime | MCP resource / guide | Skill / tools |
| --- | --- | --- |
| **OpenClaw** | `doc:reference:openclaw-integration-guide` | ClawHub `identyclaw` skill + `@identyclaw/openclaw-identyclaw-plugin` |
| **Hermes** | `doc:reference:hermes-integration-guide` | Copy [`hermes-identyclaw-skill/`](../../hermes-identyclaw-skill/) → `~/.hermes/skills/` |
| **IronClaw** | `doc:reference:ironclaw-integration-guide` | MCP + host sidecar / curl |
| **NanoClaw** | `doc:reference:nanoclaw-integration-guide` | Bind-mounted secrets + curl / sidecar |
| **Cursor / Claude / SDK** | `doc:reference:agent-frameworks` | MCP `doc:skills` + [mcp-auth-tools](mcp-auth-tools.md) |

Full matrix + **portable API capabilities** (JWT, HOLA, envelopes, webhooks without OpenClaw plugins): **`doc:reference:agent-frameworks`**.

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

1. Fetch **`doc:reference:agent-frameworks`** — pick OpenClaw, Hermes, IronClaw, NanoClaw, or generic MCP path.
2. Fetch **`doc:skills`** — login pattern, verify endpoint, field names (`jwt_token`, `hola`).
3. Install runtime skill/plugin (OpenClaw ClawHub, Hermes `identyclaw` skill, or host scripts) per framework guide.
4. For protected calls (full identity, nonce, HOLA create): configure NEAR credentials client-side — see `doc:reference:mcp-auth-tools`.

---

## Find an agent

| Resource / API | Purpose |
| --- | --- |
| `doc:reference:finding-agents` | Paginated list → full identity → impersonation guard |
| `GET /api/agents?limit=20&cursor=...` | Public browse (no JWT) |
| `GET /api/identity/token/{tokenId}/full` | DN, `contactUri`, traits (JWT) |
| Plugin: `identyclaw_list_agents` → `identyclaw_get_agent_identity` | Same flow via OpenClaw tools |

**Today:** paginate `/api/agents`, then `/full` per candidate. Server-side search / invite card / contact lookup are tracked outside this repo.

---

## Trust a peer

**Norm:** **Verify before execute** — verify HOLA, then run tools. Publish your canonical `tokenId` so peers can impersonation-guard you.

| Resource / API | Purpose |
| --- | --- |
| `doc:reference:verify-hola-recipes` | **Start here (verifiers)** — copy-paste Node/Python/bash recipes (~20 lines) |
| `doc:reference:a2a-onboarding-concierge` | Lemuel Gulliver A2A Onboarding Concierge at identyclaw-concierge.identyclaw.com:7443 |
| `doc:reference:concierge-lobby-passport` | Canonical lobby `tokenId` + multi-channel ContactURI |
| `doc:reference:a2a-registry-submission` | Operator checklist for A2A Registry submit |
| `doc:reference:identity-verification-policy` | Normative proof bar — family, liveness, partner/peer, controlling address |
| `doc:reference:hola-howto` | Build and send HOLA in ~5 minutes |
| `POST /api/identity/verify` | One-call peer verification (`verified: true` only); set `includeProfile: true` for passport summary |
| https://verify.identyclaw.com | Web UI — same report as `npx @rodit/verify-hola report` |
| `GET /api/concierge/trust-anchor` | Official concierge lobby `tokenId` when configured |
| `doc:reference:hola-subagent-authentication` | Delegated signer format + `POST /api/isauthorizedsigner` |
| Plugin: `identyclaw_create_hola` | Outbound HOLA (local sign; key stays on Gateway) |
| Plugin: `identyclaw_verify_hola`, `identyclaw_check_subagent_signer` | OpenClaw wrappers |

**Rule (verify before execute):** Do not grant tools or secrets until inbound HOLA passes **full independent validation** on the receiving peer (IdentyClaw API or direct NEAR RPC — peer's choice). Copy-paste notes: `doc:reference:verify-hola-recipes`.

---

## Reach them on a channel

IdentyClaw provides **identity and trust**, not transport.

| Resource | Purpose |
| --- | --- |
| `doc:reference:inter-agent-communication` | Optional email + HOLA patterns (Himalaya) — MCP docs only; not in ClawHub skill bundle |
| `doc:reference:collaboration-envelope` | Normative JSON envelope for any channel |
| `contactUri` from `/full` | Self-declared routing hint — `scheme:authority:identifier`; standard + extended schemes in `doc:reference:token-metadata` § ContactURI |

**Verification order:** parse envelope → verify `hola` via `/api/identity/verify` → process `task` payload only when trusted.

---

## Multi-tenant and cross-org collaboration

| Resource | Purpose |
| --- | --- |
| `doc:reference:multi-tenant-collaboration` | Fleet patterns, first-contact flow, tenant isolation checklist |
| `doc:reference:openclaw-passport-value` | When Passport beats static webhook secrets (OpenClaw operators) |
| `doc:reference:identity-verification-policy` | Proof bar before executing delegated or cross-tenant tasks |
| `public/policies/why-identyclaw.md` §12 | Conceptual background (or MCP policy resource if exposed) |

---

## Inbound events (OpenClaw)

| Resource | Purpose |
| --- | --- |
| `doc:reference:openclaw-passport-value` | Why Passport for OpenClaw — peers as `tokenId`, split auth, when to skip |
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
| `doc:reference:inter-agent-communication` | Optional email outreach (MCP; out of ClawHub skill scope) |
| `doc:reference:collaboration-envelope` | Channel-agnostic task envelope |
| `doc:reference:multi-tenant-collaboration` | Multi-tenant / cross-org operator patterns |
| `doc:reference:verify-hola-recipes` | Verify before execute — verifier copy-paste recipes |
| `doc:reference:identity-verification-policy` | Verification checklist (family, peer/partner, controller) |
| `doc:reference:hola-subagent-authentication` | Subagent delegation |
| `doc:reference:openclaw-integration-guide` | Webhook wiring |
| `doc:reference:openclaw-passport-value` | Passport vs static secrets (OpenClaw) |
| `doc:reference:mcp-auth-tools` | Client-side JWT |
| `doc:reference:mcp-connection-guide` | MCP setup and troubleshooting |
| `doc:reference:agent-frameworks` | OpenClaw / Hermes / IronClaw / NanoClaw / Cursor routing |
| `doc:reference:hermes-integration-guide` | Hermes enrollment and daily API |
| `doc:reference:ironclaw-integration-guide` | IronClaw MCP + sidecar |
| `doc:reference:nanoclaw-integration-guide` | NanoClaw container enrollment |
| `doc:reference:did-rodit-method` | DID method spec (`GET /.well-known/did-method-rodit`) |
| `doc:reference:did-method-registry-submission` | W3C DID Method Registry checklist |
| `doc:reference:standards` | IETF WIMSE alignment and convergence map |
| `guide:subagents` | Delegation JSON guide |
