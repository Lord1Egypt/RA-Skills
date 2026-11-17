## Description:

Real-time cryptocurrency prices, network fee estimates, and Lightning Network statistics via L402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve cryptocurrency prices, network fee estimates, and Lightning Network statistics for portfolio checks, transaction planning, market-data workflows, and network health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions execute an unpinned npm package.

Mitigation: Pin the package to a reviewed exact version before installing or deploying the MCP server.

Risk: Package names, tool names, and environment variables differ across the artifact files.

Mitigation: Confirm the authoritative package name and base URL environment variable, then align client configuration before use.

Risk: Tool calls contact an external crypto API and may incur L402 micropayment charges.

Mitigation: Review pricing and trust the API provider before enabling the skill in cost-sensitive or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-crypto-data)
- [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures)
- [Nautdev API base URL](https://api.nautdev.com)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text containing JSON-formatted cryptocurrency API results or JSON-formatted error objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls contact an external crypto API and may involve metered L402 micropayments.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
