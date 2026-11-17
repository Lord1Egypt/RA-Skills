## Description:

Read Apple Messages data with imsgctl: check access, list chats, inspect message history, filter by time, include attachment metadata, and watch new activity from the local data available to imsgctl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpreagan](https://clawhub.ai/user/jpreagan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and support agents use this skill to inspect local Apple Messages chats, history, attachments, and live activity when the user has authorized access to that data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose privacy-sensitive Apple Messages history, attachments, and live activity.

Mitigation: Use only with explicit user scope such as chat, date range, attachment access, and whether live monitoring is allowed; avoid broad history reads unless the user intends to expose that content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpreagan/skills/imsgctl)
- [imsgkit homepage](https://github.com/jpreagan/imsgkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or JSONL command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide live monitoring commands and attachment metadata inspection when explicitly requested.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
