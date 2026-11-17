---
name: google-stitch-workflow
version: 1.9.1
description: Use when working with Google Stitch through a disciplined MCP-first workflow. Prefer this skill for project inspection, controlled screen generation and editing, prompt structuring, and failure recovery.
---

# Google Stitch Workflow

> **v1.9.1 — field lessons.** Small text edits may not persist (verify with `download_file`), API lists lag (keep response IDs), timed-out calls can finish later (check the web UI before regenerating), and invented UI claims are review defects.
>
> **v1.9.0 — current official Stitch MCP surface.** Tool lists, parameters and the Claude Code adapter now match the official Stitch MCP server as checked on 2026-11-08 (`download_file`, `generate_variants` options, DESIGN.md upload, `delete_project`). Wrapper-only tools are marked unverified.
>
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

Official Stitch MCP tools (checked against the live schema on 2026-11-08):

- read: `list_projects`, `get_project`, `list_screens`, `get_screen`, `list_design_systems`, `download_file`
- generate/edit: `create_project`, `generate_screen_from_text`, `edit_screens`, `generate_variants`
- design system: `create_design_system`, `update_design_system`, `apply_design_system`, `upload_design_md`, `create_design_system_from_design_md`
- destructive: `delete_project`

Tools from older wrapper setups that the official server does not expose (treat as unverified): `fetch_screen_image`, `fetch_screen_code`, `get_screen_image`, `get_screen_code`, `generation_status`, `list_generations`, `build_site`.

Do not assume the browser UI, public marketing materials, and MCP surface expose the same operations.

Important retrieval nuance:

- `list_screens` and `get_screen` return `screenshot.name` and `htmlCode.name`; pass those to `download_file` to get the image or HTML
- do not fetch `downloadUrl` directly: it needs credentials and returns a JSON wrapper
- site generators are web-oriented helpers, not direct Flutter/React Native handoff tools

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
- **check what an edit returned** — a structural `edit_screens` change usually returns new screen IDs (continue from those); a small text edit can come back as DOM operations on the same screen and not be saved, so verify it with `download_file`
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

**The reliable handshake is one direct `list_projects` call through the active agent runtime** (for example `mcp__stitch__list_projects` in Claude Code). If it returns successfully, Stitch is operational. Proceed.

Its output is very large (full design theme and `designMd` per project). Summarize it with `jq` or a short script instead of reading it whole:

```bash
jq -r '.projects[] | [.name, .title, (.screenInstances | length), .updateTime] | @tsv' list_projects.json
```

The official server has no generation-tracking tools; `list_screens` / `get_screen` polling is the tracking path.

Calibrate latency only when useful: make one trivial generate call to observe the timeout threshold.

Confirm the active project with the user before editing or generating.

## Runtime adapters

This skill is agent-neutral. It requires access to a configured Stitch MCP server, not a specific agent runtime. Tool names are the same everywhere; only the call syntax differs.

- Claude Code: once the user has added the server (for example a user-scope HTTP MCP server named `stitch` at `https://stitch.googleapis.com/mcp`), tools appear as `mcp__stitch__<tool>`. Load deferred tool schemas before the first call and read the parameters from them.
- Codex, Cursor, OpenClaw, or another agent: use that runtime's MCP tool-call interface for the same tool names.
- CLI-style MCP clients: call `stitch.<tool>` with a JSON argument object.

Credentials stay in the runtime's MCP configuration, set by the user. Never print, echo, paste, or store an API key.

## Capability-first startup handshake

At the start of a Stitch session, do a quick environment and capability handshake before designing:

1. verify the Stitch MCP server is available in the active environment
2. verify authentication is valid before first generation/edit call
3. run the pre-flight probe above to confirm Stitch is responding and which tracking tools exist
4. classify the confirmed tool surface:
   - read: `list_projects`, `get_project`, `list_screens`, `get_screen`, `list_design_systems`, `download_file`
   - generate/edit: `create_project`, `generate_screen_from_text`, `edit_screens`, `generate_variants`
   - design system: `create_design_system`, `update_design_system`, `apply_design_system`, `upload_design_md`, `create_design_system_from_design_md`
   - destructive: `delete_project` (only after explicit user confirmation of the exact project)
5. if read tools are missing, stop and fix environment state first
6. if a wrapper-only tool (`fetch_screen_image`, `generation_status`, ...) is absent, that is expected; use `download_file` and polling

If design-system tools are present, inspect them early:

6. list project design systems and confirm whether one should be reused
7. prefer applying or updating the existing design system before generating sibling screens from scratch

Setup is the user's job: connecting the Stitch MCP server and its credential happens in the user's own runtime configuration, following that runtime's documentation. Do not install packages, run setup commands, or edit runtime config for the user without explicit confirmation of the exact command.
Only enter setup mode when Stitch is not configured or the user explicitly asks for setup help. If the user only wants design work, do not proactively switch into setup mode unless missing capabilities block the task.

## Hard approval gates

- do not fetch or export final code until the user has approved a visual direction
- review the screenshot first (`download_file` with `screenshot.name`) to force a preview-first loop before code retrieval
- download HTML (`download_file` with `htmlCode.name`) only after explicit user approval of the visual direction
- treat `create_project` as a privileged action: ask before creating new cloud resources
- treat `delete_project` as destructive and irreversible: name the project by title and ID and get an explicit yes first

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
