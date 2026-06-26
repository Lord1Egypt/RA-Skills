# ClawHub Publish Checklist

## Preflight

1. Confirm skill root contains `SKILL.md`.
2. Confirm frontmatter includes:
   - `name`
   - `description`
3. Confirm no secret values are hardcoded in skill files.

## Local Validation

```bash
openclaw skills list
openclaw skills info cortex-memory
openclaw skills check
```

Optional plugin validation:

```bash
openclaw plugins list
openclaw plugins inspect openclaw-cortex-memory
```

## Publish

```bash
clawhub login
clawhub whoami
clawhub publish ./skills/cortex-memory --slug cortex-memory --name "Cortex Memory" --version 0.1.0 --changelog "Initial ClawHub release" --tags latest
```

## Install Test (Clean Workspace)

```bash
openclaw skills install cortex-memory
openclaw skills info cortex-memory
```

## Post Publish

1. Start a new session.
2. Trigger retrieval workflow with a memory-related prompt.
3. Verify skill appears and is eligible in `openclaw skills list --eligible`.
