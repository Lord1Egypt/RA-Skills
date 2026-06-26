---
name: pattern-agent-api-discipline
description: Verify n8n REST API shapes via Context7 before invoking helpers — agent-meta-discipline rule that catches doc-vs-training-data drift on parameters, status enums, response shapes, and pagination model.
user-invocable: false
---

# Pattern: agent-api-discipline

> **This is an agent-discipline pattern**, not a workflow-runtime pattern. It tells the agent how to verify its own assumptions before invoking the harness's helpers — not how to design workflows.

The harness wraps n8n's public REST API. The agent's training data lags the live API by months — query-string parameter names, status enum values, response shapes, and pagination cursors drift. When the agent's recalled-from-training assumption is wrong, the failure mode is silent: a helper invocation looks plausible, the request goes through, but the response is empty or malformed, and downstream reasoning compounds the bad data.

This pattern's rule: **before relying on remembered API knowledge, query Context7 for the doc that confirms (or refutes) the shape**. Treat training data as a hint, not as ground truth.

## When to apply

Run a Context7 verification step at the start of any sub-skill that calls n8n's REST API directly or via a harness helper, especially when:

- Choosing a `--status` value (the enum drifts: `failed` vs `error`, presence/absence of `crashed` / `queued` / `new`).
- Filtering by query parameter (which fields are accepted? which are required vs optional?).
- Parsing a response (paginated via `nextCursor`? offset? what's the shape of `data[]`?).
- Calling a less-common endpoint (`/audit`, `/variables`, `/executions/stop`, `/users`, `/projects`, `/source-control`).

Skip the verification only when:

- The helper has been called recently in this session and worked — the in-session evidence supersedes recall.
- The endpoint is a frequently-exercised CRUD on `/workflows` or `/credentials` and the request is identical to documented examples in the harness's own helpers.

## How to apply

```
Tool: mcp__context7__query-docs
libraryId: "/n8n-io/n8n-docs"
query: "<endpoint> <method> parameters response shape"
```

Examples that have actually mattered for harness work:

| Sub-skill | Query |
|---|---|
| `debug` | `"GET /api/v1/executions parameters cursor nextCursor pagination response shape"` |
| `manage-credentials` (Path B) | `"GET /api/v1/credentials filter type response shape"` |
| `register-workflow-to-error-handler` | `"GET /api/v1/workflows settings.errorWorkflow shape"` |
| `bootstrap-env` | `"POST /api/v1/workflows minimum required body fields"` |
| `doctor --with-audit` | `"POST /api/v1/audit request body category sections risk fields"` |
| `run` | `"GET /api/v1/executions/{id} includeData query param response shape"` |

If Context7 returns conflicting or absent docs, FALL BACK to a live smoke against the env the agent will operate against. Document the smoke result in the relevant skill / pattern doc and proceed against the captured shape — not the remembered shape.

## Worked example: status enum drift

A common failure mode the harness has hit:

> Training data and some online tutorials use `status=failed`. n8n's current public API uses `status=error`. A `list_executions.py --status failed` call returns an empty `data` array — not an error — so an agent skimming results concludes "no failed executions" when there are dozens.

Context7 verification at the start of any execution-listing flow surfaces the correct enum (`error | success | running | canceled | waiting | crashed | queued`) and avoids the silent-empty failure.

## Worked example: parameter required vs optional

Context7's per-endpoint spec for `GET /api/v1/executions` historically marked `workflowId` as **Required**. n8n's CLI examples and release notes treat it as optional. The harness's `list_executions.py` is built around the optional reading after a live smoke confirmed it. If the spec ever flips and a future n8n release enforces `workflowId`-required, helpers depending on the optional reading would silently regress to "fetch nothing" — verification first, then reshape if needed.

## What this pattern is NOT

- It is not a directive to verify EVERY tool call. The agent's job is to ship work — verification is a focused diagnostic step at sub-skill boundaries, not a per-line interrupt.
- It is not a substitute for the helper's own input validation. Helpers reject malformed inputs at parse time; this pattern catches the case where the inputs are well-formed but built on a wrong mental model of the API.
- It is not a free-form "search for n8n documentation." Use Context7's `query-docs` against the pinned `/n8n-io/n8n-docs` library — that's what's been verified to surface the right per-endpoint specs.

## Cross-references

Sub-skills that should run a Context7 verification step:

- `skills/debug.md` — `/executions`, `/executions/{id}`, `/executions/stop`
- `skills/run.md` — `/executions`, `/executions/{id}`
- `skills/deploy.md` — `/workflows/{id}` PUT, `/workflows/{id}/activate`
- `skills/bootstrap-env.md` — `/workflows` POST + minimum body fields
- `skills/manage-credentials.md` — `/credentials` GET / POST
- `skills/register-workflow-to-error-handler.md` — `/workflows` GET (verify `settings.errorWorkflow` shape)
- `skills/doctor.md` — `/audit` POST (when `--with-audit` enabled)
