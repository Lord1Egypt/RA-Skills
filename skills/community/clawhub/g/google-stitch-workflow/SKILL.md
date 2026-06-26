---
name: google-stitch-workflow
version: 1.8.0
description: Use when working with Google Stitch through a disciplined MCP-first workflow. Prefer this skill for project inspection, controlled screen generation and editing, prompt structuring, and failure recovery.
---

# Google Stitch Workflow

Use Google Stitch as a controlled design exploration and screen-iteration surface, not as a blind code generator.

The normal loop is:

1. Inspect the project and available screens.
2. Generate or edit one screen.
3. Review the actual visual artifact.
4. Iterate in small preservation-oriented steps.
5. Move to code only after one direction is clearly accepted.

For full details, edge cases, and expanded recipes, read [`references/complete-operator-manual.md`](references/complete-operator-manual.md) as an index and load only the focused reference needed for the task.

## When To Use

Use this skill when the task involves:

- inspecting Stitch projects and screens before making changes
- generating a new screen from a structured text prompt
- refining generated screens with small controlled edits
- organizing a multi-screen redesign without losing revision history
- converting vague design requests into stronger Stitch prompts
- deciding when to stay in Stitch and when to move into production code

Do not use Stitch as the primary path when the real task is:

- deterministic code-side UI repair in an existing app
- pixel-perfect implementation fixes that do not need design exploration
- whole-product planning in one giant prompt
- assuming browser-only Stitch features exist through MCP

## Startup Handshake

Run a capability-first check before the first generation or edit.

Critical: do not use generic MCP schema discovery as the reliability test for Stitch. Some Stitch MCP environments return schema discovery errors even when direct tool calls work.

Use your agent runtime's direct MCP call mechanism instead:

```bash
# Mavis / MiniMax Agent example
mavis mcp call stitch list_projects '{}'

# mcporter-style example
mcporter call stitch.list_projects '{}'
```

For other agents, call the equivalent `stitch.list_projects` tool directly. If `list_projects` succeeds, Stitch is operational.

Then probe optional tracking tools with the same runtime adapter:

- `generation_status` with `{"operation": "last"}`
- `list_generations` with `{"projectId": "<project-id>"}`

If the optional tracking calls fail with "tool not found", record that this environment uses `list_screens` polling only.

Only enter setup mode when Stitch is not configured or the user explicitly asks for setup help. Some wrappers auto-detect project IDs; still confirm the active project before editing or generating.

Expected baseline tools:

- `list_projects`
- `get_project`
- `list_screens`
- `get_screen`
- `create_project`
- `generate_screen_from_text`
- `edit_screens`

Optional tools:

- `list_design_systems`
- `create_design_system`
- `update_design_system`
- `apply_design_system`
- `generate_variants`
- `generation_status`
- `list_generations`
- `fetch_screen_image`
- `fetch_screen_code`
- `get_screen_image`
- `get_screen_code`
- `build_site`

If baseline tools are missing, stop and fix environment state first. If optional tools are missing, continue with the baseline workflow.

## Runtime Adapters

This skill is agent-neutral. It requires access to a configured Stitch MCP server, not a specific agent runtime.

Use whichever adapter is available:

- Mavis / MiniMax Agent: `mavis mcp call stitch <tool> '<json>'`
- mcporter: `mcporter call stitch.<tool> '<json>'`
- Codex, Claude, OpenClaw, Cursor, or another agent: use that runtime's MCP tool-call interface for the same Stitch tool names

Do not make `mavis`, `mcporter`, `stitch-mcp-auto`, or wrapper image/code helpers a hard requirement unless the local environment or user explicitly chooses that path.

## Operating Rules

- Rewrite the user request into a stronger design prompt before any generate, edit, or variants call.
- Inspect before editing: list projects/screens and read the target screen first.
- Work one screen at a time.
- Keep prompts short, explicit, and preservation-oriented.
- Pick the screen structure before asking for color, type, motion, or visual polish.
- Use supplied proof only: do not invent metrics, testimonials, customer logos, prices, or social proof to make a generated screen feel complete.
- Define what must stay unchanged, not only what should change.
- Review screenshots or visual artifacts before the next major step.
- Ask users to choose using human descriptions, not opaque screen IDs.
- Expect `edit_screens` to create a revised screen instead of mutating the original.
- Do not retry the same failing payload during a polling window.
- Move to code only after one canonical screen direction is accepted.
- Treat generated code as a seed, not a finished production implementation.

Read [`references/prompt-structuring.md`](references/prompt-structuring.md) when the prompt is vague, too long, or producing generic results.

## Parameter Discipline

