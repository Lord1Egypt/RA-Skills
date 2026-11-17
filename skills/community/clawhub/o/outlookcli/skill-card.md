## Description:

Manage personal Microsoft account email, calendar, contacts, and OneDrive tasks through the m365-cli command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhah](https://clawhub.ai/user/mrhah)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agent developers use this skill to operate a personal Outlook.com, Hotmail, or Live account from an agent workflow, including mail, calendar, OneDrive, and contact lookup tasks. It is not intended for work or school Microsoft accounts or SharePoint workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive personal email, calendar, file, and contact data.

Mitigation: Avoid exposing full email bodies, attachment contents, or credential files unless the user explicitly requests the specific content.

Risk: The skill supports account-changing actions such as sending, forwarding, deleting, uploading, sharing, and calendar updates.

Mitigation: Require user confirmation before actions that send messages, change mailbox or calendar state, upload or delete files, or share OneDrive content.

Risk: The skill examples can bypass the trusted-sender filter with --force.

Mitigation: Use the trusted-sender filter by default and bypass it only after the user approves the specific email.

Risk: OneDrive sharing can create anonymous access links.

Mitigation: Avoid anonymous sharing links unless the user explicitly wants anyone with the link to have access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrhah/skills/outlookcli)
- [m365-cli npm package](https://www.npmjs.com/package/m365-cli)
- [m365-cli command reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to run m365 commands with --json for structured output where supported.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
