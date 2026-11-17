## Description:

Generates meeting briefs from upcoming calendar events and agent-accessible context, including agendas, relevant background, prep checklists, time budgets, and follow-up items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Employees and professionals use this skill to prepare for meetings by turning calendar events and related agent-accessible notes, emails, and documents into concise briefing material. It helps surface context, propose agendas, identify prep tasks, and track follow-up items before or after a meeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad meeting-prep requests may cause the agent to pull unrelated calendar, email, note, or document context.

Mitigation: Specify the exact meeting and source boundaries before invoking the skill, and avoid open-ended requests that grant wider context than needed.

Risk: Generated meeting briefs may include incomplete or stale context from the accessible materials.

Mitigation: Review the brief against the source event and key documents before relying on agenda items, prep tasks, or follow-up recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/meeting-prep-sr)
- [ClawHub publisher profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style meeting brief with agenda items, context bullets, prep checklist, and follow-up notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on the agent platform's existing authorized calendar and file-access context; no separate OAuth setup is described.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter; release created 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
