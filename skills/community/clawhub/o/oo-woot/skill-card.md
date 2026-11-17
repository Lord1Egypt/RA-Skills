## Description:

Search Woot offers and retrieve offer details through a connected Woot account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents with a connected Woot account can list live offers and retrieve details for one or more offer IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI installation code without a clear approval step.

Mitigation: Review the installer and install the CLI yourself; require approval before making installation changes.

Risk: The CLI may automatically synchronize skills at startup.

Mitigation: Review the synchronization behavior and use OO_SKILLS_SYNC_DISABLED if you need to disable startup synchronization.

Risk: OOMOL mediates Woot requests and credentials, and the hosted backend was not verified.

Mitigation: Review the OOMOL connection and avoid sending sensitive data until you are comfortable with the service handling it.

## Reference(s):

- [Woot skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-woot)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Woot API documentation](https://developer.woot.com/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Woot offer data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only offer retrieval; batch lookup supports up to 25 unique offer IDs.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
