# PROJECT.md Section Templates

Use the matching template for the project type. Adapt, don't copy blindly.

## Common header (all types)

```markdown
# <Project Name> — Project Source of Truth

> Single source of truth for this project. Updated as the project evolves.

## Quick Facts
| | |
|---|---|
| **Name** | |
| **Type** | App / CLI / Web / Library / Data / Infra / Generic |
| **Stack** | |
| **Location** | |
| **Entry point** | |
| **Build/run** | |
```

## App (macOS/iOS/Flutter/Android)

- **Screens / tabs** — list each and what it does.
- **Platform & signing** — target OS, bundle id, signing identity.
- **Build & launch** — exact build command + any always-launch rule.
- **Data model** — core entities.
- **Services / layers** — what each does.
- **Key data flows** — how the main user journey works.
- **Changelog** — dated feature/fix entries.
- **Notes log** — running list of user notes, with resolution status.
- **Design decisions / gotchas** — anything code can't tell you.

## CLI / Tool

- **Commands** — every subcommand + args.
- **Install** — pip/npm/brew, PATH, wrapper scripts.
- **Config** — config file location, env vars, flags.
- **Exit codes** — what each means.
- **Changelog** + **Notes log** + **Gotchas**.

## Web / API

- **Endpoints** — method, path, purpose.
- **Ports** — dev/prod.
- **Auth** — mechanism, tokens, keys.
- **Env vars** — required, optional, secrets (placeholders only).
- **Deploy** — platform, steps, rollback.
- **Changelog** + **Notes log** + **Gotchas**.

## Library / Package

- **API surface** — public types/functions.
- **Usage** — minimal example.
- **Publish** — versioning, registry, release steps.
- **Changelog** + **Notes log** + **Gotchas**.

## Data / Pipeline

- **Sources** — where data comes from.
- **Transforms** — what processing happens.
- **Outputs** — where results go.
- **Scheduling** — cron, triggers, resume.
- **Changelog** + **Notes log** + **Gotchas**.

## Infra / Service

- **Deploy** — platform, steps.
- **Scaling** — how it scales.
- **Monitoring** — logs, alerts, health checks.
- **Backups** — what/where/how often.
- **Changelog** + **Notes log** + **Gotchas**.

## Generic

- **What it is** — purpose, audience.
- **Stack** — language, framework.
- **Build/run** — commands, config.
- **Structure** — key folders/files.
- **Decisions & gotchas**.
- **Changelog** + **Notes log**.

## Notes log format

```markdown
## Notes from <Owner> (testing log)

> Add every note here so nothing is lost. Mark resolved items when fixed.

- **YYYY-MM-DD:** <note> — status (✅ fixed / open).
```

## Changelog format

```markdown
## Changelog

### YYYY-MM-DD — <summary>
- <change> — files touched, why.
```
