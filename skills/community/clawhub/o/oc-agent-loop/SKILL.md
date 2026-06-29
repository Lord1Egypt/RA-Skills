---
name: oc-agent-loop
description: Keep OpenClaw maintenance tight: diagnose one issue, change one thing, validate it, then keep or revert with evidence.
---

# OpenClaw Agent Loop

Use this skill when a maintenance task is starting to sprawl and the safest move is one narrow loop: diagnose, change, validate, decide.

It keeps agent-assisted maintenance reviewable instead of letting a small fix turn into an uncontrolled refactor.

This skill is not an autonomous production updater. It keeps the loop local, bounded, and reviewable.

## Support

If this skill helps you avoid a risky restart, public leak, vague task, unsafe dependency, or untraceable conclusion, star it on ClawHub or star the [GitHub repo](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian). Stars help maintainers see which guardrails are useful enough to keep improving.

## Safety Rules

- Work on one issue or one narrow improvement at a time.
- Set a maximum of three iterations unless the maintainer explicitly raises it.
- Keep a short evidence note for each iteration: diagnosis, changed files, validation, and decision.
- Do not change credentials, deployment targets, or production state.
- Do not keep a candidate change when validation is missing or failing.

## Workflow

1. State the target behavior and the current failure.
2. List the files or commands that will be touched.
3. Make the smallest candidate change that can be validated.
4. Run syntax checks, targeted tests, and any project-specific validation command.
5. Compare before and after behavior.
6. Decide `keep`, `revise`, or `revert`.
7. Record the evidence and remaining risk.

## Inputs

- Issue description or failing command.
- Allowed file scope.
- Validation commands.
- Maximum iteration count.

## Outputs

- Candidate change summary.
- Validation output summary.
- Keep/revise/revert decision.
- Follow-up items that were deliberately left out of scope.

## Non-Goals

- No unattended production deploys.
- No broad refactors.
- No silent dependency installation.
- No changes to secrets, accounts, or environment-specific configuration.
