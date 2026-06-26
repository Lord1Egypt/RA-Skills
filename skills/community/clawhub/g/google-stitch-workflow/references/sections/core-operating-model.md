---
name: google-stitch-workflow
version: 1.8.0
description: Use when working with Google Stitch through a disciplined MCP-first workflow. Prefer this skill for project inspection, controlled screen generation and editing, prompt structuring, and failure recovery.
---

# Google Stitch Workflow

> **v1.8.0 — structure-first Stitch workflow.** This version keeps the behavior-tested MCP rules and adds stronger anti-generic design gates: structural fingerprint, honest proof, token discipline, and no decorative fake chrome.

Use Google Stitch as a design exploration and screen-iteration workflow, not as a blind code generator.
The normal loop is: inspect the project, generate or edit one screen, review the visual result, iterate in small steps, and only move to code after one direction is clearly approved.

For greenfield apps, once a screen direction is accepted and exportable code is available in the active environment, use the generated HTML/CSS as the translation base instead of recreating the design from screenshots by hand.

## Workflow

Follow this process when using Stitch:

1. **Check capabilities first**
   - Verify the Stitch MCP server is available in the current environment.
   - Verify authentication works before the first generation or edit call.
   - Confirm which tools are actually present before assuming browser features exist through MCP.
   - Treat MCP installation, auth wiring, and local runtime configuration as environment prerequisites, not as the main output of the skill.

2. **Inspect before changing anything**
   - List projects and screens first.
   - Read the target screen before editing.
   - Confirm whether you are working from an existing generated screen or starting a new direction.

3. **Choose the operation type**
   - `generate` for a new canonical screen
   - `edit` for a focused improvement to an existing screen
   - `variants` for controlled branching from an approved base

4. **Work one screen at a time**
   - Write or rewrite the prompt before acting.
   - Make one short generation or one constrained edit.
   - Prefer preservation-oriented prompts that specify what must stay the same.

5. **Review the visual output immediately**
   - Prefer preview-first loops.
   - Inspect the actual screenshot artifact, not only the textual response from Stitch.
   - Compare the screenshot against a small acceptance checklist before deciding whether to edit or accept.
   - Check that the structure is product-specific, not just centered headings and repeated generic cards.
   - Reject invented proof, decorative fake chrome, and visuals that do not clarify the task.
   - Ask the user to choose using human descriptions, not opaque screen IDs.
   - Do not jump to code retrieval if the visual direction is still unclear.

6. **Move to code only after approval**
   - Fetch code or export artifacts only after the user accepts the screen direction.
   - Choose the transfer strategy from the user's real target stack before implementing.
   - For real app delivery, require parity checks between the accepted Stitch design and the implementation.

## Tools

This skill is written for a capability-first Stitch setup.

The skill assumes Stitch is already available or that the user explicitly wants help validating setup.
Do not turn every Stitch task into a setup task.

Baseline MCP tools usually include:

- `list_projects`
- `get_project`
- `list_screens`
- `get_screen`
- `create_project`
- `list_design_systems`
- `create_design_system`
- `update_design_system`
- `apply_design_system`
- `generate_screen_from_text`
- `edit_screens`
- `generate_variants`

Optional wrapper tools may include:

- `fetch_screen_image`
- `fetch_screen_code`
- `generation_status`
- `list_generations`
- `get_screen_image`
- `get_screen_code`
- `build_site`

Do not assume the browser UI, public marketing materials, and MCP surface expose the same operations.
Treat wrapper enhancements as optional until the active environment proves they exist.

Important retrieval nuance:

- `list_screens` and `get_screen` often already expose `screenshot.downloadUrl` and `htmlCode.downloadUrl`
- wrapper code/image tools are conveniences, not the only valid handoff path
- `build_site` and similar site generators are web-oriented helpers, not direct Flutter/React Native handoff tools

## When to use this skill

Use this skill when the task involves one or more of:

- inspecting Stitch projects and screens before making changes
- generating a new screen from a text prompt
- refining an existing generated screen with small, controlled edits
- organizing a multi-screen redesign effort without losing revision history
- converting vague design requests into structured prompts
- deciding when to stay in Stitch and when to move to implementation code

## When not to use this skill

Do not use Stitch as the primary path when the real task is:

- implementing production UI code directly
- making deterministic pixel-perfect edits to an existing coded screen
- redesigning an app without reliable reference screens or screenshots
- planning an entire product in one giant prompt
- evaluating engineering feasibility without a prior visual direction

Important nuance:

- for an existing coded app, Stitch is usually best as a design reference and iteration surface
- for a new app with no established implementation, accepted Stitch exports can be the fastest way to seed the first real UI structure

## Quick operating rules

