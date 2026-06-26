# OpenClaw Skill Growth — ClawHub Package

This is a **ClawHub-friendly wrapper** for the GitHub project:

- GitHub: https://github.com/Shuai-DaiDai/openclaw-skill-growth
- Release: https://github.com/Shuai-DaiDai/openclaw-skill-growth/releases/tag/v0.1.0

## Positioning

This package is for discovering and operating the OpenClaw Skill Growth plugin from within a skill-centric ecosystem.

The main repository is a full TypeScript plugin project, so this wrapper gives ClawHub users a cleaner entry point:
- what the project does
- when to use it
- how to install it
- how to run the main flows

## Best audience

- OpenClaw users with many skills to maintain
- people who want evidence-backed skill maintenance
- users who prefer guarded apply flows over blind self-modification
- people evaluating self-improving skill systems

## Included files

- `SKILL.md` — main skill definition for ClawHub
- `INSTALL.md` — install and run the real project
- `EXAMPLES.md` — common commands and usage paths
- `CHANGELOG.md` — package-level release note

## Suggested ClawHub metadata

- Slug: `openclaw-skill-growth`
- Display Name: `OpenClaw Skill Growth`
- Version: `0.1.0`
- Tags: `openclaw, skills, observability, self-improving, maintenance`

## Important note

This wrapper is intentionally smaller than the full GitHub repository.
It should act as the ClawHub discovery and entry surface, while GitHub remains the source of truth for the actual plugin code.

## License note

The main GitHub repository is published under **MIT**.
This ClawHub wrapper package is published separately as a lightweight entry-skill package and may use different package-level metadata for ClawHub compatibility.
