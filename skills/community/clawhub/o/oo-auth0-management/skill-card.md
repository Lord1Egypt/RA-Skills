## Description:

This skill guides agents in using the oo CLI to read, create, update, and delete Auth0 Management data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Auth0 administrators use this skill to inspect users, roles, and permissions, and to make approved changes through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a downloaded CLI installer whose code has not been verified.

Mitigation: Review the setup fallback before installing; use a verified CLI release or require approval before downloaded code runs.

Risk: Role and permission changes can affect access to Auth0 resources.

Mitigation: Connect only the Auth0 permissions needed and confirm the exact target and effect before write or destructive actions.

## Reference(s):

- [Auth0 Management API documentation](https://auth0.com/docs/api/management/v2)
- [Auth0](https://auth0.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Auth0 Management on ClawHub](https://clawhub.ai/oomol/skills/oo-auth0-management)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON request payloads and Auth0 API results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive operations require user confirmation.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
