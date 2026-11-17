## Description:

Pilvio (pilvio.com). Use this skill for ANY Pilvio request — searching and reading data. Whenever a task involves Pilvio, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected Pilvio account can use the skill to search and read account, billing, location, and virtual-machine information through Pilvio actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs remote CLI installer scripts, whose installer and release behavior have not been verified.

Mitigation: Review setup before enabling the skill; install a verified CLI release separately and explicitly approve installation and any added agent-skill changes.

## Reference(s):

- [Pilvio homepage](https://pilvio.com/)
- [Pilvio API documentation](https://api.pilvio.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [Pilvio skill on ClawHub](https://clawhub.ai/oomol/skills/oo-pilvio)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language responses based on Pilvio read-action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON action inputs; output depends on the requested Pilvio data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
