# Topology supplement: 2-environment (staging → production)

> This file is NOT a complete CLAUDE.md. It's a supplement to `~/.claude/skills/slim-claude-md/templates/CLAUDE.md.template`. The init-project-structure skill reads both files and merges the topology-specific sections below into the base template before substituting placeholders.

## Hard rules (topology-specific additions)

These get appended to the base "Hard rules" section:

- **Default deploy/operation target is `staging`.** Production requires explicit user approval *in the current turn*. Approval for one action does not extend to others.
- Never work directly on the staging or production database. Develop locally first against the local Docker / SQLite / dev DB.
- All data-modifying scripts must run with `--dry-run` first against the target environment. Review the diff before executing without `--dry-run`.
- Destructive operations (DELETE, TRUNCATE, DROP, force-push) require explicit user approval. Approval is per-action, not per-session.
- Production has live customer data. Read-only by default.

## Branch → environment topology table

Replaces the placeholder `## Branch → environment topology` section in the base template:

```
develop ──► staging ──► main
(local)     (Railway)   (Railway production)
```

| Branch  | Env        | Auto-deploy | Notes                                  |
|---------|------------|-------------|----------------------------------------|
| develop | local      | no          | Docker / dev DB                        |
| staging | Railway    | yes         | integration testing — default target   |
| main    | Railway    | yes (LIVE)  | production — explicit approval to push |

(Connection strings → `CLAUDE.local.md`)

**Release process:**

```bash
git checkout develop                                   # work locally, test against dev DB
git checkout staging && git merge develop && git push  # deploy to staging — happens by default
git checkout main && git merge staging && git push     # deploy to production — needs explicit approval
```

For non-trivial features, validate on staging for at least one full session before merging to main.
