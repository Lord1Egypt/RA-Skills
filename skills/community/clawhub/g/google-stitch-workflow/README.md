# Google Stitch Workflow

Agent-neutral ClawHub skill bundle for using Google Stitch through the verified MCP surface.

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

## Quick start

1. Read [`SKILL.md`](./SKILL.md).
2. Inspect the project and target screen before editing.
3. Generate one screen or make one small edit.
4. Review the visual result immediately.
5. Move to code only after one canonical screen direction is accepted.

## Included files

- [`SKILL.md`](./SKILL.md): short primary operating guide intended for the ClawHub overview page
- [`references/complete-operator-manual.md`](./references/complete-operator-manual.md): index for the full v1.8 operator manual
- [`references/sections/`](./references/sections/): focused manual sections for selective loading
- [`references/prompt-structuring.md`](./references/prompt-structuring.md): prompt shaping and repair
- [`references/visual-review-and-artifacts.md`](./references/visual-review-and-artifacts.md): review and traceability guidance
- [`references/redesign-prompt-patterns.md`](./references/redesign-prompt-patterns.md): redesign-oriented prompt patterns
- [`references/local-workflow-conventions.md`](./references/local-workflow-conventions.md): optional aliases, artifacts, and history conventions

## License

ClawHub skills are published under **MIT-0** (MIT No Attribution) by the registry.
