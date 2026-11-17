## Description:

Search Outlook mail, read threads, manage drafts, send or reply to email, and manage calendar events via Microsoft Graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with Outlook mail, calendar events, contacts, and tasks through Microsoft Graph via ClawLink. It supports mailbox discovery, message drafting and sending, calendar coordination, and related account-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and authorize a third-party ClawLink plugin with broad Microsoft account access and no pinned plugin version in the evidence.

Mitigation: Review the ClawLink plugin and OAuth consent before installation, prefer a limited Microsoft account where possible, and document how to revoke the connected app and remove the plugin.

Risk: Email send, delete, rule, contact, and calendar write actions can materially change a user's Outlook account.

Mitigation: Preview write actions and require explicit user confirmation of the target resource and intended effect before execution, especially for send, delete, rule, and calendar operations.

Risk: The live ClawLink Outlook tool catalog may differ from examples in the skill text.

Mitigation: List and describe the live Outlook tools before unfamiliar or ambiguous calls, and treat the returned catalog and tool schemas as the source of truth.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/outlook-inbox)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=outlook-inbox)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [Microsoft Graph Mail API Overview](https://learn.microsoft.com/graph/api/resources/mail-api-overview)
- [Microsoft Graph Calendar API](https://learn.microsoft.com/graph/api/resources/calendar)
- [Microsoft Graph Message Resource](https://learn.microsoft.com/graph/api/resources/message)
- [Microsoft Graph Event Resource](https://learn.microsoft.com/graph/api/resources/event)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Microsoft Graph tool-call parameters and user-facing confirmation prompts for write actions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
