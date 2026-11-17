## Description:

Use MailerSend to inspect domains, messages, sender identities, and templates, and to send transactional email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect MailerSend domains, messages, sender identities, and templates, and to send transactional email through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a remote CLI installer, and the downloaded installer and exact CLI release were not verified.

Mitigation: Review and approve CLI installation separately, use a verified release, and review its effects on other installed agent skills.

Risk: Connecting MailerSend gives OOMOL authorized account access and access to processed email data; sending email changes external state.

Mitigation: Keep account permissions narrow and confirm the exact email payload and effect before sending.

## Reference(s):

- [MailerSend API documentation](https://developers.mailersend.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [OOMOL MailerSend connection setup](https://console.oomol.com/connections/mailersend)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [CLI commands and JSON payloads; structured connector results with natural-language explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs should follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
