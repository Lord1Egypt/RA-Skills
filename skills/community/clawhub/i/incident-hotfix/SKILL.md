---
name: incident-hotfix
description: Coder-focused incident response and hotfix execution for production issues. Use when you need reproducible triage, patch/rollback decisions, CI-safe hotfix branches, evidence capture, and postmortem action tracking tied to code changes.
---

# Incident Hotfix

Use this alongside broader incident-response skills when code-level action is required.

## Workflow

1. **Classify severity** using `references/severity-matrix.md`
2. **Create hotfix branch** from current production tag/commit
3. **Reproduce and isolate** with minimal failing test
4. **Patch with rollback plan**
5. **Run focused CI checks**
6. **Capture evidence bundle**
7. **Merge + verify + postmortem actions**

## Step 1 — Create incident workspace

```bash
bash scripts/start_hotfix.sh --id INC-1234 --base main
```

This creates:
- `hotfix/INC-1234-<slug>` branch
- `docs/incidents/INC-1234/` folder
- starter files for timeline, rollback, and actions

## Step 2 — Evidence capture

```bash
bash scripts/capture_evidence.sh --id INC-1234
```

Collects into `docs/incidents/INC-1234/evidence/`:
- latest commits + diff summary
- changed files list
- local env snapshot (safe subset)
- test output logs

## Step 3 — Patch gate

Before PR/merge, ensure:
- failing case reproduced (or clearly documented)
- minimal patch scope
- rollback command documented in `ROLLBACK.md`
- focused tests pass + no new lint/type failures

## Step 4 — Postmortem actions

Use `references/action-template.md` to convert findings into concrete tasks:
- owner
- due date
- verification criteria

## Required outputs

- `docs/incidents/<id>/TIMELINE.md`
- `docs/incidents/<id>/ROLLBACK.md`
- `docs/incidents/<id>/ACTIONS.md`
- `docs/incidents/<id>/evidence/` bundle

## Notes

- Prefer smallest safe patch over broad refactor during incident.
- If root cause is uncertain, ship containment first, then permanent fix.
- Never merge hotfix without rollback path.