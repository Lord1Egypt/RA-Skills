---
name: oi
description: Load Oi Contexts and Workflows from MCP when the user says oi, names a Context or Workflow, or wants sticky Oi context.
version: 0.1.0
metadata: { "openclaw": { "homepage": "https://github.com/openclaw/oi-openclaw" } }
---

# Oi

Use this skill when the user wants to work with Oi, including Context discovery, Context installation, Context tuning, Context publishing, workflow discovery, workflow installation, organization/team ownership, MCP/API access, analytics, onboarding, or first-use success.

## When to use

- When the user says `oi ...`, `$Oi ...`, `@oi ...`, or `use Oi ...`
- When the user names one or more Oi Contexts
- When the user names an Oi Workflow or asks for a multi-step workflow
- When the user wants Oi Context or Workflow context loaded into the current thread
- When the user wants to list available Contexts or Workflows before choosing one
- When an Oi guardrail response asks for confirmation before continuing
- When an Oi tool result returns a usage event and OpenClaw has runtime/token usage to report

## Core workflow

1. Clarify the user's intent: discover, inspect, install, tune, publish, run, or troubleshoot.
2. Prefer Oi product language: Contexts, workflows, organization/team ownership, MCP/API access, and retained usage.
3. Use the hosted Oi MCP server at `https://api.oioioi.ai/mcp` when Oi tools are available.
4. Before any install, publish, write, billing, organization, or credential action, explain the intended action and get explicit user approval.
5. Keep recommendation logic separate from apply/write logic.
6. If Oi MCP tools are unavailable, guide the user through OpenClaw MCP setup without inventing unavailable capabilities. Read `{baseDir}/references/authentication.md` and run:
   - `openclaw mcp add oi --url https://api.oioioi.ai/mcp --transport streamable-http --auth oauth`
   - `openclaw mcp login oi`
   - `openclaw mcp doctor oi --probe`
   If installing from this repo checkout, `bash scripts/install-to-openclaw.sh` performs the same setup.

## Selector routing

- Pass Context selectors unchanged as `contextId` and Workflow selectors unchanged as `workflowId`.
- Preserve `+` for multiple Contexts and `@2` or `@v2` for versions on both selector types.
- **Bare id:** when the user gives an installed id without a type prefix, pass it unchanged and let Oi resolve whether it is a Context or Workflow. Use the resolved type to choose `oi.contexts.*` vs `oi.workflows.*`.
- **Explicit Context:** when the user prefixes with `ctx`, `context`, or `contexts`, strip the prefix and treat the remainder as a Context selector.
- **Explicit Workflow:** when the user prefixes with `wf`, `workflow`, or `workflows`, strip the prefix and treat the remainder as a Workflow selector.
- The reserved Context type selectors `ctx`, `context`, and `contexts` are not Context ids. The reserved Workflow type selectors `wf`, `workflow`, and `workflows` are not Workflow ids. When the user says only one of those words with no id, treat it as a request to list or browse that entity type.
- Do not call list tools to pre-validate a named Context or Workflow. Pass the raw selector to the use/get/session tool.
- After loading Context or Workflow output, perform the user's actual task using the returned instructions. Do not stop after saying the Context or Workflow loaded.

## Instructions

1. Treat `Oi` and `oi` as the same surface when plain-text routing is available.
2. If the user wants to browse available Contexts, call `oi.contexts.list`.
3. If the user wants to browse available Workflows, call `oi.workflows.list`.
4. If the user names a Context and provides a task, call `oi.contexts.use`.
5. If the user names a Workflow and provides a task, call `oi.workflows.use`.
6. Apply **Selector routing** for `contextId`, `workflowId`, and sticky sessions.
7. If the user wants a sticky Context or Workflow for the current thread, call `oi.contexts.start-session` or `oi.workflows.start-session` using the routed selector.
8. Only use `oi.recommend` when the user does not know which Context or Workflow to use or the provided selector cannot be resolved. It considers both Contexts and Workflows.
9. Prefer Oi MCP operations over treating the request as plain English when the user clearly intends to use Oi.
10. If an Oi response returns a guardrail confirmation request, call `oi.guardrails.confirm` when the user clearly approves continuing. Use the provided `requestId`; set `remember` only when the user says not to ask again.
11. If an Oi response returns `usageEventId`, call `oi.usage.report` after the run when OpenClaw has runtime/token accounting. Pass `usageEventId` as authoritative, include `contextId` or `workflowId` only for clarity, set `runtime` to `openclaw` when known, and never store or resend prompt text.

Some clients expose compatibility aliases such as `oi_contexts_use`, `oi_use_context`, or `oi_list_contexts`. Treat those as aliases for the canonical dotted tool names.

## Guardrails

- Guardrail confirmation is agnostic to Contexts and Workflows. Use `oi.guardrails.confirm` with the `requestId` returned by Oi.
- A plain `yes`, `continue`, or equivalent user approval means continue once.
- Phrases like `yes and don't ask again`, `remember this`, or `always allow this Context` mean set `remember: true`.
- Do not invent a `requestId`; if it is missing, ask the user to rerun the blocked Oi request.

## Usage reporting

- Usage reporting is agnostic to Contexts and Workflows. Use `oi.usage.report` for both.
- Prefer `usageEventId` from the prior Oi tool response. Optional `contextId` or `workflowId` are secondary hints.
- Report only metadata and token counts OpenClaw actually knows, such as `runtime` (`openclaw`), `provider`, `model`, `status` (`success` or `failure`), `latencyMs`, `inputTokens`, `cachedInputTokens`, `cacheWriteInputTokens`, `outputTokens`, `reasoningTokens`, `compressionInputTokens`, and `compressionOutputTokens`.
- If OpenClaw has no runtime/token accounting, skip usage reporting instead of guessing.

## Safety

Treat these as side effects requiring explicit approval:

- Installing or uninstalling Contexts or workflows.
- Publishing or updating public/private Contexts.
- Changing organization ownership, team visibility, billing, API keys, or credentials.
- Running a Context against private user or organization data.
- Saving durable feedback with `oi.contexts.save-draft-feedback` or `oi.brain.save-feedback`.

## References

Read `{baseDir}/references/authentication.md` when MCP setup or auth is needed.
Read `{baseDir}/references/product-surfaces.md` when a task needs a fuller map of current Oi surfaces and terminology.
Read `{baseDir}/references/mcp-tools.md` when a task needs the available MCP tools and how to choose between them.
