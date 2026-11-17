## Description:

Retrieve Ringover call, team, user, number, group, IVR, and tag data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users of an OOMOL-connected agent can inspect Ringover call records and team resources, including users, numbers, groups, IVRs, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup can execute downloaded installer code, and the exact remote installer payload is unverified.

Mitigation: Review and approve the CLI installation separately, using a verified version.

Risk: The CLI may make undisclosed changes to other agents' skills during startup.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before running it, and use limited Ringover permissions.

## Reference(s):

- [Ringover API documentation](https://developer.ringover.com/)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON API responses and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Ringover data retrieval; results depend on the connected account's permissions.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
