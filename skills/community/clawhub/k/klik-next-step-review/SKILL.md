---
name: klik-next-step-review
description: Review a proposed AI next step and classify it as ready to prepare, clarify first, or return to a person. Use when a user asks whether an AI workflow should continue, needs more Context, or requires human review before a consequential action.
---

# Klik Next-Step Review

Use this as a **non-executing** review workflow. It assesses a proposed next step; it does not operate tools, access accounts, send messages, or make commitments.

## Scope

This is an educational companion to Klik's pre-launch direction: Sessions can become useful Context and support reviewable follow-through. It is not a statement of product availability, compatibility, performance, or autonomous authority.

## Ask For Only What Is Needed

Request a short, non-sensitive description of:

1. **Source** — What Session, note, or other material supports the proposed step?
2. **Context** — Which people, prior decisions, constraints, and relevant dates matter?
3. **Proposed step** — What would be prepared, and what outcome is expected?
4. **Authority** — Is the system already authorized to prepare this work?
5. **Impact** — Would this change access, require judgment, or create an external commitment?

Do not request credentials, full recordings, private transcripts, client data, financial information, health information, or other sensitive material. A short redacted summary is enough.

## Classify The Next Step

Choose exactly one status:

- **Return to a person** when the step needs new access, depends on a person's judgment, or would create or change an external commitment.
- **Clarify first** when the source is missing, Context is stale or incomplete, scope is ambiguous, authority is unclear, or the desired outcome cannot be inspected.
- **Ready to prepare** only when source, Context, scope, authority, and expected outcome are clear. This means a draft or plan may be prepared for review; it never authorizes execution.

## Respond With A Review Card

Use this compact format:

```markdown
## Next-Step Review

**Status:** Return to a person | Clarify first | Ready to prepare
**Why:** One concise reason tied to source, Context, scope, authority, or impact.
**Safe next move:** Draft, clarify, gather Context, or return the decision to a person.
**Open question:** The one missing fact that would most improve the review.
```

If the status is **Ready to prepare**, explicitly state that the output is a reviewable draft or plan, not an action authorization.

## Related Klik Link

[Explore Klik's pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=next_step_review)
