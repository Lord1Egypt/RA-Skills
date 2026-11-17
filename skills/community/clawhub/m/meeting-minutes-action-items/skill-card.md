## Description:

Turns meeting transcripts or documents into evidence-linked minutes, decisions, action items, risks, and open questions, with optional report exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing meeting follow-ups use this skill to summarize transcripts or documents, track decisions and action items, and export reports while identifying details that need confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts or files are sent to an external AI Skills service.

Mitigation: Use only when authorized to share the meeting content with that service.

Risk: The API key could be exposed during setup or troubleshooting.

Mitigation: Store the key in environment configuration and never paste, log, or echo the full value.

Risk: Incomplete transcripts may lead to unsupported decisions, owners, or dates.

Mitigation: Review evidence excerpts and mark unsupported details as tentative or needing confirmation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/youteacher/skills/meeting-minutes-action-items)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [Meeting minutes product documentation](https://ai-skills.open-idea.net/skills/meeting-minutes-action-items)
- [API key setup](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/API-KEY.md)
- [Requests and task polling](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/HTTP-REQUESTS.md)
- [Operations and results](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/OPERATIONS.md)
- [Evidence and human review rules](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Meeting summary and structured findings; optional Markdown, DOCX, or PDF report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence excerpts, confidence and tentative flags; exports are private to the requesting user.]

## Skill Version(s):

1.2.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
