## Description:

Use Mailboxlayer through an OOMOL-connected account to validate an email address and retrieve quality signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users with the oo CLI signed in and Mailboxlayer connected can check an email address and review its Mailboxlayer quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup path can execute an installer that has not been inspected.

Mitigation: Review and install a verified CLI release yourself before use.

Risk: Automatic skill installation and synchronization can make broader changes to the agent environment.

Mitigation: Review the CLI's automatic skill installation and synchronization; if only Mailboxlayer access is needed, consider the documented OO_SKILLS_SYNC_DISABLED opt-out.

Risk: Email addresses submitted for validation are shared with OOMOL and Mailboxlayer.

Mitigation: Submit only email addresses you intend to share with OOMOL and Mailboxlayer.

## Reference(s):

- [Mailboxlayer API documentation](https://mailboxlayer.com/documentation)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Mailboxlayer skill page](https://clawhub.ai/oomol/skills/oo-mailboxlayer)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON Mailboxlayer validation result, with a concise text or Markdown summary when presented to the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks one email address per action and returns Mailboxlayer quality signals.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
