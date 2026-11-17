## Description:

Organizes emails or messages into four reviewable action views: reply, waiting, follow-up, and archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and productivity-focused agents use this skill to turn inbox summaries, chat snippets, and pending replies into a structured triage board. It produces reviewable next steps without sending messages, deleting content, or modifying external systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbox and message content may contain private or sensitive information.

Mitigation: Review and minimize input before use; redact sensitive material where practical.

Risk: Using an output path can overwrite a local file.

Mitigation: Choose an output path that is safe to create or replace, or run without an output path to print the report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/inbox-action-board)
- [Skill Definition](artifact/SKILL.md)
- [Output Template](artifact/resources/template.md)
- [Structured Spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown or JSON structured inbox triage report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, reviewable output organized into reply, waiting, follow-up, archive, risk, and today sections.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
