## Description:

Coolify (coolify.io). Use this skill for ANY Coolify request — reading, creating, updating, and deleting data. Whenever a task involves Coolify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Coolify projects, applications, and deployments, and to manage application lifecycle actions through their connected Coolify account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions direct the agent to run remote installer code without separate approval.

Mitigation: Install a reviewed oo CLI release yourself; do not have the agent run the remote installer automatically.

Risk: Coolify API access and state-changing actions can affect connected resources.

Mitigation: Restrict the API key to necessary resources and require confirmation for deployments and destructive operations.

## Reference(s):

- [Coolify API documentation](https://coolify.io/docs/api-reference/api/)
- [Coolify](https://coolify.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Operational guidance]

**Output Format:** [JSON connector results and concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Coolify data or change application and deployment state.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
