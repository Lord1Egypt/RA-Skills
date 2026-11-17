## Description:

Use Mailsoftly to read and manage contacts and contact lists through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find, create, update, and organize Mailsoftly contacts and contact lists through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to execute downloaded installers without a clear approval step or integrity checks.

Mitigation: Review and approve the CLI installation separately; prefer a verified, pinned release and review its skill-synchronization behavior.

Risk: The connected service can access Mailsoftly contacts, and write actions can change contact data.

Mitigation: Review action details and confirm the exact payload and effect before running write actions.

## Reference(s):

- [Mailsoftly homepage](https://mailsoftly.com/)
- [Mailsoftly API documentation](https://app.mailsoftly.com/developers)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Mailsoftly ClawHub release](https://clawhub.ai/oomol/skills/oo-mailsoftly)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON action results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Mailsoftly account and the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
