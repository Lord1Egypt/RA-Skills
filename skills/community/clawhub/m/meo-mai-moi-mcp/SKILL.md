---
name: meo-mai-moi-mcp
description: "Use when the user asks to connect to, authorize, or do anything with Meo Mai Moi through its remote OAuth MCP gateway: a pet, care, placement, finance, or account task run over MCP, or choosing and upgrading the scopes one needs. Not for direct REST calls with a personal Meo API token, which the separate meo-mai-moi skill covers."
---

# Meo Mai Moi MCP

Use the OAuth MCP gateway for Meo Mai Moi: pet management for nerds. Meo Mai Moi remains authoritative for product rules and permissions; MCP is the agent-facing adapter. Do not duplicate pet-domain operating knowledge from the separate `meo-mai-moi` skill.

## Connect

1. Check whether Meo MCP tools or a saved `meo-mai-moi` server are already available. Reuse a valid connection instead of registering a duplicate.
2. When the user explicitly asks to connect or authorize Meo, treat that as authority to configure only the client's `meo-mai-moi` MCP entry. Initiate OAuth yourself when the client and execution policy allow it.
3. Choose scopes with the rules below, then configure `https://mcp.meo-mai-moi.com/mcp` and authenticate through OAuth.
4. Treat these as separate states—do not collapse them:
   - **Configured**: the client has a saved `meo-mai-moi` server entry.
   - **OAuth success**: tokens were exchanged and stored.
   - **MCP probe success**: a live client session reaches the gateway (OpenClaw: `openclaw mcp probe meo-mai-moi`).
   - **Native tool projection**: Meo tools are callable in the *current* agent session (after OpenClaw `/new` or `/reset`, a Codex CLI restart into a fresh session, or an equivalent client reload).
5. Only after projection, discover tools and start with a read such as `list_pets`.

Never ask for an OAuth access token, refresh token, client secret, stored OAuth file, or Meo personal API token. An agent that runs without any browser can use an **agent client** instead: the user creates it on Meo's Developer page and stores its client id and secret in the host's secret store, where the agent reads it. Never ask for that secret in chat; see [references/connection.md](references/connection.md#headless-agents). A headless OpenClaw flow has a narrow private-chat exception for the short-lived authorization URL and single-use code; follow [references/openclaw.md](references/openclaw.md).

Read [references/connection.md](references/connection.md) for presets, scope tables, and client-neutral setup. When running in OpenClaw, read and follow [references/openclaw.md](references/openclaw.md). Read [references/safety.md](references/safety.md) before consequential writes or structured errors.

## Choose scopes

- An **explicit narrow task** requests only that task's domain scopes.
- A **broad or unqualified** request such as “connect Meo Mai Moi” or “manage my pets” defaults to the **Everyday care** preset.
- **Full management** is never inferred. Offer it only when the user asks for everything or explicitly selects it, and warn first that it permits sensitive reads and writes across finances, messages, sharing, placement, groups, profile, and invitations.
- Scope upgrades stay task-driven: reauthorize only for the missing domain scopes unless the user explicitly changes preset.

Everyday care and Full management scope strings live in [references/connection.md](references/connection.md).

## Work safely

- Discover current state and resolve stable IDs before mutating.
- For updates and deletes, preserve the version returned by the matching read.
- Use a new idempotency key for each intended write. Reuse it only to retry the exact same write after an uncertain transport failure.
- A few tools take no idempotency key, because the route behind them has no replay protection. Do not invent one, and do not retry those writes blindly after an uncertain failure: read first and check whether the write landed.
- Treat sharing, rehoming/placement, messages, groups, finance, invitations, medical media, and personal profile data as sensitive.
- Verify a completed write with the relevant read tool.

## Choose the right integration

Use this skill for remote OAuth MCP. If the user explicitly wants a direct REST integration with a user-managed Meo personal API token, stop and use the separate `meo-mai-moi` skill.

## Public documentation

- Clients: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/clients.md`
- Tools: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/tools.md`
- OAuth: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/oauth.md`
- Errors: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/errors.md`

Keep personal records, messages, invitation material, health data, and financial values out of chat unless the user needs them to decide.
