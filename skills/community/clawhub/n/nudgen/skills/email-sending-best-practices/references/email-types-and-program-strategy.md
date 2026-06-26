# Email Types And Program Strategy

## Choose The Right Type

- Campaign email:
  - one-off sends to a selected audience
  - good for updates, launches, and periodic newsletters
- Lifecycle email:
  - triggered by behavior or state transitions
  - good for onboarding, retention, reactivation, and nudges
- Transactional email:
  - tied to a specific user/system action
  - good for receipts, verification, reset, and account operations

Keep promotional content out of purely transactional workflows.

## Nudgen-Oriented Strategy

- Use campaigns for broad outbound messaging with explicit audience definitions.
- Use lifecycle-style sends for retention and re-engagement use cases.
- Use transactional sends for action-bound communication only.
- Keep template mode, signature selection, and sender identity consistent with intent.

## Program Design

- Design around lifecycle stages:
  - acquisition
  - onboarding
  - activation
  - retention
  - win-back
- Prefer behavior-driven triggers over arbitrary schedule when possible.
- Build stop rules so campaigns do not continue once success criteria are met.

## Measurement

- Track outcomes tied to business goals:
  - activation
  - conversions
  - retention
  - reactivation
- Pair outcome metrics with health metrics:
  - bounce, unsubscribe, complaint, and click-quality trends

## Practical Review Checklist

- chosen email type matches user expectation and policy
- campaign and lifecycle boundaries are not mixed unintentionally
- KPI definitions are explicit before rollout
- stop conditions and suppression behavior are validated
