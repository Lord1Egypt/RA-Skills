## Description:

Search and read Missive contacts, conversations, organizations, teams, users, and contact books through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to retrieve Missive contacts, conversations, organizations, teams, users, and contact books from an already connected account. It returns read results for an agent to use in responding to the user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup permits unverified remote code execution, and automatic skill synchronization may make changes to other agent skills.

Mitigation: Review CLI installation separately, prefer a pinned and verified release, and consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: The remote installers and live connector implementation were not verified, while Missive access is managed through the OOMOL integration.

Mitigation: Connect only the Missive account access needed and review the integration setup before use.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Missive REST API documentation](https://missiveapp.com/docs/developers/rest-api)
- [Missive homepage](https://missiveapp.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON connector results with text summaries or guidance for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Missive information; available actions depend on the connected account's access.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
