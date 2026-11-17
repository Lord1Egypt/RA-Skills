# Oi MCP Tools

Oi is exposed through the hosted MCP server at `https://api.oioioi.ai/mcp`.

Core details:

- Transport: Streamable HTTP.
- Auth: OAuth or bearer token using an Oi organization API key.
- Runtime: prefer `openclaw` when the client can send runtime metadata.

## OpenClaw setup

Register Oi in OpenClaw's MCP registry under `mcp.servers`:

```bash
openclaw mcp add oi \
  --url https://api.oioioi.ai/mcp \
  --transport streamable-http \
  --auth oauth

openclaw mcp login oi
openclaw mcp doctor oi --probe
```

If installing from a local clone of this repo, `bash scripts/install-to-openclaw.sh` performs the same skill and MCP registration steps.

For bearer-token setup, organization API key instructions, and headless auth, read `authentication.md` in this references folder.

Manual config snippet when editing `~/.openclaw/openclaw.json` directly: see `config/mcp-server.json5` in the oi-openclaw repo.

Useful commands:

- `openclaw mcp list` — show registered servers
- `openclaw mcp show oi` — show the saved Oi definition
- `openclaw mcp login oi` — complete OAuth sign-in
- `openclaw mcp doctor oi --probe` — verify connection and tools
- `openclaw mcp reload` — refresh cached MCP runtimes after config changes

MCP config under `mcp.*` hot-applies; a full gateway restart is not required for routine MCP edits.

After installing or updating the skill, start a new agent session (for example `/new`) so OpenClaw picks up the refreshed skill snapshot.

## Canonical Tools

- Identity and routing: `oi.auth.whoami`, `oi.recommend`.
- Contexts: `oi.contexts.list`, `oi.contexts.search`, `oi.contexts.create`, `oi.contexts.get`, `oi.contexts.update`, `oi.contexts.start-session`, `oi.contexts.use`, `oi.contexts.save-draft-feedback`.
- Workflows: `oi.workflows.list`, `oi.workflows.create`, `oi.workflows.get`, `oi.workflows.update`, `oi.workflows.start-session`, `oi.workflows.use`.
- Skills: `oi.skills.list`, `oi.skills.search`, `oi.skills.create`, `oi.skills.get`, `oi.skills.update`, `oi.skills.publish`, `oi.skills.use`.
- Guardrails: `oi.guardrails.list`, `oi.guardrails.create`, `oi.guardrails.get`, `oi.guardrails.update`, `oi.guardrails.delete`, `oi.guardrails.release`, `oi.guardrails.publish`, `oi.guardrails.unpublish`, `oi.guardrails.confirm`.
- Durable feedback and reporting: `oi.brain.save-feedback`, `oi.usage.report`, `oi.effectiveness.report`.

## Brain

- Use `oi.brain.save-feedback` for direct durable Org Brain or User Brain updates, not as a substitute for Context or Workflow authoring.
- Use organization scope for shared facts, terminology, policies, project context, and recurring team practices; use user scope for private preferences and individual working style.
- When scope or permission is unclear, call with `scope: auto` and `confirmed: false`, show the returned confirmation prompt, and reuse its `saveArguments` after approval.
- When the user explicitly requests a specific scoped Brain update, use that scope with `confirmed: true`.
- Never save one-off details, guesses, unconfirmed assumptions, secrets, credentials, or sensitive private data.

## Reporting

- `oi.usage.report` attaches known runtime and token accounting to a prior Context or Workflow `usageEventId`; never estimate values or send prompt text.
- `oi.effectiveness.report` records known outcomes after Context, Workflow, Skill, Connection, or Guardrail-assisted work. Report only observed outcome, retries, actions, feedback, baseline, and confidence; keep any task summary short and redacted.

## Connection tools

Use the stable Connection router only; never invent provider-specific Oi tool names:

1. `oi.connections.list`: list installed Connection instances and select the provider and optional exact instance.
2. `oi.connections.get`: inspect that Connection's live actions, endpoint keys, and input schemas.
3. `oi.connections.use`: execute the exact returned action with schema-matching arguments.

Reads do not require confirmation. Explain external writes and obtain explicit approval before setting `confirmed: true`. If the Connection is missing or unauthenticated, direct the user to install or authenticate it in Oi.

## Compatibility Aliases

Some clients expose underscore aliases. Treat these as aliases for the canonical tools:

- Canonical dots and hyphens become underscores, for example `oi_contexts_use`, `oi_workflows_start_session`, `oi_skills_use`, or `oi_connections_get`.
- Older clients may expose legacy verb-first aliases such as `oi_use_context` or `oi_list_workflows`.

Prefer canonical dotted names in OpenClaw documentation and configuration.

## Prompts and resources

- Oi prompts include `oi.routing.task`, `oi.contexts.use`, and `oi.workflows.use` when the client exposes MCP prompts.
- Marketplace resources: `oi://marketplace/contexts`, `oi://marketplace/guardrails`, `oi://marketplace/workflows`, `oi://marketplace/skills`, and `oi://marketplace/connections`.
- Organization resources: `oi://organization/contexts`, `oi://organization/guardrails`, `oi://organization/workflows`, `oi://organization/skills`, and `oi://organization/connections`.
- Legacy compatibility resources: `oi://catalog/public-contexts`, `oi://catalog/private-contexts`, and `oi://catalog/workflows`.
- Treat resources as read-only catalog context and use tools for search, execution, authoring, lifecycle changes, Brain, Connections, or reporting.

## Selection Rules

- Use `oi.contexts.use` when the user names a Context or asks Oi to do a concrete task.
- Use `oi.workflows.use` when the user names a Workflow, uses `workflow`/`wf`, or wants a repeatable multi-step process.
- Use `oi.recommend` when the user asks which setup to use.
- Use `oi.skills.use` when the user names an available Skill or asks Oi to apply one.
- Use the list/get/use Connection sequence for connected-provider data.
- Use list tools only to browse. Do not infer absence from a list preview.
- Use start-session tools when the user asks to keep a Context or Workflow active for the thread.
- Use save-draft-feedback or brain save-feedback only for durable, confirmed future behavior changes; never save secrets or one-off task details.
