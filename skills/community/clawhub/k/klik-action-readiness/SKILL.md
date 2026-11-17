---
name: klik-action-readiness
description: Turn a proposed AI follow-through step into a compact Action Readiness Card that makes source, freshness, scope, authority, expected result, and human-return conditions explicit. Use before preparing a consequential next step from remembered Context.
---

# Klik Action Readiness

Use this as a **non-executing** review workflow. It creates a compact Action Readiness Card; it does not access accounts, run tools, send messages, make commitments, or authorize execution.

## Ask For Only What Is Needed

Request a short, redacted description of:

1. **Source** — Which Session, note, or artifact supports the proposed step?
2. **Freshness** — When was the source last checked, and what could invalidate it?
3. **Scope** — What preparation is requested, and what is explicitly out of scope?
4. **Authority** — Which existing approval applies, for whom, and until when?
5. **Expected result** — What observable result would show the preparation is useful?
6. **Impact** — Would the step require new access, material judgment, or an external commitment?

Do not request credentials, full recordings, private transcripts, client data,
financial information, health information, or other sensitive material. A
short redacted summary is enough.

## Create The Card

Return this exact structure:

```markdown
## Action Readiness Card

**Readiness:** Ready to prepare | Refresh Context | Return to a person
**Source:** [redacted artifact or Session]
**Freshness:** [last checked time] · **Invalidators:** [what would make it stale]
**Allowed preparation:** [bounded draft, research, or plan only]
**Not authorized:** [access, judgment, commitment, or tool action not already approved]
**Expected result:** [observable review outcome]
**Return to a person when:** [new access, material judgment, external commitment, or conflicting Context]
```

## Decide Readiness

- Choose **Ready to prepare** only when the source, freshness, scope,
  authority, and expected result are clear. This permits a reviewable draft or
  plan only; it never authorizes execution.
- Choose **Refresh Context** when the source is missing, stale, contradictory,
  incomplete, or insufficiently traceable for the proposed preparation.
- Choose **Return to a person** when the work needs new access, material
  judgment, an external commitment, or a decision outside the existing scope.

## Guardrails

- Treat the card as a review aid, not a permission grant.
- Preserve uncertainty rather than silently filling gaps from old Context.
- Do not infer support for a recorder, model, provider, tool, integration, or
  product feature from this workflow.
- Do not convert a status of **Ready to prepare** into an execution decision.

## Related Klik Link

[Explore Klik's pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=action_readiness)
