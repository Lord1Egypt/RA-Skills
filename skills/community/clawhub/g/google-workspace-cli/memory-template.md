# Memory Template - Google Workspace CLI

Create `~/google-workspace-cli/memory.md` with this structure:

```markdown
# Google Workspace CLI Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- Auto-activate triggers for gws and Workspace API requests
- Explicit-only boundaries
- Cases where this skill must stay silent

## Environment Context
- default_account:
- fallback_account:
- tenant_type: personal | team | enterprise
- mode: inspect_only | dry_run_first | apply_allowed

## Scope Profiles
- profile name -> scopes and allowed services
- restricted scopes policy
- service account usage policy

## Change Control Defaults
- confirmation token policy
- rollback owner
- write command logging requirements

## Open Risks
- unresolved auth issues
- API enablement gaps
- policy or compliance blockers

## Notes
- stable command templates
- recurring failure signatures and fixes

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep refining boundaries and templates |
| `complete` | Stable operating baseline | Focus on optimization and reliability |
| `paused` | User paused this workflow | Keep context read-only until resumed |
| `never_ask` | User does not want setup prompts | Do not ask integration questions unless requested |

## Companion Templates

Create `~/google-workspace-cli/command-log.md` with:
- command template
- required placeholders
- expected output fields
- known side effects

Create `~/google-workspace-cli/change-control.md` with:
- command id
- dry-run evidence
- confirmation token
- rollback notes
