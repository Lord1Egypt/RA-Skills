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

- `oi.contexts.use`: Primary tool for concrete Context-backed tasks. Provide `prompt`; optionally provide raw `contextId`.
- `oi.contexts.list`: Browse a paginated preview of installed Contexts. This is not exhaustive.
- `oi.contexts.get`: Return the reusable compiled prompt for a specific Context.
- `oi.contexts.start-session`: Load one or more Contexts as reusable session context for the current thread.
- `oi.workflows.use`: Primary tool for concrete Workflow-backed tasks. Provide `prompt`; optionally provide `workflowId`.
- `oi.workflows.list`: Browse available Workflows.
- `oi.workflows.get`: Return the reusable compiled prompt scaffold for a specific Workflow.
- `oi.workflows.start-session`: Load a Workflow as reusable session context for the current thread.
- `oi.recommend`: Recommend the best installed Context or Workflow for a prompt.
- `oi.contexts.save-draft-feedback`: Save confirmed durable feedback into a mutable private Context draft.
- `oi.brain.save-feedback`: Save confirmed durable feedback into Org Brain or User Brain after explicit user approval.
- `oi.guardrails.confirm`: Confirm a triggered Guardrail and continue.
- `oi.usage.report`: Attach token accounting and runtime metadata to a prior Oi usage event.

## Connection tools

Use these only when the user's organization has configured Oi connections (for example CRM integrations):

- `oi.connections.search-records`: Search records in a connected provider through Oi.
- `oi.connections.list-tools`: List tools exposed by a connected provider.
- `oi.connections.call-tool`: Call a specific connected-provider tool through Oi.

Require explicit user approval before calling connection tools that read or write external provider data.

## Compatibility Aliases

Some clients expose underscore aliases. Treat these as aliases for the canonical tools:

- `oi_contexts_use`, `oi_use_context`
- `oi_contexts_list`, `oi_list_contexts`
- `oi_contexts_get`, `oi_get_context`
- `oi_contexts_start_session`, `oi_start_prompt_session`, `oi_start_context_session`
- `oi_workflows_use`, `oi_use_workflow`
- `oi_workflows_list`, `oi_list_workflows`
- `oi_workflows_get`, `oi_get_workflow`
- `oi_workflows_start_session`, `oi_start_workflow_session`
- `oi_recommend`, `oi_recommend_context`, `oi_recommend_workflow`
- `oi_guardrails_confirm`, `oi_usage_report`
- `oi_save_feedback_to_draft`, `oi_save_feedback_to_brain`

Prefer canonical dotted names in OpenClaw documentation and configuration.

## Selection Rules

- Use `oi.contexts.use` when the user names a Context or asks Oi to do a concrete task.
- Use `oi.workflows.use` when the user names a Workflow, uses `workflow`/`wf`, or wants a repeatable multi-step process.
- Use `oi.recommend` when the user asks which setup to use.
- Use list tools only to browse. Do not infer absence from a list preview.
- Use start-session tools when the user asks to keep a Context or Workflow active for the thread.
- Use save-draft-feedback or brain save-feedback only for durable, confirmed future behavior changes; never save secrets or one-off task details.
