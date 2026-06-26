# Memory Index

Generated from `MEMORY.md` on YYYY-MM-DD by `scripts/migrate_memory.py`.

Read this file first. Always load `sections/identity.md` and `sections/operations.md`, then load other section files only when the task needs them.

| Section | File | Description | Last Updated | Default Load |
|---|---|---|---|---|
| Identity | sections/identity.md | Personal identity, household context, and stable human facts. | YYYY-MM-DD | always |
| Operations | sections/operations.md | Operational policy, cron jobs, workflows, and maintenance rules. | YYYY-MM-DD | always |
| Projects | sections/projects.md | Active projects, repos, URLs, and current project state. | YYYY-MM-DD | on-demand |
| Infrastructure | sections/infrastructure.md | Servers, services, ports, paths, and infrastructure facts. | YYYY-MM-DD | on-demand |
| Decisions | sections/decisions.md | Key decisions, reversals, and rationale worth keeping. | YYYY-MM-DD | on-demand |
| Lessons | sections/lessons.md | Durable technical lessons learned. | YYYY-MM-DD | on-demand |
| Models | sections/models.md | Model choices, providers, agents, and routing notes. | YYYY-MM-DD | on-demand |
| Skills | sections/skills.md | Published skills, plugins, and package metadata. | YYYY-MM-DD | on-demand |

## Maintenance Notes

- Update `Last Updated` whenever a section file changes.
- Keep descriptions short and explicit so agents know what to load.
- Add new rows when you introduce new section files.
