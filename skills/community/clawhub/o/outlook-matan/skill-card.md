## Description:

Access Microsoft Outlook via Maton Gateway to read, send, and manage emails, folders, calendar events, and contacts with OAuth authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Microsoft Outlook through Maton Gateway for email, calendar, folder, connection, and contact workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables access to sensitive Outlook emails, calendar events, contacts, and folders.

Mitigation: Install only when Maton is trusted with Outlook access and use the least-privileged OAuth connection available.

Risk: The skill includes actions that can send messages or modify and delete Outlook resources.

Mitigation: Require the agent to preview outbound emails and show message, event, or contact details before modifying or deleting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/otman-ai/skills/outlook-matan)
- [Publisher Profile](https://clawhub.ai/user/otman-ai)
- [Maton](https://maton.ai)
- [Maton Connection Management](https://ctrl.maton.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with curl examples and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API key setup, OAuth connection management, Outlook request examples, query parameters, error codes, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