- **rewrite before acting** — before any `generate`, `edit`, or `variants` call, rewrite the user request into a stronger design prompt or a tighter edit intent
- **inspect before editing** — always inspect the project and target screen first; verify whether the screen is actually generated content (if `htmlCode` exists, it's more likely editable)
- **pick the operation class first** — decide whether this pass is `generate`, `edit`, or `variants`; do not blur exploration, refinement, and branching in one move
- **use the project design system on purpose** — if the project already has a good design system, reuse it explicitly before generating sibling screens or major revisions
- **work one screen at a time** — one short generation followed by controlled edits; keep one screen as the unit of iteration
- **keep prompts short, explicit, and preservation-oriented** — start with the smallest prompt that can produce a useful screen
- **review the visual result before the next major step** — review screenshots or visual artifacts immediately after each generate/edit; ask the user to choose using a human description, not an opaque screen ID
- **trust screenshots over status text** — Stitch may report that constraints were satisfied even when the image still misses visible content; inspect the screenshot before accepting
- **move to code only after one direction is clearly accepted** — confirm the visually reviewed canonical screen before export or translation; move to code only after the screen family is coherent
- **treat exports as seeds, not finished apps** — generated code can preserve hierarchy and tokens, but production work still needs data, state, accessibility, responsiveness, and tests
- **expect new screen IDs after edits** — MCP `edit_screens` may create a revised screen instead of mutating the original; report and continue from the new screen ID
- **stop repeating failing payloads** — do not brute-force retries with the same parameters
- **recover from unavailable edits deliberately** — if `edit_screens` returns a transient service error, check `list_screens` for a newly created screen; if none exists, either retry once with a smaller edit or regenerate a new candidate with the failed constraints moved to the top of the prompt
- **act as creative director** — Stitch is the designer, you provide the direction
- **define what must NOT change** — the single most important iteration rule: tell Stitch what to keep, not just what to change
- **hub-first for multi-screen projects** — generate a hub screen first, derive all other screens via edit, never fresh generate siblings
- **report state after every pass** — after each generate/edit/variants step, report the project id, screen id, artifact location if any, a short design judgment, and the next recommended move
- **enforce translation parity gates** — for real app delivery, require visual + state + platform parity checks before declaring success

## Advanced guidance

This skill intentionally separates three concerns that are often conflated:

- verified MCP capabilities in the current environment
- browser-only Stitch product features
- optional local workflow conventions that improve traceability

## Pre-flight probe — do this before first generation

**Critical:** Do NOT use generic MCP schema discovery to verify Stitch is working. Schema discovery in Stitch MCP
can return a circular-reference error (`can't resolve reference #/$defs/ScreenInstance`) even when
every tool call succeeds. This is a known MCP server-side issue, not an auth or connectivity failure.

**The reliable handshake is a direct tool call through the active agent runtime:**

```bash
# Mavis / MiniMax Agent example
mavis mcp call stitch list_projects '{}'

# mcporter-style example
mcporter call stitch.list_projects '{}'
```

For other agents, call the equivalent `stitch.list_projects` tool directly. If it returns successfully, Stitch is operational. Proceed.

Then probe optional generation tracking tools through the same runtime adapter:

```bash
# Mavis / MiniMax Agent examples
mavis mcp call stitch generation_status '{"operation": "last"}'  # expected to fail in some environments
mavis mcp call stitch list_generations '{"projectId": "<your-project-id>"}'  # same

# mcporter-style examples
mcporter call stitch.generation_status '{"operation": "last"}'
mcporter call stitch.list_generations '{"projectId": "<your-project-id>"}'
```

If both return "tool not found", add to your operating state: "No generation_status / list_generations — list_screens polling is the only tracking path".

Calibrate latency only when useful: make one trivial generate call to observe the timeout threshold.

Some wrappers auto-detect project IDs; still confirm the active project before editing or generating.

## Runtime adapters

This skill is agent-neutral. It requires access to a configured Stitch MCP server, not a specific agent runtime.

Use whichever adapter is available:

- Mavis / MiniMax Agent: `mavis mcp call stitch <tool> '<json>'`
- mcporter: `mcporter call stitch.<tool> '<json>'`
- Codex, Claude, OpenClaw, Cursor, or another agent: use that runtime's MCP tool-call interface for the same Stitch tool names

Do not make `mavis`, `mcporter`, `stitch-mcp-auto`, or wrapper image/code helpers a hard requirement unless the local environment or user explicitly chooses that path.

## Capability-first startup handshake

At the start of a Stitch session, do a quick environment and capability handshake before designing:

1. verify the Stitch MCP server is available in the active environment
2. verify authentication is valid before first generation/edit call
3. run the pre-flight probe above to confirm Stitch is responding and which tracking tools exist
4. classify the confirmed tool surface:
   - baseline MCP: `list_projects`, `get_project`, `list_screens`, `get_screen`, `create_project`, `generate_screen_from_text`, `edit_screens`
   - design-system MCP: `list_design_systems`, `create_design_system`, `update_design_system`, `apply_design_system`
   - optional tracking (often missing): `generation_status`, `list_generations`
   - optional wrapper: `fetch_screen_image`, `fetch_screen_code`, `get_screen_image`, `get_screen_code`, `build_site`
5. if baseline tools are missing, stop and fix environment state first
6. if optional tracking tools are missing, record: *"use list_screens polling only"* — do not assume generation_status/list_generations will work

If design-system tools are present, inspect them early:

6. list project design systems and confirm whether one should be reused
7. prefer applying or updating the existing design system before generating sibling screens from scratch

For environments that use `mcporter`, a typical first-time setup path is:

```bash
mcporter config add stitch --command "npx" --args "-y stitch-mcp-auto"
```

Treat setup commands as environment-specific and require explicit user confirmation before changing runtime config.
Only enter setup mode when Stitch is not configured or the user explicitly asks for setup help. If the user only wants design work, do not proactively switch into setup mode unless missing capabilities block the task.

If a local Stitch proxy/CLI is installed, useful optional commands may include:

- `doctor` for auth/config health checks
- `serve -p <projectId>` for local screen preview
- `site -p <projectId>` or `build_site` for web-oriented route generation

Treat these as environment-specific helpers, not part of the guaranteed upstream Stitch MCP contract.

## Hard approval gates

- do not fetch or export final code until the user has approved a visual direction
- when `fetch_screen_image` is available, use it to force a preview-first loop before code retrieval
- when `fetch_screen_code` is available, call it only after explicit user approval
- when wrapper image/code tools are absent, use `get_screen` and extract `screenshot.downloadUrl` / `htmlCode.downloadUrl` from the returned screen
- treat `create_project` as a privileged action: ask before creating new cloud resources

## Design-to-code parity gates (critical)

When the goal is a real app, add these gates before considering the task complete:

1. **Visual fidelity gate**  
   Verify hierarchy, spacing rhythm, typography roles, color intent, component radius, and breakpoints against the accepted Stitch screen.
   Validate on the target device or viewport, including status bars, safe areas, browser chrome, tab bars, and native bottom navigation.
2. **State/interaction gate**  
   Verify loading, empty, error, disabled, and interaction states (hover/focus/pressed or platform equivalents).
3. **Target parity gate**  
   If multiple targets are in scope, confirm equivalent structure and behavior; document intentional differences explicitly.
4. **Diff-and-repair gate**  
   Produce a drift list (`missing`, `mismatched`, `intentional`) and apply scoped fixes only. Avoid broad rewrites.

If a gate fails, return to constrained edit prompts and iterate one screen at a time.

## Non-multimodal agent path (text-first transfer)

If the implementation agent cannot reliably inspect images, do not skip Stitch; switch to a text-first transfer path:

1. treat `DESIGN.md` as the style authority
2. retrieve code/export artifacts only after visual approval gates are passed by a reviewing agent or human
3. translate using structure/tokens/components from export + `DESIGN.md`, not from screenshot memory
4. run a drift checklist in text form (`missing`, `mismatched`, `intentional`)
5. iterate with constrained patch prompts tied to that checklist

This keeps quality acceptable even when the coding agent is text-centric.

Use this execution sequence:

1. request approved design artifacts from Stitch-capable context:
   - accepted screen output
   - `DESIGN.md`
   - screen metadata (`width`, `height`, `deviceType`)
   - export/code artifact
2. build a target-screen implementation plan from those artifacts only
3. map design tokens/roles into project theme tokens before broad refactors
4. apply scoped patches per screen/section
5. emit a drift log after each pass:
   - `missing`: exists in Stitch, absent in implementation
   - `mismatched`: present but deviates materially
   - `intentional`: deliberate divergence with reason
6. iterate until high-impact drift is closed

## Research-backed skill upgrade loop

When improving this skill from external sources:

1. ingest high-signal sources (videos, docs, release notes)
2. extract only reusable transfer rules (not source trivia)
3. require at least two examples before promoting a new rule
4. encode rules as objective pass/fail checks where possible
5. write changelog entries with concrete behavioral impact
6. revalidate dated claims about models, pricing, beta features, and browser-only behavior before turning them into operating rules

Keep examples, demos, and hype in references unless they change agent behavior. The main `SKILL.md` should contain only rules the next agent can safely execute.

## Complete process order

This is the recommended sequence from blank canvas to accepted design:

1. **Empathy** → Who is the user? What should they feel?
2. **Creative direction** → Concrete vocabulary, metaphors, not abstract words
3. **Prompt with direction** → Describe what the site *is* and how it *feels*
4. **Design system** → Set color hierarchy, font hierarchy, corner radius in DESIGN.md
5. **Layout** → Use variants (Explore level) with scoped layout prompts
6. **Copywriting** → Generate real copy matching the creative brief
7. **Iterate** → One screen at a time, scoped refinements
8. **Export/code** → Only after the direction is clearly accepted

**Before step 1, create a feature matrix.** Map which features appear on which screen. Only start generating once the coverage is clear — this makes every generate/edit call a deliberate execution step, not a discovery. Three focused screens you've thought through beat ten screens you discover issues with during generation.

At the start of each pass, choose one operation class on purpose:

- `generate` for a new canonical screen
- `edit` for a focused improvement to an existing screen
- `variants` for controlled branching from a base direction

Skip steps and you'll iterate more later. Follow them and each step builds on the last.

---
