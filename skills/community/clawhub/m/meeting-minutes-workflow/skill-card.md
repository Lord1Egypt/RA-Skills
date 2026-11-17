## Description:

Generate structured meeting minutes from discussion notes, optionally sync them to Feishu docs, and manage action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team leads use this skill to turn meeting notes or discussion context into formal minutes with agendas, decisions, next steps, and trackable action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting minutes can contain sensitive content that may be synced to Feishu or saved locally without clear consent.

Mitigation: Review each Feishu sync and local action-item save before execution, and confirm the intended audience and sharing settings before publishing minutes.

Risk: The documented Feishu shell command can be unsafe when populated with untrusted meeting text.

Mitigation: Do not run the command with untrusted meeting text; use a safer argument-array or file-based workflow and inspect the rendered content before execution.

## Reference(s):

- [Meeting Types Reference](references/meeting-types.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/meeting-minutes-workflow)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown meeting minutes with optional JSON action-item records and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-driven output can include meeting metadata, agendas, decisions, attachments, next steps, and action-item status fields.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
