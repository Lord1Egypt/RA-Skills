---
name: meo-mai-moi-mcp
description: "Connect, authorize, and safely use Meo Mai Moi through its OAuth MCP gateway for pet profiles, care and health records, habits, microchips, sharing, rehoming or placement, helper profiles, messages, groups, pet finances, notifications, and account workflows. Use when a user asks an OAuth-capable agent such as Codex, Cursor, or OpenClaw to connect or authorize Meo Mai Moi, manage Meo data, choose scopes or presets, list pets, coordinate pet care, or automate a pet-related workflow. In OpenClaw, configure the native MCP entry, complete OAuth, probe, and have the user start a new session before the first Meo call. Do not use for direct REST API or personal-token integrations; use the separate meo-mai-moi skill instead."
---

# Meo Mai Moi MCP

Use the OAuth MCP gateway for Meo Mai Moi: pet management for nerds. Meo Mai
Moi remains authoritative for product rules and permissions; MCP is the
agent-facing adapter. Do not duplicate pet-domain operating knowledge from the
separate `meo-mai-moi` skill.

## Connect

1. Check whether Meo MCP tools or a saved `meo-mai-moi` server are already
   available. Reuse a valid connection instead of registering a duplicate.
2. When the user explicitly asks to connect or authorize Meo, treat that as
   authority to configure only the client's `meo-mai-moi` MCP entry. Initiate
   OAuth yourself when the client and execution policy allow it.
3. Choose scopes with the rules below, then configure
   `https://mcp.meo-mai-moi.com/mcp` and authenticate through OAuth.
4. Treat these as separate states—do not collapse them:
   - **Configured**: the client has a saved `meo-mai-moi` server entry.
   - **OAuth success**: tokens were exchanged and stored.
   - **MCP probe success**: a live client session reaches the gateway
     (OpenClaw: `openclaw mcp probe meo-mai-moi`).
   - **Native tool projection**: Meo tools are callable in the *current*
     agent session (after OpenClaw `/new` or `/reset`, or an equivalent
     client reload).
5. Only after projection, discover tools and start with a read such as
   `list_pets`.

Never ask for an OAuth access token, refresh token, client secret, stored
OAuth file, or Meo personal API token. A headless OpenClaw flow has a narrow
private-chat exception for the short-lived authorization URL and single-use
code; follow [references/openclaw.md](references/openclaw.md).

Read [references/connection.md](references/connection.md) for presets, scope
tables, and client-neutral setup. When running in OpenClaw, read and follow
[references/openclaw.md](references/openclaw.md). Read
[references/safety.md](references/safety.md) before consequential writes or
structured errors.

## Choose scopes

- An **explicit narrow task** requests only that task's domain scopes.
- A **broad or unqualified** request such as “connect Meo Mai Moi” or
  “manage my pets” defaults to the **Everyday care** preset.
- **Full management** is never inferred. Offer it only when the user asks for
  everything or explicitly selects it, and warn first that it permits
  sensitive reads and writes across finances, messages, sharing, placement,
  groups, profile, and invitations.
- Scope upgrades stay task-driven: reauthorize only for the missing domain
  scopes unless the user explicitly changes preset.

Everyday care and Full management scope strings live in
[references/connection.md](references/connection.md).

## Work safely

- Discover current state and resolve stable IDs before mutating.
- For updates and deletes, preserve the version returned by the matching read.
- Use a new idempotency key for each intended write. Reuse it only to retry the
  exact same write after an uncertain transport failure.
- Treat sharing, rehoming/placement, messages, groups, finance, invitations,
  medical media, and personal profile data as sensitive.
- Verify a completed write with the relevant read tool.

## Choose the right integration

Use this skill for remote OAuth MCP. If the user explicitly wants a direct
REST integration with a user-managed Meo personal API token, stop and use the
separate `meo-mai-moi` skill.

## Public documentation

- Clients: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/clients.md`
- Tools: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/tools.md`
- OAuth: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/oauth.md`
- Errors: `https://github.com/troioi-vn/meo-mcp/blob/main/docs/errors.md`

Keep personal records, messages, invitation material, health data, and
financial values out of chat unless the user needs them to decide.
