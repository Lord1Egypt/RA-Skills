---
name: openclaw-cost-guard
description: This skill should be used when the user asks to reduce OpenClaw token spend, audit model and cron cost risk, prevent denial-of-wallet incidents, add budget guardrails, review expensive agent defaults, or tighten AI-agent cost governance before wider rollout.
---

# OpenClaw Cost Guard

Use this skill to identify obvious cost leaks before they turn into a denial-of-wallet problem.

## Goal
Move from “the agents work” to “the agents work within an intentional budget.”

## Workflow
1. Identify the target OpenClaw config or workspace.
2. Run the bundled cost-guard script.
3. Review expensive defaults, missing budgets, and high-risk patterns.
4. If the result is `FAIL`, stop scaling usage until cost controls are tightened.
5. Apply the narrowest guardrails that reduce spend without breaking the workflow.

## Command
```bash
node {baseDir}/scripts/cost-guard.mjs --config ~/.openclaw/openclaw.json
```

The `--config` flag is optional. If omitted, the script checks the default OpenClaw config path.

## What the script checks
- whether explicit budget signals exist
- whether default models look expensive for always-on usage
- whether browser/interactive tooling appears enabled without cost discipline
- whether token limits appear excessively large
- whether the config contains multiple high-cost patterns at once
- whether the setup needs a governance recommendation before scaling

## Output format
The script returns JSON with:
- `score`
- `verdict`
- `summary`
- `findings`
- `recommendations`
- `guardrails`
- `evidence`

## Verdicts
- `PASS` — no major lightweight cost-governance gap found
- `WARN` — spend risk exists and should be reviewed
- `FAIL` — denial-of-wallet risk is materially elevated

## Important limits
- This is a lightweight static review, not a bill-reconciliation system.
- A low-risk config can still become expensive through user behavior or external automations.
- Always verify against real provider invoices and usage telemetry.

## References
- `{baseDir}/references/cost-playbook.md`
