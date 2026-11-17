## Description:

Gmail integration - Send emails, manage labels, and automate Gmail workflows with full OAuth2 support

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send Gmail messages, list recent Gmail messages, and create Gmail labels from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that OAuth support is overstated and Gmail credentials are handled poorly.

Mitigation: Review and harden the OAuth flow and credential handling before installation, and use least-privilege Google OAuth credentials.

Risk: The skill can send email through Gmail, which may affect external recipients.

Mitigation: Require explicit user review and confirmation before sending messages.

Risk: The security evidence flags unsafe email-sending details and raw email construction.

Mitigation: Validate recipient and subject inputs and use a vetted MIME message builder before sending email.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukaizj/skills/lukaizj-gmail)
- [Publisher profile](https://clawhub.ai/user/lukaizj)
- [Homepage](https://github.com/lukaizj/gmail-integration-skill)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON tool responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
