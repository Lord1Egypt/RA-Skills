---
name: klik-context-receipt
description: Turn a short, redacted work update into a reviewable Context Receipt that records source, freshness, scope, authority, open questions, and a human-return condition. Use when an agent or person needs to hand off or resume work without treating stale Context as current authority.
---

# Klik Context Receipt

Use this as a **non-executing** documentation workflow. It creates a concise, human-reviewable receipt; it does not access accounts, send messages, operate tools, make commitments, or authorize action.

## Ask For Only What Is Needed

Request a short, redacted description of:

1. **Source** — The Session, note, or artifact that supports the work.
2. **Freshness** — When the source was last checked and what could invalidate it.
3. **Scope** — What the next person or agent may prepare, and what is outside scope.
4. **Authority** — Existing approval, an expiry if known, and whether new access is needed.
5. **Open questions** — The one or two facts that must be clarified before preparation continues.

Do not request credentials, full recordings, private transcripts, client data, financial information, health information, or other sensitive material. A short redacted summary is enough.

## Create The Receipt

Return this exact structure:

```markdown
## Context Receipt

**Source:** [redacted artifact or Session]
**Freshness:** [last checked time] · **Invalidators:** [what would make it stale]
**Current Context:** [two or three factual bullets]
**Allowed preparation:** [bounded draft or analysis only]
**Not authorized:** [access, judgment, commitment, or tool action not already approved]
**Open question:** [the most important missing fact]
**Return to a person when:** [new access, judgment, external commitment, or conflicting Context]
```

## Guardrails

- Treat the receipt as a review aid, not a permission grant.
- If the source is missing, stale, contradictory, or ambiguous, write that explicitly and return the decision to a person.
- “Allowed preparation” means a draft or plan for review. It never authorizes execution.
- Do not infer support for a recorder, model, provider, tool, integration, or product feature from the receipt.

## Related Klik Link

[Explore Klik's pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=context_receipt)
