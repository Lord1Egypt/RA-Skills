## Description:

Generate structured meeting minutes from templates, sync to Feishu, and track action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to turn meeting context into structured Chinese meeting minutes, including agenda, decisions, action items, and follow-up issues. It can also guide Feishu document creation and local action-item tracking when those destinations are intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting minutes may contain confidential discussion details that could be synced to Feishu or stored locally.

Mitigation: Use the skill only when the Feishu destination and local storage location are approved for the meeting content.

Risk: The Feishu sync workflow uses shell-style command guidance for meeting text.

Mitigation: Review generated commands before execution and prefer an argument-array or API-based integration that treats meeting content as data.

## Reference(s):

- [Meeting Minutes Template](artifact/references/template.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/meeting-minutes-cn)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown meeting minutes with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language meeting template with placeholders for meeting metadata, discussion notes, decisions, action items, unresolved issues, and next meeting details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
