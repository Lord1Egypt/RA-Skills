## Description:

Microsoft Outlook/Live.com email and calendar client via Microsoft Graph API. List, search, read, send emails. View and create calendar events. Supports device code auth for servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to operate Outlook or Live.com mailbox and calendar workflows from an agent-assisted command-line environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests persistent access to mailbox and calendar data through Microsoft Graph.

Mitigation: Use least-privilege Azure permissions, review requested OAuth scopes before authentication, protect the local token file, and revoke access if credentials or tokens are exposed.

Risk: The package declares a ./outlook executable, but the submitted artifact does not include it, so runtime behavior cannot be verified from the package.

Mitigation: Do not install or run the skill until the missing executable is supplied and reviewed against the declared behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongrebeccahhh-boop/skills/outlook-email-skill-fixed)
- [Publisher profile](https://clawhub.ai/user/dongrebeccahhh-boop)
- [Microsoft Azure Portal](https://portal.azure.com)
- [Microsoft device login](https://microsoft.com/devicelogin)
- [Microsoft account app access](https://account.microsoft.com/privacy/app-access)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide Microsoft Graph API actions that read, send, and search email or manage calendar events after user authentication.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
