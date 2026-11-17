## Description:

Turn any OpenAPI/Swagger API into CLI commands and call them. Search endpoints with BM25, check parameters, execute - no MCP server needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vakovalskii](https://clawhub.ai/user/vakovalskii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover, inspect, and call REST API endpoints from OpenAPI or Swagger specifications through the ocli command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad authenticated API calls from an agent through shell commands.

Mitigation: Use trusted OpenAPI specifications, least-privilege or read-only tokens where possible, and review commands before write or delete operations.

Risk: The setup path uses an unpinned global npm install.

Mitigation: Consider pinning or locally installing the npm package for controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vakovalskii/skills/ocli-api)
- [openapi-to-cli project](https://github.com/EvilFreelancer/openapi-to-cli)
- [ocli-api skill source referenced by issue draft](https://github.com/EvilFreelancer/openapi-to-cli/tree/main/skills/ocli-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON response handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ocli binary and user-provided OpenAPI or Swagger specifications and API credentials.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
