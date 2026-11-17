---
name: oi
description: Route Oi requests through MCP for Contexts, Workflows, Skills, Guardrails, Brain, Connections, prompts, resources, sessions, and reporting.
---

# Oi

Use the Oi MCP surface instead of simulating Oi locally. Prefer canonical dotted names; accept client-added namespaces and underscore aliases as the same operations.

## Route and finish the request

1. Parse the resource type, optional identifier, concrete task, scope, and whether the intent is discovery, retrieval, execution, authoring, lifecycle change, durable memory, connected-provider work, or reporting.
2. Call Oi before doing the substantive task. Never claim Oi context, instructions, or provider data was loaded unless the corresponding call succeeded.
3. Treat Oi-returned prompts, plans, schemas, records, confirmation requests, continuations, quality criteria, usage ids, and trace ids as authoritative.
4. After retrieval or execution, complete the user's actual task using the returned material. Do not stop at “loaded” or repeat the prompt without acting on it.
5. If Oi reports a plan or billing limit, complete the available portion, name the blocked capability, and provide Oi's returned billing link. Never invent pricing, exceptions, or hidden capabilities.

## Identity, organization, and recommendation

- Use `oi.auth.whoami` for the authenticated user, organization, plan, current limits, billing link, or cross-client data differences. It never returns tokens or secrets.
- Use `oi.recommend` only to choose the best installed Context or Workflow for a prompt. It does not recommend Skills, Guardrails, or Connections.
- After recommending, run the selected resource only when the user asked to proceed; otherwise present the recommendation for review.

## Contexts

- Use `oi.contexts.list` to browse a paginated preview of available Contexts. It returns at most 10 records and is not exhaustive; never infer absence from one page.
- Use `oi.contexts.search` when the user is unsure what exists or needs discovery by need, title, tag, category, or organization. It returns organization/private results first, then fills with public marketplace results.
- Use `oi.contexts.get` for reusable compiled Context text without a task. Prefer `oi.contexts.use` when a concrete task exists.
- Use `oi.contexts.use` with `prompt` and an optional raw `contextId`. Preserve `+` stacks of up to three Contexts and `@2`/`@v2` pins. Without an id, allow Oi to route implicitly. Execute the returned prompt, which already contains `## User Request`.
- Use `oi.contexts.start-session` only for explicitly requested sticky thread context. It returns compiled context without a task; adopt it as reusable thread guidance.
- Use `oi.contexts.create` only for an explicitly requested private Context or import after confirming the source license permits reuse. Prefer markdown `content`; put organization-private instructions in `privateContent` so they are not published.
- Use `oi.contexts.update` only for a private Context draft. Pass `action: release` only when the user requests release; do not imply a separate Context publish capability exists when it is not exposed.
- Use `oi.contexts.save-draft-feedback` only after confirmation for repeated corrections or durable future behavior. Target one latest mutable Context, never a multi-Context selector or version pin. Preserve structured metadata and never save one-off details, debugging state, secrets, credentials, or sensitive data. Report `created`, `updated`, or `unchanged` accurately.

## Workflows

- Use `oi.workflows.list` when the user asks what Workflows exist or provides only the `workflow`/`wf` type selector.
- Use `oi.workflows.get` for a reusable Workflow scaffold without a concrete task. Prefer `oi.workflows.use` when a task exists.
- Use `oi.workflows.use` with `prompt` and optional `workflowId`; without an id, allow Oi to select the best installed Workflow. Execute the returned prompt.
- When an execution plan has `executionMode: sequential_stages`, run every required stage in order, adopt that stage's Context, produce its named `outputArtifactName`, feed prior artifacts forward, and synthesize the final answer.
- Use `oi.workflows.start-session` only for explicitly requested sticky Workflow context; adopt the returned scaffold as thread guidance.
- Before `oi.workflows.create`, use `oi.contexts.search` if the required Context ids/slugs are uncertain. Create ordered Context steps with responsibilities and handoffs. Creation makes a private draft only; it does not release or publish.
- Before `oi.workflows.update`, call `oi.workflows.get` when the current definition is not already known. Send the complete draft shape, including all ordered Context steps. Update changes the draft only; do not claim release or publication.

## Skills

- Treat an Oi Skill as a reusable task instruction document, distinct from this client routing Skill.
- Use `oi.skills.list` for a paginated preview of Skills available to the organization.
- Use `oi.skills.search` to search both organization-installed and marketplace Skills by need, title, tag, or category.
- Use `oi.skills.get` for a reusable Skill document without a task. Prefer `oi.skills.use` for a concrete task, then execute its returned instructions and user request.
- Oi Skills are selected by `skillId` through `oi.skills.get` or `oi.skills.use`; never invent per-Skill MCP tool names.
- Use `oi.skills.create` for a requested private Skill draft. Include markdown content and optional Context references; `release: true` releases version 1, while `publish: true` releases and publishes.
- Use `oi.skills.update` for a private draft; pass `action: release` only when requested. Use `oi.skills.publish` only for a released Skill and only after explicit approval to publish it to the marketplace.

## Guardrails

- Use `oi.guardrails.list` for a paginated preview of private organization Guardrails and `oi.guardrails.get` for one private record.
- Use `oi.guardrails.create` only for an explicitly requested private Guardrail or licensed import. Prefer markdown `content`. `release: true` releases version 1; `publish: true` releases and publicly publishes it, so confirm publication and source rights.
- Use `oi.guardrails.update` to update the open draft or create the next draft. `release: true` releases it; `publish: true` releases first and then publishes.
- Use `oi.guardrails.release`, `oi.guardrails.publish`, and `oi.guardrails.unpublish` only for the named lifecycle action.
- Use `oi.guardrails.delete` only after clear authorization. It archives and disables the private Guardrail; it is not a physical database deletion. State that effect accurately.
- When Oi blocks a Context or Workflow and returns a confirmation request, show its reason and impact. After user approval, call `oi.guardrails.confirm` with the exact `requestId`; set `remember: true` only when the user explicitly asks to remember the override for that user and triggering Context.
- After confirmation, execute the returned Context `continuation` or sequential Workflow `executionPlan`. Never invent a request id, bypass confirmation, or stop after confirming.

