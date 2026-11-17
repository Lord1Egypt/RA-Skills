## Description:

Relationship intelligence for OpenClaw that detects outreach signals, scores and ranks them, and prepares multilingual tone-aware drafts while requiring final user approval before anything is sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abderrahman-jalled](https://clawhub.ai/user/abderrahman-jalled)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to find timely relationship outreach opportunities across user-provided context, rank them by evidence and appropriateness, and prepare work or personal message drafts in an appropriate tone and language. It is designed for relationship maintenance, not sales pipelines, lead generation, or CRM data entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze sensitive relationship context such as calendars, messages, contact notes, or shared social pages.

Mitigation: Use it only with context the user intentionally provides or connects, and avoid retaining data beyond the session unless explicitly configured.

Risk: Drafts may contain incorrect inferred language, relationship context, personal details, or cultural assumptions.

Mitigation: Require user review of every draft, flag low-confidence evidence, and ask before drafting when language, relationship stream, or cultural background is unclear.

Risk: Work-only and personal-only context could be mixed in a way that over-personalizes outreach or exposes private details.

Mitigation: Keep work and personal streams separate, ask when the stream is unclear, and use only details appropriate to the selected channel.

Risk: Sensitive situations such as layoffs, health issues, breakups, deaths, financial matters, or legal matters can make outreach inappropriate.

Mitigation: Ask before drafting for sensitive situations and omit sensitive details unless the user explicitly instructs otherwise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abderrahman-jalled/skills/improve-relationships)
- [Metadata homepage](https://github.com/Abderrahman-Jalled/improve-relationships)
- [Skill definition](artifact/SKILL.md)
- [Digest template](artifact/templates/digest.md)
- [Professional outreach template](artifact/templates/outreach_professional.md)
- [Personal outreach template](artifact/templates/outreach_personal.md)
- [Ritual and cultural occasion template](artifact/templates/rituals.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown relationship digests, ranked opportunity summaries, watching tables, and draft outreach messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output; messages require user review and approval before sending.]

## Skill Version(s):

0.2.2 (source: server release evidence; artifact metadata lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
