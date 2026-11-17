## Description:

Connect to personal Microsoft accounts via Microsoft Graph API to manage email, calendar events, and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielithomas](https://clawhub.ai/user/danielithomas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use OfficeClaw to let an agent operate a personal Microsoft account through Microsoft Graph for Outlook mail, calendar events, and Microsoft To Do tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound email, reply, forward, calendar attendee, and delete operations can change user data or contact other people when capability gates are enabled.

Mitigation: Keep send and delete disabled unless needed, require confirmation for destructive actions, and configure recipient allowlists before enabling outbound operations.

Risk: Email attachments can expose local files if an agent is allowed to attach arbitrary paths.

Mitigation: Set OFFICECLAW_ALLOWED_ATTACHMENT_DIRS to a dedicated staging folder and only place approved files there.

Risk: Broad Microsoft Graph permissions increase the impact of misuse or agent error.

Mitigation: Grant the minimum Graph scopes needed for the workflow and prefer read-only mail and calendar scopes where possible.

## Reference(s):

- [OfficeClaw ClawHub release](https://clawhub.ai/danielithomas/skills/officeclaw)
- [OfficeClaw on GitHub](https://github.com/danielithomas/officeclaw)
- [OfficeClaw on PyPI](https://pypi.org/project/officeclaw/)
- [Microsoft Graph API](https://docs.microsoft.com/graph/)
- [Microsoft Entra app registration quickstart](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-compatible CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to use officeclaw commands and summarize Microsoft Graph results instead of exposing raw mailbox, calendar, or task data unnecessarily.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
