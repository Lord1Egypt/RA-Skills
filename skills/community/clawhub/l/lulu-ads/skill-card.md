## Description:

Monetize an MCP server or agent tool you're building or maintaining with disclosed sponsored slots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-the-narwhal](https://clawhub.ai/user/lulu-the-narwhal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to add disclosed sponsored slots to MCP servers or agent tools, including SDK installation, credential setup, integration patterns, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add broad external sponsored-content integration to a server.

Mitigation: Require maintainer approval before adding the remote MCP endpoint, installing SDK packages, creating a publisher account, or modifying response schemas.

Risk: API credentials are required for publisher integration.

Mitigation: Store the publisher ID and API key in environment variables or a secret manager, never hardcode the key, and pin dependencies where possible.

Risk: Sponsored fields may be inappropriate for sensitive tools or error responses.

Mitigation: Prefer per-tool opt-in, exclude sensitive tools, and verify sponsored content is not attached to error responses.

Risk: Persistent repository-level guidance could affect future agent edits.

Mitigation: Add AGENTS.md or CLAUDE.md monetization guidance only when a maintainer explicitly wants persistent project instructions.

## Reference(s):

- [Lulu Ads MCP endpoint](https://ads.getlulu.dev/mcp)
- [Lulu Ads publisher signup](https://getlulu.dev/publishers)
- [Lulu Ads publisher API](https://ads.getlulu.dev/publishers)
- [Lulu Ads documentation](https://getlulu.dev/docs.md)
- [Lulu Ads installation reference](https://ads.getlulu.dev/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP endpoint setup, SDK installation, environment-variable configuration, response schema changes, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
