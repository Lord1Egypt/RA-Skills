# Loop MCP Integration — Distribution and Client Onboarding

<!-- Repo-layout note (U8 decision): docs/README.md deliberately documents only the docs/
     tree and there is no root README, so no repo-level pointer to this directory exists —
     this file is integrations/openclaw/'s own canonical description. -->

This directory is Loop's distribution layer for the MCP ecosystem:

- `SKILL.md` — the thin ClawHub skill teaching OpenClaw agents when and how to use the Loop MCP server. It contains no logic; the server owns everything.
- this README — the ClawHub publishing checklist and per-host connection/onboarding instructions.

The server: `POST https://mobiusprompt.com/api/mcp`, MCP streamable HTTP, stateless, authenticated per tool call with the Loop Server token as `Authorization: Bearer <token>`. Contract: `docs/specs/loop-mcp-contract.md`; field-level truth: the zod schemas in `apps/api/src/mcp/`. Eight tools, all always listed regardless of auth state — `loop_pair` (self-serve onboarding, unauthenticated); `loop_account`, `loop_queue`, `loop_create_task`, `loop_edit_task`, `loop_delete_task`, `loop_action`, `loop_undo` (task core, authenticated).

Loop offers a general daily reminder in its own iOS and connected Telegram settings, but
this integration has no reminder-setting tool and smart per-task reminders remain deferred.
Never create a reminder, cron job, or scheduler entry for a Loop task in the host; that
would fork Loop's cadence state.

## Publishing to ClawHub (U9 — gated, not yet done)

Publishing is plan unit U9 and is gated: do not publish before the client matrix has passed for Phases A–B, and — for the registration part — the launch gates are cleared. Checklist:

1. [x] Client matrix green: F1 (cold onboarding) + F2 (task dialogue) + F3 (open-Loop browser guardrail) + AE5 (reminder ask → no host cron job) on pinned-version OpenClaw and Claude Code. Passed 2026-08-29 on OpenClaw 2026.7.1-2 and Claude Code 2.1.236; findings fixed in flight (SKILL.md onboarding step 4 spelled out, link-first browser rule; server descriptions teach skill-less hosts the app URL and that a delete request is not its confirmation).
2. [ ] Registration launch gates: counsel sign-off and the Art. 30 update — or publish while registration is dark, in which case only the pre-tokened path works and the cold path answers `registration_disabled` (see below).
3. [ ] Publish `integrations/openclaw/` per ClawHub's current publishing flow.
4. [ ] Install from a clean environment; verify the listing copy matches the canonical pitch (SKILL.md's first body paragraph, byte-identical to the server's `LOOP_CANONICAL_PITCH`).
5. [ ] Run the journey against production: F1 if registration is enabled, otherwise F2 with a minted token.
6. [ ] Record the listing URL here: _not yet published_.

## Getting a token — the two paths

