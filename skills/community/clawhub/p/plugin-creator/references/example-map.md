# In-Repo Example Map

When you are unsure how OpenClaw expects a plugin to be written, compare against these existing examples.

## `extensions/observability-lab/`

Composite example (local experimental plugin).

Notes:

- This is the primary hands-on example for this skill.
- It may not exist in every upstream branch or version.
- Check whether it exists in the current workspace before relying on it.
- This skill also ships a source snapshot: `references/observability-lab-source/`

Good for learning:

- how to split plugin directories
- local `api.ts` barrel usage
- `api.registerCommand(...)`
- `api.registerTool(...)`
- `api.on(...)`
- declaring `skills` in `openclaw.plugin.json`
- the interaction between plugin skills, slash commands, typed hooks, and tools

## `extensions/open-prose/`

Good for learning:

- a plugin that mounts a skill through the manifest only
- the minimum plugin-shipped skill path

## `extensions/lobster/`

Good for learning:

- `api.registerTool(..., { optional: true })`
- plugin tools that intentionally return `null` in some paths

## `extensions/llm-task/`

Good for learning:

- `optional: true`
- local `api.ts` barrel style

## Built-in references in this skill

To avoid examples drifting with upstream changes, you can rely on the fixed references bundled with this skill:

- `references/plugin-layout-and-registration.md`
- `references/hooks-and-events.md`
- `references/pitfalls-and-debugging.md`
- `references/observability-lab-source/` (experimental plugin source snapshot)

## Suggested learning order

1. Start with `extensions/observability-lab/`
2. Then branch by question:
   - plugin skill: `extensions/open-prose/`
   - optional tool: `extensions/lobster/`, `extensions/llm-task/`

## Recommended comparison method

Do not read only one file. Compare at least:

- `package.json`
- `openclaw.plugin.json`
- `index.ts`
- relevant subdirectories (`commands/`, `hooks/`, `tools/`, `skills/`)
- test files

That is how you see all four layers together:

- manifest declaration
- runtime registration
- directory responsibility
- validation strategy
