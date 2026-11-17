## Description:

SendGrid (sendgrid.com). Use this skill for ANY SendGrid request — reading, creating, and updating data. Whenever a task involves SendGrid, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect a connected SendGrid account, review available scopes and transactional templates, and send transactional email. It provides a guided workflow that checks action schemas and asks for confirmation before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback downloads and executes CLI installation code, and installation may trigger automatic skill synchronization.

Mitigation: Review and approve CLI installation separately, including any automatic skill synchronization, and use a verified release.

Risk: Sending a transactional email creates an external communication through the connected SendGrid account.

Mitigation: Use narrowly scoped SendGrid credentials and confirm the exact email payload and effect with the user before sending.

## Reference(s):

- [SendGrid API documentation](https://www.twilio.com/docs/sendgrid/api-reference)
- [SendGrid](https://sendgrid.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [SendGrid connection setup](https://console.oomol.com/connections/sendgrid)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, Text, Guidance]

**Output Format:** [JSON API results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers account information, credential scopes, transactional template listings, and email sending; sending requires confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
