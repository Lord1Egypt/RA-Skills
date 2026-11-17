## Description:

Use the Outlook connector to read, create, update, and delete Outlook data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Outlook users can use this skill to review and manage mailbox messages, folders, profile details, and mailbox settings through their connected account. It supports reading data and performing message or settings changes when the user confirms the action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code without separate consent and may introduce broader changes to agent skills through automatic synchronization.

Mitigation: Install a reviewed CLI release using a method that verifies integrity, and review whether to disable automatic skill synchronization using the oo CLI command reference.

Risk: Connected Outlook actions can send, change, or delete mailbox data.

Mitigation: Review the Outlook permissions granted to OOMOL and retain the skill's confirmation requirements for sending, changing, and deleting data.

Risk: The remote installer and hosted implementation were not verified.

Mitigation: Review the setup and CLI release before enabling the skill.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Microsoft Graph mail API overview](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview?view=graph-rest-1.0)
- [Outlook](https://www.microsoft.com/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON connector requests and responses via the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return mailbox data or change mailbox state; the skill requires confirmation for write and destructive actions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
