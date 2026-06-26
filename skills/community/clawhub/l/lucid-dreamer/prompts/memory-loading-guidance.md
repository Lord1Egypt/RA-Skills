# Memory Loading Guidance

Use sectioned memory selectively.

## Load order
1. Read `memory/index.md` first.
2. Always load:
   - `memory/sections/identity.md`
   - `memory/sections/operations.md`
3. Load additional section files only when the current request needs them.

## How to choose extra sections
- Project, repo, deployment, roadmap work → `memory/sections/projects.md`
- Services, ports, cron jobs, infra debugging → `memory/sections/infrastructure.md`
- Published skills, plugins, packaging → `memory/sections/skills.md`
- Decisions, reversals, rationale → `memory/sections/decisions.md`
- Lessons learned / recurring mistakes → `memory/sections/lessons.md`
- Models, agents, routing strategy → `memory/sections/models.md`

## Rules
- Do not preload every section by default.
- If `memory/index.md` or `memory/sections/` does not exist yet, fall back to `MEMORY.md`.
- When you update a section file, also update its `Last Updated` date in `memory/index.md`.
- Prefer reading one relevant section over the whole memory set when context is narrow.
