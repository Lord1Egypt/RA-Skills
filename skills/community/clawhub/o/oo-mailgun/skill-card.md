## Description:

Use Mailgun to inspect domains, events, templates, and suppressions, and to send email or update account settings through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Mailgun email operations through a connected account, including reviewing account data, managing templates and suppressions, and sending email. State-changing actions require review of the intended effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer and hosted runtime were not fully verified, so setup may rely on software or services whose release and behavior have not been confirmed.

Mitigation: Review CLI installation separately and use a verified release; review the connected runtime before relying on it.

Risk: Domain verification, email sending, and other write actions can change account state or send external communications.

Mitigation: Require confirmation of the exact action and its effect before domain verification or any other write, including sending email.

## Reference(s):

- [Mailgun API documentation](https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun)
- [Mailgun](https://www.mailgun.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Mailgun connector requests and responses, with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read account data or change Mailgun state, depending on the action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
