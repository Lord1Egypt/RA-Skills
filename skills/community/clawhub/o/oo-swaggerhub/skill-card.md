## Description:

SwaggerHub (swagger.io). Use this skill for ANY SwaggerHub request — searching and reading data. Whenever a task involves SwaggerHub, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to search SwaggerHub and retrieve API, domain, project, and template data through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can execute unverified remote code without a separate approval step.

Mitigation: Review and explicitly approve a verified CLI installation and any additional agent skills it installs before use.

Risk: Connecting SwaggerHub entrusts OOMOL with account access and data; the remote installer and hosted implementation remain unverified.

Mitigation: Review the connection and its access before connecting an account, and use an account whose access is appropriate for the task.

## Reference(s):

- [SwaggerHub skill release](https://clawhub.ai/oomol/skills/oo-swaggerhub)
- [SwaggerHub](https://swagger.io/tools/swaggerhub/)
- [SwaggerHub API documentation](https://support.smartbear.com/swaggerhub/docs/en/swaggerhub-apis.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, YAML, Guidance]

**Output Format:** [Structured SwaggerHub data in JSON or YAML, with shell commands for connector actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search, listing, and retrieval actions]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
