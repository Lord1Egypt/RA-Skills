## Description:

Archive MCP — wraps the Internet Archive APIs (free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need to query Internet Archive information through the Pipeworx archive MCP gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client configuration executes a mutable npm dependency and discovers tools from Pipeworx at runtime.

Mitigation: Review the resolved tool list before use and pin or review the MCP bridge package where possible.

Risk: Archive queries are sent through the Pipeworx gateway.

Mitigation: Do not send private URLs, credentials, unpublished identifiers, or sensitive query content through the gateway.

Risk: Anonymous users are rate limited.

Mitigation: Plan for rate limits or use the Pipeworx sign-up path for higher limits when appropriate.

## Reference(s):

- [Pipeworx Archive Pack](https://pipeworx.io/packs/archive)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-archive)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns JSON-RPC 2.0 responses from the Pipeworx archive MCP gateway; anonymous use is rate limited.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