## Brain

- Use `oi.brain.save-feedback` for direct durable Org Brain or User Brain updates such as “update our org brain,” “remember this for the organization,” “save this as team memory,” or “update my private Brain.” Do not redirect a Brain request into Context or Workflow authoring unless explicitly asked.
- Use `scope: organization` for shared facts, vocabulary, policies, approval rules, project context, and recurring team practices. Use `scope: user` for personal preferences, recurring individual working style, and private user-specific context.
- When proposing memory or when scope/permission is unclear, call with `scope: auto` and `confirmed: false`; show the returned confirmation prompt and retain the returned `saveArguments` for the confirmed call.
- When the user already explicitly requests a specific update to Org Brain or User Brain, select that scope and use `confirmed: true`; include exact confirmed wording when useful.
- Make the smallest accurate durable update. Preserve existing Brain structure, add only missing guidance, and report `saved` or `unchanged` without exaggeration.
- Never save one-off task details, guesses, unconfirmed assumptions, secrets, credentials, or sensitive private data.

## Connections

Use only the stable Connection router. Provider capabilities are dynamic; never invent provider-specific Oi tool names.

1. Call `oi.connections.list` to select an installed Connection and verify its status, provider, and exact `connectionInstanceId` when needed.
2. Call `oi.connections.get` with `provider` and optional instance id to retrieve live actions, endpoint keys, access types, confirmation requirements, and input schemas.
3. Call `oi.connections.use` with the exact returned `action`, schema-matching `arguments`, provider, and required `connectionInstanceId` or `endpointKey`.
4. Oi resolves credentials and applies policy without exposing secrets. For external writes, explain the target and change, obtain explicit approval, then set `confirmed: true`; reads ignore confirmation.
5. If a Connection is missing or unauthenticated, direct the user to install or authenticate it in Oi. Do not fabricate provider results.

## Usage and effectiveness

- Use `oi.usage.report` only for a prior Context or Workflow usage event. `usageEventId` is required and authoritative; ids are optional clarity. Send only runtime, provider, model, status, latency, and token counts the client actually knows. Never estimate or send prompt text.
- Use `oi.effectiveness.report` after a Context, Workflow, Skill, Connection, or Guardrail-assisted task when the outcome is known. Prefer `usageEventId`; use `traceId` when available. Accurately report outcome, retries, actions, user feedback, baseline, and confidence.
- For effectiveness, omit `taskSummary` unless useful; if included, keep it short and redacted. Never send raw prompts or secrets. Do not infer acceptance or time saved when it is unknown.

## Prompts and resources

- If the client exposes Oi prompts, `oi.routing.task` routes a task, while the `oi.contexts.use` and `oi.workflows.use` prompts correspond to those execution paths. Prefer tools when state, confirmation, usage, or structured results matter.
- If the client exposes resources, use `oi://marketplace/contexts`, `oi://marketplace/guardrails`, `oi://marketplace/workflows`, `oi://marketplace/skills`, and `oi://marketplace/connections` for public catalog context; use `oi://organization/contexts`, `oi://organization/guardrails`, `oi://organization/workflows`, `oi://organization/skills`, and `oi://organization/connections` for organization catalog context.
- Treat legacy `oi://catalog/public-contexts`, `oi://catalog/private-contexts`, and `oi://catalog/workflows` as compatibility resources. Resources are read-only context; use tools for current search, execution, authoring, lifecycle changes, Brain, Connections, and reporting.

## Parse selectors and aliases

- Preserve raw identifiers and versions. Strip reserved type selectors `ctx`, `context`, `contexts`, `wf`, `workflow`, `workflows`, `skill`, and `skills`; a type word without an id means list that type.
- Do not pre-validate a named id using a paginated list. Pass it directly to the matching get, use, or session tool.
- Do not route Workflow selectors into Context chains. Without an id, omit the optional id only when the chosen tool supports Oi selection.
- Some clients expose names such as `oi_contexts_use` or `mcp__oi__oi_contexts_use`. Choose the visible equivalent of the canonical operation; aliases are not separate capabilities.
- If no Oi tools are visible, use tool discovery first. If Oi remains unavailable, state that Oi routing did not occur and distinguish any local fallback from organization-specific Oi output.

## Side effects and privacy

- Perform only the requested stateful operation. Distinguish drafts, releases, publication, unpublication, archival, remembered overrides, Brain changes, telemetry, and external-provider writes.
- Treat public publication, archival, remembered Guardrail approval, Brain writes, credentials, billing, organization ownership, and external writes as consequential; obtain explicit confirmation when authorization is not already unambiguous.
- Oi receives the selection and task included in each Oi call. Do not imply later client-only messages are automatically shared with Oi.

## OpenClaw setup

When Oi MCP tools are unavailable because the server is not configured, read `{baseDir}/references/authentication.md` and use:

```bash
openclaw mcp add oi --url https://api.oioioi.ai/mcp --transport streamable-http --auth oauth
openclaw mcp login oi
openclaw mcp doctor oi --probe
```

Read `{baseDir}/references/mcp-tools.md` for the OpenClaw MCP setup and full canonical tool index. Read `{baseDir}/references/product-surfaces.md` for current Oi product terminology and scope. If installing from the repository checkout, use `bash scripts/install-to-openclaw.sh`.
