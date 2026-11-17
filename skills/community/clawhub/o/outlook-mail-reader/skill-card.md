## Description:

Outlook Mail Reader helps an agent use a locally controlled Chrome browser to find, filter, jump to dates in, search, and read Outlook email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users with OpenClaw browser tooling configured use this skill to inspect Outlook inboxes, navigate by date, search messages, and read selected mail in a logged-in Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Chrome browser session that has access to Outlook mail.

Mitigation: Use a separate Chrome profile or operating-system account for Outlook, keep unrelated tabs closed, and grant access only for sessions where mailbox access is intended.

Risk: The MCP setup uses a mutable chrome-devtools-mcp dependency when installed with @latest.

Mitigation: Pin or vet the chrome-devtools-mcp package version before installing, and remove the MCP configuration when the skill is no longer needed.

## Reference(s):

- [Outlook mail](https://outlook.cloud.microsoft/mail/)
- [Outlook inbox](https://outlook.cloud.microsoft/mail/inbox)
- [ClawHub skill page](https://clawhub.ai/yuyun2000/skills/outlook-mail-reader)
- [ClawHub publisher profile](https://clawhub.ai/user/yuyun2000)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox summaries, message details, date-navigation steps, search guidance, and browser-tool troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
