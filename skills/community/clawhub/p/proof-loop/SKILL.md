---
name: proof-loop
description: "Run evidence-gated coding sprints with frozen ACs, separated builder/verifier roles, and durable proof artifacts."
metadata:
  version: "0.2.1"
---
# Proof Loop

A sprint is not done until every acceptance criterion has a PASS verdict from a fresh verifier session.

Read `references/workflow.md` for the full loop spec.
Read `references/brief-template.md` for the agent brief format.
Read `references/artifacts.md` for the artifact schema.
Read `references/loopsmith-bridge.md` when deciding whether a repeated Proof Loop failure should become a Loopsmith eval case.


## Activation and Safety Boundaries

Use this skill only when the user explicitly asks for Proof Loop, proof artifacts, acceptance-criterion verification, fresh verifier separation, or an evidence-gated coding sprint. Do not activate it for ordinary code edits where the user did not request this protocol.

Proof Loop may create or update files under `.agent/tasks/<TASK_ID>/` in the current repository. Confirm the task id and repository root before creating artifacts. Do not publish artifacts, run remote validation, change repository permissions, moderate users, request full-access sandboxing, or touch credentials unless the user explicitly asks for that separate action in the current conversation.

Run helper scripts with the least privilege available. If a command could modify source files outside `.agent/tasks/<TASK_ID>/`, ask first and record the command in the evidence artifact.

## The Loop

```
spec freeze -> build -> evidence -> FRESH verify -> fix -> FRESH verify
                                         ^                      |
                                         |______________________|
                                         (repeat until all ACs = PASS)
```

## Four Roles — Always Separate

| Role | Does | Never |
|------|------|-------|
| **Spec-Freezer** | Writes spec.md with explicit ACs | Edits production code |
| **Builder** | Implements against frozen spec | Verifies own work |
| **Verifier** | Fresh session — verdicts each AC | Edits production code |
| **Fixer** | Minimal fix for what verifier flagged | Signs off on completion |

**The verifier is always a fresh session.** The agent that built cannot judge its own work.

## Acceptance Criteria Format

Every sprint brief must include explicit ACs before build starts:

```
AC1: [specific, testable condition — not a task description]
AC2: [specific, testable condition]
AC3: [specific, testable condition]
```

Good: "AC1: A German-locale user sees all prompt form field labels in German"
Bad: "AC1: Translate the form fields"

## Helper Scripts

Use these when the repository has the `proof-loop` folder available:

```bash
python3 scripts/init_task.py TASK_ID --title "Task title"
python3 scripts/check_task.py .agent/tasks/TASK_ID
```

`check_task.py` is the mechanical done gate. It returns success only when the verifier artifacts show every AC as PASS and no open problems remain.

## Sprint is DONE Only When

- Every AC has a PASS verdict in the verifier's `verdict.json`
- No problems remain in `problems.md`
- Full regression suite passes (if applicable)

## Artifacts (stored in repo)

```
.agent/tasks/<TASK_ID>/
  spec.md         -- frozen ACs + constraints + non-goals
  verdict.json    -- AC verdicts per phase (PASS/FAIL/UNKNOWN)
  problems.md     -- specific failures with file/line refs (if any)
```

See `references/artifacts.md` for schemas.
