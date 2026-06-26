# Topology supplement: 3-environment (staging → canary → production)

> This file is NOT a complete CLAUDE.md. It's a supplement to `~/.claude/skills/slim-claude-md/templates/CLAUDE.md.template`. The init-project-structure skill reads both files and merges the topology-specific sections below into the base template before substituting placeholders.

## Hard rules (topology-specific additions)

These get appended to the base "Hard rules" section:

- **Default deploy/operation target is `staging`.** Canary and production each require explicit user approval *in the current turn*. Approval for one environment does not extend to the others. Approval for one action does not extend to others.
- Never work directly on the staging, canary, or production database. Develop locally first.
- Major features must be validated on canary with production-like data before merging to main. The canary gate is non-optional for non-trivial work.
- All data-modifying scripts must run with `--dry-run` first against the target environment.
- Destructive operations (DELETE, TRUNCATE, DROP, force-push) require explicit user approval. Per-action, not per-session.
- When data fixes are needed, they must be applied to all three environments explicitly. Don't assume sync scripts will catch them — verify each environment.
- Production has live customer data. Read-only by default.

## Branch → environment topology table

Replaces the placeholder `## Branch → environment topology` section in the base template:

```
develop ──► staging ──► canary ──► main
(local)     (Railway)   (Railway)   (Railway production)
                        [validate]
```

| Branch  | Env        | Auto-deploy | Notes                                       |
|---------|------------|-------------|---------------------------------------------|
| develop | local      | no          | Docker / dev DB                             |
| staging | Railway    | yes         | integration testing — default target        |
| canary  | Railway    | yes         | pre-production validation with prod data    |
| main    | Railway    | yes (LIVE)  | production — explicit approval to push      |

(Connection strings → `CLAUDE.local.md`)

**Release process:**

```bash
git checkout develop                                   # work locally
git checkout staging && git merge develop && git push  # deploy to staging — default target
git checkout canary  && git merge staging && git push  # deploy to canary — explicit approval
# validate on canary with production-like data
git checkout main    && git merge canary  && git push  # deploy to production — explicit approval
```

**Major feature rollout process** (for significant changes — schema migrations, new dependencies, integrations):

1. Implement and test on staging
2. Sync data from production to canary if needed (so canary has realistic data)
3. Validate the feature end-to-end on canary
4. Merge to main only after canary validation passes

The canary gate exists because production has live customer data. Skipping it for "simple changes" is the most common way to break production — if you're tempted to skip, that's a signal the change is bigger than you think.