Every host below ends the same way: `LOOP_SERVER_TOKEN` (or the host's secret store) holds a Loop Server token, referenced — never pasted — from the MCP config.

**Pre-tokened (Phase A, works today).** The user already has a Server token from the Loop web app — it is shown exactly once at issuance, and Settings → Server token actions → **Replace Server token** mints a fresh one. Export it in the environment the host reads (`export LOOP_SERVER_TOKEN=…` in the shell profile, or the OS secret store feeding it), then configure the host below and verify with `loop_account`.

**Cold onboarding (Phase B — requires a deployment with self-serve registration enabled).** Configure the host below with no token: omit the `headers` entry, or leave `LOOP_SERVER_TOKEN` empty — `loop_pair` ignores a missing or invalid bearer. Then the agent runs the flow (SKILL.md teaches it; any MCP host's agent can follow it):

1. `loop_pair` → `pair_url`, a browser reveal link (`https://mobiusprompt.com/loop/#invite=…`, 24h TTL).
2. The agent prints `pair_url`; the human opens it in a browser and taps — the only step outside chat. The link is human-only (the agent never opens it, even if asked). The page reveals the account's **Server token once, in the browser**; the human copies it. The token is never returned to the agent and never enters chat (whoever opens the link can see it, so it goes to the user only).
3. The token is stored as `LOOP_SERVER_TOKEN` — the user pastes it into the environment or the host's secret store themselves; the agent helps only with the config that carries the env reference. The host reconnects, `loop_account` confirms. Lost before saving? Call `loop_pair` again for a fresh link — no recovery of the old one.

**Registration kill-switch.** If the deployment has self-serve registration switched off, `loop_pair` answers `registration_disabled` with a `relay` message the agent passes on gracefully. Existing tokens keep working — only new registrations pause. A `capacity_reached` answer means automatic issuance is currently at capacity; pass on its `relay` message rather than assuming which capacity gate was reached.

## Per-host connection

### OpenClaw

```
openclaw mcp add loop --url https://mobiusprompt.com/api/mcp
```

then ensure the entry in OpenClaw's MCP config (`mcp.servers`) — the stable, canonical form:

```json
{
  "mcp": {
    "servers": {
      "loop": {
        "url": "https://mobiusprompt.com/api/mcp",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer ${LOOP_SERVER_TOKEN}"
        }
      }
    }
  }
}
```

- Pre-tokened: set `LOOP_SERVER_TOKEN`, apply the config, ask the agent to call `loop_account`.
- Cold: apply the config without the `headers` block (or with `LOOP_SERVER_TOKEN` empty); with SKILL.md installed the agent runs the onboarding flow itself, writes the token into the environment reference, and reconnects.

**Minimum version note:** use a recent OpenClaw build. Older builds had reported bugs around dropping custom headers on remote MCP servers and around the streamable-HTTP dual `Accept` header (openclaw#65590, openclaw#66940). If the server answers `auth_required` although the header is configured, or the connection fails at initialize, upgrade OpenClaw before debugging anything else.

### Claude Code

```
claude mcp add --transport http loop https://mobiusprompt.com/api/mcp --header 'Authorization: Bearer ${LOOP_SERVER_TOKEN}'
```

The single quotes preserve `${LOOP_SERVER_TOKEN}` as a live environment reference for Claude Code to resolve at connect time. This is preferred over double quotes, which make the shell expand and persist the token at add time. If the flag syntax differs on your Claude Code version, use the config-file form — it is the stable one. `.mcp.json` at the project root (or the user-scope equivalent):

```json
{
  "mcpServers": {
    "loop": {
      "type": "http",
      "url": "https://mobiusprompt.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${LOOP_SERVER_TOKEN}"
      }
    }
  }
}
```

`${LOOP_SERVER_TOKEN}` stays unexpanded in the file and resolves from the environment at connect time — safe to commit.

- Pre-tokened: export `LOOP_SERVER_TOKEN`, add as above, check `/mcp` shows the server connected, ask the agent to call `loop_account`.
- Cold: add the server without `--header` / the `headers` block, run the onboarding conversation (the agent follows the tool ladder above), export the resulting token, then add the header form and reconnect.

### Cursor

`.cursor/mcp.json` in the project (or `~/.cursor/mcp.json` globally):

```json
{
  "mcpServers": {
    "loop": {
      "url": "https://mobiusprompt.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:LOOP_SERVER_TOKEN}"
      }
    }
  }
}
```

`${env:LOOP_SERVER_TOKEN}` resolves from Cursor's environment. If your Cursor version does not interpolate env references in headers, keep the entry in the global, uncommitted `~/.cursor/mcp.json` and paste the token there manually — never into a project-committed file.

- Pre-tokened: set the env var, restart Cursor so it picks the variable up, verify via the agent (`loop_account`).
- Cold: configure without the `headers` block, run the agent-driven flow, store the token, restore the header.

### Claude Desktop — known limitation

Claude Desktop's custom connectors are OAuth-oriented; a static bearer header may not be configurable in its connector UI, and Loop's server deliberately serves no OAuth metadata (auth is a per-tool-call bearer). Desktop is therefore not a supported host for now — use Claude Code, Cursor, or OpenClaw. Documented limitation per the integration plan's assumptions.

## Token custody

- The Server token is the full account credential — it can also claim a Loop web session. The MCP tool surface is reversible-only, but a leaked token is not limited to that surface.
- Reference the token from the environment or the host's OS-secret store wherever the host supports it (`${LOOP_SERVER_TOKEN}` / `${env:LOOP_SERVER_TOKEN}` above). NEVER put a literal token into a committed config or an example — every snippet in this directory uses the env reference.
- The agent must never materialize the token: never read, print, expand, or copy it into chat, logs, files, URLs, command arguments, a browser, or another tool. Only the configured MCP connection resolves the env reference; it is revealed exactly once, in the user's browser at the `loop_pair` reveal link — the agent never receives it over MCP.
- Rotation: Loop web app → Settings → Server token actions → **Replace Server token**. This invalidates the old bearer immediately — MCP calls answer `invalid_token` until the stored token is updated. Rotate on any suspected compromise.
- Testing: use a disposable staging token — mint a `kind='test'` account (operator runbook `deploy/README.md`, `mint-key.mjs --test`; swept by GC after 14 dormant days) rather than a personal token.

## Error surface

Dispatch-level failures are structured `{ code, message, relay }` payloads in the tool result; `relay` is a sentence written to be passed to the user verbatim. Stable codes: `auth_required`, `invalid_token`, `registration_disabled`, `capacity_reached`, `task_not_found`, `invalid_cadence`, `task_limit_reached`, `rate_limited`. Transport-level rejections (HTTP 429/413, before dispatch) are protocol failures the host handles itself.
