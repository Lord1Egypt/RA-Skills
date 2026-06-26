# Workflow Orchestrator Examples

## 1. Website migration project with overnight blocks

### Orchestration plan
- Run a bounded pre-migration audit overnight.
- Run a recap block in the morning.
- Only schedule implementation prep after reviewing the audit.

### Blocks

#### Block A: Pre-migration audit
- Classification: Safe to schedule
- Objective: Inventory files, dependencies, config touchpoints, rollback constraints, and migration risks.
- Preconditions: Repo/filesystem access exists.
- Earliest safe run time: Tonight
- Expected output: Audit memo, risk list, proposed migration sequence
- Announce: Yes
- Follow-up: Morning recap block

Payload skeleton:
```text
Project: BOS website migration
Block: Overnight pre-migration audit
Objective: Produce a bounded migration-readiness audit.

Context:
- This is a staged migration project.
- Focus only on discovery, inventory, risks, and rollout prep.
- Assume the parent session may be gone by the time you run.

Do:
- inspect the project structure and deployment touchpoints
- identify dependencies, env/config risks, and rollback concerns
- produce a concise readiness memo with recommended next blocks

Do not:
- change production
- deploy
- delete anything
- make infra or DNS changes

Expected output:
- migration-readiness summary
- top risks
- recommended next safe block
```

#### Block B: Morning recap
- Classification: Safe to schedule
- Objective: Compress the audit output into a decision-ready summary.
- Preconditions: Audit output exists.
- Earliest safe run time: Next morning
- Expected output: Recap plus go/no-go recommendation for prep work
- Announce: Yes
- Follow-up: Manual review before risky phase

#### Block C: Implementation prep
- Classification: Needs user approval first
- Objective: Prepare non-destructive migration artifacts.
- Why not auto-schedule: Depends on audit findings and may surface meaningful tradeoffs.

## 2. CRM cleanup project

### Good sequence
1. Duplicate/rule audit
2. Cleanup proposal
3. Approved cleanup batch
4. QA pass

#### Safe blocks
- duplicate detection audit
- field normalization proposal
- post-cleanup QA report

#### Needs approval
- actual record merges
- bulk status changes
- customer-visible updates

## 3. Support-ticket follow-up chain

### Good sequence
1. Overnight ticket triage summary
2. Next-morning follow-up draft prep
3. Manual approval for customer-facing sends
4. Later status check block

#### Example safe block
- Review all open tickets in scope
- group by urgency, owner, and stale age
- draft recommended follow-up queue
- do not send anything

#### Example blocked/not safe unattended
- sending replies to customers without approval
- making refunds or commitments

## 4. Audit + recap + next-step sequence

Use this when the task is ambiguous but safe to inspect.

### Sequence
- Block A: audit current state
- Block B: recap findings and propose next steps
- Block C: prep artifacts for approved path

This pattern is strong because it creates a natural checkpoint between discovery and action.

## 5. Multi-phase project where only the first few steps are safe

### Example
A new internal dashboard project

#### Safe to pre-schedule
- requirements consolidation
- asset and dependency inventory
- README cleanup
- QA checklist drafting

#### Do not pre-schedule yet
- production writes
- live integration flips
- customer-visible release steps

### Practical rule
If later phases depend on subjective review, schedule only the first safe phase and add a recap block that explicitly recommends the next block instead of assuming it.

## Fast evaluation checklist

Use this before scheduling:
- Is the block clearly scoped?
- Can it likely finish in one run?
- Can it succeed without live approvals?
- Is it reversible or low-risk?
- Would the audit trail be clear afterward?
- Does it avoid autonomy theater?
- Should the next risky phase wait for review?

If any answer is shaky, do not schedule it yet.
