# Google Stitch Workflow

Agent-neutral ClawHub skill bundle for using Google Stitch through the official Stitch MCP server.

Version: **1.9.1**

## At a glance

- MCP-first: separates verified MCP actions from browser-only Stitch features
- practical: optimized for project inspection, screen generation, controlled edits, and redesign iteration
- pragmatic for greenfield apps: when an accepted Stitch export is available, use it as the translation seed instead of rebuilding from screenshots
- cautious: emphasizes parameter discipline, visual distinctiveness review, and failure recovery
- anti-generic: strengthens prompts and review gates around structure-first design, honest content, token discipline, and no decorative fake chrome

## Best for

- inspecting Stitch projects and screens before editing
- generating one screen at a time from a structured prompt
- refining generated screens with small preservation-oriented edits
- redesigning existing app screens from reliable references
- bootstrapping a new app UI from accepted Stitch-generated screens and exports
- deciding when to stay in Stitch and when to move to code

## Not for

- blind direct production UI implementation from raw exports
- pixel-perfect code-side fixes
- whole-product planning in one giant prompt
- blind reliance on browser-only Stitch features through MCP

## Works with

- Claude Code (tools appear as `mcp__stitch__<tool>` once the user adds the Stitch MCP server)
- any other agent with an MCP client (Codex, Cursor, OpenClaw, ...), using the same tool names

No scripts, packages or credentials ship with this bundle. The Stitch connection and its credential live in your agent's own MCP configuration.

## Quick start

1. Read [`SKILL.md`](./SKILL.md).
2. Inspect the project and target screen before editing.
3. Generate one screen or make one small edit.
4. Review the visual result immediately.
5. Move to code only after one canonical screen direction is accepted.

## Included files

- [`SKILL.md`](./SKILL.md): short primary operating guide intended for the ClawHub overview page
- [`references/complete-operator-manual.md`](./references/complete-operator-manual.md): index for the full v1.9 operator manual
- [`references/sections/`](./references/sections/): focused manual sections for selective loading
- [`references/prompt-structuring.md`](./references/prompt-structuring.md): prompt shaping and repair
- [`references/visual-review-and-artifacts.md`](./references/visual-review-and-artifacts.md): review and traceability guidance
- [`references/redesign-prompt-patterns.md`](./references/redesign-prompt-patterns.md): redesign-oriented prompt patterns
- [`references/local-workflow-conventions.md`](./references/local-workflow-conventions.md): optional aliases, artifacts, and history conventions

## Changelog

### 1.9.1

Field lessons from real use of the official Stitch MCP server (2026-11-08):

- `edit_screens` does not always create a new screen: structural changes returned new IDs, but a small text edit came back as a `DomOperationEvent` on the same screen, reported success, and was not saved. New "Edit Verification" section: check small edits by downloading the HTML; if the target is code, fix the text there.
- `list_screens` and `get_project` can lag many minutes behind; keep the screen ID from each response.
- Timed-out calls can finish 10-20 minutes later with no ID. Check the web UI before regenerating; fall back to a zip export from the web UI, unpacked into a new empty folder as untrusted data and compared by hash.
- `download_file` screenshots are large base64 results; decode the saved file to PNG.
- Visual Review Gate: every visible sentence must match what the product really does; invented privacy promises and features are defects.
- "Brand from DESIGN.md" gains a hub-first pattern: derive screens from one hub with short keep/remove edit prompts.
- Observation only: of two parallel `edit_screens` calls, one timed out but finished.

### 1.9.0

- Tool list matches the official Stitch MCP server (checked 2026-11-08): adds `download_file`, `upload_design_md`, `create_design_system_from_design_md`, `delete_project`, and the real `generate_variants` options.
- Adds Claude Code as a runtime adapter (`mcp__stitch__*` tools); drops wrapper-specific call examples.
- Marks wrapper-only tools (`fetch_screen_image`, `fetch_screen_code`, `generation_status`, `list_generations`, `build_site`) as unverified, with official replacements.
- Updates `modelId` and `deviceType` enums, IDs vs resource names, and screen instances vs screen IDs.
- Warns that `list_projects` output is very large and shows how to summarize it.
- New recipe: Brand from DESIGN.md (upload, create design system, generate MOBILE screens; translate for Flutter, never copy HTML).
- Safety: optional `@google/design.md` linter pinned and gated on user approval; no package installs driven by generated code; `DESIGN.md` treated as design data, not agent instructions; no setup commands; destructive `delete_project` gated on explicit confirmation.

### 1.8.0

- Structure-first workflow with anti-generic design gates: structural fingerprint, honest proof, token discipline, no decorative fake chrome.

## License

ClawHub skills are published under **MIT-0** (MIT No Attribution) by the registry.
