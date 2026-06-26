# Memory Template - GitHub Actions

Create `~/github-actions/memory.md` with this structure:

```markdown
# GitHub Actions Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
<!-- Auto-activate rules, explicit-only boundaries, and situations to stay silent -->

## Repo Context
<!-- Repos, default branches, package managers, environments, and release surfaces -->

## Workflow Defaults
<!-- Preferred triggers, permissions, matrix rules, cache strategy, and timeout baseline -->

## Security Boundaries
<!-- Protected environments, approval rules, token policy, and forbidden deploy paths -->

## Release Rules
<!-- Tag strategy, artifact promotion path, rollback owner, and publish prerequisites -->

## Failure Signatures
<!-- Repeat incidents, root causes, and the fix that worked -->

## Notes
<!-- Short reminders that improve continuity and speed -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context is still evolving | Ask only when missing details change workflow safety or correctness |
| `complete` | Stable operating baseline exists | Prioritize execution and targeted optimization |
| `paused` | User paused setup or rollout | Keep existing context and avoid new setup prompts |
| `never_ask` | User does not want setup prompts | Do not ask activation questions unless requested |

## Key Principles

- Keep memory in natural language, not raw config dumps.
- Store only context that improves workflow quality, speed, or safety.
- Update `last` after each meaningful GitHub Actions session.
- Preserve failure signatures because they prevent repeat incidents.
- Never persist secrets, tokens, or copied credentials.
