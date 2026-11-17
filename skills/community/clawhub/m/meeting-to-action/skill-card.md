## Description:

Convert meeting notes or transcripts into clear summaries, decisions, and action items with owners and due dates. Use when a user asks to turn a meeting recording, transcript, or notes into a follow-up plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Employees and teams use this skill to turn meeting transcripts or notes into summaries, decisions, action items with owners and due dates, and draft follow-up messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting content may contain confidential or sensitive information.

Mitigation: Review sensitivity before use and keep outputs within the user context unless explicit sharing approval is given.

Risk: Action items, owners, or due dates may be inferred incorrectly from incomplete transcripts.

Mitigation: Mark uncertain owners or due dates as tentative and review drafts before acting on them.

Risk: Optional calendar, task, transcription, or meeting-platform integrations could cause unintended sharing or system changes.

Mitigation: Use read-only or draft modes unless the user explicitly approves an action, and do not send or publish changes automatically.

## Reference(s):

- [Overview](references/overview.md)
- [Auth](references/auth.md)
- [Endpoints](references/endpoints.md)
- [Webhooks](references/webhooks.md)
- [UX](references/ux.md)
- [Troubleshooting](references/troubleshooting.md)
- [Safety](references/safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary, decision list, action-item table, open questions, and draft follow-up message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft outputs only; inferred owners or due dates should be marked tentative.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
