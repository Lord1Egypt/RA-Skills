## Description:

Operates SMTP2GO through an OOMOL-connected account for email statistics, templates, sender verification, activity searches, permission checks, and email sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account operators use this skill to inspect SMTP2GO sending statistics, templates, sender verification, activity, and API-key permissions, and to send standard email through a connected account. Sending requires confirmation of the recipients and message content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic dependency setup may execute downloaded code without clear user approval and may add or update other agent skills.

Mitigation: Approve and verify the CLI separately, and check whether setup adds or updates other agent skills.

Risk: The send_email action sends email through SMTP2GO and changes account state.

Mitigation: Confirm the exact recipients and email content before sending.

## Reference(s):

- [SMTP2GO API documentation](https://apidoc.smtp2go.com/)
- [SMTP2GO website](https://www.smtp2go.com/)
- [oo CLI GitHub repository](https://github.com/oomol-lab/oo-cli)
- [SMTP2GO connection setup](https://console.oomol.com/connections/smtp2go)
- [SMTP2GO ClawHub release page](https://clawhub.ai/oomol/skills/oo-smtp2go)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected SMTP2GO account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
