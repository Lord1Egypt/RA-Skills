## Description:

Use an OOMOL-connected Confluence account to read, search, create, and update Confluence content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to work with Confluence content through their OOMOL-connected account, including searching and reading pages or creating and updating them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote installer without separate user approval.

Mitigation: Manually install a pinned, verified CLI release and require approval before running installers. Review the CLI's automatic skill-installation behavior and the permissions granted to OOMOL.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Confluence](https://www.atlassian.com/software/confluence)
- [Confluence Cloud REST API documentation](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured Confluence results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read actions and user-confirmed Confluence writes.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
