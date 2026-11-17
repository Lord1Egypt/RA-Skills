---
name: klik-session-redaction-check
description: Turn a short, redacted Session summary into a collaboration-safe Context excerpt. Use before sharing an agent or meeting handoff when the original Session may contain private details that do not belong in the next task.
---

# Klik Session Redaction Check

Use this as a **non-executing** review workflow. It creates a safe-to-share Context excerpt; it does not access accounts, run tools, send messages, make commitments, or authorize execution.

## Ask For Only What Is Needed

Request a short, redacted Session summary and the purpose of the next handoff:

1. **Handoff purpose** — What will the next person or agent prepare?
2. **Keep** — Which facts, decisions, deadlines, or open questions are necessary for that preparation?
3. **Remove** — Which details are private, irrelevant, unverified, or outside the receiving party's scope?
4. **Authority** — What existing approval, if any, applies to sharing this Context?
5. **Freshness** — When was the summary last checked, and what could make it stale?

Do not reproduce credentials, private transcripts, contact details, or sensitive personal data. Do not request recording files, full meeting audio, client data, financial information, or health information.

## Create The Check

Return this exact structure:

```markdown
## Session Redaction Check

**Handoff purpose:** [bounded preparation only]
**Keep in Context:** [necessary source-backed facts]
**Remove or redact:** [private, irrelevant, unverified, or out-of-scope details]
**Freshness:** [last checked time] · **Invalidators:** [what could change]
**Sharing authority:** [existing approval or needs review]
**Safe next step:** [draft, research, or review only]
**Return to a person when:** [new sharing permission, conflicting Context, judgment, or external commitment]
```

## Guardrails

- Treat the output as a review aid, not a permission grant.
- If authority to share is missing or unclear, mark the Context **needs review** and return it to a person.
- Preserve the source and freshness of retained facts; do not turn an unverified summary into a decision.
- A safe next step permits a draft or analysis only. It never authorizes execution.
- Do not infer support for a recorder, model, provider, tool, integration, or product feature from this workflow.

## Related Klik Link

[Explore Klik's pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=session_redaction_check)
