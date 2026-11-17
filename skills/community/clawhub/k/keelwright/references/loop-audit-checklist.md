# Loop Audit Checklist

Use this when reviewing an EXISTING autonomous loop (a script, a workflow, an agent config).
For building new loops, see the Loop Design section in SKILL.md instead.

Walk each principle. For each: state **present / partial / missing**, cite where in the code
or config it lives (or should), and give the single most valuable fix. Lead with missing
guardrails — a loop with no budget exit or no escalation path is the highest-severity finding.

## 1. Trigger clarity
- What starts the loop? (manual, cron, webhook, event, goal)
- Is the trigger deterministic? (same input → same trigger decision)
- **Missing →** the loop may never start, or start unpredictably.

## 2. Machine-checkable "done"
- Is there a concrete success condition the agent can evaluate? (tests pass, metric threshold met)
- Is it written into the agent's prompt, not just in a doc somewhere?
- **Missing →** the loop iterates until budget exhaustion with no convergence.

## 3. Deterministic verification
- Does every iteration run a real check (tests, lint, schema, diff) — not the agent's self-report?
- Is the verifier separate from the agent? (agent can't modify the check)
- **Missing →** the agent can claim success without evidence.

## 4. All exits defined
- Success exit: verifier confirms goal → loop stops
- Failure exit: unrecoverable error / retry limit → loop stops
- Budget exit: max iterations / token cap / wall-clock timeout → loop stops
- No-progress exit: state unchanged for N iterations → loop stops
- **Missing →** any unlisted exit path becomes an infinite loop.

## 5. Escalation path
- When the goal can't be met, does the loop stop and alert a human?
- Is the alert actionable? (not just "something went wrong" but "here's what failed and why")
- **Missing →** the loop silently fails or loops forever burning budget.

## 6. Context management
- Does the loop use durable state on disk (PROGRESS.md, state file) instead of relying on chat history?
- Is there a compaction strategy for long loops? (summary, trimming, sub-agent delegation)
- **Missing →** context rot causes the model to forget earlier decisions after ~20 iterations.

## 7. Autonomy boundary
- Which actions are automated vs gated behind a human?
- Are irreversible actions (publish, delete, email, merge) always gated?
- **Missing →** the loop may take destructive actions without approval.

## Severity ordering

| Finding | Severity |
|---|---|
| No budget exit + no escalation | CRITICAL |
| Success condition not machine-checkable | CRITICAL |
| Verification is agent self-report | HIGH |
| No rate limiting on external triggers | HIGH |
| No context compaction for long loops | MEDIUM |
| Trigger not deterministic | MEDIUM |
| Autonomy boundary unclear | MEDIUM |

Report format: one finding per principle, severity-ordered, with the specific file/line
where the fix should go. Do NOT pad with principles that are already present — spend the
words on the gaps.
