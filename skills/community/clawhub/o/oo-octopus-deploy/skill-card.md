## Description:

Octopus Deploy (octopus.com). Use this skill for ANY Octopus Deploy request — searching and reading data. Whenever a task involves Octopus Deploy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search and read Octopus Deploy data through their connected OOMOL account. It guides the agent through checking action schemas and issuing read requests for spaces, projects, releases, deployments, environments, tasks, and the current user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback runs remote installer scripts, and the reviewed artifact does not verify the installer or live connector implementation.

Mitigation: Require separate approval before setup and review a fixed oo CLI release, including any changes to installed agent skills.

Risk: The connected account involves credentials and Octopus deployment data handled through OOMOL.

Mitigation: Use a read-only Octopus API key and account for OOMOL's role in handling credentials and deployment data.

## Reference(s):

- [Octopus Deploy REST API documentation](https://octopus.com/docs/octopus-rest-api/getting-started)
- [Octopus Deploy](https://octopus.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command and payload guidance for read actions; it does not itself produce deployment changes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
