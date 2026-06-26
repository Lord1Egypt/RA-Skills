---
name: meta-coordinator
description: Lightweight CS and engineering issue triage with skeleton-first intake, conservative severity/category routing, ownership recommendation, no-response follow-up handling, and durable case tracking through either an issue tracker such as Linear or plain log files. Use when handling customer-reported incidents, payment confirmation delays, entitlement or permission propagation issues, billing/webhook problems, support triage, or when converting loose CS notes into structured issue records and lifecycle updates.
---

# Meta Coordinator

Turn raw CS or ops input into a durable, operationally useful issue record.

## Core workflow

1. Build the issue skeleton first.
2. Summarize and classify the issue.
3. Estimate severity conservatively.
4. Infer the most likely module.
5. Recommend a primary owner and backup owner.
6. Move the issue through NEW -> TRIAGED -> ASSIGNED -> RESOLVED.
7. If the issue is quiet, generate explicit no-response follow-up guidance.
8. Keep a durable handling record either in an issue tracker or in plain logs.

## Skeleton-first rule

Always start with this structure:

## Issue Skeleton
- Customer Issue:
- Reported Symptom:
- Product/Plan:
- Time First Noticed:
- Scope:
- Payment/Order Reference:
- Customer Identifier:
- Current Impact:
- Known Signals:
- Missing Critical Info:

Rules:
- Fill from explicit facts when possible.
- If unknown, write `unknown`.
- Normalize vague customer wording into short operational phrases.
- Keep it concise.

## Triage rules

Use only these states:
- NEW
- TRIAGED
- ASSIGNED
- RESOLVED

Use only these severities:
- low
- medium
- high

Use only these categories:
- bug
- incident
- support request
- data issue
- integration issue
- permission issue
- performance issue
- unknown

Guidance:
- Stay conservative when evidence is weak.
- Do not invent root cause.
- Do not present guesses as facts.
- Keep the issue at TRIAGED when ownership confidence is still low.
- Keep the issue at ASSIGNED when mitigation is in progress but impact remains.
- Move to RESOLVED only after explicit recovery confirmation.

## Facts / Guesses / Missing Info

Always separate:
- Facts
- Guesses
- Missing Info

This separation is mandatory.

## Module and ownership guidance

Use operationally useful module names, for example:
- billing-webhook
- entitlement-sync
- workspace-membership-sync
- auth-service
- worker-queue
- api-gateway
- customer-account-service

Recommend:
- 1 primary owner
- 1 backup owner

Use team-style owners when needed, such as:
- Billing Engineering
- Platform Backend Team
- Account Platform Team
- CS Operations
- Integrations Team

## No-response handling

When an issue is active and updates stop, do not silently stall.

Behavior:
- Short gap on active high-severity issue: request status check from primary owner.
- Moderate gap on active high-severity issue: include backup owner and ask for ETA, mitigation status, and customer impact.
- Long gap on active high-severity issue: recommend escalation or explicit incident coordination.
- Do not downgrade severity or clear ownership just because nobody replied.
- Do not mark RESOLVED without explicit confirmation.

For no-response follow-up, include:

## Follow-up Check
- Current State:
- Update Gap:
- Action:
- Risk:
- Suggested Follow-up:

## Durable record options

Choose one of these patterns based on the environment.

### Option A: issue tracker such as Linear
Use an issue tracker when durable collaboration, state changes, comments, and ownership visibility are needed.

Recommended tracker mapping:
- TRIAGED -> create or update issue in an intake state such as Backlog
- ASSIGNED -> move to an active state such as In Progress and add a routing/update comment
- no-response -> add follow-up comment
- RESOLVED -> move to a completed state such as Done and add resolution comment

Treat tracker/team/state/label names as environment-specific examples, not hard requirements.
Do not invent labels that do not exist in the target workspace.

### Option B: log-only management
Use log-only management when no issue tracker is available or when a lightweight local workflow is preferred.

Recommended log pattern:
- store one case record per line in `cases.jsonl`, or one markdown file per day under `cases/`
- write the initial Issue Skeleton + Quick Triage when the issue reaches TRIAGED
- append follow-up entries for ASSIGNED transitions, no-response checks, and RESOLVED updates
- keep a stable case id across updates

Suggested JSONL fields:
- case_id
- created_at
- updated_at
- source
- category
- severity
- state
- title
- skeleton
- likely_module
- primary_owner
- backup_owner
- next_actions
- notes

## Output format

Use this shape unless the user requests another format:

## Issue Skeleton
- Customer Issue:
- Reported Symptom:
- Product/Plan:
- Time First Noticed:
- Scope:
- Payment/Order Reference:
- Customer Identifier:
- Current Impact:
- Known Signals:
- Missing Critical Info:

## Quick Triage
- Summary:
- Category:
- Severity:
- State:

## Facts / Guesses / Missing Info
- Facts:
- Guesses:
- Missing Info:

## Likely Module
- Primary:
- Secondary:
- Confidence:

## Owner Suggestion
- Primary Owner:
- Backup Owner:
- Why:

## Next Actions
1.
2.
3.

## Status Move
- From:
- To:
- Reason:

## Usage examples

### Example 1 — billing incident
Input:
> Customer says payment confirmation is delayed and webhook processing seems broken since this morning.

Expected direction:
- category incident
- severity high
- likely module billing-webhook
- state NEW -> TRIAGED, then ASSIGNED once broader evidence arrives

### Example 2 — permission issue
Input:
> Paid teammate still cannot access the team workspace after payment and invitation.

Expected direction:
- category permission issue
- likely module workspace-membership-sync
- state TRIAGED first, then ASSIGNED if payment is confirmed and access propagation failure is evidenced

## References

Read these when needed:
- `references/demo-script-ko.md` for a Korean demo script
- `references/tracker-workflow.md` for issue-tracker mapping examples
- `references/log-only-workflow.md` for log-only management guidance
