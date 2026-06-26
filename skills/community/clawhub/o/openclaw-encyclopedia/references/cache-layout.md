# `.OpenClaw-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.OpenClaw-Encyclopedia/
  docs/
    docs.openclaw.ai/
      ... cached official docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable OpenClaw notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of official OpenClaw docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://docs.openclaw.ai/tools/skills
->
.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/tools/skills.md
```

### `notes/components/`
Store environment-specific component notes here.

Suggested filenames:
- `gateway.md`
- `skills.md`
- `sessions.md`
- `automation.md`
- `messaging.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `skill-authoring.md`
- `cron-vs-heartbeat.md`
- `gateway-security-review.md`
- `session-behavior-gotchas.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
