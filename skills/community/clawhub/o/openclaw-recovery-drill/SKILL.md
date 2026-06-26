---
name: openclaw-recovery-drill
description: This skill should be used when the user asks to test OpenClaw recovery readiness, rehearse backup/restore, run a disaster-recovery drill, validate operator recovery playbooks, check restore confidence before upgrades, or prove that backups are actually restorable instead of merely existing.
---

# OpenClaw Recovery Drill

Use this skill to verify that an OpenClaw deployment can be recovered under pressure.

## Goal
Shift the conversation from “we have backups” to “we can recover reliably within an acceptable time.”

## Workflow
1. Identify the target workspace and any known backup roots.
2. Run the bundled drill script.
3. Review the readiness score, gaps, and proposed drill plan.
4. If the result is `FAIL`, treat it as an operator-readiness problem, not a documentation problem.
5. If the user wants a live drill, execute the restore only in a safe test location first.

## Command
```bash
node {baseDir}/scripts/recovery-drill.mjs \
  --workspace /absolute/path/to/workspace \
  --backup-root /absolute/path/to/backups
```

Both flags are optional. If omitted, the script checks common OpenClaw locations.

## What the script checks
- whether candidate backup roots exist
- whether recent backup files or directories are present
- whether the workspace contains the key operator files needed for recovery
- whether restore/runbook signals exist
- whether backups look recent enough for a realistic drill
- whether the operator has clear next-step drill actions

## Output format
The script returns JSON with:
- `score`
- `verdict`
- `summary`
- `findings`
- `recommendations`
- `drillPlan`
- `evidence`

## Verdicts
- `PASS` — recovery posture looks usable for a lightweight drill
- `WARN` — partial coverage; recoverability is uncertain
- `FAIL` — backup or restore confidence is too weak to trust

## Important limits
- This is a readiness check, not proof of successful recovery by itself.
- A real drill should restore into an isolated test path and verify startup.
- Presence of backup files does not equal application-level recovery.

## References
- `{baseDir}/references/drill-checklist.md`
