## Description:

Search and read Buildium data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Buildium account users use this skill to retrieve rental owners, properties, units, and property notes from their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute a downloaded installer without verification or a clear approval step; the remote installer and hosted connector implementation were not verified.

Mitigation: Review setup before enabling the skill, install and verify the CLI separately, and connect only the Buildium account and permissions intended for OOMOL.

## Reference(s):

- [Buildium](https://www.buildium.com)
- [Buildium API documentation](https://developer.buildium.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides read actions for Buildium owners, properties, units, and property notes; action schemas are checked before requests.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