Stitch payloads are parameter-sensitive.

- `deviceType`: use uppercase `"MOBILE"` or `"DESKTOP"` for generation. For `edit_screens`, omit `deviceType` entirely unless the active schema proves otherwise.
- `selectedScreenIds`: use bare screen IDs as an array, not full resource names.
- `modelId`: use only identifiers exposed by the active MCP schema.
- Prompt length: keep prompts short, usually under about 500 characters.

Example edit payload:

```json
{
  "projectId": "8675077932533356979",
  "selectedScreenIds": ["69b3228b6c5f4b9f9efceea4b6a30168"],
  "prompt": "Make the primary button darker. Keep everything else identical."
}
```

## Timeout Recovery

The HTTP timeout is not the same as generation failure. Stitch may drop the connection while the server-side generation continues.

After a `generate_screen_from_text` timeout:

1. Record the timeout moment.
2. Wait 60 seconds.
3. Call `list_screens` with the project ID.
4. Inspect for a new screen matching the intended device and prompt.
5. Repeat every 60 seconds.
6. Declare failure only after about 3 minutes for mobile or 10 minutes for desktop.
7. Retry only after the polling window, and use an adjusted prompt or device type.

Prefer mobile-first generation when possible. Desktop generations can take significantly longer and may need browser-side fallback after repeated MCP failures.

For the complete failure matrix, read [`references/sections/mcp-api-and-failure-recovery.md`](references/sections/mcp-api-and-failure-recovery.md#failure-handling).

## Visual Review Gate

Never accept a Stitch result based only on text status. Inspect the actual visual output.

Before asking for approval or moving to code, check:

- screen hierarchy is clear
- primary action is obvious
- the screen has a structural fingerprint beyond centered headings and generic cards
- typography scale feels intentional
- spacing and density match the product type
- responsive direction is plausible for the target device
- important content is not cropped, hidden, or visually ambiguous
- the result is more specific than a generic SaaS mockup
- no fake browser, phone, IDE, or code-window chrome is used as decoration
- any visible metrics, testimonials, logos, prices, or claims came from the user or are clearly placeholders

Read [`references/visual-review-and-artifacts.md`](references/visual-review-and-artifacts.md) for screenshot handling, traceability, and review artifacts.

## Move To Code

Fetch code or export artifacts only after a visual direction is accepted.

Choose the transfer strategy from the real target stack:

- Web app: use exported HTML/CSS as the structure and token seed when available.
- Existing app: preserve established routing, data boundaries, and component conventions.
- Native or Flutter app: translate layout, tokens, and interaction intent rather than copying web-specific code.

Before calling implementation complete, verify parity:

- visual parity against the accepted Stitch screen
- state parity for loading, empty, error, and success states
- responsive parity across the target breakpoints
- accessibility and keyboard behavior where applicable
- production data, routing, and auth boundaries still work

Read [`references/local-workflow-conventions.md`](references/local-workflow-conventions.md) for optional artifact naming and traceability conventions.

## Workflow Recipes

Use these as the default recipes:

- Inspect before editing: list projects, list screens, read target screen, then decide generate/edit/variant.
- Generate first, then refine: create one canonical candidate, review it, then make small edits.
- Preview-first approval loop: show visual options and ask for a human-readable choice before fetching code.
- Redesign from reference: describe the existing screen, preserve product constraints, and request a specific direction.
- Full app redesign: generate a hub screen first, then derive related screens from that hub.

For expanded recipes, read [`references/sections/workflow-recipes.md`](references/sections/workflow-recipes.md).

## Reference Map

- [`references/complete-operator-manual.md`](references/complete-operator-manual.md): index for the full v1.7 operator manual
- [`references/sections/core-operating-model.md`](references/sections/core-operating-model.md): startup, runtime adapters, approval gates, and core operating model
- [`references/sections/mcp-api-and-failure-recovery.md`](references/sections/mcp-api-and-failure-recovery.md): MCP boundaries, parameter discipline, timeouts, and recovery
- [`references/sections/export-and-code-translation.md`](references/sections/export-and-code-translation.md): export, Fidelity Pack, parity, and implementation handoff
- [`references/prompt-structuring.md`](references/prompt-structuring.md): prompt shaping and repair patterns
- [`references/redesign-prompt-patterns.md`](references/redesign-prompt-patterns.md): redesign-specific prompt recipes
- [`references/visual-review-and-artifacts.md`](references/visual-review-and-artifacts.md): screenshot review and artifact handoff
- [`references/local-workflow-conventions.md`](references/local-workflow-conventions.md): optional local aliases, artifact paths, and history conventions
