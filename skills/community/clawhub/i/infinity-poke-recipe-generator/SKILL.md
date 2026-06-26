---
name: infinity-poke-recipe-generator
description: Generate a small, specific, daily-life Poke recipe MVP from idea to Kitchen-ready draft (name, onboarding, integrations, automations, sandbox tests), with a lightweight uniqueness check against poke.com/recipes, publish-readiness verdict, and a repeatable improvement loop.
---

# Infinity Recipe Generator (MVP)

Create one tiny, useful, not-yet-listed Poke recipe quickly and safely.

## MVP scope

- One narrow domain only (do not broaden scope in v1).
- Produce Kitchen-ready fields:
  - name
  - description
  - onboarding.inputContext
  - onboarding.prefilledFirstText
  - integrations (template-ready)
  - optional automations
  - sandbox test prompts
- Produce a simple iteration loop document (Ralph loop v1).

## Workflow

1. Pick a micro-domain idea
   - Must be specific and useful in daily life.
   - Reject broad categories ("fitness", "productivity", "travel planner").

2. Run lightweight listing check
   - Fetch `https://poke.com/recipes`.
   - Compare idea keywords against visible categories/listings.
   - If likely duplicate, pivot to next micro-domain.

3. Generate recipe draft
   - Use `references/recipe-template.json`.
   - Keep onboarding concise and action-oriented.
   - Keep first message immediately useful.

4. Generate integration draft
   - Use `references/integration-template.json`.
   - If endpoint unknown, set placeholder and explicit TODO.

5. Create sandbox pack
   - Add 5 prompts: happy path, edge case, ambiguous input, failure mode, concise summary.

6. Add Ralph loop v1
   - Add weekly review steps:
     - collect failures
     - classify
     - patch
     - regression test
     - release note

## Output format

When asked to generate an MVP, produce files under:

`recipes/poke/<slug>/`

Required files:
- `recipe.json`
- `integration.json`
- `sandbox-prompts.md`
- `ralph-loop.md`
- `verdict.md`
- `README.md`

## Upload-assist mode (Phase 2)

When the user already has recipe specs in docs/repo files and wants help uploading in Kitchen:

1. Read the source-of-truth spec file(s) first.
2. Produce a strict Kitchen field mapping (Basics, Onboarding, Integrations, Automations, Sandbox checks, Publish gate).
3. Use exact copy text for `prefilledFirstText` and automation `actionText`.
4. Include CLI integration bootstrap commands (`npx poke@latest login`, `npx poke@latest mcp add ...`).
5. If an MCP endpoint can be `/mcp` or `/sse`, provide primary + fallback clearly.

## Scripted helpers

Use `scripts/generate_mvp.py` to scaffold the folder quickly.

Example:

```bash
python3 skills/infinity-poke-recipe-generator/scripts/generate_mvp.py \
  --idea "Expiry Ping" \
  --slug expiry-ping \
  --out recipes/poke/expiry-ping
```

Then run a publish-readiness verdict and refine the generated files.
