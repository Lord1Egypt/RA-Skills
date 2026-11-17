## Description:

Read and act on the user's Outlook / Microsoft 365 mailbox — mail, folders, calendar, contacts, tasks — via the Outlook REST API, using a bearer token lifted from their signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to read and manage a user's Microsoft 365 mailbox, including email, folders, calendar events, contacts, and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted curl options used with a mailbox authorization header could redirect an authenticated request if untrusted input controls request options or the API destination.

Mitigation: Keep request options and the API destination under trusted control, constrain destinations to the intended Outlook API host, and review the unresolved references before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chrischall/skills/office-outlook-mcp)
- [Outlook REST API request recipes](artifact/references/api-recipes.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands, Guidance]

**Output Format:** [Mailbox and calendar data as JSON or concise text; setup and request guidance as Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and modify mailbox resources; handle returned message content as private user and third-party data.]

## Skill Version(s):

0.13.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
