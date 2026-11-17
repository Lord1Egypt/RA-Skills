## Description:

The Swarm (theswarm.com). Use this skill for ANY The Swarm request — searching and reading data. Whenever a task involves The Swarm, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search and retrieve company and profile data, and to check credit usage, through a connected The Swarm account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A routine request may lead to running an unverified CLI installer without prior approval.

Mitigation: Preinstall a reviewed, version-pinned CLI and require approval before any installer fallback runs.

Risk: The connected OOMOL account mediates access to The Swarm data.

Mitigation: Review the requested action and its schema, and use an account connection authorized for the data being accessed.

## Reference(s):

- [The Swarm API Reference](https://docs.theswarm.com/docs/api-reference/introduction)
- [The Swarm](https://www.theswarm.com)
- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; action results are returned as JSON data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and its live input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
