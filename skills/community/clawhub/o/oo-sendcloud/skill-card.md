## Description:

Manage SendCloud account details and email templates, and send email through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

For teams that use SendCloud for email operations. Agents can check account details, manage templates, and send email through the user's connected SendCloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags setup instructions that download and run an unverified script whose contents were not inspected.

Mitigation: Use the skill only when needed, and verify the oo CLI installer and its effects before installing.

Risk: Sending email or changing and deleting templates can affect recipients or SendCloud data.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval before deletions.

## Reference(s):

- [SendCloud email API documentation](https://www.sendcloud.net/doc/email_v2/)
- [SendCloud](https://www.sendcloud.net/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API requests, Email content, Text and JSON results]

**Output Format:** [JSON action payloads and results; email content may be HTML or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read account and template data, create or update templates, send email, or delete templates.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
