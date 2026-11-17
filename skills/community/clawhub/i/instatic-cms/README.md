# Instatic CMS Skill

An [OpenClaw](https://docs.openclaw.ai) skill for operating a self-hosted [Instatic](https://github.com/corebunch/instatic) instance: install modes, the full admin API, the content model, canvas editing, publishing, design tokens, automation surfaces, and verification discipline.

Knowledge compiled against Instatic v0.0.20; later versions can drift. The skill tells the agent to re-verify against a pinned checkout before trusting behavior.

## Layout

```text
README.md
SKILL.md                index: quick reference, critical rules, workflow
instatic-cms/
  install.md            compose modes, image/platform notes, upgrade procedure
  database.md           engines, dialect rules, storage model, boot, health
  content-model.md      tables, fields (16 types), templates/VCs/layouts, loops, forms
  api.md                every admin endpoint grouped by function, capability gates, env vars
  styling.md            design tokens, class registry, four-bundle CSS pipeline
  publishing.md         draft-to-publish pipeline, hole semantics, export vs deploy, imports, TLS
  workspaces.md         admin UI: canvas modes, content/data/media workspaces, spotlight
  automation.md         REST / AI agent / MCP / plugin automation doors
  verification.md       evidence bar: liveness, publish checks, UI flow tests
```

## Install as a skill

Clone this repo into your agent skills directory (for example as `instatic-cms` inside `~/.openclaw/workspace/skills/`). `SKILL.md` sits at the package root and reaches its support files through the `instatic-cms/` folder, so keep the structure as-is when you copy. No scripts, pure markdown.

## Authoring method

- Everything was extracted from the pinned `v0.0.20` source: route tables and handler doc-headers in `server/handlers/cms/`, union definitions in `src/core/data/schemas.ts`, `src/core/capabilities.ts`, and the upstream `docs/` tree.
- Two upstream-prose vs source discrepancies are documented in the skill itself (capability count; field-type taxonomy). Source was treated as the authority.
- No deployment-specific facts: the skill is written generic to any self-hosted Instatic.

MIT-style intent: this is our documentation work about an MIT-licensed product; the upstream repo governs its own licensing questions.
