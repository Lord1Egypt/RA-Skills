## Description:

Outlook Pywin32 is a pywin32-based command-line tool for local Microsoft Outlook mail, calendar, account, and folder automation.

This skill is for research and development only.

## Publisher:

[jonathanhuangfirst](https://clawhub.ai/user/jonathanhuangfirst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end-user automation agents use this skill to operate a local Outlook profile on Windows through command-line actions for mail, calendar, account, and folder management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive mailbox and calendar data from a local Outlook profile.

Mitigation: Install only on trusted machines and use explicit account settings so commands target the intended mailbox.

Risk: Mail reading can change message state by marking messages as read.

Mitigation: Review read operations before execution and avoid running them against shared or work mailboxes without approval.

Risk: Calendar creation and edit commands can change user scheduling data.

Mitigation: Verify the target account, event subject, start time, and proposed changes before running calendar-new or calendar-edit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jonathanhuangfirst/skills/outlook-pywin32)
- [Publisher Profile](https://clawhub.ai/user/jonathanhuangfirst)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command examples and structured command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Microsoft Outlook, Python 3.7+, and pywin32.]

## Skill Version(s):

0.8.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
